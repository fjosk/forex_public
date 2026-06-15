#!/usr/bin/env python3
"""ema_200_psar_stoch_trend_scalp -- EMA200 macro + PSAR micro + Stoch oversold entry. web:opofinance.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "ema_200_psar_stoch_trend_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "ema200, psar_dir, stoch_k",
    "long": "close > ema200 AND psar_dir > 0 AND stoch_k crosses above 20",
    "short": "close < ema200 AND psar_dir < 0 AND stoch_k crosses below 80",
    "desc": "Three-layer scalp: EMA200 macro trend + PSAR micro trend + Stochastic entry timing",
    "source": "web:https://blog.opofinance.com/en/parabolic-sar-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """EMA200 sets macro bias; PSAR confirms micro-trend; stoch cross times the pullback entry."""
    ema200 = ind["ema200"][pos]
    psar_dir = ind["psar_dir"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    c = ind["close"][pos]
    if nan(ema200, psar_dir, stk, stk_p, c):
        return None
    stoch_xu = stk > 20 and stk_p <= 20
    stoch_xd = stk < 80 and stk_p >= 80
    if c > ema200 and psar_dir > 0 and stoch_xu:
        return "long"
    if c < ema200 and psar_dir < 0 and stoch_xd:
        return "short"
    return None
