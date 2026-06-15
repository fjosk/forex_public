#!/usr/bin/env python3
"""cowabunga_system -- Multi-indicator EMA5/10 cross filtered by RSI, Stoch, MACD. BabyPips."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "cowabunga_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "15m/1h",
    "indicators": "ema5, ema8, rsi, stoch_k, macd_hist",
    "long": "ema5 crosses above ema8, RSI>50, stoch_k rising and <80, macd_hist positive or rising",
    "short": "ema5 crosses below ema8, RSI<50, stoch_k falling and >20, macd_hist negative or falling",
    "desc": "Cowabunga: EMA cross with RSI, Stochastic, and MACD momentum alignment",
    "source": "web:https://www.babypips.com/trading/cowabunga-system",
}


def signal(ind, pos, htf=None):
    """Cowabunga: ema5/ema8 cross confirmed by RSI, stoch direction, and MACD histogram."""
    if pos < 1:
        return None
    e5_0 = ind["ema5"][pos]
    e8_0 = ind["ema8"][pos]
    e5_1 = ind["ema5"][pos - 1]
    e8_1 = ind["ema8"][pos - 1]
    r = ind["rsi"][pos]
    sk0 = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    mh0 = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    if nan(e5_0, e8_0, e5_1, e8_1, r, sk0, sk1, mh0, mh1):
        return None

    # Long
    if (_xup(e5_0, e5_1, e8_0, e8_1)
            and r > 50
            and sk0 > sk1 and sk0 < 80
            and (mh0 > 0 or mh0 > mh1)):
        return "long"

    # Short
    if (_xdn(e5_0, e5_1, e8_0, e8_1)
            and r < 50
            and sk0 < sk1 and sk0 > 20
            and (mh0 < 0 or mh0 < mh1)):
        return "short"

    return None
