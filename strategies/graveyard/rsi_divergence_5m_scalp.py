#!/usr/bin/env python3
"""rsi_divergence_5m_scalp -- RSI/price slope divergence with RSI > or < 50 filter. web:ebc.com."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_divergence_5m_scalp",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "5m",
    "indicators": "rsi, lr_slope_rsi, lr_slope_price",
    "long": "price slope negative AND rsi slope positive (bullish div) AND rsi > 50",
    "short": "price slope positive AND rsi slope negative (bearish div) AND rsi < 50",
    "desc": "RSI/price slope divergence (lr_slope proxy) with RSI level confirmation",
    "source": "web:https://www.ebc.com/forex/rsi-divergence-strategies-timing-the-market-like-a-pro",
}


def signal(ind, pos, htf=None):
    """Approximate RSI divergence using linear regression slopes of price vs RSI."""
    rsi = ind["rsi"][pos]
    lr_price = ind["lr_slope_price"][pos]
    lr_rsi = ind["lr_slope_rsi"][pos]
    if nan(rsi, lr_price, lr_rsi):
        return None
    bull_div = lr_price < 0 and lr_rsi > 0
    bear_div = lr_price > 0 and lr_rsi < 0
    if bull_div and rsi > 50:
        return "long"
    if bear_div and rsi < 50:
        return "short"
    return None
