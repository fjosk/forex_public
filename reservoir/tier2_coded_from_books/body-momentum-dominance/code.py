# Engine signal function for 'body_momentum_dominance' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def body_momentum_dominance(I, i, htf):
    if i < 1:
        return None
    b = I["body_mom"][i]
    b1 = I["body_mom"][i-1]
    if _nan(b, b1):
        return None
    if b > 70 and b1 <= 70:
        return "long"
    if b < 20 and b1 >= 20:
        return "short"
    return None
