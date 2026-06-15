#!/usr/bin/env python3
"""momentum_forecast_oscillator_f_trend_acceleration -- Forecast Oscillator (%F): long when fosc
> 0 and rising, short when fosc < 0; reverse on zero-line cross.

Source: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch.6 pp.145-146.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "momentum_forecast_oscillator_f_trend_acceleration",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "fosc",
    "long": "fosc > 0 and fosc > fosc[1] (forecast oscillator positive and rising: price accelerating above trendline)",
    "short": "fosc < 0 and fosc < fosc[1] (forecast oscillator negative and falling: price decelerating below trendline)",
    "desc": "Forecast Oscillator (%F): trend acceleration signal -- long when %F positive and rising, short when negative and falling",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.6 pp.145-146",
}


def signal(ind, pos, htf=None):
    """Forecast oscillator zero-line + slope direction."""
    if pos < 1:
        return None
    f = ind["fosc"][pos]
    f1 = ind["fosc"][pos - 1]
    if nan(f, f1):
        return None
    if f > 0 and f > f1:
        return "long"
    if f < 0 and f < f1:
        return "short"
    return None
