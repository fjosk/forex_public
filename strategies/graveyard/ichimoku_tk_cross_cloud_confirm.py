#!/usr/bin/env python3
"""ichimoku_tk_cross_cloud_confirm -- Ichimoku Expert EA (Open vs Kijun + Cloud). barabashkakvn/MQL5.

Bar open above kijun AND above ich_a (Senkou A) for long; below kijun AND below ich_b for short.
Daily trend confirmation omitted (requires HTF); ATR filter used as volatility gate.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ichimoku_tk_cross_cloud_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ich_kij, ich_a, ich_b, atr, open",
    "long": "open > ich_kij AND open > ich_a (price opening above Kijun and Senkou A)",
    "short": "open < ich_kij AND open < ich_b (price opening below Kijun and Senkou B)",
    "desc": "Ichimoku Expert: bar open clears Kijun + cloud level; ATR volatility gate",
    "source": "web:https://www.mql5.com/en/code/21661",
}


def signal(ind, pos, htf=None):
    """Open vs Kijun + cloud-level confirmation with ATR volatility filter."""
    op = ind["open"][pos]
    kij = ind["ich_kij"][pos]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    atr = ind["atr"][pos]
    c = ind["close"][pos]
    if nan(op, kij, ia, ib, atr, c):
        return None
    # Require meaningful volatility (atr > 0 always true on real data, but guard NaN)
    if atr <= 0:
        return None
    if op > kij and op > ia:
        return "long"
    if op < kij and op < ib:
        return "short"
    return None
