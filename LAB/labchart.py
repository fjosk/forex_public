#!/usr/bin/env python3
"""Shared core for the two LAB chart dashboards (overlay view /lab/ + plain view /chart/).

Both views serve the same UNIFIED parquet candles the same way; only the overlay (roster/signals
routes + richer chart.js) and the static assets differ. This module owns the duplicated ~95%:
the bounded-LRU parquet candle store, the meta scan, the candle/meta handlers, gzip middleware,
the asset-version index render, and a make_base_app() factory each app wires its own
static/templates (+ optional extra routes) into.

LAB-INTERNAL: this imports pandas + reads parquet, so it must NEVER be imported by the TRADE
dashboard (which stays LAB-free and pandas-free). The unified-hub launcher mounts the two LAB
apps; this is shared only between them.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from aiohttp import web

import sys

LAB_ROOT = Path(__file__).resolve().parent
UNIFIED = LAB_ROOT / "parquet" / "unified"
WEBCORE = LAB_ROOT.parent / "webcore"   # shared design system (/shared/theme.css); for standalone dev
                                        # (under the hub, absolute /shared/* resolves to the trader parent)

sys.path.insert(0, str(LAB_ROOT.parent))   # FOREX root -> `from shared import ...`
from shared import instruments as _instr    # noqa: E402  the single instrument registry

# Display order for the dropdown comes from the instrument registry (shared/instruments.py, the ONE
# source of truth for the universe). build_meta() still scans the parquet dir for what actually
# exists; instruments not listed fall to the end, undownloaded ones simply do not appear.
INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]   # FOREX keeps 5m (sister-lab had none)
COIN_ORDER = _instr.universe()

# Bounded in-memory frame cache. 1m frames are large (BTC ~4.6M rows); cap count
# and evict oldest so browsing every coin at 1m does not leak memory.
_CACHE: dict = {}
_ORDER: list = []
_CACHE_MAX = 8
_NEED_COLS = ["open_time", "open", "high", "low", "close", "volume"]


def load_df(coin: str, interval: str):
    p = UNIFIED / coin / f"{coin}-{interval}.parquet"
    if not p.exists():
        return None
    mtime = p.stat().st_mtime          # reload when the daily cron rewrites the file
    key = (coin, interval)
    cached = _CACHE.get(key)
    if cached is not None and cached[0] == mtime:
        return cached[1]
    df = pd.read_parquet(p, columns=_NEED_COLS)
    _CACHE[key] = (mtime, df)
    _ORDER.append(key)
    while len(_ORDER) > _CACHE_MAX:
        _CACHE.pop(_ORDER.pop(0), None)
    return df


def build_meta() -> dict:
    """Scan the unified tree once: pairs, each pair's date range + bar count.
    (The spot->futures seam / MANIFEST handling below is a sister-lab carryover -- FOREX has a single
    data source and NO combine.py/MANIFEST, so `seams` is always empty and `has_backfill` is never
    set. Kept inert + harmless; do not rely on it for FOREX.)"""
    seams = {}
    man = UNIFIED / "MANIFEST.json"
    if man.exists():
        seams = json.loads(man.read_text()).get("seams", {})

    info = {}
    for coin_dir in UNIFIED.glob("*"):
        if not coin_dir.is_dir():
            continue
        coin = coin_dir.name
        ivs = [iv for iv in INTERVALS if (coin_dir / f"{coin}-{iv}.parquet").exists()]
        if not ivs:
            continue
        rec = {"intervals": ivs}
        day = coin_dir / f"{coin}-1d.parquet"
        if day.exists():
            d = pd.read_parquet(day, columns=["open_time"])
            if len(d):
                rec["start"] = int(d.open_time.iloc[0] // 1000)
                rec["end"] = int(d.open_time.iloc[-1] // 1000)
                rec["days"] = int(len(d))
        s = seams.get(coin)
        if s and s.get("spot_backfill_rows_1m"):
            rec["futures_start"] = int(s["futures_start_ms"] // 1000)
            rec["has_backfill"] = True
        info[coin] = rec

    coins = [c for c in COIN_ORDER if c in info] + [c for c in info if c not in COIN_ORDER]
    return {"intervals": INTERVALS, "coins": coins, "info": info}


async def handle_meta(request):
    return web.json_response(request.app["meta"])


async def handle_candles(request):
    q = request.query
    coin = q.get("coin", "BTCUSDT")
    interval = q.get("interval", "1h")
    if interval not in INTERVALS:
        return web.json_response({"error": "bad interval"}, status=400)
    try:
        limit = min(int(q.get("limit", 3000)), 50000)
    except ValueError:
        limit = 3000
    end = q.get("end")  # epoch seconds, optional (page backward)

    df = load_df(coin, interval)
    if df is None:
        return web.json_response({"error": "no data", "candles": []}, status=404)
    if end is not None:
        try:
            df = df[df["open_time"] <= int(end) * 1000]
        except ValueError:
            pass
    earliest = int(df["open_time"].iloc[0] // 1000) if len(df) else None
    sl = df.tail(limit)
    t = (sl["open_time"].to_numpy() // 1000).tolist()
    o = sl["open"].tolist(); h = sl["high"].tolist()
    lo = sl["low"].tolist(); c = sl["close"].tolist(); v = sl["volume"].tolist()
    candles = [{"time": t[i], "open": o[i], "high": h[i], "low": lo[i],
                "close": c[i], "volume": v[i]} for i in range(len(t))]
    return web.json_response({"candles": candles, "earliest": earliest})


@web.middleware
async def gzip_mw(request, handler):
    """Gzip every response when the client accepts it. The candle JSON (up to ~330 KB
    for 3000 bars, re-fetched on each page-backward) and signal JSON compress ~70%, the
    dominant transfer cost on this dashboard."""
    resp = await handler(request)
    if "gzip" in request.headers.get("Accept-Encoding", "") and isinstance(resp, web.Response):
        resp.enable_compression()
    return resp


def make_index_handler(static: Path, templates: Path):
    """Index handler that injects a cache-bust token (newest static-asset mtime) into the
    {{ASSET_V}} placeholders so a CSS/JS edit always reaches the client. If the template has no
    placeholder the replace is a harmless no-op."""
    async def handle_index(request):
        html = (templates / "index.html").read_text()
        v = int(max((static / "style.css").stat().st_mtime, (static / "chart.js").stat().st_mtime))
        return web.Response(text=html.replace("{{ASSET_V}}", str(v)), content_type="text/html")
    return handle_index


def make_base_app(static: Path, templates: Path, extra_get=None) -> web.Application:
    """The shared LAB chart app: gzip + meta + candles + asset-versioned index + /static.
    extra_get = list of (path, handler) the caller adds (the overlay view adds roster/signals)."""
    app = web.Application(middlewares=[gzip_mw])
    app["meta"] = build_meta()
    app.router.add_get("/", make_index_handler(static, templates))
    app.router.add_get("/api/meta", handle_meta)
    app.router.add_get("/api/candles", handle_candles)
    for path, handler in (extra_get or []):
        app.router.add_get(path, handler)
    app.router.add_static("/static/", static)
    if WEBCORE.is_dir():
        app.router.add_static("/shared/", WEBCORE)   # standalone-dev only; redundant under the hub
    return app
