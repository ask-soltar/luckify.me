#!/usr/bin/env python3
"""
Test different thresholds specifically for Moderate conditions.
"""

import pandas as pd

# Load scored data
df = pd.read_csv('2ball_scored_35_65.csv')

# Filter for graded only (no pushes)
graded = df[df['actual_winner'] != 'Push'].copy()

# Separate by condition
moderate = graded[graded['condition'] == 'Moderate'].copy()
calm = graded[graded['condition'] == 'Calm'].copy()

print("="*70)
print("THRESHOLD TESTING BY CONDITION")
print("="*70)

thresholds = [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 10.0]

print("\n" + "MODERATE CONDITIONS".center(70))
print("-"*70)
print(f"{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Loss Rate':>10}")
print("-"*70)

moderate_results = []

for threshold in thresholds:
    filtered = moderate[moderate['difference'] >= threshold].copy()

    if len(filtered) > 0:
        wins = len(filtered[filtered['correct'] == True])
        losses = len(filtered) - wins
        loss_rate = (losses / len(filtered)) * 100
        win_rate = 100 - loss_rate

        moderate_results.append({
            'threshold': threshold,
            'qualified': len(filtered),
            'wins': wins,
            'win_rate': win_rate,
            'loss_rate': loss_rate
        })

        print(f"    >= {threshold:5.1f}   {len(filtered):10.0f} {wins:6.0f} {loss_rate:9.1f}%")

# CALM CONDITIONS for comparison
print("\n" + "CALM CONDITIONS (for comparison)".center(70))
print("-"*70)
print(f"{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

calm_results = []

for threshold in thresholds:
    filtered = calm[calm['difference'] >= threshold].copy()

    if len(filtered) > 0:
        wins = len(filtered[filtered['correct'] == True])
        loss_rate = (len(filtered) - wins) / len(filtered) * 100
        win_rate = 100 - loss_rate

        calm_results.append({
            'threshold': threshold,
            'qualified': len(filtered),
            'wins': wins,
            'win_rate': win_rate
        })

        print(f"    >= {threshold:5.1f}   {len(filtered):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# COMPARISON TABLE - Best thresholds
print("\n" + "="*70)
print("COMPARISON: Best Thresholds")
print("="*70)

df_mod = pd.DataFrame(moderate_results).sort_values('win_rate', ascending=False)
df_calm = pd.DataFrame(calm_results).sort_values('win_rate', ascending=False)

print(f"\nTOP 3 for MODERATE:")
for i, (_, row) in enumerate(df_mod.head(3).iterrows(), 1):
    print(f"  {i}. >= {row['threshold']:.1f}: {row['qualified']:.0f} qualified, {row['win_rate']:.1f}% win rate")

print(f"\nTOP 3 for CALM:")
for i, (_, row) in enumerate(df_calm.head(3).iterrows(), 1):
    print(f"  {i}. >= {row['threshold']:.1f}: {row['qualified']:.0f} qualified, {row['win_rate']:.1f}% win rate")

# HYBRID STRATEGY: Different thresholds by condition
print("\n" + "="*70)
print("HYBRID STRATEGY: Different Thresholds by Condition")
print("="*70)

best_moderate_threshold = df_mod.iloc[0]['threshold']
best_calm_threshold = df_calm.iloc[0]['threshold']

print(f"\nOptimal for Moderate: >= {best_moderate_threshold}")
print(f"Optimal for Calm: >= {best_calm_threshold}")

# Apply hybrid
moderate_hybrid = moderate[moderate['difference'] >= best_moderate_threshold].copy()
calm_hybrid = calm[calm['difference'] >= best_calm_threshold].copy()

combined = pd.concat([moderate_hybrid, calm_hybrid])

if len(combined) > 0:
    wins = len(combined[combined['correct'] == True])
    win_rate = (wins / len(combined)) * 100

    print(f"\nResults with Hybrid Strategy:")
    print(f"  Total qualified: {len(combined)}")
    print(f"  Wins: {wins}")
    print(f"  Win Rate: {win_rate:.1f}%")

    print(f"\n  Moderate (>= {best_moderate_threshold}): {len(moderate_hybrid)} qualified, {(len(moderate_hybrid[moderate_hybrid['correct']==True])/len(moderate_hybrid)*100):.1f}% win rate")
    print(f"  Calm (>= {best_calm_threshold}): {len(calm_hybrid)} qualified, {(len(calm_hybrid[calm_hybrid['correct']==True])/len(calm_hybrid)*100):.1f}% win rate")

# Compare to overall >= 5.0
print("\n" + "="*70)
print("COMPARISON TO OVERALL >= 5.0")
print("="*70)

overall_5 = graded[graded['difference'] >= 5.0]
overall_wins = len(overall_5[overall_5['correct'] == True])
overall_rate = (overall_wins / len(overall_5)) * 100

print(f"\nUniform >= 5.0 strategy:")
print(f"  Qualified: {len(overall_5)}")
print(f"  Win Rate: {overall_rate:.1f}%")

print(f"\nHybrid strategy:")
print(f"  Qualified: {len(combined)}")
print(f"  Win Rate: {win_rate:.1f}%")
print(f"  Difference: {win_rate - overall_rate:+.1f}pp")
