#!/usr/bin/env python3
"""ut_bot_alerts -- UT Bot: ATR trailing stop flip using ut_pos precomputed indicator. web:quantnomad.com.

ut_pos is the precomputed UT Bot trailing-stop position signal (+1 = price above trail,
-1 = price below). A flip from -1 to +1 = long; from +1 to -1 = short.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ut_bot_alerts",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ut_pos",
    "long": "ut_pos flips from -1 to +1 (price crosses above ATR trailing stop)",
    "short": "ut_pos flips from +1 to -1 (price crosses below ATR trailing stop)",
    "desc": "UT Bot ATR trailing stop flip (one of the most-forked TradingView scripts)",
    "source": "web:https://quantnomad.com/implementing-ut-bot-strategy-in-python-with-vectorbt/",
}


def signal(ind, pos, htf=None):
    """UT Bot: ut_pos flip from -1 to +1 (long) or +1 to -1 (short)."""
    utp = ind["ut_pos"][pos]
    utpp = ind["ut_pos"][pos - 1]
    if nan(utp, utpp):
        return None
    if utp == 1 and utpp == -1:
        return "long"
    if utp == -1 and utpp == 1:
        return "short"
    return None
