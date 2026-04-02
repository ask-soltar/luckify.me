#!/usr/bin/env python3
"""
Analyze 2-ball scores using Golf Historics v3 with difference >= 4 filter.
"""

import pandas as pd

# Load the scored results (using Score column from v1)
df = pd.read_csv('2ball_scored_golf_historics.csv')

# Calculate difference
df['difference'] = df['winner_score'] - df['loser_score']

# Exclude pushes
graded = df[df['actual_winner'] != 'Push'].copy()

print("="*70)
print("OVERALL - All Matchups (No Filter)")
print("="*70)

wins_all = len(graded[graded['correct'] == True])
rate_all = (wins_all / len(graded)) * 100

print(f"Matchups: {len(graded)}")
print(f"Wins: {wins_all}")
print(f"Losses: {len(graded) - wins_all}")
print(f"Win Rate: {rate_all:.1f}%\n")

print("="*70)
print("FILTER: Difference >= 4")
print("="*70)

filtered = graded[graded['difference'] >= 4].copy()

if len(filtered) > 0:
    wins = len(filtered[filtered['correct'] == True])
    rate = (wins / len(filtered)) * 100

    print(f"\nTotal Qualified: {len(filtered)}")
    print(f"Wins: {wins}")
    print(f"Losses: {len(filtered) - wins}")
    print(f"Win Rate: {rate:.1f}%\n")

print("="*70)
print("BY ROUND TYPE (Difference >= 4)")
print("="*70)

for round_type in ['Open', 'Positioning', 'Closing']:
    subset = filtered[filtered['round_type'] == round_type]

    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        losses = len(subset[subset['correct'] == False])
        win_rate = (wins / len(subset)) * 100

        print(f"\n{round_type}:")
        print(f"  Qualified: {len(subset)}")
        print(f"  Wins: {wins}")
        print(f"  Losses: {losses}")
        print(f"  Win Rate: {win_rate:.1f}%")
    else:
        print(f"\n{round_type}: No data")

# Also show by round type without filter
print(f"\n" + "="*70)
print("BY ROUND TYPE (No Filter)")
print("="*70)

for round_type in ['Open', 'Positioning', 'Closing']:
    subset = graded[graded['round_type'] == round_type]

    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        losses = len(subset[subset['correct'] == False])
        win_rate = (wins / len(subset)) * 100

        print(f"\n{round_type}:")
        print(f"  Matchups: {len(subset)}")
        print(f"  Wins: {wins}")
        print(f"  Losses: {losses}")
        print(f"  Win Rate: {win_rate:.1f}%")
    else:
        print(f"\n{round_type}: No data")
