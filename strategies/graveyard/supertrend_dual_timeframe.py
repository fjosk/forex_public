#!/usr/bin/env python3
"""supertrend_dual_timeframe -- Dual-timeframe SuperTrend: HTF filter + fast flip entry. web:netpicks.com.

HTF (4h) st_dir sets direction bias; current TF st_dir_fast flip provides the entry trigger.
Only trade in the direction of the higher-timeframe SuperTrend.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "supertrend_dual_timeframe",
    "cadences": ["day"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "st_dir_fast (current TF), htf st_dir (higher TF filter)",
    "long": "htf st_dir == 1 AND st_dir_fast flips from -1 to +1",
    "short": "htf st_dir == -1 AND st_dir_fast flips from +1 to -1",
    "desc": "Dual-timeframe SuperTrend: HTF direction filter + fast-TF flip entry",
    "source": "web:https://www.netpicks.com/supertrend-indicator/",
}


def signal(ind, pos, htf=None):
    """HTF SuperTrend filter + fast SuperTrend flip entry."""
    sdf, sdfp = ind["st_dir_fast"][pos], ind["st_dir_fast"][pos - 1]
    if nan(sdf, sdfp):
        return None
    # use htf st_dir for higher-TF bias when available; fall back to st_dir
    if htf is not None and "st_dir" in htf:
        htf_sd = htf["st_dir"][pos]
        if nan(htf_sd):
            return None
    else:
        htf_sd = ind["st_dir"][pos]
        if nan(htf_sd):
            return None
    if htf_sd == 1 and sdf == 1 and sdfp == -1:
        return "long"
    if htf_sd == -1 and sdf == -1 and sdfp == 1:
        return "short"
    return None
