#!/usr/bin/env python3
"""multi_rsi_timeframe_divergence -- Multi RSI Timeframe Divergence (approximated). berlinguyinca/freqtrade.

Original uses RSI(14) on base TF vs RSI(14) on 8x HTF resampled TF. Approximated here
using rsi (RSI14) vs rsi2 (RSI2, a fast variant) as a divergence proxy: when fast RSI
has fallen far below the slower RSI the concept of base-TF lagging macro is preserved.
SMA5 / SMA200 long-term bias filter approximated with sma10 (closest to SMA5 available).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "multi_rsi_timeframe_divergence",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversion",
    "tf": "1h",
    "indicators": "rsi, rsi2, sma10, sma200",
    "long": "sma10 >= sma200 AND rsi2 < rsi - 20 (fast RSI lagging slow RSI in bull trend)",
    "short": "not implemented (long-only in source; symmetric short added for FX)",
    "desc": "RSI divergence between fast and slow periods as HTF-divergence approximation with SMA200 bias",
    "source": "web:https://github.com/freqtrade/freqtrade-strategies/blob/main/user_data/strategies/berlinguyinca/MultiRSI.py",
}


def signal(ind, pos, htf=None):
    """Multi RSI divergence -- sma10/sma200 bias + rsi2 lagging rsi by 20 points."""
    r = ind["rsi"][pos]
    r2 = ind["rsi2"][pos]
    s10 = ind["sma10"][pos]
    s200 = ind["sma200"][pos]
    if nan(r, r2, s10, s200):
        return None
    # Long: price in uptrend (sma10 >= sma200) and fast RSI significantly below slow RSI
    if s10 >= s200 and r2 < r - 20.0:
        return "long"
    # Short: price in downtrend (sma10 < sma200) and fast RSI significantly above slow RSI
    if s10 < s200 and r2 > r + 20.0:
        return "short"
    return None
