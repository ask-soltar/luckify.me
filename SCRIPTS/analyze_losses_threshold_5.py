#!/usr/bin/env python3
"""
Analyze losses at threshold >= 5.0 to find patterns.
"""

import pandas as pd

# Load scored data
df = pd.read_csv('2ball_scored_35_65.csv')

# Filter for threshold >= 5.0, exclude pushes, get losses only
graded = df[df['actual_winner'] != 'Push'].copy()
threshold_5 = graded[graded['difference'] >= 5.0].copy()
losses = threshold_5[threshold_5['correct'] == False].copy()

print(f"="*70)
print(f"LOSSES AT THRESHOLD >= 5.0")
print(f"="*70)
print(f"\nTotal losses: {len(losses)}")
print(f"(Out of {len(threshold_5)} qualified predictions)\n")

# Pattern 1: By Round Type
print("="*70)
print("BY ROUND TYPE")
print("="*70)

for round_type in ['Open', 'Positioning', 'Closing']:
    subset = losses[losses['round_type'] == round_type]
    if len(subset) > 0:
        print(f"\n{round_type}: {len(subset)} losses")
        print(f"  Conditions: {subset['condition'].value_counts().to_dict()}")

# Pattern 2: By Condition
print("\n" + "="*70)
print("BY CONDITION")
print("="*70)

for condition in sorted(losses['condition'].unique()):
    subset = losses[losses['condition'] == condition]
    if len(subset) > 0:
        print(f"\n{condition}: {len(subset)} losses")
        round_types = subset['round_type'].value_counts()
        for rt, count in round_types.items():
            print(f"  {rt}: {count}")

# Pattern 3: Score differential distribution
print("\n" + "="*70)
print("SCORE DIFFERENTIAL DISTRIBUTION (Losses)")
print("="*70)

print(f"\nMean difference: {losses['difference'].mean():.2f}")
print(f"Median difference: {losses['difference'].median():.2f}")
print(f"Min difference: {losses['difference'].min():.2f}")
print(f"Max difference: {losses['difference'].max():.2f}")

# Break down by difference ranges
for min_diff in [5.0, 6.0, 7.0, 8.0, 10.0]:
    count = len(losses[losses['difference'] >= min_diff])
    if count > 0:
        pct = (count / len(losses)) * 100
        print(f"  >= {min_diff}: {count} losses ({pct:.1f}%)")

# Pattern 4: Loser score distribution
print("\n" + "="*70)
print("LOSER SCORE DISTRIBUTION (Losses)")
print("="*70)

print(f"\nMean loser score: {losses['loser_score'].mean():.2f}")
print(f"Median loser score: {losses['loser_score'].median():.2f}")
print(f"Min loser score: {losses['loser_score'].min():.2f}")
print(f"Max loser score: {losses['loser_score'].max():.2f}")

# Distribution
for min_score in [-2, -1, 0, 1]:
    count = len(losses[losses['loser_score'] >= min_score])
    if count > 0:
        print(f"  Loser score >= {min_score}: {count} losses")

# Pattern 5: Show specific losing matchups
print("\n" + "="*70)
print("SAMPLE LOSING MATCHUPS (First 15)")
print("="*70)

for idx, (_, row) in enumerate(losses.head(15).iterrows(), 1):
    print(f"\n{idx}. {row['player_a']} vs {row['player_b']}")
    print(f"   Condition: {row['condition']} | Round Type: {row['round_type']}")
    print(f"   Prediction: {row['prediction']} (Score: {row['score_a']:.2f})")
    print(f"   Actual Winner: {row['actual_winner']} (Score: {row['score_b']:.2f})")
    print(f"   Difference: {row['difference']:.2f}")

# Pattern 6: Condition + Round Type combo for losses
print("\n" + "="*70)
print("CONDITION × ROUND TYPE COMBOS (Losses)")
print("="*70)

combos = losses.groupby(['condition', 'round_type']).size().reset_index(name='count')
combos = combos.sort_values('count', ascending=False)

for _, row in combos.iterrows():
    print(f"\n{row['condition']} × {row['round_type']}: {row['count']} losses")
