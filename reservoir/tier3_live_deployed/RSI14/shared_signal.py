# Shared signal function 'rsi14' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def rsi14(ind, pos, htf=None):
    """RSI(14) reversal taken with the EMA200 trend: long above EMA200 on RSI cross up
    through 30, short below EMA200 on RSI cross down through 70."""
    r, r1, c, e200 = ind["rsi"][pos], ind["rsi"][pos - 1], ind["close"][pos], ind["ema200"][pos]
    if _nan(r, r1, c, e200):
        return None
    if c > e200 and r > 30 and r1 <= 30:
        return "long"
    if c < e200 and r < 70 and r1 >= 70:
        return "short"
    return None
