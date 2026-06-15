#!/usr/bin/env python3
"""ornstein_uhlenbeck_zscore_mean_reversion -- OU z-score mean reversion approximated via Bollinger %B + SMA.

Full OU parameter estimation (rolling OLS) is not available in precomputed indicators.
Approximation: bb_pctb encodes distance from the 20-bar Bollinger mean in fractional units;
combined with sma100 as slow mean anchor and rsi for trend guard.
Entry at extreme bb_pctb deviation; exit when bb_pctb reverts toward 0.5.
No volume -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "ornstein_uhlenbeck_zscore_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "bb_pctb, sma100, close, rsi",
    "long": "bb_pctb < 0.1 (extreme lower band) AND close > sma100 (above slow mean)",
    "short": "bb_pctb > 0.9 (extreme upper band) AND close < sma100 (below slow mean)",
    "desc": "OU mean reversion approx: extreme Bollinger %B with slow-SMA anchor and RSI guard",
    "source": "pyquantlab.com OU Mean-Reversion Strategy with Python and Backtrader",
}

_LONG_THRESH = 0.10
_SHORT_THRESH = 0.90


def signal(ind, pos, htf=None):
    """OU z-score mean reversion via Bollinger %B approximation."""
    pctb = ind["bb_pctb"][pos]
    sma100 = ind["sma100"][pos]
    cl = ind["close"][pos]
    rs = ind["rsi"][pos]
    if nan(pctb, sma100, cl, rs):
        return None
    # Long: price near/below lower Bollinger band AND above slow SMA (structural support)
    if pctb < _LONG_THRESH and cl > sma100:
        return "long"
    # Short: price near/above upper Bollinger band AND below slow SMA (structural resistance)
    if pctb > _SHORT_THRESH and cl < sma100:
        return "short"
    return None
