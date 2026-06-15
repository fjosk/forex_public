#!/usr/bin/env python3
"""rsi_bollinger_bands_on_rsi -- Bollinger Bands applied to RSI series; computed inline. barabashkakvn MQL5 2018."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_bollinger_bands_on_rsi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "rsi",
    "long": "RSI drops below its own lower Bollinger Band (RSI_avg - 2*RSI_stddev)",
    "short": "RSI rises above its own upper Bollinger Band (RSI_avg + 2*RSI_stddev)",
    "desc": "Bollinger Bands applied to the RSI series; dynamic oversold/overbought thresholds",
    "source": "barabashkakvn MQL5 CodeBase 2018 (mql5.com/en/code/20705)",
}

_BB_PERIOD = 20
_BB_SIGMA = 2.0


def signal(ind, pos, htf=None):
    """Compute inline BB on RSI window; enter on RSI crossing outside the bands."""
    if pos < _BB_PERIOD:
        return None
    rsi_arr = ind["rsi"]
    r = rsi_arr[pos]
    if nan(r):
        return None
    # collect rolling window
    window = [rsi_arr[pos - i] for i in range(_BB_PERIOD)]
    if any(nan(v) for v in window):
        return None
    mean_r = sum(window) / _BB_PERIOD
    var_r = sum((v - mean_r) ** 2 for v in window) / _BB_PERIOD
    std_r = var_r ** 0.5
    upper = mean_r + _BB_SIGMA * std_r
    lower = mean_r - _BB_SIGMA * std_r
    if r < lower:
        return "long"
    if r > upper:
        return "short"
    return None
