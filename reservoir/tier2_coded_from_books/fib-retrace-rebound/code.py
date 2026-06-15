# Engine signal function for 'fib_retrace_rebound' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def fib_retrace_rebound(I, i, htf):
    if i < 1:
        return None
    H, L = I["frac_up_px"][i], I["frac_dn_px"][i]
    c, e50 = I["close"][i], I["ema50"][i]
    lo, hi = I["low"][i], I["high"][i]
    if _nan(H, L, c, e50, lo, hi) or H <= L:
        return None
    rng = H - L
    tol = 0.0025 * c

    def near(lvl):
        return abs(c - lvl) <= tol

    if c > e50 and (near(H - 0.382 * rng) or near(H - 0.5 * rng) or near(H - 0.618 * rng)) and lo >= L:
        return "long"     # uptrend pullback into a fib retracement, swing low held
    if c < e50 and (near(L + 0.382 * rng) or near(L + 0.5 * rng) or near(L + 0.618 * rng)) and hi <= H:
        return "short"    # downtrend rally into a fib retracement, swing high held
    return None
