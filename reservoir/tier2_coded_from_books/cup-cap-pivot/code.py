# Engine signal function for 'cup_cap_pivot' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def cup_cap_pivot(I, i, htf):
    if i < 2:
        return None
    h, h1, h2 = I["high"][i], I["high"][i-1], I["high"][i-2]
    l, l1, l2 = I["low"][i], I["low"][i-1], I["low"][i-2]
    c, c1 = I["close"][i], I["close"][i-1]
    e1 = I["ema20"][i-1]
    if _nan(h, h1, h2, l, l1, l2, c, c1, e1):
        return None
    cap = h1 > h2 and h1 > h
    cup = l1 < l2 and l1 < l
    if cup and c > h1 and c1 < e1:
        return "long"
    if cap and c < l1 and c1 > e1:
        return "short"
    return None
