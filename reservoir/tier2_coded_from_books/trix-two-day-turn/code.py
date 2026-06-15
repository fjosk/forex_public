# Engine signal function for 'trix_two_day_turn' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def trix_two_day_turn(I, i, htf):
    if i < 2:
        return None
    t = I['trix'][i]; t1 = I['trix'][i-1]; t2 = I['trix'][i-2]
    if _nan(t, t1, t2):
        return None
    if t > t1 and t1 > t2:
        return 'long'
    if t < t1 and t1 < t2:
        return 'short'
    return None
