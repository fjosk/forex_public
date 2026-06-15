#!/usr/bin/env python3
"""fisher_transform_signal_crossover -- Fisher Transform / trigger line crossover. quantifiedstrategies.com."""
from strategies._common import nan, _xup, _xdn, REVERT, ALL_CLASSES

META = {
    "id": "fisher_transform_signal_crossover",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "4h",
    "indicators": "fisher, fisher_trig",
    "long": "Fisher line crosses above its trigger/signal line",
    "short": "Fisher line crosses below its trigger/signal line",
    "desc": "Ehlers Fisher Transform: fisher/fisher_trig crossover as turning-point signal",
    "source": "web:https://www.quantifiedstrategies.com/fisher-transform/",
}


def signal(ind, pos, htf=None):
    """Fisher / fisher_trig crossover."""
    fi = ind["fisher"][pos]
    fip = ind["fisher"][pos - 1]
    ft = ind["fisher_trig"][pos]
    ftp = ind["fisher_trig"][pos - 1]
    if nan(fi, fip, ft, ftp):
        return None
    if _xup(fi, fip, ft, ftp):
        return "long"
    if _xdn(fi, fip, ft, ftp):
        return "short"
    return None
