#!/usr/bin/env python3
"""yearly_position_12month_filter -- 12-month range position filter: trade breakouts in lowest/highest third. encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul.

Close in highest third of 12-month range (pos > 0.667) AND upward momentum -> long breakout.
Close in lowest third (pos < 0.333) AND downward momentum -> short breakout.
Uses yr_high/yr_low as the 252-bar range, and SMA200 slope for momentum direction.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "yearly_position_12_month_range_selection_filter",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "close,yr_high,yr_low,sma200",
    "long": "close in highest third of 12-month range (pos>0.667) AND close freshly above SMA200 -> breakout long",
    "short": "close in lowest third (pos<0.333) AND close freshly below SMA200 -> breakout short",
    "desc": "12-month range position filter: breakout longs preferred in upper third, shorts in lower third",
    "source": "encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul Ch60-63 Tables 60.4-63.4",
}


def signal(ind, pos, htf=None):
    """Yearly position + SMA200 cross in the favored range tier."""
    if pos < 1:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    yh   = ind["yr_high"][pos]
    yl   = ind["yr_low"][pos]
    s200 = ind["sma200"][pos]
    s2001 = ind["sma200"][pos - 1]
    if nan(c, c1, yh, yl, s200, s2001):
        return None
    rng = yh - yl
    if rng <= 0:
        return None
    pos_pct = (c - yl) / rng
    cross_up = c > s200 and c1 <= s2001
    cross_dn = c < s200 and c1 >= s2001
    # Best performance for longs: highest third (new highs territory)
    if pos_pct > 0.667 and cross_up:
        return "long"
    # Best performance for shorts: lowest third
    if pos_pct < 0.333 and cross_dn:
        return "short"
    return None
