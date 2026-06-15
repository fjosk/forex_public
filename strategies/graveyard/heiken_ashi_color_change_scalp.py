#!/usr/bin/env python3
"""heiken_ashi_color_change_scalp -- HA color pullback then resumption with MACD/RSI momentum confirm. web:fxcc.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "heiken_ashi_color_change_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ha_close, ha_open, macd_hist, rsi",
    "long": "prev HA red, current HA green (trend resumption) AND MACD hist > 0 or RSI > 50",
    "short": "prev HA green, current HA red AND MACD hist < 0 or RSI < 50",
    "desc": "Heiken Ashi color-change trend resumption scalp with MACD/RSI momentum confirmation",
    "source": "web:https://www.fxcc.com/heiken-ashi-strategy",
}


def signal(ind, pos, htf=None):
    """One counter-trend HA candle then trend-color resumes; confirmed by MACD or RSI momentum."""
    hac = ind["ha_close"][pos]
    hao = ind["ha_open"][pos]
    hac_p = ind["ha_close"][pos - 1]
    hao_p = ind["ha_open"][pos - 1]
    mh = ind["macd_hist"][pos]
    rsi = ind["rsi"][pos]
    if nan(hac, hao, hac_p, hao_p, mh, rsi):
        return None
    ha_bull = hac > hao
    ha_bear = hac < hao
    ha_bull_p = hac_p > hao_p
    ha_bear_p = hac_p < hao_p
    mom_bull = mh > 0 or rsi > 50
    mom_bear = mh < 0 or rsi < 50
    # one counter-trend candle then resumption
    if ha_bear_p and ha_bull and mom_bull:
        return "long"
    if ha_bull_p and ha_bear and mom_bear:
        return "short"
    return None
