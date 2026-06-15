#!/usr/bin/env python3
"""channel_envelope_mean_reversion_swing_trade -- Buy near rising EMA; sell at upper channel. come_into_my_trading_room_alexander_elder.

Elder: in uptrend (close > EMA20 + EMA sloping up), buy when price pulls back to EMA.
In downtrend, short when price rallies to EMA. Exit at upper/lower Keltner channel line.
Uses ema20 as the centerline and kc_lo/kc_up as the channel envelope.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "channel_envelope_mean_reversion_swing_trade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "close,ema20,ema50,kc_lo,kc_up",
    "long": "Price touches or dips below ema20 AND ema20 > ema50 (uptrend context) AND kc_lo below",
    "short": "Price touches or rises above ema20 AND ema20 < ema50 (downtrend context) AND kc_up above",
    "desc": "Channel envelope swing trade: buy at EMA in uptrend, short at EMA in downtrend, target opposite channel",
    "source": "book:come_into_my_trading_room_alexander_elder",
}


def signal(ind, pos, htf=None):
    """Channel swing trade: fade to EMA in trend direction."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    e20  = ind["ema20"][pos]
    e50  = ind["ema50"][pos]
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    if nan(c, e20, e50, kc_lo, kc_up):
        return None

    # Uptrend: ema20 above ema50; price pulls back to ema20 from above
    if e20 > e50 and c <= e20 and c > kc_lo:
        return "long"

    # Downtrend: ema20 below ema50; price rallies back to ema20 from below
    if e20 < e50 and c >= e20 and c < kc_up:
        return "short"

    return None
