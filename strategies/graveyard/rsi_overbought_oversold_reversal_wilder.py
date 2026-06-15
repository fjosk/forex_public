#!/usr/bin/env python3
"""rsi_overbought_oversold_reversal_wilder -- Wilder RSI OB/OS level entry: long when RSI <= 30, short when RSI >= 70. trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_reversal_wilder",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "rsi",
    "long": "RSI reaches oversold (RSI <= 30), enter on next bar",
    "short": "RSI reaches overbought (RSI >= 70), enter on next bar",
    "desc": "Wilder RSI OB/OS entry: at extreme level enter reversal on the next bar",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

OB = 70.0
OS = 30.0


def signal(ind, pos, htf=None):
    """Long when RSI touches oversold zone; short when RSI touches overbought zone."""
    if pos < 1:
        return None
    rs = ind["rsi"][pos]
    rs1 = ind["rsi"][pos - 1]
    if nan(rs, rs1):
        return None
    # Enter at the first bar that hits the extreme (cross into zone)
    if rs <= OS and rs1 > OS:
        return "long"
    if rs >= OB and rs1 < OB:
        return "short"
    return None
