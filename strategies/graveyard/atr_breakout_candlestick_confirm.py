#!/usr/bin/env python3
"""atr_breakout_candlestick_confirm -- ATR band breakout confirmed by engulfing candle. web:github.com/zeta-zetra."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "atr_breakout_candlestick_confirm",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h",
    "indicators": "atr, high, low, close, open",
    "long": "high > midpoint + 1.5*ATR and bullish engulfing (close > open and close > prior open, open < prior close)",
    "short": "low < midpoint - 1.5*ATR and bearish engulfing (close < open and close < prior open, open > prior close)",
    "desc": "ATR band breakout confirmed by bullish/bearish engulfing candlestick pattern (zeta-zetra)",
    "source": "web:https://github.com/zeta-zetra/code",
}

_K = 1.5


def signal(ind, pos, htf=None):
    """ATR breakout above/below midpoint +/- K*ATR, confirmed by engulfing candle."""
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    cl = ind["close"][pos]
    op = ind["open"][pos]
    cl1 = ind["close"][pos - 1]
    op1 = ind["open"][pos - 1]
    atr = ind["atr"][pos]
    if nan(hi, lo, cl, op, cl1, op1, atr):
        return None
    midpoint = (cl1 + op1) / 2.0
    upper_band = midpoint + _K * atr
    lower_band = midpoint - _K * atr
    # bullish engulfing: current bar bullish, wraps prior bar
    bull_engulf = cl > op and op <= cl1 and cl >= op1
    # bearish engulfing: current bar bearish, wraps prior bar
    bear_engulf = cl < op and op >= cl1 and cl <= op1
    if hi > upper_band and bull_engulf:
        return "long"
    if lo < lower_band and bear_engulf:
        return "short"
    return None
