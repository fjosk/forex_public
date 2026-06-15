# Shared signal function 'chandelier' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def chandelier(ind, pos, htf=None):
    """Chandelier Exit direction flip: long when the ratcheting direction flips -1 -> +1, short on
    the mirror +1 -> -1. ind carries chand_dir (+1/-1 per bar). Forward-test candidate (cleared the
    gate + both walk-forwards on SUI but FRAGILE under execution stress)."""
    d, d1 = ind["chand_dir"][pos], ind["chand_dir"][pos - 1]
    if _nan(d, d1):
        return None
    if d == 1 and d1 == -1:
        return "long"
    if d == -1 and d1 == 1:
        return "short"
    return None
