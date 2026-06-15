#!/usr/bin/env python3
"""rate_of_change_momentum_centerline_pullback_trend_aligned -- ROC dips below zero in uptrend then ticks up (centerline pullback re-entry). Elder.

tier1 momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rate_of_change_momentum_centerline_pullback_trend_aligned",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "roc, ema50",
    "long": "EMA50 rising (trend up) AND ROC < 0 AND ROC turns up (tick up from below zero)",
    "short": "EMA50 falling (trend down) AND ROC > 0 AND ROC turns down (tick down from above zero)",
    "desc": "Elder ROC centerline pullback re-entry: dip below zero in uptrend then tick up = long",
    "source": "Elder, Trading for a Living, Sec 28 Momentum/ROC Trading Rules, Fig 28-3, p.146-148",
}


def signal(ind, pos, htf=None):
    """ROC centerline pullback aligned with EMA50 trend direction."""
    if pos < 1:
        return None
    r = ind["roc"][pos]
    r1 = ind["roc"][pos - 1]
    e = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    if nan(r, r1, e, e1):
        return None
    trend_up = e > e1
    trend_dn = e < e1
    # Centerline pullback: ROC was below zero, now ticks up, inside uptrend
    if trend_up and r < 0 and r > r1:
        return "long"
    # Centerline rally: ROC was above zero, now ticks down, inside downtrend
    if trend_dn and r > 0 and r < r1:
        return "short"
    return None
