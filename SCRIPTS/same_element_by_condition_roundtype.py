#!/usr/bin/env python3
"""
Same element performance by threshold ranges, round type, and condition.
Two ranges: 1.5-4.0 and 4.0+
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

# Filter for same elements
same = valid[valid['element_relationship'] == 'same'].copy()

print("="*70)
print("SAME ELEMENT: 1.5-4.0 vs 4.0+ BREAKDOWN")
print("="*70)

ranges = {
    '1.5-4.0': (1.5, 4.0),
    '4.0+': (4.0, 100)
}

round_types = ['Open', 'Positioning', 'Closing']
conditions = ['Calm', 'Moderate']

for range_name, (min_diff, max_diff) in ranges.items():
    range_data = same[(same['difference'] >= min_diff) & (same['difference'] < max_diff)].copy()

    print(f"\n{'='*70}")
    print(f"RANGE: {range_name}")
    print(f"{'='*70}")

    # Overall
    wins = len(range_data[range_data['correct'] == True])
    rate = (wins / len(range_data)) * 100
    print(f"\nOVERALL: {len(range_data)} matchups, {wins} wins, {rate:.1f}%\n")

    # By Round Type
    print(f"BY ROUND TYPE:")
    print(f"{'Type':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
    print("-"*40)

    for rt in round_types:
        rt_data = range_data[range_data['round_type'] == rt]
        if len(rt_data) > 0:
            rt_wins = len(rt_data[rt_data['correct'] == True])
            rt_rate = (rt_wins / len(rt_data)) * 100
            print(f"{rt:>12} {len(rt_data):>10.0f} {rt_wins:>6.0f} {rt_rate:>9.1f}%")

    # By Condition
    print(f"\nBY CONDITION:")
    print(f"{'Condition':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
    print("-"*40)

    for cond in conditions:
        cond_data = range_data[range_data['condition'] == cond]
        if len(cond_data) > 0:
            cond_wins = len(cond_data[cond_data['correct'] == True])
            cond_rate = (cond_wins / len(cond_data)) * 100
            print(f"{cond:>12} {len(cond_data):>10.0f} {cond_wins:>6.0f} {cond_rate:>9.1f}%")

    # Cross-tabulation: Condition x Round Type
    print(f"\nCONDITION x ROUND TYPE:")
    print(f"\n{'Type':>12} {'Calm':>12} {'Moderate':>12}")
    print("-"*40)

    for rt in round_types:
        calm_data = range_data[(range_data['round_type'] == rt) & (range_data['condition'] == 'Calm')]
        moderate_data = range_data[(range_data['round_type'] == rt) & (range_data['condition'] == 'Moderate')]

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

# Comparison table
print(f"\n{'='*70}")
print("COMPARISON: 1.5-4.0 vs 4.0+")
print(f"{'='*70}")

data_1_5_4 = same[(same['difference'] >= 1.5) & (same['difference'] < 4.0)]
data_4_plus = same[same['difference'] >= 4.0]

print(f"\n{'Category':>20} {'1.5-4.0':>15} {'4.0+':>15}")
print("-"*50)

# Overall
wins_1_5_4 = len(data_1_5_4[data_1_5_4['correct'] == True])
rate_1_5_4 = (wins_1_5_4 / len(data_1_5_4)) * 100 if len(data_1_5_4) > 0 else 0

wins_4_plus = len(data_4_plus[data_4_plus['correct'] == True])
rate_4_plus = (wins_4_plus / len(data_4_plus)) * 100 if len(data_4_plus) > 0 else 0

print(f"{'Overall':>20} {rate_1_5_4:>14.1f}% {rate_4_plus:>14.1f}%")
print(f"{'Sample size':>20} {len(data_1_5_4):>14.0f} {len(data_4_plus):>14.0f}")

# By round type
for rt in round_types:
    rt_1_5_4 = data_1_5_4[data_1_5_4['round_type'] == rt]
    rt_4_plus = data_4_plus[data_4_plus['round_type'] == rt]

    rate_1_5_4_rt = (len(rt_1_5_4[rt_1_5_4['correct']==True])/len(rt_1_5_4)*100) if len(rt_1_5_4) > 0 else 0
    rate_4_plus_rt = (len(rt_4_plus[rt_4_plus['correct']==True])/len(rt_4_plus)*100) if len(rt_4_plus) > 0 else 0

    print(f"{rt:>20} {rate_1_5_4_rt:>14.1f}% {rate_4_plus_rt:>14.1f}%")

# By condition
print()
for cond in conditions:
    cond_1_5_4 = data_1_5_4[data_1_5_4['condition'] == cond]
    cond_4_plus = data_4_plus[data_4_plus['condition'] == cond]

    rate_1_5_4_cond = (len(cond_1_5_4[cond_1_5_4['correct']==True])/len(cond_1_5_4)*100) if len(cond_1_5_4) > 0 else 0
    rate_4_plus_cond = (len(cond_4_plus[cond_4_plus['correct']==True])/len(cond_4_plus)*100) if len(cond_4_plus) > 0 else 0

    print(f"{cond:>20} {rate_1_5_4_cond:>14.1f}% {rate_4_plus_cond:>14.1f}%")

# Best combos
print(f"\n{'='*70}")
print("BEST COMBOS")
print(f"{'='*70}")

print(f"\n1.5-4.0 Range - Best performers:")
for rt in round_types:
    for cond in conditions:
        combo_data = data_1_5_4[(data_1_5_4['round_type'] == rt) & (data_1_5_4['condition'] == cond)]
        if len(combo_data) >= 3:
            wins = len(combo_data[combo_data['correct'] == True])
            rate = (wins / len(combo_data)) * 100
            print(f"  {cond:>10} + {rt:>12}: {rate:>5.1f}% ({len(combo_data):.0f} matchups)")

print(f"\n4.0+ Range - Best performers:")
for rt in round_types:
    for cond in conditions:
        combo_data = data_4_plus[(data_4_plus['round_type'] == rt) & (data_4_plus['condition'] == cond)]
        if len(combo_data) >= 3:
            wins = len(combo_data[combo_data['correct'] == True])
            rate = (wins / len(combo_data)) * 100
            print(f"  {cond:>10} + {rt:>12}: {rate:>5.1f}% ({len(combo_data):.0f} matchups)")
