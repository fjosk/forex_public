#!/usr/bin/env python3
"""rsi_bb_ema_trend -- RSI > 50 + close > bb_mid + close > ema50 triple confirmation. tradingpedia.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "rsi_bb_ema_trend",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "rsi, bb_mid, ema50",
    "long": "close > ema50 AND close > bb_mid AND rsi > 50 (all three bull)",
    "short": "close < ema50 AND close < bb_mid AND rsi <= 50 (all three bear)",
    "desc": "TradingPedia triple-filter: EMA50 trend + Bollinger mid + RSI 50 all agree",
    "source": "web:https://www.tradingpedia.com/forex-trading-strategies/combining-relative-strength-index-bollinger-bands-and-emas/",
}


def signal(ind, pos, htf=None):
    """All three filters must agree: ema50, bb_mid, rsi."""
    c = ind["close"][pos]
    cp = ind["close"][pos - 1]
    e50 = ind["ema50"][pos]
    e50p = ind["ema50"][pos - 1]
    bbm = ind["bb_mid"][pos]
    rs = ind["rsi"][pos]
    if nan(c, cp, e50, e50p, bbm, rs):
        return None
    # Only fire on the bar where the state first becomes valid (transition)
    bull_now = c > e50 and c > bbm and rs > 50
    bull_prev = cp > e50p and cp > bbm
    bear_now = c < e50 and c < bbm and rs <= 50
    bear_prev = cp < e50p and cp < bbm
    if bull_now and not bull_prev:
        return "long"
    if bear_now and not bear_prev:
        return "short"
    return None
