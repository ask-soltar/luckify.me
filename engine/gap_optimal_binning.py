#!/usr/bin/env python3
"""
Optimal Non-Symmetric Gap Bucketing using Decision Tree Binning

Finds data-driven bucket boundaries (may be asymmetric) where gap values
with similar predictive power are grouped together.

Compares results to symmetric size-10 bucketing.
"""

import os
import sys
import gspread
import pandas as pd
import numpy as np
import duckdb
from sklearn.tree import DecisionTreeClassifier
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


def analyze_buckets(df, bucket_col, name, min_n=MIN_N):
    """Score bucketing approach."""
    bucketed = df.groupby(bucket_col).agg({
        'diff_course_avg': ['count',
                            lambda x: (x <= GOOD_THRESHOLD).sum() / len(x) * 100,
                            lambda x: (x >= BAD_THRESHOLD).sum() / len(x) * 100]
    }).round(1)

    bucketed.columns = ['n', 'good_pct', 'bad_pct']
    bucketed = bucketed[bucketed['n'] >= min_n]

    if bucketed.empty:
        return None

    n_buckets = len(bucketed)
    avg_good = bucketed['good_pct'].mean()
    std_good = bucketed['good_pct'].std()

    # Calculate population baseline
    pop_good = (df['diff_course_avg'] <= GOOD_THRESHOLD).sum() / len(df) * 100

    # Count actionable edges
    bucketed['edge'] = bucketed['good_pct'] - pop_good
    actionable = len(bucketed[(bucketed['edge'] > 5) | (bucketed['edge'] < -5)])

    return {
        'name': name,
        'n_buckets': n_buckets,
        'avg_good_pct': avg_good,
        'std_good_pct': std_good,
        'actionable_edges': actionable,
        'action_pct': 100 * actionable / n_buckets if n_buckets > 0 else 0,
        'buckets': bucketed
    }


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
    df["gap"] = pd.to_numeric(df["gap"], errors="coerce")

    # Filter to valid data
    df = df[df["diff_course_avg"].notna() & df["gap"].notna()].copy()
    print(f"  {len(df)} rows with valid gap and diff_course_avg")

    # Create target variable
    df["is_good"] = (df["diff_course_avg"] <= GOOD_THRESHOLD).astype(int)

    print(f"\n  Gap range: {df['gap'].min():.0f} to {df['gap'].max():.0f}")
    print(f"  Baseline good%: {df['is_good'].mean() * 100:.1f}%")

    # ========================================================================
    # APPROACH 1: Fine bucketing (size 5) to see distribution
    # ========================================================================
    print("\n" + "="*75)
    print("APPROACH 1: FINE BUCKETING (Size 5)")
    print("="*75)

    df['bucket_size5'] = df['gap'].apply(
        lambda x: int(x / 5) * 5 if x >= 0 else -int(abs(x) / 5) * 5
    )

    result_5 = analyze_buckets(df, 'bucket_size5', 'Size 5')
    if result_5:
        print(f"Buckets: {result_5['n_buckets']}")
        print(f"Actionable edges: {result_5['actionable_edges']} ({result_5['action_pct']:.1f}%)")
        print(f"Avg good%: {result_5['avg_good_pct']:.2f}%, std: {result_5['std_good_pct']:.2f}%")

    # ========================================================================
    # APPROACH 2: Symmetric bucketing (size 10) baseline
    # ========================================================================
    print("\n" + "="*75)
    print("APPROACH 2: SYMMETRIC BUCKETING (Size 10) — BASELINE")
    print("="*75)

    df['bucket_size10'] = df['gap'].apply(
        lambda x: int(x / 10) * 10 if x >= 0 else -int(abs(x) / 10) * 10
    )

    result_10 = analyze_buckets(df, 'bucket_size10', 'Size 10')
    if result_10:
        print(f"Buckets: {result_10['n_buckets']}")
        print(f"Actionable edges: {result_10['actionable_edges']} ({result_10['action_pct']:.1f}%)")
        print(f"Avg good%: {result_10['avg_good_pct']:.2f}%, std: {result_10['std_good_pct']:.2f}%")

    # ========================================================================
    # APPROACH 3: Decision Tree Binning (optimal non-symmetric)
    # ========================================================================
    print("\n" + "="*75)
    print("APPROACH 3: DECISION TREE BINNING (Optimal Non-Symmetric)")
    print("="*75)

    # Train decision tree to find optimal splits
    X = df[['gap']].values
    y = df['is_good'].values

    # Limit depth to find reasonable number of buckets
    tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=int(len(df) * 0.01), random_state=42)
    tree.fit(X, y)

    # Extract split thresholds
    def get_leaves(tree, feature_names=['gap']):
        tree_ = tree.tree_
        feature_name = [feature_names[i] if i != -2 else "undefined!" for i in tree_.feature]

        paths = []
        def recurse(node, path):
            if tree_.feature[node] != -2:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                # Left child (<=)
                recurse(tree_.children_left[node], path + [f"{name} <= {threshold:.1f}"])
                # Right child (>)
                recurse(tree_.children_right[node], path + [f"{name} > {threshold:.1f}"])
            else:
                paths.append(path)

        recurse(0, [])
        return paths

    thresholds = sorted(set(tree.tree_.threshold[tree.tree_.threshold != -2]))
    print(f"Optimal split points: {[f'{t:.1f}' for t in thresholds]}")

    # Create buckets from thresholds
    bins = [-100] + list(thresholds) + [100]
    df['bucket_optimal'] = pd.cut(df['gap'], bins=bins, labels=False)

    result_opt = analyze_buckets(df, 'bucket_optimal', 'Optimal')
    if result_opt:
        print(f"Buckets: {result_opt['n_buckets']}")
        print(f"Actionable edges: {result_opt['actionable_edges']} ({result_opt['action_pct']:.1f}%)")
        print(f"Avg good%: {result_opt['avg_good_pct']:.2f}%, std: {result_opt['std_good_pct']:.2f}%")

    # ========================================================================
    # COMPARISON
    # ========================================================================
    print("\n" + "="*75)
    print("COMPARISON: Which bucketing is best?")
    print("="*75)
    print(f"{'Approach':<30} {'Buckets':>8} {'Action%':>10} {'Std Dev':>10}")
    print("-"*75)

    for result in [result_5, result_10, result_opt]:
        if result:
            print(f"{result['name']:<30} {result['n_buckets']:>8} {result['action_pct']:>9.1f}% {result['std_good_pct']:>10.2f}%")

    # Save detailed results
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if result_opt and result_opt['buckets'] is not None:
        result_opt['buckets'].to_csv(os.path.join(OUTPUT_DIR, "gap_optimal_buckets.csv"))

        # Show bucket boundaries
        print(f"\nOptimal bucket boundaries:")
        bounds = [-100] + list(thresholds) + [100]
        for i in range(len(bounds) - 1):
            print(f"  Bucket {i}: {bounds[i]:.0f} to {bounds[i+1]:.0f}")

        print(f"\nResults saved to {OUTPUT_DIR}/gap_optimal_buckets.csv")

    # Recommendation
    print("\n" + "="*75)
    print("RECOMMENDATION")
    print("="*75)

    if result_opt and result_10:
        if result_opt['action_pct'] > result_10['action_pct'] + 5:
            print("✓ Use OPTIMAL (asymmetric) bucketing — significantly better action%")
        elif result_opt['std_good_pct'] < result_10['std_good_pct'] - 0.5:
            print("✓ Use OPTIMAL (asymmetric) bucketing — more stable")
        else:
            print("✓ Stick with SYMMETRIC (size 10) bucketing — simpler, comparable performance")


if __name__ == "__main__":
    main()
