# Shared signal function 'copp' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def copp(ind, pos, htf=None):
    """Coppock-curve zero-cross: long when Coppock crosses up through 0, short on the mirror."""
    cp, cp1 = ind["coppock"][pos], ind["coppock"][pos - 1]
    if _nan(cp, cp1):
        return None
    if cp > 0 and cp1 <= 0:
        return "long"
    if cp < 0 and cp1 >= 0:
        return "short"
    return None
