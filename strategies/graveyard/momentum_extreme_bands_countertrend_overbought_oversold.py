#!/usr/bin/env python3
"""momentum_extreme_bands_countertrend_overbought_oversold -- ROC penetrates +/-2*roc_sd band ->
countertrend fade; go long when ROC < -2*SD (momentum oversold), short when ROC > +2*SD.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.6 pp.131-133.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "momentum_extreme_bands_countertrend_overbought_oversold",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "roc, roc_sd",
    "long": "ROC < -2 * roc_sd (momentum penetrates lower extreme band)",
    "short": "ROC > +2 * roc_sd (momentum penetrates upper extreme band)",
    "desc": "Momentum extreme-bands countertrend: fade when ROC exceeds +/-2 rolling standard deviations",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.6 pp.131-133",
}


def signal(ind, pos, htf=None):
    """Countertrend fade when ROC penetrates the +/-2*roc_sd extreme band."""
    r = ind["roc"][pos]
    sd = ind["roc_sd"][pos]
    if nan(r, sd) or sd <= 0:
        return None
    band = 2.0 * sd
    if r < -band:
        return "long"
    if r > band:
        return "short"
    return None
