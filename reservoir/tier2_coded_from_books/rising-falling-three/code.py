# Engine signal function for 'rising_falling_three' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def rising_falling_three(I, i, htf):
    if i < 4:
        return None
    o4 = I['open'][i-4]; c4 = I['close'][i-4]
    h4 = I['high'][i-4]; l4 = I['low'][i-4]
    c = I['close'][i]
    vals = [o4, c4, h4, l4, c]
    for j in (i-3, i-2, i-1):
        vals.extend([I['open'][j], I['close'][j], I['high'][j], I['low'][j]])
    if _nan(*vals):
        return None
    b0 = abs(c4 - o4)
    small = all(abs(I['close'][j] - I['open'][j]) < 0.5 * b0 for j in (i-3, i-2, i-1))
    inside = all(I['high'][j] <= h4 and I['low'][j] >= l4 for j in (i-3, i-2, i-1))
    if c4 > o4 and small and inside and c > c4:
        return 'long'
    if c4 < o4 and small and inside and c < c4:
        return 'short'
    return None
