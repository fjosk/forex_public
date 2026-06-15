#!/usr/bin/env python3
"""fractal_breakout_ma100 -- Fractal breakout above/below SMA100 with RSI and stoch confirm. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "fractal_breakout_ma100",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "15m",
    "indicators": "sma100, frac_up_px, frac_dn_px, rsi, stoch_k",
    "long": "close > sma100 AND close > frac_up_px AND rsi > 55 AND stoch_k rising",
    "short": "close < sma100 AND close < frac_dn_px AND rsi < 45 AND stoch_k falling",
    "desc": "Williams fractal breakout filtered by MA100 trend + RSI + stochastic momentum",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies/94-scalping-breakout-scalping-strategy/",
}


def signal(ind, pos, htf=None):
    """Close beyond fractal level on the correct side of MA100 with RSI and stoch confirmation."""
    sma = ind["sma100"][pos]
    frac_up = ind["frac_up_px"][pos]
    frac_dn = ind["frac_dn_px"][pos]
    rsi = ind["rsi"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    c = ind["close"][pos]
    if nan(sma, frac_up, frac_dn, rsi, stk, stk_p, c):
        return None
    stoch_rise = stk > stk_p
    if c > sma and c > frac_up and rsi > 55 and stoch_rise:
        return "long"
    if c < sma and c < frac_dn and rsi < 45 and not stoch_rise:
        return "short"
    return None
