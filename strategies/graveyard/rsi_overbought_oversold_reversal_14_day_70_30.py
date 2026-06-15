#!/usr/bin/env python3
"""rsi_overbought_oversold_reversal_14_day_70_30 -- RSI(14) cross back above 30 / below 70 reversal entry. currency_strategy_a_practitioner_s_guide_to_curren Ch4."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_reversal_14_day_70_30",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "rsi",
    "long": "RSI(14) crosses back above 30 oversold level (was <= 30)",
    "short": "RSI(14) crosses back below 70 overbought level (was >= 70)",
    "desc": "Standard RSI 70/30 cross-back reversal: oversold exit = long, overbought exit = short",
    "source": "book: currency_strategy_a_practitioner_s_guide_to_curren, Ch4",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """Long when RSI exits oversold; short when RSI exits overbought."""
    if pos < 1:
        return None
    rs = ind["rsi"][pos]
    rs1 = ind["rsi"][pos - 1]
    if nan(rs, rs1):
        return None
    if rs1 <= OS and rs > OS:
        return "long"
    if rs1 >= OB and rs < OB:
        return "short"
    return None
