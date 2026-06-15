#!/usr/bin/env python3
"""island_reversal_gap_out_gap_back_entry -- Island reversal: second gap confirms isolated cluster. encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul.

Island bottom: bar[a] gaps down from [a-1] (high[a]<low[a-1]); one or more bars in the island;
bar[b] gaps up out of the island (low[b]>high[b-1]) -> long entry at bar b.
Island top: bar[a] gaps up; bar[b] gaps down -> short entry.
Signal fires at bar b (pos=current). Looks back up to 10 bars for the first opposing gap.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "island_reversal_gap_out_gap_back_entry",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h-1d",
    "indicators": "high,low,close",
    "long": "Island bottom: prior gap-down creating an isolated zone; current bar gaps up out of it -> long",
    "short": "Island top: prior gap-up creating isolated zone; current bar gaps down out -> short",
    "desc": "Island reversal: second opposing gap leaves a stranded cluster, entry on the second gap",
    "source": "book:encyclopedia_of_chart_patterns_2nd_ed_thomas_n_bul",
}

_MAX_ISLAND_BARS = 8   # max bars between the two opposing gaps


def signal(ind, pos, htf=None):
    """Island reversal: current bar's gap must be opposite to a recent prior gap."""
    if pos < 3:
        return None
    h  = ind["high"]
    lo = ind["low"]
    c  = ind["close"]
    if nan(h[pos], lo[pos], c[pos], h[pos-1], lo[pos-1]):
        return None

    # Current bar gaps UP (low > prior high) -> look back for an initial gap DOWN
    if lo[pos] > h[pos-1]:
        for k in range(1, min(_MAX_ISLAND_BARS + 1, pos)):
            if nan(h[pos-k-1], lo[pos-k]):
                break
            if h[pos-k] < lo[pos-k-1]:   # gap down from bar k+1 -> bar k
                return "long"
        return None

    # Current bar gaps DOWN (high < prior low) -> look back for an initial gap UP
    if h[pos] < lo[pos-1]:
        for k in range(1, min(_MAX_ISLAND_BARS + 1, pos)):
            if nan(lo[pos-k-1], h[pos-k]):
                break
            if lo[pos-k] > h[pos-k-1]:   # gap up from bar k+1 -> bar k
                return "short"
        return None

    return None
