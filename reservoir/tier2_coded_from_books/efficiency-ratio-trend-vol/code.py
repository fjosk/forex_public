# Engine signal function for 'efficiency_ratio_trend_vol' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def efficiency_ratio_trend_vol(I, i, htf):
    if i < 1:
        return None
    thr = 0.35
    er = I['eff_ratio'][i]; er1 = I['eff_ratio'][i-1]
    e = I['ema20'][i]; e1 = I['ema20'][i-1]
    if _nan(er, er1, e, e1):
        return None
    er_turn = er > thr and er1 <= thr
    if er_turn and e > e1:
        return 'long'
    if er_turn and e < e1:
        return 'short'
    return None
