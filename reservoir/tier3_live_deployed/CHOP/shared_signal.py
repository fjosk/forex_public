# Shared signal function 'chop_breakout' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def chop_breakout(ind, pos, htf=None):
    """Choppiness-regime-exit breakout: when the Choppiness Index drops THROUGH 38.2 (ranging ->
    trending transition), enter in the direction of close vs EMA50. ind carries chop/close/ema50.
    Forward-test candidate (cleared the gate on SOL/NEAR, 3/3-engine + walk-forward ROBUST + rolling
    ROBUST, but FRAGILE under the execution-stress filter; paper/testnet only, NOT a proven edge,
    NOT on the live roster)."""
    ch, ch1, c, e = ind["chop"][pos], ind["chop"][pos - 1], ind["close"][pos], ind["ema50"][pos]
    if _nan(ch, ch1, c, e):
        return None
    if ch1 >= 38.2 and ch < 38.2:
        if c > e:
            return "long"
        if c < e:
            return "short"
    return None
