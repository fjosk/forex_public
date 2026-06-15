#!/usr/bin/env python3
"""triple_screen_ema_macd_histogram_trend_pullback_system -- Elder Triple-Screen: HTF EMA slope + daily MACD-H below zero ticking up (or stoch low) = pullback entry in trend direction. Elder.

tier1 multi-timeframe momentum. Price/OHLC only.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "triple_screen_ema_macd_histogram_trend_pullback_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "ema50, macd_hist, stoch_k",
    "long": "EMA50 rising AND (MACD-Hist < 0 AND ticking up) OR stoch_k < 30",
    "short": "EMA50 falling AND (MACD-Hist > 0 AND ticking down) OR stoch_k > 70",
    "desc": "Elder Triple-Screen trend-pullback: EMA trend direction + MACD-H counter-trend dip entry",
    "source": "Elder, Come Into My Trading Room, Ch.6 Triple Screen Update Screen One/Two/Three, pp.131-137",
}


def signal(ind, pos, htf=None):
    """EMA trend gate + MACD-H pullback entry or stochastic extreme."""
    if pos < 1:
        return None
    e = ind["ema50"][pos]
    e1 = ind["ema50"][pos - 1]
    h = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    sk = ind["stoch_k"][pos]
    if nan(e, e1, h, h1, sk):
        return None
    trend_up = e > e1
    trend_dn = e < e1
    # Long: EMA rising AND (MACD-H below zero ticking up OR stoch oversold)
    if trend_up and ((h < 0 and h > h1) or sk < 30):
        return "long"
    # Short: EMA falling AND (MACD-H above zero ticking down OR stoch overbought)
    if trend_dn and ((h > 0 and h < h1) or sk > 70):
        return "short"
    return None
