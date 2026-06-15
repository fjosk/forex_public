#!/usr/bin/env python3
"""rsi2_connors_mean_reversion -- Connors RSI(2) mean reversion with SMA200 trend filter. StockCharts."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "rsi2_connors_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "daily",
    "indicators": "rsi2, sma200, close_sma5",
    "long": "close above sma200, RSI(2) <= 10 (deeply oversold)",
    "short": "close below sma200, RSI(2) >= 90 (deeply overbought)",
    "desc": "Connors RSI-2 mean reversion: ultra-short RSI extreme in trend direction",
    "source": "web:https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2",
}


def signal(ind, pos, htf=None):
    """RSI(2) extreme in trend direction: long when rsi2<=10 above SMA200."""
    c = ind["close"][pos]
    sma200 = ind["sma200"][pos]
    r2 = ind["rsi2"][pos]
    if nan(c, sma200, r2):
        return None

    if c > sma200 and r2 <= 10:
        return "long"
    if c < sma200 and r2 >= 90:
        return "short"

    return None
