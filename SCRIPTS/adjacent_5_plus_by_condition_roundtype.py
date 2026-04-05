#!/usr/bin/env python3
"""
Adjacent elements at >= 5.0 threshold, broken down by condition and round type.
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
    cycle = ['Wood', 'Earth', 'Water', 'Fire', 'Metal']
    if elem_a not in cycle or elem_b not in cycle:
        return 'unknown'
    idx_a = cycle.index(elem_a)
    idx_b = cycle.index(elem_b)
    dist = min(abs(idx_a - idx_b), 5 - abs(idx_a - idx_b))
    return 'adjacent' if dist == 1 else 'opposite'

valid['element_relationship'] = valid.apply(
    lambda row: get_element_relationship(row['Element [A]'], row['Element [B]']),
    axis=1
)

# Filter for adjacent >= 5.0
adjacent_5plus = valid[(valid['element_relationship'] == 'adjacent') & (valid['difference'] >= 5.0)].copy()

print("="*70)
print("ADJACENT ELEMENTS >= 5.0 BREAKDOWN")
print("="*70)

round_types = ['Open', 'Positioning', 'Closing']
conditions = ['Calm', 'Moderate']

# Overall
wins = len(adjacent_5plus[adjacent_5plus['correct'] == True])
rate = (wins / len(adjacent_5plus)) * 100
print(f"\nOVERALL: {len(adjacent_5plus)} matchups, {wins} wins, {rate:.1f}%\n")

# By Round Type
print(f"BY ROUND TYPE:")
print(f"{'Type':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for rt in round_types:
    rt_data = adjacent_5plus[adjacent_5plus['round_type'] == rt]
    if len(rt_data) > 0:
        rt_wins = len(rt_data[rt_data['correct'] == True])
        rt_rate = (rt_wins / len(rt_data)) * 100
        print(f"{rt:>12} {len(rt_data):>10.0f} {rt_wins:>6.0f} {rt_rate:>9.1f}%")

# By Condition
print(f"\nBY CONDITION:")
print(f"{'Condition':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for cond in conditions:
    cond_data = adjacent_5plus[adjacent_5plus['condition'] == cond]
    if len(cond_data) > 0:
        cond_wins = len(cond_data[cond_data['correct'] == True])
        cond_rate = (cond_wins / len(cond_data)) * 100
        print(f"{cond:>12} {len(cond_data):>10.0f} {cond_wins:>6.0f} {cond_rate:>9.1f}%")

# Cross-tabulation: Condition x Round Type
print(f"\nCONDITION x ROUND TYPE:")
print(f"\n{'Type':>12} {'Calm':>12} {'Moderate':>12}")
print("-"*40)

for rt in round_types:
    calm_data = adjacent_5plus[(adjacent_5plus['round_type'] == rt) & (adjacent_5plus['condition'] == 'Calm')]
    moderate_data = adjacent_5plus[(adjacent_5plus['round_type'] == rt) & (adjacent_5plus['condition'] == 'Moderate')]

    calm_str = ""
    if len(calm_data) > 0:
        calm_wins = len(calm_data[calm_data['correct'] == True])
        calm_rate = (calm_wins / len(calm_data)) * 100
        calm_str = f"{calm_rate:.1f}% ({len(calm_data):.0f})"
    else:
        calm_str = "—"

    moderate_str = ""
    if len(moderate_data) > 0:
        moderate_wins = len(moderate_data[moderate_data['correct'] == True])
        moderate_rate = (moderate_wins / len(moderate_data)) * 100
        moderate_str = f"{moderate_rate:.1f}% ({len(moderate_data):.0f})"
    else:
        moderate_str = "—"

    print(f"{rt:>12} {calm_str:>12} {moderate_str:>12}")

# Best combos
print(f"\n{'='*70}")
print("BEST COMBOS")
print(f"{'='*70}")

combos = []
for rt in round_types:
    for cond in conditions:
        combo_data = adjacent_5plus[(adjacent_5plus['round_type'] == rt) & (adjacent_5plus['condition'] == cond)]
        if len(combo_data) > 0:
            wins = len(combo_data[combo_data['correct'] == True])
            rate = (wins / len(combo_data)) * 100
            combos.append((f"{cond} x {rt}", rate, len(combo_data)))

combos.sort(key=lambda x: x[1], reverse=True)
for label, rate, count in combos:
    print(f"  {label:>20}: {rate:>5.1f}% ({count} matchups)")
