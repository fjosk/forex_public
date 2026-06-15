#!/usr/bin/env python3
"""volatility_breakout_from_the_open_percent_of_prior_range -- Williams open-range breakout:
enter when price moves 50% of the prior bar's high-low range above/below the day open.
Long Term Secrets to Short-Term Trading, Ch.4."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_breakout_from_the_open_percent_of_prior_range",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "day_open,high,low",
    "long": "high > day_open + 0.50 * (high[i-1] - low[i-1])",
    "short": "low < day_open - 0.50 * (high[i-1] - low[i-1])",
    "desc": "Williams volatility breakout: 50% of prior bar range offset from day open triggers entry",
    "source": "Long Term Secrets to Short-Term Trading, Ch.4 (Williams volatility breakout)",
}

_P = 0.50   # percent of prior range; book tuned per market ~50-70%


def signal(ind, pos, htf=None):
    """Open + P * prior-range volatility breakout."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    do = ind["day_open"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    if nan(h, l, do, h1, l1):
        return None
    prior_range = h1 - l1
    if prior_range <= 0:
        return None
    band = _P * prior_range
    if h > do + band:
        return "long"
    if l < do - band:
        return "short"
    return None
