#!/usr/bin/env python3
"""fibonacci_618_pullback -- Fibonacci 61.8% golden zone pullback with reversal bar. web:forexfactory."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "fibonacci_618_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, close, open, high, low",
    "long": "price pulled back into 61.8-78.6% retracement zone of last up-swing (frac_dn to frac_up) with bullish bar",
    "short": "price pulled back into golden zone of last down-swing with bearish bar",
    "desc": "Fibonacci 61.8% golden zone pullback entry using fractal swing points",
    "source": "web:https://www.forexfactory.com/thread/349103-simple-fibonacci-trading",
}

_NEAR_TOL = 0.003  # 0.3% proximity tolerance to the Fib zone


def signal(ind, pos, htf=None):
    """Fibonacci 61.8% pullback in golden zone with bar confirmation."""
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    if nan(c, o, h, lo, fup, fdn):
        return None
    if fup <= fdn:
        return None
    fib_range = fup - fdn
    if fib_range <= 0:
        return None
    # Bull golden zone: 61.8-78.6% from swing high (= 21.4-38.2% from swing low)
    fib_618 = fdn + 0.382 * fib_range   # 61.8% retrace from the top
    fib_786 = fdn + 0.214 * fib_range   # 78.6% retrace from the top
    at_bull_zone = fib_786 <= c <= fib_618
    # Bullish reversal bar: close > open (bullish body), long lower wick
    reversal_bull = c > o and (lo < fib_618)
    if at_bull_zone and reversal_bull:
        return "long"
    # Bear golden zone: 61.8-78.6% retrace from swing low
    fib_618_b = fup - 0.382 * fib_range
    fib_786_b = fup - 0.214 * fib_range
    at_bear_zone = fib_618_b <= c <= fib_786_b
    reversal_bear = c < o and (h > fib_618_b)
    if at_bear_zone and reversal_bear:
        return "short"
    return None
