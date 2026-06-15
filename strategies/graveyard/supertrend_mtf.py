#!/usr/bin/env python3
"""supertrend_mtf -- Supertrend multi-timeframe: HTF bias + current-TF flip. web:forexfactory.com.

4h SuperTrend sets directional bias (via htf); 1h SuperTrend flip provides the entry.
Both timeframes must agree. No volume dependency.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "supertrend_mtf",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "st_dir (current TF flip), htf st_dir (4h bias)",
    "long": "htf st_dir == 1 AND st_dir flips from -1 to +1",
    "short": "htf st_dir == -1 AND st_dir flips from +1 to -1",
    "desc": "Supertrend multi-timeframe: 4h bias + 1h flip entry",
    "source": "web:https://www.forexfactory.com/thread/272796-super-trend-system",
}


def signal(ind, pos, htf=None):
    """HTF SuperTrend bias + current-TF flip entry."""
    sd = ind["st_dir"][pos]
    sdp = ind["st_dir"][pos - 1]
    if nan(sd, sdp):
        return None
    if htf is not None and "st_dir" in htf:
        htf_sd = htf["st_dir"][pos]
        if nan(htf_sd):
            return None
    else:
        # fall back to st_dir_fast as slow/fast proxy when no htf
        htf_sd = ind["st_dir"][pos]
        if nan(htf_sd):
            return None
    if htf_sd == 1 and sd == 1 and sdp == -1:
        return "long"
    if htf_sd == -1 and sd == -1 and sdp == 1:
        return "short"
    return None
