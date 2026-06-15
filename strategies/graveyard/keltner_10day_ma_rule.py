#!/usr/bin/env python3
"""keltner_10day_ma_rule -- Keltner 10-Day Moving Average Rule: buy when close breaks above upper Keltner channel, sell when below lower channel; always reverse on opposite band penetration. Kaufman Ch Applications of Single Trends.

Price/OHLC only. No volume.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "keltner_10day_ma_rule",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "kc_up, kc_lo, kc_mid, close",
    "long": "Close penetrates above the upper Keltner channel band",
    "short": "Close penetrates below the lower Keltner channel band",
    "desc": "Keltner 10-day MA rule: close outside the Keltner channel signals trend direction; always reverse on opposite band",
    "source": "trading_systems_and_methods_kaufman -- Applications of Single Trends The 10-Day Moving Average Rule (Keltner 1960)",
}


def signal(ind, pos, htf=None):
    """Close outside the Keltner channel -> enter in that direction."""
    c = ind["close"][pos]
    ku = ind["kc_up"][pos]
    kl = ind["kc_lo"][pos]
    if nan(c, ku, kl):
        return None
    if c > ku:
        return "long"
    if c < kl:
        return "short"
    return None
