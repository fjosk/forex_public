#!/usr/bin/env python3
"""first_of_month_buy_bond_market -- Buy on the first trading day of each month, bypassing
historically poor months (January, February, April, October).
long_term_secrets_to_short_term_trading Ch.10.

Adapted from T-Bond calendar rule: first-trading-day long on non-excluded months. Applied
here to FX as a generic calendar momentum effect.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "first_of_month_buy_bond_market",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of any month except January, February, April, October",
    "short": "not used (long-only calendar rule)",
    "desc": "First-of-month bond buy: long on the first trading day of non-excluded months",
    "source": "long_term_secrets_to_short_term_trading Ch.10 Month-End Trading in the Bond Market",
}

_EXCLUDED_MONTHS = {1, 2, 4, 10}   # Jan, Feb, Apr, Oct


def signal(ind, pos, htf=None):
    """Buy on first trading day of allowed months."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    m = dt.month
    if m in _EXCLUDED_MONTHS:
        return None
    return "long"
