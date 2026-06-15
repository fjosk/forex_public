#!/usr/bin/env python3
"""ny_killzone_london_overlap -- NY open killzone pivot breakout/bounce (13-16 UTC).

Time-gated to 13:00-16:00 UTC (08:00-11:00 ET = London-NY overlap).
Entry: price breaks above piv_r1 (resistance breakout) or bounces from piv_s1
with a bullish body_mom, or breaks below piv_s1 (support breakdown).
body_mom > 0 confirms bullish pressure; body_mom < 0 confirms bearish.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "ny_killzone_london_overlap",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "5m, 15m",
    "indicators": "hour_utc, close, piv_r1, piv_s1, body_mom",
    "long": "13-16 UTC: close breaks above piv_r1 OR close near piv_s1 with body_mom > 0",
    "short": "13-16 UTC: close breaks below piv_s1 OR close near piv_r1 with body_mom < 0",
    "desc": "NY killzone (London-NY overlap 13-16 UTC) pivot breakout and bounce",
    "source": "web:https://theforexgeek.com/new-york-killzone-strategy/",
}

_KZ_START = 13
_KZ_END = 16
_NEAR_PCT = 0.002   # 0.2% proximity to pivot = "near" threshold


def signal(ind, pos, htf=None):
    """NY killzone pivot breakout/bounce."""
    hour = ind["hour_utc"][pos]
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    r1 = ind["piv_r1"][pos]
    s1 = ind["piv_s1"][pos]
    bm = ind["body_mom"][pos]
    if nan(hour, c, c1, r1, s1, bm):
        return None
    if not (_KZ_START <= hour <= _KZ_END):
        return None
    if c == 0:
        return None

    # Breakout above piv_r1
    if c > r1 and c1 <= r1:
        return "long"
    # Bounce from piv_s1 support
    near_s1 = abs(c - s1) / c < _NEAR_PCT
    if near_s1 and bm > 0:
        return "long"
    # Breakdown below piv_s1
    if c < s1 and c1 >= s1:
        return "short"
    # Rejection at piv_r1
    near_r1 = abs(c - r1) / c < _NEAR_PCT
    if near_r1 and bm < 0:
        return "short"
    return None
