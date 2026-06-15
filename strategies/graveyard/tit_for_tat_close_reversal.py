#!/usr/bin/env python3
"""tit_for_tat_close_reversal -- Contra-momentum: fade the close vs prior close direction.

Price/OHLC only (no volume) -> FX-applicable.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "tit_for_tat_close_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "close",
    "long": "close < close[-1] (price fell -> anticipate bounce)",
    "short": "close > close[-1] (price rose -> anticipate fade)",
    "desc": "Tit for tat: pure contra-momentum baseline, fade the close vs prior close direction",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/youtube/tit_for_tat.html",
}


def signal(ind, pos, htf=None):
    """Contra-momentum: fade the prior bar's close change direction."""
    if pos < 1:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c0, c1):
        return None
    if c0 < c1:
        return "long"
    if c0 > c1:
        return "short"
    return None
