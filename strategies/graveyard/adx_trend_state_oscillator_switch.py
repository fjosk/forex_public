#!/usr/bin/env python3
"""adx_trend_state_oscillator_switch -- ADX rising above 15 activates trend mode; enter in dominant-DI direction. Trade Your Way to Financial Freedom Ch.8.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_trend_state_oscillator_switch",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "adx,di_plus,di_minus",
    "long": "ADX rising AND ADX > 15 (trend regime) AND DI+ > DI-",
    "short": "ADX rising AND ADX > 15 (trend regime) AND DI- > DI+",
    "desc": "LeBeau ADX regime gate: ADX rising above 15 signals trend state; enter in DI-dominant direction",
    "source": "trade_your_way_to_financial_freedom_mabroke_blogsp Ch.8",
}


def signal(ind, pos, htf=None):
    """Trend-regime trigger: ADX rising > 15, direction from DI dominance."""
    if pos < 1:
        return None
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    if nan(adx, adx1, dip, dim):
        return None
    trending = adx > adx1 and adx > 15
    if not trending:
        return None
    if dip > dim:
        return "long"
    if dim > dip:
        return "short"
    return None
