# Shared signal function 'b10' (from sister-lab/shared/strategies.py).
# Form: fn(ind, pos, htf) -> 'long'|'short'|None. Pure: no I/O, no state.

def b10(ind, pos, htf=None):
    """BINOPT-10 strong-signal Ichimoku: an Ichimoku TK cross taken in the cloud's direction AND
    confirmed by MACD. Long above the cloud on Tenkan-over-Kijun with macd>signal; short on the
    mirror below the cloud with macd<signal. ind carries ich_ten/ich_kij/ich_a/ich_b/close + macd/
    macd_sig (the spans are decision-time aligned by the caller, same as `ichi`). Forward-test
    candidate (cleared the gate on ONDO but rolling-WFO OVERFIT + FRAGILE under stress)."""
    c = ind["close"][pos]
    ten, kij = ind["ich_ten"][pos], ind["ich_kij"][pos]
    ten1, kij1 = ind["ich_ten"][pos - 1], ind["ich_kij"][pos - 1]
    a, b = ind["ich_a"][pos], ind["ich_b"][pos]
    m, s = ind["macd"][pos], ind["macd_sig"][pos]
    if _nan(c, ten, kij, ten1, kij1, a, b, m, s):
        return None
    cloud_top, cloud_bot = max(a, b), min(a, b)
    if c > cloud_top and ten > kij and ten1 <= kij1 and m > s:
        return "long"
    if c < cloud_bot and ten < kij and ten1 >= kij1 and m < s:
        return "short"
    return None
