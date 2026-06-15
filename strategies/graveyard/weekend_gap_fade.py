#!/usr/bin/env python3
"""weekend_gap_fade -- Monday open gap fade vs Friday close. EarnForex gap strategy.

Detect: dow == 0 (Monday) AND gap between open[pos] and prev_dhc (Friday close).
Long: negative gap (Monday opened below Friday close) >= 5x spread proxy.
Short: positive gap >= 5x spread proxy.
Spread proxy: atr * 0.05 per pip unit (conservative; gap threshold tunable).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "weekend_gap_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "dow, open, prev_dhc, atr",
    "long": "Monday open gap DOWN vs Friday close >= 5x spread proxy (fade the gap up)",
    "short": "Monday open gap UP vs Friday close >= 5x spread proxy (fade the gap down)",
    "desc": "Weekend gap fade: Monday open vs Friday close gap, enter opposite direction",
    "source": "web:https://www.earnforex.com/forex-strategy/forex-gap-strategy/",
}

_GAP_ATR_MULT = 0.05   # spread proxy = atr * 0.05; 5x spread = atr * 0.25


def signal(ind, pos, htf=None):
    """Weekend gap fade."""
    dow = ind["dow"][pos]
    o = ind["open"][pos]
    prev_c = ind["prev_dhc"][pos]
    atr = ind["atr"][pos]
    if nan(dow, o, prev_c, atr) or atr == 0:
        return None
    # dow == 0 represents Monday (engine convention: Mon=0, Sun=6 Python weekday)
    if dow != 0:
        return None
    gap = o - prev_c
    threshold = 5 * _GAP_ATR_MULT * atr
    if gap < -threshold:
        return "long"
    if gap > threshold:
        return "short"
    return None
