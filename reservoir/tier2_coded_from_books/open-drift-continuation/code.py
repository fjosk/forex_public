# Engine signal function for 'open_drift_continuation' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def open_drift_continuation(I, i, htf):
    do, plc, c, a = I["day_open"][i], I["prev_dlc"][i], I["close"][i], I["atr"][i]
    if _nan(do, plc, c, a) or a <= 0:
        return None
    gap_atr = (do - plc) / a
    if 0.3 <= gap_atr <= 1.5 and c > do:
        return "long"
    if -1.5 <= gap_atr <= -0.3 and c < do:
        return "short"
    return None
