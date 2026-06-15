#!/usr/bin/env python3
"""hummingbot_macd_bb_mean_reversion -- Hummingbot MACD + Bollinger Band Mean Reversion."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hummingbot_macd_bb_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "bb_pctb, macd_hist, macd",
    "long": "bb_pctb < 0.2 AND macd_hist > 0 AND macd < 0 (momentum turning from oversold)",
    "short": "bb_pctb > 0.8 AND macd_hist < 0 AND macd > 0 (momentum turning from overbought)",
    "desc": "Hummingbot V2 directional: BB %B near band extreme + MACD histogram divergence",
    "source": "hummingbot.org/blog/directional-trading-with-macd-and-bollinger-bands/",
}


def signal(ind, pos, htf=None):
    """BB %B near extreme + MACD histogram turning while MACD line still lagging."""
    pctb = ind["bb_pctb"][pos]
    mh = ind["macd_hist"][pos]
    ml = ind["macd"][pos]
    if nan(pctb, mh, ml):
        return None
    if pctb < 0.2 and mh > 0 and ml < 0:
        return "long"
    if pctb > 0.8 and mh < 0 and ml > 0:
        return "short"
    return None
