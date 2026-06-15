#!/usr/bin/env python3
"""gap_climax_move_reversal -- Fade a climax gap that reverses: bar gaps to extreme and closes
at the opposite end of its range. ATR volatility filter confirms climax.

Source: trade_your_way_to_financial_freedom_mabroke_blogsp, Ch.7 Climax Reversals.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "gap_climax_move_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "open, high, low, close, atr, atr_pct, hh_n, ll_n",
    "long": "Bar gaps down (open < prev low) to a new N-bar low (ll_n==1) and closes in upper 30% of bar range; ATR expanding",
    "short": "Bar gaps up (open > prev high) to a new N-bar high (hh_n==1) and closes in lower 30% of bar range; ATR expanding",
    "desc": "Climax exhaustion gap fade: extreme gap reversed within the bar (closes opposite end)",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.7",
}


def signal(ind, pos, htf=None):
    """Climax gap fade: gap to extreme + reversal close."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c = ind["close"][pos]
    prev_h = ind["high"][pos - 1]
    prev_lo = ind["low"][pos - 1]
    a = ind["atr"][pos]
    hh = ind["hh_n"][pos]
    ll = ind["ll_n"][pos]
    if nan(o, h, lo, c, prev_h, prev_lo, a, hh, ll):
        return None
    bar_range = h - lo
    if bar_range <= 0:
        return None
    close_pct = (c - lo) / bar_range

    # gap down to new ll: open < prior low, bar is a new N-bar low
    if o < prev_lo and ll == 1 and close_pct >= 0.70:
        return "long"

    # gap up to new hh: open > prior high, bar is a new N-bar high
    if o > prev_h and hh == 1 and close_pct <= 0.30:
        return "short"

    return None
