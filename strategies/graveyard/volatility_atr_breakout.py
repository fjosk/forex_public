#!/usr/bin/env python3
"""volatility_atr_breakout -- Volatility ATR directional breakout: close change > ATR*2. freqtrade VolatilitySystem.

When the magnitude of the close-to-close change on the current bar exceeds the prior bar's ATR * 2,
enter in the direction of the move. Exits on the opposing signal (TREND_FLIP). Adapted for any
timeframe (no 3m resampling required; rule is bar-native).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "volatility_atr_breakout",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "atr, close",
    "long": "close - close[1] > ATR[1] * 2.0 (large bullish bar exceeds prior ATR threshold)",
    "short": "close[1] - close > ATR[1] * 2.0 (large bearish bar exceeds prior ATR threshold)",
    "desc": "Volatility ATR directional breakout: bar close-change magnitude exceeds 2x previous ATR",
    "source": "https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/futures/VolatilitySystem.py",
}

_ATR_MULT = 2.0


def signal(ind, pos, htf=None):
    """Close-change vs ATR threshold breakout."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    atr1 = ind["atr"][pos - 1]
    if nan(c, c1, atr1):
        return None
    threshold = _ATR_MULT * atr1
    change = c - c1
    if change > threshold:
        return "long"
    if -change > threshold:
        return "short"
    return None
