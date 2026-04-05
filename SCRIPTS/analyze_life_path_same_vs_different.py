#!/usr/bin/env python3
"""
Compare same vs different Life Path numbers (like elements and horoscopes).
Pulls life path from Golf_Analytics and merges with matchup data.
"""

import pandas as pd

# Load data
matchups = pd.read_csv('matchup.csv')
scored = pd.read_csv('2ball_scored_35_65.csv')

# Try to load Golf_Analytics with life path
try:
    ga = pd.read_csv('ANALYSIS_v3_export.csv')
    print("Loaded ANALYSIS_v3_export.csv")
except:
    try:
        ga = pd.read_csv('analysis_v2_with_life_path.csv')
        print("Loaded analysis_v2_with_life_path.csv")
    except:
        print("ERROR: Could not find export with life path data")
        exit(1)

# Extract player -> life path mapping
player_col = 'player_name'
life_path_col = 'life_path'

# Verify columns exist
if player_col not in ga.columns or life_path_col not in ga.columns:
    print(f"ERROR: Missing columns")
    print(f"Available: {list(ga.columns)}")
    exit(1)

# Build mapping (take first occurrence of each player)
player_life_path = ga[[player_col, life_path_col]].drop_duplicates(subset=[player_col]).set_index(player_col)[life_path_col].to_dict()

print(f"Loaded life path data for {len(player_life_path)} players")

# Merge with matchup data
merged = matchups.merge(
    scored[['player_a', 'player_b', 'correct', 'difference', 'condition', 'round_type']],
    left_on=['Player A', 'Player B'],
    right_on=['player_a', 'player_b'],
    how='left'
)

# Filter valid
valid = merged[merged['correct'].notna()].copy()

# Add life path for both players
valid['life_path_a'] = valid['Player A'].map(player_life_path)
valid['life_path_b'] = valid['Player B'].map(player_life_path)

# Filter out rows where life path is missing
valid = valid[(valid['life_path_a'].notna()) & (valid['life_path_b'].notna())].copy()

print(f"Matched {len(valid)} matchups with life path data\n")

# Define life path relationship
def get_life_path_relationship(lp_a, lp_b):
    if lp_a == lp_b:
        return 'same'
    return 'different'

valid['life_path_relationship'] = valid.apply(
    lambda row: get_life_path_relationship(row['life_path_a'], row['life_path_b']),
    axis=1
)

print("="*70)
print("LIFE PATH COMPARISON: SAME vs DIFFERENT")
print("="*70)

# Distribution
dist = valid['life_path_relationship'].value_counts()
print(f"\nTotal matchups with life path data: {len(valid)}")
for rel, count in dist.items():
    pct = (count / len(valid)) * 100
    print(f"  {rel:>10}: {count:4.0f} ({pct:5.1f}%)")

# Same life path
same_lp = valid[valid['life_path_relationship'] == 'same']
same_lp_correct = same_lp[same_lp['correct'] == True]
same_lp_rate = (len(same_lp_correct) / len(same_lp) * 100) if len(same_lp) > 0 else 0

# Different life path
diff_lp = valid[valid['life_path_relationship'] == 'different']
diff_lp_correct = diff_lp[diff_lp['correct'] == True]
diff_lp_rate = (len(diff_lp_correct) / len(diff_lp) * 100) if len(diff_lp) > 0 else 0

print(f"\n{'='*70}")
print("BASELINE WIN RATES")
print(f"{'='*70}")

print(f"\nSame Life Path: {same_lp_rate:.1f}% ({len(same_lp_correct)}/{len(same_lp)})")
print(f"Different Life Path: {diff_lp_rate:.1f}% ({len(diff_lp_correct)}/{len(diff_lp)})")
print(f"Difference: {same_lp_rate - diff_lp_rate:.1f}pp")

# Threshold analysis for same life path
print(f"\n{'='*70}")
print("SAME LIFE PATH: THRESHOLD PROGRESSION")
print(f"{'='*70}")

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

for threshold in thresholds:
    above = same_lp[same_lp['difference'] >= threshold]
    if len(above) > 0:
        wins = len(above[above['correct'] == True])
        win_rate = (wins / len(above)) * 100
        print(f"    >= {threshold:5.1f}   {len(above):10.0f} {wins:6.0f} {win_rate:9.1f}%")

# By condition
print(f"\n{'='*70}")
print("SAME LIFE PATH BY CONDITION")
print(f"{'='*70}")

for cond in ['Calm', 'Moderate']:
    same_cond = same_lp[same_lp['condition'] == cond]
    if len(same_cond) > 0:
        wins = len(same_cond[same_cond['correct'] == True])
        rate = (wins / len(same_cond)) * 100
        print(f"\n{cond}: {rate:.1f}% ({wins}/{len(same_cond)})")

# Comparison with elements
print(f"\n{'='*70}")
print("COMPARISON: LIFE PATH vs ELEMENT vs HOROSCOPE")
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

# Horoscope same
def get_horoscope_relationship(horo_a, horo_b):
    if horo_a == horo_b:
        return 'same'
    return 'different'

valid['horoscope_relationship'] = valid.apply(
    lambda row: get_horoscope_relationship(row['Horoscope [A]'], row['Horoscope [B]']),
    axis=1
)

same_horo = valid[valid['horoscope_relationship'] == 'same']
same_horo_correct = same_horo[same_horo['correct'] == True]
same_horo_rate = (len(same_horo_correct) / len(same_horo) * 100) if len(same_horo) > 0 else 0

diff_horo = valid[valid['horoscope_relationship'] == 'different']
diff_horo_correct = diff_horo[diff_horo['correct'] == True]
diff_horo_rate = (len(diff_horo_correct) / len(diff_horo) * 100) if len(diff_horo) > 0 else 0

print(f"\n{'Measure':>25} {'Life Path':>15} {'Element':>15} {'Horoscope':>15}")
print("-"*70)
print(f"{'Same':>25} {same_lp_rate:>14.1f}% {same_elem_rate:>14.1f}% {same_horo_rate:>14.1f}%")
print(f"{'Different':>25} {diff_lp_rate:>14.1f}% {diff_elem_rate:>14.1f}% {diff_horo_rate:>14.1f}%")
print(f"{'Same - Different':>25} {same_lp_rate - diff_lp_rate:>14.1f}pp {same_elem_rate - diff_elem_rate:>14.1f}pp {same_horo_rate - diff_horo_rate:>14.1f}pp")
