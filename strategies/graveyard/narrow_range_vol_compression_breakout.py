#!/usr/bin/env python3
"""narrow_range_vol_compression_breakout -- Narrow-range volatility compression breakout: uptrend + 5-day range <= 60% of 50-day range, then close breaks above the Donchian upper band (upside breakout). Tharp Ch.7.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "narrow_range_vol_compression_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "rng5, rng50, sma200, dc_up, dc_lo, close",
    "long": "Uptrend (close > sma200) + rng5 <= 60% of rng50 + close breaks above dc_up",
    "short": "Downtrend (close < sma200) + rng5 <= 60% of rng50 + close breaks below dc_lo",
    "desc": "Volatility compression breakout: narrow 5-day range vs 50-day, confirmed by Donchian breakout in trend direction",
    "source": "trade_your_way_to_financial_freedom -- Ch.7 Volatility / Filters vs Setups narrow-range setup",
}

_COMPRESSION_RATIO = 0.60


def signal(ind, pos, htf=None):
    """Compressed range in trend direction then close breaks Donchian."""
    c = ind["close"][pos]
    r5 = ind["rng5"][pos]
    r50 = ind["rng50"][pos]
    ma = ind["sma200"][pos]
    dcu = ind["dc_up"][pos]
    dcl = ind["dc_lo"][pos]
    if nan(c, r5, r50, ma, dcu, dcl):
        return None
    if r50 <= 0:
        return None
    compressed = r5 <= _COMPRESSION_RATIO * r50
    if not compressed:
        return None
    if c > ma and c > dcu:
        return "long"
    if c < ma and c < dcl:
        return "short"
    return None
