#!/usr/bin/env python3
"""ema_short_medium_htf_confirm -- EMA8 crosses EMA21 with SMA200 HTF trend filter. ReinforcedAverageStrategy."""
from strategies._common import nan, TREND_FLIP, _xup, ALL_CLASSES

META = {
    "id": "ema_short_medium_htf_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema8, ema21, sma200",
    "long": "ema8 crosses above ema21 AND close > sma200 (HTF trend proxy)",
    "short": "not used; long-only -- exit on reverse cross",
    "desc": "Short EMA cross medium EMA with SMA200 as HTF trend direction filter",
    "source": "https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/ReinforcedAverageStrategy.py",
}


def signal(ind, pos, htf=None):
    """EMA8 x EMA21 crossover with SMA200 trend filter."""
    e8 = ind["ema8"][pos]
    e8_1 = ind["ema8"][pos - 1]
    e21 = ind["ema21"][pos]
    e21_1 = ind["ema21"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(e8, e8_1, e21, e21_1, s200, c):
        return None
    if _xup(e8, e8_1, e21, e21_1) and c > s200:
        return "long"
    if _xup(e21, e21_1, e8, e8_1):
        return "short"
    return None
