# Engine signal function for 'high_tight_flag_break' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def high_tight_flag_break(I, i, htf):
    if i < 61:
        return None
    h, l, c = I["high"], I["low"], I["close"]
    if _nan(c[i]):
        return None
    base_win = [l[k] for k in range(i-60, i-20)]
    swing_win = [h[k] for k in range(i-20, i-2)]
    flag_h_win = [h[k] for k in range(i-8, i)]
    flag_l_win = [l[k] for k in range(i-8, i)]
    if any(_nan(x) for x in base_win) or any(_nan(x) for x in swing_win) \
            or any(_nan(x) for x in flag_h_win) or any(_nan(x) for x in flag_l_win):
        return None
    base_lo = min(base_win)
    if base_lo == 0:
        return None
    swing_hi = max(swing_win)
    if swing_hi == 0:
        return None
    doubled = (swing_hi - base_lo) / base_lo >= 0.90
    flag_hi = max(flag_h_win)
    flag_lo = min(flag_l_win)
    tight = (swing_hi - flag_lo) / swing_hi <= 0.25
    if doubled and tight and c[i] > flag_hi:
        return "long"
    return None
