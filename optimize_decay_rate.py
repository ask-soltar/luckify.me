"""
Optimization Test: Find Optimal Exponential Decay Rate

Train on 2022-2024 data (establish baseline + recent form)
Test on 2025-2026 data (predict vs actual)
Compare decay rates: 10, 15, 20, 25, 30, 40, 50, 75, 100
Find which minimizes prediction error (MAE)
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("DECAY RATE OPTIMIZATION TEST")
print("Train: 2022-2024 | Test: 2025-2026")
print("=" * 80)

# Load recent form data
print("\n[1] Loading recent form data...")
df = pd.read_csv('exponential_decay_recent_form.csv')

print(f"    Total records: {len(df):,}")
print(f"    Year range: {df['year'].min()}-{df['year'].max()}")

# Add player volatility tier
print("\n[2] Adding player sample quality tier...")
player_vol = pd.read_csv('player_volatility_table.csv')
df = df.merge(player_vol[['player_id', 'reliability', 'resid_n']], on='player_id', how='left')

print(f"    Merged with reliability tiers")

# Split data: train 2022-2024, test 2025-2026
print("\n[3] Splitting data...")
df['is_test_period'] = df['year'].isin([2025, 2026])

train = df[~df['is_test_period']].copy()
test = df[df['is_test_period']].copy()

print(f"    Train (2022-2024): {len(train):,} records")
print(f"    Test (2025-2026): {len(test):,} records")

# For each decay rate, blend baseline + recent form and measure error
print("\n[4] Testing decay rates...")

test_decay_rates = [10, 15, 20, 25, 30, 40, 50, 75, 100]
results = []

for decay_rate in test_decay_rates:
    print(f"\n    Testing decay_rate = {decay_rate}...")

    # Calculate blend: baseline (Off Par from train) + recent form
    # For test data, use most recent recent_form value
    test_copy = test.copy()

    # Use recent_form from decay_rate (if available)
    form_col = f'recent_form_decay_{decay_rate}'
    if form_col not in test_copy.columns:
        # If specific decay rate not calculated, use nearest one
        if decay_rate <= 20:
            form_col = 'recent_form_decay_20'
        else:
            form_col = 'recent_form_decay_50'

    # Calculate blended projection: 70% baseline (historical), 30% recent form
    test_copy['baseline_vs_par'] = train.groupby('player_id')['Off Par'].mean().reindex(test_copy['player_id']).values

    # Fill NaN recent form with baseline
    test_copy[form_col] = test_copy[form_col].fillna(test_copy['baseline_vs_par'])

    test_copy['projected_vs_par_blended'] = (
        0.70 * test_copy['baseline_vs_par'] +
        0.30 * test_copy[form_col]
    )

    # Calculate residuals
    test_copy['residual'] = test_copy['Off Par'] - test_copy['projected_vs_par_blended']

    # Metrics
    mae = np.abs(test_copy['residual']).mean()
    rmse = np.sqrt((test_copy['residual'] ** 2).mean())
    std = test_copy['residual'].std()
    mean_residual = test_copy['residual'].mean()

    results.append({
        'decay_rate': decay_rate,
        'mae': mae,
        'rmse': rmse,
        'std': std,
        'bias': mean_residual,
        'n_samples': len(test_copy)
    })

    print(f"      MAE: {mae:.4f} | RMSE: {rmse:.4f} | Bias: {mean_residual:.4f}")

results_df = pd.DataFrame(results)

# Find optimal
print("\n[5] RESULTS SUMMARY...")
print("\n" + results_df.to_string(index=False))

best_idx = results_df['mae'].idxmin()
best_rate = results_df.loc[best_idx, 'decay_rate']
best_mae = results_df.loc[best_idx, 'mae']

print(f"\n    OPTIMAL DECAY RATE: {best_rate:.0f}")
print(f"    Best MAE: {best_mae:.4f}")

# Test by sample quality tier
print("\n[6] GAME THEORY: OPTIMAL RATE BY SAMPLE QUALITY...")

test_with_form = test.copy()
form_col_best = f'recent_form_decay_{int(best_rate)}'
if form_col_best not in test_with_form.columns:
    form_col_best = 'recent_form_decay_50'

test_with_form['baseline'] = train.groupby('player_id')['Off Par'].mean().reindex(test_with_form['player_id']).values
test_with_form[form_col_best] = test_with_form[form_col_best].fillna(test_with_form['baseline'])
test_with_form['projected'] = (0.70 * test_with_form['baseline'] + 0.30 * test_with_form[form_col_best])
test_with_form['residual'] = test_with_form['Off Par'] - test_with_form['projected']

for tier in ['WEAK', 'MEDIUM', 'STRONG']:
    tier_data = test_with_form[test_with_form['reliability'] == tier]
    if len(tier_data) > 0:
        mae = np.abs(tier_data['residual']).mean()
        rmse = np.sqrt((tier_data['residual'] ** 2).mean())
        print(f"\n    {tier} (N={tier_data['resid_n'].mean():.0f}):")
        print(f"      MAE: {mae:.4f} | RMSE: {rmse:.4f}")

# Save results
results_df.to_csv('decay_rate_optimization_results.csv', index=False)

print("\n[7] Files saved:")
print(f"    decay_rate_optimization_results.csv")

print("\n" + "=" * 80)
print("OPTIMIZATION COMPLETE")
print("=" * 80)
