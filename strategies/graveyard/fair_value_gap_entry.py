#!/usr/bin/env python3
"""fair_value_gap_entry -- ICT Fair Value Gap retrace entry. ICT official tutorial.

Detects the most recent unmitigated bullish or bearish FVG (three-candle imbalance)
and enters when price retraces into the gap zone. CE (50% midpoint) preferred.
Trend bias filter: use sma200_dir for context gating.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "fair_value_gap_entry",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m, 15m, 1h",
    "indicators": "high, low, close, atr, sma200_dir",
    "long": "bullish FVG (gap_lo = high[i-2] < low[i]); price retraces into zone; sma200_dir >= 0",
    "short": "bearish FVG (gap_hi = low[i-2] > high[i]); price retraces into zone; sma200_dir <= 0",
    "desc": "ICT Fair Value Gap entry: three-candle imbalance retrace at gap zone",
    "source": "web:https://innercircletrader.net/tutorials/fair-value-gap-trading-strategy/",
}

_LOOKBACK = 40


def signal(ind, pos, htf=None):
    """ICT FVG retrace entry."""
    c = ind["close"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    sma_dir = ind["sma200_dir"][pos]
    if nan(c, hi, lo, sma_dir):
        return None

    high = ind["high"]
    low = ind["low"]
    close = ind["close"]

    # Bullish FVG: gap_lo = high[i-1], gap_hi = low[i+1]
    if sma_dir >= 0:
        for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
            if i + 1 > pos:
                continue
            g_lo = high[i - 1]
            g_hi = low[i + 1]
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                continue
            mitigated = any(close[j] < g_lo for j in range(i + 1, pos) if not nan(close[j]))
            if mitigated:
                break
            if lo <= g_hi and c >= g_lo:
                return "long"
            break

    # Bearish FVG: gap_hi = low[i-1], gap_lo = high[i+1]
    if sma_dir <= 0:
        for i in range(pos - 2, max(1, pos - _LOOKBACK), -1):
            if i + 1 > pos:
                continue
            g_hi = low[i - 1]
            g_lo = high[i + 1]
            if nan(g_lo, g_hi) or g_hi <= g_lo:
                continue
            mitigated = any(close[j] > g_hi for j in range(i + 1, pos) if not nan(close[j]))
            if mitigated:
                break
            if hi >= g_lo and c <= g_hi:
                return "short"
            break

    return None
