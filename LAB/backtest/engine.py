#!/usr/bin/env python3
"""
Generalised per-pair backtest engine for the FOREX/backtest strategy library (ported from sister-lab).

ONE engine, pluggable strategy. ENTRY is any signal function; EXIT is per-strategy.

TIMEFRAME CADENCE. The engine runs a strategy on a chosen entry timeframe, evaluates exits on a
finer sub-bar timeframe, and reads one higher timeframe for trend bias. Three named cadences:
  - "day"   : entry 1h,  exit 15m, htf 4h   (DEFAULT)
  - "swing" : entry 4h,  exit 1h,  htf 1d
  - "scalp" : entry 15m, exit 1m,  htf 1h
Intrabar straddles resolve PESSIMISTICALLY (a bar touching both stop and target books the STOP).

EXECUTION = the OSTIUM cost model (costs.py), wired 2026-06-06. `run(..., cost_model=)` defaults to
costs.GATE (Ostium realistic-worst); each cost hits its own axis (see GAUNTLET.md):
  - Open fee 0.03% (3 bps) on open notional; closing fee 0%.
  - Round-trip SPREAD/impact per asset class (major/cross/commodity/exotic), charged once per trade.
  - Adverse-fill SLIPPAGE on market exits (stop/time-stop): stop*(1 - dir*slip), where slip is
    VOLATILITY-SCALED per bar (costs.slip_fraction_array: floor + 5% of the bar's ATR-in-bps, capped;
    GAUNTLET.md rule 3 -- slippage is the real killer and scales with volatility). Take-profit fills
    at the trigger (resting, no slip). Entry takes the same per-bar slippage.
  - ROLLOVER (carry) is per ASSET CLASS (costs.holding_per_day): majors cheap, commodities/exotics
    dearer -- realistic per class, not one worst-uniform number.
  - GAP-THROUGH-STOP: if a sub-bar OPENS beyond the stop (Ostium RWA market-reopen gap), the stop
    fills at the gap open, not at its level.
  - Per-day ROLLOVER (carry) over the holding window; FUNDING is ~0 for FX so it is not modelled.
  - $0.10 oracle fee per close (fixed $).
  - Sizing: risk 2% of active equity / stop distance; notional capped at equity * LEVERAGE * 0.80
    (LEVERAGE=15 is a CONSERVATIVE cap carried from sister-lab; Ostium allows more per-pair -- revisit
    when tuning); min notional $10; min stop 0.4%.
  - Per-pair backtest-start trim: no simulation before the pair's safe year
    (shared/instruments.backtest_start_year), excluding sparse 2000-2003 HistData.
  - Liquidation (equity <= 0): refund to $1000 and continue (research mode).

SL/TP RULE (per the operator): the engine NEVER imposes its own SL/TP over a strategy's. Each strategy
supplies its own exit config (sl_atr, tp_atr, trail, time stop, exit-on-opposite) via the catalog;
the engine merges it over DEFAULT_EXIT (the fallback for a strategy that specifies none).

A strategy is a callable: strategy(I, i, htf) -> 'long' | 'short' | None
  I   = dict of precomputed entry-tf indicator numpy arrays (read I['x'][i], [i-1] ...)
  i   = current entry-tf bar index
  htf = dict of higher-tf-derived arrays mapped onto each entry-tf bar

Reads the LAB unified parquet (one series per pair, FOREX schema). NOTE: FX/commodity volume is
always 0 in this data, so VOLUME-BASED strategies must not be used (a catalog/authoring rule).
"""

import numpy as np
import pandas as pd

import indicators as ind   # its bootstrap also puts the FOREX root on sys.path (for `from shared import ...`)
import indicators_books as _indb   # book-extracted candidate indicators (Stage 2)
import costs as _costs             # the Ostium cost model (single source for fees/spread/rollover)
from shared import exits as _exits
from shared import instruments as _instr   # per-pair asset class + backtest-start year

_EPOCH = pd.Timestamp("1970-01-01", tz="UTC")


