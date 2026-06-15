#!/usr/bin/env python3
"""ipda_20_40_60_range -- IPDA lookback range sweep and reversal. ICT / Interbank Price Delivery Algorithm.

Price approaches or sweeps the 20-day rolling low/high (nearest IPDA target) and
closes back inside; entry in the direction of the sweep reversal.
Source: web:https://innercircletrader.net/tutorials/ict-ipda/
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "ipda_20_40_60_range",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "dc_up, dc_lo (Donchian rolling extremes), close, high, low, atr",
    "long": "daily close sweeps below 20-day low then closes back above it (body return); 40-day low not broken",
    "short": "daily close sweeps above 20-day high then closes back below it; 40-day high not broken",
    "desc": "IPDA 20/40-day lookback sweep-and-reversal",
    "source": "web:https://innercircletrader.net/tutorials/ict-ipda/",
}

# Approximate 20-day and 40-day windows on 4h bars (6 x 4h = 1 trading day)
_BARS_PER_DAY = 6
_W20 = 20 * _BARS_PER_DAY   # 120 bars
_W40 = 40 * _BARS_PER_DAY   # 240 bars


def signal(ind, pos, htf=None):
    """IPDA sweep of 20-day rolling extreme with body return; 40-day extreme not broken."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    if nan(c, lo, hi):
        return None
    if pos < _W40 + 1:
        return None

    # Rolling extremes over the prior window (exclude current bar)
    highs = ind["high"]
    lows = ind["low"]

    # 20-day range extremes (look back _W20 bars, not including current)
    lo20 = min(lows[pos - _W20: pos])
    hi20 = max(highs[pos - _W20: pos])

    # 40-day range extremes
    lo40 = min(lows[pos - _W40: pos])
    hi40 = max(highs[pos - _W40: pos])

    if nan(lo20, hi20, lo40, hi40):
        return None

    # Long: spike below 20-day low with body close back above it
    # Validity gate: 40-day low is NOT broken (body does not close below lo40)
    if lo < lo20 and c > lo20 and c > lo40:
        return "long"

    # Short: spike above 20-day high with body close back below it
    # Validity gate: 40-day high is NOT broken
    if hi > hi20 and c < hi20 and c < hi40:
        return "short"

    return None
