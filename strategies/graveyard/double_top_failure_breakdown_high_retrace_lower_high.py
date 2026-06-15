#!/usr/bin/env python3
"""double_top_failure_breakdown_high_retrace_lower_high -- Double-top failure: lower high then break of intervening low. douglas_mark_the_disciplined_trader_1990_isbn_0132.

Short setup: price made a prior swing high (frac_up), pulled back, rallied to a LOWER high (second
peak fails), then breaks below the intervening swing low (frac_dn). Uses fractal indicators for
swing points. Mirror long: double-bottom with higher low + break of intervening swing high.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "double_top_failure_breakdown_high_retrace_lower_high",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "close,frac_up,frac_dn,frac_up_px,frac_dn_px",
    "long": "Double bottom: prior swing low, higher swing low (frac_dn_px > prior frac_dn_px), break above intervening swing high (close > frac_up_px)",
    "short": "Double top: prior swing high, lower swing high (frac_up_px < prior frac_up_px), break below intervening swing low (close < frac_dn_px)",
    "desc": "Double-top/bottom failure: second swing fails to match prior extreme; confirmed by break of intervening pivot",
    "source": "book:douglas_mark_the_disciplined_trader_1990_isbn_0132",
}


def signal(ind, pos, htf=None):
    """Double-top/bottom failure breakdown: lower high + break of intervening low (or vice versa)."""
    if pos < 4:
        return None
    c        = ind["close"]
    frac_up  = ind["frac_up"]      # 1.0 when current bar IS a fractal up pivot, else 0
    frac_dn  = ind["frac_dn"]
    fup_px   = ind["frac_up_px"]   # price of the most recent confirmed fractal up pivot
    fdn_px   = ind["frac_dn_px"]   # price of the most recent confirmed fractal dn pivot
    if nan(c[pos], fup_px[pos], fdn_px[pos]):
        return None

    # Look back for the previous fractal pivot prices (one period before the current confirmed one)
    # Strategy: find the second-most-recent fractal up/down pivot to compare heights
    # Search last 50 bars for two distinct frac_up pivots
    prev_fup_px = None
    prev_fdn_px = None
    current_fup_px = fup_px[pos]
    current_fdn_px = fdn_px[pos]

    for k in range(pos-1, max(pos-60, 1), -1):
        if nan(fup_px[k]):
            continue
        if prev_fup_px is None and abs(fup_px[k] - current_fup_px) > 1e-8:
            prev_fup_px = fup_px[k]
        if prev_fup_px is not None:
            break

    for k in range(pos-1, max(pos-60, 1), -1):
        if nan(fdn_px[k]):
            continue
        if prev_fdn_px is None and abs(fdn_px[k] - current_fdn_px) > 1e-8:
            prev_fdn_px = fdn_px[k]
        if prev_fdn_px is not None:
            break

    # --- Short: double-top failure ---
    # Current frac high is LOWER than the prior one AND close breaks below current frac low
    if prev_fup_px is not None and not nan(prev_fup_px):
        lower_high = current_fup_px < prev_fup_px
        break_low  = c[pos] < current_fdn_px
        if lower_high and break_low:
            return "short"

    # --- Long: double-bottom failure ---
    # Current frac low is HIGHER than the prior one AND close breaks above current frac high
    if prev_fdn_px is not None and not nan(prev_fdn_px):
        higher_low  = current_fdn_px > prev_fdn_px
        break_high  = c[pos] > current_fup_px
        if higher_low and break_high:
            return "long"

    return None
