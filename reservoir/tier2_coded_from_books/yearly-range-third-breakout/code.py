# Engine signal function for 'yearly_range_third_breakout' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def yearly_range_third_breakout(I, i, htf):
    if i < 1:
        return None
    yh = I["yr_high"][i]
    yl = I["yr_low"][i]
    c = I["close"][i]
    c1 = I["close"][i-1]
    dcu = I["dc_up"][i-1]
    dcl = I["dc_lo"][i-1]
    if _nan(yh, yl, c, c1, dcu, dcl) or yh <= yl:
        return None
    rng = yh - yl
    lo_b = yl + rng / 3.0
    hi_b = yl + 2.0 * rng / 3.0
    if c > dcu and c1 <= dcu and c <= lo_b:
        return "long"
    if c < dcl and c1 >= dcl and c >= hi_b:
        return "short"
    return None
