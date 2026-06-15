#!/usr/bin/env python3
"""prior_day_range_support_resistance_fade_limit_at_range_edges -- Fade approaches to prior-day
high/low: buy near prior-day low, sell near prior-day high.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.16.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "prior_day_range_support_resistance_fade_limit_at_range_edges",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "close, prev_dhh, prev_dll, atr",
    "long": "Close within 0.25*ATR above prev_dll (approaching prior-day low support)",
    "short": "Close within 0.25*ATR below prev_dhh (approaching prior-day high resistance)",
    "desc": "Prior-day range edge fade: buy near prior-day low support, sell near prior-day high resistance",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.16",
}


def signal(ind, pos, htf=None):
    """Fade approaches to prior-day H/L range edges."""
    c = ind["close"][pos]
    pdh = ind["prev_dhh"][pos]
    pdl = ind["prev_dll"][pos]
    a = ind["atr"][pos]
    if nan(c, pdh, pdl, a) or a <= 0 or pdh <= pdl:
        return None
    buf = 0.25 * a
    if c <= pdl + buf:
        return "long"
    if c >= pdh - buf:
        return "short"
    return None
