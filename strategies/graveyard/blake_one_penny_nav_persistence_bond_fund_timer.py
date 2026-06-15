#!/usr/bin/env python3
"""blake_one_penny_nav_persistence_bond_fund_timer -- One-bar close direction persistence: buy on uptick, exit on downtick. The New Market Wizards, Gil Blake chapter.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "blake_one_penny_nav_persistence_bond_fund_timer",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "Close[i] > Close[i-1] (uptick day)",
    "short": "Close[i] < Close[i-1] (downtick day)",
    "desc": "Gil Blake one-penny rule: 1-bar close direction persistence signal; long on up-close, short on down-close",
    "source": "the_new_market_wizards Gil Blake chapter",
}


def signal(ind, pos, htf=None):
    """1-bar momentum: sign of today's close vs yesterday's close."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c, c1):
        return None
    if c > c1:
        return "long"
    if c < c1:
        return "short"
    return None
