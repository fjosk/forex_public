#!/usr/bin/env python3
"""monday_open_below_friday_close_buy -- Buy when Monday opens below the previous Friday close
(gap-down start to the week). long_term_secrets_to_short_term_trading Ch.3.

Adapted from S&P 500 day-of-week pattern: when the week begins with a downside gap it tends
to recover intraday/intraweek. Signal on Monday bars where open < prior close.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "monday_open_below_friday_close_buy",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "dow,open,close",
    "long": "today is Monday (dow==0) AND open < prior close (Monday gap down buy)",
    "short": "not used (long-only calendar rule)",
    "desc": "Monday open-below-Friday-close gap buy: downside Monday open tends to recover",
    "source": "long_term_secrets_to_short_term_trading Ch.3 pp.51-55 Figures 3.7-3.11",
}


def signal(ind, pos, htf=None):
    """Buy Monday gap-down opens."""
    if pos < 1:
        return None
    dw  = ind["dow"][pos]
    o   = ind["open"][pos]
    c1  = ind["close"][pos - 1]
    if nan(dw, o, c1):
        return None
    # Monday = weekday 0 in Python
    if int(dw) == 0 and o < c1:
        return "long"
    return None
