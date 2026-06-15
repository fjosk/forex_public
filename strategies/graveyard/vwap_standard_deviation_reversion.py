#!/usr/bin/env python3
"""vwap_standard_deviation_reversion -- VWAP band fade using BB bands as SD proxy. FMZ."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "vwap_standard_deviation_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "5m/1h",
    "indicators": "vwap, bb_up, bb_lo, close",
    "long": "close crosses below bb_lo (BB lower band as 2-SD proxy), price below vwap",
    "short": "close crosses above bb_up (BB upper band as 2-SD proxy), price above vwap",
    "desc": "VWAP deviation reversion: fade price at Bollinger Band extremes relative to VWAP",
    "source": "web:https://www.fmz.com/lang/en/strategy/474675",
}


def signal(ind, pos, htf=None):
    """Fade extremes: price beyond BB band (2-SD proxy) with VWAP directional filter."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    vwap = ind["vwap"][pos]
    bb_up = ind["bb_up"][pos]
    bb_lo = ind["bb_lo"][pos]
    if nan(c, c1, vwap, bb_up, bb_lo):
        return None

    # Long: close drops below lower BB (oversold extreme) and price is below vwap
    if c < bb_lo and c1 >= bb_lo and c < vwap:
        return "long"

    # Short: close rises above upper BB (overbought extreme) and price is above vwap
    if c > bb_up and c1 <= bb_up and c > vwap:
        return "short"

    return None
