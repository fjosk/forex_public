# Engine signal function for 'harami_inside_body' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def harami_inside_body(I, i, htf):
    if i < 2:
        return None
    o = I['open'][i]; c = I['close'][i]
    o1 = I['open'][i-1]; c1 = I['close'][i-1]
    o2 = I['open'][i-2]; c2 = I['close'][i-2]
    e1 = I['ema20'][i-1]
    if _nan(o, c, o1, c1, o2, c2, e1):
        return None
    body1 = abs(c1 - o1)
    inside = (max(o, c) <= max(o1, c1)) and (min(o, c) >= min(o1, c1))
    big1 = body1 > 1.5 * abs(c2 - o2)
    if inside and big1 and c1 < o1 and c1 < e1:
        return 'long'
    if inside and big1 and c1 > o1 and c1 > e1:
        return 'short'
    return None
