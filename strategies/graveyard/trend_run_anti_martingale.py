#!/usr/bin/env python3
"""trend_run_anti_martingale -- Anti-Martingale: pyramid winners in trend direction after pullback. trading_systems_and_methods_kaufman_perry_j_kaufma.

Long-term trend: close > SMA200 (up).
Entry: trend up AND close just turned DOWN (down-close after a prior up-close run).
The anti-Martingale sizing (double after each profitable day) is outside the signal contract;
the signal captures the same pullback-entry trigger.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "trend_run_anti_martingale",
    "cadences": ["day"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "close,sma200",
    "long": "Trend up (SMA200) AND prior close was up-bar (run started) AND current close is down (entry after first pullback)",
    "short": "Trend down AND prior close was down-bar AND current close is up",
    "desc": "Anti-Martingale run: enter on pullback after a profitable run, pyramid in trend direction",
    "source": "trading_systems_and_methods_kaufman_perry_j_kaufma Ch22 p571",
}


def signal(ind, pos, htf=None):
    """Anti-Martingale entry: first pullback day after a prior profitable close in trend."""
    if pos < 2:
        return None
    c  = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    c2 = ind["close"][pos - 2]
    s  = ind["sma200"][pos]
    if nan(c, c1, c2, s):
        return None
    trend_up = c > s
    trend_dn = c < s
    # Long: trend up, prior bar was an up-bar (profitable), current is a pullback
    if trend_up and c1 > c2 and c < c1:
        return "long"
    # Short: trend down, prior bar was a down-bar, current is a bounce
    if trend_dn and c1 < c2 and c > c1:
        return "short"
    return None
