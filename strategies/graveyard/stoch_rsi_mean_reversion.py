#!/usr/bin/env python3
"""stoch_rsi_mean_reversion -- Stochastic RSI extreme re-cross with SMA200 filter. QuantifiedStrategies.

StochRSI exits the extreme zone (cross back above 0.2 for long, cross back below 0.8 for short)
with optional SMA200 trend alignment. 78% win rate reported on FX 4h in published backtest.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stoch_rsi_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "srsi_k, sma200",
    "long": "srsi_k crosses back above 0.2 (exit oversold) and close > SMA200",
    "short": "srsi_k crosses back below 0.8 (exit overbought) and close < SMA200",
    "desc": "StochRSI extreme re-cross mean reversion with SMA200 trend filter",
    "source": "web:https://www.quantifiedstrategies.com/stochastic-rsi/; Chande & Kroll (1994)",
}


def signal(ind, pos, htf=None):
    """StochRSI re-cross out of extreme zone."""
    sk = ind["srsi_k"][pos]
    sk1 = ind["srsi_k"][pos - 1]
    s200 = ind["sma200"][pos]
    c = ind["close"][pos]
    if nan(sk, sk1, s200, c):
        return None
    # long: srsi_k crosses above 0.2 (was oversold, now recovering)
    if sk > 0.2 and sk1 <= 0.2 and c > s200:
        return "long"
    # short: srsi_k crosses below 0.8 (was overbought, now fading)
    if sk < 0.8 and sk1 >= 0.8 and c < s200:
        return "short"
    return None
