#!/usr/bin/env python3
"""tsmom_slow -- Time-series momentum (slow): sign of trailing 252-bar return, Moskowitz/Ooi/Pedersen 2012.. Ported from sister-lab catalog (http://docs.lhpedersen.com/TimeSeriesMomentum.pdf).

Self-contained (sister-lab catalog helper inlined). Volume-free, engine.precompute indicators only.
"""
from strategies._common import nan, ALL_CLASSES

META = {
    "id": "tsmom_slow", "cadences": ['day', 'swing'], "exit": {'sl_atr': 2.0, 'tp_atr': 4.0, 'trail': True, 'chand_mult': 3.0, 'trail_activate_r': 1.0, 'time_stop_h': 48, 'exit_opposite': True}, "asset_classes": ALL_CLASSES,
    "style": "momentum", "tf": "4h-1d", "indicators": "252-bar return sign",
    "long": "252-bar return flips positive", "short": "252-bar return flips negative", "desc": "Time-series momentum (slow): sign of trailing 252-bar return, Moskowitz/Ooi/Pedersen 2012.", "source": "sister-lab catalog: http://docs.lhpedersen.com/TimeSeriesMomentum.pdf",
}


def _tsmom(I, i, n):
    if i <= n:
        return None
    c, cn, c1, cn1 = I["close"][i], I["close"][i-n], I["close"][i-1], I["close"][i-1-n]
    if nan(c, cn, c1, cn1) or cn <= 0 or cn1 <= 0:
        return None
    r, r1 = c / cn - 1.0, c1 / cn1 - 1.0
    if r > 0 and r1 <= 0:
        return "long"
    if r < 0 and r1 >= 0:
        return "short"
    return None


def signal(I, i, htf=None):
    return _tsmom(I, i, 252)
