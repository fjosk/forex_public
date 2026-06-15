#!/usr/bin/env python3
"""perfect_order_moving_average_trend_entry -- SMA10>20>50>100>200 stacked in perfect order with ADX > 20 rising. day_trading_swing_trading_the_currency_market."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "perfect_order_moving_average_trend_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "sma10, sma20, sma50, sma100, sma200, adx",
    "long": "SMA10>SMA20>SMA50>SMA100>SMA200 AND ADX > 20 and rising",
    "short": "SMA10<SMA20<SMA50<SMA100<SMA200 AND ADX > 20 and rising",
    "desc": "Perfect Order: all 5 SMAs stacked sequentially with ADX confirming trend strength",
    "source": "book:day_trading_swing_trading_the_currency_market_tech Ch 9 pp.138-140",
}

ADX_MIN = 20.0


def signal(ind, pos, htf=None):
    """Perfect Order MA stack with ADX threshold; enter on first bar the order holds."""
    if pos < 1:
        return None
    s10 = ind["sma10"][pos]
    s20 = ind["sma20"][pos]
    s50 = ind["sma50"][pos]
    s100 = ind["sma100"][pos]
    s200 = ind["sma200"][pos]
    adx = ind["adx"][pos]
    adx1 = ind["adx"][pos - 1]
    if nan(s10, s20, s50, s100, s200, adx, adx1):
        return None
    adx_ok = adx > ADX_MIN and adx > adx1
    if s10 > s20 > s50 > s100 > s200 and adx_ok:
        return "long"
    if s10 < s20 < s50 < s100 < s200 and adx_ok:
        return "short"
    return None
