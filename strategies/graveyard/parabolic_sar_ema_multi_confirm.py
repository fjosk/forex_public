#!/usr/bin/env python3
"""parabolic_sar_ema_multi_confirm -- Parabolic SAR + EMA Multi-Confirm EA. kb.mycoder.pro.

EMA200 as primary trend filter; SAR flip in the direction of EMA trend triggers entry.
psar_dir == 1 means SAR is below price (bullish). psar_dir == -1 means SAR above (bearish).
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_ema_multi_confirm",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, ema200, close",
    "long": "close > ema200 AND psar_dir just flipped to bullish (was -1, now 1)",
    "short": "close < ema200 AND psar_dir just flipped to bearish (was 1, now -1)",
    "desc": "SAR flip in direction of EMA200 trend",
    "source": "web:https://kb.mycoder.pro/apibridge/parabolic-sar-ema-strategy-for-mt4/",
}


def signal(ind, pos, htf=None):
    """SAR flip in EMA200 trend direction."""
    sd = ind["psar_dir"][pos]
    sd1 = ind["psar_dir"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(sd, sd1, c, e200):
        return None
    ema_bull = c > e200
    ema_bear = c < e200
    # SAR flipped bullish: was -1 (above price), now 1 (below price)
    sar_flip_bull = sd == 1 and sd1 == -1
    # SAR flipped bearish: was 1 (below price), now -1 (above price)
    sar_flip_bear = sd == -1 and sd1 == 1
    if ema_bull and sar_flip_bull:
        return "long"
    if ema_bear and sar_flip_bear:
        return "short"
    return None
