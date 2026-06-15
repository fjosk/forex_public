#!/usr/bin/env python3
"""connors_rsi_crsi -- Connors RSI (CRSI) approximation. Larry Connors / ForexTrainingGroup.

True CRSI = (RSI(3) + RSI_streak(2) + Percentile_ROC(100)) / 3.
RSI(3) is not a direct key; approximation uses rsi2 (short-period momentum) as proxy.
Entry when rsi2 < 15 (very oversold) with sma200 trend filter.
Note: this is an approximation of CRSI using available keys only.
Source: web:https://forextraininggroup.com/ultimate-guide-to-the-connors-rsi-crsi-indicator/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_rsi_crsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "rsi2, sma200, close_sma5, close",
    "long": "CRSI approx: rsi2 < 15 (proxy for CRSI < 10/15); close > sma200",
    "short": "CRSI approx: rsi2 > 85 (proxy for CRSI > 85/90); close < sma200",
    "desc": "Connors CRSI approximation via rsi2: extreme short-period oversold/overbought with SMA200 filter",
    "source": "web:https://forextraininggroup.com/ultimate-guide-to-the-connors-rsi-crsi-indicator/",
}


def signal(ind, pos, htf=None):
    """CRSI approximation: rsi2 extreme + sma200 filter (RSI(3) unavailable; rsi2 used as proxy)."""
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    r2 = ind["rsi2"][pos]
    if nan(c, s200, r2):
        return None

    if c > s200 and r2 < 15.0:
        return "long"
    if c < s200 and r2 > 85.0:
        return "short"

    return None
