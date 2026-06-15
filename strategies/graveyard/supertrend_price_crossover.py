#!/usr/bin/env python3
"""supertrend_price_crossover -- SuperTrend line vs price crossover. QuantConnect forum."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_price_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "st_line, st_dir, close",
    "long": "st_line < close (SuperTrend below price = bullish); fires on flip",
    "short": "st_line > close (SuperTrend above price = bearish); fires on flip",
    "desc": "SuperTrend price crossover: go long when ST line crosses below price, short when above",
    "source": "QuantConnect forum discussion 16136 -- SuperTrend strategy (community, 2024)",
}


def signal(ind, pos, htf=None):
    """Enter when SuperTrend line changes side relative to price."""
    d = ind["st_dir"][pos]
    d1 = ind["st_dir"][pos - 1]
    c = ind["close"][pos]
    stl = ind["st_line"][pos]
    if nan(d, d1, c, stl):
        return None
    # Use st_dir flip as the crossover trigger
    if d > 0 and d1 <= 0:
        return "long"
    if d < 0 and d1 >= 0:
        return "short"
    return None
