#!/usr/bin/env python3
"""daily_bias_4h_entry_15m_trigger -- Daily EMA bias, pivot S/R pullback, RSI 50 cross trigger. blog.opofinance.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "daily_bias_4h_entry_15m_trigger",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema50, ema200, rsi, piv_s1, piv_r1",
    "long": "htf daily close > ema50 & ema200; price near piv_s1 support; rsi crosses above 50",
    "short": "htf daily close < ema50 & ema200; price near piv_r1 resistance; rsi crosses below 50",
    "desc": "Top-down: daily EMA bias -> 4h pivot S/R pullback -> RSI 50 cross trigger",
    "source": "web:https://blog.opofinance.com/en/daily-bias-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Daily EMA bias gated on pivot proximity and RSI 50 cross."""
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    rs = ind["rsi"][pos]
    rsp = ind["rsi"][pos - 1]
    s1 = ind["piv_s1"][pos]
    r1 = ind["piv_r1"][pos]
    if nan(c, e50, e200, rs, rsp, s1, r1):
        return None

    # Daily bias from htf when available, else fall back to current-bar ema50/200
    if htf is not None:
        bias_arr = htf.get("bias")
        if bias_arr is not None and not nan(bias_arr[pos]):
            daily_bull = bias_arr[pos] > 0
            daily_bear = bias_arr[pos] < 0
        else:
            daily_bull = c > e50 and c > e200
            daily_bear = c < e50 and c < e200
    else:
        daily_bull = c > e50 and c > e200
        daily_bear = c < e50 and c < e200

    rsi_cross_up = rs > 50 and rsp <= 50
    rsi_cross_dn = rs < 50 and rsp >= 50

    # Near pivot: within 0.2% of the level
    near_s1 = s1 > 0 and c <= s1 * 1.002 and c >= s1 * 0.998
    near_r1 = r1 > 0 and c >= r1 * 0.998 and c <= r1 * 1.002

    if daily_bull and near_s1 and rsi_cross_up:
        return "long"
    if daily_bear and near_r1 and rsi_cross_dn:
        return "short"
    return None
