#!/usr/bin/env python3
"""roc_std_breakout -- Volatility-adaptive ROC breakout (self-normalizing threshold).. Ported from sister-lab catalog (https://thesecretmindset.com/rate-of-change/).

Self-contained (sister-lab catalog helper inlined). Volume-free, engine.precompute indicators only.
"""
import numpy as np
from strategies._common import nan, ALL_CLASSES

META = {
    "id": "roc_std_breakout", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'time_stop_h': 36, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "breakout", "tf": "1h-1d", "indicators": "ROC(9) + its 30-bar mean/std, EMA(50)",
    "long": "ROC > mean+1std of its recent distribution, close>EMA50", "short": "ROC < mean-1std, close<EMA50", "desc": "Volatility-adaptive ROC breakout (self-normalizing threshold).", "source": "sister-lab catalog: https://thesecretmindset.com/rate-of-change/",
}


def signal(I, i, htf=None):
    roc = I["roc"]
    if i < 31 or nan(roc[i]):
        return None
    win = roc[i-30:i]
    win = win[~np.isnan(win)]
    if len(win) < 20:
        return None
    mu = win.mean(); sd = win.std()
    if sd <= 0 or nan(I["ema50"][i], I["close"][i]):
        return None
    if roc[i] > mu + sd and I["close"][i] > I["ema50"][i]:
        return "long"
    if roc[i] < mu - sd and I["close"][i] < I["ema50"][i]:
        return "short"
    return None
