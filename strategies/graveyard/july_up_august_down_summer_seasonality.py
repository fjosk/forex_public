#!/usr/bin/env python3
"""july_up_august_down_summer_seasonality -- Long USD pairs in July (USD/JPY rose 9/11 years),
short USD pairs in August (USD/JPY fell 9/11 years, avg -2.1%).
day_trading_swing_trading_the_currency_market_tech Ch.7 Summer Seasonality Figs 7.4-7.5.

Enters on the first trading day of July (long USD) and first trading day of August (short USD).
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "july_up_august_down_summer_seasonality",
    "cadences": ["day", "swing"],
    "exit": {**TREND, "time_stop_h": 504},   # ~21 trading days = hold full month
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of July (USD/JPY, USD/CAD tend to rise in July)",
    "short": "first trading day of August (USD/JPY, USD/CAD tend to fall in August)",
    "desc": "July-up August-down summer seasonality: long USD in July, short USD in August",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.7 Summer Seasonality Figs 7.4-7.5",
}


def signal(ind, pos, htf=None):
    """Long USD in July open, short USD in August open."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    m = dt.month
    if m == 7:
        return "long"
    if m == 8:
        return "short"
    return None
