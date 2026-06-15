#!/usr/bin/env python3
"""rsi_forex_skewness_risk_premia -- Rolling return skewness regime signal. QC FX Skewness.

Long when rolling skewness of daily close returns < -0.6 (negatively skewed, positive upside ahead).
Short when skewness > +0.6. Skewness computed inline from close array over a 20-bar lookback.
Weekly-rebalance style: only signals at week boundary (dow == 1, Monday bars).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_forex_skewness_risk_premia",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1d",
    "indicators": "close, dow",
    "long": "rolling 20-bar return skewness < -0.6 (negative skew = positive tail expected)",
    "short": "rolling 20-bar return skewness > +0.6 (positive skew = downside risk ahead)",
    "desc": "FX return skewness risk premia: fade positive skew, ride negative skew; weekly rebalance",
    "source": "web:https://www.quantconnect.com/learning/articles/investment-strategy-library/risk-premia-in-forex-markets",
}

_N = 20


def signal(ind, pos, htf=None):
    """Rolling skewness of returns over 20 bars; signal only on Monday (weekly rebalance)."""
    if pos < _N + 1:
        return None
    dow = ind["dow"][pos]
    if nan(dow):
        return None
    # Only fire on Monday (dow == 1) for weekly-rebalance style
    if dow != 1:
        return None
    closes = ind["close"]
    c0 = closes[pos - _N - 1]
    if nan(c0):
        return None
    # Compute returns and their skewness
    rets = []
    for i in range(pos - _N, pos + 1):
        c_prev = closes[i - 1]
        c_cur = closes[i]
        if nan(c_prev, c_cur) or c_prev == 0:
            return None
        rets.append((c_cur - c_prev) / c_prev)
    n = len(rets)
    if n < 3:
        return None
    mu = sum(rets) / n
    var = sum((r - mu) ** 2 for r in rets) / n
    if var <= 0:
        return None
    sigma = var ** 0.5
    skew = sum((r - mu) ** 3 for r in rets) / (n * sigma ** 3)
    if skew < -0.6:
        return "long"
    if skew > 0.6:
        return "short"
    return None
