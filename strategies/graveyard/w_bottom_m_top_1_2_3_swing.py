#!/usr/bin/env python3
"""w_bottom_m_top_1_2_3_swing -- W bottom / M top (double bottom/top with 1-2-3 swing structure). j_person_a_complete_guide_to_technical_trading_tac.

Long: after downtrend, price makes low (pt1 = prior fractal low), rallies (pt2 = intervening
fractal high), pulls back to pt3 > pt1 (higher low), then close breaks above pt2 high -> buy.
Short: high (pt1 = fractal high), pullback (pt2 = fractal low), rally to pt3 < pt1 (lower high),
then close breaks below pt2 low -> sell. Uses fractal pivot indicators.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "w_bottom_m_top_1_2_3_swing",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "close,frac_up_px,frac_dn_px",
    "long": "W bottom: two fractal lows where second low > first; close breaks above intervening fractal high (pt2)",
    "short": "M top: two fractal highs where second high < first; close breaks below intervening fractal low (pt2)",
    "desc": "W bottom / M top 1-2-3 swing: double bottom/top confirmed by breakout of the reaction extreme",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}


def _find_two_pivots(arr, pos, look=80):
    """Return (px1, px2) = two most recent DISTINCT pivot prices, px2 is newer."""
    px2 = px1 = None
    prev = arr[pos]
    for k in range(pos-1, max(pos-look, 0), -1):
        if nan(arr[k]):
            continue
        if px2 is None:
            px2 = prev
        if abs(arr[k] - px2) > 1e-8:
            px1 = arr[k]
            break
    return px1, px2


def signal(ind, pos, htf=None):
    """W bottom / M top: second pivot milder than first + breakout confirmation."""
    if pos < 5:
        return None
    c      = ind["close"]
    fup_px = ind["frac_up_px"]
    fdn_px = ind["frac_dn_px"]
    if nan(c[pos], fup_px[pos], fdn_px[pos]):
        return None

    # --- Long: W bottom ---
    # Find two most recent fractal lows
    dn1, dn2 = _find_two_pivots(fdn_px, pos)
    if dn1 is not None and dn2 is not None and not nan(dn1, dn2):
        # dn2 is more recent; pt3 (second low) must be HIGHER than pt1 (first low)
        if dn2 > dn1:
            # Intervening fractal high (pt2) = current frac_up_px as the reaction high
            pt2_high = fup_px[pos]
            if not nan(pt2_high) and c[pos] > pt2_high:
                return "long"

    # --- Short: M top ---
    up1, up2 = _find_two_pivots(fup_px, pos)
    if up1 is not None and up2 is not None and not nan(up1, up2):
        if up2 < up1:   # second high is lower
            pt2_low = fdn_px[pos]
            if not nan(pt2_low) and c[pos] < pt2_low:
                return "short"

    return None
