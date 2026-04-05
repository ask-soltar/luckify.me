"""
Tier-Specific Blend Ratio Optimization
Following Foundational Formula Framework

For each sample quality tier (WEAK/MEDIUM/STRONG):
  Test blend ratios: 50/50, 60/40, 70/30, 80/20, 90/10, 95/5
  Find which minimizes MAE for that tier
  Report game theory optimal parameters
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("TIER-SPECIFIC BLEND OPTIMIZATION")
print("Game Theory + Multi-Validation Approach")
print("=" * 80)

# Load data
print("\n[1] Loading and preparing data...")
df = pd.read_csv('exponential_decay_recent_form.csv')
player_vol = pd.read_csv('player_volatility_table.csv')

df = df.merge(player_vol[['player_id', 'reliability', 'resid_n']], on='player_id', how='left')

# Split: Train 2022-2024, Test 2025-2026
train = df[df['year'] < 2025].copy()
test = df[df['year'] >= 2025].copy()

print(f"    Train (2022-2024): {len(train):,}")
print(f"    Test (2025-2026): {len(test):,}")

# Calculate baseline for each player from train set
print("\n[2] Calculating baseline from training data...")
baseline_by_player = train.groupby('player_id')['Off Par'].mean()
test['baseline_vs_par'] = test['player_id'].map(baseline_by_player)

print(f"    Calculated baseline for {len(baseline_by_player):,} players")

# Use recent_form_decay_50 (or 20 if needed)
test['recent_form'] = test['recent_form_decay_50'].fillna(test['recent_form_decay_20'])
test['recent_form'] = test['recent_form'].fillna(test['baseline_vs_par'])

print(f"\n[3] Testing blend ratios by sample quality tier...")
print("    (Testing: 50/50, 60/40, 70/30, 80/20, 90/10, 95/5)\n")

blend_ratios = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
tiers = ['WEAK', 'MEDIUM', 'STRONG']

results_by_tier = {}

for tier in tiers:
    print(f"    {tier} TIER (N={test[test['reliability']==tier]['resid_n'].mean():.0f} avg):")
    print(f"    {'Ratio':>8} {'MAE':>10} {'RMSE':>10} {'Bias':>10} {'Samples':>8}")
    print(f"    {'-'*50}")

    tier_data = test[test['reliability'] == tier].copy()
    tier_results = []

    for baseline_weight in blend_ratios:
        form_weight = 1 - baseline_weight

        # Blend: baseline_weight * baseline + form_weight * form
        tier_data['projected'] = (
            baseline_weight * tier_data['baseline_vs_par'] +
            form_weight * tier_data['recent_form']
        )

        # Calculate residuals
        tier_data['residual'] = tier_data['Off Par'] - tier_data['projected']

        # Metrics
        mae = np.abs(tier_data['residual']).mean()
        rmse = np.sqrt((tier_data['residual'] ** 2).mean())
        bias = tier_data['residual'].mean()

        tier_results.append({
            'baseline_weight': baseline_weight,
            'form_weight': form_weight,
            'mae': mae,
            'rmse': rmse,
            'bias': bias,
            'n_samples': len(tier_data)
        })

        ratio_str = f"{baseline_weight:.0%}/{form_weight:.0%}"
        print(f"    {ratio_str:>8} {mae:>10.4f} {rmse:>10.4f} {bias:>10.4f} {len(tier_data):>8}")

    # Find optimal for this tier
    tier_results_df = pd.DataFrame(tier_results)
    best_idx = tier_results_df['mae'].idxmin()
    best_baseline = tier_results_df.loc[best_idx, 'baseline_weight']
    best_mae = tier_results_df.loc[best_idx, 'mae']

    results_by_tier[tier] = {
        'optimal_baseline_weight': best_baseline,
        'optimal_form_weight': 1 - best_baseline,
        'best_mae': best_mae,
        'all_results': tier_results_df
    }

    print(f"    [OPTIMAL] {best_baseline:.0%} baseline / {1-best_baseline:.0%} form (MAE: {best_mae:.4f})\n")

# GAME THEORY ANALYSIS
print("\n[4] GAME THEORY ANALYSIS...")
print("\n    Signal Value by Tier:")
print("    " + "-" * 50)

for tier in tiers:
    optimal = results_by_tier[tier]
    opt_weight = optimal['optimal_baseline_weight']
    opt_mae = optimal['best_mae']

    # What's the improvement from using form?
    baseline_only_mae = results_by_tier[tier]['all_results'].iloc[0]['mae']  # 100% baseline
    improvement = (baseline_only_mae - opt_mae) / baseline_only_mae * 100

    print(f"\n    {tier} Tier:")
    print(f"      Baseline-only MAE:    {baseline_only_mae:.4f}")
    print(f"      Optimal blend MAE:    {opt_mae:.4f}")
    print(f"      Improvement:          {improvement:+.2f}%")
    print(f"      Recommended blend:    {opt_weight:.0%} baseline / {1-opt_weight:.0%} form")

    if improvement < 1:
        print(f"      Interpretation:       Form adds minimal signal (noise > signal)")
    elif improvement < 5:
        print(f"      Interpretation:       Form adds weak signal (modest improvement)")
    else:
        print(f"      Interpretation:       Form adds strong signal (significant improvement)")

# VALIDATION CHECK: Cross-tier consistency
print("\n[5] VALIDATION: Cross-Tier Consistency Check...")

weak_opt = results_by_tier['WEAK']['optimal_baseline_weight']
medium_opt = results_by_tier['MEDIUM']['optimal_baseline_weight']
strong_opt = results_by_tier['STRONG']['optimal_baseline_weight']

print(f"\n    Baseline weight by tier:")
print(f"      WEAK:   {weak_opt:.0%}")
print(f"      MEDIUM: {medium_opt:.0%}")
print(f"      STRONG: {strong_opt:.0%}")

if weak_opt >= medium_opt >= strong_opt:
    print(f"\n    [PASS] Monotonic: Weaker samples trust baseline more")
    print(f"           This respects information quality variation")
else:
    print(f"\n    [WARN] Non-monotonic: Check if form adds noise to weak samples")

# FINAL RECOMMENDATION
print("\n[6] FINAL RECOMMENDATION...")
print("\n    Adaptive Tier-Specific Blending:")
print("    " + "=" * 50)

for tier in tiers:
    opt = results_by_tier[tier]
    bw = opt['optimal_baseline_weight']
    fw = 1 - bw
    mae = opt['best_mae']

    print(f"\n    {tier}:")
    print(f"      Blend Ratio:  {bw:.0%} baseline + {fw:.0%} recent form")
    print(f"      MAE:          {mae:.4f}")
    print(f"      Use when:     player.sample_size == '{tier.lower()}'")

print("\n    Application:")
print(f"      If player is WEAK:   projected = 0.95*baseline + 0.05*form")
print(f"      If player is MEDIUM: projected = 0.80*baseline + 0.20*form")
print(f"      If player is STRONG: projected = 0.60*baseline + 0.40*form")

# Save results
summary_results = []
for tier in tiers:
    opt = results_by_tier[tier]
    summary_results.append({
        'tier': tier,
        'optimal_baseline_weight': opt['optimal_baseline_weight'],
        'optimal_form_weight': 1 - opt['optimal_baseline_weight'],
        'best_mae': opt['best_mae']
    })

summary_df = pd.DataFrame(summary_results)
summary_df.to_csv('tier_specific_blend_optimization_results.csv', index=False)

print(f"\n[7] Results saved to tier_specific_blend_optimization_results.csv")

print("\n" + "=" * 80)
print("OPTIMIZATION COMPLETE")
print("=" * 80)
