#!/usr/bin/env python3
"""atr_trailing_stop_chandelier -- Chandelier Exit as entry using chand_dir flip. QuantConnect / Chuck LeBeau.

The chandelier exit direction (chand_dir) is used as the entry trigger: when it flips from -1 to +1
the trend has turned bullish; from +1 to -1 it has turned bearish. The engine's own trailing exit
(TREND) manages the actual stop ratchet so the strategy focuses on the entry signal only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "atr_trailing_stop_chandelier",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "chand_dir, atr",
    "long": "chand_dir flips from -1 to +1 (highest-high minus 2*ATR stop crossed upward)",
    "short": "chand_dir flips from +1 to -1 (lowest-low plus 2*ATR stop crossed downward)",
    "desc": "Chandelier Exit direction flip used as trend-entry signal; ATR trailing stop as exit",
    "source": "https://www.quantconnect.com/forum/discussion/11358/ -- Chuck LeBeau Chandelier Exit",
}


def signal(ind, pos, htf=None):
    """Chandelier direction flip entry."""
    d = ind["chand_dir"][pos]
    d1 = ind["chand_dir"][pos - 1]
    if nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
