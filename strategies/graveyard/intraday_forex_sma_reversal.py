#!/usr/bin/env python3
"""intraday_forex_sma_reversal -- Intraday Forex SMA Mean Reversion. QuantConnect/Lean."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "intraday_forex_sma_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "close_sma5, hour_utc",
    "long": "close < close_sma5 * 1.001 within 15-20 UTC trading window",
    "short": "close > close_sma5 * 1.001 within 15-20 UTC trading window",
    "desc": "Intraday EURUSD SMA5 mean reversion during 10:00-15:00 ET window (15-20 UTC)",
    "source": "github.com/QuantConnect/Lean IntradayReversalCurrencyMarketsAlpha.py",
}

_WIN_START = 15  # 10:00 ET = ~15 UTC
_WIN_END = 20    # 15:00 ET = ~20 UTC


def signal(ind, pos, htf=None):
    """Price ~0.1% off SMA5 during the NY session window (15-20 UTC)."""
    c = ind["close"][pos]
    s5 = ind["close_sma5"][pos]
    hr = ind["hour_utc"][pos]
    if nan(c, s5, hr):
        return None
    if not (_WIN_START <= hr < _WIN_END):
        return None
    threshold = s5 * 1.001
    if c < threshold and c < s5:
        return "long"
    if c > threshold:
        return "short"
    return None
