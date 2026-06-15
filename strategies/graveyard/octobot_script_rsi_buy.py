#!/usr/bin/env python3
"""octobot_script_rsi_buy -- RSI(14) oversold long-only mean-reversion. OctoBot-Script basis example.

Long only: enter when RSI drops below 28 (extreme oversold). Uses rsi (14-period, closest
available to the source's period=10) as the signal. Exit via REVERT archetype (ATR-based).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "octobot_script_rsi_buy",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "rsi",
    "long": "rsi < 28 (extreme oversold)",
    "short": "not defined (long only)",
    "desc": "RSI oversold long-only mean-reversion; OctoBot-Script basis example",
    "source": "web:https://github.com/Drakkar-Software/OctoBot-Script/blob/master/docs/strategies/basis.md",
}


def signal(ind, pos, htf=None):
    """RSI below 28 = long; no short side."""
    r = ind["rsi"][pos]
    if nan(r):
        return None
    if r < 28:
        return "long"
    return None
