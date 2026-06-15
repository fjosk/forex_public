#!/usr/bin/env python3
"""pullback_momentum_50ema_rsi_engulfing -- EMA50 pullback with RSI 40-45 and engulfing candle. ForexTester."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "pullback_momentum_50ema_rsi_engulfing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h/daily",
    "indicators": "ema50, rsi, body_mom",
    "long": "ema50 rising, RSI 40-45, close above ema50, bullish engulfing (body_mom flip)",
    "short": "ema50 falling, RSI 55-60, close below ema50, bearish engulfing",
    "desc": "Pullback to rising EMA50 with RSI cooling and engulfing candle confirmation",
    "source": "web:https://forextester.com/blog/momentum-trading-strategies/",
}


def signal(ind, pos, htf=None):
    """EMA50 pullback: trend + RSI cooled to 40-45 + engulfing candle at EMA."""
    if pos < 3:
        return None
    c = ind["close"][pos]
    e50_0 = ind["ema50"][pos]
    e50_3 = ind["ema50"][pos - 3]
    r = ind["rsi"][pos]
    bm0 = ind["body_mom"][pos]
    bm1 = ind["body_mom"][pos - 1]
    if nan(c, e50_0, e50_3, r, bm0, bm1):
        return None

    ema50_rising = e50_0 > e50_3

    # Long: rising EMA50, RSI in 40-45 cooling zone, price above EMA50, bullish engulf
    if (ema50_rising
            and 40 <= r <= 45
            and c > e50_0
            and bm0 > 0 and bm1 < 0):
        return "long"

    # Short: falling EMA50, RSI in 55-60, price below EMA50, bearish engulf
    ema50_falling = e50_0 < e50_3
    if (ema50_falling
            and 55 <= r <= 60
            and c < e50_0
            and bm0 < 0 and bm1 > 0):
        return "short"

    return None
