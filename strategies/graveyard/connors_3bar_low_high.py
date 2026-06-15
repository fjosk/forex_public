#!/usr/bin/env python3
"""connors_3bar_low_high -- Connors 3-Bar Low mean reversion. Larry Connors / QuantifiedStrategies.

Three consecutive bars each making a lower high AND lower low, while price is above
SMA200 and below the 5-bar SMA. Buy the third bar close; exit above 5-bar SMA.
Source: web:https://www.quantifiedstrategies.com/larry-connors-3-day-high-low-method/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_3bar_low_high",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "sma200, close_sma5, high, low, close",
    "long": "close > sma200; close < close_sma5; 3 consecutive lower highs+lows",
    "short": "close < sma200; close > close_sma5; 3 consecutive higher highs+lows (mirror)",
    "desc": "Connors 3-Bar Low: three consecutive declining bars in an uptrend mean-reversion buy",
    "source": "web:https://www.quantifiedstrategies.com/larry-connors-3-day-high-low-method/",
}


def signal(ind, pos, htf=None):
    """Connors 3-bar lower-high+lower-low pattern above SMA200."""
    if pos < 3:
        return None
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    sma5 = ind["close_sma5"][pos]
    h0 = ind["high"][pos]
    h1 = ind["high"][pos - 1]
    h2 = ind["high"][pos - 2]
    h3 = ind["high"][pos - 3]
    l0 = ind["low"][pos]
    l1 = ind["low"][pos - 1]
    l2 = ind["low"][pos - 2]
    l3 = ind["low"][pos - 3]
    if nan(c, s200, sma5, h0, h1, h2, h3, l0, l1, l2, l3):
        return None

    # Long: three consecutive lower highs+lows; close > sma200; close < sma5
    if (c > s200 and c < sma5
            and h2 < h3 and l2 < l3
            and h1 < h2 and l1 < l2
            and h0 < h1 and l0 < l1):
        return "long"

    # Short: three consecutive higher highs+lows; close < sma200; close > sma5
    if (c < s200 and c > sma5
            and h2 > h3 and l2 > l3
            and h1 > h2 and l1 > l2
            and h0 > h1 and l0 > l1):
        return "short"

    return None
