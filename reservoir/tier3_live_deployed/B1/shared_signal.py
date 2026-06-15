# Shared signal function 'b1' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def b1(ind, pos, htf=None):
    """B1 MACD weak-rally SELL (short only): price drifted up over 3 bars while the MACD line is
    still <=0 and the histogram is negative and rolling over."""
    c, c3 = ind["close"][pos], ind["close"][pos - 3]
    ml, mh, mh1 = ind["macd"][pos], ind["macd_hist"][pos], ind["macd_hist"][pos - 1]
    if _nan(c, c3, ml, mh, mh1):
        return None
    if c > c3 and ml <= 0 and mh < 0 and mh < mh1:
        return "short"
    return None
