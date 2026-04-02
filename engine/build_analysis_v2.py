#!/usr/bin/env python3
"""
Build ANALYSIS_v2 sheet from all years of Golf_Analytics data.

Columns G-N and Q are computed as VALUES in Python (faster writes, faster sheet load).
Columns O, P, R are kept as FORMULAS (they aggregate across all ANALYSIS rows).

To revert any column to a formula, see: docs/analysis_formula_reference.md
"""

import re
import time
import sys
import os
import gspread
from google.oauth2.service_account import Credentials

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE   = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID     = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SOURCE_SHEET = "ANALYSIS"
TARGET_SHEET = "ANALYSIS_v2"
SCOPES       = ["https://www.googleapis.com/auth/spreadsheets"]
BATCH_SIZE   = 500   # higher is ok since we write values, not formulas

HEADER = [
    "player_id", "player_name", "event_id", "year", "event_name", "round_num",
    "score", "par", "course_avg", "diff_course_avg", "condition", "color",
    "exec", "upside", "player_hist_par", "player_his_cnt", "Off Par", "Adj_his_par",
    "round_type"
]

# ─── Golf_Analytics column indices ───────────────────────────────────────────
GA_YEAR     = 0
GA_EVENT    = 1
GA_PLAYER   = 2
GA_SCORES   = [3, 4, 5, 6]        # D-G  R1-R4 scores
GA_COLORS   = [17, 18, 19, 20]    # R-U  R1-R4 rhythm/color
GA_EXECS    = [21, 24, 27, 30]    # V, Y, AB, AE  R1-R4 exec
GA_UPSIDES  = [22, 25, 28, 31]    # W, Z, AC, AF  R1-R4 upside
GA_RT       = [46, 47, 48, 49]    # AU-AX  R1-R4 round types
GA_WITHDRAW = 65                   # BN  withdrawal round

# ─── EVENTS column indices ───────────────────────────────────────────────────
EV_ID       = 0
EV_NAME     = 7     # H
EV_COND     = [33, 34, 35, 36]    # AH-AK  R1-R4 conditions
EV_YEAR     = 45    # AT
EV_CALM     = [46, 47, 48, 49]    # AU-AX  Calm R1-R4 avg
EV_MOD      = [50, 51, 52, 53]    # AY-BB  Moderate R1-R4 avg
EV_TOUGH    = [54, 55, 56, 57]    # BC-BF  Tough R1-R4 avg

# ─── EVENTS_COURSES column indices ───────────────────────────────────────────
EC_EVENT_ID = 0    # A
EC_YEAR     = 2    # C
EC_PAR      = 3    # D
EC_PRIMARY  = 4    # E  (1 = primary course)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def col_letter(n: int) -> str:
    result = ""
    n += 1
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def get_col(row, idx, default=""):
    try:
        val = row[idx]
        if isinstance(val, str):
            val = val.strip()
        return val if val != "" else default
    except IndexError:
        return default


def adjust_row(formula: str, from_row: int, to_row: int) -> str:
    """Shift non-absolute row references. B2→B3 but $B$2 unchanged."""
    if not isinstance(formula, str) or not formula.startswith("="):
        return formula
    pattern = r"(?<!\$)([A-Z]{1,3})" + str(from_row) + r"(?!\d)"
    return re.sub(pattern, lambda m: m.group(1) + str(to_row), formula)


def expand_locked_range(formula: str, total_rows: int) -> str:
    """
    Expand locked ranges like $Q$2:$Q$76737 to $Q$2:$Q$<total_rows>.
    Handles any column letter pattern.
    """
    pattern = r"(\$[A-Z]{1,3}\$2:\$[A-Z]{1,3}\$)(\d+)"
    return re.sub(pattern, lambda m: m.group(1) + str(total_rows), formula)


def compute_score(ga_row, round_num, course_avg):
    """Score with withdrawal penalty. Mirrors col-G formula logic."""
    scores      = [safe_float(get_col(ga_row, c)) for c in GA_SCORES]
    wr          = safe_float(get_col(ga_row, GA_WITHDRAW))
    wd_round    = int(wr) if wr is not None else 0
    actual      = scores[round_num - 1]

    if wd_round == 0:
        return actual if actual is not None else ""

    if round_num > wd_round:
        return ""

    if round_num == wd_round:
        prior = [s for s in scores[:wd_round - 1] if s is not None]
        if not prior:
            ca = safe_float(course_avg)
            return (ca + 4) if ca is not None else ""
        return min(prior) + 4

    return actual if actual is not None else ""


