#!/usr/bin/env python3
"""
Analyze win rates by round type (no score filters).
"""

import pandas as pd

# Load the scored results
df = pd.read_csv('2ball_scored_golf_historics.csv')

# Exclude pushes
graded = df[df['actual_winner'] != 'Push'].copy()

print("="*70)
print("WIN RATE BY ROUND TYPE (No Score Filters)")
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

print(f"\n" + "="*70)
print(f"TOTAL: {len(graded)} graded matchups")
print(f"="*70)
