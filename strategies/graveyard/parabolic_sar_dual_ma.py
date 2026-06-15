#!/usr/bin/env python3
"""parabolic_sar_dual_ma -- PSAR direction + SMA20/50 crossover confirmation. web:https://forextester.com/blog/parabolic-sar-moving-average-strategy/"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_dual_ma",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "psar_dir, sma20, sma50, close",
    "long": "psar_dir == 1 (bullish) AND sma20 crosses above sma50",
    "short": "psar_dir == -1 (bearish) AND sma20 crosses below sma50",
    "desc": "PSAR dual-MA: PSAR direction filter with SMA20/50 crossover trigger (sma50 proxies sma40)",
    "source": "web:https://forextester.com/blog/parabolic-sar-moving-average-strategy/",
}


def signal(ind, pos, htf=None):
    """PSAR bullish/bearish combined with SMA20/50 cross (sma50 proxies sma40)."""
    pdir = ind["psar_dir"][pos]
    s20 = ind["sma20"][pos]
    s20_1 = ind["sma20"][pos - 1]
    s50 = ind["sma50"][pos]
    s50_1 = ind["sma50"][pos - 1]
    if nan(pdir, s20, s20_1, s50, s50_1):
        return None
    psar_bull = pdir == 1
    psar_bear = pdir == -1
    sma_cross_up = _xup(s20, s20_1, s50, s50_1)
    sma_cross_dn = _xdn(s20, s20_1, s50, s50_1)
    if psar_bull and sma_cross_up:
        return "long"
    if psar_bear and sma_cross_dn:
        return "short"
    return None
