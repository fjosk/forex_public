#!/usr/bin/env python3
"""single_ma_trend_filter_breakout -- Price crosses above/below a single MA with ADX trend filter. j_person_a_complete_guide_to_technical_trading_tac.

Buy when price (close) crosses above EMA50 AND ADX>20 (trend filter to reduce whipsaw in ranges).
Sell when price crosses below EMA50 AND ADX>20.
Note: book explicitly warns this whipsaws in choppy markets; ADX gate added as the recommended fix.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "single_moving_average_trend_filter_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema50,adx",
    "long": "close crosses above EMA50 with ADX>20 confirming trend",
    "short": "close crosses below EMA50 with ADX>20 confirming trend",
    "desc": "Single MA breakout with ADX trend filter to avoid choppy-market whipsaw",
    "source": "j_person_a_complete_guide_to_technical_trading_tac Ch8 pp135-141",
}


def signal(ind, pos, htf=None):
    """Single MA crossover gated by ADX trend filter."""
    if pos < 1:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e  = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    dx = ind["adx"][pos]
    if nan(c, c1, e, e1, dx):
        return None
    if dx < 20:
        return None
    if c > e and c1 <= e1:
        return "long"
    if c < e and c1 >= e1:
        return "short"
    return None
