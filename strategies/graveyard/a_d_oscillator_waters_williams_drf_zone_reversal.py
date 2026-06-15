#!/usr/bin/env python3
"""a_d_oscillator_waters_williams_drf_zone_reversal -- DRF (Daily Raw Figure) zone reversal: go long when DRF enters oversold zone, short when it enters overbought zone. trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "a_d_oscillator_waters_williams_drf_zone_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "open,high,low,close (DRF computed inline)",
    "long": "DRF (Daily Raw Figure) crosses into oversold zone (<= 0.30)",
    "short": "DRF crosses into overbought zone (>= 0.70)",
    "desc": "Waters/Williams A/D oscillator zone reversal: DRF = ((H-O)+(C-L))/(2*(H-L)) penetrates OB/OS zone",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

OB = 0.70
OS = 0.30


def signal(ind, pos, htf=None):
    """Long when DRF enters oversold (<= OS), short when it enters overbought (>= OB)."""
    if pos < 1:
        return None
    o = ind["open"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    c = ind["close"][pos]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c1 = ind["close"][pos - 1]
    if nan(o, h, l, c, o1, h1, l1, c1):
        return None
    # DRF formula: (BP + SP) / (2*(H-L)); BP=H-O, SP=C-L; gap fix handled via raw O/H/L/C
    def _drf(op, hi, lo, cl):
        rng = hi - lo
        if rng <= 0:
            return None
        bp = hi - op
        sp = cl - lo
        return (bp + sp) / (2.0 * rng)

    drf = _drf(o, h, l, c)
    drf1 = _drf(o1, h1, l1, c1)
    if nan(drf, drf1):
        return None
    # Enter on crossing into zone (first bar inside OB/OS)
    if drf <= OS and drf1 > OS:
        return "long"
    if drf >= OB and drf1 < OB:
        return "short"
    return None
