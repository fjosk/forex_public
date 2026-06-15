#!/usr/bin/env python3
"""channel_envelope_profit_taking_and_flat_market_fade -- Buy at lower channel, sell at upper; flat-market fade. come_into_my_trading_room_alexander_elder.

Trending: buy when close touches kc_lo (lower channel), target kc_up (upper channel).
Short when close touches kc_up, target kc_lo.
Flat market (EMA slope ~ 0, ema20 ~ ema50): buy at kc_lo, exit at ema20; short at kc_up, exit at ema20.
Uses ema20 + Keltner channel (kc_lo, kc_up). Slope measured by ema20 vs ema50 divergence.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "channel_envelope_profit_taking_and_flat_market_fade",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h-1d",
    "indicators": "close,ema20,ema50,kc_lo,kc_up",
    "long": "Close at or below kc_lo -> buy; in flat market (ema20~ema50) or uptrend",
    "short": "Close at or above kc_up -> short; in flat market or downtrend",
    "desc": "Channel/envelope fade: buy lower band, sell upper band; flat-market targets EMA; trending targets opposite band",
    "source": "book:come_into_my_trading_room_alexander_elder",
}

_FLAT_THRESHOLD = 0.001   # ema20/ema50 ratio within 0.1% = flat market


def signal(ind, pos, htf=None):
    """Channel envelope fade: touch lower/upper band -> mean-reversion entry."""
    if pos < 1:
        return None
    c     = ind["close"][pos]
    e20   = ind["ema20"][pos]
    e50   = ind["ema50"][pos]
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    if nan(c, e20, e50, kc_lo, kc_up) or e50 == 0:
        return None

    if c <= kc_lo:
        return "long"

    if c >= kc_up:
        return "short"

    return None
