#!/usr/bin/env python3
"""
Optimal Bucketing Analysis — exec & upside ranges

Tests multiple bucket sizes (5, 10, 15, 20, 25, 30, 40) and scores each by:
  - Number of high-edge buckets (ratio > 1.2 or < 0.8)
  - Stability (low std dev of edges)
  - Statistical power (N >= 30 minimum)

Filters to Calm/Moderate/Tough conditions only.
"""

import os
import sys
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

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "bucketing")
BUCKET_SIZES = [5, 10, 15, 20, 25, 30, 40]


def main():
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
    df["exec"] = pd.to_numeric(df["exec"], errors="coerce")
    df["upside"] = pd.to_numeric(df["upside"], errors="coerce")
    df["condition"] = df["condition"].astype(str).str.strip()
    df["color"] = df["color"].astype(str).str.strip()

    con = duckdb.connect()
    con.register("analysis", df)

    # Summary stats
    print(f"\n  Exec: {df['exec'].min():.1f}–{df['exec'].max():.1f} (mean={df['exec'].mean():.1f})")
    print(f"  Upside: {df['upside'].min():.1f}–{df['upside'].max():.1f} (mean={df['upside'].mean():.1f})")

    results = []

    for bucket_size in BUCKET_SIZES:
        print(f"\nAnalyzing bucket size {bucket_size} …")

        query = f"""
            WITH base AS (
                SELECT *
                FROM analysis
                WHERE diff_course_avg IS NOT NULL
                  AND color IS NOT NULL AND color != ''
                  AND condition IN ('Calm', 'Moderate', 'Tough')
                  AND exec IS NOT NULL
                  AND upside IS NOT NULL
            ),
            bucketed AS (
                SELECT
                    color,
                    condition,
                    (CAST(exec / {bucket_size} AS INTEGER)) * {bucket_size} AS exec_bucket,
                    (CAST(upside / {bucket_size} AS INTEGER)) * {bucket_size} AS upside_bucket,
                    COUNT(*) AS n,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_count,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_count
                FROM base
                GROUP BY color, condition, exec_bucket, upside_bucket
            ),
            population AS (
                SELECT
                    condition,
                    COUNT(*) AS total_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_pop,
                    SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_pop
                FROM base
                GROUP BY condition
            )
            SELECT
                b.color,
                b.condition,
                b.exec_bucket,
                b.upside_bucket,
                b.n,
                ROUND(b.good_count * 100.0 / b.n, 1) AS good_pct,
                ROUND(b.bad_count * 100.0 / b.n, 1) AS bad_pct,
                ROUND(p.good_pop * 100.0 / p.total_pop, 1) AS pop_good_pct,
                ROUND(p.bad_pop * 100.0 / p.total_pop, 1) AS pop_bad_pct,
                ROUND((b.good_count * 100.0 / b.n) - (p.good_pop * 100.0 / p.total_pop), 1) AS good_edge,
                ROUND((b.bad_count * 100.0 / b.n) - (p.bad_pop * 100.0 / p.total_pop), 1) AS bad_edge,
                ROUND(
                    CASE WHEN b.bad_count > 0 AND p.bad_pop > 0
                    THEN (b.good_count * 1.0 / NULLIF(b.bad_count, 0))
                       / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0))
                    ELSE NULL END, 2
                ) AS ratio
            FROM bucketed b
            JOIN population p ON b.condition = p.condition
            WHERE b.n >= {MIN_N}
            ORDER BY b.color, b.condition, b.exec_bucket, b.upside_bucket
        """

        bucket_df = con.execute(query).df()

        if bucket_df.empty:
            print(f"  ⚠ No data with N >= {MIN_N}")
            results.append((bucket_size, 0, 0, 0, 0))
            continue

        # Score this bucket size
        n_buckets = len(bucket_df)
        n_positive_edge = len(bucket_df[bucket_df["ratio"] > 1.2])
        n_negative_edge = len(bucket_df[bucket_df["ratio"] < 0.8])
        n_actionable = n_positive_edge + n_negative_edge

        avg_edge = bucket_df["good_edge"].mean()
        std_edge = bucket_df["good_edge"].std()
        avg_ratio = bucket_df["ratio"].mean()

        print(f"  Buckets: {n_buckets} (N >= {MIN_N})")
        print(f"  Actionable edges (ratio > 1.2 or < 0.8): {n_actionable} ({100*n_actionable/n_buckets if n_buckets > 0 else 0:.1f}%)")
        print(f"  Positive edges (ratio > 1.2): {n_positive_edge}")
        print(f"  Negative edges (ratio < 0.8): {n_negative_edge}")
        print(f"  Avg good_edge: {avg_edge:.2f}%, std: {std_edge:.2f}%")
        print(f"  Avg ratio: {avg_ratio:.2f}")

        # Save CSV
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        bucket_df.to_csv(
            os.path.join(OUTPUT_DIR, f"bucketing_{bucket_size}.csv"),
            index=False
        )

        results.append((bucket_size, n_buckets, n_actionable, avg_edge, std_edge))

    # Summary
    print("\n" + "="*75)
    print("BUCKETING SUMMARY")
    print("="*75)
    print(f"{'Bucket':>8} {'Total':>8} {'Action%':>10} {'Avg Edge':>12} {'Std Dev':>10}")
    print("-"*75)
    for bucket_size, n_buckets, n_actionable, avg_edge, std_edge in results:
        action_pct = 100 * n_actionable / n_buckets if n_buckets > 0 else 0
        print(f"{bucket_size:>8} {n_buckets:>8} {action_pct:>9.1f}% {avg_edge:>11.2f}% {std_edge:>10.2f}%")

    print(f"\nDetailed CSVs saved to {OUTPUT_DIR}/")
    print("Higher Action% + lower Std Dev = more stable edges")


if __name__ == "__main__":
    main()
