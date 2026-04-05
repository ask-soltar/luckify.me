#!/usr/bin/env python3
"""
Analyze prediction accuracy by Wu Xing Element.
"""

import pandas as pd

# Load matchup data
matchups = pd.read_csv('matchup.csv')

# Load scored results
scored = pd.read_csv('2ball_scored_35_65.csv')

# Merge
merged = matchups.merge(
    scored[['player_a', 'player_b', 'correct']],
    left_on=['Player A', 'Player B'],
    right_on=['player_a', 'player_b'],
    how='left'
)

# Filter valid (with outcomes)
valid = merged[merged['correct'].notna()].copy()

print("="*70)
print("WU XING ELEMENT ANALYSIS")
print("="*70)

print(f"\nTotal valid matchups: {len(valid)}\n")

# Pattern 1: Win rate by individual element
print("="*70)
print("WIN RATE BY PLAYER ELEMENT (Player A)")
print("="*70)

elements = valid['Element [A]'].unique()
elements_sorted = sorted([e for e in elements if pd.notna(e)])

for element in elements_sorted:
    subset = valid[valid['Element [A]'] == element]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        print(f"{element:>8}: {len(subset):3.0f} matchups, {wins:3.0f} wins, {win_rate:5.1f}% win rate")

# Pattern 2: Element pairings (A vs B)
print(f"\n" + "="*70)
print("WIN RATE BY ELEMENT PAIRING (A element vs B element)")
print("="*70)

pairings = []

for elem_a in elements_sorted:
    for elem_b in elements_sorted:
        subset = valid[(valid['Element [A]'] == elem_a) & (valid['Element [B]'] == elem_b)]
        if len(subset) >= 5:  # Only show if at least 5 samples
            wins = len(subset[subset['correct'] == True])
            win_rate = (wins / len(subset)) * 100
            pairings.append({
                'elem_a': elem_a,
                'elem_b': elem_b,
                'matchups': len(subset),
                'wins': wins,
                'win_rate': win_rate
            })

# Sort by win rate descending
pairings_df = pd.DataFrame(pairings).sort_values('win_rate', ascending=False)

print(f"\n{'A Element':>8} {'B Element':>8} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

for _, row in pairings_df.head(15).iterrows():
    print(f"{row['elem_a']:>8} {row['elem_b']:>8} {row['matchups']:>10.0f} {row['wins']:>6.0f} {row['win_rate']:>9.1f}%")

print(f"\n... (showing top 15 of {len(pairings_df)} total pairings)\n")

# Pattern 3: Element relationships (5-element cycle)
print("="*70)
print("ELEMENT CYCLE RELATIONSHIPS (Wu Xing Theory)")
print("="*70)

# Wu Xing cycle: Wood > Earth > Water > Fire > Metal > Wood
# (each element controls the next)

element_cycle = {
    'Wood': {'controls': 'Earth', 'controlled_by': 'Metal'},
    'Earth': {'controls': 'Water', 'controlled_by': 'Wood'},
    'Water': {'controls': 'Fire', 'controlled_by': 'Earth'},
    'Fire': {'controls': 'Metal', 'controlled_by': 'Water'},
    'Metal': {'controls': 'Wood', 'controlled_by': 'Fire'}
}

print(f"\nWu Xing Dominance (A controls B - does A win more?):\n")

for elem_a, rules in element_cycle.items():
    elem_b_controlled = rules['controls']
    subset = valid[(valid['Element [A]'] == elem_a) & (valid['Element [B]'] == elem_b_controlled)]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        print(f"  {elem_a:>6} vs {elem_b_controlled:>6} ({elem_a} controls): {len(subset):3.0f} matchups, {win_rate:5.1f}% win rate")

print(f"\nWu Xing Weakness (A is controlled by B - does A win less?):\n")

for elem_a, rules in element_cycle.items():
    elem_b_controlling = rules['controlled_by']
    subset = valid[(valid['Element [A]'] == elem_a) & (valid['Element [B]'] == elem_b_controlling)]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        win_rate = (wins / len(subset)) * 100
        print(f"  {elem_a:>6} vs {elem_b_controlling:>6} ({elem_b_controlling} controls {elem_a}): {len(subset):3.0f} matchups, {win_rate:5.1f}% win rate")

# Pattern 4: Same element vs different
print(f"\n" + "="*70)
print("SAME ELEMENT vs DIFFERENT")
print("="*70)

same_elem = valid[valid['Element [A]'] == valid['Element [B]']]
diff_elem = valid[valid['Element [A]'] != valid['Element [B]']]

if len(same_elem) > 0:
    wins_same = len(same_elem[same_elem['correct'] == True])
    rate_same = (wins_same / len(same_elem)) * 100
    print(f"\nSame element:")
    print(f"  Matchups: {len(same_elem)}")
    print(f"  Win rate: {rate_same:.1f}%")

if len(diff_elem) > 0:
    wins_diff = len(diff_elem[diff_elem['correct'] == True])
    rate_diff = (wins_diff / len(diff_elem)) * 100
    print(f"\nDifferent elements:")
    print(f"  Matchups: {len(diff_elem)}")
    print(f"  Win rate: {rate_diff:.1f}%")

# Pattern 5: Element by condition
print(f"\n" + "="*70)
print("ELEMENT PERFORMANCE BY CONDITION (Top 3)")
print("="*70)

for condition in ['Calm', 'Moderate']:
    subset_cond = valid[valid['Condition'] == condition]
    if len(subset_cond) > 0:
        print(f"\n{condition}:")

        elem_performance = []
        for element in elements_sorted:
            elem_subset = subset_cond[subset_cond['Element [A]'] == element]
            if len(elem_subset) >= 10:
                wins = len(elem_subset[elem_subset['correct'] == True])
                win_rate = (wins / len(elem_subset)) * 100
                elem_performance.append({
                    'element': element,
                    'matchups': len(elem_subset),
                    'wins': wins,
                    'win_rate': win_rate
                })

        elem_df = pd.DataFrame(elem_performance).sort_values('win_rate', ascending=False)
        for _, row in elem_df.head(3).iterrows():
            print(f"  {row['element']:>8}: {row['matchups']:3.0f} matchups, {row['win_rate']:5.1f}% win rate")
