#!/usr/bin/env python3
"""global_equity_ibs_mean_reversion -- Internal Bar Strength Mean Reversion. QuantConnect/Lean IBS."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "global_equity_ibs_mean_reversion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1d",
    "indicators": "close, high, low",
    "long": "IBS < 0.2 (close near bar low -> oversold within day range)",
    "short": "IBS > 0.8 (close near bar high -> overbought within day range)",
    "desc": "Internal Bar Strength single-pair fixed-threshold variant (IBS = (close-low)/(high-low))",
    "source": "github.com/QuantConnect/Lean GlobalEquityMeanReversionIBSAlpha.py",
}


def signal(ind, pos, htf=None):
    """IBS fixed-threshold per-pair mean reversion (cross-sectional ranking replaced by thresholds)."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    if nan(c, h, lo):
        return None
    bar_range = h - lo
    if bar_range <= 0:
        return None
    ibs = (c - lo) / bar_range
    if ibs < 0.2:
        return "long"
    if ibs > 0.8:
        return "short"
    return None
