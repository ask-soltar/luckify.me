#!/usr/bin/env python3
"""
Analyze same element and Wu Xing opposite matchups with thresholds.
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

# Define Wu Xing relationships
# Cycle: Wood > Earth > Water > Fire > Metal > Wood
# Adjacent (one element controls next): Wood-Earth, Earth-Water, Water-Fire, Fire-Metal, Metal-Wood
# Opposites (non-adjacent): Wood-Water, Wood-Fire, Earth-Fire, Earth-Metal, Water-Metal

def get_element_relationship(elem_a, elem_b):
    """Classify relationship between two elements."""
    if elem_a == elem_b:
        return 'same'

    cycle = ['Wood', 'Earth', 'Water', 'Fire', 'Metal']
    if elem_a not in cycle or elem_b not in cycle:
        return 'unknown'

    idx_a = cycle.index(elem_a)
    idx_b = cycle.index(elem_b)

    # Distance in cycle (minimum)
    dist = min(abs(idx_a - idx_b), 5 - abs(idx_a - idx_b))

    if dist == 1:
        return 'adjacent'
    else:
        return 'opposite'

valid['element_relationship'] = valid.apply(
    lambda row: get_element_relationship(row['Element [A]'], row['Element [B]']),
    axis=1
)

print("="*70)
print("ELEMENT RELATIONSHIP FILTERING")
print("="*70)

print(f"\nTotal valid matchups: {len(valid)}\n")

# Category breakdown
categories = valid['element_relationship'].value_counts()
print("Matchup Categories:")
for cat, count in categories.items():
    pct = (count / len(valid)) * 100
    print(f"  {cat:>10}: {count:4.0f} ({pct:5.1f}%)")

# Test thresholds for each relationship category
thresholds = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]

relationships = ['same', 'opposite', 'adjacent']

print(f"\n{'='*70}")
print("THRESHOLD TESTING BY ELEMENT RELATIONSHIP")
print(f"{'='*70}")

results_by_rel = {}

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel].copy()

    if len(subset) == 0:
        continue

    print(f"\n{rel.upper()} ELEMENTS")
    print(f"Total: {len(subset)} matchups")
    print(f"{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
    print("-"*70)

    results_by_rel[rel] = []

    for threshold in thresholds:
        filtered = subset[subset['difference'] >= threshold].copy()

        if len(filtered) > 0:
            wins = len(filtered[filtered['correct'] == True])
            win_rate = (wins / len(filtered)) * 100

            results_by_rel[rel].append({
                'threshold': threshold,
                'qualified': len(filtered),
                'wins': wins,
                'win_rate': win_rate
            })

            print(f"    >= {threshold:5.1f}   {len(filtered):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# Find best threshold for each relationship
print(f"\n{'='*70}")
print("BEST THRESHOLD PER ELEMENT RELATIONSHIP")
print(f"{'='*70}")

best_results = {}

for rel in relationships:
    if results_by_rel.get(rel):
        df_rel = pd.DataFrame(results_by_rel[rel])
        best = df_rel.sort_values('win_rate', ascending=False).iloc[0]
        best_results[rel] = best

        print(f"\n{rel.upper()}:")
        print(f"  Optimal threshold: >= {best['threshold']:.1f}")
        print(f"  Qualified: {int(best['qualified'])}")
        print(f"  Win Rate: {best['win_rate']:.1f}%")

# Baseline comparison
print(f"\n{'='*70}")
print("BASELINE COMPARISONS (No filter, all thresholds)")
print(f"{'='*70}")

for rel in relationships:
    subset = valid[valid['element_relationship'] == rel]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        print(f"\n{rel.upper()} elements (no threshold):")
        print(f"  Matchups: {len(subset)}")
        print(f"  Win Rate: {win_rate:.1f}%")

# Combined strategy
print(f"\n{'='*70}")
print("COMBINED STRATEGY")
print(f"{'='*70}")

combined = pd.DataFrame()

for rel in relationships:
    if rel in best_results:
        best = best_results[rel]
        threshold = best['threshold']
        subset = valid[(valid['element_relationship'] == rel) & (valid['difference'] >= threshold)]
        combined = pd.concat([combined, subset])

if len(combined) > 0:
    wins = len(combined[combined['correct'] == True])
    win_rate = (wins / len(combined)) * 100

    print(f"\nApplying optimal threshold per element relationship:")
    print(f"  Total qualified: {len(combined)}")
    print(f"  Total wins: {wins}")
    print(f"  Overall win rate: {win_rate:.1f}%")

    # Show breakdown
    print(f"\n  Breakdown:")
    for rel in relationships:
        if rel in best_results:
            best = best_results[rel]
            subset = combined[combined['element_relationship'] == rel]
            if len(subset) > 0:
                sub_wins = len(subset[subset['correct'] == True])
                sub_rate = (sub_wins / len(subset)) * 100
                print(f"    {rel:>10} (>= {best['threshold']:.1f}): {len(subset):3.0f} qualified, {sub_wins:3.0f} wins, {sub_rate:5.1f}%")

# By condition
print(f"\n{'='*70}")
print("SAME ELEMENT BY CONDITION")
print(f"{'='*70}")

same_calm = valid[(valid['element_relationship'] == 'same') & (valid['condition'] == 'Calm')]
same_moderate = valid[(valid['element_relationship'] == 'same') & (valid['condition'] == 'Moderate')]

if len(same_calm) > 0:
    wins = len(same_calm[same_calm['correct'] == True])
    print(f"\nSame element + Calm: {len(same_calm)} matchups, {(wins/len(same_calm)*100):.1f}% win rate")

if len(same_moderate) > 0:
    wins = len(same_moderate[same_moderate['correct'] == True])
    print(f"Same element + Moderate: {len(same_moderate)} matchups, {(wins/len(same_moderate)*100):.1f}% win rate")

# Sample matchups
print(f"\n{'='*70}")
print("SAMPLE: Same Element Wins")
print(f"{'='*70}")

same_wins = valid[(valid['element_relationship'] == 'same') & (valid['correct'] == True)].head(10)

for idx, (_, row) in enumerate(same_wins.iterrows(), 1):
    print(f"{idx}. {row['Player A']} ({row['Element [A]']}) vs {row['Player B']} ({row['Element [B]']}) | {row['Condition']} {row['Round Type']} | Diff: {row['difference']:.2f}")
