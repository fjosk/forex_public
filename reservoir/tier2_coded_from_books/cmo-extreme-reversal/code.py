# Engine signal function for 'cmo_extreme_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def cmo_extreme_reversal(I, i, htf):
    if i < 1:
        return None
    cm, cm1 = I["cmo"][i], I["cmo"][i-1]
    if _nan(cm, cm1):
        return None
    if cm1 <= -50 and cm > cm1:               # CMO turning up out of oversold extreme
        return "long"
    if cm1 >= 50 and cm < cm1:                 # CMO turning down out of overbought extreme
        return "short"
    return None
