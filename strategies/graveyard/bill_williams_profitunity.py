#!/usr/bin/env python3
"""bill_williams_profitunity -- Alligator awake + fractal above/below teeth entry. web:forexfactory.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "bill_williams_profitunity",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "al_jaw, al_teeth, al_lips, frac_up, frac_dn, frac_up_bar_high, frac_dn_bar_low, high, low",
    "long": "Alligator awake bullish (lips>teeth>jaw) and up-fractal forms above teeth",
    "short": "Alligator awake bearish (lips<teeth<jaw) and down-fractal forms below teeth",
    "desc": "Bill Williams Profitunity: Alligator awake + fractal breakout beyond teeth",
    "source": "web:https://www.forexfactory.com/thread/26044-profitunity-chaos-trading-system-by-bill-williams",
}


def signal(ind, pos, htf=None):
    """Alligator awake + fractal above/below teeth."""
    jaw = ind["al_jaw"][pos]
    teeth = ind["al_teeth"][pos]
    lips = ind["al_lips"][pos]
    fup = ind["frac_up"][pos]
    fdn = ind["frac_dn"][pos]
    hi = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(jaw, teeth, lips, hi, lo):
        return None
    # frac_up/frac_dn may be boolean or 0/1; treat truthy
    awake_bull = lips > teeth and teeth > jaw
    awake_bear = lips < teeth and teeth < jaw
    if awake_bull and fup and hi > teeth:
        return "long"
    if awake_bear and fdn and lo < teeth:
        return "short"
    return None
