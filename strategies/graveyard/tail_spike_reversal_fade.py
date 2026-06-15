#!/usr/bin/env python3
"""tail_spike_reversal_fade -- A bar with an outlier wick extending well beyond recent ATR
signals rejection; fade in the direction opposite the tail. elder_alexander_trading_for_a_living.

Long tail down (long lower wick > 2*ATR below body low): fade up (go long).
Long tail up (long upper wick > 2*ATR above body high): fade down (go short).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "tail_spike_reversal_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "open,high,low,close,atr",
    "long": "current bar has a long lower tail (low wicks down > 2*ATR below the body's lower edge) - rejected low, fade up",
    "short": "current bar has a long upper tail (high wicks up > 2*ATR above the body's upper edge) - rejected high, fade down",
    "desc": "Tail spike reversal fade: outlier wick extending >2*ATR beyond the bar body signals price rejection",
    "source": "elder_alexander_trading_for_a_living Sec 21 Tails (Steidlmayer p.89-90)",
}


def signal(ind, pos, htf=None):
    """Fade when a bar has an outlier-length wick beyond the body."""
    o  = ind["open"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    c  = ind["close"][pos]
    a  = ind["atr"][pos]
    if nan(o, hi, lo, c, a) or a <= 0:
        return None
    body_lo = min(o, c)
    body_hi = max(o, c)
    lower_wick = body_lo - lo
    upper_wick = hi - body_hi
    threshold = 2.0 * a
    if lower_wick > threshold:
        return "long"
    if upper_wick > threshold:
        return "short"
    return None
