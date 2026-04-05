#!/usr/bin/env python3
"""
Show all thresholds with win rate > 54% for each element relationship.
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
print("WINNING RANGES (Win Rate > 54%)")
print("="*70)

thresholds = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]

relationships = ['same', 'adjacent', 'opposite']

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel].copy()

    if len(subset) == 0:
        continue

    print(f"\n{'='*70}")
    print(f"{rel.upper()} ELEMENTS")
    print(f"{'='*70}")
    print(f"{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10} {'Status':>10}")
    print("-"*70)

    winning_ranges = []

    for threshold in thresholds:
        filtered = subset[subset['difference'] >= threshold].copy()

        if len(filtered) > 0:
            wins = len(filtered[filtered['correct'] == True])
            win_rate = (wins / len(filtered)) * 100

            status = "WIN" if win_rate > 54 else ""

            print(f"    >= {threshold:5.1f}   {len(filtered):10.0f} {wins:6.0f} {win_rate:9.1f}% {status:>10}")

            if win_rate > 54:
                winning_ranges.append({
                    'threshold': threshold,
                    'qualified': len(filtered),
                    'wins': wins,
                    'win_rate': win_rate
                })

    if winning_ranges:
        print(f"\nWinning thresholds (>54%):")
        for wr in winning_ranges:
            print(f"    >= {wr['threshold']:.1f}: {wr['qualified']:3.0f} qualified, {wr['win_rate']:5.1f}% win rate")

# Summary table
print(f"\n{'='*70}")
print("SUMMARY: VIABLE RANGES BY ELEMENT RELATIONSHIP")
print(f"{'='*70}")

print(f"\n{'Relationship':>12} {'Min Threshold':>15} {'Max Threshold':>15} {'Sample Win Rate':>20}")
print("-"*70)

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel].copy()

    if len(subset) == 0:
        continue

    winning_thresholds = []

    for threshold in thresholds:
        filtered = subset[subset['difference'] >= threshold].copy()

        if len(filtered) > 0:
            wins = len(filtered[filtered['correct'] == True])
            win_rate = (wins / len(filtered)) * 100

            if win_rate > 54:
                winning_thresholds.append(threshold)

    if winning_thresholds:
        min_threshold = min(winning_thresholds)
        max_threshold = max(winning_thresholds)

        # Get sample win rate at min threshold
        min_filtered = subset[subset['difference'] >= min_threshold]
        min_wins = len(min_filtered[min_filtered['correct'] == True])
        min_rate = (min_wins / len(min_filtered)) * 100

        print(f"{rel:>12} >= {min_threshold:5.1f}    to   >= {max_threshold:5.1f}    {min_rate:5.1f}% at min threshold")

# Comparison table with all three
print(f"\n{'='*70}")
print("DIRECT COMPARISON: All Thresholds >54%")
print(f"{'='*70}")

print(f"\n{'Threshold':>10} {'Same %':>10} {'Adjacent %':>10} {'Opposite %':>10}")
print("-"*70)

for threshold in thresholds:
    same = valid[valid['element_relationship'] == 'same']
    adjacent = valid[valid['element_relationship'] == 'adjacent']
    opposite = valid[valid['element_relationship'] == 'opposite']

    same_filt = same[same['difference'] >= threshold]
    adj_filt = adjacent[adjacent['difference'] >= threshold]
    opp_filt = opposite[opposite['difference'] >= threshold]

    same_rate = (len(same_filt[same_filt['correct']==True])/len(same_filt)*100) if len(same_filt) > 0 else 0
    adj_rate = (len(adj_filt[adj_filt['correct']==True])/len(adj_filt)*100) if len(adj_filt) > 0 else 0
    opp_rate = (len(opp_filt[opp_filt['correct']==True])/len(opp_filt)*100) if len(opp_filt) > 0 else 0

    # Mark with WIN if >54%
    same_str = f"{same_rate:5.1f}%" + (" WIN" if same_rate > 54 else "")
    adj_str = f"{adj_rate:5.1f}%" + (" WIN" if adj_rate > 54 else "")
    opp_str = f"{opp_rate:5.1f}%" + (" WIN" if opp_rate > 54 else "")

    print(f"    >= {threshold:5.1f}   {same_str:>10} {adj_str:>10} {opp_str:>10}")

# Recommendation
print(f"\n{'='*70}")
print("RECOMMENDED STRATEGY")
print(f"{'='*70}")

print(f"\nFor >54% win rates:")
print(f"  - Same elements:   Use thresholds >= 3.0 to >= 8.0 (all qualify)")
print(f"  - Adjacent elements: Use thresholds >= 4.5 to >= 8.0")
print(f"  - Opposite elements: Never qualifies at >54% (max 50.4%)")
print(f"\n  STRATEGY: EXCLUDE opposite elements entirely")
print(f"  FOCUS: Use SAME + ADJACENT with appropriate thresholds")
