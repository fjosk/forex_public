#!/usr/bin/env python3
"""aud_usd_rsi_bb_macd_stoch_multi -- AUD/USD Multi-Indicator RSI BB MACD Stochastic. ksjagtap/QuantConnect.

Multi-indicator confluence: RSI range + BB proximity OR MACD threshold for direction.
ML gate stripped; pure indicator-based logic.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "aud_usd_rsi_bb_macd_stoch_multi",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1d",
    "indicators": "rsi, bb_lo, bb_up, macd, close",
    "long": "(55 < rsi < 70 AND close near bb_lo) OR macd > 0 threshold",
    "short": "(20 < rsi < 65 AND close near bb_up) OR macd < -threshold",
    "desc": "Multi-indicator RSI + BB proximity + MACD threshold confluence; ML gate removed",
    "source": "web:https://github.com/ksjagtap/QuantConnect-Trading-Strategies/blob/master/AUD_USD_multi_strategy.py",
}


def signal(ind, pos, htf=None):
    """RSI range + BB proximity + MACD threshold confluence."""
    r = ind["rsi"][pos]
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    m = ind["macd"][pos]
    c = ind["close"][pos]
    if nan(r, bb_lo, bb_up, m, c):
        return None
    if c <= 0:
        return None
    bb_dist_lower = (c - bb_lo) / c
    bb_dist_upper = (bb_up - c) / c
    long_signal = (55 < r < 70 and bb_dist_lower < 0.02) or m > 0.0001
    short_signal = (20 < r < 65 and bb_dist_upper < 0.025) or m < -0.0001
    if long_signal and r < 70:
        return "long"
    if short_signal and r > 20:
        return "short"
    return None
