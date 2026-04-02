#!/usr/bin/env python3
"""
Threshold Analysis — diff_course_avg by Round Type × Color

Metrics per bucket:
  - good_pct   : % rounds where diff_course_avg ≤ -2
  - bad_pct    : % rounds where diff_course_avg ≥ +2
  - good_edge  : good_pct minus population baseline
  - bad_edge   : bad_pct minus population baseline
  - ratio      : (good/bad) for this group vs (good/bad) for population
                 > 1.0 = more good relative to bad than population average

Three views:
  1. Round Type × Color          (primary)
  2. Condition × Color           (secondary)
  3. Round Type × Condition × Color (deep)

Filters:
  - round_type not in ('Remove', 'REMOVE', '') — excludes marked rounds
  - diff_course_avg not blank
  - color not blank
  - N >= 30 minimum sample
"""

import os
import sys
import argparse
import gspread
import pandas as pd
import duckdb
from google.oauth2.service_account import Credentials

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDS_FILE     = os.path.join(BASE_DIR, "luckifyme-f6c83489cd24.json")
SHEET_ID       = "1K4Zfb3VDZsnOitxmc4w3yoIi0Ng7dPby32fQLAl9lok"
SCOPES         = ["https://www.googleapis.com/auth/spreadsheets"]
ANALYSIS_SHEET = "ANALYSIS_v2"   # swap to "ANALYSIS" once renamed
MIN_N          = 30
GOOD_THRESHOLD = -2
BAD_THRESHOLD  = 2

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "threshold")


# ─── Helpers ─────────────────────────────────────────────────────────────────

