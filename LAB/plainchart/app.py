#!/usr/bin/env python3
"""
FOREX offline plain chart dashboard (no strategy overlay). PORTED from sister-lab/LAB/plainchart.

Thin shell over the shared LAB chart core (labchart): candle/meta serving, parquet store, gzip,
and asset-versioned index all live there; this app only wires its own static/templates.

PORT CONVENTION (FOREX project): base 9500, increment by 10 per service (9500, 9510, 9520 ...),
chosen far from sister-lab (91xx) and BINARYOPTION (84xx/92xx). This chart dashboard = 9500.
BIND: Tailscale interface ONLY (127.0.0.1), not 0.0.0.0 -- the lab is reachable over the
tailnet, not exposed on every interface.

Run: /home/user/global-venv/bin/python3 LAB/plainchart/app.py
  Tailscale: http://127.0.0.1:9500
"""
from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # LAB root -> import labchart
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # FOREX root -> from shared import ...
import labchart                  # noqa: E402  (LAB chart core)
from shared import ostium_data   # noqa: E402  (read-only Ostium Builder API client; now in shared/)
import registry_view             # noqa: E402  (read-only backtest registry -> /results page)
import pnl_view                  # noqa: E402  (read-only trader state -> /pnl page)
from aiohttp import web          # noqa: E402

HERE = Path(__file__).resolve().parent

# entry-tf bar duration in seconds, to turn (end, limit) into a from/to window for the Ostium API.
_IV_SECS = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600, "4h": 14400, "1d": 86400}


async def handle_ostium_candles(request):
    """Serve OHLC candles from the Ostium Builder API (live), shaped like /api/candles so the
    chart's Paper/Live views can read live candles transparently. ostium_data.get_ohlc uses blocking
    requests, so it runs in a thread executor to keep the event loop free."""
    q = request.query
    coin = q.get("coin", "EURUSD")
    interval = q.get("interval", "1h")
    if interval not in ostium_data.RES_MAP:
        return web.json_response({"error": "bad interval", "candles": []}, status=400)
    if coin not in ostium_data.PAIR_MAP:   # only EUR/JPY + USD/ZAR are not on Ostium's feed
        return web.json_response({"candles": [], "earliest": None, "error": "not on Ostium"})
    try:
        limit = min(int(q.get("limit", 3000)), 50000)
    except ValueError:
        limit = 3000
    end = q.get("end")
    to_s = int(end) if end else int(time.time())
    from_s = to_s - limit * _IV_SECS[interval]
    try:
        raw = await asyncio.get_event_loop().run_in_executor(
            None, ostium_data.get_ohlc, coin, interval, from_s, to_s)
    except Exception as exc:                # upstream/network failure -> 502, never crash the handler
        return web.json_response({"error": str(exc)[:120], "candles": []}, status=502)
    candles = [{"time": c["open_time"] // 1000, "open": c["open"], "high": c["high"],
                "low": c["low"], "close": c["close"], "volume": 0} for c in raw]
    # If the fetch returned fewer than asked, we hit Ostium's history start -> mark earliest so
    # the chart stops paging backward there.
    earliest = candles[0]["time"] if (candles and len(candles) < limit) else None
    return web.json_response({"candles": candles, "earliest": earliest})


async def handle_ostium_pairs(request):
    """Our instrument codes that Ostium actually lists -- the Paper/Live views hide the rest."""
    return web.json_response({"pairs": list(ostium_data.PAIR_MAP.keys())})


async def handle_results(request):
    """The /results page: full backtest record (every gauntlet strategy). Renders results.html
    with the {{ASSET_V}} cache-bust token from results.js/style.css mtime (mirrors the index
    handler in labchart)."""
    html = (HERE / "templates" / "results.html").read_text()
    v = int(max((HERE / "static" / "style.css").stat().st_mtime,
                (HERE / "static" / "results.js").stat().st_mtime))
    return web.Response(text=html.replace("{{ASSET_V}}", str(v)), content_type="text/html")


async def handle_registry(request):
    """Backtest registry summary (one row per strategy+cadence). Empty payload when the gauntlet
    has not produced a registry yet -- the page renders a clean 'no backtests yet' state."""
    data = registry_view.summary()
    if data is None:
        return web.json_response({"meta": {"n_strategies": 0, "n_rows": 0}, "rows": []})
    return web.json_response(data)


async def handle_registry_pairs(request):
    """Per-pair breakdown for one (strategy, cadence), lazy-loaded on row expand."""
    sid = request.query.get("id", "")
    cadence = request.query.get("cadence", "")
    data = registry_view.pairs(sid, cadence)
    if data is None:
        return web.json_response({"id": sid, "cadence": cadence, "pairs": []})
    return web.json_response(data)


async def handle_pnl(request):
    """The /pnl page: Paper + Live PnL at a glance. ASSET_V cache-bust from pnl.js/style.css mtime."""
    html = (HERE / "templates" / "pnl.html").read_text()
    v = int(max((HERE / "static" / "style.css").stat().st_mtime,
                (HERE / "static" / "pnl.js").stat().st_mtime))
    return web.Response(text=html.replace("{{ASSET_V}}", str(v)), content_type="text/html")


async def handle_pnl_data(request):
    """Compact Paper + Live PnL summary (empty until the trader has written state)."""
    return web.json_response(pnl_view.summary())


def make_app() -> web.Application:
    return labchart.make_base_app(HERE / "static", HERE / "templates",
                                  extra_get=[("/api/ostium_candles", handle_ostium_candles),
                                             ("/api/ostium_pairs", handle_ostium_pairs),
                                             ("/results", handle_results),
                                             ("/api/registry", handle_registry),
                                             ("/api/registry/pairs", handle_registry_pairs),
                                             ("/pnl", handle_pnl),
                                             ("/api/pnl", handle_pnl_data)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9500)        # FOREX base port (increment 10 per service)
    ap.add_argument("--host", default="127.0.0.1")        # Tailscale interface ONLY (not 0.0.0.0)
    args = ap.parse_args()
    app = make_app()
    print(f"FOREX plain chart on http://{args.host}:{args.port}  ({len(app['meta']['coins'])} instruments)")
    web.run_app(app, host=args.host, port=args.port, print=None)


if __name__ == "__main__":
    main()
