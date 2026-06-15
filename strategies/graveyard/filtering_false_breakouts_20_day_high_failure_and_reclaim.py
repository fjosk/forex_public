#!/usr/bin/env python3
"""filtering_false_breakouts_20day_reclaim -- 20-day high made, 3-bar pullback to 2-day low, then reclaim of 20-day high. day_trading_swing_trading_kathy_lien."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "filtering_false_breakouts_20_day_high_failure_and_reclaim",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dc_up, dc_lo, hh_n, ll_n, high, low, close",
    "long": "new 20-day high made, pullback within 3 bars to 2-day low, then close reclaims the 20-day high",
    "short": "new 20-day low made, recovery within 3 bars to 2-day high, then close breaks the 20-day low again",
    "desc": "Filtering false breakouts: 20-day high/low failure-and-reclaim confirmation entry (Kathy Lien)",
    "source": "day_trading_swing_trading_the_currency_market_tech",
}


def signal(ind, pos, htf=None):
    """20-day breakout + 3-bar pullback + reclaim pattern."""
    if pos < 6:
        return None
    h = ind["high"]
    l = ind["low"]
    c = ind["close"]
    dc_up = ind["dc_up"]
    dc_lo = ind["dc_lo"]

    cv = c[pos]
    hv = h[pos]
    lv = l[pos]

    if nan(cv, hv, lv):
        return None

    # Current bar close must reclaim a 20-day high that was previously broken
    # Check if within the last 5 bars there was a new 20-day high,
    # followed by a 2-day low within 3 bars of that event,
    # and now price reclaims the original 20-day high level.

    # Simplified mechanical version:
    # 1. Look back 2-5 bars to find when a 20-day high was made (dc_up[k-1] was broken by h[k])
    # 2. After that, a 2-day low (low < min(low[k-1], low[k-2])) occurred within 3 bars
    # 3. Current bar closes above the dc_up level at the time of the original breakout

    for bp in range(2, 6):  # bar where breakout happened: pos-bp
        if pos - bp < 2:
            break
        orig_dc = dc_up[pos - bp - 1]
        if nan(orig_dc):
            continue
        if h[pos - bp] <= orig_dc:
            continue  # no 20-day high breakout at this bar
        # Found a 20-day high at pos-bp; check if a 2-day low formed within next 3 bars
        pullback_found = False
        for pp in range(1, 4):
            pb = pos - bp + pp
            if pb >= pos:
                break
            if pb < 2 or nan(l[pb], l[pb - 1], l[pb - 2]):
                continue
            two_day_low = min(l[pb - 1], l[pb - 2])
            if l[pb] < two_day_low:
                pullback_found = True
                break
        if pullback_found and cv > orig_dc:
            return "long"

    # Mirror for short
    for bp in range(2, 6):
        if pos - bp < 2:
            break
        orig_dc = dc_lo[pos - bp - 1]
        if nan(orig_dc):
            continue
        if l[pos - bp] >= orig_dc:
            continue
        pullback_found = False
        for pp in range(1, 4):
            pb = pos - bp + pp
            if pb >= pos:
                break
            if pb < 2 or nan(h[pb], h[pb - 1], h[pb - 2]):
                continue
            two_day_high = max(h[pb - 1], h[pb - 2])
            if h[pb] > two_day_high:
                pullback_found = True
                break
        if pullback_found and cv < orig_dc:
            return "short"

    return None
