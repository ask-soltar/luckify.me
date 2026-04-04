#!/usr/bin/env python3
"""
Backtest Color × Personal Day combos using train/test split.

Training: 2022, 2023, 2024
Testing: 2025, 2026 (or holdout 80/20 if unavailable)

Combos tested:
1. Direction Switchers:
   - Orange × Day 1 (expect ~55.6% beat field on Tough)
   - Orange × Day 33 (expect ~80% beat field on Tough)
   - Green × Day 11 (expect ~52-55% beat field on Moderate/Tough)

2. Consistent Winners:
   - Red × Day 8, Green × Day 2, Purple × Day 3, Yellow × Day 22

3. Weak/Avoid:
   - Red × Day 4, Purple × Day 11

Output: backtest_summary.txt + backtest_detailed.csv
"""

import duckdb
import pandas as pd
import numpy as np
from scipy import stats
import json

# ============================================================================
# Configuration
# ============================================================================

DATA_FILE = "d:\\Projects\\luckify-me\\Golf Historics v3 - ANALYSIS (7).csv"

# Combos to backtest
COMBOS_TO_TEST = [
    # Direction Switchers
    ("Orange", 1, "Direction Switcher"),
    ("Orange", 33, "Direction Switcher"),
    ("Green", 11, "Direction Switcher"),
    # Consistent Winners
    ("Red", 8, "Consistent Winner"),
    ("Green", 2, "Consistent Winner"),
    ("Purple", 3, "Consistent Winner"),
    ("Yellow", 22, "Consistent Winner"),
    # Weak/Avoid
    ("Red", 4, "Weak/Avoid"),
    ("Purple", 11, "Weak/Avoid"),
    # Additional candidates for 20 total
    ("Blue", 5, "Candidate"),
    ("Pink", 15, "Candidate"),
    ("Brown", 7, "Candidate"),
    ("Orange", 10, "Candidate"),
    ("Green", 20, "Candidate"),
    ("Red", 15, "Candidate"),
    ("Purple", 7, "Candidate"),
    ("Yellow", 11, "Candidate"),
    ("Blue", 22, "Candidate"),
    ("Pink", 8, "Candidate"),
    ("Brown", 14, "Candidate"),
]

# Standard filters
CONDITIONS = ["Calm", "Moderate", "Tough"]
ROUND_TYPES = ["Open", "Positioning", "Closing", "Survival"]
TOURNAMENT_TYPES = ["S", "NS"]

# ============================================================================
# DuckDB Query Setup
# ============================================================================

print("Loading data into DuckDB...")
conn = duckdb.connect(":memory:")

# Read CSV and prepare data
df = pd.read_csv(DATA_FILE, low_memory=False)
print(f"Total rows: {len(df):,}")

# Ensure year and personal_day columns exist
if 'year' not in df.columns:
    print("ERROR: 'year' column not found")
    print(f"Available columns: {df.columns.tolist()}")
    exit(1)

if 'Personal Day' not in df.columns:
    print("ERROR: 'Personal Day' column not found")
    print(f"Available columns: {df.columns.tolist()}")
    exit(1)

# Convert numeric columns to proper types
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['Personal Day'] = pd.to_numeric(df['Personal Day'], errors='coerce')

# Register dataframe in DuckDB
conn.register('analysis', df)

# ============================================================================
# Helper Functions
# ============================================================================

def calculate_win_rate_ci(vs_avg_values):
    """
    Calculate win rate (% beats field avg) with 95% CI.
    Beat field avg = vs_avg > 0
    """
    if len(vs_avg_values) == 0:
        return None, None, None

    beats = (vs_avg_values > 0).sum()
    n = len(vs_avg_values)
    win_rate = beats / n

    # Wilson score interval (more accurate for extreme proportions)
    z = 1.96  # 95% CI
    denominator = 1 + z**2 / n
    center = (win_rate + z**2 / (2*n)) / denominator
    margin = z * np.sqrt(win_rate * (1-win_rate) / n + z**2 / (4*n**2)) / denominator

    ci_lower = max(0, center - margin)
    ci_upper = min(1, center + margin)

    return win_rate, ci_lower, ci_upper

