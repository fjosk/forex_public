#!/usr/bin/env python3
"""3commas_dca_rsi_bb_macd -- 3Commas DCA Bot RSI + BB + MACD Deal Start Conditions. 3commas.io.

RSI oversold exit crossover + BB %B below lower band + MACD bullish crossover below zero.
All three AND for long. Mirror for short.
"""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "3commas_dca_rsi_bb_macd",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "rsi, bb_pctb, macd, macd_sig",
    "long": "rsi crosses above 30 AND bb_pctb < 0.0 AND macd < 0 AND macd crosses above macd_sig",
    "short": "rsi crosses below 70 AND bb_pctb > 1.0 AND macd > 0 AND macd crosses below macd_sig",
    "desc": "3Commas DCA deal start: RSI oversold exit + BB below lower band + MACD bullish cross below zero",
    "source": "web:https://help.3commas.io/en/articles/3108986-dca-bots-technical-analysis-deal-start-conditions-and-deal-close-conditions",
}


def signal(ind, pos, htf=None):
    """3Commas RSI + BB%B + MACD confluence entry."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    pctb = ind["bb_pctb"][pos]
    m = ind["macd"][pos]
    m1 = ind["macd"][pos - 1]
    ms = ind["macd_sig"][pos]
    ms1 = ind["macd_sig"][pos - 1]
    if nan(r, r1, pctb, m, m1, ms, ms1):
        return None
    # Long: RSI crossing up through 30, bb_pctb below lower band (<0), MACD < 0 and crossing above signal
    if _xup(r, r1, 30.0, 30.0) and pctb < 0.0 and m < 0 and _xup(m, m1, ms, ms1):
        return "long"
    # Short: RSI crossing down through 70, bb_pctb above upper band (>1), MACD > 0 and crossing below signal
    if _xdn(r, r1, 70.0, 70.0) and pctb > 1.0 and m > 0 and _xdn(m, m1, ms, ms1):
        return "short"
    return None
