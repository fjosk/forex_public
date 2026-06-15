#!/usr/bin/env python3
"""market_structure_shift_mss -- Market Structure Shift displacement entry. ICT / SMC community.

After a fractal sweep a large displacement candle (body > 1.0 ATR) closes beyond
the prior fractal in the reversal direction, confirming the MSS. Entry taken on
that bar.
Source: web:https://tradingfinder.com/education/forex/ict-mss/
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "market_structure_shift_mss",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, open, high, low, frac_up_px, frac_dn_px, atr",
    "long": "prior bar sweeps below frac_dn_px; current bar body > 1.0 ATR bullish AND close above frac_up_px",
    "short": "prior bar sweeps above frac_up_px; current bar body > 1.0 ATR bearish AND close below frac_dn_px",
    "desc": "ICT Market Structure Shift: sweep then large displacement body beyond prior fractal",
    "source": "web:https://tradingfinder.com/education/forex/ict-mss/",
}


def signal(ind, pos, htf=None):
    """MSS: prior bar sweeps fractal; current bar has large displacement body closing through opposite fractal."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    o = ind["open"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    atr = ind["atr"][pos]
    lo_prev = ind["low"][pos - 1]
    hi_prev = ind["high"][pos - 1]
    frac_lo_prev = ind["frac_dn_px"][pos - 1]
    frac_hi_prev = ind["frac_up_px"][pos - 1]
    if nan(c, o, frac_lo, frac_hi, atr, lo_prev, hi_prev, frac_lo_prev, frac_hi_prev):
        return None
    if atr == 0:
        return None

    body = abs(c - o)

    # Long MSS: prior bar swept below fractal low; current bar has large bullish body
    # closing above the prior fractal high (structural flip)
    if lo_prev < frac_lo_prev and c > o and body >= 1.0 * atr and c > frac_hi_prev:
        return "long"

    # Short MSS: prior bar swept above fractal high; current bar large bearish body
    # closing below the prior fractal low
    if hi_prev > frac_hi_prev and c < o and body >= 1.0 * atr and c < frac_lo_prev:
        return "short"

    return None
