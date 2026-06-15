#!/usr/bin/env python3
"""bollinger_band_sd_channel_breakout -- Bollinger Band channel breakout: close breaks above upper or below lower band signals a volatility expansion trend entry. Kaufman Ch.18.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_band_sd_channel_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "bb_up, bb_lo, close",
    "long": "Close breaks above upper Bollinger band (20,2)",
    "short": "Close breaks below lower Bollinger band (20,2)",
    "desc": "Bollinger Band channel breakout: close outside the upper or lower standard-deviation band signals trend continuation",
    "source": "trading_systems_and_methods_kaufman -- Ch.18 Standard Deviation Bands / Bollinger bands",
}


def signal(ind, pos, htf=None):
    """Close outside the 2-SD Bollinger band -> breakout entry."""
    c = ind["close"][pos]
    bu = ind["bb_up"][pos]
    bl = ind["bb_lo"][pos]
    if nan(c, bu, bl):
        return None
    if c > bu:
        return "long"
    if c < bl:
        return "short"
    return None
