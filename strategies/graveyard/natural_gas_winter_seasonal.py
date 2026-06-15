#!/usr/bin/env python3
"""natural_gas_winter_seasonal -- Natural gas winter seasonal entry. UFO TradeWithUFOs study.

Primary window: long on first 3 days of September (injection-to-draw transition).
Short window: short on first 3 days of April (winter demand drop, injection season).
"""
import datetime
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "natural_gas_winter_seasonal",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "open_time, ema20, atr",
    "long": "September day 1-3: pre-winter storage draw seasonal long",
    "short": "April day 1-3: spring injection season shoulder short",
    "desc": "Natural gas winter seasonal: Sep long (7/10 years +56%) and Apr short",
    "source": "web:https://www.tradewithufos.com/natural-gas-with-a-tactical-seasonal-edge/",
}


def signal(ind, pos, htf=None):
    """Natural gas winter seasonal entry."""
    ts = ind["open_time"][pos]
    if nan(ts):
        return None
    dt = datetime.datetime.utcfromtimestamp(ts / 1000)
    m = dt.month
    d = dt.day
    if m == 9 and d <= 3:
        return "long"
    if m == 4 and d <= 3:
        return "short"
    return None
