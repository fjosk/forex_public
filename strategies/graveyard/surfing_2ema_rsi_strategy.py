#!/usr/bin/env python3
"""surfing_2ema_rsi_strategy -- EMA-of-high/low crossover with RSI filter. MQL5 forum 478642."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "surfing_2ema_rsi_strategy",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "ema_hi13, ema_lo13, rsi",
    "long": "close crosses above ema_hi13 AND rsi > 55 AND rsi rising (rsi[pos] > rsi[pos-1])",
    "short": "close crosses below ema_lo13 AND rsi < 45 AND rsi falling (rsi[pos] < rsi[pos-1])",
    "desc": "Surfing EA: price crossing EMA of highs/lows confirmed by RSI direction and level",
    "source": "MQL5 forum thread 478642 -- Surfing EA D1 (MQL4)",
}


def signal(ind, pos, htf=None):
    """Close crosses EMA-of-high (long) or EMA-of-low (short), filtered by RSI."""
    ehi = ind["ema_hi13"][pos]
    elo = ind["ema_lo13"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    rsi_val = ind["rsi"][pos]
    rsi1 = ind["rsi"][pos - 1]
    if nan(ehi, elo, c, c1, rsi_val, rsi1):
        return None
    # Long: close crosses above ema_hi13
    if c1 < ehi and c > ehi and rsi_val > 55 and rsi_val > rsi1:
        return "long"
    # Short: close crosses below ema_lo13
    if c1 > elo and c < elo and rsi_val < 45 and rsi_val < rsi1:
        return "short"
    return None
