#!/usr/bin/env python3
"""macd_trend_signal_crossover -- Normalized MACD delta vs 0.25% price threshold. QuantConnect Lean."""
from strategies._common import nan, TREND, ALL_CLASSES

# Source uses 0.0025 equity threshold; kept as-is (same scale concern as macd_alpha_model_normalized
# but this spec is for stocks so the original number is preserved).

META = {
    "id": "macd_trend_signal_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "macd, macd_sig, close",
    "long": "(macd - macd_sig) / close > 0.0025",
    "short": "(macd - macd_sig) / close < -0.0025",
    "desc": "MACD normalized signal delta vs price threshold (QuantConnect MACDTrendAlgorithm)",
    "source": "https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/MACDTrendAlgorithm.py",
}

_THRESHOLD = 0.0025


def signal(ind, pos, htf=None):
    """Normalized MACD delta entry."""
    m = ind["macd"][pos]
    ms = ind["macd_sig"][pos]
    c = ind["close"][pos]
    if nan(m, ms, c) or c == 0:
        return None
    delta = (m - ms) / c
    if delta > _THRESHOLD:
        return "long"
    if delta < -_THRESHOLD:
        return "short"
    return None
