# Engine signal function for 'dual_ma_neutral' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dual_ma_neutral(I, i, htf):
    if i < 1:
        return None
    c = I['close'][i]; c1 = I['close'][i-1]
    e20 = I['ema20'][i]; e20p = I['ema20'][i-1]
    e50 = I['ema50'][i]; e50p = I['ema50'][i-1]
    if _nan(c, c1, e20, e20p, e50, e50p):
        return None
    above = c > e20 and c > e50
    below = c < e20 and c < e50
    above_prev = c1 > e20p and c1 > e50p
    below_prev = c1 < e20p and c1 < e50p
    if above and not above_prev:
        return 'long'
    if below and not below_prev:
        return 'short'
    return None
