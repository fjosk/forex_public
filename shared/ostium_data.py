#!/usr/bin/env python3
"""
Ostium live data client (READ-ONLY) -- the foundation for two things:
  1. displaying Ostium's own chart (OHLC candles + live ticks) in our dashboard, and
  2. driving a PAPER / forward-test engine off Ostium's LIVE mark price, so paper tracks
     what a real Ostium trade would do.

SOURCE: Ostium's public "Builder API" (https://builder.ostium.io) -- NO auth, NO wallet, NO
RPC. Verified reachable from this host (CloudFront, not ISP-blocked, no DoH shim needed).
This is the canonical real-time source: Ostium's oracle is PULL-based (on-chain price exists
only at trade execution), so live mark must come from this off-chain HTTP/WS feed, not the chain.

Endpoints (verified 2026-06-06):
  GET  /v1/prices                 -> all pairs: bid/mid/ask, isMarketOpen, schedule, timestamp
  POST /v1/ohlc                   -> OHLC candles (resolutions 1/5/15/60/240/1D, history to >=2023)
  wss://builder.ostium.io/v1/prices/stream  -> live tick stream (not used here yet; REST poll first)

MARKET HOURS: RWA pairs (FX/metals/energy) FREEZE outside their window (isMarketOpen=false, price
stuck at last close); crypto is 24/7. A paper engine MUST gate on isMarketOpen / the schedule.
"""

import requests

from shared import instruments as _instr   # the single instrument registry

BASE = "https://builder.ostium.io"

# Ostium mappings are DERIVED from the instrument registry (shared/instruments.py) so the universe
# lives in one place. The verified facts (2026-06-06) now live as registry fields:
#   PAIR_MAP      = our code -> Ostium /v1/prices name (the 14 Ostium-listed instruments).
#   NOT_ON_OSTIUM = universe codes Ostium does not list (EURJPY, USDZAR -- trade via gTrade).
#   OHLC_PAIR     = /v1/ohlc asset-name overrides where it differs from the price name
#                   (WTI prices "WTI-USD" but candles "CL-USD"; COPPER price "XCU-USD" -> candles "HG-USD").
PAIR_MAP = _instr.ostium_pair_map()
NOT_ON_OSTIUM = _instr.ostium_not_listed()
OHLC_PAIR = _instr.ostium_ohlc_overrides()

# Our interval -> Ostium OHLC resolution string.
RES_MAP = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1d": "1D"}


def get_prices(timeout=20):
    """All Ostium pairs -> {ostium_pair: {mid, bid, ask, isMarketOpen, ts}}."""
    r = requests.get(f"{BASE}/v1/prices", timeout=timeout)
    r.raise_for_status()
    out = {}
    for p in r.json().get("prices", []):
        out[p["pair"]] = {
            "mid": p.get("mid"), "bid": p.get("bid"), "ask": p.get("ask"),
            "isMarketOpen": p.get("isMarketOpen"), "ts": p.get("timestampSeconds"),
        }
    return out


def get_mark(code, timeout=20):
    """Live mark for OUR instrument code (e.g. 'EURUSD'). Returns the price dict or None if the
    instrument is not on Ostium's feed. Use for paper-trade marking (mid) + fills (bid/ask)."""
    pair = PAIR_MAP.get(code)
    if pair is None:
        return None
    return get_prices(timeout).get(pair)


def get_ohlc(code, interval, from_s, to_s, timeout=30):
    """OHLC candles for OUR code/interval over [from_s, to_s] (epoch SECONDS).
    Returns list of {open_time(ms,UTC), open, high, low, close, source='ostium'} -- shaped to
    line up with our sister-lab-schema parquet (open_time in ms). Empty list if not on Ostium."""
    pair = OHLC_PAIR.get(code) or PAIR_MAP.get(code)
    if pair is None:
        return []
    body = {"pair": pair, "fromTimestampSeconds": int(from_s),
            "toTimestampSeconds": int(to_s), "resolution": RES_MAP[interval]}
    r = requests.post(f"{BASE}/v1/ohlc", json=body, timeout=timeout)
    r.raise_for_status()
    return [{"open_time": int(c["time"]), "open": c["open"], "high": c["high"],
             "low": c["low"], "close": c["close"], "source": "ostium"}
            for c in r.json().get("data", [])]


if __name__ == "__main__":
    import sys
    px = get_prices()
    print(f"Ostium /v1/prices: {len(px)} pairs reachable")
    for code in ("EURUSD", "XAUUSD", "WTI", "NATGAS"):
        m = get_mark(code)
        print(f"  {code:8s} -> {PAIR_MAP[code]:9s} mid={m['mid']} open={m['isMarketOpen']}")
    c = get_ohlc("EURUSD", "1h", 1779000000, 1780693140)
    print(f"  EURUSD 1h candles: {len(c)}  last={c[-1] if c else None}")
