#!/usr/bin/env python3
"""volatility_zone_range_risk_bands -- Volatility Zone Range/Risk Bands (Chande-Kroll): zones built around prior close using 10-day SMA of absolute daily change; breakout above H1 = long, below L1 = short. Kaufman Ch.18.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_zone_range_risk_bands",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "abschg, close",
    "long": "Close > prev_close + abschg (above H1 zone boundary)",
    "short": "Close < prev_close - abschg (below L1 zone boundary)",
    "desc": "Volatility zone breakout: zones centered on prior close expanded by average absolute daily change; breakout outside H1/L1 signals trend",
    "source": "trading_systems_and_methods_kaufman -- Ch.18 Zones for Forecasting Range and Risk Control (Chande & Kroll New Technical Trader)",
}


def signal(ind, pos, htf=None):
    """Close breaks outside H1/L1 zone boundary built from prior close +/- avg |change|."""
    if pos < 1:
        return None
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    # abschg = |close - close[1]|, SMA-smoothed; serves as A in the spec formula
    a = ind["abschg"][pos]
    if nan(c, c1, a):
        return None
    h1 = c1 + a   # upper zone boundary H1
    l1 = c1 - a   # lower zone boundary L1
    if c > h1:
        return "long"
    if c < l1:
        return "short"
    return None
