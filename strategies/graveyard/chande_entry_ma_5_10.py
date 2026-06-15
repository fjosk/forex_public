#!/usr/bin/env python3
"""chande_entry_ma_5_10 -- Chande Entry 5/10 MA Price Cross. Kevin Davey entry #3."""
from strategies._common import nan, _xdn, _xup, REVERT, ALL_CLASSES

META = {
    "id": "chande_entry_ma_5_10",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "close_sma5, sma10",
    "long": "SMA5 crosses BELOW SMA10 AND close < SMA5 (counter-trend pullback entry)",
    "short": "SMA5 crosses ABOVE SMA10 AND close > SMA5",
    "desc": "Chande pullback entry: fast MA turns down and price already below it (Davey book #3)",
    "source": "zeta-zetra.github.io/docs-forex-strategies-python/books/chande_entry.html",
}


def signal(ind, pos, htf=None):
    """SMA5/SMA10 crossover counter-trend entry (Chande/Davey style)."""
    s5 = ind["close_sma5"][pos]
    s51 = ind["close_sma5"][pos - 1]
    s10 = ind["sma10"][pos]
    s101 = ind["sma10"][pos - 1]
    c = ind["close"][pos]
    if nan(s5, s51, s10, s101, c):
        return None
    if _xdn(s5, s51, s10, s101) and c < s5:
        return "long"
    if _xup(s5, s51, s10, s101) and c > s5:
        return "short"
    return None
