#!/usr/bin/env python3
"""doji_pause_stall_reversal_candle_at_a_major_level -- Doji at a major level (pivot S/R):
small body relative to range signals indecision/reversal at a key price zone.
Thirty Days of Forex Trading, Day 25."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "doji_pause_stall_reversal_candle_at_a_major_level",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr,piv_s1,piv_r1,ema20",
    "long": "doji (body < 10% of range) near pivot S1 with price below ema20 (at support in downtrend)",
    "short": "doji near pivot R1 with price above ema20 (at resistance in uptrend)",
    "desc": "Doji stall/pause reversal at pivot S/R zone with trend context",
    "source": "Thirty Days of Forex Trading, Day 25 (doji at matched low/major level)",
}

_BODY_RATIO = 0.10   # body <= 10% of range = doji
_ZONE_ATR = 1.0      # within 1 ATR of pivot level


def signal(ind, pos, htf=None):
    """Doji at pivot S/R zone with ema20 trend context."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    a = ind["atr"][pos]
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    ema = ind["ema20"][pos]
    if nan(o, h, l, c, a, s1, r1, ema):
        return None
    rng = h - l
    if rng <= 0:
        return None
    body = abs(c - o)
    # Is it a doji?
    if body > _BODY_RATIO * rng:
        return None
    zone = _ZONE_ATR * a
    # Bullish doji at support in downtrend
    if abs(c - s1) <= zone and c < ema:
        return "long"
    # Bearish doji at resistance in uptrend
    if abs(c - r1) <= zone and c > ema:
        return "short"
    return None
