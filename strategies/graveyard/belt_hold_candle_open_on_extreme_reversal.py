#!/usr/bin/env python3
"""belt_hold_candle_open_on_extreme_reversal -- Single-bar reversal: bullish belt-hold opens
at/near its low and closes higher; bearish belt-hold opens at/near its high and closes lower.
J. Person, A Complete Guide to Technical Trading Tactics, Glossary."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "belt_hold_candle_open_on_extreme_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr",
    "long": "open == low (within 5% ATR) and close > open (bullish belt-hold)",
    "short": "open == high (within 5% ATR) and close < open (bearish belt-hold)",
    "desc": "Belt-hold reversal: bar opens on its extreme (low or high) and closes opposite",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Glossary 'belt-hold candle'",
}

_TOL = 0.05   # open within 5% of ATR from the extreme


def signal(ind, pos, htf=None):
    """Belt-hold: open at/near the bar extreme, close moves away from it."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    a = ind["atr"][pos]
    if nan(o, h, l, c, a):
        return None
    tol = _TOL * a
    # Bullish: open near low, close above open
    if abs(o - l) <= tol and c > o:
        return "long"
    # Bearish: open near high, close below open
    if abs(o - h) <= tol and c < o:
        return "short"
    return None
