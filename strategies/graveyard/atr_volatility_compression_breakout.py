#!/usr/bin/env python3
"""atr_volatility_compression_breakout -- ATR/BB width compression breakout (percentile gate). Emma Kirsten / Coding Nexus.

Waits for BB width to compress to a low percentile (bbw_pct low = squeeze), then enters the first
Donchian breakout. bbw_pct is a precomputed percentile of BB width -- a direct proxy for ATR
compression without needing a rolling-percentile of atr_pct.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "atr_volatility_compression_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "bbw_pct, dc_up, dc_lo, close",
    "long": "bbw_pct in compression (< 25th pct) AND close breaks above Donchian upper",
    "short": "bbw_pct in compression AND close breaks below Donchian lower",
    "desc": "Volatility compression breakout: BB width percentile squeeze gate + Donchian breakout trigger",
    "source": "https://medium.com/coding-nexus/atr-volatility-compression-a-winning-breakout-strategy-with-python-8aba9008a65b",
}

# bbw_pct == 0.0 means BB width is at its minimum in the lookback window (full compression).
# The precomputed key ranges 0.0 (narrowest) to 1.0 (widest). Use 0.25 as the squeeze threshold.
_SQUEEZE_THRESH = 0.25


def signal(ind, pos, htf=None):
    """BB width compression gate + Donchian breakout."""
    bwp = ind["bbw_pct"][pos]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    c = ind["close"][pos]
    if nan(bwp, dc_up, dc_lo, c):
        return None
    compression = bwp < _SQUEEZE_THRESH
    if not compression:
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
