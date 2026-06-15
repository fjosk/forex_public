#!/usr/bin/env python3
"""parabolic_sar_dual_timeframe_entry -- PSAR direction entry with ADX trend filter. zeta-zetra."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_dual_timeframe_entry",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, adx, close",
    "long": "psar_dir turns bullish (pos-1 bearish -> pos bullish) with adx>20",
    "short": "psar_dir turns bearish (pos-1 bullish -> pos bearish) with adx>20",
    "desc": "PSAR direction flip entry with ADX strength filter; approximates dual-PSAR spec",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/youtube/parabolic_sar.html",
}

# NOTE: spec calls for two PSAR instances (fast/slow); only one psar_dir is precomputed.
# Approximation: use psar_dir flip as the primary signal plus ADX strength gate.
_ADX_MIN = 20


def signal(ind, pos, htf=None):
    """PSAR direction flip with ADX filter (collapsed from dual-PSAR spec)."""
    pd = ind["psar_dir"][pos]
    pd1 = ind["psar_dir"][pos - 1]
    adx = ind["adx"][pos]
    c = ind["close"][pos]
    if nan(pd, pd1, adx, c):
        return None
    if adx < _ADX_MIN:
        return None
    # psar_dir > 0 = bullish (price above PSAR), < 0 = bearish
    if pd > 0 and pd1 <= 0:
        return "long"
    if pd < 0 and pd1 >= 0:
        return "short"
    return None