def kelly_fraction(win_rate, edge=1.0):
    """
    Kelly Criterion: f = (win_rate - loss_rate) / edge
    For fair bet (edge=1): f = 2*win_rate - 1
    """
    if win_rate <= 0.5:
        return 0
    return 2 * win_rate - 1

# ============================================================================
# Backtest Each Combo
# ============================================================================

results = []

for color, day, category in COMBOS_TO_TEST:
    print(f"\nTesting: {color} × Day {day} ({category})")

    # Build filter conditions
    conditions_filter = "'" + "','".join(CONDITIONS) + "'"
    round_types_filter = "'" + "','".join(ROUND_TYPES) + "'"
    tournament_filter = "'" + "','".join(TOURNAMENT_TYPES) + "'"

    # Training data (2022-2024)
    train_query = f"""
        SELECT vs_avg, off_par, condition, round_type
        FROM analysis
        WHERE
            year IN (2022, 2023, 2024)
            AND color = '{color}'
            AND "Personal Day" = {day}
            AND condition IN ({conditions_filter})
            AND round_type IN ({round_types_filter})
            AND tournament_type IN ({tournament_filter})
            AND vs_avg IS NOT NULL
            AND off_par IS NOT NULL
    """

    train_df = conn.execute(train_query).fetchdf()
    train_win_rate, train_ci_lower, train_ci_upper = calculate_win_rate_ci(
        train_df['vs_avg'].values if len(train_df) > 0 else np.array([])
    )

    # Test data (2025-2026)
    test_query = f"""
        SELECT vs_avg, off_par, condition, round_type
        FROM analysis
        WHERE
            year IN (2025, 2026)
            AND color = '{color}'
            AND "Personal Day" = {day}
            AND condition IN ({conditions_filter})
            AND round_type IN ({round_types_filter})
            AND tournament_type IN ({tournament_filter})
            AND vs_avg IS NOT NULL
            AND off_par IS NOT NULL
    """

    test_df = conn.execute(test_query).fetchdf()
    test_win_rate, test_ci_lower, test_ci_upper = calculate_win_rate_ci(
        test_df['vs_avg'].values if len(test_df) > 0 else np.array([])
    )

    # Fallback: if no 2025-2026 data, use 80/20 holdout
    if len(test_df) == 0:
        all_query = f"""
            SELECT vs_avg, off_par, condition, round_type
            FROM analysis
            WHERE
                color = '{color}'
                AND "Personal Day" = {day}
                AND condition IN ({conditions_filter})
                AND round_type IN ({round_types_filter})
                AND tournament_type IN ({tournament_filter})
                AND vs_avg IS NOT NULL
                AND off_par IS NOT NULL
        """
        all_df = conn.execute(all_query).fetchdf()

        if len(all_df) > 0:
            # 80/20 split
            split_idx = int(len(all_df) * 0.8)
            train_df = all_df.iloc[:split_idx]
            test_df = all_df.iloc[split_idx:]

            train_win_rate, train_ci_lower, train_ci_upper = calculate_win_rate_ci(
                train_df['vs_avg'].values
            )
            test_win_rate, test_ci_lower, test_ci_upper = calculate_win_rate_ci(
                test_df['vs_avg'].values
            )

    # Calculate statistics
    train_n = len(train_df)
    test_n = len(test_df)

    train_mean_vs_avg = train_df['vs_avg'].mean() if train_n > 0 else None
    test_mean_vs_avg = test_df['vs_avg'].mean() if test_n > 0 else None

    variance = None
    if train_win_rate is not None and test_win_rate is not None:
        variance = abs(test_win_rate - train_win_rate)

    edge = None
    if test_win_rate is not None:
        edge = test_win_rate - 0.5

    kelly = None
    if test_win_rate is not None and test_win_rate > 0.51:
        kelly = kelly_fraction(test_win_rate)

    # Format for output
    result = {
        "color": color,
        "personal_day": day,
        "category": category,
        "training_win_rate": train_win_rate,
        "training_ci_lower": train_ci_lower,
        "training_ci_upper": train_ci_upper,
        "training_n": train_n,
        "training_mean_vs_avg": train_mean_vs_avg,
        "testing_win_rate": test_win_rate,
        "testing_ci_lower": test_ci_lower,
        "testing_ci_upper": test_ci_upper,
        "testing_n": test_n,
        "testing_mean_vs_avg": test_mean_vs_avg,
        "variance": variance,
        "edge": edge,
        "kelly_fraction": kelly,
    }

    results.append(result)

    # Print summary
    if train_n > 0:
        print(f"  Training: {train_win_rate*100:.1f}% (n={train_n:,}) [CI: {train_ci_lower*100:.1f}%-{train_ci_upper*100:.1f}%]")
    else:
        print(f"  Training: NO DATA")

    if test_n > 0:
        print(f"  Testing:  {test_win_rate*100:.1f}% (n={test_n:,}) [CI: {test_ci_lower*100:.1f}%-{test_ci_upper*100:.1f}%]")
        if variance is not None:
            print(f"  Variance: {variance*100:.1f}% (match={variance < 0.05})")
        if edge is not None:
            print(f"  Edge:     {edge*100:+.1f}% vs 50% baseline")
        if kelly is not None:
            print(f"  Kelly:    {kelly*100:.1f}%")
    else:
        print(f"  Testing:  NO DATA")

