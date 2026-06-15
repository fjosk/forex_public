#!/usr/bin/env python3
"""adx_regime_mean_reversion_filter -- ADX regime-adaptive mean reversion / trend switch. Quant-Signals.

ADX < 25: range-bound regime -> fade RSI extremes (mean reversion).
ADX > 25: trending regime -> follow DI direction with ema50/sma200 alignment.
Source: web:https://quant-signals.com/adx-trading-strategy/
"""
from strategies._common import nan, REVERT, TREND, ALL_CLASSES

META = {
    "id": "adx_regime_mean_reversion_filter",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "adx, di_plus, di_minus, rsi, bb_pctb, willr, ema50, sma200",
    "long": "range (ADX<25): RSI<30 or bb_pctb<0 or willr<-80; trend (ADX>25): di_plus>di_minus and ema50>sma200",
    "short": "range (ADX<25): RSI>70 or bb_pctb>1 or willr>-20; trend (ADX>25): di_minus>di_plus and ema50<sma200",
    "desc": "ADX regime switch: mean reversion in low-ADX ranges, trend-follow in high-ADX moves",
    "source": "web:https://quant-signals.com/adx-trading-strategy/",
}

_ADX_RANGE = 25.0
_ADX_TREND = 25.0


def signal(ind, pos, htf=None):
    """ADX-adaptive: range mode uses RSI/bbpctb/willr fade; trend mode uses DI+ema direction."""
    adx = ind["adx"][pos]
    rsi = ind["rsi"][pos]
    bb = ind["bb_pctb"][pos]
    willr = ind["willr"][pos]
    di_p = ind["di_plus"][pos]
    di_m = ind["di_minus"][pos]
    e50 = ind["ema50"][pos]
    s200 = ind["sma200"][pos]
    if nan(adx, rsi, bb, willr, di_p, di_m, e50, s200):
        return None

    if adx < _ADX_RANGE:
        # Range mode: mean reversion
        if rsi < 30 or bb < 0.0 or willr < -80:
            return "long"
        if rsi > 70 or bb > 1.0 or willr > -20:
            return "short"
    elif adx > _ADX_TREND:
        # Trend mode: directional momentum
        if di_p > di_m and e50 > s200:
            return "long"
        if di_m > di_p and e50 < s200:
            return "short"

    return None
