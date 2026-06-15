#!/usr/bin/env python3
"""parabolic_sar_adx_trend_confirmation -- PSAR direction + ADX trending filter. Zeta-Zetra Parabolic ADX.

Long when PSAR is bullish (psar_dir==1) and ADX confirms trend (>25).
Short when PSAR is bearish (psar_dir==-1) and ADX>25.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "parabolic_sar_adx_trend_confirmation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "psar, psar_dir, adx, close",
    "long": "psar_dir == 1 (PSAR below price) AND adx > 25",
    "short": "psar_dir == -1 (PSAR above price) AND adx > 25",
    "desc": "Parabolic SAR direction with ADX trend-strength filter",
    "source": "web:https://zeta-zetra.github.io/docs-forex-strategies-python/chatgpt/parabolic_adx.html",
}


def signal(ind, pos, htf=None):
    """PSAR bullish/bearish direction gated by ADX > 25."""
    pd_ = ind["psar_dir"][pos]
    adx = ind["adx"][pos]
    c = ind["close"][pos]
    if nan(pd_, adx, c):
        return None
    trend = adx > 25
    if trend and pd_ == 1:
        return "long"
    if trend and pd_ == -1:
        return "short"
    return None
