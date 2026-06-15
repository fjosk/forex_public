# Engine signal function for 'outside_down_lower_open' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def outside_down_lower_open(I, i, htf):
    if i < 2:
        return None
    o = I['open'][i]
    c1 = I['close'][i-1]; h1 = I['high'][i-1]; l1 = I['low'][i-1]
    h2 = I['high'][i-2]; l2 = I['low'][i-2]
    if _nan(o, c1, h1, l1, h2, l2):
        return None
    outside_down = h1 > h2 and l1 < l2 and c1 < l2
    if outside_down and o < c1:
        return 'long'
    outside_up = h1 > h2 and l1 < l2 and c1 > h2
    if outside_up and o > c1:
        return 'short'
    return None
