# Engine signal function for 'nested_swing_structure' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def nested_swing_structure(I, i, htf):
    if i < 1:
        return None
    fd, fu = I["frac_dn"][i], I["frac_up"][i]
    fd_px, fu_px = I["frac_dn_px"][i], I["frac_up_px"][i]
    c, e50 = I["close"][i], I["ema50"][i]
    if _nan(c, e50):
        return None
    # frac_*_px is forward-filled, so the value at i-1 is the PRIOR confirmed
    # swing price (the one in effect right before a new fractal confirms at i).
    prev_swing_low = I["frac_dn_px"][i-1]
    prev_swing_high = I["frac_up_px"][i-1]
    if fd and not _nan(fd_px, prev_swing_low) and fd_px > prev_swing_low and c > e50:
        return "long"   # higher-low above prior swing low, price above EMA50
    if fu and not _nan(fu_px, prev_swing_high) and fu_px < prev_swing_high and c < e50:
        return "short"  # lower-high below prior swing high, price below EMA50
    return None
