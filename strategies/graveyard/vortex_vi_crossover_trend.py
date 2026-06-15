#!/usr/bin/env python3
"""vortex_vi_crossover_trend -- VI+/VI- crossover with SMA50 trend filter. enlightenedstocktrading."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "vortex_vi_crossover_trend",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "vi_plus, vi_minus, sma50, close",
    "long": "vi_plus crosses above vi_minus AND close > sma50",
    "short": "vi_minus crosses above vi_plus AND close < sma50",
    "desc": "Vortex VI+/VI- crossover confirmed by price above/below SMA50 trend filter",
    "source": "enlightenedstocktrading.com Vortex Indicator guide; stockindicators.dev Python implementation",
}


def signal(ind, pos, htf=None):
    """VI+ crosses VI- with SMA50 trend confirmation."""
    vp = ind["vi_plus"][pos]
    vm = ind["vi_minus"][pos]
    vp1 = ind["vi_plus"][pos - 1]
    vm1 = ind["vi_minus"][pos - 1]
    s50 = ind["sma50"][pos]
    c = ind["close"][pos]
    if nan(vp, vm, vp1, vm1, s50, c):
        return None
    if _xup(vp, vp1, vm, vm1) and c > s50:
        return "long"
    if _xdn(vp, vp1, vm, vm1) and c < s50:
        return "short"
    return None
