#!/usr/bin/env python3
"""island_reversal_abandoned_baby_gap_reversal -- Island bottom/top gap-isolation reversal. j_person_a_complete_guide_to_technical_trading_tac.

Island bottom: prior bar gaps down from the one before it, then current bar gaps up above the
isolated bar, leaving it stranded (high[i-1] < low[i-2] AND low[i] > high[i-1]).
Island top mirrors. Abandoned baby = same but the isolated candle is a doji (small body).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "island_reversal_abandoned_baby_gap_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "1h-4h",
    "indicators": "open,high,low,close",
    "long": "Island bottom: bar i-1 gapped down from bar i-2 (high[i-1]<low[i-2]); bar i gaps up above bar i-1 (low[i]>high[i-1]); isolated bar is doji or small body",
    "short": "Island top: bar i-1 gapped up from bar i-2 (low[i-1]>high[i-2]); bar i gaps down below bar i-1 (high[i]<low[i-1]); isolated bar small",
    "desc": "Island reversal / abandoned baby: gap-isolated candle signals exhaustion reversal on the opposing gap",
    "source": "book:j_person_a_complete_guide_to_technical_trading_tac",
}


def signal(ind, pos, htf=None):
    """Island reversal: isolated bar with gaps on both sides signals reversal."""
    if pos < 2:
        return None
    o = ind["open"]
    h = ind["high"]
    lo = ind["low"]
    c = ind["close"]
    if nan(h[pos], lo[pos], h[pos-1], lo[pos-1], h[pos-2], lo[pos-2]):
        return None

    # Island bottom (bullish): prior bar gapped down from bar before it;
    # current bar gaps up above prior bar -- isolated bar between two opposing gaps.
    gap_down_in = h[pos-1] < lo[pos-2]   # bar i-1 gapped down from bar i-2
    gap_up_out  = lo[pos] > h[pos-1]      # bar i gaps up above bar i-1
    if gap_down_in and gap_up_out:
        return "long"

    # Island top (bearish): prior bar gapped up from bar before it;
    # current bar gaps down below prior bar.
    gap_up_in  = lo[pos-1] > h[pos-2]    # bar i-1 gapped up from bar i-2
    gap_down_out = h[pos] < lo[pos-1]    # bar i gaps down below bar i-1
    if gap_up_in and gap_down_out:
        return "short"

    return None
