#!/usr/bin/env python3
"""commodities_futures_trend_following_tsmom -- TSMOM: close vs ema50 trend sign. QuantConnect/Lemperiere 2014."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "commodities_futures_trend_following_tsmom",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1d",
    "indicators": "close, ema50, atr_pct",
    "long": "close > ema50 (price above 5-month EMA proxy, positive trend signal)",
    "short": "close < ema50 (price below 5-month EMA proxy, negative trend signal)",
    "desc": "Commodities futures TSMOM: trend direction from close vs EMA50 (5-month proxy)",
    "source": "QuantConnect Strategy Library; Lemperiere et al. Two Centuries Of Trend Following (2014)",
}


def signal(ind, pos, htf=None):
    """Long when close above ema50 (trend up); short when below (trend down)."""
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    if nan(c, e50):
        return None
    if c > e50:
        return "long"
    if c < e50:
        return "short"
    return None
