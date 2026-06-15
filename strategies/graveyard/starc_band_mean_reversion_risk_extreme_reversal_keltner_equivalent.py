#!/usr/bin/env python3
"""starc_band_mean_reversion_risk_extreme_reversal_keltner_equivalent -- STARC band (SMA +/-
2*ATR = Keltner equivalent) touch -> fade toward central mean.

Source: binary_options_unmasked_pdfdrive, Ch.7 Starc Bands.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "starc_band_mean_reversion_risk_extreme_reversal_keltner_equivalent",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "kc_lo, kc_up, kc_mid, close",
    "long": "Close <= kc_lo (lower Keltner / STARC band touch): fade up toward kc_mid",
    "short": "Close >= kc_up (upper Keltner / STARC band touch): fade down toward kc_mid",
    "desc": "STARC band (Keltner equivalent) mean-reversion: band-touch -> fade toward basis",
    "source": "binary_options_unmasked_pdfdrive Ch.7",
}


def signal(ind, pos, htf=None):
    """STARC/Keltner band touch -> fade toward central mean."""
    c = ind["close"][pos]
    klo = ind["kc_lo"][pos]
    kup = ind["kc_up"][pos]
    if nan(c, klo, kup):
        return None
    if c <= klo:
        return "long"
    if c >= kup:
        return "short"
    return None
