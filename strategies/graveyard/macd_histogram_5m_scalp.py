#!/usr/bin/env python3
"""macd_histogram_5m_scalp -- MACD histogram cross with RSI momentum filter. web:itbfx.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_histogram_5m_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "macd_hist, rsi",
    "long": "macd_hist turns positive AND rsi > 50",
    "short": "macd_hist turns negative AND rsi < 50",
    "desc": "MACD histogram sign-change entry with RSI momentum confirmation 5m scalp",
    "source": "web:https://itbfx.com/technical/best-macd-settings-for-1-minute-chart/",
}


def signal(ind, pos, htf=None):
    """MACD histogram cross combined with RSI above/below 50 for momentum direction."""
    mh = ind["macd_hist"][pos]
    mh_p = ind["macd_hist"][pos - 1]
    rsi = ind["rsi"][pos]
    if nan(mh, mh_p, rsi):
        return None
    if mh > 0 and mh_p <= 0 and rsi > 50:
        return "long"
    if mh < 0 and mh_p >= 0 and rsi < 50:
        return "short"
    return None
