#!/usr/bin/env python3
"""inducement_liquidity_trap -- ICT inducement liquidity trap: false breakout + reversal.

The "inducement" is a minor fractal that lures retail traders into a false breakout.
Price sweeps the inducement fractal, then reverses aggressively. Enter on the reversal.

Long: price sweeps below the most recent minor low (frac_dn_px sweep), then the bar
      closes back above that swept level -- the trap has fired, enter long.
Short: price sweeps above frac_up_px, closes back below -- enter short.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "inducement_liquidity_trap",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m, 1h, 4h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr",
    "long": "price sweeps below recent frac_dn_px (minor low), body closes back above -- trap fired",
    "short": "price sweeps above recent frac_up_px (minor high), body closes back below -- trap fired",
    "desc": "Inducement liquidity trap: minor fractal sweep + body reversal entry",
    "source": "web:https://acy.com/en/market-news/education/smc-playbook-series-part-2-spot-liquidity-pools-trading-j-o-103837/",
}


def signal(ind, pos, htf=None):
    """Inducement liquidity trap signal."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    fup = ind["frac_up_px"][pos - 1]
    fdn = ind["frac_dn_px"][pos - 1]
    if nan(c, h, l, fup, fdn):
        return None
    # Sweep below frac_dn then close back above (bullish trap reversal)
    if l < fdn and c > fdn:
        return "long"
    # Sweep above frac_up then close back below (bearish trap reversal)
    if h > fup and c < fup:
        return "short"
    return None
