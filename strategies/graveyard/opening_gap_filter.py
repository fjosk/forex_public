#!/usr/bin/env python3
"""opening_gap_filter -- Opening gap up/gap down continuation bias. buku_panduan.

Gap up (open > prior close) -> long; gap down (open < prior close) -> short.
Applies a minimum gap size filter (0.05% of close) to avoid trivial overnight noise.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "opening_gap_filter",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "open,close",
    "long": "open > prior close by >= 0.05% (gap up -> continuation long)",
    "short": "open < prior close by >= 0.05% (gap down -> continuation short)",
    "desc": "Opening gap continuation: gap up or down signals directional bias for the session",
    "source": "buku_panduan BCA Sekuritas BEST manual, Section 10.4 p.56",
}


def signal(ind, pos, htf=None):
    """Opening gap up/down continuation signal."""
    if pos < 1:
        return None
    op = ind["open"][pos]
    c1 = ind["close"][pos - 1]
    if nan(op, c1) or c1 == 0:
        return None
    gap_pct = (op - c1) / c1
    threshold = 0.0005  # 0.05% minimum gap
    if gap_pct >= threshold:
        return "long"
    if gap_pct <= -threshold:
        return "short"
    return None
