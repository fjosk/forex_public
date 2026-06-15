#!/usr/bin/env python3
"""turtle_soup -- ICT Turtle Soup false breakout reversal. ICT / Michael Huddleston.

Price briefly pierces a recent swing high/low (the wick) but the candle BODY closes
back inside the range. Spike must be 0.25-2.0 ATR in size. Targets range midpoint.
Source: web:https://innercircletrader.net/tutorials/ict-turtle-soup-pattern/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "turtle_soup",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr",
    "long": "low spikes below frac_dn_px by 0.25-2.0 ATR; body (close) returns above frac_dn_px on same bar",
    "short": "high spikes above frac_up_px by 0.25-2.0 ATR; body (close) returns below frac_up_px on same bar",
    "desc": "ICT Turtle Soup: spike-and-body-return false breakout reversal",
    "source": "web:https://innercircletrader.net/tutorials/ict-turtle-soup-pattern/",
}

_MIN_SPIKE = 0.25
_MAX_SPIKE = 2.0


def signal(ind, pos, htf=None):
    """Turtle Soup: wick pierces fractal level; body closes back inside; ATR-gated spike."""
    c = ind["close"][pos]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    atr = ind["atr"][pos]
    if nan(c, lo, hi, frac_lo, frac_hi, atr) or atr == 0:
        return None

    # Long: wick below fractal low; body returns above it (same bar)
    if lo < frac_lo and c > frac_lo:
        spike = frac_lo - lo
        if _MIN_SPIKE * atr <= spike <= _MAX_SPIKE * atr:
            return "long"

    # Short: wick above fractal high; body returns below it (same bar)
    if hi > frac_hi and c < frac_hi:
        spike = hi - frac_hi
        if _MIN_SPIKE * atr <= spike <= _MAX_SPIKE * atr:
            return "short"

    return None
