#!/usr/bin/env python3
"""
Find all strong combos in test data, broken down by round type.

Searches for combos with ratio > 1.2 or < 0.8 in test set (2025-2026),
then shows which round types drive the edges.
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

    # Find all strong combos in test (2025-2026)
    print("\nFinding strong combos in test set (2025-2026) …")

    query = f"""
        WITH base AS (
            SELECT *
            FROM analysis
            WHERE diff_course_avg IS NOT NULL
              AND color IS NOT NULL AND color != ''
              AND condition IN ('Calm', 'Moderate', 'Tough')
              AND exec_bucket IS NOT NULL
              AND upside_bucket IS NOT NULL
              AND CAST(year AS INTEGER) >= 2025
              AND CAST(year AS INTEGER) <= 2026
        ),
        pop_overall AS (
            SELECT
                COUNT(*) AS total_pop,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_pop,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_pop
            FROM base
        ),
        by_combo AS (
            SELECT
                color,
                condition,
                CAST(exec_bucket AS INTEGER) AS exec_bucket,
                CAST(upside_bucket AS INTEGER) AS upside_bucket,
                COUNT(*) AS n,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) <= {GOOD_THRESHOLD} THEN 1 ELSE 0 END) AS good_count,
                SUM(CASE WHEN CAST(diff_course_avg AS DOUBLE) >= {BAD_THRESHOLD} THEN 1 ELSE 0 END) AS bad_count
            FROM base
            GROUP BY color, condition, exec_bucket, upside_bucket
        )
        SELECT
            c.color,
            c.condition,
            c.exec_bucket,
            c.upside_bucket,
            c.n,
            ROUND(c.good_count * 100.0 / c.n, 1) AS good_pct,
            ROUND(c.bad_count * 100.0 / c.n, 1) AS bad_pct,
            ROUND((c.good_count * 100.0 / c.n) - (p.good_pop * 100.0 / p.total_pop), 1) AS good_edge,
            ROUND(
                CASE WHEN c.bad_count > 0 AND p.bad_pop > 0
                THEN (c.good_count * 1.0 / NULLIF(c.bad_count, 0))
                   / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0))
                ELSE NULL END, 2
            ) AS ratio
        FROM by_combo c
        CROSS JOIN pop_overall p
        WHERE c.n >= {MIN_N}
          AND (c.good_count * 1.0 / NULLIF(c.bad_count, 0)) / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0)) > 1.2
           OR (c.good_count * 1.0 / NULLIF(c.bad_count, 0)) / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0)) < 0.8
        ORDER BY ABS((c.good_count * 1.0 / NULLIF(c.bad_count, 0)) / (p.good_pop * 1.0 / NULLIF(p.bad_pop, 0)) - 1.0) DESC
    """

    combos_df = con.execute(query).df()
    print(f"Found {len(combos_df)} strong combos (ratio > 1.2 or < 0.8, N >= {MIN_N})")

    # Print header
    print("\n" + "="*120)
    print("STRONG COMBOS IN TEST (2025-2026) — BREAKDOWN BY ROUND TYPE")
    print("="*120)

    all_results = []

    # For each strong combo
    for idx, (_, combo_row) in enumerate(combos_df.iterrows()):
        color = combo_row["color"]
        condition = combo_row["condition"]
        exec_bucket = int(combo_row["exec_bucket"])
        upside_bucket = int(combo_row["upside_bucket"])
        combo_ratio = combo_row["ratio"]
        combo_edge = combo_row["good_edge"]

        print(f"\n[{idx+1}/{len(combos_df)}] {color.upper()} | {condition} | Exec {exec_bucket}-{exec_bucket+25} | Upside {upside_bucket}-{upside_bucket+25}")
        print(f"      Overall: Edge {combo_edge:+.1f}%, Ratio {combo_ratio:.2f}, N={int(combo_row['n'])}")
        print("-" * 120)
        print(f"{'Round Type':<15} {'N':>6} {'Good%':>7} {'Bad%':>7} {'Edge':>8} {'Ratio':>7}")
        print("-" * 120)

        query_round = f"""
            WITH base AS (
                SELECT *
                FROM analysis
                WHERE diff_course_avg IS NOT NULL
                  AND color = '{color}'
                  AND condition = '{condition}'
                  AND CAST(exec_bucket AS INTEGER) = {exec_bucket}
                  AND CAST(upside_bucket AS INTEGER) = {upside_bucket}
                  AND round_type IN ('Open', 'Survival', 'Positioning', 'Closing')
                  AND CAST(year AS INTEGER) >= 2025
                  AND CAST(year AS INTEGER) <= 2026
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
            WHERE r.n >= 20
            ORDER BY r.round_type
        """

        round_df = con.execute(query_round).df()

        if round_df.empty:
            print("  (No round-type breakdown with N >= 20)")
            continue

        for _, round_row in round_df.iterrows():
            ratio = round_row["ratio"]
            edge = round_row["good_edge"]
            ratio_str = f"{ratio:.2f}" if pd.notna(ratio) else "n/a"
            edge_str = f"{edge:+.1f}" if pd.notna(edge) else "n/a"
            print(f"{round_row['round_type']:<15} {int(round_row['n']):>6} {round_row['good_pct']:>7.1f} {round_row['bad_pct']:>7.1f} {edge_str:>8} {ratio_str:>7}")

            all_results.append({
                "color": color,
                "condition": condition,
                "exec_bucket": exec_bucket,
                "upside_bucket": upside_bucket,
                "round_type": round_row["round_type"],
                "n": int(round_row["n"]),
                "good_pct": round_row["good_pct"],
                "bad_pct": round_row["bad_pct"],
                "good_edge": edge,
                "ratio": ratio,
                "combo_overall_ratio": combo_ratio,
            })

    # Save results
    if all_results:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        results_df = pd.DataFrame(all_results)
        csv_path = os.path.join(OUTPUT_DIR, "strong_combos_by_round_2025_2026.csv")
        results_df.to_csv(csv_path, index=False)

        print(f"\n\nResults saved to {csv_path}")
        print(f"Total round-type combinations: {len(all_results)}")


if __name__ == "__main__":
    main()
