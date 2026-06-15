#!/usr/bin/env python3
"""fibonacci_618_ote_pullback -- Fibonacci 61.8% OTE pullback entry using fractals. web:elirox."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "fibonacci_618_ote_pullback",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "frac_up_px, frac_dn_px, rsi, close, low, high",
    "long": "close near 61.8% retrace of last up-fractal swing (from frac_dn_px to frac_up_px), rsi < 50",
    "short": "close near 61.8% retrace of last down-fractal swing, rsi > 50",
    "desc": "Fibonacci 61.8% OTE pullback entry using fractal swing high/low, RSI confirmation",
    "source": "web:https://elirox.com/strategies/fibonacci-retracement-forex-strategy-guide/",
}

_NEAR_TOL = 0.003  # 0.3% of price = near the Fib level


def signal(ind, pos, htf=None):
    """Fibonacci 61.8% pullback entry from fractal swing extremes."""
    c = ind["close"][pos]
    fup = ind["frac_up_px"][pos]
    fdn = ind["frac_dn_px"][pos]
    rsi = ind["rsi"][pos]
    if nan(c, fup, fdn, rsi):
        return None
    if fup <= fdn:
        return None
    fib_range = fup - fdn
    if fib_range <= 0:
        return None
    # Bull setup: pullback to 61.8% from swing high (0.382 up from swing low)
    fib_618_bull = fdn + 0.382 * fib_range
    # Bear setup: pullback to 61.8% from swing low (0.382 down from swing high)
    fib_618_bear = fup - 0.382 * fib_range
    near_bull = abs(c - fib_618_bull) / (c + 1e-10) < _NEAR_TOL
    near_bear = abs(c - fib_618_bear) / (c + 1e-10) < _NEAR_TOL
    # Long: near the bull retracement level, price approaching from above, rsi < 50
    if near_bull and rsi < 50:
        return "long"
    # Short: near the bear retracement level, rsi > 50
    if near_bear and rsi > 50:
        return "short"
    return None
