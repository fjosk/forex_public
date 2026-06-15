#!/usr/bin/env python3
"""hidden_smash_day_reversal -- Hidden smash day: up/down close in extreme 25% of range. long_term_secrets_to_short_term_trading.

Buy setup: up-close day but close in bottom 25% of range and below open. Trigger: next bar breaks above setup bar high.
Sell setup: down-close day but close in top 25% of range and above open. Trigger: next bar breaks below setup bar low.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "hidden_smash_day_reversal",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "1h-4h",
    "indicators": "open,high,low,close",
    "long": "prior bar: up-close AND close <= low+0.25*range AND close<open; current bar: high > prior bar high",
    "short": "prior bar: down-close AND close >= high-0.25*range AND close>open; current bar: low < prior bar low",
    "desc": "Hidden smash day reversal: misleading bar (up close but near low) triggers breakout next bar",
    "source": "long_term_secrets_to_short_term_trading, Ch7 Figs7.10-7.11 pp.102-104",
}


def signal(ind, pos, htf=None):
    """Hidden smash day reversal: detect the setup on prior bar, trigger on current bar extreme."""
    if pos < 2:
        return None
    # Current bar
    h = ind["high"][pos]
    l = ind["low"][pos]
    # Setup bar (pos - 1)
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    l1 = ind["low"][pos - 1]
    c2 = ind["close"][pos - 2]
    if nan(h, l, c1, o1, h1, l1, c2):
        return None
    rng1 = h1 - l1
    if rng1 <= 0:
        return None
    # Buy setup: up close (c1 > c2) but close in lower 25% of bar range AND below open
    buy_setup = c1 > c2 and c1 <= l1 + 0.25 * rng1 and c1 < o1
    # Sell setup: down close (c1 < c2) but close in upper 25% of bar range AND above open
    sell_setup = c1 < c2 and c1 >= h1 - 0.25 * rng1 and c1 > o1
    if buy_setup and h > h1:
        return "long"
    if sell_setup and l < l1:
        return "short"
    return None
