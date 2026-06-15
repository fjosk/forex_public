# Engine signal function for 'dual_lookback_pullback' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dual_lookback_pullback(I, i, htf):
    if i < 30:
        return None
    c, c9, c30 = I["close"][i], I["close"][i-9], I["close"][i-30]
    if _nan(c, c9, c30):
        return None
    if c > c30 and c < c9:                    # longer-term up, short-term dip -> buy the pullback
        return "long"
    if c < c30 and c > c9:                    # longer-term down, short-term pop -> sell the bounce
        return "short"
    return None
