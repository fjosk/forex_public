# Shared signal function 'atrc' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def atrc(ind, pos, htf=None):
    """ATR-channel breakout: close breaks EMA20 +/- 2*ATR with EMA20 sloping the same way."""
    c, e20, atr, e20p5 = ind["close"][pos], ind["ema20"][pos], ind["atr"][pos], ind["ema20"][pos - 5]
    if _nan(c, e20, atr, e20p5) or atr <= 0:
        return None
    if c > e20 + 2.0 * atr and e20 > e20p5:
        return "long"
    if c < e20 - 2.0 * atr and e20 < e20p5:
        return "short"
    return None
