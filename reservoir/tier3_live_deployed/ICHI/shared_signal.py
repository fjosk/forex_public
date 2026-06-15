# Shared signal function 'ichi' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def ichi(ind, pos, htf=None):
    """Ichimoku TK cross taken only in the cloud's direction: long on Tenkan-over-Kijun above the
    cloud, short on the mirror below it. ind carries ich_ten/ich_kij/ich_a/ich_b/close; the span
    arrays are decision-time aligned by the caller (LAB shifts by disp; TRADE evaluates the
    point form, proven identical at the last bar)."""
    ten, kij, ten1, kij1 = ind["ich_ten"][pos], ind["ich_kij"][pos], ind["ich_ten"][pos - 1], ind["ich_kij"][pos - 1]
    c, a, b = ind["close"][pos], ind["ich_a"][pos], ind["ich_b"][pos]
    if _nan(ten, kij, ten1, kij1, c, a, b):
        return None
    top, bot = max(a, b), min(a, b)
    if ten > kij and ten1 <= kij1 and c > top:
        return "long"
    if ten < kij and ten1 >= kij1 and c < bot:
        return "short"
    return None
