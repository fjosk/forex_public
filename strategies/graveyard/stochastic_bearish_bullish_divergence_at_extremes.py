#!/usr/bin/env python3
"""stochastic_bearish_bullish_divergence_at_extremes -- Stochastic divergence at OB/OS extremes using fractal swing pivots. j_person_a_complete_guide_to_technical_trading_tac Ch8."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "stochastic_bearish_bullish_divergence_at_extremes",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "stoch_k,stoch_d,frac_dn_px,frac_up_px,low,high",
    "long": "Bullish divergence: recent fractal low below prior fractal low but stoch %K is higher than at prior fractal low, stoch in OS zone",
    "short": "Bearish divergence: recent fractal high above prior fractal high but stoch %K is lower than at prior fractal high, stoch in OB zone",
    "desc": "Stochastic bullish/bearish divergence at OB/OS extremes detected via fractal swing pivots",
    "source": "book: j_person_a_complete_guide_to_technical_trading_tac, Ch8",
}

OB = 80.0
OS = 20.0


def signal(ind, pos, htf=None):
    """Divergence: price new extreme vs stochastic shallower extreme at OB/OS."""
    if pos < 2:
        return None
    sk = ind["stoch_k"][pos]
    sd = ind["stoch_d"][pos]
    if nan(sk, sd):
        return None

    # Bullish divergence: look for recent fractal low < prior fractal low price
    # but stoch at recent low is higher than stoch at prior low
    # Approximate: compare frac_dn_px[pos] vs frac_dn_px[pos-1] (prior fractal low px)
    fdp = ind["frac_dn_px"][pos]
    fdp1 = ind["frac_dn_px"][pos - 1]
    sk1 = ind["stoch_k"][pos - 1]
    if not nan(fdp, fdp1, sk, sk1):
        if fdp < fdp1 and sk > sk1 and sk <= OS:
            return "long"

    # Bearish divergence: recent fractal high > prior fractal high price
    # but stoch at recent high is lower
    fup = ind["frac_up_px"][pos]
    fup1 = ind["frac_up_px"][pos - 1]
    if not nan(fup, fup1, sk, sk1):
        if fup > fup1 and sk < sk1 and sk >= OB:
            return "short"

    return None
