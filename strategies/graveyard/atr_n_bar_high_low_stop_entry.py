#!/usr/bin/env python3
"""atr_n_bar_high_low_stop_entry -- ATR-filtered N-bar Donchian breakout. web:mql5.com/SafeScalperPro."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "atr_n_bar_high_low_stop_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "hh_n, ll_n, atr, close",
    "long": "close > hh_n + 0.5*ATR (N-bar high plus ATR buffer)",
    "short": "close < ll_n - 0.5*ATR (N-bar low minus ATR buffer)",
    "desc": "ATR-filtered N-bar high/low Donchian stop-entry (SafeScalperPro variant)",
    "source": "web:https://www.mql5.com/en/market/product/165581",
}

_ATR_BUF = 0.5


def signal(ind, pos, htf=None):
    """Close breaks above N-bar high + ATR buffer, or below N-bar low - ATR buffer."""
    cl = ind["close"][pos]
    hhn = ind["hh_n"][pos]
    lln = ind["ll_n"][pos]
    atr = ind["atr"][pos]
    if nan(cl, hhn, lln, atr):
        return None
    if cl > hhn + _ATR_BUF * atr:
        return "long"
    if cl < lln - _ATR_BUF * atr:
        return "short"
    return None
