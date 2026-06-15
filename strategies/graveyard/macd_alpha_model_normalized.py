#!/usr/bin/env python3
"""macd_alpha_model_normalized -- Normalized MACD signal vs 0.5% bounce threshold. QuantConnect Lean."""
from strategies._common import nan, TREND, ALL_CLASSES

# Source uses 1% threshold for equities; halved to 0.5% for FX pips scale.

META = {
    "id": "macd_alpha_model_normalized",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "macd_sig, close",
    "long": "macd_sig / close > 0.005 (signal > 0.5% of price)",
    "short": "macd_sig / close < -0.005",
    "desc": "MACD Alpha Model: normalized signal line vs price with bounce threshold to reduce whipsaw",
    "source": "https://github.com/QuantConnect/Lean/blob/master/Algorithm.Framework/Alphas/MacdAlphaModel.py",
}

_THRESHOLD = 0.005  # halved from equity default 0.01 for FX scale


def signal(ind, pos, htf=None):
    """Normalized MACD signal vs price threshold."""
    ms = ind["macd_sig"][pos]
    c = ind["close"][pos]
    if nan(ms, c) or c == 0:
        return None
    norm = ms / c
    if norm > _THRESHOLD:
        return "long"
    if norm < -_THRESHOLD:
        return "short"
    return None
