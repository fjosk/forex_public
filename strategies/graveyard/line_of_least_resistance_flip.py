#!/usr/bin/env python3
"""line_of_least_resistance_flip -- Livermore: habitual rally/decline fails -> line of least resistance flips. reminiscences_of_a_stock_operator_edwin_lefevre.

Proxy: after a down-leg (close < ema20 by > 0.5*ATR), price fails to reclaim ema20 within 3 bars
(RSI stays below 50) -> line of resistance stays down -> short.
Mirror: after an up-leg, price fails to fall back below ema20 -> long.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "line_of_least_resistance_flip",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema20,rsi,atr",
    "long": "close > ema20 by > 0.5*ATR for 2+ bars AND rsi > 50 (price stays above EMA after down-leg = line flipped up)",
    "short": "close < ema20 by > 0.5*ATR for 2+ bars AND rsi < 50 (price stays below EMA after up-leg = line flipped down)",
    "desc": "Line-of-least-resistance flip: price refuses to return to its average (EMA + RSI confirm) = trend direction confirmed",
    "source": "reminiscences_of_a_stock_operator_edwin_lefevre, ch.XVII",
}


def signal(ind, pos, htf=None):
    """Persistent failure to return to mean signals line-of-least-resistance shift."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    ema = ind["ema20"][pos]
    ema1 = ind["ema20"][pos - 1]
    rs = ind["rsi"][pos]
    atr = ind["atr"][pos]
    if nan(c, c1, ema, ema1, rs, atr):
        return None
    band = 0.5 * atr
    # Both bars persistently above ema20 + RSI > 50 = bullish line confirmed
    above_both = (c > ema + band) and (c1 > ema1 + band)
    below_both = (c < ema - band) and (c1 < ema1 - band)
    if above_both and rs > 50:
        return "long"
    if below_both and rs < 50:
        return "short"
    return None
