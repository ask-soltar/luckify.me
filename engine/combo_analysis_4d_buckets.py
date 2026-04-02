#!/usr/bin/env python3
"""
4D Analysis with Buckets: Round Type x Condition x Color x (Exec + Upside)

Tests if exec/upside bucket combo adds signal to foundation.
Exec and upside treated as a package (player performance vs potential).
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


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="4D: Round Type x Condition x Color x (Exec+Upside)")
    parser.add_argument("--year-min", type=int, default=None, help="Min year (inclusive)")
    parser.add_argument("--year-max", type=int, default=None, help="Max year (inclusive)")
    args = parser.parse_args()

    # Load data
    print("Authenticating ...")
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss     = client.open_by_key(SHEET_ID)

    print(f"Loading {ANALYSIS_SHEET} ...")
    raw    = ss.worksheet(ANALYSIS_SHEET).get_all_values()
    df     = pd.DataFrame(raw[1:], columns=raw[0])
    print(f"  {len(df)} rows loaded")

    # Clean
    df["diff_course_avg"] = pd.to_numeric(df["diff_course_avg"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["round_type"] = df["round_type"].astype(str).str.strip()
    df["condition"] = df["condition"].astype(str).str.strip()
    df["color"] = df["color"].astype(str).str.strip()
    df["exec_bucket"] = pd.to_numeric(df["exec_bucket"], errors="coerce")
    df["upside_bucket"] = pd.to_numeric(df["upside_bucket"], errors="coerce")

    con = duckdb.connect()
    con.register("analysis", df)

    # Build year filter if specified
    year_filter = ""
    if args.year_min is not None or args.year_max is not None:
        conditions = []
        if args.year_min is not None:
            conditions.append(f"CAST(year AS INTEGER) >= {args.year_min}")
        if args.year_max is not None:
            conditions.append(f"CAST(year AS INTEGER) <= {args.year_max}")
        year_filter = " AND " + " AND ".join(conditions) if conditions else ""

    # Base CTE
    BASE_CTE = f"""
        base AS (
            SELECT *
            FROM analysis
            WHERE diff_course_avg IS NOT NULL
              AND color IS NOT NULL AND color != ''
              AND condition IN ('Calm', 'Moderate', 'Tough')
              AND round_type IS NOT NULL AND round_type != ''
              AND exec_bucket IS NOT NULL
              AND upside_bucket IS NOT NULL{year_filter}
        )
    """

    # Query
    query = f"""
        WITH {BASE_CTE},
        population AS (
            SELECT
                round_type,
                condition,
                COUNT(*) AS total_pop,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_pop,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_pop
            FROM base
            GROUP BY round_type, condition
        ),
        by_combo AS (
            SELECT
                round_type,
                condition,
                color,
                CAST(exec_bucket AS INTEGER) AS exec_bucket,
                CAST(upside_bucket AS INTEGER) AS upside_bucket,
                COUNT(*) AS n,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_count,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_count,
                AVG(CAST(diff_course_avg AS DOUBLE)) AS avg_diff
            FROM base
            GROUP BY round_type, condition, color, exec_bucket, upside_bucket
        )
        SELECT
            c.round_type,
            c.condition,
            c.color,
            c.exec_bucket,
            c.upside_bucket,
            c.n,
            ROUND(c.good_count * 100.0 / c.n, 1) AS good_pct,
            ROUND(c.bad_count * 100.0 / c.n, 1) AS bad_pct,
            ROUND(p.good_pop * 100.0 / p.total_pop, 1) AS pop_good_pct,
            ROUND(p.bad_pop * 100.0 / p.total_pop, 1) AS pop_bad_pct,
            ROUND((c.good_count * 100.0 / c.n) - (p.good_pop * 100.0 / p.total_pop), 1) AS good_edge,
            ROUND((c.bad_count * 100.0 / c.n) - (p.bad_pop * 100.0 / p.total_pop), 1) AS bad_edge,
            ROUND(
                CASE WHEN c.bad_count > 0 AND p.bad_pop > 0
                THEN (c.good_count * 1.0 / NULLIF(c.bad_count, 0))
                   / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0))
                ELSE NULL END, 2
            ) AS ratio,
            ROUND(c.avg_diff, 2) AS avg_diff
        FROM by_combo c
        JOIN population p ON c.round_type = p.round_type AND c.condition = p.condition
        WHERE c.n >= {MIN_N}
        ORDER BY c.round_type, c.condition, c.color, c.exec_bucket, c.upside_bucket
    """

    print("Running query ...")
    combo_df = con.execute(query).df()

    # Print summary
    print(f"\n{'='*90}")
    print("4D ANALYSIS - Round Type x Condition x Color x (Exec+Upside Buckets)")
    print("="*90)

    year_range_str = "All years"
    if args.year_min is not None or args.year_max is not None:
        year_min_str = str(args.year_min) if args.year_min is not None else "-"
        year_max_str = str(args.year_max) if args.year_max is not None else "-"
        year_range_str = f"{year_min_str}-{year_max_str}"

    print(f"Years: {year_range_str}")
    print(f"Total combos with N >= {MIN_N}: {len(combo_df)}")
    print(f"Threshold: good = diff <= {GOOD_THRESHOLD}, bad = diff >= {BAD_THRESHOLD}\n")

    # Breakdown by edge strength
    positive_strong = len(combo_df[combo_df["ratio"] > 1.2])
    negative_strong = len(combo_df[combo_df["ratio"] < 0.8])
    neutral = len(combo_df[(combo_df["ratio"] >= 0.9) & (combo_df["ratio"] <= 1.1)])

    print(f"Strong positive edges (ratio > 1.2): {positive_strong}")
    print(f"Strong negative edges (ratio < 0.8): {negative_strong}")
    print(f"Neutral (0.9-1.1): {neutral}")
    print(f"Other: {len(combo_df) - positive_strong - negative_strong - neutral}")

    # Top positive combos
    print(f"\nTop 15 Positive Edges (by good_edge):")
    print("-" * 100)
    top_positive = combo_df[combo_df["ratio"] > 1.0].nlargest(15, "good_edge")
    for _, row in top_positive.iterrows():
        print(f"  {row['round_type']:12} {row['condition']:<8} {row['color']:>8} | "
              f"Exec {int(row['exec_bucket']):2} Up {int(row['upside_bucket']):2} | "
              f"N {row['n']:>4.0f} | Edge {row['good_edge']:>+6.1f}% | Ratio {row['ratio']:>6.2f}")

    # Top negative combos
    print(f"\nTop 15 Negative Edges (by good_edge):")
    print("-" * 100)
    top_negative = combo_df[combo_df["ratio"] < 1.0].nsmallest(15, "good_edge")
    for _, row in top_negative.iterrows():
        print(f"  {row['round_type']:12} {row['condition']:<8} {row['color']:>8} | "
              f"Exec {int(row['exec_bucket']):2} Up {int(row['upside_bucket']):2} | "
              f"N {row['n']:>4.0f} | Edge {row['good_edge']:>+6.1f}% | Ratio {row['ratio']:>6.2f}")

    # Save CSV
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    year_suffix = ""
    if args.year_min is not None or args.year_max is not None:
        year_min_str = str(args.year_min) if args.year_min is not None else "all"
        year_max_str = str(args.year_max) if args.year_max is not None else "all"
        year_suffix = f"_{year_min_str}_{year_max_str}"

    csv_path = os.path.join(OUTPUT_DIR, f"4d_buckets{year_suffix}.csv")
    combo_df.to_csv(csv_path, index=False)
    print(f"\nFull results saved to {csv_path}")


if __name__ == "__main__":
    main()
