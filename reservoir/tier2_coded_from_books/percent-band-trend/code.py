# Engine signal function for 'percent_band_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def percent_band_trend(I, i, htf):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    up, up1 = I["pct_band_up"][i], I["pct_band_up"][i-1]
    lo, lo1 = I["pct_band_lo"][i], I["pct_band_lo"][i-1]
    if _nan(c, c1, up, up1, lo, lo1):
        return None
    if c > up and c1 <= up1:
        return "long"
    if c < lo and c1 >= lo1:
        return "short"
    return None
