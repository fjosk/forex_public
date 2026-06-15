# Engine signal function for 'cup_cap_3bar_pivot' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def cup_cap_3bar_pivot(I, i, htf):
    if i < 2:
        return None
    c, e50 = I["close"][i], I["ema50"][i]
    h0, h1, h2 = I["high"][i], I["high"][i-1], I["high"][i-2]
    l0, l1, l2 = I["low"][i], I["low"][i-1], I["low"][i-2]
    if _nan(c, e50, h0, h1, h2, l0, l1, l2):
        return None
    cap = h1 > h2 and h1 > h0
    cup = l1 < l2 and l1 < l0
    if c < e50 and cap and c > h1:
        return "long"
    if c > e50 and cup and c < l1:
        return "short"
    return None
