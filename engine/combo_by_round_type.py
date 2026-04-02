#!/usr/bin/env python3
"""
Analyze validated combos broken down by Round Type.

Shows Orange/Moderate/25-50, Purple/Calm/25-50, etc. across
Open/Survival/Positioning/Closing rounds.

Helps identify which round types drive the edge.
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
ANALYSIS_SHEET = "ANALYSIS_v2"
MIN_N          = 30
GOOD_THRESHOLD = -2
BAD_THRESHOLD  = 2

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "combo")

# Validated combos
VALIDATED_COMBOS = [
    ("Red", "Calm", 25, 50),
    ("Red", "Calm", 50, 75),
    ("Yellow", "Calm", 50, 25),
    ("Orange", "Moderate", 25, 50),
    ("Purple", "Calm", 25, 50),
    ("Green", "Moderate", 25, 75),
]


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Combo analysis by round type")
    parser.add_argument("--year-min", type=int, default=None, help="Min year (inclusive)")
    parser.add_argument("--year-max", type=int, default=None, help="Max year (inclusive)")
    args = parser.parse_args()

    # Load data
    print("Authenticating …")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    print(f"Loading {ANALYSIS_SHEET} …")
    raw    = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    df     = pd.DataFrame(raw[1:], columns=raw[0])
    print(f"  {len(df)} rows loaded")

    # Clean
    df["diff_course_avg"] = pd.to_numeric(df["diff_course_avg"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["exec_bucket"] = pd.to_numeric(df["exec_bucket"], errors="coerce")
    df["upside_bucket"] = pd.to_numeric(df["upside_bucket"], errors="coerce")
    df["round_type"] = df["round_type"].astype(str).str.strip()
    df["condition"] = df["condition"].astype(str).str.strip()
    df["color"] = df["color"].astype(str).str.strip()

    con = duckdb.connect()
    con.register("analysis", df)

    # Build year filter
    year_filter = ""
    if args.year_min is not None or args.year_max is not None:
        conditions = []
        if args.year_min is not None:
            conditions.append(f"CAST(year AS INTEGER) >= {args.year_min}")
        if args.year_max is not None:
            conditions.append(f"CAST(year AS INTEGER) <= {args.year_max}")
        year_filter = " AND " + " AND ".join(conditions) if conditions else ""

    year_range_str = "All years"
    if args.year_min is not None or args.year_max is not None:
        year_min_str = str(args.year_min) if args.year_min is not None else "—"
        year_max_str = str(args.year_max) if args.year_max is not None else "—"
        year_range_str = f"{year_min_str}–{year_max_str}"

    # Print header
    print("\n" + "="*100)
    print("VALIDATED COMBOS BY ROUND TYPE")
    print("="*100)
    print(f"Years: {year_range_str}\n")

    all_results = []

    # For each validated combo
    for color, condition, exec_bucket, upside_bucket in VALIDATED_COMBOS:
        print(f"\n{color.upper()} | {condition} | Exec {exec_bucket}-{exec_bucket+25} | Upside {upside_bucket}-{upside_bucket+25}")
        print("-" * 100)
        print(f"{'Round Type':<15} {'N':>6} {'Good%':>7} {'Bad%':>7} {'Edge':>8} {'Ratio':>7} {'Confidence':>12}")
        print("-" * 100)

        query = f"""
            WITH base AS (
                SELECT *
                FROM analysis
                WHERE diff_course_avg IS NOT NULL
                  AND color = '{color}'
                  AND condition = '{condition}'
                  AND CAST(exec_bucket AS INTEGER) = {exec_bucket}
                  AND CAST(upside_bucket AS INTEGER) = {upside_bucket}
                  AND round_type IN ('Open', 'Survival', 'Positioning', 'Closing'){year_filter}
            ),
            pop_overall AS (
                SELECT
                    COUNT(*) AS total_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_pop
                FROM base
            ),
            by_round AS (
                SELECT
                    round_type,
                    COUNT(*) AS n,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_count,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_count
                FROM base
                GROUP BY round_type
            )
            SELECT
                r.round_type,
                r.n,
                ROUND(r.good_count * 100.0 / r.n, 1) AS good_pct,
                ROUND(r.bad_count * 100.0 / r.n, 1) AS bad_pct,
                ROUND((r.good_count * 100.0 / r.n) - (p.good_pop * 100.0 / p.total_pop), 1) AS good_edge,
                ROUND(
                    CASE WHEN r.bad_count > 0 AND p.bad_pop > 0
                    THEN (r.good_count * 1.0 / NULLIF(r.bad_count, 0))
                       / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0))
                    ELSE NULL END, 2
                ) AS ratio
            FROM by_round r
            CROSS JOIN pop_overall p
            WHERE r.n >= {MIN_N}
            ORDER BY r.round_type
        """

        result_df = con.execute(query).df()

        if result_df.empty:
            print("  (No data with N >= 30)")
            continue

        for _, row in result_df.iterrows():
            ratio = row["ratio"]
            edge = row["good_edge"]
            n = int(row["n"])

            # Confidence heuristic
            if n < 50:
                confidence = "Low (N<50)"
            elif n < 100:
                confidence = "Medium (N<100)"
            else:
                confidence = "High (N>100)"

            ratio_str = f"{ratio:.2f}" if pd.notna(ratio) else "n/a"
            edge_str = f"{edge:+.1f}" if pd.notna(edge) else "n/a"
            print(f"{row['round_type']:<15} {n:>6} {row['good_pct']:>7.1f} {row['bad_pct']:>7.1f} {edge_str:>8} {ratio_str:>7} {confidence:>12}")

            all_results.append({
                "color": color,
                "condition": condition,
                "exec_bucket": exec_bucket,
                "upside_bucket": upside_bucket,
                "round_type": row["round_type"],
                "n": n,
                "good_pct": row["good_pct"],
                "bad_pct": row["bad_pct"],
                "good_edge": edge,
                "ratio": ratio,
            })

    # Save combined results
    if all_results:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        year_suffix = ""
        if args.year_min is not None or args.year_max is not None:
            year_min_str = str(args.year_min) if args.year_min is not None else "all"
            year_max_str = str(args.year_max) if args.year_max is not None else "all"
            year_suffix = f"_{year_min_str}_{year_max_str}"

        results_df = pd.DataFrame(all_results)
        csv_path = os.path.join(OUTPUT_DIR, f"validated_combos_by_round{year_suffix}.csv")
        results_df.to_csv(csv_path, index=False)
        print(f"\n\nResults saved to {csv_path}")


if __name__ == "__main__":
    main()
