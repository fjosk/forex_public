# Engine signal function for 'outside_reversal_rsi' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def outside_reversal_rsi(I, i, htf):
    if i < 1:
        return None
    h0, h1 = I["high"][i], I["high"][i-1]
    l0, l1 = I["low"][i], I["low"][i-1]
    c0, c1 = I["close"][i], I["close"][i-1]
    r = I["rsi"][i]
    if _nan(h0, h1, l0, l1, c0, c1, r):
        return None
    outside = h0 > h1 and l0 < l1
    if outside and c0 < c1 and r > 60:
        return "short"
    if outside and c0 > c1 and r > 40 - 1e-9 and r < 40:
        return "long"
    return None
