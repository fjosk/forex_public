#!/usr/bin/env python3
"""dual_ema_value_pullback_entry -- EMA21 trending; enter on pullback where low touches EMA13 (value zone). Elder Come Into My Trading Room Ch.5.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "dual_ema_value_pullback_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema21,ema13,low,high",
    "long": "EMA21 rising AND low <= EMA13 (pullback to value near shorter EMA)",
    "short": "EMA21 falling AND high >= EMA13 (rally to value near shorter EMA)",
    "desc": "Elder dual EMA value-pullback: EMA21 sets trend direction; enter on pullback into EMA13 (value zone)",
    "source": "come_into_my_trading_room_alexander_elder Ch.5 Moving Averages Value Trades",
}


def signal(ind, pos, htf=None):
    """Trend via EMA21 slope; pullback entry when price low (or high) touches EMA13."""
    if pos < 1:
        return None
    e21 = ind["ema21"][pos]
    e21p = ind["ema21"][pos - 1]
    e13 = ind["ema13"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    if nan(e21, e21p, e13, lo, hi):
        return None
    ema_up = e21 > e21p
    ema_dn = e21 < e21p
    if ema_up and lo <= e13:
        return "long"
    if ema_dn and hi >= e13:
        return "short"
    return None
