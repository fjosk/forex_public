#!/usr/bin/env python3
"""fibonacci_pullback_swing -- Fibonacci golden zone pullback with stochastic confirmation. web:swingfolio.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "fibonacci_pullback_swing",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1d",
    "indicators": "frac_up_px, frac_dn_px, close, stoch_k",
    "long": "price in 38.2-61.8% retracement of recent fractal swing, stoch_k < 25",
    "short": "price in 38.2-61.8% retracement of recent fractal swing upward, stoch_k > 75",
    "desc": "Fibonacci 38.2-61.8% golden zone pullback with Stochastic oversold confirmation",
    "source": "web:https://swingfolio.com/blog/fibonacci-pullback-trading-strategy",
}


def signal(ind, pos, htf=None):
    """Fibonacci golden zone pullback entry."""
    swing_hi = ind["frac_up_px"][pos]
    swing_lo = ind["frac_dn_px"][pos]
    c = ind["close"][pos]
    sk = ind["stoch_k"][pos]
    if nan(swing_hi, swing_lo, c, sk):
        return None
    rng = swing_hi - swing_lo
    if rng <= 0:
        return None
    fib382 = swing_hi - 0.382 * rng
    fib618 = swing_hi - 0.618 * rng
    # Long: price in golden zone (retraced from swing high), stochastic oversold
    if fib618 <= c <= fib382 and sk < 25:
        return "long"
    # Short: price retraced back up into golden zone from swing low, stochastic overbought
    fib382_dn = swing_lo + 0.382 * rng
    fib618_dn = swing_lo + 0.618 * rng
    if fib382_dn <= c <= fib618_dn and sk > 75:
        return "short"
    return None
