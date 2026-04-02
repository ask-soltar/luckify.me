#!/usr/bin/env python3
"""
Show win rates for specific difference RANGES (not cumulative).
E.g., 3.0-3.5, 3.5-4.0, etc.
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

print("="*70)
print("WIN RATES BY DIFFERENCE RANGE (Itemized)")
print("="*70)

# Define ranges
ranges = [
    (0, 3.0),
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
]

relationships = ['same', 'adjacent', 'opposite']

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel].copy()

    if len(subset) == 0:
        continue

    print(f"\n{'='*70}")
    print(f"{rel.upper()} ELEMENTS")
    print(f"{'='*70}")
    print(f"{'Range':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10} {'Status':>10}")
    print("-"*70)

    for min_diff, max_diff in ranges:
        in_range = subset[(subset['difference'] >= min_diff) & (subset['difference'] < max_diff)]

        if len(in_range) > 0:
            wins = len(in_range[in_range['correct'] == True])
            win_rate = (wins / len(in_range)) * 100
            status = "WIN" if win_rate > 54 else ""

            print(f"{min_diff:5.1f}-{max_diff:5.1f}   {len(in_range):10.0f} {wins:6.0f} {win_rate:9.1f}% {status:>10}")

# Comparison table
print(f"\n{'='*70}")
print("COMPARISON TABLE: All Ranges")
print(f"{'='*70}")

print(f"\n{'Range':>12}", end="")
for rel in relationships:
    print(f" {rel.upper():>12}", end="")
print()

print("-"*70)

for min_diff, max_diff in ranges:
    print(f"{min_diff:5.1f}-{max_diff:5.1f}  ", end="")

    for rel in relationships:
        subset = valid[valid['element_relationship'] == rel]
        in_range = subset[(subset['difference'] >= min_diff) & (subset['difference'] < max_diff)]

        if len(in_range) > 0:
            wins = len(in_range[in_range['correct'] == True])
            win_rate = (wins / len(in_range)) * 100
            status = " WIN" if win_rate > 54 else ""
            print(f" {win_rate:6.1f}%{status:<6}", end="")
        else:
            print(f" {'N/A':>12}", end="")

    print()

# Summary: Show which ranges are >54% for each relationship
print(f"\n{'='*70}")
print("SUMMARY: Ranges >54% Win Rate")
print(f"{'='*70}")

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel]
    winning_ranges = []

    for min_diff, max_diff in ranges:
        in_range = subset[(subset['difference'] >= min_diff) & (subset['difference'] < max_diff)]

        if len(in_range) > 0:
            wins = len(in_range[in_range['correct'] == True])
            win_rate = (wins / len(in_range)) * 100

            if win_rate > 54:
                winning_ranges.append(f"{min_diff:.1f}-{max_diff:.1f}")

    if winning_ranges:
        print(f"\n{rel.upper()}:")
        print(f"  Winning ranges: {', '.join(winning_ranges)}")
    else:
        print(f"\n{rel.upper()}:")
        print(f"  No ranges exceed 54%")

# Show volume concentration
print(f"\n{'='*70}")
print("VOLUME CONCENTRATION (Where most matchups cluster)")
print(f"{'='*70}")

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel]

    print(f"\n{rel.upper()}:")

    max_count = 0
    densest_range = None

    for min_diff, max_diff in ranges:
        in_range = subset[(subset['difference'] >= min_diff) & (subset['difference'] < max_diff)]

        if len(in_range) > max_count:
            max_count = len(in_range)
            densest_range = (min_diff, max_diff)

    if densest_range:
        print(f"  Densest range: {densest_range[0]:.1f}-{densest_range[1]:.1f} ({max_count} matchups)")
