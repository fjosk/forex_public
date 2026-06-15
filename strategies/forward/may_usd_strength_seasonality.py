#!/usr/bin/env python3
"""may_usd_strength_seasonality -- May USD-strength seasonal bias: short AUD/USD and NZD/USD
on the first trading day of May (AUD rose only 2/11 years, NZD only 3/11 years in May).
day_trading_swing_trading_the_currency_market_tech Ch.7.

USD-strength in May = short AUD and NZD vs USD.
Signal = short at first trading day of May; engine closes via time-stop (~21 days).
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "may_usd_strength_seasonality",
    "cadences": ["day", "swing"],
    "exit": {**TREND, "time_stop_h": 504},   # ~21 trading days = hold through May
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "not used (USD-strength bias means short AUD/NZD; long side would be USD pairs)",
    "short": "first trading day of May (AUD/USD, NZD/USD tend to fall in May - USD strength)",
    "desc": "May USD-strength seasonal: short AUD/USD and NZD/USD at May open, hold through month",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.7 Other Cases of Seasonality May Figs 7.6-7.7",
}


def signal(ind, pos, htf=None):
    """Short USD-quote pairs (AUD/USD, NZD/USD) at May open."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    if dt.month != 5:
        return None
    return "short"
