#!/usr/bin/env python3
"""usd_jpy_spike_reversal_exhaustion -- After a fast multi-bar directional impulse (> 3*ATR),
a counter-bar reversing > 1*ATR in the opposite direction signals exhaustion; fade in the
counter direction. currency_trading_for_dummies_2nd_edition_by_brian.

Impulse measured as net close change over 6 bars. Counter-move measured as the current bar's
range in the direction opposite the impulse vs ATR threshold.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "usd_jpy_spike_reversal_exhaustion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h-4h",
    "indicators": "close,high,low,open,atr",
    "long": "prior 6-bar move was strongly down (< -3*ATR), current bar reverses up by >= 1*ATR (fade down-impulse)",
    "short": "prior 6-bar move was strongly up (> 3*ATR), current bar reverses down by >= 1*ATR (fade up-impulse)",
    "desc": "USD/JPY spike-reversal exhaustion: fast impulse then counter-bar >= 1*ATR signals exhaustion and fade",
    "source": "currency_trading_for_dummies_2nd_edition_by_brian Ch.8 Jumping on spike reversals",
}

_IMPULSE_BARS = 6
_IMPULSE_ATR  = 3.0
_REVERSAL_ATR = 1.0


def signal(ind, pos, htf=None):
    """Fade when a large directional impulse is followed by a meaningful counter-bar."""
    if pos < _IMPULSE_BARS:
        return None
    c   = ind["close"][pos]
    c_n = ind["close"][pos - _IMPULSE_BARS]
    a   = ind["atr"][pos]
    hi  = ind["high"][pos]
    lo  = ind["low"][pos]
    o   = ind["open"][pos]
    if nan(c, c_n, a, hi, lo, o) or a <= 0:
        return None
    impulse = c_n - c  # positive = price fell over the window (down-impulse)
    # Down-impulse exhaustion: price fell > 3*ATR, current bar closes higher than it opened
    if impulse > _IMPULSE_ATR * a:
        counter = c - min(o, lo)  # upward reversal size
        if counter >= _REVERSAL_ATR * a:
            return "long"
    # Up-impulse exhaustion: price rose > 3*ATR, current bar closes lower than it opened
    if impulse < -_IMPULSE_ATR * a:
        counter = max(o, hi) - c  # downward reversal size
        if counter >= _REVERSAL_ATR * a:
            return "short"
    return None
