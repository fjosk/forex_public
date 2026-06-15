#!/usr/bin/env python3
"""moving_average_with_percentage_price_band_mab -- Price breaks above SMA20*(1+band) or below SMA20*(1-band) as trend entry. trading_systems_and_methods_kaufman."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "moving_average_with_percentage_price_band_mab",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close, sma20",
    "long": "Close breaks above SMA20 * (1 + 0.002) upper percentage band",
    "short": "Close breaks below SMA20 * (1 - 0.002) lower percentage band",
    "desc": "MA with percentage band (MAB): breakout above/below MA envelope triggers trend entry",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma Ch 21 Table 21-12",
}

BAND_PCT = 0.002   # 0.2% band (FX-appropriate small percentage)


def signal(ind, pos, htf=None):
    """Close exceeds SMA20 +/- percentage band for breakout entry."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    sma = ind["sma20"][pos]
    if nan(c, c1, sma):
        return None
    upper = sma * (1.0 + BAND_PCT)
    lower = sma * (1.0 - BAND_PCT)
    # Entry on cross into/through the band
    if c > upper and c1 <= upper:
        return "long"
    if c < lower and c1 >= lower:
        return "short"
    return None
