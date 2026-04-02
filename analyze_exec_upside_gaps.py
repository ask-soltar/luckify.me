#!/usr/bin/env python3
"""
Analyze patterns in raw Exec vs Upside gaps in matchup data.
"""

import pandas as pd

# Load matchup data
matchups = pd.read_csv('matchup.csv')

# Load scored results for comparison
scored = pd.read_csv('2ball_scored_35_65.csv')

# Merge to get outcome data
merged = matchups.merge(
    scored[['player_a', 'player_b', 'correct']],
    left_on=['Player A', 'Player B'],
    right_on=['player_a', 'player_b'],
    how='left'
)

# Calculate gaps
merged['gap_a'] = merged['Upside [A]'] - merged['Exec A']
merged['gap_b'] = merged['Upside [B]'] - merged['Exec B']
merged['gap_diff'] = merged['gap_a'] - merged['gap_b']
merged['gap_abs_diff'] = abs(merged['gap_diff'])

# Filter out rows without correct data (pushes, failed scoring)
valid = merged[merged['correct'].notna()].copy()

print("="*70)
print("EXEC vs UPSIDE GAP ANALYSIS")
print("="*70)

print(f"\nTotal valid matchups: {len(valid)}\n")

# Pattern 1: Distribution of gaps
print("="*70)
print("GAP DISTRIBUTIONS")
print("="*70)

print(f"\nIndividual Player Gaps (Upside - Exec):")
print(f"  Mean gap: {valid['gap_a'].mean():.2f}")
print(f"  Median gap: {valid['gap_a'].median():.2f}")
print(f"  Min gap: {valid['gap_a'].min():.2f}")
print(f"  Max gap: {valid['gap_a'].max():.2f}")

print(f"\nGap Difference (Player A gap - Player B gap):")
print(f"  Mean diff: {valid['gap_diff'].mean():.2f}")
print(f"  Median diff: {valid['gap_diff'].median():.2f}")
print(f"  Min diff: {valid['gap_diff'].min():.2f}")
print(f"  Max diff: {valid['gap_diff'].max():.2f}")

# Pattern 2: Do larger gaps correlate with wins?
print(f"\n" + "="*70)
print("DO GAPS CORRELATE WITH PREDICTION ACCURACY?")
print("="*70)

# Category by gap difference magnitude
print(f"\nBy Gap Difference Magnitude (absolute value):")

for gap_range in [(0, 5), (5, 10), (10, 20), (20, 50)]:
    subset = valid[(valid['gap_abs_diff'] >= gap_range[0]) & (valid['gap_abs_diff'] < gap_range[1])]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        print(f"  |Gap diff| {gap_range[0]:2d}-{gap_range[1]:2d}: {len(subset):3.0f} matchups, {wins:3.0f} wins, {win_rate:5.1f}% win rate")

# Pattern 3: Gap patterns by condition
print(f"\n" + "="*70)
print("GAP PATTERNS BY CONDITION")
print("="*70)

for condition in ['Calm', 'Moderate']:
    subset = valid[valid['Condition'] == condition]
    if len(condition) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        mean_gap_diff = subset['gap_abs_diff'].mean()

        print(f"\n{condition}:")
        print(f"  Matchups: {len(subset)}")
        print(f"  Mean |gap diff|: {mean_gap_diff:.2f}")
        print(f"  Win rate: {win_rate:.1f}%")

        # Show distribution
        for gap_range in [(0, 5), (5, 10), (10, 20)]:
            sub_subset = subset[(subset['gap_abs_diff'] >= gap_range[0]) & (subset['gap_abs_diff'] < gap_range[1])]
            if len(sub_subset) > 0:
                sub_wins = len(sub_subset[sub_subset['correct'] == True])
                sub_rate = (sub_wins / len(sub_subset)) * 100
                print(f"    |Gap| {gap_range[0]:2d}-{gap_range[1]:2d}: {len(sub_subset):2.0f} matchups, {sub_rate:5.1f}% win")

# Pattern 4: Gap patterns by round type
print(f"\n" + "="*70)
print("GAP PATTERNS BY ROUND TYPE (Calm only)")
print("="*70)

