#!/usr/bin/env python3
"""shooting_star_star_top -- Shooting star / star top: small body at low end of range, long upper shadow, at top. j_person_a_complete_guide_to_technical_trading_tac.

Star: small real body at the lower end of bar range with a long upper shadow and little/no lower
shadow. Optional gap above prior bar. Signals failed rally / reversal down. Bearish only.
Trend context via EMA50. This is a more general star pattern (also covers morning-doji-star type
shapes at tops).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "shooting_star_star_top",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h-4h",
    "indicators": "open,high,low,close,ema50",
    "long": "none (star top is short-only)",
    "short": "Small body at lower end of bar range; upper shadow >= 2x body; lower shadow ~ 0; optional gap above prior; prior uptrend",
    "desc": "Shooting star / star top: small body near low of bar with long upper wick signals bearish reversal",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}

_SHADOW_RATIO = 2.0    # upper shadow >= 2x body
_LOWER_MAX    = 0.25   # lower shadow <= 25% of upper shadow
_BODY_TOP_MAX = 0.35   # body must sit in the lower 35% of bar range (shaved bottom)


def signal(ind, pos, htf=None):
    """Star top: small body at session low with long upper wick signals reversal."""
    if pos < 1:
        return None
    o   = ind["open"][pos]
    h   = ind["high"][pos]
    lo  = ind["low"][pos]
    c   = ind["close"][pos]
    ema = ind["ema50"][pos]
    if nan(o, h, lo, c, ema):
        return None

    # Require prior uptrend
    if c <= ema:
        return None

    body       = abs(c - o)
    upper_shad = h - max(o, c)
    lower_shad = min(o, c) - lo
    bar_range  = h - lo

    if bar_range == 0:
        return None

    # Body must sit near the low of the bar (shaved bottom)
    body_top_from_low = max(o, c) - lo
    if body_top_from_low > _BODY_TOP_MAX * bar_range:
        return None                     # body too high in the bar

    if (upper_shad >= _SHADOW_RATIO * max(body, 1e-10) and
            lower_shad <= _LOWER_MAX * upper_shad):
        return "short"

    return None
