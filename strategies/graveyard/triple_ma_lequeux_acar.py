#!/usr/bin/env python3
"""triple_ma_lequeux_acar -- Lequeux-Acar triple MA trend-following: price vs 3 MAs count. currency_strategy_a_practitioner_s_guide_to_curren.

Original: SMA(32), SMA(61), SMA(117). Proxied with SMA20/SMA50/SMA100 (closest available spanning short/med/long).
Long: close above ALL three MAs (full trend alignment).
Short: close below ALL three MAs.
Fires only on the bar when the count first reaches 3 (new entry into full-alignment).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "triple_ma_lequeux_acar",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,sma20,sma50,sma100",
    "long": "close above SMA20, SMA50, and SMA100 (all three, newly aligned -> full long)",
    "short": "close below SMA20, SMA50, and SMA100 (all three, newly aligned -> full short)",
    "desc": "Lequeux-Acar triple MA hedge ratio: price vs SMA20/50/100 count-3 = full trend signal",
    "source": "currency_strategy_a_practitioner_s_guide_to_curren Ch10 Sec10.10.6 lines1222-1234",
}


def signal(ind, pos, htf=None):
    """Full MA alignment (all 3) -> long or short; fire on new entry into aligned state."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    s20  = ind["sma20"][pos];  s201  = ind["sma20"][pos - 1]
    s50  = ind["sma50"][pos];  s501  = ind["sma50"][pos - 1]
    s100 = ind["sma100"][pos]; s1001 = ind["sma100"][pos - 1]
    if nan(c, c1, s20, s201, s50, s501, s100, s1001):
        return None
    all_above      = c  > s20  and c  > s50  and c  > s100
    all_above_prev = c1 > s201 and c1 > s501 and c1 > s1001
    all_below      = c  < s20  and c  < s50  and c  < s100
    all_below_prev = c1 < s201 and c1 < s501 and c1 < s1001
    if all_above and not all_above_prev:
        return "long"
    if all_below and not all_below_prev:
        return "short"
    return None
