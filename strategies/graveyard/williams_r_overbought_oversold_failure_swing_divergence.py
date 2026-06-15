#!/usr/bin/env python3
"""williams_r_overbought_oversold_failure_swing_divergence -- Williams %R OB/OS with HTF trend gate and failure-swing (turn before reaching line). elder_alexander_trading_for_a_living Sec29."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "williams_r_overbought_oversold_failure_swing_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h-4h",
    "indicators": "willr,ema50 (HTF bias via htf arg)",
    "long": "%R falls below -90 (oversold) in uptrend OR failure swing (turns up without reaching -90)",
    "short": "%R rises above -10 (overbought) in downtrend OR failure swing (turns down without reaching -10)",
    "desc": "Williams %R OB/OS entry with HTF trend filter; failure-swing variant also captured",
    "source": "book: elder_alexander_trading_for_a_living, Sec29",
}

# Engine uses 0..-100 convention (negative scale, -100=oversold, 0=overbought)
OB = -10.0   # %R >= -10 = overbought
OS = -90.0   # %R <= -90 = oversold


def signal(ind, pos, htf=None):
    """%R OB/OS reversal, gated on HTF trend. Engine %R convention: 0 at top, -100 at bottom."""
    if pos < 1:
        return None
    wr = ind["willr"][pos]
    wr1 = ind["willr"][pos - 1]
    if nan(wr, wr1):
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
    # OB/OS signal: enter when %R touches zone in direction of HTF trend
    if bias >= 0 and wr <= OS:
        return "long"
    if bias <= 0 and wr >= OB:
        return "short"
    # Failure swing: %R turns before reaching the extreme line
    # Long failure: %R was declining but turns up (wr > wr1) in lower half (< -50) without reaching OS
    if bias >= 0 and OS < wr < -50 and wr > wr1:
        return "long"
    # Short failure: %R turns down (wr < wr1) in upper half (> -50) without reaching OB
    if bias <= 0 and -50 < wr < OB and wr < wr1:
        return "short"
    return None
