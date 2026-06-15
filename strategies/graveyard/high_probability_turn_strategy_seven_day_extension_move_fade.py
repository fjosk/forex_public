#!/usr/bin/env python3
"""high_probability_turn_strategy_seven_day_extension_move_fade -- Fade after 7 consecutive
same-direction daily candles (close < open for 7 = buy; close > open for 7 = sell).

Source: day_trading_swing_trading_the_currency_market_tech, Ch. pp.155-164.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "high_probability_turn_strategy_seven_day_extension_move_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-daily",
    "indicators": "open, close",
    "long": "7 consecutive bearish bars (close < open each): extension fade long",
    "short": "7 consecutive bullish bars (close > open each): extension fade short",
    "desc": "Seven-day extension fade: buy after 7 straight down-candles, sell after 7 straight up-candles",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch. pp.155-164",
}

_N = 7  # consecutive bars required


def signal(ind, pos, htf=None):
    """Fade after N consecutive same-direction candles."""
    if pos < _N:
        return None
    opens = ind["open"]
    closes = ind["close"]
    if nan(opens[pos], closes[pos]):
        return None

    # check last _N bars (pos-N+1 .. pos)
    all_bear = True
    all_bull = True
    for i in range(pos - _N + 1, pos + 1):
        o_i = opens[i]
        c_i = closes[i]
        if nan(o_i, c_i):
            return None
        if c_i >= o_i:
            all_bear = False
        if c_i <= o_i:
            all_bull = False

    if all_bear:
        return "long"
    if all_bull:
        return "short"
    return None
