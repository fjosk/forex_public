#!/usr/bin/env python3
"""chandelier_exit_atr_trailing -- Chandelier Exit direction flip system. Charles Le Beau / StockCharts.

Uses the pre-computed chand_dir key: flip from -1 to +1 = long entry; flip from +1 to -1 = short.
No secondary entry signal needed; the flip IS the entry trigger (Le Beau always-in system).
Source: web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "chandelier_exit_atr_trailing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "chand_dir, atr, hh_n, ll_n",
    "long": "chand_dir flips from -1 to +1 (price broke above the short chandelier stop)",
    "short": "chand_dir flips from +1 to -1 (price broke below the long chandelier stop)",
    "desc": "Chandelier Exit always-in flip system: direction change on the chandelier trailing stop",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit",
}


def signal(ind, pos, htf=None):
    """Chandelier direction flip: chand_dir -1 -> +1 = long; +1 -> -1 = short."""
    if pos < 1:
        return None
    cd = ind["chand_dir"][pos]
    cd1 = ind["chand_dir"][pos - 1]
    if nan(cd, cd1):
        return None

    if cd == 1 and cd1 == -1:
        return "long"
    if cd == -1 and cd1 == 1:
        return "short"

    return None
