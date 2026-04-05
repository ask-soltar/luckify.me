#!/usr/bin/env python3
"""
Zodiac same vs adjacent, broken into 0.5 increment ranges.
"""

import pandas as pd

# Load data
matchups = pd.read_csv('matchup.csv')
scored = pd.read_csv('2ball_scored_35_65.csv')
analysis = pd.read_csv('ANALYSIS_v3_export.csv')

# Extract player -> zodiac mapping
player_zodiac = analysis[['player_name', 'zodiac']].drop_duplicates(subset=['player_name']).set_index('player_name')['zodiac'].to_dict()

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

# Define zodiac relationships
zodiac_cycle = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']

def get_zodiac_relationship(z_a, z_b):
    if z_a == z_b:
        return 'same'
    if z_a not in zodiac_cycle or z_b not in zodiac_cycle:
        return 'unknown'
    idx_a = zodiac_cycle.index(z_a)
    idx_b = zodiac_cycle.index(z_b)
    dist = min(abs(idx_a - idx_b), 12 - abs(idx_a - idx_b))
    if dist == 1:
        return 'adjacent'
    else:
        return 'other'

valid['zodiac_relationship'] = valid.apply(
    lambda row: get_zodiac_relationship(row['zodiac_a'], row['zodiac_b']),
    axis=1
)

# Define ranges
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
]

print("="*80)
print("ZODIAC SAME vs ADJACENT: POINT INTERVALS (0.5 increments)")
print("="*80)

same_z = valid[valid['zodiac_relationship'] == 'same']
adjacent_z = valid[valid['zodiac_relationship'] == 'adjacent']

print(f"\n{'Range':>12} {'SAME Wins':>12} {'SAME Rate':>12} {'ADJ Wins':>12} {'ADJ Rate':>12} {'Diff':>8}")
print("-"*80)

for min_diff, max_diff in ranges:
    same_in_range = same_z[(same_z['difference'] >= min_diff) & (same_z['difference'] < max_diff)]
    adjacent_in_range = adjacent_z[(adjacent_z['difference'] >= min_diff) & (adjacent_z['difference'] < max_diff)]

    same_str = ""
    if len(same_in_range) > 0:
        same_wins = len(same_in_range[same_in_range['correct'] == True])
        same_rate = (same_wins / len(same_in_range)) * 100
        same_str = f"{same_wins}/{len(same_in_range)} ({same_rate:5.1f}%)"
    else:
        same_str = "—"
        same_rate = 0

    adj_str = ""
    if len(adjacent_in_range) > 0:
        adj_wins = len(adjacent_in_range[adjacent_in_range['correct'] == True])
        adj_rate = (adj_wins / len(adjacent_in_range)) * 100
        adj_str = f"{adj_wins}/{len(adjacent_in_range)} ({adj_rate:5.1f}%)"
    else:
        adj_str = "—"
        adj_rate = 0

    diff_str = ""
    if len(same_in_range) > 0 and len(adjacent_in_range) > 0:
        diff_str = f"{same_rate - adj_rate:+.1f}pp"

    print(f"{min_diff:5.1f}-{max_diff:5.1f}  {same_str:>12} {adj_str:>12} {diff_str:>8}")

# Summary statistics
print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")

same_total = len(same_z)
same_wins = len(same_z[same_z['correct'] == True])
same_rate = (same_wins / same_total * 100) if same_total > 0 else 0

adj_total = len(adjacent_z)
adj_wins = len(adjacent_z[adjacent_z['correct'] == True])
adj_rate = (adj_wins / adj_total * 100) if adj_total > 0 else 0

print(f"\nSAME ZODIAC:     {same_wins}/{same_total} = {same_rate:.1f}%")
print(f"ADJACENT ZODIAC: {adj_wins}/{adj_total} = {adj_rate:.1f}%")
print(f"Difference: {same_rate - adj_rate:.1f}pp\n")

# Ranges >54% for each
print("Ranges >54%:")
same_winning = []
adj_winning = []

for min_diff, max_diff in ranges:
    same_in_range = same_z[(same_z['difference'] >= min_diff) & (same_z['difference'] < max_diff)]
    adjacent_in_range = adjacent_z[(adjacent_z['difference'] >= min_diff) & (adjacent_z['difference'] < max_diff)]

    if len(same_in_range) > 0:
        same_wins_r = len(same_in_range[same_in_range['correct'] == True])
        same_rate_r = (same_wins_r / len(same_in_range)) * 100
        if same_rate_r > 54:
            same_winning.append(f"{min_diff:.1f}-{max_diff:.1f}")

    if len(adjacent_in_range) > 0:
        adj_wins_r = len(adjacent_in_range[adjacent_in_range['correct'] == True])
        adj_rate_r = (adj_wins_r / len(adjacent_in_range)) * 100
        if adj_rate_r > 54:
            adj_winning.append(f"{min_diff:.1f}-{max_diff:.1f}")

print(f"\nSAME:     {', '.join(same_winning) if same_winning else 'None'}")
print(f"ADJACENT: {', '.join(adj_winning) if adj_winning else 'None'}")

# Cumulative thresholds
print(f"\n{'='*80}")
print("CUMULATIVE: Minimum Threshold Performance")
print(f"{'='*80}")

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

print(f"\n{'Threshold':>10} {'SAME Qual':>12} {'SAME Rate':>12} {'ADJ Qual':>12} {'ADJ Rate':>12}")
print("-"*80)

for threshold in thresholds:
    same_above = same_z[same_z['difference'] >= threshold]
    adj_above = adjacent_z[adjacent_z['difference'] >= threshold]

    same_str = ""
    if len(same_above) > 0:
        same_wins_t = len(same_above[same_above['correct'] == True])
        same_rate_t = (same_wins_t / len(same_above)) * 100
        same_str = f"{len(same_above):3.0f} @ {same_rate_t:5.1f}%"
    else:
        same_str = "—"

    adj_str = ""
    if len(adj_above) > 0:
        adj_wins_t = len(adj_above[adj_above['correct'] == True])
        adj_rate_t = (adj_wins_t / len(adj_above)) * 100
        adj_str = f"{len(adj_above):3.0f} @ {adj_rate_t:5.1f}%"
    else:
        adj_str = "—"

    print(f"    >= {threshold:5.1f}   {same_str:>12} {adj_str:>12}")
