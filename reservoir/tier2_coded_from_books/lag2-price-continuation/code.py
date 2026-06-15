# Engine signal function for 'lag2_price_continuation' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def lag2_price_continuation(I, i, htf):
    if i < 3:
        return None
    c2, c3 = I["close"][i-2], I["close"][i-3]
    if _nan(c2, c3):
        return None
    if c2 > c3:
        return "long"
    if c2 < c3:
        return "short"
    return None
