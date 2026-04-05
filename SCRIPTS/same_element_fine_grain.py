#!/usr/bin/env python3
"""
Fine-grained analysis of same element matchups with 0.5 increments.
"""

import pandas as pd

# Load data
matchups = pd.read_csv('matchup.csv')
scored = pd.read_csv('2ball_scored_35_65.csv')

# Merge
merged = matchups.merge(
    scored[['player_a', 'player_b', 'correct', 'difference', 'condition', 'round_type']],
    left_on=['Player A', 'Player B'],
    right_on=['player_a', 'player_b'],
    how='left'
)

# Filter valid
valid = merged[merged['correct'].notna()].copy()

# Define relationships
def get_element_relationship(elem_a, elem_b):
    if elem_a == elem_b:
        return 'same'
    return 'other'

valid['element_relationship'] = valid.apply(
    lambda row: get_element_relationship(row['Element [A]'], row['Element [B]']),
    axis=1
)

# Filter for same elements only
same = valid[valid['element_relationship'] == 'same'].copy()

print("="*70)
print("SAME ELEMENT DETAILED RANGES (0.5 increments)")
print("="*70)

print(f"\nTotal same element matchups: {len(same)}\n")

# Define fine-grained ranges
ranges = [
    (0, 0.5),
    (0.5, 1.0),
    (1.0, 1.5),
    (1.5, 2.0),
    (2.0, 2.5),
    (2.5, 3.0),
    (3.0, 3.5),
    (3.5, 4.0),
    (4.0, 4.5),
    (4.5, 5.0),
    (5.0, 5.5),
    (5.5, 6.0),
    (6.0, 6.5),
    (6.5, 7.0),
    (7.0, 7.5),
    (7.5, 8.0),
    (8.0, 9.0),
    (9.0, 10.0),
]

print(f"{'Range':>12} {'Matchups':>10} {'Wins':>6} {'Losses':>6} {'Win Rate':>10} {'Status':>10}")
print("-"*70)

results = []

for min_diff, max_diff in ranges:
    in_range = same[(same['difference'] >= min_diff) & (same['difference'] < max_diff)]

    if len(in_range) > 0:
        wins = len(in_range[in_range['correct'] == True])
        losses = len(in_range) - wins
        win_rate = (wins / len(in_range)) * 100
        status = "WIN" if win_rate > 54 else ""

        results.append({
            'range': f"{min_diff:.1f}-{max_diff:.1f}",
            'matchups': len(in_range),
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate
        })

        print(f"{min_diff:5.1f}-{max_diff:5.1f}  {len(in_range):10.0f} {wins:6.0f} {losses:6.0f} {win_rate:9.1f}% {status:>10}")

# Summary statistics
print(f"\n{'='*70}")
print("SUMMARY STATISTICS")
print(f"{'='*70}")

df_results = pd.DataFrame(results)

# Ranges >54%
winning = df_results[df_results['win_rate'] > 54]
print(f"\nRanges > 54% win rate: {len(winning)} out of {len(df_results)}")
if len(winning) > 0:
    print(f"Ranges: {', '.join(winning['range'].tolist())}")

# Volume analysis
print(f"\nVolume distribution:")
print(f"  0.0-3.0: {sum(df_results[df_results['range'].isin(['0.0-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-2.5', '2.5-3.0'])]['matchups'])} matchups")
print(f"  3.0-5.0: {sum(df_results[df_results['range'].isin(['3.0-3.5', '3.5-4.0', '4.0-4.5', '4.5-5.0'])]['matchups'])} matchups")
print(f"  5.0-8.0: {sum(df_results[df_results['range'].isin(['5.0-5.5', '5.5-6.0', '6.0-6.5', '6.5-7.0', '7.0-7.5', '7.5-8.0'])]['matchups'])} matchups")
print(f"  8.0+:    {sum(df_results[~df_results['range'].isin(['0.0-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-2.5', '2.5-3.0', '3.0-3.5', '3.5-4.0', '4.0-4.5', '4.5-5.0', '5.0-5.5', '5.5-6.0', '6.0-6.5', '6.5-7.0', '7.0-7.5', '7.5-8.0'])]['matchups'])} matchups")

# Best ranges
print(f"\nTop 5 ranges by win rate:")
top5 = df_results.nlargest(5, 'win_rate')
for idx, (_, row) in enumerate(top5.iterrows(), 1):
    print(f"  {idx}. {row['range']}: {row['win_rate']:.1f}% ({row['wins']:.0f}/{row['matchups']:.0f})")

# Worst ranges
print(f"\nWorst 5 ranges by win rate:")
bottom5 = df_results.nsmallest(5, 'win_rate')
for idx, (_, row) in enumerate(bottom5.iterrows(), 1):
    print(f"  {idx}. {row['range']}: {row['win_rate']:.1f}% ({row['wins']:.0f}/{row['matchups']:.0f})")

# Cumulative analysis
print(f"\n{'='*70}")
print("CUMULATIVE: Minimum Threshold Performance")
print(f"{'='*70}")

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]

for threshold in thresholds:
    above_threshold = same[same['difference'] >= threshold]
    if len(above_threshold) > 0:
        wins = len(above_threshold[above_threshold['correct'] == True])
        win_rate = (wins / len(above_threshold)) * 100
        print(f"    >= {threshold:5.1f}   {len(above_threshold):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# By condition
print(f"\n{'='*70}")
print("SAME ELEMENT BY CONDITION")
print(f"{'='*70}")

for condition in ['Calm', 'Moderate']:
    same_cond = same[same['condition'] == condition]
    if len(same_cond) > 0:
        print(f"\n{condition}:")
        print(f"  Total: {len(same_cond)}")
        wins = len(same_cond[same_cond['correct'] == True])
        print(f"  Wins: {wins}")
        print(f"  Win Rate: {(wins/len(same_cond)*100):.1f}%")

        # Show best range for this condition
        print(f"\n  Best ranges:")
        best_ranges = []
        for min_diff, max_diff in ranges[:10]:  # Check first 10 ranges
            in_range = same_cond[(same_cond['difference'] >= min_diff) & (same_cond['difference'] < max_diff)]
            if len(in_range) >= 5:
                wins_range = len(in_range[in_range['correct'] == True])
                win_rate_range = (wins_range / len(in_range)) * 100
                best_ranges.append((f"{min_diff:.1f}-{max_diff:.1f}", win_rate_range, len(in_range)))

        best_ranges.sort(key=lambda x: x[1], reverse=True)
        for label, rate, count in best_ranges[:3]:
            print(f"    {label}: {rate:.1f}% ({count} matchups)")
