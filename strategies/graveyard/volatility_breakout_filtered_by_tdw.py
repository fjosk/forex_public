#!/usr/bin/env python3
"""volatility_breakout_filtered_by_tdw -- Daily range breakout gated by day-of-week using
the S&P 500 optimal day set: buy Mon/Tue/Wed, sell Thu/Fri.
long_term_secrets_to_short_term_trading Ch.4 Figures 4.2-4.18.

Companion to trade_day_of_week_tdw_volatility_breakout which uses bond-market day sets.
This module uses the S&P-optimized day sets instead (different market-specific finding).
Breakout trigger: close > prev_dhh (long) or close < prev_dll (short).
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "volatility_breakout_filtered_by_tdw",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dow,close,prev_dhh,prev_dll",
    "long": "close > prior-day high AND today is Mon, Tue, or Wed (S&P best buy days)",
    "short": "close < prior-day low AND today is Thu or Fri (S&P best sell days)",
    "desc": "S&P-variant TDW volatility breakout: daily range breaks on historically optimal buy/sell weekdays",
    "source": "long_term_secrets_to_short_term_trading Ch.4 pp.62-70",
}

# Python weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
_BUY_DAYS  = {0, 1, 2}   # Monday, Tuesday, Wednesday
_SELL_DAYS = {3, 4}       # Thursday, Friday


def signal(ind, pos, htf=None):
    """Range breakout gated by S&P-optimal weekday sets."""
    if pos < 1:
        return None
    dw   = ind["dow"][pos]
    c    = ind["close"][pos]
    phh  = ind["prev_dhh"][pos]
    pll  = ind["prev_dll"][pos]
    if nan(dw, c, phh, pll):
        return None
    wd = int(dw)
    if wd in _BUY_DAYS and c > phh:
        return "long"
    if wd in _SELL_DAYS and c < pll:
        return "short"
    return None
