#!/usr/bin/env python3
"""bollinger_bands_mean_reversion_ea -- Bollinger Bands Mean Reversion EA. MQL4 BB Fade EA."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "bollinger_bands_mean_reversion_ea",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "4h",
    "indicators": "bb_up, bb_lo",
    "long": "prior bar closed below bb_lo; current bar closes back above bb_lo (re-entry)",
    "short": "prior bar closed above bb_up; current bar closes back below bb_up (re-entry)",
    "desc": "BB band re-entry fade: enter on the first close back inside the Bollinger Band",
    "source": "medium.com/@bushra.muzafar82/bollinger-bands-ea-mql4-download",
}


def signal(ind, pos, htf=None):
    """BB re-entry fade: price pierced the band on prior bar, re-enters on current bar."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    bbl = ind["bb_lo"][pos]
    bbl1 = ind["bb_lo"][pos - 1]
    bbu = ind["bb_up"][pos]
    bbu1 = ind["bb_up"][pos - 1]
    if nan(c, c1, bbl, bbl1, bbu, bbu1):
        return None
    if c1 < bbl1 and c > bbl:
        return "long"
    if c1 > bbu1 and c < bbu:
        return "short"
    return None
