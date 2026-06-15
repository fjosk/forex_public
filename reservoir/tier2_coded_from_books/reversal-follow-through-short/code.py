# Engine signal function for 'reversal_follow_through_short' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def reversal_follow_through_short(I, i, htf):
    if i < 1:
        return None
    h0, h1 = I["high"][i], I["high"][i-1]
    l0, l1 = I["low"][i], I["low"][i-1]
    c0, c1 = I["close"][i], I["close"][i-1]
    if _nan(h0, h1, l0, l1, c0, c1):
        return None
    if l0 < l1 and c0 > c1:
        return "short"
    if h0 > h1 and c0 < c1:
        return "long"
    return None