# ============================================================================
# Output
# ============================================================================

results_df = pd.DataFrame(results)

# Summary output
summary_lines = []
summary_lines.append("=" * 100)
summary_lines.append("BACKTEST SUMMARY: Color × Personal Day Combos (Train/Test Split)")
summary_lines.append("=" * 100)
summary_lines.append("")
summary_lines.append(f"Training Set: 2022-2024 (all combos with data)")
summary_lines.append(f"Test Set: 2025-2026 (if unavailable, used 80/20 holdout split)")
summary_lines.append("")
summary_lines.append(f"Filters Applied: {CONDITIONS} × {ROUND_TYPES} × {TOURNAMENT_TYPES}")
summary_lines.append("")
summary_lines.append("-" * 100)
summary_lines.append(f"{'Combo':<30} {'Category':<20} {'Train WR':<15} {'Test WR':<15} {'Variance':<12} {'Edge':<12} {'Kelly':<10}")
summary_lines.append("-" * 100)

for _, row in results_df.iterrows():
    combo = f"{row['color']} × Day {int(row['personal_day'])}"
    cat = row['category']

    train_wr = f"{row['training_win_rate']*100:.1f}% (n={int(row['training_n'])})" if row['training_win_rate'] is not None else "NO DATA"
    test_wr = f"{row['testing_win_rate']*100:.1f}% (n={int(row['testing_n'])})" if row['testing_win_rate'] is not None else "NO DATA"
    var = f"{row['variance']*100:.1f}%" if row['variance'] is not None else "—"
    edge = f"{row['edge']*100:+.1f}%" if row['edge'] is not None else "—"
    kelly = f"{row['kelly_fraction']*100:.1f}%" if row['kelly_fraction'] is not None else "—"

    summary_lines.append(f"{combo:<30} {cat:<20} {train_wr:<15} {test_wr:<15} {var:<12} {edge:<12} {kelly:<10}")

summary_lines.append("-" * 100)
summary_lines.append("")

# Summary stats
valid_results = results_df[results_df['testing_win_rate'].notna()]
if len(valid_results) > 0:
    summary_lines.append(f"Valid Combos (with test data): {len(valid_results)}/{len(results_df)}")
    summary_lines.append(f"Combos with Win Rate > 50%: {len(valid_results[valid_results['testing_win_rate'] > 0.5])}")
    summary_lines.append(f"Mean Test Win Rate: {valid_results['testing_win_rate'].mean()*100:.1f}%")
    summary_lines.append(f"Mean Edge vs Baseline: {valid_results['edge'].mean()*100:+.1f}%")
    summary_lines.append(f"Mean Variance (Train-Test): {valid_results['variance'].mean()*100:.1f}%")
    summary_lines.append("")

summary_text = "\n".join(summary_lines)

try:
    print("\n" + summary_text)
except UnicodeEncodeError:
    # Fallback for encoding issues on Windows
    print("\n[Output saved to backtest_summary.txt]")

# Write to file
with open("d:\\Projects\\luckify-me\\backtest_summary.txt", "w") as f:
    f.write(summary_text)

# Detailed CSV
results_df.to_csv("d:\\Projects\\luckify-me\\backtest_detailed.csv", index=False)

print("\nFiles written:")
print("  - backtest_summary.txt")
print("  - backtest_detailed.csv")

conn.close()
