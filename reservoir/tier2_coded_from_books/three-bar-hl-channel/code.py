# Engine signal function for 'three_bar_hl_channel' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def three_bar_hl_channel(I, i, htf):
    if i < 1:
        return None
    e, e1 = I["ema50"][i], I["ema50"][i-1]
    lo, lo1 = I["low"][i], I["low"][i-1]
    hi, hi1 = I["high"][i], I["high"][i-1]
    mal, mal1 = I["mal3"][i], I["mal3"][i-1]
    mah, mah1 = I["mah3"][i], I["mah3"][i-1]
    if _nan(e, e1, lo, lo1, hi, hi1, mal, mal1, mah, mah1):
        return None
    up = e > e1
    dn = e < e1
    if up and lo <= mal and lo1 > mal1:
        return "long"
    if dn and hi >= mah and hi1 < mah1:
        return "short"
    return None
