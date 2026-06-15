# Engine signal function for 'range_compression_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def range_compression_breakout(I, i, htf):
    if i < 1:
        return None
    r5, r50 = I["rng5"][i], I["rng50"][i]
    c, s = I["close"][i], I["sma50"][i]
    h, l = I["high"][i], I["low"][i]
    du1, dl1 = I["dc_up"][i-1], I["dc_lo"][i-1]
    if _nan(r5, r50, c, s, h, l, du1, dl1):
        return None
    if not (r5 <= 0.60 * r50):
        return None
    if c > s and h >= du1:
        return "long"
    if c < s and l <= dl1:
        return "short"
    return None
