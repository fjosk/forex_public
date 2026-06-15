#!/usr/bin/env python3
"""stoch_rsi_hull_5m -- StochRSI exit OB/OS + RSI50 + HMA trend 5m scalp. AtaQuant blog.

Long: srsi_k crosses above 20 AND rsi > 50 AND hma21 rising.
Short: srsi_k crosses below 80 AND rsi < 50 AND hma21 falling.
hma21 direction used as proxy for Hull Suite green/red signal.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stoch_rsi_hull_5m",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "srsi_k, rsi, hma21",
    "long": "srsi_k crosses above 20, rsi > 50, hma21 rising",
    "short": "srsi_k crosses below 80, rsi < 50, hma21 falling",
    "desc": "Stochastic RSI exit OB/OS + RSI50 + Hull Suite 5m scalp",
    "source": "web:https://ataquant.com/5-minute-scalping-strategy-with-stochastic-rsi/",
}


def signal(ind, pos, htf=None):
    """StochRSI + RSI50 + HMA 5m scalp."""
    sk0 = ind["srsi_k"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    rsi = ind["rsi"][pos]
    h0 = ind["hma21"][pos]
    h1 = ind["hma21"][pos - 1]
    if nan(sk0, sk1, rsi, h0, h1):
        return None
    if sk0 > 20 and sk1 <= 20 and rsi > 50 and h0 > h1:
        return "long"
    if sk0 < 80 and sk1 >= 80 and rsi < 50 and h0 < h1:
        return "short"
    return None
