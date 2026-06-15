# Engine signal function for 'dark_cloud_piercing' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dark_cloud_piercing(I, i, htf):
    if i < 1:
        return None
    o = I['open'][i]; c = I['close'][i]
    o1 = I['open'][i-1]; c1 = I['close'][i-1]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    if _nan(o, c, o1, c1, h1, l1):
        return None
    mid1 = (o1 + c1) / 2.0
    if c1 < o1 and o < l1 and c > mid1 and c < o1:
        return 'long'
    if c1 > o1 and o > h1 and c < mid1 and c > o1:
        return 'short'
    return None
