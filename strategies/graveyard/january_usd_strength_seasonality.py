#!/usr/bin/env python3
"""january_usd_strength_seasonality -- January USD-strength seasonal bias: long USD pairs
(USD/CHF, USD/JPY) and short EUR/USD on the first trading day of January.
day_trading_swing_trading_the_currency_market_tech Ch.7.

USD rose vs EUR 9/11 years, vs CHF +2.1% avg, vs JPY +1.3% avg in January (1997-2007 sample).
This module signals the generic long-USD direction on January open; pair-specific routing
happens via the gauntlet (USD/CHF + USD/JPY -> long; EUR/USD -> short).
Since the engine tests each pair independently, 'long' on a USD-base pair = USD strength;
on EUR/USD the USD-strength side = short. We encode the dominant direction as long (USD-strength)
and rely on the gauntlet to confirm per-pair fit.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "january_usd_strength_seasonality",
    "cadences": ["day", "swing"],
    "exit": {**TREND, "time_stop_h": 504},   # ~21 trading days = hold full January
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of January (USD-strength month: long USD/CHF, USD/JPY)",
    "short": "first trading day of January on EUR/USD (USD-strength = short EUR/USD)",
    "desc": "January USD-strength seasonal: long USD on month open, hold through January",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.7 Seasonality in January Figs 7.1-7.3",
}


def signal(ind, pos, htf=None):
    """Long USD at January open (USD-strength seasonal)."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    if dt.month != 1:
        return None
    return "long"
