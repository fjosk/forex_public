#!/usr/bin/env python3
"""three_bar_four_bar_play -- Narrow-range resting bars after a wide-range bar; breakout of the resting cluster. tradersguidetosuccess.

PRICE/OHLC only. Wide bar = range > 1.5x ATR; resting bars = next 1-2 bars with smaller range holding near wide-bar extreme.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "3_bar_4_bar_play_narrow_range_rest_after_wide_range_bar",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "atr, high, low, close",
    "long": "wide-range up bar followed by 1-2 narrow resting bars; current bar breaks above resting cluster high",
    "short": "wide-range down bar followed by 1-2 narrow resting bars; current bar breaks below resting cluster low",
    "desc": "Narrow-range rest after a wide-range commitment bar, enter on breakout of the resting cluster",
    "source": "tradersguidetosuccess",
}


def signal(ind, pos, htf=None):
    """Narrow-range rest breakout after a wide-range bar."""
    if pos < 3:
        return None
    h = ind["high"]
    l = ind["low"]
    c = ind["close"]
    a = ind["atr"][pos]
    if nan(h[pos], l[pos], c[pos], a) or a <= 0:
        return None

    # bar ranges
    rng_cur = h[pos] - l[pos]
    rng1 = h[pos - 1] - l[pos - 1]
    rng2 = h[pos - 2] - l[pos - 2]
    rng3 = h[pos - 3] - l[pos - 3]

    # wide-range bar threshold: > 1.5x ATR
    wide_thresh = 1.5 * a
    narrow_thresh_factor = 0.7  # resting bar range < 70% of wide bar

    # Pattern: pos-2 is wide up bar, pos-1 is narrow resting bar, pos breaks above
    if rng2 > wide_thresh and c[pos - 2] > (h[pos - 2] + l[pos - 2]) / 2:
        if rng1 < rng2 * narrow_thresh_factor and l[pos - 1] >= l[pos - 2]:
            rest_high = h[pos - 1]
            if h[pos] > rest_high:
                return "long"

    if rng2 > wide_thresh and c[pos - 2] < (h[pos - 2] + l[pos - 2]) / 2:
        if rng1 < rng2 * narrow_thresh_factor and h[pos - 1] <= h[pos - 2]:
            rest_low = l[pos - 1]
            if l[pos] < rest_low:
                return "short"

    # Pattern: pos-3 is wide bar, pos-2 and pos-1 are resting bars, pos breaks
    if rng3 > wide_thresh and c[pos - 3] > (h[pos - 3] + l[pos - 3]) / 2:
        if (rng2 < rng3 * narrow_thresh_factor and l[pos - 2] >= l[pos - 3]
                and rng1 < rng3 * narrow_thresh_factor and l[pos - 1] >= l[pos - 3]):
            rest_high = max(h[pos - 2], h[pos - 1])
            if h[pos] > rest_high:
                return "long"

    if rng3 > wide_thresh and c[pos - 3] < (h[pos - 3] + l[pos - 3]) / 2:
        if (rng2 < rng3 * narrow_thresh_factor and h[pos - 2] <= h[pos - 3]
                and rng1 < rng3 * narrow_thresh_factor and h[pos - 1] <= h[pos - 3]):
            rest_low = min(l[pos - 2], l[pos - 1])
            if l[pos] < rest_low:
                return "short"

    return None
