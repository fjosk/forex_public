#!/usr/bin/env python3
"""
HistData.com bulk M1 downloader for the FOREX lab universe.

Source: https://www.histdata.com free generic-ASCII M1 bars. Unlike Binance Vision
(a plain public S3 bucket, see sister-lab/LAB/download.sh), each HistData download needs a
per-request token scraped from the pair/year page and a matching Referer header. The
community `histdata` package handles that handshake, so this downloader wraps it and
adds the three things the package does NOT do: resume (skip files already present),
atomic writes (download to a temp dir, validate, then move), and zip validation (the
fragile token path can return an HTML error page with HTTP 200, which a naive writer
would save as a corrupt ".zip").

Auto-discovery instead of hardcoded start dates: HistData has no clean file listing, so
the range is probed. We try every year from START_YEAR up to now; a year before a pair's
earliest data simply raises (no token / no data) and is skipped. The S3-style "ask what
exists" philosophy of the sister-lab downloader, adapted to a site with no index.

Granularity: M1 only (downsamples losslessly to 5m/15m/1h/4h/1d, all the backtest uses).
Tick is a different, far larger product and is intentionally not handled here.

Layout (mirrors sister-lab/LAB/data):
    LAB/data/<pair>/DAT_ASCII_<PAIR>_M1_<YYYY>.zip       past years (one per year)
    LAB/data/<pair>/DAT_ASCII_<PAIR>_M1_<YYYYMM>.zip     current year (one per month)

Usage:
    python3 download.py                      # all 13 HistData FX pairs, full history (from START_YEAR)
    python3 download.py --pairs eurusd       # one pair
    python3 download.py --start-year 2024    # shallow probe / quick test
Environment overrides (for the download.sh wrapper + cron parity with sister-lab):
    PAIRS, OUT_ROOT, FOREX_START_YEAR, FOREX_SLEEP
"""

import argparse
import os
import signal
import sys
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone

from histdata import download_hist_data

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # FOREX root
from shared import instruments as _instr   # the single instrument registry

# --- Configuration defaults (override via CLI flags or environment) ---
# The HistData FX/metals/energy pairs (the universe minus the Dukascopy-only commodities
# WTI/copper/natgas, which HistData does not carry). Single-sourced from the instrument registry.
DEFAULT_PAIRS = _instr.histdata_pairs()
DEFAULT_OUT_ROOT = "/home/user/FOREX/LAB/data"
DEFAULT_START_YEAR = 2000          # HistData's earliest (EUR/USD M1 starts here)
DEFAULT_SLEEP_SECONDS = 2.0        # be polite to a small free site; avoid rate-blocks
REQUEST_TIMEOUT = 90               # the histdata package calls requests WITHOUT a timeout;
                                   # a throttled/hung connection would block forever, so we
                                   # cap each call ourselves. 90s clears the multi-MB per-year
                                   # files with margin; a timeout becomes a logged retry.

# HistData generic-ASCII naming, recreated here so a file's presence can be checked
# BEFORE spending a network round-trip on it. Must match the histdata package exactly.
PLATFORM = "ASCII"
TIME_FRAME = "M1"


@contextmanager
def time_limit(seconds):
    """
    Hard wall-clock cap on a blocking call via SIGALRM. The histdata package issues
    requests with no timeout, so a stalled socket would hang the whole run; the alarm
    interrupts the blocked syscall and raises, which fetch_one catches as a transient
    error. Main-thread only (signal.alarm's constraint), which download.py always is.
    """
    def _on_alarm(signum, frame):
        raise TimeoutError("call exceeded {}s".format(seconds))

    previous = signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)                       # cancel even if the body raised
        signal.signal(signal.SIGALRM, previous)


def expected_filename(pair, year, month):
    """Name the histdata package writes for this pair/year[/month]. PAIR is upper-case."""
    if month is None:
        stamp = str(year)
    else:
        stamp = "{}{:02d}".format(year, month)
    return "DAT_{}_{}_{}_{}.zip".format(PLATFORM, pair.upper(), TIME_FRAME, stamp)


def is_valid_zip(path):
    """True only for a structurally sound zip. Catches HTML error pages saved as .zip."""
    if not zipfile.is_zipfile(path):
        return False
    try:
        with zipfile.ZipFile(path) as z:
            return z.testzip() is None        # testzip returns the first bad member, or None
    except zipfile.BadZipFile:
        return False


