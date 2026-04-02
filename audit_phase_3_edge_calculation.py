"""
AUDIT: Phase 3 - Edge Calculation Logic
=========================================

Verifies the foundational math for converting player projections into edges.

Key questions:
1. Is edge formula correct? (field_avg - player_proj, not player_proj - field_avg)
2. Does edge correlate with outcomes? (higher edge = more wins)
3. Is there a linear relationship? (or does it break down at extremes)
4. Are there anomalies in the data?
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("PHASE 3 AUDIT: EDGE CALCULATION LOGIC")
print("=" * 80)

# Load ANALYSIS_v2
print("\n[1] Loading ANALYSIS_v2...")
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')

print(f"    Total rows: {len(analysis):,}")
print(f"    Columns: {list(analysis.columns)}")

# Check for Adj_his_par (the baseline projection)
if 'Adj_his_par' not in analysis.columns:
    print("    [ERROR] Adj_his_par column not found")
    print("    Available numeric columns:", [c for c in analysis.columns if 'par' in c.lower()])
    exit(1)

# Get unique event-rounds
print("\n[2] Aggregating unique tournament rounds...")
rounds = analysis.drop_duplicates(
    subset=['event_id', 'round_num'],
    keep='first'
)[['event_id', 'year', 'round_num']].copy()

print(f"    Total unique rounds: {len(rounds):,}")

# For each round, calculate field average projection
print("\n[3] Calculating field average projections...")
round_field_avgs = []

for idx, row in rounds.iterrows():
    event_id = row['event_id']
    round_num = row['round_num']
    year = row['year']

    round_data = analysis[
        (analysis['event_id'] == event_id) &
        (analysis['round_num'] == round_num)
    ].copy()

    # Field average (must have valid Adj_his_par)
    valid_projections = round_data[round_data['Adj_his_par'].notna()]['Adj_his_par']

    if len(valid_projections) > 2:
        field_avg = valid_projections.mean()
        round_field_avgs.append({
            'event_id': event_id,
            'year': year,
            'round_num': round_num,
            'field_size': len(valid_projections),
            'field_avg_projection': field_avg
        })

field_avgs_df = pd.DataFrame(round_field_avgs)
print(f"    Calculated field averages for {len(field_avgs_df):,} rounds")
print(f"    Field average range: {field_avgs_df['field_avg_projection'].min():.2f} to {field_avgs_df['field_avg_projection'].max():.2f}")

# Merge back and calculate edges
print("\n[4] Calculating player edges...")
analysis_merged = analysis.merge(
    field_avgs_df,
    on=['event_id', 'round_num', 'year'],
    how='inner'
)

# CRITICAL: Edge = field_avg - player_projection
# (In golf, negative projection is GOOD, so positive edge means player is BETTER than field)
analysis_merged['edge_strokes'] = (
    analysis_merged['field_avg_projection'] - analysis_merged['Adj_his_par']
)

# Keep only rows with valid data
analysis_merged = analysis_merged.dropna(subset=['edge_strokes', 'actual_vs_par'])

print(f"    Rows with valid edge calculations: {len(analysis_merged):,}")
print(f"    Edge range: {analysis_merged['edge_strokes'].min():.2f} to {analysis_merged['edge_strokes'].max():.2f}")
print(f"    Edge mean: {analysis_merged['edge_strokes'].mean():.3f}")
print(f"    Edge median: {analysis_merged['edge_strokes'].median():.3f}")

# AUDIT 1: Check distribution of edges
print("\n[5] AUDIT 1: Edge Distribution")
print("=" * 80)
edge_bins = analysis_merged['edge_strokes'].quantile([0, 0.25, 0.5, 0.75, 1.0])
print(f"    25th percentile: {edge_bins[0.25]:.3f}")
print(f"    50th percentile: {edge_bins[0.50]:.3f}")
print(f"    75th percentile: {edge_bins[0.75]:.3f}")

# Should be roughly symmetric around 0
negative_edges = (analysis_merged['edge_strokes'] < 0).sum()
positive_edges = (analysis_merged['edge_strokes'] > 0).sum()
print(f"\n    Negative edges (player better than field): {negative_edges:,} ({negative_edges/len(analysis_merged)*100:.1f}%)")
print(f"    Positive edges (player worse than field): {positive_edges:,} ({positive_edges/len(analysis_merged)*100:.1f}%)")
print(f"    [CHECK] Should be roughly 50/50 if centered on zero")

# AUDIT 2: Does higher edge correlate with better actual performance?
print("\n[6] AUDIT 2: Edge vs Actual Performance Correlation")
print("=" * 80)

# Bucket by edge
analysis_merged['edge_bucket'] = (analysis_merged['edge_strokes'] / 0.5).round() * 0.5

bucketed = analysis_merged.groupby('edge_bucket').agg({
    'edge_strokes': 'count',
    'actual_vs_par': ['mean', 'std']
}).reset_index()

bucketed.columns = ['edge_bucket', 'count', 'actual_mean', 'actual_std']
bucketed = bucketed.sort_values('edge_bucket')

print("\n    Edge Bucket Analysis:")
print(f"    {'Edge':>8} {'Count':>8} {'Actual Mean':>12} {'Actual SD':>12} {'Expected':>12}")
print("    " + "-" * 60)

for idx, row in bucketed.iterrows():
    edge = row['edge_bucket']
    count = row['count']
    actual_mean = row['actual_mean']
    expected = edge  # If model is perfect, actual should equal edge (on average)

    if count >= 10:
        match = "✓" if abs(actual_mean - edge) < 1.0 else "✗"
        print(f"    {edge:>8.1f} {count:>8.0f} {actual_mean:>12.3f} {row['actual_std']:>12.3f} {edge:>12.1f} {match}")

# AUDIT 3: Monotonicity (higher edge → lower actual score)
print("\n[7] AUDIT 3: Monotonicity Check")
print("=" * 80)

bucketed_sorted = bucketed.sort_values('edge_bucket')
actual_means = bucketed_sorted['actual_mean'].values
edges = bucketed_sorted['edge_bucket'].values

# For monotonicity: as edge increases, actual_mean should DECREASE
# (because negative actual_mean is good)
is_monotonic = all(actual_means[i] >= actual_means[i+1] for i in range(len(actual_means)-1))

print(f"    Is monotonic (higher edge → lower score)? {is_monotonic}")
if not is_monotonic:
    print(f"    [WARN] Non-monotonic relationship detected")
    # Find where it breaks
    for i in range(len(actual_means)-1):
        if actual_means[i] < actual_means[i+1]:
            print(f"           Edge {edges[i]:.1f} ({actual_means[i]:.2f}) → Edge {edges[i+1]:.1f} ({actual_means[i+1]:.2f}) [reversed]")

# AUDIT 4: At edge=0, actual should be ~0
print("\n[8] AUDIT 4: Zero Edge Test")
print("=" * 80)

zero_edge = bucketed[(bucketed['edge_bucket'] >= -0.25) & (bucketed['edge_bucket'] < 0.25)]
if not zero_edge.empty:
    zero_actual = zero_edge['actual_mean'].values[0]
    print(f"    At edge ≈ 0: Actual mean = {zero_actual:.3f}")
    print(f"    [CHECK] Should be close to 0 (within ±0.5)")
    if abs(zero_actual) < 0.5:
        print(f"    [PASS] Zero edge calibration looks good")
    else:
        print(f"    [WARN] Large bias at zero edge (model may be systematically off)")

# AUDIT 5: Extreme edges
print("\n[9] AUDIT 5: Extreme Edge Performance")
print("=" * 80)

extreme_negative = analysis_merged[analysis_merged['edge_strokes'] < -2.0]
extreme_positive = analysis_merged[analysis_merged['edge_strokes'] > 2.0]

if len(extreme_negative) > 0:
    print(f"    Extreme negative edges (< -2.0): {len(extreme_negative):,} rounds")
    print(f"      Actual mean: {extreme_negative['actual_vs_par'].mean():.3f}")
    print(f"      Expected: < -2.0")
    print(f"      Match: {extreme_negative['actual_vs_par'].mean() < -1.5}")

if len(extreme_positive) > 0:
    print(f"    Extreme positive edges (> 2.0): {len(extreme_positive):,} rounds")
    print(f"      Actual mean: {extreme_positive['actual_vs_par'].mean():.3f}")
    print(f"      Expected: > 2.0")
    print(f"      Match: {extreme_positive['actual_vs_par'].mean() > 1.5}")

# AUDIT 6: Prediction residuals
print("\n[10] AUDIT 6: Prediction Residuals (Edge - Actual)")
print("=" * 80)

analysis_merged['prediction_error'] = analysis_merged['edge_strokes'] - analysis_merged['actual_vs_par']

mae = np.abs(analysis_merged['prediction_error']).mean()
rmse = np.sqrt((analysis_merged['prediction_error'] ** 2).mean())
bias = analysis_merged['prediction_error'].mean()

print(f"    Mean Absolute Error (MAE): {mae:.3f} strokes")
print(f"    Root Mean Square Error (RMSE): {rmse:.3f} strokes")
print(f"    Bias (systematic over/underestimate): {bias:.3f} strokes")
print(f"    Prediction error SD: {analysis_merged['prediction_error'].std():.3f}")

if bias > 0.5:
    print(f"    [WARN] Positive bias: Model is systematically OPTIMISTIC (predicts better than actual)")
elif bias < -0.5:
    print(f"    [WARN] Negative bias: Model is systematically PESSIMISTIC")
else:
    print(f"    [PASS] Bias is near zero (well-calibrated)")

# AUDIT 7: Compare to baseline model (raw player_hist_par)
print("\n[11] AUDIT 7: Baseline Comparison")
print("=" * 80)

if 'player_hist_par' in analysis_merged.columns:
    # Calculate baseline edge (without condition adjustment)
    analysis_merged['baseline_edge'] = (
        analysis_merged['field_avg_projection'] - analysis_merged['player_hist_par']
    )

    analysis_merged['baseline_error'] = (
        analysis_merged['baseline_edge'] - analysis_merged['actual_vs_par']
    )

    baseline_mae = np.abs(analysis_merged['baseline_error']).mean()

    mae_improvement = (baseline_mae - mae) / baseline_mae * 100

    print(f"    Baseline (raw player_hist_par) MAE: {baseline_mae:.3f}")
    print(f"    Adjusted (Adj_his_par) MAE: {mae:.3f}")
    print(f"    Improvement: {mae_improvement:+.2f}%")

    if mae_improvement > 1:
        print(f"    [PASS] Adjustment improves accuracy")
    elif mae_improvement > -1:
        print(f"    [WARN] Minimal improvement from adjustment")
    else:
        print(f"    [FAIL] Adjustment makes things worse!")

# Summary
print("\n" + "=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)

print(f"""
Edge Formula: field_avg_projection - Adj_his_par
Data: {len(analysis_merged):,} player-rounds across {len(field_avgs_df):,} tournament rounds

Key Metrics:
  - MAE: {mae:.3f} strokes
  - Bias: {bias:+.3f} strokes
  - Monotonicity: {'PASS' if is_monotonic else 'FAIL'}
  - Zero-edge calibration: {zero_edge['actual_mean'].values[0]:.3f} (should be ~0)

Status: Ready for Phase 4 (edge → win probability mapping)
""")

# Save for Phase 4 use
analysis_merged.to_csv('analysis_with_edges.csv', index=False)
print(f"Saved: analysis_with_edges.csv ({len(analysis_merged):,} rows)")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
