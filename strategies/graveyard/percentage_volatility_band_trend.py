#!/usr/bin/env python3
"""percentage_volatility_band_trend -- Percentage/Volatility Band Trend System: enter when close breaks outside the Keltner (ATR-scaled MA band); exit to flat when close returns to the centerline. Kaufman Bands and Channels section.

Price/OHLC only. No volume.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "percentage_volatility_band_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "kc_up, kc_lo, kc_mid, close",
    "long": "Close breaks above upper Keltner band (MA + ATR-scaled offset)",
    "short": "Close breaks below lower Keltner band (MA - ATR-scaled offset)",
    "desc": "Volatility band trend system using Keltner channel: breakout above/below band enters trend; chandelier trail exits",
    "source": "trading_systems_and_methods_kaufman -- Bands and Channels section percentage/volatility band",
}


def signal(ind, pos, htf=None):
    """Close outside Keltner band enters; chandelier trail (via TREND exit) manages the position."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    ku = ind["kc_up"][pos]
    kl = ind["kc_lo"][pos]
    km = ind["kc_mid"][pos]
    ku1 = ind["kc_up"][pos - 1]
    kl1 = ind["kc_lo"][pos - 1]
    if nan(c, c1, ku, kl, km, ku1, kl1):
        return None
    # Breakout entry: close crosses outside the band
    if c > ku and c1 <= ku1:
        return "long"
    if c < kl and c1 >= kl1:
        return "short"
    return None
