#!/usr/bin/env python3
"""aroon_crossover_trend_strategy -- Aroon Up/Down crossover with strength >= 70. StockCharts.

Aroon Up crosses above Aroon Down with Aroon Up >= 70 and Aroon Down <= 30 (strong uptrend).
Aroon Down crosses above Aroon Up with Aroon Down >= 70 and Aroon Up <= 30 (strong downtrend).
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "aroon_crossover_trend_strategy",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "aroon_up, aroon_dn, atr",
    "long": "aroon_up crosses above aroon_dn with aroon_up >= 70 and aroon_dn <= 30",
    "short": "aroon_dn crosses above aroon_up with aroon_dn >= 70 and aroon_up <= 30",
    "desc": "Aroon Up/Down crossover with strong-trend confirmation (StockCharts standard)",
    "source": "web:https://chartschool.stockcharts.com aroon; Tushar Chande New Technical Trader (1994)",
}


def signal(ind, pos, htf=None):
    """Aroon cross with directional strength filter."""
    aup = ind["aroon_up"][pos]
    adn = ind["aroon_dn"][pos]
    aup1 = ind["aroon_up"][pos - 1]
    adn1 = ind["aroon_dn"][pos - 1]
    if nan(aup, adn, aup1, adn1):
        return None
    if _xup(aup, aup1, adn, adn1) and aup >= 70 and adn <= 30:
        return "long"
    if _xdn(aup, aup1, adn, adn1) and adn >= 70 and aup <= 30:
        return "short"
    return None
