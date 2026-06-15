#!/usr/bin/env python3
"""elder_triple_screen_system -- Elder Triple Screen Trading System.
web:https://quantstrategy.io/blog/what-is-the-triple-screen-trading-system-alexander-elder-trading-strategy/
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "elder_triple_screen_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "4h",
    "indicators": "macd_hist, ema200, force2, stoch_k, atr, high, low",
    "long": "HTF rising (macd_hist up OR ema200 rising) AND stoch_k<25 OR force2<0 AND close>high[prev]",
    "short": "HTF falling AND stoch_k>75 OR force2>0 AND close<low[prev]",
    "desc": "Elder Triple Screen: Screen1=HTF trend, Screen2=oscillator pullback, Screen3=price breakout",
    "source": "web:https://quantstrategy.io/blog/what-is-the-triple-screen-trading-system-alexander-elder-trading-strategy/",
}


def signal(ind, pos, htf=None):
    """Three-screen filter: HTF trend + oscillator pullback + price breakout confirmation."""
    mh = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    e200 = ind["ema200"][pos]
    e200_1 = ind["ema200"][pos - 1]
    sk = ind["stoch_k"][pos]
    f2 = ind["force2"][pos]
    c = ind["close"][pos]
    h1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    if nan(mh, mh1, e200, e200_1, sk, f2, c, h1, lo1):
        return None
    # Screen 1: HTF trend direction
    htf_up = (mh > mh1) or (e200 > e200_1)
    htf_dn = (mh < mh1) or (e200 < e200_1)
    # Screen 2: oscillator pullback
    pull_long = sk < 25 or f2 < 0
    pull_short = sk > 75 or f2 > 0
    # Screen 3: breakout
    break_long = c > h1
    break_short = c < lo1
    if htf_up and pull_long and break_long:
        return "long"
    if htf_dn and pull_short and break_short:
        return "short"
    return None
