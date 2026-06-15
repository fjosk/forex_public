#!/usr/bin/env python3
"""freqtrade_stoch_adx_cci_exit -- Stochastic overbought/oversold + ADX trend fade. freqtrade Strategy004.

Strategy004 defines an exit trigger (overbought stochastic + weakening ADX + close above EMA5).
Adapted as a full mean-reversion signal: short when stochastic overbought AND ADX weak AND close
above EMA5 (fade the peak); long when stochastic oversold AND ADX weak AND close below EMA5 (fade
the trough). REVERT archetype with a tight time stop suits the mean-reversion style.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_stoch_adx_cci_exit",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "5m",
    "indicators": "adx, stoch_k, stoch_d, ema5",
    "long": "ADX(14) smoothed < 25 AND (stoch_k < 30 OR stoch_d < 30) AND close < ema5 (oversold fade)",
    "short": "ADX smoothed < 25 AND (stoch_k > 70 OR stoch_d > 70) AND close > ema5 (overbought fade)",
    "desc": "Stochastic overbought/oversold fade with ADX weakness gate; adapted from freqtrade Strategy004 exit",
    "source": "https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/Strategy004.py",
}

_ADX_WEAK = 25.0
_OB = 70.0
_OS = 30.0


def _slow_adx(ind, pos, period=5):
    """Simple moving average of ADX over last `period` bars (smoothed ADX)."""
    if pos < period:
        return None
    vals = ind["adx"][pos - period + 1: pos + 1]
    if any(v != v or v is None for v in vals):
        return None
    return float(sum(vals)) / period


def signal(ind, pos, htf=None):
    """Stochastic overbought/oversold fade with weakening ADX."""
    slow_adx = _slow_adx(ind, pos)
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    e5 = ind["ema5"][pos]
    c = ind["close"][pos]
    if nan(slow_adx, sk, sd, e5, c):
        return None
    if slow_adx >= _ADX_WEAK:
        return None
    # Short: overbought stochastic + close above EMA5
    if (sk > _OB or sd > _OB) and c > e5:
        return "short"
    # Long: oversold stochastic + close below EMA5
    if (sk < _OS or sd < _OS) and c < e5:
        return "long"
    return None
