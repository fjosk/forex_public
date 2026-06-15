#!/usr/bin/env python3
"""precision_15m_ma45_89_stoch -- EMA50/SMA100 dual-MA trend + stoch cross entry. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "precision_15m_ma45_89_stoch",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "15m",
    "indicators": "ema50 (proxy MA45), sma100 (proxy MA89), stoch_k",
    "long": "close > ema50 > sma100 AND stoch_k turning up from below 50",
    "short": "close < ema50 < sma100 AND stoch_k turning down from above 50",
    "desc": "Dual-MA trend color + stochastic cross entry on 15m (TMA arrow approximated by price structure)",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies-ii/173-precision-scalping-on-the-15-minute-chart/",
}


def signal(ind, pos, htf=None):
    """Price above both MAs in order; stochastic turning in trend direction for entry."""
    e50 = ind["ema50"][pos]
    s100 = ind["sma100"][pos]
    stk = ind["stoch_k"][pos]
    stk_p = ind["stoch_k"][pos - 1]
    c = ind["close"][pos]
    if nan(e50, s100, stk, stk_p, c):
        return None
    trend_up = c > e50 and e50 > s100
    trend_dn = c < e50 and e50 < s100
    stoch_up = stk > stk_p and stk_p < 50
    stoch_dn = stk < stk_p and stk_p > 50
    if trend_up and stoch_up:
        return "long"
    if trend_dn and stoch_dn:
        return "short"
    return None
