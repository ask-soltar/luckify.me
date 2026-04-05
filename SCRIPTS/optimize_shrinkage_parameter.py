"""
Optimize Shrinkage Parameter

Test different shrinkage multipliers (currently using 12):
(player_hist_par * N + condition_avg * shrinkage_param) / (N + shrinkage_param)

Find which parameter minimizes prediction error (MAE).
"""

import pandas as pd
import numpy as np

print("Loading data...")
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')
residuals = pd.read_csv('residual_table.csv')

# Merge to get actual outcomes
merged = residuals.merge(
    analysis[['player_id', 'event_id', 'year', 'round_num', 'player_hist_par', 'player_his_cnt']],
    left_on=['player_id', 'event_id', 'year', 'round_num'],
    right_on=['player_id', 'event_id', 'year', 'round_num'],
    how='inner'
)

merged = merged.dropna(subset=['player_hist_par', 'player_his_cnt', 'actual_vs_par', 'condition'])
print(f"Total player-rounds: {len(merged)}")

# Calculate condition averages (for each condition)
condition_avgs = analysis.groupby('condition')['player_hist_par'].mean()
print(f"\nCondition averages:")
print(condition_avgs)

# Map condition averages to our merged data
merged['condition_avg'] = merged['condition'].map(condition_avgs)
merged = merged.dropna(subset=['condition_avg'])

# Test different shrinkage parameters
test_params = [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50]
results = []

print(f"\n=== TESTING SHRINKAGE PARAMETERS ===")
print(f"{'Param':>6} {'MAE':>8} {'RMSE':>8} {'Bias':>8} {'SD':>8}")
print("-" * 40)

for param in test_params:
    # Recalculate adjusted prediction with this parameter
    merged['adj_pred'] = (merged['player_hist_par'] * merged['player_his_cnt'] +
                          merged['condition_avg'] * param) / (merged['player_his_cnt'] + param)

    # Calculate residuals
    merged['residual'] = merged['actual_vs_par'] - merged['adj_pred']

    # Metrics
    mae = np.abs(merged['residual']).mean()
    rmse = np.sqrt((merged['residual'] ** 2).mean())
    bias = merged['residual'].mean()
    sd = merged['residual'].std()

    results.append({
        'param': param,
        'MAE': mae,
        'RMSE': rmse,
        'Bias': bias,
        'SD': sd
    })

    print(f"{param:6.0f} {mae:8.4f} {rmse:8.4f} {bias:8.4f} {sd:8.4f}")

results_df = pd.DataFrame(results)

# Find optimal
best_mae_idx = results_df['MAE'].idxmin()
best_rmse_idx = results_df['RMSE'].idxmin()
best_param_mae = results_df.loc[best_mae_idx, 'param']
best_param_rmse = results_df.loc[best_rmse_idx, 'param']

print("\n=== OPTIMAL PARAMETERS ===")
print(f"Best MAE:  parameter = {best_param_mae:.0f} (MAE = {results_df.loc[best_mae_idx, 'MAE']:.4f})")
print(f"Best RMSE: parameter = {best_param_rmse:.0f} (RMSE = {results_df.loc[best_rmse_idx, 'RMSE']:.4f})")
print(f"Current:   parameter = 12 (MAE = {results_df[results_df['param']==12]['MAE'].values[0]:.4f})")

# By sample size tier
print("\n=== BEST PARAMETER BY SAMPLE SIZE TIER ===")

# Load player volatility to get tiers
player_vol = pd.read_csv('player_volatility_table.csv')
merged = merged.merge(player_vol[['player_id', 'reliability']], on='player_id', how='left')

for tier in ['WEAK', 'MEDIUM', 'STRONG']:
    tier_data = merged[merged['reliability'] == tier]
    if len(tier_data) > 0:
        print(f"\n{tier}:")
        best_mae = 999
        best_p = 0
        for param in test_params:
            tier_data_copy = tier_data.copy()
            tier_data_copy['adj_pred'] = (tier_data_copy['player_hist_par'] * tier_data_copy['player_his_cnt'] +
                                          tier_data_copy['condition_avg'] * param) / (tier_data_copy['player_his_cnt'] + param)
            tier_data_copy['residual'] = tier_data_copy['actual_vs_par'] - tier_data_copy['adj_pred']
            mae = np.abs(tier_data_copy['residual']).mean()
            if mae < best_mae:
                best_mae = mae
                best_p = param
        print(f"  Best parameter: {best_p:.0f} (MAE = {best_mae:.4f})")

# Visualization
print("\n=== MAE TREND ===")
for idx, row in results_df.iterrows():
    print(f"{int(row['param']):3.0f}: MAE = {row['MAE']:.4f}")

# Save results
results_df.to_csv('shrinkage_parameter_optimization.csv', index=False)
print(f"\nResults saved to shrinkage_parameter_optimization.csv")
