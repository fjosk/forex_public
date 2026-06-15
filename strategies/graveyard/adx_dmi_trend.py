#!/usr/bin/env python3
"""adx_dmi_trend -- ADX + DMI Trend Strategy.
web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/ADX%20-%20DMI%20Trend%20Strategy.pine
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "adx_dmi_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "adx, di_plus, di_minus, sma20",
    "long": "ADX slope positive AND ADX > 23 AND DI+ > DI- AND close >= sma20",
    "short": "ADX slope positive AND ADX > 23 AND DI- > DI+ AND close <= sma20",
    "desc": "ADX rising + directional movement + MA trend filter; drops FX volume gate",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/ADX%20-%20DMI%20Trend%20Strategy.pine",
}

_ADX_KEY = 23
_ADX_SLOPE_LOOKBACK = 5


def signal(ind, pos, htf=None):
    """ADX slope + DI direction + price above/below SMA20 trend filter."""
    if pos < _ADX_SLOPE_LOOKBACK:
        return None
    adx = ind["adx"][pos]
    adx_back = ind["adx"][pos - _ADX_SLOPE_LOOKBACK]
    dip = ind["di_plus"][pos]
    dim = ind["di_minus"][pos]
    c = ind["close"][pos]
    sma = ind["sma20"][pos]
    if nan(adx, adx_back, dip, dim, c, sma):
        return None
    adx_slope = adx > adx_back
    if not (adx_slope and adx > _ADX_KEY):
        return None
    if dip > dim and c >= sma:
        return "long"
    if dim > dip and c <= sma:
        return "short"
    return None
