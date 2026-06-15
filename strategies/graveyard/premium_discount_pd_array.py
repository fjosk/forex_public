#!/usr/bin/env python3
"""premium_discount_pd_array -- ICT PD Array Premium/Discount zone entry. ICT / Michael Huddleston.

Buy only in the discount zone (below 50% of the frac_dn to frac_up dealing range)
when price touches the lower portion; sell only in the premium zone (above 50%).
Deep discount (<21%) and deep premium (>79%) are highest-probability zones.
Source: web:https://innercircletrader.net/tutorials/ict-pd-array-key-to-trade-execution/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "premium_discount_pd_array",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr",
    "long": "price in deep discount zone (<21% of dealing range) and touches frac_dn_px support; bullish close",
    "short": "price in deep premium zone (>79%) and touches frac_up_px resistance; bearish close",
    "desc": "ICT PD Array: enter in deep discount (long) or deep premium (short) zone of dealing range",
    "source": "web:https://innercircletrader.net/tutorials/ict-pd-array-key-to-trade-execution/",
}

_DEEP_DISCOUNT = 0.21   # below this fraction = deep discount
_DEEP_PREMIUM = 0.79    # above this fraction = deep premium


def signal(ind, pos, htf=None):
    """PD Array: enter at deep discount or deep premium relative to frac_lo/frac_hi dealing range."""
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

    pos_in_range = (c - frac_lo) / rng   # 0.0 = at low, 1.0 = at high

    # Long: deep discount zone; price touches frac_dn support and shows bullish close
    if pos_in_range < _DEEP_DISCOUNT and lo <= frac_lo * 1.001 and c > c1:
        return "long"

    # Short: deep premium zone; price touches frac_hi resistance and shows bearish close
    if pos_in_range > _DEEP_PREMIUM and hi >= frac_hi * 0.999 and c < c1:
        return "short"

    return None
