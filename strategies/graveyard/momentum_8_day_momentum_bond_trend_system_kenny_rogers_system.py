#!/usr/bin/env python3
"""momentum_8_day_momentum_bond_trend_system_kenny_rogers_system -- Kenny Rogers 8-day momentum:
buy when today's close > close 8 bars ago; short when today's close < close 8 bars ago.

Source: long_term_secrets_to_short_term_trading, Ch.~14 pp.211-212.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "momentum_8_day_momentum_bond_trend_system_kenny_rogers_system",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "close",
    "long": "close > close[8] (8-bar momentum positive)",
    "short": "close < close[8] (8-bar momentum negative)",
    "desc": "Kenny Rogers 8-day close momentum: buy on positive 8-bar rate-of-change, sell on negative",
    "source": "long_term_secrets_to_short_term_trading Ch.~14 pp.211-212",
}


def signal(ind, pos, htf=None):
    """8-bar close momentum: long if close > close[8], short if close < close[8]."""
    if pos < 8:
        return None
    c0 = ind["close"][pos]
    c8 = ind["close"][pos - 8]
    if nan(c0, c8):
        return None
    if c0 > c8:
        return "long"
    if c0 < c8:
        return "short"
    return None
