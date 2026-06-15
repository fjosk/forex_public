#!/usr/bin/env python3
"""williams_r_timing_entry -- Williams %R timing entry: add to uptrend when %R near low (oversold dip), add to downtrend when near high (overbought rally). trading_systems_and_methods_kaufman_perry_j_kaufma Ch6."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "williams_r_timing_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h-4h",
    "indicators": "willr,ema50 (HTF bias via htf arg)",
    "long": "%R <= -80 (close near 10-day low = dip) within major uptrend",
    "short": "%R >= -20 (close near 10-day high = rally) within major downtrend",
    "desc": "Williams %R timing: buy dips (%R oversold) in major uptrend; sell rallies (%R overbought) in major downtrend",
    "source": "book: trading_systems_and_methods_kaufman_perry_j_kaufma, Ch6",
}

# Engine %R convention: 0 = overbought (close near high), -100 = oversold (close near low)
OB_THRESH = -20.0   # %R >= -20: close near high = overbought/rally in downtrend
OS_THRESH = -80.0   # %R <= -80: close near low = oversold/dip in uptrend


def signal(ind, pos, htf=None):
    """Trend-direction entry on %R dip/rally timing using HTF bias."""
    if pos < 1:
        return None
    wr = ind["willr"][pos]
    if nan(wr):
        return None
    # HTF trend
    if htf is not None:
        bias = htf["bias"][pos] if not nan(htf["bias"][pos]) else 0
    else:
        c = ind["close"][pos]
        e = ind["ema50"][pos]
        if nan(c, e):
            return None
        bias = 1 if c > e else -1
    if bias > 0 and wr <= OS_THRESH:
        return "long"
    if bias < 0 and wr >= OB_THRESH:
        return "short"
    return None
