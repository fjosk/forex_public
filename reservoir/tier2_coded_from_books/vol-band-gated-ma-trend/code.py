# Engine signal function for 'vol_band_gated_ma_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def vol_band_gated_ma_trend(I, i, htf):
    if i < 2:
        return None
    va, vd, ac = I["vavg"][i], I["vsd"][i], I["abschg"][i]
    s, s1, s2 = I["sma50"][i], I["sma50"][i-1], I["sma50"][i-2]
    if _nan(va, vd, ac, s, s1, s2):
        return None
    low_lim = va - vd
    high_lim = va + 2.0 * vd
    if not (ac > low_lim and ac < high_lim):
        return None
    if s > s1 and s1 <= s2:
        return "long"
    if s < s1 and s1 >= s2:
        return "short"
    return None
