#!/usr/bin/env python3
"""optimal_trade_entry_ote -- ICT Optimal Trade Entry Fibonacci zone. ICT / Michael Huddleston.

After structure shifts in the desired direction, price retraces to the
62-79% Fibonacci zone of the most recent impulse. Price must first cross below
50% (long) or above 50% (short) before the OTE band is valid.
Source: web:https://innercircletrader.net/tutorials/ict-optimal-trade-entry-ote-pattern/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "optimal_trade_entry_ote",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr",
    "long": "price retraces 62-79% of impulse (frac_dn to frac_up) and was below 50% midpoint; rejection candle",
    "short": "price retraces 62-79% of impulse (frac_up to frac_dn) and was above 50% midpoint; rejection candle",
    "desc": "ICT OTE: 62-79% Fibonacci retrace of prior impulse with 50% validity gate",
    "source": "web:https://innercircletrader.net/tutorials/ict-optimal-trade-entry-ote-pattern/",
}


def signal(ind, pos, htf=None):
    """OTE: price enters 62-79% fib retrace zone of prior impulse; close must have crossed below/above midpoint."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    lo = ind["low"][pos]
    hi = ind["high"][pos]
    frac_lo = ind["frac_dn_px"][pos]
    frac_hi = ind["frac_up_px"][pos]
    if nan(c, c1, lo, hi, frac_lo, frac_hi):
        return None

    rng = frac_hi - frac_lo
    if rng <= 0:
        return None

    mid = frac_lo + 0.50 * rng

    # Long OTE: impulse from frac_lo to frac_hi; retrace into 62-79% of that range from top
    ote_lo = frac_hi - 0.79 * rng   # deeper retrace = lower price
    ote_hi = frac_hi - 0.62 * rng   # shallower retrace = higher price
    # Price must have traded below midpoint (discount territory) at some point on this or prior bar
    was_below_mid = c1 < mid or lo < mid
    if was_below_mid and lo <= ote_hi and c >= ote_lo and c > c1:
        # Rejection confirm: current close above prior close (bullish reversal candle)
        return "long"

    # Short OTE: impulse from frac_hi to frac_lo; retrace into 62-79% of range from bottom
    ote_short_lo = frac_lo + 0.62 * rng   # lower boundary in premium
    ote_short_hi = frac_lo + 0.79 * rng   # upper boundary in premium
    was_above_mid = c1 > mid or hi > mid
    if was_above_mid and hi >= ote_short_lo and c <= ote_short_hi and c < c1:
        return "short"

    return None
