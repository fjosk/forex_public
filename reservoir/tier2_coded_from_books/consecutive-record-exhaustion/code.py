# Engine signal function for 'consecutive_record_exhaustion' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def consecutive_record_exhaustion(I, i, htf):
    if i < 1:
        return None
    o = I['open'][i]; c = I['close'][i]; c1 = I['close'][i-1]
    dnr1 = I['dn_record_count'][i-1]
    upr1 = I['up_record_count'][i-1]
    if _nan(o, c, c1, dnr1, upr1):
        return None
    bull_reversal_bar = c > o and c > c1
    bear_reversal_bar = c < o and c < c1
    if dnr1 >= 8 and bull_reversal_bar:
        return 'long'
    if upr1 >= 8 and bear_reversal_bar:
        return 'short'
    return None
