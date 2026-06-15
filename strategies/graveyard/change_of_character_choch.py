#!/usr/bin/env python3
"""change_of_character_choch -- CHoCH trend reversal: close breaks counter-trend fractal.

Uses frac_up_px / frac_dn_px and a simple structure-state proxy to distinguish
CHoCH (reversal) from BOS (continuation).

CHoCH long (bear->bull flip): in a downtrend (hh_n large = no recent new HH),
  close breaks above the most recent frac_up_px (breaks the last lower high).
CHoCH short (bull->bear flip): in an uptrend (ll_n large = no recent new LL),
  close breaks below the most recent frac_dn_px (breaks the last higher low).

hh_n/ll_n track the bar-count since last HH/LL; a large value signals a weakening trend.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "change_of_character_choch",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "15m, 1h, 4h",
    "indicators": "close, frac_up_px, frac_dn_px, hh_n, ll_n, atr",
    "long": "downtrend context (hh_n large), close breaks above last frac_up_px (CHoCH bull)",
    "short": "uptrend context (ll_n large), close breaks below last frac_dn_px (CHoCH bear)",
    "desc": "Change of Character (CHoCH) trend reversal: counter-trend fractal break",
    "source": "web:https://innercircletrader.net/tutorials/break-of-structure-vs-change-of-character/",
}

_TREND_BARS = 10   # hh_n / ll_n threshold: at least this many bars without a new HH/LL


def signal(ind, pos, htf=None):
    """CHoCH trend reversal signal."""
    c = ind["close"][pos]
    c1 = ind["close"][pos - 1]
    fup = ind["frac_up_px"][pos - 1]
    fdn = ind["frac_dn_px"][pos - 1]
    hh = ind["hh_n"][pos]    # bars since last HH; large = downtrend / no new highs
    ll = ind["ll_n"][pos]    # bars since last LL; large = uptrend / no new lows
    if nan(c, c1, fup, fdn, hh, ll):
        return None
    # CHoCH long: in a downtrend (hh_n >= threshold), close breaks above last lower-high
    if hh >= _TREND_BARS and c > fup and c1 <= fup:
        return "long"
    # CHoCH short: in an uptrend (ll_n >= threshold), close breaks below last higher-low
    if ll >= _TREND_BARS and c < fdn and c1 >= fdn:
        return "short"
    return None
