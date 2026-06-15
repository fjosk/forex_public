#!/usr/bin/env python3
"""cci_50_system -- CCI Dr. Bob: ZLC pattern (cci zero-cross with ema50 filter). ForexFactory/Dr.Bob."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "cci_50_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "cci, ema50",
    "long": "CCI(14) crosses above zero AND close > ema50 (ZLC pattern; CCI50 approximated by CCI14 + ema50 trend)",
    "short": "CCI(14) crosses below zero AND close < ema50",
    "desc": "CCI-50 System ZLC pattern: CCI zero-line cross with EMA50 trend filter (CCI50 not available; use CCI14+ema50)",
    "source": "web:https://www.forexfactory.com/thread/27536-cci-50-system",
}


def signal(ind, pos, htf=None):
    """CCI zero-line cross with ema50 trend filter (approximation of Dr. Bob ZLC with available indicators)."""
    cc = ind["cci"][pos]
    ccp = ind["cci"][pos - 1]
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(cc, ccp, c, e50):
        return None
    cci_cross_up = cc > 0 and ccp <= 0
    cci_cross_dn = cc < 0 and ccp >= 0
    above = c > e50
    if cci_cross_up and above:
        return "long"
    if cci_cross_dn and not above:
        return "short"
    return None
