# Engine signal function for 'bb_band_break_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def bb_band_break_trend(I, i, htf):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    bu, bu1 = I["bb_up"][i], I["bb_up"][i-1]
    bl, bl1 = I["bb_lo"][i], I["bb_lo"][i-1]
    if _nan(c, c1, bu, bu1, bl, bl1):
        return None
    if c > bu and c1 <= bu1:
        return "long"
    if c < bl and c1 >= bl1:
        return "short"
    return None
