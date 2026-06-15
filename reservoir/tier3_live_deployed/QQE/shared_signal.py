# Shared signal function 'qqe' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def qqe(ind, pos, htf=None):
    """QQE: smoothed-RSI (rsi_ma) crosses the QQE trailing line; long above the line while >50,
    short below while <50."""
    r, l, r1, l1 = ind["qqe_rsima"][pos], ind["qqe_line"][pos], ind["qqe_rsima"][pos - 1], ind["qqe_line"][pos - 1]
    if _nan(r, l, r1, l1):
        return None
    if r > l and r1 <= l1 and r > 50:
        return "long"
    if r < l and r1 >= l1 and r < 50:
        return "short"
    return None
