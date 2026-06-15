# Engine signal function for 'belt_hold_flip' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def belt_hold_flip(I, i, htf):
    if i < 1:
        return None
    o = I['open'][i]; h = I['high'][i]; l = I['low'][i]; c = I['close'][i]
    c1 = I['close'][i-1]; e1 = I['ema20'][i-1]
    if _nan(o, h, l, c, c1, e1):
        return None
    rng = h - l
    if rng <= 0:
        return None
    k = 0.05
    if (o - l) <= k * rng and c > o and c1 < e1:
        return 'long'
    if (h - o) <= k * rng and c < o and c1 > e1:
        return 'short'
    return None
