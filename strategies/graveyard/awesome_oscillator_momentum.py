#!/usr/bin/env python3
"""awesome_oscillator_momentum -- Awesome Oscillator Momentum Direction. HPotter/TradingView.

Long when AO rises (current > previous, blue bar). Short when AO falls (current < previous, red bar).
Bill Williams AO = SMA5 midpoints minus SMA34 midpoints.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "awesome_oscillator_momentum",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "ao",
    "long": "ao[pos] > ao[pos-1] (AO rising / blue bar)",
    "short": "ao[pos] < ao[pos-1] (AO falling / red bar)",
    "desc": "Awesome Oscillator momentum direction: long on rising AO, short on falling AO",
    "source": "web:https://www.tradingview.com/script/fSHXMVey-Bill-Williams-Awesome-Oscillator-AO-Backtest/",
}


def signal(ind, pos, htf=None):
    """AO rising = long, AO falling = short."""
    ao = ind["ao"][pos]
    ao1 = ind["ao"][pos - 1]
    if nan(ao, ao1):
        return None
    if ao > ao1:
        return "long"
    if ao < ao1:
        return "short"
    return None
