#!/usr/bin/env python3
"""equal_highs_lows_liquidity -- Equal highs/lows liquidity raid + reversal entry.

Scans recent fractal extremes for an equal-level cluster (within 0.1 * ATR).
When price raids that cluster and the body closes back inside, enter in the
reversal direction targeting the opposing cluster.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "equal_highs_lows_liquidity",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h, 4h",
    "indicators": "close, high, low, frac_up_px, frac_dn_px, atr",
    "long": "equal lows cluster identified; spike below cluster; body closes back above",
    "short": "equal highs cluster identified; spike above cluster; body closes back below",
    "desc": "Equal highs/lows liquidity raid: stop-cluster sweep then reversal entry",
    "source": "web:https://acy.com/en/market-news/education/market-education-stop-hunting-trading-swing-highs-lows-liquidity-j-o-20250822-095643/",
}

_LOOKBACK = 50
_EQ_ATR_MULT = 0.1   # proximity threshold for equal level grouping
_MIN_CLUSTER = 2     # minimum fractals at the same level to form a cluster


def _find_cluster(prices, threshold):
    """Return the average price of the first cluster with >= MIN_CLUSTER members."""
    if not prices:
        return None
    for i, px in enumerate(prices):
        group = [p for p in prices if abs(p - px) <= threshold]
        if len(group) >= _MIN_CLUSTER:
            return sum(group) / len(group)
    return None


def signal(ind, pos, htf=None):
    """Equal highs/lows liquidity raid + reversal."""
    c = ind["close"][pos]
    h = ind["high"][pos]
    l = ind["low"][pos]
    atr = ind["atr"][pos]
    if nan(c, h, l, atr) or atr == 0:
        return None

    tol = _EQ_ATR_MULT * atr
    start = max(0, pos - _LOOKBACK)

    # Collect fractal lows and highs from lookback window
    frac_lo_vals = []
    frac_hi_vals = []
    for i in range(start, pos):
        fd = ind["frac_dn_px"][i]
        fu = ind["frac_up_px"][i]
        if not nan(fd):
            frac_lo_vals.append(fd)
        if not nan(fu):
            frac_hi_vals.append(fu)

    # Find equal lows cluster
    eq_lows = _find_cluster(frac_lo_vals, tol)
    if eq_lows is not None:
        if l < eq_lows and c > eq_lows:
            return "long"

    # Find equal highs cluster
    eq_highs = _find_cluster(frac_hi_vals, tol)
    if eq_highs is not None:
        if h > eq_highs and c < eq_highs:
            return "short"

    return None
