"""
Test: Shrinkage-Adjusted Formula vs Raw Historical Par

Compare prediction accuracy:
- Raw player_hist_par
- vs Adj_his_par (shrinkage-adjusted)

Metrics: MAE, RMSE, Residual SD, Calibration
"""

import pandas as pd
import numpy as np

print("Loading data...")
# Load both tables
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')
residuals = pd.read_csv('residual_table.csv')

# Merge to get both raw and adjusted predictions plus actual
merged = residuals.merge(
    analysis[['player_id', 'event_id', 'year', 'round_num', 'player_hist_par', 'Adj_his_par', 'Off Par']],
    left_on=['player_id', 'event_id', 'year', 'round_num'],
    right_on=['player_id', 'event_id', 'year', 'round_num'],
    how='inner'
)

# Remove rows with missing values
merged = merged.dropna(subset=['player_hist_par', 'Adj_his_par', 'Off Par', 'actual_vs_par'])

print(f"Total player-rounds for comparison: {len(merged)}")

# Calculate residuals for each method
# actual_vs_par is already in the table
merged['residual_raw'] = merged['actual_vs_par'] - merged['player_hist_par']
merged['residual_shrink'] = merged['actual_vs_par'] - merged['Adj_his_par']

# Metrics
def calculate_metrics(residuals, name):
    """Calculate prediction metrics"""
    mae = np.abs(residuals).mean()
    rmse = np.sqrt((residuals ** 2).mean())
    sd = residuals.std()
    mean_residual = residuals.mean()

    print(f"\n{name}:")
    print(f"  Mean Absolute Error:     {mae:.4f} strokes")
    print(f"  Root Mean Squared Error: {rmse:.4f} strokes")
    print(f"  Residual SD:             {sd:.4f} strokes")
    print(f"  Mean Residual (bias):    {mean_residual:.4f} strokes")

    return {'MAE': mae, 'RMSE': rmse, 'SD': sd, 'Bias': mean_residual}

print("\n=== OVERALL ACCURACY COMPARISON ===")
raw_metrics = calculate_metrics(merged['residual_raw'], "Raw player_hist_par")
shrink_metrics = calculate_metrics(merged['residual_shrink'], "Shrinkage-Adjusted (Adj_his_par)")

# Compare
print("\n=== IMPROVEMENT ===")
print(f"MAE improvement:   {(raw_metrics['MAE'] - shrink_metrics['MAE']) / raw_metrics['MAE'] * 100:+.2f}%")
print(f"RMSE improvement:  {(raw_metrics['RMSE'] - shrink_metrics['RMSE']) / raw_metrics['RMSE'] * 100:+.2f}%")
print(f"SD improvement:    {(raw_metrics['SD'] - shrink_metrics['SD']) / raw_metrics['SD'] * 100:+.2f}%")

# Test by sample size tier (using resid_n from player volatility)
player_vol = pd.read_csv('player_volatility_table.csv')
merged = merged.merge(
    player_vol[['player_id', 'resid_n', 'reliability']],
    on='player_id',
    how='left'
)

print("\n=== BY SAMPLE SIZE TIER ===")
for tier in ['WEAK', 'MEDIUM', 'STRONG']:
    tier_data = merged[merged['reliability'] == tier]
    if len(tier_data) > 0:
        print(f"\n{tier} (N={tier_data['resid_n'].mean():.0f} samples):")
        raw_mae = np.abs(tier_data['residual_raw']).mean()
        shrink_mae = np.abs(tier_data['residual_shrink']).mean()
        improvement = (raw_mae - shrink_mae) / raw_mae * 100
        print(f"  Raw MAE:    {raw_mae:.4f}")
        print(f"  Shrink MAE: {shrink_mae:.4f}")
        print(f"  Improvement: {improvement:+.2f}%")

# Test by condition bucket
print("\n=== BY CONDITION ===")
for condition in merged['condition'].unique():
    if pd.notna(condition):
        cond_data = merged[merged['condition'] == condition]
        raw_mae = np.abs(cond_data['residual_raw']).mean()
        shrink_mae = np.abs(cond_data['residual_shrink']).mean()
        improvement = (raw_mae - shrink_mae) / raw_mae * 100
        print(f"{condition:12} (N={len(cond_data):5}): {improvement:+.2f}% improvement")

# Calibration: do predictions match actual distribution?
print("\n=== CALIBRATION CHECK ===")
raw_mean = merged['player_hist_par'].mean()
shrink_mean = merged['Adj_his_par'].mean()
actual_mean = merged['actual_vs_par'].mean()

print(f"Actual average vs par:        {actual_mean:+.4f}")
print(f"Raw prediction average:       {raw_mean:+.4f} (error: {raw_mean - actual_mean:+.4f})")
print(f"Shrink prediction average:    {shrink_mean:+.4f} (error: {shrink_mean - actual_mean:+.4f})")

# Save detailed comparison
comparison = merged[['player_id', 'player_name', 'event_name', 'year', 'round_num',
                     'player_hist_par', 'Adj_his_par', 'actual_vs_par',
                     'residual_raw', 'residual_shrink', 'reliability']].copy()
comparison['raw_error_abs'] = np.abs(comparison['residual_raw'])
comparison['shrink_error_abs'] = np.abs(comparison['residual_shrink'])
comparison['shrink_wins'] = (comparison['shrink_error_abs'] < comparison['raw_error_abs']).astype(int)

comparison.to_csv('shrinkage_formula_comparison.csv', index=False)
print(f"\nDetailed comparison saved to shrinkage_formula_comparison.csv")

win_rate = comparison['shrink_wins'].mean()
print(f"\nShrinkage formula wins on {win_rate:.1%} of player-rounds")
