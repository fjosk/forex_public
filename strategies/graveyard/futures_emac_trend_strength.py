#!/usr/bin/env python3
"""futures_emac_trend_strength -- EMA crossover volatility-normalized forecast. QuantConnect Baltas."""
from strategies._common import nan, TREND, ALL_CLASSES

# ema13 ~ ema16 (fast), ema50 ~ ema64 (slow). atr_pct as volatility denominator proxy.

META = {
    "id": "futures_emac_trend_strength",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ema13, ema50, atr_pct",
    "long": "ema13 - ema50 normalized by atr_pct > 0 (positive trend forecast)",
    "short": "ema13 - ema50 normalized by atr_pct < 0 (negative trend forecast)",
    "desc": "EMAC volatility-normalized trend forecast (Carver Systematic Trading methodology)",
    "source": "https://www.quantconnect.com/research/15875/futures-fast-trend-following-with-trend-strength/",
}

_SCALAR = 4.1
_BUFFER = 0.05  # 5% of max forecast=20 as dead band to avoid hairpin trades


def signal(ind, pos, htf=None):
    """EMA crossover divided by ATR_pct as volatility proxy; sign = direction."""
    e13 = ind["ema13"][pos]
    e50 = ind["ema50"][pos]
    ap = ind["atr_pct"][pos]
    if nan(e13, e50, ap) or ap == 0:
        return None
    emac = e13 - e50
    raw = emac / ap
    capped = max(-20.0, min(20.0, raw * _SCALAR))
    if capped > _BUFFER:
        return "long"
    if capped < -_BUFFER:
        return "short"
    return None
