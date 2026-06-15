# Engine signal function for 'consec_down_close_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def consec_down_close_fade(I, i, htf):
    if i < 3:
        return None
    c, c1, c2, c3 = I["close"][i], I["close"][i-1], I["close"][i-2], I["close"][i-3]
    if _nan(c, c1, c2, c3):
        return None
    if c < c1 and c1 < c2 and c2 < c3:        # three lower closes in a row -> fade long
        return "long"
    if c > c1 and c1 > c2 and c2 > c3:        # three higher closes in a row -> fade short
        return "short"
    return None
