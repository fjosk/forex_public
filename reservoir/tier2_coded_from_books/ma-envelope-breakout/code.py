# Engine signal function for 'ma_envelope_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def ma_envelope_breakout(I, i, htf):
    if i < 1:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]
    s = I['sma20'][i]; s1 = I['sma20'][i-1]
    if _nan(c, c1, s, s1):
        return None
    up = s * 1.03; lo = s * 0.97
    if c > up and c1 <= s1 * 1.03:
        return 'long'
    if c < lo and c1 >= s1 * 0.97:
        return 'short'
    return None
