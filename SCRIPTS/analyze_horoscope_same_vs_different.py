#!/usr/bin/env python3
"""
Compare same vs different Western horoscopes (like we did for Wu Xing elements).
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

# Define horoscope relationship
def get_horoscope_relationship(horo_a, horo_b):
    if horo_a == horo_b:
        return 'same'
    return 'different'

valid['horoscope_relationship'] = valid.apply(
    lambda row: get_horoscope_relationship(row['Horoscope [A]'], row['Horoscope [B]']),
    axis=1
)

print("="*70)
print("HOROSCOPE COMPARISON: SAME vs DIFFERENT")
print("="*70)

# Distribution
dist = valid['horoscope_relationship'].value_counts()
print(f"\nTotal valid matchups: {len(valid)}")
for rel, count in dist.items():
    pct = (count / len(valid)) * 100
    print(f"  {rel:>10}: {count:4.0f} ({pct:5.1f}%)")

# Same horoscopes
same_horo = valid[valid['horoscope_relationship'] == 'same']
same_horo_correct = same_horo[same_horo['correct'] == True]
same_horo_rate = (len(same_horo_correct) / len(same_horo) * 100) if len(same_horo) > 0 else 0

# Different horoscopes
diff_horo = valid[valid['horoscope_relationship'] == 'different']
diff_horo_correct = diff_horo[diff_horo['correct'] == True]
diff_horo_rate = (len(diff_horo_correct) / len(diff_horo) * 100) if len(diff_horo) > 0 else 0

print(f"\n{'='*70}")
print("BASELINE WIN RATES")
print(f"{'='*70}")

print(f"\nSame Horoscope: {same_horo_rate:.1f}% ({len(same_horo_correct)}/{len(same_horo)})")
print(f"Different Horoscope: {diff_horo_rate:.1f}% ({len(diff_horo_correct)}/{len(diff_horo)})")
print(f"Difference: {same_horo_rate - diff_horo_rate:.1f}pp")

# Threshold analysis for same horoscopes
print(f"\n{'='*70}")
print("SAME HOROSCOPE: THRESHOLD PROGRESSION")
print(f"{'='*70}")

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

for threshold in thresholds:
    above = same_horo[same_horo['difference'] >= threshold]
    if len(above) > 0:
        wins = len(above[above['correct'] == True])
        win_rate = (wins / len(above)) * 100
        print(f"    >= {threshold:5.1f}   {len(above):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# By condition
print(f"\n{'='*70}")
print("SAME HOROSCOPE BY CONDITION")
print(f"{'='*70}")

for cond in ['Calm', 'Moderate']:
    same_cond = same_horo[same_horo['condition'] == cond]
    if len(same_cond) > 0:
        wins = len(same_cond[same_cond['correct'] == True])
        rate = (wins / len(same_cond)) * 100
        print(f"\n{cond}: {rate:.1f}% ({wins}/{len(same_cond)})")

# By round type
print(f"\n{'='*70}")
print("SAME HOROSCOPE BY ROUND TYPE")
print(f"{'='*70}")

for rt in ['Open', 'Positioning', 'Closing']:
    same_rt = same_horo[same_horo['round_type'] == rt]
    if len(same_rt) > 0:
        wins = len(same_rt[same_rt['correct'] == True])
        rate = (wins / len(same_rt)) * 100
        print(f"\n{rt}: {rate:.1f}% ({wins}/{len(same_rt)})")

# Comparison with elements
print(f"\n{'='*70}")
print("COMPARISON: HOROSCOPE vs ELEMENT")
print(f"{'='*70}")

# Element same
def get_element_relationship(elem_a, elem_b):
    if elem_a == elem_b:
        return 'same'
    return 'different'

valid['element_relationship'] = valid.apply(
    lambda row: get_element_relationship(row['Element [A]'], row['Element [B]']),
    axis=1
)

same_elem = valid[valid['element_relationship'] == 'same']
same_elem_correct = same_elem[same_elem['correct'] == True]
same_elem_rate = (len(same_elem_correct) / len(same_elem) * 100) if len(same_elem) > 0 else 0

diff_elem = valid[valid['element_relationship'] == 'different']
diff_elem_correct = diff_elem[diff_elem['correct'] == True]
diff_elem_rate = (len(diff_elem_correct) / len(diff_elem) * 100) if len(diff_elem) > 0 else 0

print(f"\n{'Measure':>25} {'Horoscope':>15} {'Element':>15}")
print("-"*55)
print(f"{'Same':>25} {same_horo_rate:>14.1f}% {same_elem_rate:>14.1f}%")
print(f"{'Different':>25} {diff_horo_rate:>14.1f}% {diff_elem_rate:>14.1f}%")
print(f"{'Same - Different':>25} {same_horo_rate - diff_horo_rate:>14.1f}pp {same_elem_rate - diff_elem_rate:>14.1f}pp")
