#!/usr/bin/env python3
"""keltner_channel_mean_reversion -- KC pullback: breakout trend re-entry at EMA center. LuxAlgo."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "keltner_channel_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h/4h",
    "indicators": "kc_up, kc_lo, kc_mid, atr, close, open",
    "long": "prior breakout above kc_up; pullback then close above kc_mid with bullish candle",
    "short": "prior breakout below kc_lo; pullback then close below kc_mid with bearish candle",
    "desc": "KC pullback mean-reversion: breakout trend, retrace to center EMA, resume",
    "source": "web:https://www.luxalgo.com/blog/keltner-channel-strategy-surf-volatility-bands/",
}


def signal(ind, pos, htf=None):
    """KC center-line pullback entry after an outer-band breakout."""
    if pos < 11:
        return None
    c = ind["close"][pos]
    o = ind["open"][pos]
    kc_mid = ind["kc_mid"][pos]
    kc_up = ind["kc_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    atr = ind["atr"][pos]
    c1 = ind["close"][pos - 1]
    kc_mid1 = ind["kc_mid"][pos - 1]
    if nan(c, o, kc_mid, kc_up, kc_lo, atr, c1, kc_mid1):
        return None

    # Check if price touched upper band within last 10 bars
    in_up_trend = False
    in_dn_trend = False
    for i in range(1, 11):
        if pos - i < 0:
            break
        ci = ind["close"][pos - i]
        kui = ind["kc_up"][pos - i]
        kli = ind["kc_lo"][pos - i]
        if nan(ci, kui, kli):
            continue
        if ci > kui:
            in_up_trend = True
        if ci < kli:
            in_dn_trend = True

    # Resumption after pullback to midline
    # Long: prior upper touch, previous bar near/below mid, current close back above mid with bullish candle
    at_mid_long_prev = abs(c1 - kc_mid1) < atr * 0.5
    if in_up_trend and at_mid_long_prev and c > kc_mid and c > o:
        return "long"

    # Short: prior lower touch, previous bar near/above mid, current close back below mid with bearish candle
    kc_mid1_s = ind["kc_mid"][pos - 1]
    at_mid_short_prev = abs(c1 - kc_mid1_s) < atr * 0.5
    if in_dn_trend and at_mid_short_prev and c < kc_mid and c < o:
        return "short"

    return None
