#!/usr/bin/env python3
"""aroon_crossover_macd_confirm -- Aroon Up/Down threshold + MACD line crosses signal. quantifiedstrategies.com."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "aroon_crossover_macd_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "aroon_up, aroon_dn, macd, macd_sig",
    "long": "aroon_up > 70 AND aroon_dn < 30 AND MACD crosses above signal line",
    "short": "aroon_dn > 70 AND aroon_up < 30 AND MACD crosses below signal line",
    "desc": "Aroon directional strength (70/30 threshold) + MACD/signal crossover confirmation",
    "source": "web:https://www.quantifiedstrategies.com/aroon-indicator-strategy/",
}


def signal(ind, pos, htf=None):
    """Aroon directional filter + MACD line/signal crossover."""
    aup = ind["aroon_up"][pos]
    adn = ind["aroon_dn"][pos]
    mc = ind["macd"][pos]
    mcp = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    msp = ind["macd_sig"][pos - 1]
    if nan(aup, adn, mc, mcp, ms, msp):
        return None
    aroon_bull = aup > 70 and adn < 30
    aroon_bear = adn > 70 and aup < 30
    macd_cross_up = _xup(mc, mcp, ms, msp)
    macd_cross_dn = _xdn(mc, mcp, ms, msp)
    if aroon_bull and macd_cross_up:
        return "long"
    if aroon_bear and macd_cross_dn:
        return "short"
    return None
