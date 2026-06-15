#!/usr/bin/env python3
"""adx_rising_di_directional -- ADX Rising with DI Direction.
web:https://github.com/zeta-zetra/code
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_rising_di_directional",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "adx, di_plus, di_minus",
    "long": "ADX > 15 AND ADX > prev_ADX + 0.4 AND DI+ > DI-",
    "short": "ADX > 15 AND ADX > prev_ADX + 0.4 AND DI- > DI+",
    "desc": "Rising ADX (by 0.4 vs prior bar) above 15 confirms strengthening trend with DI direction",
    "source": "web:https://github.com/zeta-zetra/code",
}


def signal(ind, pos, htf=None):
    """ADX above 15 and rising by 0.4 vs prior bar, directioned by DI+/DI-."""
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    if nan(adx, adx1, dip, dim):
        return None
    if adx <= 15 or adx <= adx1 + 0.4:
        return None
    if dip > dim:
        return "long"
    if dim > dip:
        return "short"
    return None
