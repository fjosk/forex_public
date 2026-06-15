#!/usr/bin/env python3
"""three_ducks_system -- 3 Ducks: SMA50 alignment across htf + current-bar SMA50 cross. BabyPips / Captain Currency."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_ducks_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "sma50",
    "long": "htf (4H) close > sma50 AND current close crosses above sma50",
    "short": "htf close < sma50 AND current close crosses below sma50",
    "desc": "3 Ducks: higher-TF SMA50 alignment then current-TF SMA50 cross entry (SMA50 approx for SMA60)",
    "source": "web:https://www.babypips.com/trading/system-review-3-ducks-system",
}


def signal(ind, pos, htf=None):
    """HTF SMA50 alignment + current-bar SMA50 crossover. SMA50 approximates the original SMA60."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    s50 = ind["sma50"][pos]
    s50p = ind["sma50"][pos - 1]
    if nan(c, cp, s50, s50p):
        return None

    # Duck 3 on current TF: price crosses SMA50
    duck3_up = c > s50 and cp <= s50p
    duck3_dn = c < s50 and cp >= s50p

    # Duck 1 + 2 from htf when available
    if htf is not None:
        bias_arr = htf.get("bias")
        if bias_arr is not None and not nan(bias_arr[pos]):
            htf_bull = bias_arr[pos] > 0
            htf_bear = bias_arr[pos] < 0
        else:
            htf_bull = c > s50
            htf_bear = c < s50
    else:
        htf_bull = c > s50
        htf_bear = c < s50

    if htf_bull and duck3_up:
        return "long"
    if htf_bear and duck3_dn:
        return "short"
    return None
