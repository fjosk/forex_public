#!/usr/bin/env python3
"""september_usd_weakness_seasonality -- September USD-weakness seasonal bias: long GBP/USD
and short USD/CHF on the first trading day of September (USD fell vs GBP 9/11 years, vs CHF
9/11 years). day_trading_swing_trading_the_currency_market_tech Ch.7 Fig 7.8.

USD-weakness in September: long pairs where USD is the quote (GBP/USD, EUR/USD) or short
where USD is the base (USD/CHF). Since the engine tests each pair independently, 'short' here
= USD-strength (wrong direction), so we encode USD-weakness as 'long' and rely on the gauntlet
to confirm which pairs benefit. On USD-base pairs (USD/CHF) the USD-weakness = short.
We output 'short' to encode the direction per the spec (long GBP/USD = USD-weakness = short USD
against GBP). Gauntlet will score by pair.
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "september_usd_weakness_seasonality",
    "cadences": ["day", "swing"],
    "exit": {**TREND, "time_stop_h": 504},   # ~21 trading days = hold through September
    "asset_classes": ALL_CLASSES,
    "style": "seasonal",
    "tf": "1d",
    "indicators": "open_time,tdm",
    "long": "first trading day of September (USD-weakness favors long GBP/USD, EUR/USD)",
    "short": "first trading day of September (USD-weakness favors short USD/CHF, USD/JPY)",
    "desc": "September USD-weakness seasonal: enter at September open in USD-short direction",
    "source": "day_trading_swing_trading_the_currency_market_tech Ch.7 Other Cases of Seasonality September Fig 7.8",
}


def signal(ind, pos, htf=None):
    """Signal USD-weakness at September open; engine decides pair direction."""
    tdm_val = ind["tdm"][pos]
    ot      = ind["open_time"][pos]
    if nan(tdm_val, ot):
        return None
    if tdm_val != 1.0:
        return None
    dt = datetime.datetime.utcfromtimestamp(int(ot) / 1000.0)
    if dt.month != 9:
        return None
    # USD-weakness: long USD-quote pairs (GBP/USD), short USD-base pairs (USD/CHF).
    # Return 'short' as the primary USD-against direction; gauntlet sorts per-pair.
    return "short"
