# Engine signal function for 'dual_ma_countertrend' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dual_ma_countertrend(I, i, htf):
    if i < 1:
        return None
    c, s50 = I["close"][i], I["sma50"][i]
    e9, e9p = I["ema9"][i], I["ema9"][i-1]
    e21, e21p = I["ema21"][i], I["ema21"][i-1]
    if _nan(c, s50, e9, e9p, e21, e21p):
        return None
    trend_up = c > s50
    trend_dn = c < s50
    fast_cross_dn = _xdn(e9, e9p, e21, e21p)
    fast_cross_up = _xup(e9, e9p, e21, e21p)
    if trend_up and fast_cross_dn:
        return "long"
    if trend_dn and fast_cross_up:
        return "short"
    return None
