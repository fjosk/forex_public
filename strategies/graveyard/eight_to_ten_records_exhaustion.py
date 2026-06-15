#!/usr/bin/env python3
"""eight_to_ten_records_exhaustion -- 8-10 consecutive new records exhaustion reversal. j_person_a_complete_guide_to_technical_trading_tac.

After 8+ consecutive new lows, a bar with close above open (bullish reversal) -> long.
After 8+ consecutive new highs, a bar with close below open (bearish reversal) -> short.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "eight_to_ten_records_exhaustion",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "4h",
    "indicators": "dn_record_count,up_record_count,close,open",
    "long": "dn_record_count >= 8 AND current bar is bullish (close > open)",
    "short": "up_record_count >= 8 AND current bar is bearish (close < open)",
    "desc": "8-to-10 consecutive new records exhaustion: count of new highs/lows + bullish/bearish reversal bar",
    "source": "j_person_a_complete_guide_to_technical_trading_tac, Ch4 pp.57-59",
}


def signal(ind, pos, htf=None):
    """Exhaustion reversal after 8+ consecutive new highs or lows."""
    if pos < 1:
        return None
    dn_cnt = ind["dn_record_count"][pos]
    up_cnt = ind["up_record_count"][pos]
    c = ind["close"][pos]
    o = ind["open"][pos]
    if nan(dn_cnt, up_cnt, c, o):
        return None
    if dn_cnt >= 8 and c > o:
        return "long"
    if up_cnt >= 8 and c < o:
        return "short"
    return None
