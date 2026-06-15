#!/usr/bin/env python3
"""psar_adx_trend_filter -- PSAR direction with ADX strength confirmation. zeta-zetra.

Enter only when PSAR signals a direction change AND ADX confirms trend is strong (>20).
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "psar_adx_trend_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, adx",
    "long": "psar_dir flips to 1 (SAR below price) AND ADX > 20",
    "short": "psar_dir flips to -1 (SAR above price) AND ADX > 20",
    "desc": "Parabolic SAR with ADX trend-strength filter",
    "source": "https://zeta-zetra.github.io/docs-forex-strategies-python/chatgpt/parabolic_adx.html",
}

_ADX_THRESH = 20.0


def signal(ind, pos, htf=None):
    """PSAR flip with ADX confirmation."""
    d = ind["psar_dir"][pos]
    d1 = ind["psar_dir"][pos - 1]
    a = ind["adx"][pos]
    if nan(d, d1, a):
        return None
    if d == 1 and d1 != 1 and a > _ADX_THRESH:
        return "long"
    if d == -1 and d1 != -1 and a > _ADX_THRESH:
        return "short"
    return None
