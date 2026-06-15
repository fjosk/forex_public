#!/usr/bin/env python3
"""triple_timeframe_trend_entry -- Weekly/Daily/4H trend alignment + RSI pullback to 45 then reclaim 50. mindmathmoney.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "triple_timeframe_trend_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ema50, ema200, rsi",
    "long": "htf macro bull (ema50 > ema200 proxy); current close > ema50; RSI reclaims 50 from below 45",
    "short": "htf macro bear; current close < ema50; RSI fails back below 50 from above 55",
    "desc": "Triple timeframe trend: htf macro bias + daily ema50 filter + 4H RSI pullback reclaim entry",
    "source": "web:https://www.mindmathmoney.com/articles/multi-timeframe-analysis-trading-strategy-the-complete-guide-to-trading-multiple-timeframes",
}


def signal(ind, pos, htf=None):
    """Multi-TF trend alignment with RSI pullback reclaim."""
    c = ind["close"][pos]
    e50 = ind["ema50"][pos]
    e200 = ind["ema200"][pos]
    rs = ind["rsi"][pos]
    rsp = ind["rsi"][pos - 1]
    if nan(c, e50, e200, rs, rsp):
        return None

    # Macro bias from htf; fall back to ema50 > ema200 as weekly proxy
    if htf is not None:
        bias_arr = htf.get("bias")
        if bias_arr is not None and not nan(bias_arr[pos]):
            macro_bull = bias_arr[pos] > 0
            macro_bear = bias_arr[pos] < 0
        else:
            macro_bull = e50 > e200
            macro_bear = e50 < e200
    else:
        macro_bull = e50 > e200
        macro_bear = e50 < e200

    daily_bull = c > e50
    daily_bear = c < e50

    # RSI pulls back below 45 then reclaims 50
    rsi_reclaim = rs > 50 and rsp <= 50 and rsp < 45
    # RSI rises above 55 then falls back below 50
    rsi_fail = rs < 50 and rsp >= 50 and rsp > 55

    if macro_bull and daily_bull and rsi_reclaim:
        return "long"
    if macro_bear and daily_bear and rsi_fail:
        return "short"
    return None
