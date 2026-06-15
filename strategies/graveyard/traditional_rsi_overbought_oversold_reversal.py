#!/usr/bin/env python3
"""traditional_rsi_overbought_oversold_reversal -- RSI 70/30 cross-back-through reversal as described in Naked Forex. naked_forex_high_probability_techniques_for_tradin Ch2."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "traditional_rsi_overbought_oversold_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "rsi",
    "long": "RSI was above 30 then crosses back above 30 (was below 30 = oversold, now exiting)",
    "short": "RSI was above 70 then crosses back below 70 (overbought exit)",
    "desc": "Naked Forex traditional RSI 70/30 cross-back reversal: oversold exit = long, overbought exit = short",
    "source": "book: naked_forex_high_probability_techniques_for_tradin, Ch2",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """Long when RSI crosses back above 30; short when RSI crosses back below 70."""
    if pos < 1:
        return None
    rs = ind["rsi"][pos]
    rs1 = ind["rsi"][pos - 1]
    if nan(rs, rs1):
        return None
    if rs1 < OS and rs >= OS:
        return "long"
    if rs1 > OB and rs <= OB:
        return "short"
    return None
