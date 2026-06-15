#!/usr/bin/env python3
"""elder_triple_screen -- Elder Triple Screen: HTF trend + stochastic wave + EMA entry. mql5 blog 2019.

Tide = HTF bias (EMA20>EMA50 on H4, mapped to htf.bias).
Wave = stochastic K exits oversold/overbought on entry TF.
Entry = price crosses EMA9 (approximated by ema9) on entry TF.
sma50 proxies MA(48) from the spec.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_triple_screen",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "ema9, stoch_k, stoch_d",
    "long": "HTF bias bullish AND stoch_k exits oversold (<20 prior, >=20 now) AND close > ema9",
    "short": "HTF bias bearish AND stoch_k exits overbought (>80 prior, <=80 now) AND close < ema9",
    "desc": "Elder Triple Screen: HTF trend bias + stochastic wave + EMA9 entry cross",
    "source": "https://www.mql5.com/en/blogs/post/731016 Elder Triple Screen Strategy",
}


def signal(ind, pos, htf=None):
    """Triple screen: HTF trend + stoch exit OB/OS + price/EMA9 cross."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    e9 = ind["ema9"][pos]
    e91 = ind["ema9"][pos - 1]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(c, c1, e9, e91, sk, sk1):
        return None
    htf_bull = (htf["bias"][pos] > 0) if (htf is not None) else True
    htf_bear = (htf["bias"][pos] < 0) if (htf is not None) else True
    # Wave: stoch exits oversold (K crosses above 20)
    wave_os = sk1 < 20 and sk >= 20
    # Wave: stoch exits overbought (K crosses below 80)
    wave_ob = sk1 > 80 and sk <= 80
    # Entry: price crosses above/below ema9
    entry_long = c > e9 and c1 <= e91
    entry_short = c < e9 and c1 >= e91
    if htf_bull and wave_os and entry_long:
        return "long"
    if htf_bear and wave_ob and entry_short:
        return "short"
    return None
