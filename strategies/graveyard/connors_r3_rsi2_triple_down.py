#!/usr/bin/env python3
"""connors_r3_rsi2_triple_down -- Connors R3 RSI(2) triple-decline pattern. Larry Connors / QuantifiedStrategies.

Three consecutive declining RSI(2) readings starting from below 60, with a final
RSI(2) < 10 (deep oversold), while price is above SMA200. Exit: RSI(2) > 70.
Source: web:https://www.quantifiedstrategies.com/larry-connors-r3-strategy/
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "connors_r3_rsi2_triple_down",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "daily",
    "indicators": "rsi2, sma200, close",
    "long": "close > sma200; rsi2 declined 3 consecutive bars starting from below 60; rsi2 < 10",
    "short": "not part of original system (long-only design); omitted",
    "desc": "Connors R3: three-bar RSI(2) decline from <60 to final reading <10, above SMA200",
    "source": "web:https://www.quantifiedstrategies.com/larry-connors-r3-strategy/",
}


def signal(ind, pos, htf=None):
    """Connors R3: three RSI(2) declines from <60, final reading <10, price above SMA200."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    s200 = ind["sma200"][pos]
    r0 = ind["rsi2"][pos]
    r1 = ind["rsi2"][pos - 1]
    r2 = ind["rsi2"][pos - 2]
    if nan(c, s200, r0, r1, r2):
        return None

    # Three consecutive declines: r2 > r1 > r0; first started from below 60; final < 10
    if (c > s200
            and r2 < 60      # first day of decline started from below 60
            and r2 > r1
            and r1 > r0
            and r0 < 10):
        return "long"

    return None
