#!/usr/bin/env python3
"""reversal_follow_through_lower_low_higher_close -- Lower-low higher-close fade (Kaufman 80% reversal). trading_systems_and_methods_kaufman_perry_j_kaufma.

Short: bar makes a lower low than prior bar but closes ABOVE prior close -> failed reversal fade.
Long (mirror): bar makes a higher high but closes BELOW prior close -> fade the false up-day.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "reversal_follow_through_lower_low_higher_close",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "high,low,close",
    "long": "high[pos] > high[pos-1] AND close[pos] < close[pos-1] (false up-day -> fade long)",
    "short": "low[pos] < low[pos-1] AND close[pos] > close[pos-1] (lower low but higher close = failed reversal -> short)",
    "desc": "Reversal follow-through fade: bar with lower low + higher close (or higher high + lower close) signals counter-direction",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma, Ch15 p.413-416 Table15-11",
}


def signal(ind, pos, htf=None):
    """Lower-low + higher-close (or higher-high + lower-close) fade signal."""
    if pos < 1:
        return None
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(h, l, c, h1, l1, c1):
        return None
    # Short: lower low but closes above prior close (80% reversal pattern)
    if l < l1 and c > c1:
        return "short"
    # Long: higher high but closes below prior close (mirror fade)
    if h > h1 and c < c1:
        return "long"
    return None