def fetch_one(pair, year, month, pair_dir, now_y, now_m):
    """
    Download a single pair/year[/month] archive with resume + atomic write + validation.

    Returns one of: 'skip' (already present), 'ok' (downloaded), 'unavailable'
    (no data for this period -- expected for years before a pair's listing), 'corrupt'
    (server returned non-zip), or 'error' (transient; next run retries since no file lands).
    """
    final_path = os.path.join(pair_dir, expected_filename(pair, year, month))

    # The in-progress current month grows daily, so always refetch it; every other
    # completed period is immutable once present.
    is_current_month = (year == now_y and month == now_m)
    if os.path.exists(final_path) and not is_current_month:
        return "skip"

    # Atomic write: land in a per-pair temp dir, validate, then move into place. A kill
    # mid-download leaves junk only in .part, never a half-written file that resume trusts.
    tmp_dir = os.path.join(pair_dir, ".part")
    os.makedirs(tmp_dir, exist_ok=True)

    try:
        with time_limit(REQUEST_TIMEOUT):
            got = download_hist_data(
                year=str(year),
                month=(str(month) if month is not None else None),
                pair=pair,
                time_frame=TIME_FRAME,
                platform=PLATFORM,
                output_directory=tmp_dir,
                verbose=False,
            )
    except AssertionError:
        # No token / "no data could be found" -> this period is not on HistData. Expected
        # for the years before a pair's earliest listing; not an error.
        return "unavailable"
    except Exception as exc:  # network/transient: log and move on, resume heals it
        sys.stderr.write("  WARN {} {} transient: {}\n".format(pair, year, exc))
        return "error"

    if not is_valid_zip(got):
        # Fragile token path can return an HTML error page with HTTP 200. Discard it so
        # resume retries rather than trusting a corrupt archive.
        try:
            os.remove(got)
        except OSError:
            pass
        return "corrupt"

    os.replace(got, final_path)               # atomic on the same filesystem
    return "ok"


def main():
    # Line-buffer stdout so progress and the cron log stay current even when redirected
    # to a file; default full buffering loses everything if the process is killed.
    sys.stdout.reconfigure(line_buffering=True)

    parser = argparse.ArgumentParser(description="HistData M1 bulk downloader (FOREX lab)")
    parser.add_argument("--pairs", default=os.environ.get("PAIRS", " ".join(DEFAULT_PAIRS)),
                        help="space- or comma-separated HistData pair codes (e.g. eurusd usdjpy)")
    parser.add_argument("--out", default=os.environ.get("OUT_ROOT", DEFAULT_OUT_ROOT),
                        help="raw-archive root (one subfolder created per pair)")
    parser.add_argument("--start-year", type=int,
                        default=int(os.environ.get("FOREX_START_YEAR", DEFAULT_START_YEAR)),
                        help="earliest year to probe; lower it only to reach older data")
    parser.add_argument("--sleep", type=float,
                        default=float(os.environ.get("FOREX_SLEEP", DEFAULT_SLEEP_SECONDS)),
                        help="seconds to pause between network calls")
    args = parser.parse_args()

    pairs = [p.lower() for p in args.pairs.replace(",", " ").split()]
    now = datetime.now(timezone.utc)          # month-boundary slop costs at most one extra refetch
    now_y, now_m = now.year, now.month

    print("=" * 46)
    print(" HistData M1 pull")
    print(" pairs      : {}".format(" ".join(pairs)))
    print(" years      : {}..{} + {} months of {}".format(args.start_year, now_y - 1, now_m, now_y))
    print(" out        : {}".format(args.out))
    print("=" * 46)

    for pair in pairs:
        pair_dir = os.path.join(args.out, pair)
        os.makedirs(pair_dir, exist_ok=True)
        tally = {"ok": 0, "skip": 0, "unavailable": 0, "corrupt": 0, "error": 0}

        # Past years: one archive per year (month=None is required for past years).
        for year in range(args.start_year, now_y):
            result = fetch_one(pair, year, None, pair_dir, now_y, now_m)
            tally[result] += 1
            if result == "ok":
                print("  ok  {} {}".format(pair, year))
            if result != "skip":              # only network attempts cost a pause
                time.sleep(args.sleep)

        # Current year: one archive per month up to the present month.
        for month in range(1, now_m + 1):
            result = fetch_one(pair, now_y, month, pair_dir, now_y, now_m)
            tally[result] += 1
            if result == "ok":
                print("  ok  {} {}-{:02d}".format(pair, now_y, month))
            if result != "skip":
                time.sleep(args.sleep)

        print("  {}: {} downloaded, {} present, {} unavailable, {} corrupt, {} errors".format(
            pair, tally["ok"], tally["skip"], tally["unavailable"], tally["corrupt"], tally["error"]))

    print("=" * 46)
    print("Done. Archives are zipped CSV under {}".format(args.out))


if __name__ == "__main__":
    main()
