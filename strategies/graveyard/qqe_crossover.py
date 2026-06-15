#!/usr/bin/env python3
"""qqe_crossover -- QQE (Quantitative Qualitative Estimation) line cross above/below 50. HowToTrade.

QQE smoothed RSI line crosses the slow ATR trailing band, filtered by the 50 midline for
momentum confirmation. Widely used on FX MetaTrader charts.
"""
from strategies._common import nan, _xup, _xdn, TREND_FLIP, ALL_CLASSES

META = {
    "id": "qqe_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "qqe_line, qqe_rsima",
    "long": "qqe_line crosses above qqe_rsima and qqe_line > 50",
    "short": "qqe_line crosses below qqe_rsima and qqe_line < 50",
    "desc": "QQE smoothed-RSI crossover filtered by 50 midline",
    "source": "web:https://howtotrade.com/indicators/qqe-indicator/",
}


def signal(ind, pos, htf=None):
    """QQE cross with 50-level filter."""
    ql = ind["qqe_line"][pos]
    qr = ind["qqe_rsima"][pos]
    ql1 = ind["qqe_line"][pos - 1]
    qr1 = ind["qqe_rsima"][pos - 1]
    if nan(ql, qr, ql1, qr1):
        return None
    if _xup(ql, ql1, qr, qr1) and ql > 50:
        return "long"
    if _xdn(ql, ql1, qr, qr1) and ql < 50:
        return "short"
    return None
