#!/usr/bin/env python3
"""dark_cloud_cover_piercing_pattern -- Two-candle reversal pair: piercing pattern (bullish) or
dark cloud cover (bearish). Gap open then close past prior body midpoint.
J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.49."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "dark_cloud_cover_piercing_pattern",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "piercing: bar1 long down body, bar2 gaps below bar1 close and closes above bar1 body midpoint",
    "short": "dark cloud: bar1 long up body, bar2 opens above bar1 high and closes below bar1 midpoint",
    "desc": "Piercing/dark-cloud-cover two-candle gap-and-midpoint-penetration reversal",
    "source": "J. Person, A Complete Guide to Technical Trading Tactics, Ch.4 p.49",
}


def signal(ind, pos, htf=None):
    """Piercing (long) or dark cloud cover (short) two-candle reversal."""
    if pos < 1:
        return None
    o1 = ind["open"][pos - 1]
    c1 = ind["close"][pos - 1]
    h1 = ind["high"][pos - 1]
    o2 = ind["open"][pos]
    c2 = ind["close"][pos]
    if nan(o1, c1, h1, o2, c2):
        return None

    # Piercing (bullish): bar1 down body, bar2 gaps below bar1 close, closes above midpoint
    if c1 < o1:
        body1 = o1 - c1
        if body1 > 0:
            midpoint = c1 + body1 / 2.0
            if o2 < c1 and c2 > midpoint and c2 > o2:
                return "long"

    # Dark cloud (bearish): bar1 up body, bar2 opens above bar1 high, closes below midpoint
    if c1 > o1:
        body1 = c1 - o1
        if body1 > 0:
            midpoint = o1 + body1 / 2.0
            if o2 > h1 and c2 < midpoint and c2 < o2:
                return "short"

    return None
