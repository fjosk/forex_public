#!/usr/bin/env python3
"""elder_triple_screen_scalp -- Elder 3-screen: MACD tide + Stoch wave + stoch rising entry. web:asktraders.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_triple_screen_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "macd_hist, stoch_k",
    "long": "macd_hist > 0 (tide) AND stoch_k < 20 (wave) AND stoch rising (entry)",
    "short": "macd_hist < 0 AND stoch_k > 80 AND stoch falling",
    "desc": "Elder Triple Screen scalp: MACD histogram tide + stochastic wave + stoch direction entry",
    "source": "web:https://www.asktraders.com/learn-to-trade/trading-guide/elders-triple-screening-strategy/",
}


def signal(ind, pos, htf=None):
    """MACD histogram for trend direction; stoch oversold/overbought for pullback; stoch direction for entry."""
    mh = ind["macd_hist"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    if nan(mh, stk, stk_p):
        return None
    if mh > 0 and stk < 20 and stk > stk_p:
        return "long"
    if mh < 0 and stk > 80 and stk < stk_p:
        return "short"
    return None
