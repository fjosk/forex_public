#!/usr/bin/env python3
"""jesse_ifr2_ichimoku -- Jesse IFR2 with Ichimoku cloud filter (Hilbert dropped; sma200_dir proxy)."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "jesse_ifr2_ichimoku",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "rsi2, ich_a, ich_b, sma200_dir",
    "long": "rsi2 < 10 AND close > ich_a AND close > ich_b AND sma200_dir >= 0 (uptrend proxy)",
    "short": "not implemented (long only in source)",
    "desc": "IFR2 RSI(2) oversold with Ichimoku cloud filter; sma200_dir replaces Hilbert trendmode",
    "source": "github.com/jesse-ai/example-strategies IFR2/__init__.py",
}


def signal(ind, pos, htf=None):
    """RSI(2) extreme oversold above Ichimoku cloud with sma200 direction as trendmode proxy."""
    c = ind["close"][pos]
    r2 = ind["rsi2"][pos]
    ia = ind["ich_a"][pos]
    ib = ind["ich_b"][pos]
    s200d = ind["sma200_dir"][pos]
    if nan(c, r2, ia, ib, s200d):
        return None
    if r2 < 10 and c > ia and c > ib and s200d >= 0:
        return "long"
    return None
