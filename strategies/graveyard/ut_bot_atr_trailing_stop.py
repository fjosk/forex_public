#!/usr/bin/env python3
"""ut_bot_atr_trailing_stop -- UT Bot ATR trailing stop via st_dir (SuperTrend proxy). web:tradesearcher.ai.

The UT Bot is mechanically equivalent to the SuperTrend indicator (ATR-based ratcheting
trailing stop that flips on price crossover). Use st_dir as the direct proxy.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "ut_bot_atr_trailing_stop",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "st_dir (SuperTrend proxy for UT Bot ATR trail)",
    "long": "st_dir flips from -1 to +1 (ATR trail flips bullish)",
    "short": "st_dir flips from +1 to -1 (ATR trail flips bearish)",
    "desc": "UT Bot ATR trailing stop flip (approximated by SuperTrend st_dir)",
    "source": "web:https://tradesearcher.ai/blog/ut-bot-alerts-strategy-guide-backtest-examples",
}


def signal(ind, pos, htf=None):
    """UT Bot trailing stop flip via SuperTrend st_dir proxy."""
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(sd, sdp):
        return None
    if sd == 1 and sdp == -1:
        return "long"
    if sd == -1 and sdp == 1:
        return "short"
    return None
