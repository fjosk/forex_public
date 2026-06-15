#!/usr/bin/env python3
"""donchian_channel_breakout_daily -- Donchian 20-day channel breakout (AlgomaticTrading). web:substack."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "donchian_channel_breakout_daily",
    "cadences": ["swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, atr",
    "long": "close above Donchian 20-day high",
    "short": "close below Donchian 20-day low",
    "desc": "Simple Donchian 20-period channel breakout: long on new high, short on new low",
    "source": "web:https://algomatictrading.substack.com/p/strategy-8-the-easiest-trend-system",
}


def signal(ind, pos, htf=None):
    """Donchian daily channel breakout."""
    c = ind["close"][pos]
    dc_up = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    if nan(c, dc_up, dc_lo):
        return None
    if c > dc_up:
        return "long"
    if c < dc_lo:
        return "short"
    return None
