#!/usr/bin/env python3
"""macd_line_signal_line_crossover -- MACD line crosses above/below Signal line. elder_alexander_trading_for_a_living."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "macd_line_signal_line_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "macd, macd_sig",
    "long": "MACD line crosses above Signal line",
    "short": "MACD line crosses below Signal line",
    "desc": "MACD line/signal crossover: classic momentum-trend entry on 12/26/9 crossover",
    "source": "book:elder_alexander_trading_for_a_living Sec 26 p.130-131",
}


def signal(ind, pos, htf=None):
    """Long on MACD crossing above Signal; short on MACD crossing below Signal."""
    if pos < 1:
        return None
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    s = ind["macd_sig"][pos]
    s1 = ind["macd_sig"][pos - 1]
    if nan(m, m1, s, s1):
        return None
    if _xup(m, m1, s, s1):
        return "long"
    if _xdn(m, m1, s, s1):
        return "short"
    return None
