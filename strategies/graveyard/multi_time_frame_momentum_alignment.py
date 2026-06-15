#!/usr/bin/env python3
"""multi_time_frame_momentum_alignment -- MTF momentum alignment: entry-TF stochastic extreme turning AND HTF stochastic agreeing. Currency Trading for Dummies.

tier1 multi-timeframe. Price/OHLC only.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "multi_time_frame_momentum_alignment",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h-4h",
    "indicators": "stoch_k, stoch_d",
    "long": "Stoch_K < 20 AND ticking up AND HTF stoch_k < 50 (both timeframes oversold-aligned)",
    "short": "Stoch_K > 80 AND ticking down AND HTF stoch_k > 50 (both timeframes overbought-aligned)",
    "desc": "MTF stochastic alignment: entry-TF extreme turning in direction confirmed by HTF oversold/overbought",
    "source": "Currency Trading for Dummies, Ch.12 Looking at momentum in multiple time frames",
}


def signal(ind, pos, htf=None):
    """Entry-TF stochastic extreme + HTF alignment."""
    if pos < 1:
        return None
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(sk, sk1):
        return None
    # HTF stochastic level
    htf_sk = None
    if htf is not None:
        hsk = htf.get("stoch_k")
        if hsk is not None and len(hsk) >= 1:
            v = hsk[-1]
            if v == v:  # not NaN
                htf_sk = v
    # Long: entry-TF oversold turning up, HTF also below midline
    if sk < 20 and sk > sk1:
        if htf_sk is None or htf_sk < 50:
            return "long"
    # Short: entry-TF overbought turning down, HTF also above midline
    if sk > 80 and sk < sk1:
        if htf_sk is None or htf_sk > 50:
            return "short"
    return None
