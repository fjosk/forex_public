#!/usr/bin/env python3
"""range_reversal_at_oscillator_extreme_overbought_oversold_in_weak_adx_r -- Range trade: weak
ADX (< 25) + RSI at extreme (< 30 / > 70) + price near MA support/resistance -> fade.

Source: day_trading_swing_trading_the_currency_market_tech, Ch.8 Table 8.1.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "range_reversal_at_oscillator_extreme_overbought_oversold_in_weak_adx_r",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "adx, rsi, stoch_k, sma20, sma50, close",
    "long": "ADX < 25 AND (RSI < 30 OR stoch_k < 30) AND close near sma20 or sma50 support",
    "short": "ADX < 25 AND (RSI > 70 OR stoch_k > 70) AND close near sma20 or sma50 resistance",
    "desc": "Range oscillator extreme fade: weak ADX + overbought/oversold RSI/Stochastic near MA support/resistance",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.8 Table 8.1",
}

_ADX_RANGE = 25.0
_OS = 30.0
_OB = 70.0
_MA_TOL_ATR = 0.5  # within 0.5 ATR of an MA = "near MA"


def signal(ind, pos, htf=None):
    """Weak-ADX range: RSI/Stoch extreme near a key MA -> fade."""
    adx = ind["adx"][pos]
    r = ind["rsi"][pos]
    sk = ind["stoch_k"][pos]
    c = ind["close"][pos]
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    a = ind["atr"][pos]
    if nan(adx, r, sk, c, s20, s50, a) or a <= 0:
        return None
    if adx >= _ADX_RANGE:
        return None
    tol = _MA_TOL_ATR * a
    near_ma = abs(c - s20) <= tol or abs(c - s50) <= tol
    if not near_ma:
        return None
    if r < _OS or sk < _OS:
        return "long"
    if r > _OB or sk > _OB:
        return "short"
    return None
