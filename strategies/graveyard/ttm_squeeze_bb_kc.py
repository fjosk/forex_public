#!/usr/bin/env python3
"""ttm_squeeze_bb_kc -- TTM Squeeze (Bollinger inside Keltner) momentum breakout scalp.

Squeeze is ON when bb_lo > kc_lo and bb_up < kc_up. Squeeze fires when BB expands
outside KC. Enter in direction of momentum proxy (close vs bb_mid). Require at least
3 consecutive squeeze bars before the fire.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "ttm_squeeze_bb_kc",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m-15m",
    "indicators": "bb_up, bb_lo, bb_mid, kc_up, kc_lo, close",
    "long": "BB expands outside KC (squeeze fires) AND close > bb_mid (positive momentum)",
    "short": "squeeze fires AND close < bb_mid (negative momentum)",
    "desc": "TTM Squeeze: BB inside KC compression then expansion momentum scalp",
    "source": "web:https://volatilitybox.com/research/ttm-squeeze-indicator/",
}

_SQUEEZE_MIN_BARS = 3


def signal(ind, pos, htf=None):
    """TTM Squeeze BB-KC compression breakout scalp."""
    bb_up = ind["bb_up"]
    bb_lo = ind["bb_lo"]
    bb_mid = ind["bb_mid"]
    kc_up = ind["kc_up"]
    kc_lo = ind["kc_lo"]
    close = ind["close"]

    # Check current bar and previous bar values
    b_up0 = bb_up[pos]; b_lo0 = bb_lo[pos]; bm0 = bb_mid[pos]
    k_up0 = kc_up[pos]; k_lo0 = kc_lo[pos]; c0 = close[pos]
    b_up1 = bb_up[pos - 1]; b_lo1 = bb_lo[pos - 1]
    k_up1 = kc_up[pos - 1]; k_lo1 = kc_lo[pos - 1]
    if nan(b_up0, b_lo0, bm0, k_up0, k_lo0, c0, b_up1, b_lo1, k_up1, k_lo1):
        return None

    # Current bar: squeeze is OFF (fired)
    squeeze_off_now = not (b_lo0 > k_lo0 and b_up0 < k_up0)
    # Previous bar: squeeze was ON
    squeeze_on_prev = b_lo1 > k_lo1 and b_up1 < k_up1

    if not (squeeze_off_now and squeeze_on_prev):
        return None

    # Count consecutive squeeze bars before pos (need at least _SQUEEZE_MIN_BARS)
    count = 0
    i = pos - 1
    while i >= 0 and count < _SQUEEZE_MIN_BARS:
        bi_up = bb_up[i]; bi_lo = bb_lo[i]; ki_up = kc_up[i]; ki_lo = kc_lo[i]
        if nan(bi_up, bi_lo, ki_up, ki_lo):
            break
        if bi_lo > ki_lo and bi_up < ki_up:
            count += 1
            i -= 1
        else:
            break

    if count < _SQUEEZE_MIN_BARS:
        return None

    if c0 > bm0:
        return "long"
    if c0 < bm0:
        return "short"
    return None
