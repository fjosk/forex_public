#!/usr/bin/env python3
"""doji_reversal_confirmation_gated -- Doji after a directional move triggers a pending reversal;
entry confirmed only when a subsequent Donchian break occurs in the reversal direction.
Currency Trading for Dummies 2nd Ed., Ch.11."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "doji_reversal_confirmation_gated",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,dc_up,dc_lo,ema20",
    "long": "doji after decline (close below ema20), then close > dc_up confirmation",
    "short": "doji after advance (close above ema20), then close < dc_lo confirmation",
    "desc": "Doji reversal confirmation-gated: doji signals stall, entry only on subsequent level break",
    "source": "Currency Trading for Dummies 2nd Ed., Ch.11 'Doji'",
}

_BODY_RATIO = 0.10   # doji: body <= 10% of bar range
_LOOKBACK = 3        # check prior N bars for doji after a move


def signal(ind, pos, htf=None):
    """Doji in prior 3 bars, then current bar breaks Donchian in reversal direction."""
    if pos < _LOOKBACK + 1:
        return None
    c = ind["close"][pos]
    dc_hi = ind["dc_up"][pos]
    dc_lo = ind["dc_lo"][pos]
    ema = ind["ema20"][pos]
    if nan(c, dc_hi, dc_lo, ema):
        return None
    # Check if there was a doji in the prior LOOKBACK bars
    found_doji_after_decline = False
    found_doji_after_advance = False
    for k in range(1, _LOOKBACK + 1):
        o_k = ind["open"][pos - k]
        h_k = ind["high"][pos - k]
        l_k = ind["low"][pos - k]
        c_k = ind["close"][pos - k]
        if nan(o_k, h_k, l_k, c_k):
            continue
        rng = h_k - l_k
        if rng <= 0:
            continue
        if abs(c_k - o_k) <= _BODY_RATIO * rng:
            if c_k < ema:
                found_doji_after_decline = True
            elif c_k > ema:
                found_doji_after_advance = True
    # Confirmation breakout
    if found_doji_after_decline and c > dc_hi:
        return "long"
    if found_doji_after_advance and c < dc_lo:
        return "short"
    return None