def get_condition(ev_row, round_num):
    return get_col(ev_row, EV_COND[round_num - 1])


def get_course_avg(ev_row, condition, round_num):
    r = round_num - 1
    col_map = {"Calm": EV_CALM, "Moderate": EV_MOD, "Tough": EV_TOUGH}
    cols = col_map.get(condition)
    return get_col(ev_row, cols[r]) if cols else ""


def get_off_par(score, par, ga_row, round_num):
    """score - par, blank if missing or round_type = Remove."""
    if score == "" or par == "":
        return ""
    round_type = get_col(ga_row, GA_RT[round_num - 1])
    if round_type == "Remove":
        return ""
    s, p = safe_float(score), safe_float(par)
    return (s - p) if s is not None and p is not None else ""


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("Authenticating …")
    if not os.path.exists(CREDS_FILE):
        sys.exit(f"ERROR: credentials file not found → {CREDS_FILE}")

    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    # ── 1. Golf_Analytics ─────────────────────────────────────────────────────
    print("Reading Golf_Analytics …")
    ga_data = ss.worksheet("Golf_Analytics").get_all_values()

    ga_lookup: dict[tuple, list] = {}
    combos:    set[tuple]        = set()

    for row in ga_data[1:]:
        if len(row) >= 3:
            year   = str(row[GA_YEAR]).strip()
            event  = row[GA_EVENT].strip()
            player = row[GA_PLAYER].strip()
            if player and event and year:
                key = (player, event, year)
                ga_lookup[key] = row
                combos.add(key)

    combos = sorted(combos)
    total_data_rows = len(combos) * 4
    locked_range_end = total_data_rows + 1   # row 2 to last data row
    print(f"  {len(combos)} combos → {total_data_rows} rows  (locked ranges will end at row {locked_range_end})")

    # ── 2. EVENTS ─────────────────────────────────────────────────────────────
    print("Reading EVENTS …")
    ev_data = ss.worksheet("EVENTS").get_all_values()

    event_id_lookup: dict[tuple, str] = {}
    events_by_id:    dict[str, list]  = {}

    for row in ev_data[1:]:
        if len(row) > EV_YEAR:
            ev_id   = row[EV_ID].strip()
            ev_name = row[EV_NAME].strip()
            ev_year = str(row[EV_YEAR]).strip()
            if ev_id and ev_name and ev_year:
                event_id_lookup[(ev_name, ev_year)] = ev_id
                events_by_id[ev_id] = row

    print(f"  {len(event_id_lookup)} events loaded")

    # ── 3. EVENTS_COURSES ─────────────────────────────────────────────────────
    print("Reading EVENTS_COURSES …")
    ec_data = ss.worksheet("EVENTS_COURSES").get_all_values()

    par_lookup: dict[tuple, str] = {}
    for row in ec_data[1:]:
        if len(row) > EC_PRIMARY:
            ec_id      = row[EC_EVENT_ID].strip()
            ec_year    = str(row[EC_YEAR]).strip()
            ec_par     = row[EC_PAR].strip()
            ec_primary = row[EC_PRIMARY].strip()
            if ec_id and ec_year and ec_primary == "1":
                par_lookup[(ec_id, ec_year)] = ec_par

    print(f"  {len(par_lookup)} par values loaded")

    # ── 4. ANALYSIS row-2 formula templates (O, P, R only) ───────────────────
    print("Reading ANALYSIS formula templates …")
    tmpl = ss.worksheet(SOURCE_SHEET).row_values(2, value_render_option="FORMULA")
    while len(tmpl) < 18:
        tmpl.append("")

    tmpl_a = tmpl[0]    # col A  – player_id (MATCH formula, keep)
    tmpl_o = tmpl[14]   # col O  – player_hist_par
    tmpl_p = tmpl[15]   # col P  – player_his_cnt
    tmpl_r = tmpl[17]   # col R  – Adj_his_par

    print(f"  Locked ranges will expand to row {locked_range_end}")

    # ── 5. Prepare ANALYSIS_v2 ────────────────────────────────────────────────
    print(f"Preparing {TARGET_SHEET} …")
    try:
        v2 = ss.worksheet(TARGET_SHEET)
        existing = v2.get_all_values()
        # Build set of already-written (player, event, year) combos
        done: set[tuple] = set()
        for row in existing[1:]:
            if len(row) >= 5 and row[1] and row[4] and row[3]:
                done.add((row[1].strip(), row[4].strip(), str(row[3]).strip()))
        next_row = len(existing) + 1
        print(f"  Resuming — {len(done)} combos already done, continuing from row {next_row}")
    except gspread.exceptions.WorksheetNotFound:
        v2 = ss.add_worksheet(TARGET_SHEET, rows=total_data_rows + 10, cols=18)
        v2.update("A1:S1", [HEADER], value_input_option="USER_ENTERED")
        done     = set()
        next_row = 2
        print("  Created new sheet")
        time.sleep(0.5)

    # Filter to only pending combos
    combos = [(p, e, y) for (p, e, y) in combos if (p, e, y) not in done]
    print(f"  {len(combos)} combos remaining → {len(combos) * 4} rows to write")

    # ── 6. Build all rows ─────────────────────────────────────────────────────
    print("Building rows …")
    all_rows   = []
    row_num    = next_row
    warn_count = 0

    for player, event, year in combos:
        event_id = event_id_lookup.get((event, year), "")
        if not event_id and warn_count < 20:
            print(f"  WARNING: no event_id for ({event!r}, {year!r})")
            warn_count += 1

        ga_row = ga_lookup.get((player, event, year), [])
        ev_row = events_by_id.get(event_id, [])
        # Use EVENTS year for par lookup (matches EVENTS_COURSES convention)
        events_year = get_col(ev_row, EV_YEAR) if ev_row else year
        par = par_lookup.get((event_id, events_year), "")
        # Fallback to Golf_Analytics year if still not found
        if par == "" and year != events_year:
            par = par_lookup.get((event_id, year), "")

        for rnd in range(1, 5):
            condition  = get_condition(ev_row, rnd)    if ev_row else ""
            course_avg = get_course_avg(ev_row, condition, rnd) if ev_row else ""
            score      = compute_score(ga_row, rnd, course_avg) if ga_row else ""

            s = safe_float(score)
            c = safe_float(course_avg)
            diff_ca = (s - c) if s is not None and c is not None else ""

            color    = get_col(ga_row, GA_COLORS[rnd - 1])  if ga_row else ""
            exec_val = get_col(ga_row, GA_EXECS[rnd - 1])   if ga_row else ""
            upside   = get_col(ga_row, GA_UPSIDES[rnd - 1]) if ga_row else ""
            off_par    = get_off_par(score, par, ga_row, rnd)  if ga_row else ""
            round_type = get_col(ga_row, GA_RT[rnd - 1])      if ga_row else ""

            # Formulas for O, P, R — adjust row ref AND expand locked ranges
            def build_formula(tmpl_f):
                f = adjust_row(tmpl_f, 2, row_num)
                f = expand_locked_range(f, locked_range_end)
                return f

            row = [
                adjust_row(tmpl_a, 2, row_num),   # A – player_id (formula)
                player,                             # B – player_name
                event_id,                           # C – event_id
                year,                               # D – year
                event,                              # E – event_name
                rnd,                                # F – round_num
                score,                              # G – score (value)
                par,                                # H – par (value)
                course_avg,                         # I – course_avg (value)
                diff_ca,                            # J – diff_course_avg (value)
                condition,                          # K – condition (value)
                color,                              # L – color (value)
                exec_val,                           # M – exec (value)
                upside,                             # N – upside (value)
                build_formula(tmpl_o),              # O – player_hist_par (formula)
                build_formula(tmpl_p),              # P – player_his_cnt (formula)
                off_par,                            # Q – Off Par (value)
                build_formula(tmpl_r),              # R – Adj_his_par (formula)
                round_type,                         # S – round_type (value)
            ]

            all_rows.append(row)
            row_num += 1

    print(f"  Built {len(all_rows)} rows")

    # ── 7. Write in batches ───────────────────────────────────────────────────
    n_batches = (len(all_rows) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Writing to {TARGET_SHEET} ({n_batches} batches of ≤{BATCH_SIZE} rows) …")

    for i in range(0, len(all_rows), BATCH_SIZE):
        batch     = all_rows[i : i + BATCH_SIZE]
        start_row = next_row + i
        end_row   = start_row + len(batch) - 1
        rng       = f"A{start_row}:{col_letter(18)}{end_row}"

        v2.update(rng, batch, value_input_option="USER_ENTERED")

        batch_num = i // BATCH_SIZE + 1
        print(f"  [{batch_num}/{n_batches}] rows {start_row}–{end_row} ✓")

        if i + BATCH_SIZE < len(all_rows):
            time.sleep(1.2)

    print(f"\nDone! {TARGET_SHEET} built with {row_num - 2} rows.")
    print("Verify years, scores, and conditions look correct — then swap in as ANALYSIS.")


if __name__ == "__main__":
    main()
