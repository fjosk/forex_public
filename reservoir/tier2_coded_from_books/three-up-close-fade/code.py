# Engine signal function for 'three_up_close_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def three_up_close_fade(I, i, htf):
    if i < 3:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]; c2 = I['close'][i-2]; c3 = I['close'][i-3]
    h1 = I['high'][i-1]; l1 = I['low'][i-1]
    if _nan(c, c1, c2, c3, h1, l1):
        return None
    long_run = c > c1 and c1 > c2 and c2 > c3
    if long_run and c > h1:
        return 'short'
    short_run = c < c1 and c1 < c2 and c2 < c3
    if short_run and c < l1:
        return 'long'
    return None
