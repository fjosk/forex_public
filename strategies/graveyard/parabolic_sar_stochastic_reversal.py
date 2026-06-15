#!/usr/bin/env python3
"""parabolic_sar_stochastic_reversal -- Parabolic SAR + Stochastic Reversal EA. MQL4 SAR Stoch."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_stochastic_reversal",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "psar_dir, stoch_k",
    "long": "psar_dir == 1 (SAR below price = bullish) AND stoch_k rising",
    "short": "psar_dir == -1 (SAR above price = bearish) AND stoch_k falling",
    "desc": "PSAR trend flip + stochastic momentum direction for entry confirmation",
    "source": "kb.mycoder.pro/apibridge/parabolic-sarstocastic-strategy-for-mt4/",
}


def signal(ind, pos, htf=None):
    """PSAR direction + stochastic rising/falling for trend-entry confirmation."""
    pd = ind["psar_dir"][pos]
    sk = ind["stoch_k"][pos]
    sk1 = ind["stoch_k"][pos - 1]
    if nan(pd, sk, sk1):
        return None
    if pd == 1 and sk > sk1:
        return "long"
    if pd == -1 and sk < sk1:
        return "short"
    return None
