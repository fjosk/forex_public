#!/usr/bin/env python3
"""ema10_21_50_5m_trend -- EMA50 slope trend + price in EMA9/21 midpoint zone entry. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema10_21_50_5m_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema9 (proxy ema10), ema21, ema50",
    "long": "ema50 rising AND close in [ema21, ema9] midpoint zone",
    "short": "ema50 falling AND close in [ema9, ema21] midpoint zone",
    "desc": "EMA10/21/50 trend-pullback scalp: price enters the EMA midpoint zone on retracement",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies-ii/164-5-min-scalping-system/",
}


def signal(ind, pos, htf=None):
    """EMA50 slope determines trend; entry when close is inside the EMA9/21 midpoint zone."""
    if pos < 5:
        return None
    e9 = ind["ema9"][pos]
    e21 = ind["ema21"][pos]
    e50 = ind["ema50"][pos]
    e50_old = ind["ema50"][pos - 5]
    c = ind["close"][pos]
    if nan(e9, e21, e50, e50_old, c):
        return None
    trend_up = e50 > e50_old
    trend_dn = e50 < e50_old
    zone_hi = max(e9, e21)
    zone_lo = min(e9, e21)
    in_zone = zone_lo <= c <= zone_hi
    if not in_zone:
        return None
    if trend_up:
        return "long"
    if trend_dn:
        return "short"
    return None
