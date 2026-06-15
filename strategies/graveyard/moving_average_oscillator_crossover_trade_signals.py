#!/usr/bin/env python3
"""moving_average_oscillator_crossover_trade_signals -- EMA9 crosses EMA20 or MACD line/signal cross for FX swing entries. currency_trading_for_dummies_2nd_edition_by_brian."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES, _xup, _xdn

META = {
    "id": "moving_average_oscillator_crossover_trade_signals",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ema9, ema20, macd, macd_sig",
    "long": "EMA9 crosses above EMA20 AND MACD crosses above Signal (double confirmation)",
    "short": "EMA9 crosses below EMA20 AND MACD crosses below Signal (double confirmation)",
    "desc": "MA/oscillator crossover: EMA9/20 cross confirmed by MACD line/signal cross",
    "source": "book:currency_trading_for_dummies_2nd_edition_by_brian Ch 10",
}


def signal(ind, pos, htf=None):
    """EMA9/20 cross confirmed by MACD/Signal cross for double-confirmation entry."""
    if pos < 1:
        return None
    e9 = ind["ema9"][pos]
    e9_1 = ind["ema9"][pos - 1]
    e20 = ind["ema20"][pos]
    e20_1 = ind["ema20"][pos - 1]
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(e9, e9_1, e20, e20_1, m, m1, ms, ms1):
        return None
    if _xup(e9, e9_1, e20, e20_1) and _xup(m, m1, ms, ms1):
        return "long"
    if _xdn(e9, e9_1, e20, e20_1) and _xdn(m, m1, ms, ms1):
        return "short"
    return None
