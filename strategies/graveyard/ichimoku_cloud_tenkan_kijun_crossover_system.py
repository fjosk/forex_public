#!/usr/bin/env python3
"""ichimoku_cloud_tenkan_kijun_crossover_system -- Ichimoku Tenkan/Kijun cross with cloud-position strength filter. currency_trading_for_dummies_2nd_edition_by_brian."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "ichimoku_cloud_tenkan_kijun_crossover_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ich_ten, ich_kij, ich_a, ich_b, close",
    "long": "Tenkan crosses above Kijun; strong signal when price is above the cloud",
    "short": "Tenkan crosses below Kijun; strong signal when price is below the cloud",
    "desc": "Ichimoku Tenkan/Kijun crossover system with cloud-position strength confirmation",
    "source": "book:currency_trading_for_dummies_2nd_edition_by_brian Ch 11-12",
}


def signal(ind, pos, htf=None):
    """Tenkan/Kijun cross; confirmed by price position relative to cloud."""
    if pos < 1:
        return None
    ten = ind["ich_ten"][pos]
    ten1 = ind["ich_ten"][pos - 1]
    kij = ind["ich_kij"][pos]
    kij1 = ind["ich_kij"][pos - 1]
    c = ind["close"][pos]
    span_a = ind["ich_a"][pos]
    span_b = ind["ich_b"][pos]
    if nan(ten, ten1, kij, kij1, c, span_a, span_b):
        return None
    cloud_top = max(span_a, span_b)
    cloud_bot = min(span_a, span_b)
    if _xup(ten, ten1, kij, kij1):
        # Accept signal when price is inside or above cloud (medium/strong)
        if c >= cloud_bot:
            return "long"
    if _xdn(ten, ten1, kij, kij1):
        # Accept signal when price is inside or below cloud (medium/strong)
        if c <= cloud_top:
            return "short"
    return None
