# Engine signal function for 'efficiency_ratio_trend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def efficiency_ratio_trend(I, i, htf):
    if i < 1:
        return None
    er, e, e1, c = I["er10"][i], I["ema20"][i], I["ema20"][i-1], I["close"][i]
    if _nan(er, e, e1, c):
        return None
    if er >= 0.6 and e > e1 and c > e:
        return "long"
    if er >= 0.6 and e < e1 and c < e:
        return "short"
    return None
