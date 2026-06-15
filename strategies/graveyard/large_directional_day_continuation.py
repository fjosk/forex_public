#!/usr/bin/env python3
"""large_directional_day_continuation -- Large directional day (no-contrarian) continuation bias. currency_trading_for_dummies_2nd_edition_by_brian.

On a large directional bar (range >= 2*ATR AND close in top/bottom portion of range),
do NOT fade; bias continuation. Enter in the direction of the large move, exit at bar close (next bar open).
Proxy: prior bar range > 2*ATR + close in upper/lower 25% of bar range -> trend continuation.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "large_directional_day_continuation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "high,low,close,open,atr",
    "long": "prior bar range >= 2*ATR AND close in upper 25% of range AND close > open (large up-bar -> continue long)",
    "short": "prior bar range >= 2*ATR AND close in lower 25% of range AND close < open (large down-bar -> continue short)",
    "desc": "Large directional day continuation: established big directional bar -> bias continuation next bar",
    "source": "currency_trading_for_dummies_2nd_edition_by_brian, Ch8/9 anti-fade rule",
}


def signal(ind, pos, htf=None):
    """Large directional bar continuation bias."""
    if pos < 1:
        return None
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    atr = ind["atr"][pos]
    if nan(h1, l1, c1, o1, atr):
        return None
    rng1 = h1 - l1
    if rng1 < 2.0 * atr or rng1 <= 0:
        return None
    rng_pos = (c1 - l1) / rng1
    if c1 > o1 and rng_pos >= 0.75:
        return "long"
    if c1 < o1 and rng_pos <= 0.25:
        return "short"
    return None
