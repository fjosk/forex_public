#!/usr/bin/env python3
"""ema_slope_trend_filter_13_day_ema -- 13-bar EMA slope sets direction; enter on pullback where price low (long) or high (short) touches the EMA. Elder Trading for a Living Sec.25.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_slope_trend_filter_13_day_ema",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema13,low,high",
    "long": "EMA13 rising AND low <= EMA13 (pullback to rising EMA)",
    "short": "EMA13 falling AND high >= EMA13 (rally to falling EMA)",
    "desc": "Elder 13-bar EMA slope trend filter with value-zone pullback entry",
    "source": "elder_alexander_trading_for_a_living Sec.25 Moving Averages Trading Rules",
}


def signal(ind, pos, htf=None):
    """EMA13 slope direction; enter when price pulls back to touch the EMA."""
    if pos < 1:
        return None
    e = ind["ema13"][pos]
    e1 = ind["ema13"][pos - 1]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    if nan(e, e1, lo, hi):
        return None
    if e > e1 and lo <= e:
        return "long"
    if e < e1 and hi >= e:
        return "short"
    return None
