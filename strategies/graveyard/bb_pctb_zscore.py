#!/usr/bin/env python3
"""bb_pctb_zscore -- Bollinger %B / Z-score reversion at 2-sigma extremes.. Ported from sister-lab catalog (https://www.tradingview.com/script/XkjJJIJ2-Mean-Reversion-BB-Z-Score-RSI-EMA200/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "bb_pctb_zscore", "cadences": ['day'], "exit": {'sl_atr': 1.5, 'tp_atr': 2.0, 'trail': True, 'time_stop_h': 24, 'exit_opposite': False}, "asset_classes": ALL_CLASSES,
    "style": "mean_reversion", "tf": "15m-4h", "indicators": "Bollinger(20,2) %B / Z-score",
    "long": "Close below lower band (%B<0, z<=-2)", "short": "Close above upper band (%B>1, z>=+2)", "desc": "Bollinger %B / Z-score reversion at 2-sigma extremes.", "source": "sister-lab catalog: https://www.tradingview.com/script/XkjJJIJ2-Mean-Reversion-BB-Z-Score-RSI-EMA200/",
}


def signal(I, i, htf):
    pb, c, mid = I["bb_pctb"][i], I["close"][i], I["bb_mid"][i]
    if _nan(pb, c, mid):
        return None
    if pb < 0.0:            # close below the lower band (z <= -2)
        return "long"
    if pb > 1.0:
        return "short"
    return None
