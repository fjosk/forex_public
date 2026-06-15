#!/usr/bin/env python3
"""rsi_overbought_oversold_exit_signal -- RSI 75/25 cross-back-out-of-zone reversal, filtered by ADX < 25 (range markets). currency_trading_for_dummies_2nd_edition_by_brian Ch11."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_overbought_oversold_exit_signal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "rsi,adx",
    "long": "RSI crosses back up above 25 (from below) AND ADX < 25 (non-trending)",
    "short": "RSI crosses back down below 75 (from above) AND ADX < 25",
    "desc": "RSI 75/25 OB/OS cross-back-out reversal filtered to range-bound markets (ADX < 25)",
    "source": "book: currency_trading_for_dummies_2nd_edition_by_brian, Ch11-12",
}

OB = 75.0
OS = 25.0
ADX_MAX = 25.0


def signal(ind, pos, htf=None):
    """Long when RSI exits oversold (<25->above 25) in a ranging market; short on RSI exiting overbought."""
    if pos < 1:
        return None
    rs = ind["rsi"][pos]
    rs1 = ind["rsi"][pos - 1]
    ax = ind["adx"][pos]
    if nan(rs, rs1, ax):
        return None
    if ax >= ADX_MAX:
        return None
    if rs1 < OS and rs >= OS:
        return "long"
    if rs1 > OB and rs <= OB:
        return "short"
    return None
