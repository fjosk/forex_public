#!/usr/bin/env python3
"""november_nzd_usd_appreciation_seasonality -- Long NZD/USD on the first trading day of
November (NZD appreciated vs USD 8 of 11 years, average +1.9%).
day_trading_swing_trading_the_currency_market_tech Ch.7 Fig 7.9.

Signal fires on tdm==1 in November; engine holds via time-stop through month end.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "november_nzd_usd_appreciation_seasonality",
    "cadences": ["day", "swing"],
    "exit": {**TREND, "time_stop_h": 504},   # ~21 trading days = hold through November
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of November (NZD/USD tends to appreciate, 8/11 years avg +1.9%)",
    "short": "not used",
    "desc": "November NZD/USD appreciation seasonal: long at November open, hold through month",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.7 November and Incorporating Seasonality Fig 7.9",
}


def signal(ind, pos, htf=None):
    """Long NZD/USD at November open."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    if dt.month != 11:
        return None
    return "long"
