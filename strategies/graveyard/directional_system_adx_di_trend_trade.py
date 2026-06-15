#!/usr/bin/env python3
"""directional_system_adx_di_trend_trade -- Elder ADX/DI trend trade: best long when DI+ and ADX both above DI- and ADX rising; best short mirror. Elder Trading for a Living Sec.27.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "directional_system_adx_di_trend_trade",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus",
    "long": "DI+ > DI- AND ADX > DI- AND ADX rising",
    "short": "DI- > DI+ AND ADX > DI+ AND ADX rising",
    "desc": "Elder Directional System best-signal: DI dominance + ADX above both DI lines + ADX rising confirms strong trend",
    "source": "elder_alexander_trading_for_a_living Sec.27 The Directional System",
}


def signal(ind, pos, htf=None):
    """Elder best-quality DI/ADX signal: dominant DI leads, ADX above minority DI and rising."""
    if pos < 1:
        return None
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    if nan(dip, dim, adx, adx1):
        return None
    adx_rising = adx > adx1
    if dip > dim and adx > dim and adx_rising:
        return "long"
    if dim > dip and adx > dip and adx_rising:
        return "short"
    return None
