#!/usr/bin/env python3
"""vr_rsi_robot_multi_timeframe -- RSI multi-timeframe: H1 primary + D1 HTF confirmation. VR RSI Robot.

Long when RSI > 20 (exiting oversold) and RSI rising on H1, AND same condition on D1 (via htf).
Short when RSI < 80 (exiting overbought) and RSI falling on H1, AND same on D1.
HTF (higher timeframe) RSI read from htf dict when available; graceful fallback on primary only.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "vr_rsi_robot_multi_timeframe",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "1h",
    "indicators": "rsi (H1 primary + D1 via htf)",
    "long": "rsi > 20 AND rsi rising (H1) AND htf rsi > 20 AND htf rsi rising (D1)",
    "short": "rsi < 80 AND rsi falling (H1) AND htf rsi < 80 AND htf rsi falling (D1)",
    "desc": "Multi-timeframe RSI exit from OB/OS: H1 impulse confirmed by D1 direction",
    "source": "web:https://www.mql5.com/en/code/mt4/experts/best",
}


def signal(ind, pos, htf=None):
    """H1 RSI recovering from OB/OS confirmed by D1 HTF RSI direction."""
    r = ind["rsi"][pos]
    r1 = ind["rsi"][pos - 1]
    if nan(r, r1):
        return None
    # H1 conditions
    h1_long = r > 20 and r > r1
    h1_short = r < 80 and r < r1
    # D1 confirmation via htf if available
    if htf is not None:
        htf_rsi = htf.get("bias")  # use bias as HTF trend proxy (1=up, -1=down)
        if htf_rsi is not None:
            htf_pos = htf_rsi[pos] if hasattr(htf_rsi, "__len__") else htf_rsi
            if not nan(htf_pos):
                if h1_long and htf_pos > 0:
                    return "long"
                if h1_short and htf_pos < 0:
                    return "short"
                return None
    # Fallback: H1 only
    if h1_long:
        return "long"
    if h1_short:
        return "short"
    return None
