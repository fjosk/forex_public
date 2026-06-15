#!/usr/bin/env python3
"""intraday_etf_momentum_open_close -- Morning direction predicts afternoon: sign of open-to-midday return.

Approximation on 1h bars: at the London-NY session open (hour_utc==13 = 9am ET), compare close
vs day_open to get morning direction. Signal at NY afternoon session (hour_utc==19 = 3pm ET).
Exit at session close (hour_utc==20 or next bar). FX sessions differ from US equity hours but the
intraday momentum effect is directionally testable on forex session timing.
No volume -> FX-applicable (partial -- effect is equity-originated).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "intraday_etf_momentum_open_close",
    "cadences": ["day"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "close, day_open, hour_utc",
    "long": "at hour_utc==19: close at ~13 UTC above day_open (morning return positive)",
    "short": "at hour_utc==19: morning return negative",
    "desc": "Intraday open-to-close momentum: afternoon entry in direction of morning session return",
    "source": "quantconnect.com/learning/articles/investment-strategy-library/intraday-etf-momentum Lou et al. 2019",
}


def signal(ind, pos, htf=None):
    """Afternoon entry in direction of morning session return (1h bar approximation)."""
    hr = ind["hour_utc"][pos]
    if nan(hr):
        return None
    # Only signal at the NY afternoon session (approx 3pm ET = 19:00 UTC)
    if int(hr) != 19:
        return None
    cl = ind["close"][pos]
    do = ind["day_open"][pos]
    if nan(cl, do) or do == 0:
        return None
    morning_return = (cl - do) / do
    if morning_return > 0:
        return "long"
    if morning_return < 0:
        return "short"
    return None
