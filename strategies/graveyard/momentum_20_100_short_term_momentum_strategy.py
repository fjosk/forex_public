#!/usr/bin/env python3
"""momentum_20_100_short_term_momentum_strategy -- 20 EMA / 100 SMA momentum cross with MACD
confirmation: buy after price crosses above both MAs with MACD histogram recently turning positive.

Source: day_trading_swing_trading_the_currency_market_tech, pp.150-155.
"""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "momentum_20_100_short_term_momentum_strategy",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema20, sma100, macd_hist, close",
    "long": "Close crosses above both ema20 AND sma100 (price > ema20 > sma100 proxy) AND macd_hist turned positive within 5 bars",
    "short": "Close crosses below both ema20 AND sma100 AND macd_hist turned negative within 5 bars",
    "desc": "20-100 momentum strategy: dual-MA breakout confirmed by MACD histogram sign flip within 5 bars",
    "source": "day_trading_swing_trading_the_currency_market_tech pp.150-155",
}

_MACD_LOOK = 5  # bars to scan for recent MACD zero-cross


def signal(ind, pos, htf=None):
    """20EMA/100SMA cross + MACD histogram recently turned."""
    if pos < _MACD_LOOK + 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    s100 = ind["sma100"][pos]
    s100_1 = ind["sma100"][pos - 1]
    mh = ind["macd_hist"][pos]
    if nan(c, c1, e20, e20_1, s100, s100_1, mh):
        return None

    # Check if MACD hist turned positive/negative within _MACD_LOOK bars
    macd_turned_pos = False
    macd_turned_neg = False
    for k in range(1, _MACD_LOOK + 1):
        mh_k = ind["macd_hist"][pos - k]
        if nan(mh_k):
            continue
        if mh > 0 > mh_k:
            macd_turned_pos = True
        if mh < 0 < mh_k:
            macd_turned_neg = True

    # Long: close crossed above both MAs + MACD recently turned positive
    above_both = c > e20 and c > s100
    was_below = c1 <= e20_1 or c1 <= s100_1
    if above_both and was_below and macd_turned_pos:
        return "long"

    # Short: close crossed below both MAs + MACD recently turned negative
    below_both = c < e20 and c < s100
    was_above = c1 >= e20_1 or c1 >= s100_1
    if below_both and was_above and macd_turned_neg:
        return "short"

    return None
