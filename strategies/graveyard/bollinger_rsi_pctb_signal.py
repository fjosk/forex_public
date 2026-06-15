#!/usr/bin/env python3
"""bollinger_rsi_pctb_signal -- Bollinger %B + RSI mean-reversion entry. armelf Financial-Algorithms.

No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, _xup, ALL_CLASSES

META = {
    "id": "bollinger_rsi_pctb_signal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "bb_pctb, rsi",
    "long": "bb_pctb crosses above 0 (re-enters lower band zone) OR bb_pctb<0.2 AND rsi<=50",
    "short": "bb_pctb > 0.8 AND rsi >= 50",
    "desc": "Bollinger %B + RSI: long at lower band extremes, short at upper band with momentum",
    "source": "github.com/armelf/Financial-Algorithms Bollinger RSI Strategy",
}


def signal(ind, pos, htf=None):
    """Bollinger %B + RSI mean-reversion entry."""
    if pos < 1:
        return None
    pctb0 = ind["bb_pctb"][pos]
    pctb1 = ind["bb_pctb"][pos - 1]
    rs = ind["rsi"][pos]
    if nan(pctb0, pctb1, rs):
        return None
    # Long variant A: %B crosses above 0 from below
    long_a = pctb0 > 0 and pctb1 <= 0
    # Long variant B: deep oversold + RSI not in uptrend
    long_b = pctb0 < 0.2 and rs <= 50
    if long_a or long_b:
        return "long"
    # Short: near upper band with momentum not yet exhausted
    if pctb0 > 0.8 and rs >= 50:
        return "short"
    return None
