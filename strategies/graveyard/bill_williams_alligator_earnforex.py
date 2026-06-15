#!/usr/bin/env python3
"""bill_williams_alligator_earnforex -- Bill Williams Alligator EA (EarnForex).
web:https://www.earnforex.com/metatrader-expert-advisors/bill-williams-alligator/
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "bill_williams_alligator_earnforex",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "any",
    "indicators": "al_jaw, al_teeth, al_lips",
    "long": "Lips > Teeth > Jaw, all three lines rising",
    "short": "Lips < Teeth < Jaw, all three lines falling",
    "desc": "Bill Williams Alligator: fan-open bullish (lips>teeth>jaw, rising) or bearish (reverse)",
    "source": "web:https://www.earnforex.com/metatrader-expert-advisors/bill-williams-alligator/",
}


def signal(ind, pos, htf=None):
    """Alligator fan-open with slope confirmation on all three lines."""
    jaw = ind["al_jaw"][pos]
    teeth = ind["al_teeth"][pos]
    lips = ind["al_lips"][pos]
    jaw1 = ind["al_jaw"][pos - 1]
    teeth1 = ind["al_teeth"][pos - 1]
    lips1 = ind["al_lips"][pos - 1]
    if nan(jaw, teeth, lips, jaw1, teeth1, lips1):
        return None
    rising = lips > lips1 and teeth > teeth1 and jaw > jaw1
    falling = lips < lips1 and teeth < teeth1 and jaw < jaw1
    if lips > teeth and teeth > jaw and rising:
        return "long"
    if lips < teeth and teeth < jaw and falling:
        return "short"
    return None
