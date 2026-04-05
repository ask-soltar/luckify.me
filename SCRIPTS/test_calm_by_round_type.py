#!/usr/bin/env python3
"""
Test thresholds separately for each round type within Calm conditions.
"""

import pandas as pd

# Load scored data
df = pd.read_csv('2ball_scored_35_65.csv')

# Filter for graded Calm only
calm = df[(df['actual_winner'] != 'Push') & (df['condition'] == 'Calm')].copy()

print("="*70)
print("CALM CONDITIONS: THRESHOLD TESTING BY ROUND TYPE")
print("="*70)

thresholds = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]

round_types = ['Open', 'Positioning', 'Closing']

results_by_round = {}

for round_type in round_types:
    print(f"\n{'='*70}")
    print(f"{round_type.upper()}")
    print(f"{'='*70}")

    subset = calm[calm['round_type'] == round_type].copy()
    total = len(subset)

    print(f"Total Calm {round_type.lower()} matchups: {total}\n")
    print(f"{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
    print("-"*70)

    results_by_round[round_type] = []

    for threshold in thresholds:
        filtered = subset[subset['difference'] >= threshold].copy()

        if len(filtered) > 0:
            wins = len(filtered[filtered['correct'] == True])
            win_rate = (wins / len(filtered)) * 100

            results_by_round[round_type].append({
                'threshold': threshold,
                'qualified': len(filtered),
                'wins': wins,
                'win_rate': win_rate
            })

            print(f"    >= {threshold:5.1f}   {len(filtered):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# Summary: Best threshold per round type
print(f"\n{'='*70}")
print("BEST THRESHOLD PER ROUND TYPE (Calm)")
print(f"{'='*70}")

summary = []

for round_type in round_types:
    if results_by_round[round_type]:
        df_results = pd.DataFrame(results_by_round[round_type])
        best = df_results.sort_values('win_rate', ascending=False).iloc[0]

        summary.append({
            'round_type': round_type,
            'threshold': best['threshold'],
            'qualified': int(best['qualified']),
            'wins': int(best['wins']),
            'win_rate': best['win_rate']
        })

        print(f"\n{round_type}:")
        print(f"  Optimal threshold: >= {best['threshold']:.1f}")
        print(f"  Qualified: {int(best['qualified'])}")
        print(f"  Wins: {int(best['wins'])}")
        print(f"  Win Rate: {best['win_rate']:.1f}%")

# Combined results with optimized thresholds per round type
print(f"\n{'='*70}")
print("OPTIMIZED STRATEGY: Different Thresholds by Round Type (within Calm)")
print(f"{'='*70}")

df_summary = pd.DataFrame(summary)

combined_filtered = pd.DataFrame()

for _, row in df_summary.iterrows():
    rt = row['round_type']
    thresh = row['threshold']
    subset = calm[(calm['round_type'] == rt) & (calm['difference'] >= thresh)]
    combined_filtered = pd.concat([combined_filtered, subset])

if len(combined_filtered) > 0:
    total_wins = len(combined_filtered[combined_filtered['correct'] == True])
    total_rate = (total_wins / len(combined_filtered)) * 100

    print(f"\nApplying optimal threshold per round type:")
    print(f"  Total qualified: {len(combined_filtered)}")
    print(f"  Total wins: {total_wins}")
    print(f"  Overall win rate: {total_rate:.1f}%")

    print(f"\n  Breakdown:")
    for _, row in df_summary.iterrows():
        print(f"    {row['round_type']:12} >= {row['threshold']:.1f}: {row['qualified']:2.0f} qualified, {row['wins']:2.0f} wins, {row['win_rate']:5.1f}% win")

# Compare to uniform threshold
print(f"\n{'='*70}")
print("COMPARISON: Uniform vs. Optimized by Round Type")
print(f"{'='*70}")

uniform_5 = calm[calm['difference'] >= 5.0]
uniform_wins = len(uniform_5[uniform_5['correct'] == True])
uniform_rate = (uniform_wins / len(uniform_5)) * 100

print(f"\nUniform >= 5.0 (across all round types):")
print(f"  Qualified: {len(uniform_5)}")
print(f"  Wins: {uniform_wins}")
print(f"  Win Rate: {uniform_rate:.1f}%")

if len(combined_filtered) > 0:
    print(f"\nOptimized (different threshold per round type):")
    print(f"  Qualified: {len(combined_filtered)}")
    print(f"  Wins: {total_wins}")
    print(f"  Win Rate: {total_rate:.1f}%")

    print(f"\nDifference: {total_rate - uniform_rate:+.1f}pp")
