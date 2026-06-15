#!/usr/bin/env python3
"""elliott_wave_oscillator_ewo_trend_and_wave_system -- EWO n-bar new-high (wave 3 up) or new-low (wave 3 down) trigger; exit when EWO crosses zero. Kaufman TSM Ch.14.

tier1 (price-action/trend). Price/OHLC only.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "elliott_wave_oscillator_ewo_trend_and_wave_system",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "ewo",
    "long": "EWO makes a new n-bar high (wave 3 up) with EWO > 0",
    "short": "EWO makes a new n-bar low (wave 3 down) with EWO < 0",
    "desc": "Elliott Wave Oscillator wave-3 trigger: EWO at n-bar extreme in the same sign confirms impulse wave entry",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.14 Automating Elliott Wave",
}

_N = 50  # robust n range 50-140 per spec; 50 bars lookback for new-high/low


def signal(ind, pos, htf=None):
    """EWO at n-bar extreme in its sign zone -> wave-3 impulse entry."""
    if pos < _N:
        return None
    ewo = ind["ewo"][pos]
    if nan(ewo):
        return None
    window = ind["ewo"][pos - _N:pos + 1]
    if any(nan(v) for v in window):
        return None
    hi = max(window[:-1])   # prior n bars (exclude current)
    lo = min(window[:-1])
    # wave 3 up: EWO > 0 and makes a new n-bar high
    if ewo > 0 and ewo > hi:
        return "long"
    # wave 3 down: EWO < 0 and makes a new n-bar low
    if ewo < 0 and ewo < lo:
        return "short"
    return None
