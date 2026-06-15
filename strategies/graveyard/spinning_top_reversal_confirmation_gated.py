#!/usr/bin/env python3
"""spinning_top_reversal_confirmation_gated -- Spinning top momentum stall + confirmation candle. currency_trading_for_dummies_2nd_edition_by_brian.

Spinning top: small body, short roughly symmetric tails, appearing after a run of same-direction
candles. Reversal only confirmed by the NEXT candle (the confirmation candle is the signal bar).
Bullish: spinning top after >= 3 down closes, confirmed by an up close. Bearish: mirrors.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "spinning_top_reversal_confirmation_gated",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "open,high,low,close",
    "long": "Spinning top at pos-1 after >=3 consecutive down closes; current bar closes up (confirmation)",
    "short": "Spinning top at pos-1 after >=3 consecutive up closes; current bar closes down (confirmation)",
    "desc": "Spinning top stall pattern with confirmation: small-body symmetric-wick candle after a run + confirming close",
    "source": "book:currency_trading_for_dummies_2nd_edition_by_brian",
}

_BODY_RANGE_MAX = 0.35   # spinning top body <= 35% of bar range
_TAIL_SYM_MAX   = 2.5    # larger tail <= 2.5x smaller tail (roughly symmetric)
_RUN_BARS       = 3      # minimum consecutive same-direction closes before the top


def _is_spinning_top(o, h, lo, c):
    """Return True if the OHLC values define a spinning top."""
    body      = abs(c - o)
    bar_range = h - lo
    if bar_range == 0:
        return False
    if body > _BODY_RANGE_MAX * bar_range:
        return False
    upper_shad = h - max(o, c)
    lower_shad = min(o, c) - lo
    # Symmetric tails: neither dominates strongly
    small_tail = min(upper_shad, lower_shad)
    large_tail = max(upper_shad, lower_shad)
    if small_tail == 0:
        return False    # one tail is zero -> pin bar, not spinning top
    return large_tail <= _TAIL_SYM_MAX * small_tail


def signal(ind, pos, htf=None):
    """Spinning top after a run, confirmed by the current bar."""
    if pos < _RUN_BARS + 1:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    for k in range(pos - _RUN_BARS - 1, pos + 1):
        if nan(o[k], h[k], lo[k], c[k]):
            return None

    # Spinning top must be at pos-1
    if not _is_spinning_top(o[pos-1], h[pos-1], lo[pos-1], c[pos-1]):
        return None

    # Count consecutive same-direction closes ending at pos-2
    # Down run (for bullish setup)
    down_run = 0
    for k in range(pos-2, pos - _RUN_BARS - 2, -1):
        if c[k] < c[k-1]:
            down_run += 1
        else:
            break

    if down_run >= _RUN_BARS and c[pos] > c[pos-1]:
        return "long"

    # Up run (for bearish setup)
    up_run = 0
    for k in range(pos-2, pos - _RUN_BARS - 2, -1):
        if c[k] > c[k-1]:
            up_run += 1
        else:
            break

    if up_run >= _RUN_BARS and c[pos] < c[pos-1]:
        return "short"

    return None
