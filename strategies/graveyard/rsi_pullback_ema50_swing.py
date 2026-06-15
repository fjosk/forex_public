#!/usr/bin/env python3
"""rsi_pullback_ema50_swing -- RSI pullback to 40 near EMA50 with bullish candle. PriceActionNinja."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi_pullback_ema50_swing",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "ema50, rsi, atr, close, open",
    "long": "close above ema50, RSI<=40, price within 0.5 ATR of ema50, bullish candle",
    "short": "close below ema50, RSI>=60, price within 0.5 ATR of ema50, bearish candle",
    "desc": "RSI pullback to EMA50 swing: oversold dip in trend near the 50 EMA",
    "source": "web:https://priceactionninja.com/the-best-4h-swing-trading-method-for-consistent-trades/",
}


def signal(ind, pos, htf=None):
    """Uptrend pullback: RSI cools to <=40 near EMA50 with bullish candle."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    e50 = ind["ema50"][pos]
    r = ind["rsi"][pos]
    atr = ind["atr"][pos]
    if nan(c, o, e50, r, atr):
        return None

    at_ema = abs(c - e50) < atr * 0.5

    if c > e50 and r <= 40 and at_ema and c > o:
        return "long"
    if c < e50 and r >= 60 and at_ema and c < o:
        return "short"

    return None
