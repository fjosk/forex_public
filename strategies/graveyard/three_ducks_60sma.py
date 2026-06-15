#!/usr/bin/env python3
"""three_ducks_60sma -- Three Ducks multi-timeframe SMA alignment. web:babypips.com.

All three ducks must align: price above SMA50 on HTF and current TF. Entry on current-TF
cross above SMA50 (sma60 not available; sma50 used as documented substitution).
No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "three_ducks_60sma",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "sma50, htf sma50 (duck 1 + 2), close",
    "long": "HTF close > sma50 AND current close crosses above sma50",
    "short": "HTF close < sma50 AND current close crosses below sma50",
    "desc": "Three Ducks: SMA50 alignment across HTF and current TF (sma60 approximated by sma50)",
    "source": "web:https://forums.babypips.com/t/the-3-ducks-trading-system/6430",
}


def signal(ind, pos, htf=None):
    """Three Ducks SMA50 alignment entry."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    sma = ind["sma50"][pos]
    if nan(c, cp, sma):
        return None
    # HTF duck: use htf bias if available, else use st_dir as proxy
    if htf is not None and "bias" in htf:
        htf_bias = htf["bias"][pos]
        if nan(htf_bias):
            return None
        htf_long = htf_bias > 0
        htf_short = htf_bias < 0
    else:
        # fallback: just use current SMA200 slope as macro proxy
        sma200 = ind["sma200"][pos]
        sma200p = ind["sma200"][pos - 1]
        if nan(sma200, sma200p):
            return None
        htf_long = sma200 > sma200p
        htf_short = sma200 < sma200p
    # current TF duck: close crosses sma50
    cross_up = c > sma and cp <= sma
    cross_dn = c < sma and cp >= sma
    if htf_long and cross_up:
        return "long"
    if htf_short and cross_dn:
        return "short"
    return None
