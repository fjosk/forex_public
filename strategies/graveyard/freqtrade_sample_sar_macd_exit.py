#!/usr/bin/env python3
"""freqtrade_sample_sar_macd_exit -- RSI/stoch oversold + BB lower entry; SAR or Fisher exit. freqtrade Strategy002."""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "freqtrade_sample_sar_macd_exit",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean-reversion",
    "tf": "1h",
    "indicators": "psar, psar_dir, rsi, stoch_k, bb_lo, fisher, fisher_trig",
    "long": "rsi<30 AND stoch_k<20 AND close<bb_lo; long-only oversold entry",
    "short": "not used (long-only strategy)",
    "desc": "RSI/stoch oversold + BB lower touch entry; PSAR or Fisher exit signal",
    "source": "freqtrade/freqtrade-strategies Strategy002.py",
}


def signal(ind, pos, htf=None):
    """Oversold multi-oscillator entry below lower BB; long-only."""
    c = ind["close"][pos]
    rsi = ind["rsi"][pos]
    stk = ind["stoch_k"][pos]
    bb_lo = ind["bb_lo"][pos]
    psar_d = ind["psar_dir"][pos]
    fsh = ind["fisher"][pos]
    if nan(c, rsi, stk, bb_lo, psar_d, fsh):
        return None
    # Long entry: all three confirm oversold below lower BB
    if rsi < 30 and stk < 20 and c < bb_lo and psar_d > 0:
        return "long"
    # SAR-based exit flip: if PSAR is above price, bearish reversal -- no new long
    # Fisher normalized > 0.3 also signals exit; use it as a short proxy when overbought
    if fsh > 0.3 and psar_d < 0 and c > bb_lo:
        return "short"
    return None