def _year_ms(year):
    """Epoch milliseconds for Jan 1 00:00 UTC of `year` (per-pair backtest-start trim)."""
    return int((pd.Timestamp(year=int(year), month=1, day=1, tz="UTC") - _EPOCH) // pd.Timedelta("1ms"))

from paths import UNIFIED   # single source (paths.py, derived from __file__) -- do not re-hardcode

# Bar duration in epoch-ms for every interval the unified parquet ships.
TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000,
         "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}

# Named cadences: (entry_tf, exit_tf, htf_tf). Default "day" == original engine.
CADENCES = {
    "day":   ("1h", "15m", "4h"),
    "swing": ("4h", "1h", "1d"),
    "scalp": ("15m", "1m", "1h"),
}

# Account/sizing defaults. COSTS come from the Ostium cost model (costs.py), NOT from here.
BANKROLL = 1000.0
RISK_PCT = 0.02
LEVERAGE = 15                # CONSERVATIVE notional cap (Ostium allows more per-pair -- FX 200x /
                            # commodity 100x); revisit per-pair when tuning. Not a fee.
MIN_STOP_PCT = 0.004
MAX_NOTIONAL_PCT = 0.80
MIN_NOTIONAL = 10.0

DEFAULT_EXIT = {"sl_atr": 2.0, "tp_atr": 4.0, "trail": True, "chand_mult": 3.0,
                "trail_activate_r": 1.0, "time_stop_h": 48, "exit_opposite": False}


def _load(coin, tf):
    import os
    p = f"{UNIFIED}/{coin}/{coin}-{tf}.parquet"
    if not os.path.exists(p):
        return None
    df = pd.read_parquet(p, columns=["open_time", "open", "high", "low", "close", "volume", "quote_volume"])
    return df.sort_values("open_time").reset_index(drop=True)


# --- carry ----------------------------------------------------------------
# Ostium charges a ROLLOVER (carry) by TIME, applied in run() via costs.py per-asset-class
# (costs.VenueProfile.holding_per_day). FUNDING is ~0 for our FX/commodity universe (the crypto skew
# mechanism), so it is not modelled. The sister-lab Binance-funding path was removed here on the
# Stage-2 cost-wiring (2026-06-06) -- carry is now costs.OSTIUM rollover, not Binance funding.


def _htf_map(df_entry, df_htf, entry_ms, htf_ms):
    """Map higher-tf-derived features onto each entry bar (last CLOSED htf bar):
    trend bias (EMA20>EMA50), EMA50 slope sign, ADX. Alignment uses each bar's
    close time (open_time + bar_duration) so no lookahead leaks across the seam."""
    e20 = ind.ema(df_htf["close"], 20); e50 = ind.ema(df_htf["close"], 50)
    bias = np.where(e20.notna() & e50.notna(), np.where(e20 > e50, 1.0, -1.0), 0.0)
    slope = np.sign((e50 - e50.shift(3)).fillna(0)).to_numpy()
    adxh = ind.adx(df_htf, 14).to_numpy()
    right = pd.DataFrame({"ct": df_htf["open_time"].to_numpy() + htf_ms,
                          "bias": bias, "slope": slope, "adx4": adxh}).sort_values("ct")
    left = pd.DataFrame({"ct": df_entry["open_time"].to_numpy() + entry_ms, "_i": range(len(df_entry))})
    m = pd.merge_asof(left.sort_values("ct"), right, on="ct", direction="backward").sort_values("_i")
    return {"bias": m["bias"].fillna(0).to_numpy(),
            "slope": m["slope"].fillna(0).to_numpy(),
            "adx4": m["adx4"].fillna(0).to_numpy()}


_BOOK_INDICATORS = ['abschg', 'accel', 'asi', 'asi_hsp', 'asi_lsp', 'body_mom', 'buy_swing', 'bwmfi', 'close_loc_sma', 'close_sma5', 'demand_osc', 'dm_buy_countdown', 'dm_proj_hi', 'dn_record_count', 'dow', 'drf', 'eff_ratio', 'ema_hi13', 'ema_lo13', 'er10', 'ewo', 'filt_pct', 'force2', 'fosc', 'frac_dn_bar_high', 'frac_up_bar_low', 'hh_n', 'll_n', 'lo_shadow_sma', 'lr_slope_price', 'lr_slope_rsi', 'lrs20', 'mah3', 'mal3', 'mdi', 'mv', 'obtr', 'obtr_ema', 'pct_band_lo', 'pct_band_up', 'pvt', 'pvt_sma', 'rng5', 'rng50', 'rng_sma20', 'roc_sd', 'round_step', 'run_ext', 'sell_swing', 'sma10', 'sma100', 'sma200', 'sma3_high', 'sma3_low', 'sma_high21', 'sma_low21', 'sroc', 'strength_osc', 'tdm', 'thermo', 'thermo_ema', 'tsi', 'tsi_sig', 'udvo', 'udvo_dn', 'udvo_up', 'up_record_count', 'up_shadow_sma', 'vavg', 'vci', 'vci_sma', 'vidya', 'vol_sma5', 'vsd', 'yr_high', 'yr_low']


def precompute(df1):
    """Superset of entry-tf indicators the strategy library may read."""
    close = df1["close"]
    I = {"close": close.to_numpy(), "high": df1["high"].to_numpy(),
         "low": df1["low"].to_numpy(), "volume": df1["volume"].to_numpy()}
    I["atr"] = ind.atr(df1, 14).to_numpy()
    I["atr_pct"] = np.divide(I["atr"], I["close"], out=np.zeros_like(I["atr"]), where=I["close"] > 0)
    I["rsi"] = ind.rsi(close, 14).to_numpy()
    I["adx"] = ind.adx(df1, 14).to_numpy()
    for p in (5, 8, 9, 13, 20, 21, 50, 200):
        I[f"ema{p}"] = ind.ema(close, p).to_numpy()
    I["sma20"] = ind.sma(close, 20).to_numpy()
    I["sma50"] = ind.sma(close, 50).to_numpy()
    ml, ms, mh = ind.macd(close)
    I["macd"], I["macd_sig"], I["macd_hist"] = ml.to_numpy(), ms.to_numpy(), mh.to_numpy()
    k, d = ind.stochastic(df1, 14, 3, 3)
    I["stoch_k"], I["stoch_d"] = k.to_numpy(), d.to_numpy()
    st_line, st_dir = ind.supertrend(df1, 10, 3.0)
    I["st_line"], I["st_dir"] = st_line.to_numpy(), st_dir.to_numpy()
    ps, pt = ind.psar(df1)
    I["psar"], I["psar_dir"] = ps.to_numpy(), pt.to_numpy()
    ten, kij, sa, sb = ind.ichimoku(df1)
    I["ich_ten"], I["ich_kij"] = ten.to_numpy(), kij.to_numpy()
    I["ich_a"], I["ich_b"] = sa.to_numpy(), sb.to_numpy()
    jaw, teeth, lips = ind.alligator(df1)
    I["al_jaw"], I["al_teeth"], I["al_lips"] = jaw.to_numpy(), teeth.to_numpy(), lips.to_numpy()
    I["sma200_dir"] = ind.sma_trend_direction(close, 200, 5).to_numpy()
    # Extended indicators for the research catalog.
    mid, bb_lo, bb_up = ind.bollinger(close, 20, 2.0)
    I["bb_mid"], I["bb_lo"], I["bb_up"] = mid.to_numpy(), bb_lo.to_numpy(), bb_up.to_numpy()
    bw = (bb_up - bb_lo)
    I["bb_pctb"] = np.divide((close.to_numpy() - bb_lo.to_numpy()), bw.to_numpy(),
                             out=np.full(len(close), np.nan), where=bw.to_numpy() > 0)
    I["bb_width"] = np.divide(bw.to_numpy(), mid.to_numpy(),
                              out=np.full(len(close), np.nan), where=mid.to_numpy() > 0)
    kc_mid, kc_lo, kc_up = ind.keltner(df1, 20, 2.0, 10)
    I["kc_lo"], I["kc_up"], I["kc_mid"] = kc_lo.to_numpy(), kc_up.to_numpy(), kc_mid.to_numpy()
    dc_up, dc_lo = ind.donchian(df1, 20)
    I["dc_up"], I["dc_lo"] = dc_up.to_numpy(), dc_lo.to_numpy()
    I["cci"] = ind.cci(df1, 20).to_numpy()
    I["willr"] = ind.williams_r(df1, 14).to_numpy()
    I["mfi"] = ind.mfi(df1, 14).to_numpy()
    I["rsi2"] = ind.rsi(close, 2).to_numpy()
    srk, srd = ind.stoch_rsi(close, 14, 14, 3, 3)
    I["srsi_k"], I["srsi_d"] = srk.to_numpy(), srd.to_numpy()
    I["roc"] = ind.roc(close, 9).to_numpy()
    ha_o, ha_h, ha_l, ha_c = ind.heikin_ashi(df1)
    I["ha_open"], I["ha_close"] = ha_o.to_numpy(), ha_c.to_numpy()
    dip, dim = ind.directional_indicators(df1, 14)
    I["di_plus"], I["di_minus"] = dip.to_numpy(), dim.to_numpy()
    I["vwap"] = ind.vwap_session(df1).to_numpy()
    d_open, p_hh, p_ll, p_hc, p_lc = ind.utc_day_features(df1)
    I["day_open"], I["prev_dhh"], I["prev_dll"] = d_open, p_hh, p_ll
    I["prev_dhc"], I["prev_dlc"] = p_hc, p_lc
    I["hour_utc"] = ((df1["open_time"].to_numpy() // 3_600_000) % 24).astype(float)
    # Day-of-week (0=Mon .. 6=Sun, UTC). The Unix epoch 1970-01-01 was a Thursday (=3), so adding 4
    # to the epoch-day index anchors Monday=0. Additive + 0-diff for existing strategies (only the
    # session/time-of-day class reads it).
    I["dow"] = (((df1["open_time"].to_numpy() // 86_400_000) + 4) % 7).astype(float)
    I["vol_sma20"] = ind.avg_volume(df1, 20).to_numpy()
    # --- round-2 research indicators (catalog2) ---
    vip, vim = ind.vortex(df1, 14); I["vi_plus"], I["vi_minus"] = vip.to_numpy(), vim.to_numpy()
    au, ad, ao_ = ind.aroon(df1, 25); I["aroon_up"], I["aroon_dn"], I["aroon_osc"] = au.to_numpy(), ad.to_numpy(), ao_.to_numpy()
    I["cmo"] = ind.cmo(close, 20).to_numpy()
    tx, txs = ind.trix(close); I["trix"], I["trix_sig"] = tx.to_numpy(), txs.to_numpy()
    I["ao"] = ind.awesome_oscillator(df1).to_numpy()
    I["ac"] = ind.accelerator(df1).to_numpy()
    I["hma21"] = ind.hma(close, 21).to_numpy()
    I["dema20"] = ind.dema(close, 20).to_numpy()
    I["tema9"], I["tema21"] = ind.tema(close, 9).to_numpy(), ind.tema(close, 21).to_numpy()
    I["vwma20"] = ind.vwma(df1, 20).to_numpy()
    I["cmf"] = ind.cmf(df1, 20).to_numpy()
    I["force13"] = ind.force_index(df1, 13).to_numpy()
    I["eom"] = ind.ease_of_movement(df1, 14).to_numpy()
    I["uo"] = ind.ultimate_oscillator(df1).to_numpy()
    bull, bear = ind.elder_ray(df1, 13); I["bull_power"], I["bear_power"] = bull.to_numpy(), bear.to_numpy()
    I["coppock"] = ind.coppock(close).to_numpy()
    kk, kks = ind.kst(close); I["kst"], I["kst_sig"] = kk.to_numpy(), kks.to_numpy()
    I["dpo"] = ind.dpo(close, 20).to_numpy()
    obv_s = ind.obv(df1); I["obv"] = obv_s.to_numpy(); I["obv_sma"] = obv_s.rolling(20).mean().to_numpy()
    adl_s = ind.ad_line(df1); I["adl"] = adl_s.to_numpy(); I["adl_ema"] = ind._ema_std(adl_s, 21).to_numpy()
    I["chaikin_osc"] = ind.chaikin_oscillator(df1).to_numpy()
    I["kama"] = ind.kama(close, 10).to_numpy()
    fu, fd, fup, fdp = ind.fractals(df1)
    I["frac_up"], I["frac_dn"] = fu.to_numpy(), fd.to_numpy()
    I["frac_up_px"], I["frac_dn_px"] = fup.to_numpy(), fdp.to_numpy()
    pv = ind.daily_pivots(df1)
    I["piv_p"], I["piv_r1"], I["piv_s1"], I["piv_r2"], I["piv_s2"] = pv
    wt1, wt2 = ind.wavetrend(df1); I["wt1"], I["wt2"] = wt1.to_numpy(), wt2.to_numpy()
    I["stc"] = ind.schaff_trend_cycle(close).to_numpy()
    fsh, fsht = ind.fisher_transform(df1); I["fisher"], I["fisher_trig"] = fsh.to_numpy(), fsht.to_numpy()
    qr, ql = ind.qqe(close); I["qqe_rsima"], I["qqe_line"] = qr.to_numpy(), ql.to_numpy()
    I["ssl_hlv"] = ind.ssl_channel(df1, 10).to_numpy()
    _uts, utp = ind.ut_bot(df1); I["ut_pos"] = utp.to_numpy()
    rff, rfd = ind.range_filter(df1); I["rf_filt"], I["rf_dir"] = rff.to_numpy(), rfd.to_numpy()
    ckl, cks = ind.chande_kroll(df1); I["ck_long"], I["ck_short"] = ckl.to_numpy(), cks.to_numpy()
    I["chand_dir"] = ind.chandelier_dir(df1).to_numpy()
    I["bbw_pct"] = ind.bbw_percentile(close, 20, 120).to_numpy()
    kvo, kvos = ind.klinger(df1); I["kvo"], I["kvo_sig"] = kvo.to_numpy(), kvos.to_numpy()
    cr3, cr4, cs3, cs4 = ind.camarilla_pivots(df1)
    I["cam_r3"], I["cam_r4"], I["cam_s3"], I["cam_s4"] = cr3, cr4, cs3, cs4
    _stf_l, stf_d = ind.supertrend(df1, 10, 1.0); I["st_dir_fast"] = stf_d.to_numpy()
    # --- round-3 research indicators (catalog2 round-3, 2026-06-04) ---
    I["ema144"], I["ema169"] = ind.ema(close, 144).to_numpy(), ind.ema(close, 169).to_numpy()
    gs, gl = ind.gmma(close); I["gmma_s"], I["gmma_l"] = gs.to_numpy(), gl.to_numpy()
    I["chop"] = ind.choppiness(df1, 14).to_numpy()
    I["hurst"] = ind.hurst(close, 100).to_numpy()
    I["open"] = df1["open"].to_numpy()
    I["open_time"] = df1["open_time"].to_numpy()
    # --- book-extracted candidate indicators (Stage 2, 2026-06-05; additive, 0-diff for non-book strats) ---
    for _bk in _BOOK_INDICATORS:
        try:
            I[_bk] = np.asarray(getattr(_indb, _bk)(df1), dtype=float)
        except Exception:
            I[_bk] = np.full(len(df1), np.nan)
    return I


def _atr_window(h, l, c, idx, win=24, period=14):
    if idx < win - 1:
        return None
    s = idx - win + 1
    hh, ll, cc = h[s:idx+1], l[s:idx+1], c[s:idx+1]
    pc = np.empty(len(cc)); pc[0] = np.nan; pc[1:] = cc[:-1]
    tr = np.maximum.reduce([hh - ll, np.abs(hh - pc), np.abs(ll - pc)]); tr[0] = np.nan
    v = ind._wilder_run(tr, period, 1)[-1]
    return None if np.isnan(v) else float(v)


def prepare(coin, cadence="day"):
    """Load + precompute everything a backtest needs for one (coin, cadence) ONCE so a
    sweep can SHARE it across every strategy on that coin/cadence (precompute is the
    expensive part). Returns a ctx dict, or None if the coin lacks data.

    Exit sub-bars are kept as sorted numpy O/H/L/C arrays; the bar loop slices the bars
    belonging to each entry bar via searchsorted (O(1) memory, identical visit order)."""
    entry_tf, exit_tf, htf_tf = CADENCES[cadence]
    ENTRY_MS, EXIT_MS, HTF_MS = TF_MS[entry_tf], TF_MS[exit_tf], TF_MS[htf_tf]
    df1 = _load(coin, entry_tf)
    if df1 is None or len(df1) < 250:
        return None
    I = precompute(df1)
    df4 = _load(coin, htf_tf)
    htf = (_htf_map(df1, df4, ENTRY_MS, HTF_MS) if df4 is not None
           else {"bias": np.zeros(len(df1)), "slope": np.zeros(len(df1)), "adx4": np.zeros(len(df1))})
    hex_ = _load(coin, exit_tf)
    e_ot = e_o = e_h = e_l = e_c = None
    if hex_ is not None:
        e_ot = hex_["open_time"].to_numpy()
        e_o = hex_["open"].to_numpy()   # sub-bar open -> gap-through-stop detection
        e_h, e_l, e_c = hex_["high"].to_numpy(), hex_["low"].to_numpy(), hex_["close"].to_numpy()
    return {"I": I, "htf": htf, "e_ot": e_ot, "e_o": e_o, "e_h": e_h, "e_l": e_l, "e_c": e_c,
            "ENTRY_MS": ENTRY_MS, "EXIT_MS": EXIT_MS, "n": len(df1), "cadence": cadence}


def run(coin, strategy, exit_cfg=None, start=205, cadence="day", ctx=None, end=None, cost_model=None):
    """Backtest one strategy on one coin over its full unified history, priced with the OSTIUM cost
    model (costs.py). gates are OFF (research mode): liquidation refunds $1000 and continues.
    cadence selects (entry, exit, htf) timeframes (see CADENCES). Pass a prepared `ctx`
    (engine.prepare) to reuse a shared precompute across many strategies. `start`/`end` bound the
    simulated entry-bar window (fresh $1000 account over [start, end)); used for walk-forward
    in/out-of-sample splits. `cost_model` = a costs.CostModel; default costs.GATE (Ostium realistic
    base). The stress test passes costs.for_scenario(name) to degrade it."""
    ex = {**DEFAULT_EXIT, **(exit_cfg or {})}
    # OSTIUM cost model -- each leg on its OWN axis (GAUNTLET.md rule): open/close fee + spread are
    # per-trade; rollover is per-day held; slippage is the adverse fill; oracle is a fixed $/close.
    cm = cost_model or _costs.GATE
    aclass = _instr.cost_class(coin)
    _s, _p = cm.scenario, cm.profile
    open_fee_rate  = (_p.open_fee_bps           / 10_000.0) * _s["fee_mult"]
    close_fee_rate = (_p.close_fee_bps          / 10_000.0) * _s["fee_mult"]
    spread_rate    = (_p.spread_bps(aclass)     / 10_000.0) * _s["slip_mult"]   # round-trip, charged once/trade
    hold_rate_day  = (_p.holding_per_day(aclass) / 10_000.0) * _s["hold_mult"]  # rollover/carry per CLASS, per day
    oracle_usd     = _p.oracle_fee_usd                                          # fixed $ per close
    if ctx is None:
        ctx = prepare(coin, cadence)
    if ctx is None:
        return None
    I = ctx["I"]; htf = ctx["htf"]
    # VOLATILITY-SCALED slippage (rule 3): per-bar adverse-fill fraction = floor + 5% of the bar's
    # ATR (in bps), capped at the fat-tail ceiling, scenario-scaled. Replaces the old flat floor;
    # vectorised once here so the bar loop just indexes slip_arr[i] (current-bar volatility).
    slip_arr = _costs.slip_fraction_array(_p, I["atr_pct"], _s["slip_mult"])
    e_ot, e_o, e_h, e_l, e_c = ctx["e_ot"], ctx.get("e_o"), ctx["e_h"], ctx["e_l"], ctx["e_c"]
    ENTRY_MS, EXIT_MS = ctx["ENTRY_MS"], ctx["EXIT_MS"]
    close = I["close"]; atr = I["atr"]; open_time = I["open_time"]
    n = ctx["n"]
    nn = n if end is None else min(int(end), n)        # window upper bound (walk-forward)
    # Per-pair early-data trim: never simulate before the pair's safe backtest-start year (HistData
    # 2000-2003 is too sparse). max() keeps the indicator warm-up `start` too.
    bt_year = _instr.backtest_start_year(coin)
    eff_start = max(start, int(np.searchsorted(open_time, _year_ms(bt_year), side="left"))) if bt_year else start
    realized = 0.0; cum_net = 0.0; pos = None; liq = 0
    trades = []; curve = []

    def aeq(mark):
        u = pos["dir"] * (mark - pos["entry"]) * pos["qty"] if pos else 0.0
        return BANKROLL + realized + u

    def close_pos(px, reason, now_ms):
        nonlocal realized, pos, cum_net
        gross = pos["dir"] * (px - pos["entry"]) * pos["qty"]
        notional = abs(pos["qty"] * pos["entry"])          # entry-notional proxy (stable over the hold)
        cfee = abs(pos["qty"] * px) * close_fee_rate       # closing fee (0 on Ostium)
        spread = notional * spread_rate                    # round-trip spread/impact, charged once at close
        days = max(0.0, (now_ms - pos["opened_ms"]) / 86_400_000.0)
        roll = notional * hold_rate_day * days             # Ostium rollover/carry (time axis)
        oracle = oracle_usd                                # fixed $ oracle fee per close
        realized += gross - cfee - spread - roll - oracle
        net = gross - pos["open_fee"] - cfee - spread - roll - oracle
        cum_net += net
        trades.append({"coin": coin, "side": pos["side"], "entry_time": int(pos["opened_ms"]),
                       "exit_time": int(now_ms), "entry_px": pos["entry"], "exit_px": float(px),
                       # stop_px = the LAST stop level (post-trailing); target_px = static TP.
                       # Recorded so the dashboard overlay can draw the SL/TP lines per trade.
                       "stop_px": float(pos["stop"]), "target_px": float(pos["target"]),
                       "net": float(net), "rollover": float(roll), "spread_cost": float(spread),
                       "oracle_fee": float(oracle), "funding": 0.0,   # funding ~0 for FX (kept for schema)
                       "r_multiple": float(net / pos["risk_usd"]) if pos["risk_usd"] > 0 else 0.0,
                       "reason": reason, "hold_h": (now_ms - pos["opened_ms"]) / 3_600_000})
        pos = None

    for i in range(eff_start, nn):
        t_i = int(open_time[i]); mark = close[i]
        cur_slip = float(slip_arr[i])    # this bar's volatility-scaled adverse-fill slippage fraction
        # exits on sub-bars belonging to this entry bar
        if pos is not None and e_ot is not None:
            lo = int(np.searchsorted(e_ot, t_i, side="left"))
            hi = int(np.searchsorted(e_ot, t_i + ENTRY_MS, side="left"))
            for k in range(lo, hi):
                otime = int(e_ot[k]); hib = e_h[k]; lob = e_l[k]; sc = e_c[k]
                if otime <= pos["opened_ms"]:
                    continue
                pos["best"] = max(pos["best"], hib) if pos["dir"] > 0 else min(pos["best"], lob)
                sd = abs(pos["entry"] - pos["orig_stop"])
                if ex["trail"] and sd > 0 and _exits.profit_r(pos["dir"], pos["best"], pos["entry"], sd) >= ex["trail_activate_r"]:
                    catr = _atr_window(e_h, e_l, e_c, k)
                    if catr:
                        chand = _exits.chandelier_stop(pos["best"], pos["dir"], ex["chand_mult"], catr)
                        be = _exits.breakeven_stop(pos["entry"], pos["dir"], sd)
                        new = _exits.tighten_stop(pos["stop"], chand, be, pos["dir"])
                        if new != pos["stop"]:
                            pos["stop"] = new; pos["trailing"] = True
                # Pessimistic straddle resolution: when a single sub-bar touches BOTH the stop and
                # the target we cannot know the intrabar order, so assume the STOP hit first. Check
                # the stop before the target -- this removes the old TP-first optimism that
                # over-stated edge on wide bars. A bar that only touches the target still books it.
                # Stop/time-stop are MARKET exits -> fill with adverse volatility-scaled slippage
                # (stop*(1 - dir*cur_slip)); take-profit is a resting trigger -> fill at the level.
                stop_fill = pos["stop"] * (1 - pos["dir"] * cur_slip)
                # GAP-THROUGH-STOP (Ostium RWA reopen risk): if the sub-bar OPENED beyond the stop,
                # the stop cannot fill at its level -> fill at the gap open (the realistic worse
                # price), not the stop. Otherwise fill ~stop with adverse slippage.
                gap_o = e_o[k] if e_o is not None else None
                done = None
                if pos["dir"] > 0:
                    if lob <= pos["stop"]:
                        fill = gap_o if (gap_o is not None and gap_o < stop_fill) else stop_fill
                        done = (fill, "trailing_stop" if pos["trailing"] else "stop_loss")
                    elif pos["target"] > 0 and hib >= pos["target"]:
                        done = (pos["target"], "take_profit")
                else:
                    if hib >= pos["stop"]:
                        fill = gap_o if (gap_o is not None and gap_o > stop_fill) else stop_fill
                        done = (fill, "trailing_stop" if pos["trailing"] else "stop_loss")
                    elif pos["target"] > 0 and lob <= pos["target"]:
                        done = (pos["target"], "take_profit")
                if done is None and (otime + EXIT_MS - pos["opened_ms"]) / 3_600_000 >= ex["time_stop_h"]:
                    done = (sc * (1 - pos["dir"] * cur_slip), "time_stop")
                if done:
                    close_pos(done[0], done[1], otime + EXIT_MS); break

        # signal at the entry-bar close
        sig = strategy(I, i, htf) if (not np.isnan(atr[i]) and atr[i] > 0) else None

        # exit-on-opposite
        if pos is not None and ex["exit_opposite"] and sig and sig != pos["side"]:
            close_pos(mark, "opposite", t_i + ENTRY_MS)

        if aeq(mark) <= 0:
            if pos is not None:
                close_pos(mark, "liquidation", t_i + ENTRY_MS)
            realized = 0.0; liq += 1

        if pos is None and sig:
            eq = aeq(mark)
            o = _size(sig, eq, mark, atr[i], ex, cur_slip, open_fee_rate)
            if o:
                o.update(side=sig, opened_ms=t_i + ENTRY_MS, best=o["entry"], trailing=False)
                realized -= o["open_fee"]; pos = o

        u = pos["dir"] * (mark - pos["entry"]) * pos["qty"] if pos else 0.0
        curve.append((t_i, BANKROLL + cum_net + u))

    return {"coin": coin, "trades": trades, "liquidations": liq,
            "curve": [[int(t), float(e)] for t, e in curve[::max(1, len(curve)//1200)]],
            "stats": _stats(trades, curve),
            "meta": {"start": int(open_time[0]), "end": int(open_time[-1]), "bars": n, "cadence": cadence}}


def _size(side, eq, mark, atr_v, ex, slip, open_fee_rate):   # slip + open-fee always supplied by run()
    d = 1 if side == "long" else -1
    if eq <= 0 or mark <= 0 or not atr_v or atr_v <= 0:
        return None
    entry = mark * (1 + d * slip)
    stop_dist = _exits.stop_distance(atr_v, ex["sl_atr"], entry, MIN_STOP_PCT)
    risk = eq * RISK_PCT
    qty = risk / stop_dist
    if qty * entry > eq * LEVERAGE * MAX_NOTIONAL_PCT:
        qty = eq * LEVERAGE * MAX_NOTIONAL_PCT / entry
    if qty <= 0 or qty * entry < MIN_NOTIONAL:
        return None
    stop = _exits.initial_stop(entry, d, stop_dist)
    target = _exits.initial_target(entry, d, atr_v, ex["tp_atr"]) if ex["tp_atr"] > 0 else 0.0
    return {"entry": entry, "qty": qty, "dir": d, "stop": stop, "orig_stop": stop,
            "target": target, "open_fee": qty * entry * open_fee_rate, "risk_usd": risk}


def _stats(trades, curve):
    n = len(trades)
    eq = np.array([e for _, e in curve]) if curve else np.array([BANKROLL])
    peak = np.maximum.accumulate(eq); dd = (eq - peak) / peak
    base = {"trades": n, "final_eq": round(float(eq[-1]), 2),
            "return_pct": round(float(eq[-1] / BANKROLL - 1) * 100, 2),
            "max_dd_pct": round(float(dd.min()) * 100, 2) if len(dd) else 0.0}
    if n == 0:
        base.update(win_rate=None, profit_factor=None, expectancy_r=None, net=0.0)
        return base
    nets = np.array([t["net"] for t in trades]); w = nets[nets > 0]; l = nets[nets < 0]
    base.update(win_rate=round(100 * len(w) / n, 1),
                profit_factor=round(float(w.sum() / -l.sum()), 3) if l.sum() < 0 else None,
                expectancy_r=round(float(np.mean([t["r_multiple"] for t in trades])), 3),
                net=round(float(nets.sum()), 2))
    return base
