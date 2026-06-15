#!/usr/bin/env python3
"""keltner_channel_breakout -- Keltner channel breakout: close above/below KC bands. web:quantifiedstrategies."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "keltner_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "kc_up, kc_lo, kc_mid",
    "long": "close above upper Keltner Channel band",
    "short": "close below lower Keltner Channel band",
    "desc": "Keltner channel breakout: enter on close beyond the band, exit on return to EMA midline",
    "source": "web:https://www.quantifiedstrategies.com/keltner-bands-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """Keltner channel breakout."""
    c = ind["close"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    if nan(c, kc_up, kc_lo):
        return None
    if c > kc_up:
        return "long"
    if c < kc_lo:
        return "short"
    return None
