#!/usr/bin/env python3
"""big_shadow_engulfing_reversal_at_a_zone -- Outside bar (higher high + lower low than prior)
with close near extreme; widest range of last 5 bars; zone approximated by pivot S/R proximity.
Naked Forex, Ch.6 'The Big Shadow'."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "big_shadow_engulfing_reversal_at_a_zone",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr,piv_s1,piv_r1",
    "long": "outside bar with close near high, widest range of 5 bars, close near pivot S1 support",
    "short": "outside bar with close near low, widest range of 5 bars, close near pivot R1 resistance",
    "desc": "Big Shadow: outside bar with close near extreme (widest range of 5) at a S/R zone",
    "source": "Naked Forex, Ch.6 'The Big Shadow' (p.109-110)",
}

_CLOSE_EDGE = 0.25   # close must be in top/bottom 25% of bar range
_ZONE_ATR = 1.5      # within 1.5 ATR of pivot level counts as a zone


def signal(ind, pos, htf=None):
    """Big Shadow: outside bar, close near extreme, at pivot S/R zone."""
    if pos < 5:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    a = ind["atr"][pos]
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    if nan(o, h, l, c, h1, l1, a, s1, r1):
        return None
    rng = h - l
    if rng <= 0:
        return None
    # Outside bar: higher high and lower low than prior bar
    if not (h > h1 and l < l1):
        return None
    # Must be widest bar range of last 5 bars
    max_rng = max(
        ind["high"][pos - k] - ind["low"][pos - k]
        for k in range(1, 5)
        if not nan(ind["high"][pos - k], ind["low"][pos - k])
    )
    if rng <= max_rng:
        return None
    # Bullish big shadow: close in top 25% of bar, near S1
    close_from_top = (h - c) / rng
    close_from_bot = (c - l) / rng
    if close_from_top <= _CLOSE_EDGE and abs(c - s1) <= _ZONE_ATR * a:
        return "long"
    # Bearish big shadow: close in bottom 25% of bar, near R1
    if close_from_bot <= _CLOSE_EDGE and abs(c - r1) <= _ZONE_ATR * a:
        return "short"
    return None