calm = valid[valid['Condition'] == 'Calm'].copy()

for round_type in ['Open', 'Positioning', 'Closing']:
    subset = calm[calm['Round Type'] == round_type]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        mean_gap_diff = subset['gap_abs_diff'].mean()

        print(f"\n{round_type}:")
        print(f"  Matchups: {len(subset)}")
        print(f"  Mean |gap diff|: {mean_gap_diff:.2f}")
        print(f"  Win rate: {win_rate:.1f}%")

# Pattern 5: Do consistent scores (low gap) beat volatile scores (high gap)?
print(f"\n" + "="*70)
print("CONSISTENCY vs VOLATILITY")
print("="*70)

# Players with gap = 0 (Exec = Upside)
flat = valid[valid['gap_a'] == 0]
print(f"\nFlat Exec/Upside (gap=0):")
print(f"  Matchups: {len(flat)}")
if len(flat) > 0:
    wins = len(flat[flat['correct'] == True])
    print(f"  Win rate (as predicted): {(wins/len(flat)*100):.1f}%")

# Players with large gaps
volatile = valid[valid['gap_a'] >= 25]
print(f"\nHigh-gap players (Upside >= 25 points above Exec):")
print(f"  Matchups: {len(volatile)}")
if len(volatile) > 0:
    wins = len(volatile[volatile['correct'] == True])
    print(f"  Win rate (as predicted): {(wins/len(volatile)*100):.1f}%")

# Pattern 6: When player with higher gap wins vs lower gap
print(f"\n" + "="*70)
print("HIGHER GAP ADVANTAGE")
print("="*70)

# Did the player with higher gap actually win?
valid['higher_gap_won'] = (valid['gap_a'] > valid['gap_b']) & (valid['correct'] == True)

higher_gap_count = len(valid[valid['gap_a'] > valid['gap_b']])
higher_gap_wins = len(valid[valid['higher_gap_won']])

if higher_gap_count > 0:
    higher_gap_rate = (higher_gap_wins / higher_gap_count) * 100
    print(f"\nWhen Player A has higher gap than Player B:")
    print(f"  Matchups where A has higher gap: {higher_gap_count}")
    print(f"  A actually predicted correctly: {higher_gap_wins}")
    print(f"  Win rate: {higher_gap_rate:.1f}%")

# Reverse
lower_gap_count = len(valid[valid['gap_a'] < valid['gap_b']])
lower_gap_wins = len(valid[(valid['gap_a'] < valid['gap_b']) & (valid['correct'] == True)])

if lower_gap_count > 0:
    lower_gap_rate = (lower_gap_wins / lower_gap_count) * 100
    print(f"\nWhen Player A has lower gap than Player B:")
    print(f"  Matchups where A has lower gap: {lower_gap_count}")
    print(f"  A actually predicted correctly: {lower_gap_wins}")
    print(f"  Win rate: {lower_gap_rate:.1f}%")

# Pattern 7: Gap gap gap - is there a threshold?
print(f"\n" + "="*70)
print("SAMPLE MATCHUPS: Analyzing Gap Patterns")
print("="*70)

# Show some high-gap vs low-gap matchups
print(f"\nHigh Gap Difference Wins (|gap_diff| >= 15, correct=True):")
high_gap_wins = valid[(valid['gap_abs_diff'] >= 15) & (valid['correct'] == True)].head(5)
for idx, (_, row) in enumerate(high_gap_wins.iterrows(), 1):
    print(f"{idx}. {row['Player A']} (gap={row['gap_a']:2.0f}) vs {row['Player B']} (gap={row['gap_b']:2.0f}) | Condition: {row['Condition']}")

print(f"\nLow Gap Difference Wins (|gap_diff| < 5, correct=True):")
low_gap_wins = valid[(valid['gap_abs_diff'] < 5) & (valid['correct'] == True)].head(5)
for idx, (_, row) in enumerate(low_gap_wins.iterrows(), 1):
    print(f"{idx}. {row['Player A']} (gap={row['gap_a']:2.0f}) vs {row['Player B']} (gap={row['gap_b']:2.0f}) | Condition: {row['Condition']}")
