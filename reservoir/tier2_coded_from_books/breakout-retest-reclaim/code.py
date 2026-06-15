# Engine signal function for 'breakout_retest_reclaim' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def breakout_retest_reclaim(I, i, htf):
    if i < 7:
        return None
    o = I['open'][i]; c = I['close'][i]
    hi = I['high'][i]; lo = I['low'][i]
    dcu = I['dc_up'][i]; dcl = I['dc_lo'][i]
    if _nan(o, c, hi, lo, dcu, dcl):
        return None
    broke_up = False
    for j in range(i-6, i):
        cj = I['close'][j]; dcuj = I['dc_up'][j-1]
        if not _nan(cj, dcuj) and cj > dcuj:
            broke_up = True
            break
    retest = lo <= dcu * 1.002
    hold = c > dcu and c > o
    if broke_up and retest and hold:
        return 'long'
    broke_dn = False
    for j in range(i-6, i):
        cj = I['close'][j]; dclj = I['dc_lo'][j-1]
        if not _nan(cj, dclj) and cj < dclj:
            broke_dn = True
            break
    retest_d = hi >= dcl * 0.998
    hold_d = c < dcl and c < o
    if broke_dn and retest_d and hold_d:
        return 'short'
    return None
