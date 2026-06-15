#!/usr/bin/env python3
"""pivot_point_worksheet_oversold_support_buy -- Daily pivot S2 bounce with stochastic/RSI oversold filter. j_person_a_complete_guide_to_technical_trading_tac.

5-day trend down + oversold (stoch and/or RSI) -> long at S2; mirror at R2 for shorts.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "pivot_point_worksheet_oversold_support_buy",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "mean_revert",
    "tf": "1h-4h",
    "indicators": "piv_s2,piv_r2,close,stoch_k,rsi,sma10",
    "long": "close <= piv_s2 AND stoch_k<25 AND rsi<40 AND sma10 slope down (close<sma10 at pos-4)",
    "short": "close >= piv_r2 AND stoch_k>75 AND rsi>60 AND sma10 slope up (close>sma10 at pos-4)",
    "desc": "Daily pivot S2/R2 bounce with stochastic+RSI oversold/overbought filter and 5-bar trend gate",
    "source": "j_person_a_complete_guide_to_technical_trading_tac, Ch11 Fig11.1 pp.194-196",
}


def signal(ind, pos, htf=None):
    """Pivot S2/R2 bounce with oscillator oversold/overbought filter."""
    if pos < 5:
        return None
    c = ind["close"][pos]
    s2 = ind["piv_s2"][pos]
    r2 = ind["piv_r2"][pos]
    sk = ind["stoch_k"][pos]
    rs = ind["rsi"][pos]
    ma = ind["sma10"][pos]
    ma_old = ind["sma10"][pos - 4]
    if nan(c, s2, r2, sk, rs, ma, ma_old):
        return None
    # 5-bar trend proxy: sma10 direction
    trend_down = ma < ma_old
    trend_up = ma > ma_old
    oversold = sk < 25 and rs < 40
    overbought = sk > 75 and rs > 60
    if c <= s2 and oversold and trend_down:
        return "long"
    if c >= r2 and overbought and trend_up:
        return "short"
    return None