def print_table(df, group_col, title):
    print(f"\n{'='*75}")
    print(f"  {title}")
    print(f"{'='*75}")
    print(f"  {'Color':<10} {'N':>6} {'Good%':>7} {'Bad%':>7} "
          f"{'PGood%':>8} {'PBad%':>7} {'GoodEdge':>9} {'BadEdge':>8} {'Ratio':>7}")
    print(f"  {'-'*75}")
    for _, row in df.iterrows():
        ratio_str = f"{row['ratio']:>7.2f}" if pd.notna(row['ratio']) else "    n/a"
        print(
            f"  {row['color']:<10} {int(row['n']):>6} "
            f"{row['good_pct']:>7.1f} {row['bad_pct']:>7.1f} "
            f"{row['pop_good_pct']:>8.1f} {row['pop_bad_pct']:>7.1f} "
            f"{row['good_edge']:>+9.1f} {row['bad_edge']:>+8.1f} "
            f"{ratio_str}"
        )


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    # ── Parse arguments ───────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="Threshold analysis with optional year filtering")
    parser.add_argument("--year-min", type=int, default=None, help="Min year (inclusive)")
    parser.add_argument("--year-max", type=int, default=None, help="Max year (inclusive)")
    args = parser.parse_args()

    # ── Load data ─────────────────────────────────────────────────────────────
    print("Authenticating …")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    print(f"Loading {ANALYSIS_SHEET} …")
    raw    = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    df     = pd.DataFrame(raw[1:], columns=raw[0])
    print(f"  {len(df)} rows loaded")

    # ── Clean ─────────────────────────────────────────────────────────────────
    df["diff_course_avg"] = pd.to_numeric(df["diff_course_avg"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Register with DuckDB
    con = duckdb.connect()
    con.register("analysis", df)

    # ── Build year filter if specified ─────────────────────────────────────────
    year_filter = ""
    if args.year_min is not None or args.year_max is not None:
        conditions = []
        if args.year_min is not None:
            conditions.append(f"CAST(year AS INTEGER) >= {args.year_min}")
        if args.year_max is not None:
            conditions.append(f"CAST(year AS INTEGER) <= {args.year_max}")
        year_filter = " AND " + " AND ".join(conditions) if conditions else ""

    # ── Base CTE (reused across all queries) ──────────────────────────────────
    BASE_CTE = f"""
        base AS (
            SELECT *
            FROM analysis
            WHERE diff_course_avg IS NOT NULL
              AND color IS NOT NULL
              AND color != ''
              AND round_type IS NOT NULL
              AND UPPER(TRIM(round_type)) NOT IN ('REMOVE', ''){year_filter}
        )
    """

    def run_query(group_cols: list[str]) -> pd.DataFrame:
        group_str = ", ".join(f"b.{c}" for c in group_cols)
        pop_group = ", ".join(group_cols) if len(group_cols) > 1 else group_cols[0]
        # For population, use everything EXCEPT color to get the baseline
        pop_group_no_color = [c for c in group_cols if c != "color"]

        if pop_group_no_color:
            pop_select = ", ".join(pop_group_no_color)
            pop_join   = " AND ".join(f"g.{c} = p.{c}" for c in pop_group_no_color)
            pop_group_clause = f"GROUP BY {pop_select}"
        else:
            pop_select = "'all' AS _all"
            pop_join   = "1=1"
            pop_group_clause = ""

        return con.execute(f"""
            WITH {BASE_CTE},
            population AS (
                SELECT
                    {pop_select},
                    COUNT(*) AS total_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD}  THEN 1 ELSE 0 END) AS bad_pop
                FROM base
                {pop_group_clause}
            ),
            by_group AS (
                SELECT
                    {group_str},
                    COUNT(*) AS n,
                    SUM(CASE WHEN CAST(b.diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_count,
                    SUM(CASE WHEN CAST(b.diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD}  THEN 1 ELSE 0 END) AS bad_count,
                    AVG(CAST(b.diff_course_avg AS DOUBLE)) AS avg_diff
                FROM base b
                GROUP BY {group_str}
            )
            SELECT
                {', '.join(f'g.{c}' for c in group_cols)},
                g.n,
                ROUND(g.good_count * 100.0 / g.n, 1) AS good_pct,
                ROUND(g.bad_count  * 100.0 / g.n, 1) AS bad_pct,
                ROUND(p.good_pop   * 100.0 / p.total_pop, 1) AS pop_good_pct,
                ROUND(p.bad_pop    * 100.0 / p.total_pop, 1) AS pop_bad_pct,
                ROUND((g.good_count * 100.0 / g.n) - (p.good_pop * 100.0 / p.total_pop), 1) AS good_edge,
                ROUND((g.bad_count  * 100.0 / g.n) - (p.bad_pop  * 100.0 / p.total_pop), 1) AS bad_edge,
                ROUND(
                    CASE WHEN g.bad_count > 0 AND p.bad_pop > 0
                    THEN (g.good_count * 1.0 / NULLIF(g.bad_count, 0))
                       / (p.good_pop   * 1.0 / NULLIF(p.bad_pop,  0))
                    ELSE NULL END, 2
                ) AS ratio,
                ROUND(g.avg_diff, 2) AS avg_diff
            FROM by_group g
            JOIN population p ON {pop_join}
            WHERE g.n >= {MIN_N}
            ORDER BY {', '.join(f'g.{c}' for c in group_cols[:-1])}, good_edge DESC
        """).df()

    # ── View 1: Round Type × Color ────────────────────────────────────────────
    print("\n\n" + "█"*75)
    print("  VIEW 1: ROUND TYPE × COLOR")
    print("█"*75)
    year_range_str = "All years"
    if args.year_min is not None or args.year_max is not None:
        year_min_str = str(args.year_min) if args.year_min is not None else "—"
        year_max_str = str(args.year_max) if args.year_max is not None else "—"
        year_range_str = f"{year_min_str}–{year_max_str}"
    print(f"  Years: {year_range_str}")
    print(f"  Threshold: good = diff ≤ {GOOD_THRESHOLD}, bad = diff ≥ {BAD_THRESHOLD}  |  Min N = {MIN_N}")
    print("  Ratio > 1.0 = more good/bad than population baseline")

    rt_df = run_query(["round_type", "color"])
    for rt in ["Open", "Survival", "Positioning", "Closing"]:
        subset = rt_df[rt_df["round_type"] == rt]
        if not subset.empty:
            print_table(subset, "round_type", rt)

    # ── View 2: Condition × Color ─────────────────────────────────────────────
    print("\n\n" + "█"*75)
    print("  VIEW 2: CONDITION × COLOR")
    print("█"*75)

    cond_df = run_query(["condition", "color"])
    for cond in ["Calm", "Moderate", "Tough"]:
        subset = cond_df[cond_df["condition"] == cond]
        if not subset.empty:
            print_table(subset, "condition", cond)

    # ── View 3: Round Type × Condition × Color ───────────────────────────────
    print("\n\n" + "█"*75)
    print("  VIEW 3: ROUND TYPE × CONDITION × COLOR  (deep cut)")
    print("█"*75)

    deep_df = run_query(["round_type", "condition", "color"])
    for rt in ["Open", "Survival", "Positioning", "Closing"]:
        for cond in ["Calm", "Moderate", "Tough"]:
            subset = deep_df[(deep_df["round_type"] == rt) & (deep_df["condition"] == cond)]
            if not subset.empty:
                print_table(subset, "color", f"{rt} — {cond}")

    # ── Save CSVs ─────────────────────────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Add year suffix to filenames for easy comparison
    year_suffix = ""
    if args.year_min is not None or args.year_max is not None:
        year_min_str = str(args.year_min) if args.year_min is not None else "all"
        year_max_str = str(args.year_max) if args.year_max is not None else "all"
        year_suffix = f"_{year_min_str}_{year_max_str}"

    rt_df.to_csv(os.path.join(OUTPUT_DIR, f"by_roundtype_color{year_suffix}.csv"), index=False)
    cond_df.to_csv(os.path.join(OUTPUT_DIR, f"by_condition_color{year_suffix}.csv"), index=False)
    deep_df.to_csv(os.path.join(OUTPUT_DIR, f"by_roundtype_condition_color{year_suffix}.csv"), index=False)

    print(f"\n\nResults saved to {OUTPUT_DIR}/")
    print("Done. Switch back with /model haiku to save tokens.")


if __name__ == "__main__":
    main()
