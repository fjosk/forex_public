#!/usr/bin/env python3
"""weekday_reversal_up_monday_down_tuesday -- Two-day same-direction run on Mon+Tue predicts
a Wednesday reversal (~58% historically across 23 futures markets).
trading_systems_and_methods_kaufman_perry_j_kaufma Ch.15.

XX pattern (Mon and Tue both moved in the same direction) -> fade on Tuesday close.
Enter on Tuesday's close in the direction OPPOSITE the 2-day run.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "weekday_reversal_up_monday_down_tuesday",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1d",
    "indicators": "dow,close",
    "long": "Tuesday bar (dow==1) AND both Monday and Tuesday closed DOWN - fade the down-run long",
    "short": "Tuesday bar (dow==1) AND both Monday and Tuesday closed UP - fade the up-run short",
    "desc": "Weekday reversal XX pattern: two-day same-direction Mon+Tue run reverses on Wednesday ~58%",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch.15 Weekday Patterns pp.400-405",
}


def signal(ind, pos, htf=None):
    """Fade a two-day Mon/Tue run on the Tuesday close."""
    if pos < 2:
        return None
    dw  = ind["dow"][pos]
    c   = ind["close"][pos]
    c1  = ind["close"][pos - 1]
    c2  = ind["close"][pos - 2]
    if nan(dw, c, c1, c2):
        return None
    # Signal fires on Tuesday (weekday 1)
    if int(dw) != 1:
        return None
    mon_up = c1 > c2   # Monday: bar before Tuesday
    tue_up = c > c1    # Tuesday: current bar
    if mon_up and tue_up:
        # Both up -> fade down (short)
        return "short"
    if not mon_up and not tue_up:
        # Both down -> fade up (long)
        return "long"
    return None
