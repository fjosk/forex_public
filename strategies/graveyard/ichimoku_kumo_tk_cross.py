#!/usr/bin/env python3
"""ichimoku_kumo_tk_cross -- Kumo breakout + TK cross confirmation. PyQuantLab."""
from strategies._common import nan, TREND, _xup, _xdn, ALL_CLASSES

META = {
    "id": "ichimoku_kumo_tk_cross",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_a, ich_b, ich_ten, ich_kij, close",
    "long": "close above cloud (both spans) AND tenkan crosses above kijun",
    "short": "close below cloud AND tenkan crosses below kijun",
    "desc": "Ichimoku Kumo breakout with TK cross confirmation (three-component alignment)",
    "source": "https://pyquantlab.com/article.php?file=Ichimoku+Cloud+Breakout+Trading+Strategy+with+Trailing+Stops.html",
}


def signal(ind, pos, htf=None):
    """Kumo breakout + TK cross alignment."""
    a = ind["ich_a"][pos]
    b = ind["ich_b"][pos]
    ten = ind["ich_ten"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij = ind["ich_kij"][pos]
    kij1 = ind["ich_kij"][pos - 1]
    c = ind["close"][pos]
    if nan(a, b, ten, ten1, kij, kij1, c):
        return None
    cloud_top = max(a, b)
    cloud_bot = min(a, b)
    above_cloud = c > cloud_top
    below_cloud = c < cloud_bot
    if above_cloud and _xup(ten, ten1, kij, kij1):
        return "long"
    if below_cloud and _xdn(ten, ten1, kij, kij1):
        return "short"
    return None
