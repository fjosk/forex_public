#!/usr/bin/env python3
"""key_reversal_day_outside_reversal -- Outside-range key reversal day. trading_systems_and_methods_kaufman_perry_j_kaufma.

Bearish key reversal: uptrend over n days (close above SMA20), today makes a new n-day high,
today's low is lower than yesterday's low, today closes below yesterday's close.
Bullish key reversal mirrors: downtrend, new n-day low, higher high, close above prior close.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "key_reversal_day_outside_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,sma20,hh_n,ll_n",
    "long": "Downtrend (close<sma20), today new N-day low (ll_n), today high>prior high, today close>prior close",
    "short": "Uptrend (close>sma20), today new N-day high (hh_n), today low<prior low, today close<prior close",
    "desc": "Key reversal day: outside-bar geometry that reverses the prior trend direction",
    "source": "book:trading_systems_and_methods_kaufman_perry_j_kaufma",
}


def signal(ind, pos, htf=None):
    """Key reversal day: extreme + reversal close against prior trend."""
    if pos < 1:
        return None
    h   = ind["high"]
    lo  = ind["low"]
    c   = ind["close"]
    sma = ind["sma20"][pos]
    hhn = ind["hh_n"][pos]   # rolling highest-high (20-bar window in engine)
    lln = ind["ll_n"][pos]   # rolling lowest-low
    if nan(h[pos], lo[pos], c[pos], h[pos-1], lo[pos-1], c[pos-1], sma, hhn, lln):
        return None

    # Bearish key reversal: uptrend, new N-day high, lower low, close below prior close
    if (c[pos] > sma and
            h[pos] >= hhn and
            lo[pos] < lo[pos-1] and
            c[pos] < c[pos-1]):
        return "short"

    # Bullish key reversal: downtrend, new N-day low, higher high, close above prior close
    if (c[pos] < sma and
            lo[pos] <= lln and
            h[pos] > h[pos-1] and
            c[pos] > c[pos-1]):
        return "long"

    return None
