#!/usr/bin/env python3
"""jesse_rsi_tv_style -- RSI crosses above 35 (long entry); symmetric short for FX. jesse-ai TradingView RSI."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "jesse_rsi_tv_style",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "4h",
    "indicators": "rsi",
    "long": "RSI crosses above 35 (momentum building from oversold region)",
    "short": "RSI crosses below 65 (momentum rolling from overbought region; FX mirror)",
    "desc": "Jesse TradingView RSI crossover: RSI crosses 35 up for long, 65 down for short",
    "source": "jesse-ai/example-strategies TradingView_RSI/__init__.py",
}


def signal(ind, pos, htf=None):
    """RSI crossover at momentum-building thresholds."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(r, r1):
        return None
    if r > 35 and r1 <= 35:
        return "long"
    if r < 65 and r1 >= 65:
        return "short"
    return None
