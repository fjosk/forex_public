#!/usr/bin/env python3
"""freqtrade_cmc_winner_triple_oscillator -- CMCWinner CCI+CMO dual oscillator (MFI dropped: volume=0 on FX)."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_cmc_winner_triple_oscillator",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "cci, cmo",
    "long": "prev bar: cci < -100 AND cmo < -50 (MFI dropped: volume=0 on FX)",
    "short": "not implemented (long only in source; short symmetry added)",
    "desc": "Dual oscillator extreme oversold entry: CCI + CMO (MFI omitted, volume=0 on FX)",
    "source": "github.com/freqtrade/freqtrade-strategies berlinguyinca/CMCWinner.py",
}


def signal(ind, pos, htf=None):
    """CCI + CMO dual-oversold on previous bar (MFI excluded: FX volume=0)."""
    cci1 = ind["cci"][pos - 1]
    cmo1 = ind["cmo"][pos - 1]
    if nan(cci1, cmo1):
        return None
    if cci1 < -100 and cmo1 < -50:
        return "long"
    if cci1 > 100 and cmo1 > 50:
        return "short"
    return None
