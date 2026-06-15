#!/usr/bin/env python3
"""shooting_star_bearish_reversal -- Shooting Star / Hammer single-candle reversal. je-suis-tm Python."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "shooting_star_bearish_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "open, high, low, close, ema20",
    "long": "Hammer: long lower shadow >= 2x body, tiny upper shadow, body > 0, close < ema20",
    "short": "Shooting Star: long upper shadow >= 2x body, tiny lower shadow, body > 0, close > ema20",
    "desc": "Shooting Star / Hammer single-candle reversal with EMA20 trend context filter",
    "source": "je-suis-tm/quant-trading (Python backtest); inverted hammer study",
}


def signal(ind, pos, htf=None):
    """Detect shooting star (short) or hammer (long) candlestick patterns."""
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    e20 = ind["ema20"][pos]
    if nan(o, h, lo, c, e20):
        return None
    body = abs(c - o)
    if body == 0:
        return None
    upper_shd = h - max(c, o)
    lower_shd = min(c, o) - lo
    # Shooting Star: bearish reversal after uptrend
    if upper_shd >= 2.0 * body and lower_shd < 0.3 * body and c > e20:
        return "short"
    # Hammer: bullish reversal after downtrend
    if lower_shd >= 2.0 * body and upper_shd < 0.3 * body and c < e20:
        return "long"
    return None
