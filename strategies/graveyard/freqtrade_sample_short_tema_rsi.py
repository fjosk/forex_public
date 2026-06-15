#!/usr/bin/env python3
"""freqtrade_sample_short_tema_rsi -- Bidirectional TEMA RSI Bollinger template. Freqtrade official."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_sample_short_tema_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "rsi, tema9, bb_mid",
    "long": "rsi crosses up through 30 AND tema9 <= bb_mid AND tema9 rising",
    "short": "rsi crosses up through 70 AND tema9 > bb_mid AND tema9 falling",
    "desc": "Bidirectional TEMA RSI Bollinger template (Freqtrade official sample strategy)",
    "source": "https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_strategy.py",
}


def signal(ind, pos, htf=None):
    """Bidirectional TEMA RSI Bollinger signal."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    t9 = ind["tema9"][pos]
    t9_1 = ind["tema9"][pos - 1]
    bm = ind["bb_mid"][pos]
    if nan(r, r1, t9, t9_1, bm):
        return None
    # Long: RSI crosses up through 30, tema below midband and rising
    if r > 30 and r1 <= 30 and t9 <= bm and t9 > t9_1:
        return "long"
    # Short: RSI crosses up through 70, tema above midband and falling
    if r > 70 and r1 <= 70 and t9 > bm and t9 < t9_1:
        return "short"
    return None
