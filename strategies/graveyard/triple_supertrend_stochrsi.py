#!/usr/bin/env python3
"""triple_supertrend_stochrsi -- Dual ST + StochRSI crossover + EMA200 filter. Mel0nTek PineScript."""
from strategies._common import nan, TREND, ALL_CLASSES, _xup, _xdn

META = {
    "id": "triple_supertrend_stochrsi",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema200, srsi_k, srsi_d, st_dir, st_dir_fast",
    "long": "close > ema200 AND srsi_k crosses above srsi_d while srsi_k < 20 AND (st_dir > 0 OR st_dir_fast > 0)",
    "short": "close < ema200 AND srsi_k crosses below srsi_d while srsi_k > 80 AND (st_dir < 0 OR st_dir_fast < 0)",
    "desc": "Dual-SuperTrend + StochRSI oversold/overbought + EMA200 trend filter (simplified from triple ST)",
    "source": "hasnocool/tradingview-pine-scripts 3x SuperTrend (Mel0nTek V1); 2 STs used (3rd not available)",
}


def signal(ind, pos, htf=None):
    """EMA200 trend + StochRSI crossover from extreme zone + at least one ST in agreement."""
    e200 = ind["ema200"][pos]
    c = ind["close"][pos]
    sk = ind["srsi_k"][pos]
    sd = ind["srsi_d"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    sd1 = ind["srsi_d"][pos - 1]
    std = ind["st_dir"][pos]
    stdf = ind["st_dir_fast"][pos]
    if nan(e200, c, sk, sd, sk1, sd1, std, stdf):
        return None
    if c > e200 and _xup(sk, sk1, sd, sd1) and sk < 20 and (std > 0 or stdf > 0):
        return "long"
    if c < e200 and _xdn(sk, sk1, sd, sd1) and sk > 80 and (std < 0 or stdf < 0):
        return "short"
    return None
