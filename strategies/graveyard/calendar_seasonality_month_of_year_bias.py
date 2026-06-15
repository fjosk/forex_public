#!/usr/bin/env python3
"""calendar_seasonality_month_of_year_bias -- Month-of-year seasonal bias: long in strong
months (Apr/Aug/Oct/Nov/Dec/Jan), short in September (historically weakest).
the_naked_trader_how_anyone_can_still_make_money_t.

Enters on the first trading day of each month (tdm==1) if that month has a directional bias.
September = short bias; April/August/October/November/December/January = long bias.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "calendar_seasonality_month_of_year_bias",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of Apr, Aug, Oct, Nov, Dec, or Jan (historically strong months)",
    "short": "first trading day of September (historically weakest month, avg -1.4%)",
    "desc": "Month-of-year seasonal bias: enter at month open in direction of historical monthly tendency",
    "source": "the_naked_trader_how_anyone_can_still_make_money_t Ch.4 Times Of The Year",
}

_LONG_MONTHS  = {1, 4, 8, 10, 11, 12}   # Jan, Apr, Aug, Oct, Nov, Dec
_SHORT_MONTHS = {9}                      # September


def signal(ind, pos, htf=None):
    """Enter at the first trading day of a seasonally biased month."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    # Derive month from epoch-ms timestamp
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    m = dt.month
    if m in _LONG_MONTHS:
        return "long"
    if m in _SHORT_MONTHS:
        return "short"
    return None
