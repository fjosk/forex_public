#!/usr/bin/env python3
"""octobot_macd_pattern -- OctoBot MACD Histogram Pattern Evaluator. Drakkar-Software/OctoBot.

W-shape (double bottom) in MACD histogram = bullish. M-shape (double top) = bearish.
V-shape: sharp single-bar bounce. Lambda: sharp single-bar drop.
Pattern detection over a 4-bar rolling window on macd_hist.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "octobot_macd_pattern",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd_hist",
    "long": "W-pattern or V-pattern in MACD histogram (bullish reversal shape)",
    "short": "M-pattern or Lambda (inverted-V) in MACD histogram (bearish reversal shape)",
    "desc": "OctoBot MACD histogram shape evaluator: W/V = long, M/Lambda = short",
    "source": "web:https://raw.githubusercontent.com/Drakkar-Software/OctoBot-Tentacles/master/Evaluator/TA/momentum_evaluator/momentum.py",
}


def signal(ind, pos, htf=None):
    """MACD histogram W/V/M/Lambda pattern recognition."""
    h0 = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    h2 = ind["macd_hist"][pos - 2]
    h3 = ind["macd_hist"][pos - 3]
    if nan(h0, h1, h2, h3):
        return None
    # W-pattern: h3 < h2 > h1 < h0 (double bottom with recovery)
    w_pattern = h3 < h2 and h2 > h1 and h1 < h0
    # V-pattern: sharp single bounce -- h1 < h2 and h1 < h0 and h0 rising strongly
    v_pattern = h1 < h2 and h1 < h0 and (h0 - h1) > abs(h2 - h1)
    # M-pattern: h3 > h2 < h1 > h0 (double top with rollover)
    m_pattern = h3 > h2 and h2 < h1 and h1 > h0
    # Lambda (inverted-V): h1 > h2 and h1 > h0, sharp drop
    lambda_pattern = h1 > h2 and h1 > h0 and (h1 - h0) > abs(h2 - h1)
    if w_pattern or v_pattern:
        return "long"
    if m_pattern or lambda_pattern:
        return "short"
    return None
