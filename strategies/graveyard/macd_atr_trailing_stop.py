#!/usr/bin/env python3
"""macd_atr_trailing_stop -- MACD crossover on pullback (SMA20 declining). mementum backtrader."""
from strategies._common import nan, TREND, _xup, ALL_CLASSES

# Source uses SMA30; sma20 is the closest available key.
# Trailing stop logic is handled by the engine exit module (TREND archetype includes chandelier trail).

META = {
    "id": "macd_atr_trailing_stop",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "macd, macd_sig, sma20",
    "long": "MACD crosses above signal AND sma20 is below its value 10 bars ago (pullback context)",
    "short": "not used (long-only per source)",
    "desc": "MACD crossover entry on SMA pullback; ATR trailing stop via engine exit archetype",
    "source": "https://github.com/mementum/backtrader/blob/master/samples/macd-settings/macd-settings.py",
}

_SMA_LOOKBACK = 10


def signal(ind, pos, htf=None):
    """MACD cross above signal with SMA20 in declining context."""
    if pos < _SMA_LOOKBACK:
        return None
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    m1 = ind["macd"][pos - 1]
    ms1 = ind["macd_sig"][pos - 1]
    s20 = ind["sma20"][pos]
    s20_lag = ind["sma20"][pos - _SMA_LOOKBACK]
    if nan(m, ms, m1, ms1, s20, s20_lag):
        return None
    sma_declining = s20 < s20_lag
    if _xup(m, m1, ms, ms1) and sma_declining:
        return "long"
    return None
