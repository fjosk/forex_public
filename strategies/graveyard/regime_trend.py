#!/usr/bin/env python3
"""regime_trend -- Hurst-regime-gated EMA50 trend-slope flip.. Ported from sister-lab catalog (https://www.tradingview.com/script/zagpmoKH-Volatility-Regime-Classifier-QuantRegime/).

Volume-free + uses only engine.precompute indicators. Signal body copied verbatim from the sister-lab
research catalog (same indicator framework); the def was renamed to signal(). Exit carried as-is.
"""
from strategies._common import _nan, _xup, _xdn, ALL_CLASSES

META = {
    "id": "regime_trend", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "trend", "tf": "1h-4h", "indicators": "Hurst(100), EMA(50)",
    "long": "Hurst>0.55 and EMA50 slope flips up", "short": "Hurst>0.55 and EMA50 slope flips down", "desc": "Hurst-regime-gated EMA50 trend-slope flip.", "source": "sister-lab catalog: https://www.tradingview.com/script/zagpmoKH-Volatility-Regime-Classifier-QuantRegime/",
}


def signal(I, i, htf):
    """Hurst-gated trend: only act when Hurst>0.55 (persistent/trending regime), then follow a
    fresh EMA50 slope flip. The regime gate is the new element (EMA-slope core is generic)."""
    H, e, e1, e2 = I["hurst"][i], I["ema50"][i], I["ema50"][i-1], I["ema50"][i-2]
    if _nan(H, e, e1, e2) or H <= 0.55:
        return None
    if e > e1 and e1 <= e2:
        return "long"
    if e < e1 and e1 >= e2:
        return "short"
    return None
