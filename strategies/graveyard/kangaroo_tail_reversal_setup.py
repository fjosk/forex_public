#!/usr/bin/env python3
"""kangaroo_tail_reversal_setup -- Single tall-wick bar that pokes beyond range then closes back. come_into_my_trading_room_alexander_elder.

Kangaroo tail: a bar with an unusually long shadow relative to body and neighbours. Down-pointing
(long lower shadow) at or below recent support = buy; up-pointing (long upper shadow) at or above
recent resistance = sell. Lower shadow at least 2x body, upper shadow small (and vice versa for
the short setup). Uses Donchian channel as the support/resistance proxy.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "kangaroo_tail_reversal_setup",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close,atr,dc_lo,dc_up",
    "long": "Long lower shadow >= 2x body AND low pokes below recent Donchian low; upper shadow small",
    "short": "Long upper shadow >= 2x body AND high pokes above recent Donchian high; lower shadow small",
    "desc": "Kangaroo tail reversal: tall single-wick bar probing beyond S/R then snapping back",
    "source": "book:come_into_my_trading_room_alexander_elder",
}

_SHADOW_RATIO = 2.0   # shadow must be >= 2x body
_TAIL_ATR     = 1.0   # minimum shadow length in ATR multiples (filters tiny-range bars)


def signal(ind, pos, htf=None):
    """Kangaroo tail: long shadow pokes beyond S/R; body stays near the other end."""
    if pos < 1:
        return None
    o   = ind["open"][pos]
    h   = ind["high"][pos]
    lo  = ind["low"][pos]
    c   = ind["close"][pos]
    atr = ind["atr"][pos]
    sup = ind["dc_lo"][pos-1]   # prior-bar Donchian low as support
    res = ind["dc_up"][pos-1]   # prior-bar Donchian high as resistance
    if nan(o, h, lo, c, atr, sup, res) or atr == 0:
        return None

    body        = abs(c - o)
    upper_shad  = h - max(o, c)
    lower_shad  = min(o, c) - lo

    # Bullish kangaroo tail: long lower shadow pokes below support, body near top
    if (lower_shad >= _SHADOW_RATIO * max(body, 1e-10) and
            lower_shad >= _TAIL_ATR * atr and
            upper_shad <= 0.5 * lower_shad and
            lo <= sup):
        return "long"

    # Bearish kangaroo tail: long upper shadow pokes above resistance, body near bottom
    if (upper_shad >= _SHADOW_RATIO * max(body, 1e-10) and
            upper_shad >= _TAIL_ATR * atr and
            lower_shad <= 0.5 * upper_shad and
            h >= res):
        return "short"

    return None
