#!/usr/bin/env python3
"""lunch_break_mean_reversion -- Midday mean-reversion: fade the morning return at 17:00 UTC (noon ET).

At noon ET (17:00 UTC on 1h bars), compare close vs prior close as a morning-return proxy.
Positive morning return -> short (expect reversal); negative -> long. Hold 1 bar (~1h).
FX note: the lunch-break liquidity dip is an equity-market microstructure effect; this tests
whether a similar time-of-day mean-reversion rhythm exists in FX.
No volume -> FX-applicable (partial).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "lunch_break_mean_reversion",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "close, hour_utc",
    "long": "at hour_utc==17: close < close[-1] (morning fell -> fade up)",
    "short": "at hour_utc==17: close > close[-1] (morning rose -> fade down)",
    "desc": "Lunch break mean reversion: fade prior-hour return at noon ET (17:00 UTC) 1h hold",
    "source": "github.com/QuantConnect/Lean Algorithm.Python/Alphas/MeanReversionLunchBreakAlpha.py",
}


def signal(ind, pos, htf=None):
    """Noon ET (17:00 UTC) mean-reversion: fade prior close direction."""
    if pos < 1:
        return None
    hr = ind["hour_utc"][pos]
    if nan(hr):
        return None
    if int(hr) != 17:
        return None
    c0 = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    if nan(c0, c1):
        return None
    morning_return = (c0 - c1) / c1 if c1 != 0 else 0
    if morning_return < 0:
        return "long"
    if morning_return > 0:
        return "short"
    return None
