#!/usr/bin/env python3
"""qqe_mod -- QQE primary line cross of RSI-MA (primary QQE above/below midpoint). Mihkel00."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "qqe_mod",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h/4h",
    "indicators": "qqe_line, qqe_rsima",
    "long": "qqe_line crosses above qqe_rsima (primary QQE bullish cross)",
    "short": "qqe_line crosses below qqe_rsima (primary QQE bearish cross)",
    "desc": "QQE Mod primary: qqe_line vs qqe_rsima crossover as momentum entry",
    "source": "web:https://www.tradingview.com/script/TpUW4muw-QQE-MOD/",
}


def signal(ind, pos, htf=None):
    """QQE primary crossover: qqe_line crosses above/below qqe_rsima."""
    if pos < 1:
        return None
    ql0 = ind["qqe_line"][pos]
    qr0 = ind["qqe_rsima"][pos]
    ql1 = ind["qqe_line"][pos - 1]
    qr1 = ind["qqe_rsima"][pos - 1]
    if nan(ql0, qr0, ql1, qr1):
        return None

    if ql0 > qr0 and ql1 <= qr1:
        return "long"
    if ql0 < qr0 and ql1 >= qr1:
        return "short"

    return None
