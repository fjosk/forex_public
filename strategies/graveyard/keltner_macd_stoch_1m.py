#!/usr/bin/env python3
"""keltner_macd_stoch_1m -- Price inside Keltner + MACD hist direction + stoch extreme. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "keltner_macd_stoch_1m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "kc_lo, kc_up, sma100 (proxy sma89), macd_hist, stoch_k",
    "long": "close > sma100 AND close inside Keltner AND macd_hist < 0 AND stoch_k < 40",
    "short": "close < sma100 AND close inside Keltner AND macd_hist > 0 AND stoch_k > 60",
    "desc": "Keltner Channel + MACD histogram + Stochastic extreme 1m/5m scalp",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies/21-keltner-scalping/",
}


def signal(ind, pos, htf=None):
    """Price inside Keltner channels on the correct side of SMA100; MACD and stoch confirm direction."""
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    sma = ind["sma100"][pos]
    mh = ind["macd_hist"][pos]
    stk = ind["stoch_k"][pos]
    c = ind["close"][pos]
    if nan(kc_lo, kc_up, sma, mh, stk, c):
        return None
    in_channel = kc_lo <= c <= kc_up
    if not in_channel:
        return None
    if c > sma and mh < 0 and stk < 40:
        return "long"
    if c < sma and mh > 0 and stk > 60:
        return "short"
    return None
