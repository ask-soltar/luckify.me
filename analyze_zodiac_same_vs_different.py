#!/usr/bin/env python3
"""
Compare same vs different Chinese Zodiac animals.
"""

import pandas as pd

# Load data
matchups = pd.read_csv('matchup.csv')
scored = pd.read_csv('2ball_scored_35_65.csv')
analysis = pd.read_csv('ANALYSIS_v3_export.csv')

# Extract player -> zodiac mapping
player_zodiac = analysis[['player_name', 'zodiac']].drop_duplicates(subset=['player_name']).set_index('player_name')['zodiac'].to_dict()

print(f"Loaded zodiac data for {len(player_zodiac)} players")

# Merge with matchup data
merged = matchups.merge(
    scored[['player_a', 'player_b', 'correct', 'difference', 'condition', 'round_type']],
    left_on=['Player A', 'Player B'],
    right_on=['player_a', 'player_b'],
    how='left'
)

# Filter valid
valid = merged[merged['correct'].notna()].copy()

# Add zodiac for both players
valid['zodiac_a'] = valid['Player A'].map(player_zodiac)
valid['zodiac_b'] = valid['Player B'].map(player_zodiac)

# Filter out missing zodiac
valid = valid[(valid['zodiac_a'].notna()) & (valid['zodiac_b'].notna())].copy()

print(f"Matched {len(valid)} matchups with zodiac data\n")

# Define zodiac relationship
def get_zodiac_relationship(z_a, z_b):
    if z_a == z_b:
        return 'same'
    return 'different'

valid['zodiac_relationship'] = valid.apply(
    lambda row: get_zodiac_relationship(row['zodiac_a'], row['zodiac_b']),
    axis=1
)

print("="*70)
print("CHINESE ZODIAC COMPARISON: SAME vs DIFFERENT")
print("="*70)

# Distribution
dist = valid['zodiac_relationship'].value_counts()
print(f"\nTotal matchups with zodiac data: {len(valid)}")
for rel, count in dist.items():
    pct = (count / len(valid)) * 100
    print(f"  {rel:>10}: {count:4.0f} ({pct:5.1f}%)")

# Same zodiac
same_z = valid[valid['zodiac_relationship'] == 'same']
same_z_correct = same_z[same_z['correct'] == True]
same_z_rate = (len(same_z_correct) / len(same_z) * 100) if len(same_z) > 0 else 0

# Different zodiac
diff_z = valid[valid['zodiac_relationship'] == 'different']
diff_z_correct = diff_z[diff_z['correct'] == True]
diff_z_rate = (len(diff_z_correct) / len(diff_z) * 100) if len(diff_z) > 0 else 0

print(f"\n{'='*70}")
print("BASELINE WIN RATES")
print(f"{'='*70}")

print(f"\nSame Zodiac: {same_z_rate:.1f}% ({len(same_z_correct)}/{len(same_z)})")
print(f"Different Zodiac: {diff_z_rate:.1f}% ({len(diff_z_correct)}/{len(diff_z)})")
print(f"Difference: {same_z_rate - diff_z_rate:.1f}pp")

# Threshold analysis
print(f"\n{'='*70}")
print("SAME ZODIAC: THRESHOLD PROGRESSION")
print(f"{'='*70}")

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

for threshold in thresholds:
    above = same_z[same_z['difference'] >= threshold]
    if len(above) > 0:
        wins = len(above[above['correct'] == True])
        win_rate = (wins / len(above)) * 100
        print(f"    >= {threshold:5.1f}   {len(above):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# By condition
print(f"\n{'='*70}")
print("SAME ZODIAC BY CONDITION")
print(f"{'='*70}")

for cond in ['Calm', 'Moderate']:
    same_cond = same_z[same_z['condition'] == cond]
    if len(same_cond) > 0:
        wins = len(same_cond[same_cond['correct'] == True])
        rate = (wins / len(same_cond)) * 100
        print(f"\n{cond}: {rate:.1f}% ({wins}/{len(same_cond)})")

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(f"\nZodiac Signal Strength: {same_z_rate - diff_z_rate:.1f}pp")
if same_z_rate - diff_z_rate > 10:
    print("  Rating: STRONG (>10pp)")
elif same_z_rate - diff_z_rate > 5:
    print("  Rating: MODERATE (5-10pp)")
elif same_z_rate - diff_z_rate > 0:
    print("  Rating: WEAK (0-5pp)")
else:
    print("  Rating: NEGATIVE or NO SIGNAL")
