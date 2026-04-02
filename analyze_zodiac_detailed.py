#!/usr/bin/env python3
"""
Detailed zodiac analysis: same vs adjacent vs opposite.
Chinese zodiac is a 12-year cycle: Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig.
Adjacent = 1 step in cycle; Opposite = 6 steps (opposite side of wheel).
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
    # Calculate distance (minimum of forward and backward)
    dist = min(abs(idx_a - idx_b), 12 - abs(idx_a - idx_b))
    if dist == 1:
        return 'adjacent'
    elif dist == 6:
        return 'opposite'
    else:
        return 'other'

valid['zodiac_relationship'] = valid.apply(
    lambda row: get_zodiac_relationship(row['zodiac_a'], row['zodiac_b']),
    axis=1
)

print("="*70)
print("CHINESE ZODIAC: DETAILED ANALYSIS")
print("="*70)

# Distribution
dist = valid['zodiac_relationship'].value_counts()
print(f"\nTotal matchups: {len(valid)}")
for rel, count in dist.items():
    pct = (count / len(valid)) * 100
    print(f"  {rel:>10}: {count:4.0f} ({pct:5.1f}%)")

# Baseline by relationship
print(f"\n{'='*70}")
print("BASELINE WIN RATES BY RELATIONSHIP")
print(f"{'='*70}")

for rel in ['same', 'adjacent', 'opposite', 'other']:
    subset = valid[valid['zodiac_relationship'] == rel]
    if len(subset) > 0:
        wins = len(subset[subset['correct'] == True])
        rate = (wins / len(subset)) * 100
        print(f"\n{rel.upper():>10}: {rate:.1f}% ({wins}/{len(subset)})")

# Deep dive: SAME ZODIAC by condition and round type
same_z = valid[valid['zodiac_relationship'] == 'same']

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

# Same zodiac by condition and round type
print(f"\n{'='*70}")
print("SAME ZODIAC: CONDITION x ROUND TYPE BREAKDOWN")
print(f"{'='*70}")

print(f"\nOVERALL: {len(same_z)} matchups, {len(same_z[same_z['correct']==True])} wins, {len(same_z[same_z['correct']==True])/len(same_z)*100:.1f}%\n")

print("BY ROUND TYPE:")
print(f"{'Type':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for rt in ['Open', 'Positioning', 'Closing']:
    rt_data = same_z[same_z['round_type'] == rt]
    if len(rt_data) > 0:
        rt_wins = len(rt_data[rt_data['correct'] == True])
        rt_rate = (rt_wins / len(rt_data)) * 100
        print(f"{rt:>12} {len(rt_data):>10.0f} {rt_wins:>6.0f} {rt_rate:>9.1f}%")

print(f"\nBY CONDITION:")
print(f"{'Condition':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for cond in ['Calm', 'Moderate']:
    cond_data = same_z[same_z['condition'] == cond]
    if len(cond_data) > 0:
        cond_wins = len(cond_data[cond_data['correct'] == True])
        cond_rate = (cond_wins / len(cond_data)) * 100
        print(f"{cond:>12} {len(cond_data):>10.0f} {cond_wins:>6.0f} {cond_rate:>9.1f}%")

# Cross-tabulation
print(f"\nCONDITION x ROUND TYPE:")
print(f"\n{'Type':>12} {'Calm':>12} {'Moderate':>12}")
print("-"*40)

for rt in ['Open', 'Positioning', 'Closing']:
    calm_data = same_z[(same_z['round_type'] == rt) & (same_z['condition'] == 'Calm')]
    moderate_data = same_z[(same_z['round_type'] == rt) & (same_z['condition'] == 'Moderate')]

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

# ADJACENT ZODIAC analysis
print(f"\n{'='*70}")
print("ADJACENT ZODIAC (1 step in cycle)")
print(f"{'='*70}")

adjacent_z = valid[valid['zodiac_relationship'] == 'adjacent']

print(f"\nOVERALL: {len(adjacent_z)} matchups, {len(adjacent_z[adjacent_z['correct']==True])} wins, {len(adjacent_z[adjacent_z['correct']==True])/len(adjacent_z)*100:.1f}%\n")

print("BY ROUND TYPE:")
print(f"{'Type':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for rt in ['Open', 'Positioning', 'Closing']:
    rt_data = adjacent_z[adjacent_z['round_type'] == rt]
    if len(rt_data) > 0:
        rt_wins = len(rt_data[rt_data['correct'] == True])
        rt_rate = (rt_wins / len(rt_data)) * 100
        print(f"{rt:>12} {len(rt_data):>10.0f} {rt_wins:>6.0f} {rt_rate:>9.1f}%")

print(f"\nBY CONDITION:")
print(f"{'Condition':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for cond in ['Calm', 'Moderate']:
    cond_data = adjacent_z[adjacent_z['condition'] == cond]
    if len(cond_data) > 0:
        cond_wins = len(cond_data[cond_data['correct'] == True])
        cond_rate = (cond_wins / len(cond_data)) * 100
        print(f"{cond:>12} {len(cond_data):>10.0f} {cond_wins:>6.0f} {cond_rate:>9.1f}%")

# OPPOSITE ZODIAC analysis
print(f"\n{'='*70}")
print("OPPOSITE ZODIAC (6 steps in cycle, opposite side)")
print(f"{'='*70}")

opposite_z = valid[valid['zodiac_relationship'] == 'opposite']

print(f"\nOVERALL: {len(opposite_z)} matchups, {len(opposite_z[opposite_z['correct']==True])} wins, {len(opposite_z[opposite_z['correct']==True])/len(opposite_z)*100:.1f}%\n")

print("BY ROUND TYPE:")
print(f"{'Type':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for rt in ['Open', 'Positioning', 'Closing']:
    rt_data = opposite_z[opposite_z['round_type'] == rt]
    if len(rt_data) > 0:
        rt_wins = len(rt_data[rt_data['correct'] == True])
        rt_rate = (rt_wins / len(rt_data)) * 100
        print(f"{rt:>12} {len(rt_data):>10.0f} {rt_wins:>6.0f} {rt_rate:>9.1f}%")

print(f"\nBY CONDITION:")
print(f"{'Condition':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*40)

for cond in ['Calm', 'Moderate']:
    cond_data = opposite_z[opposite_z['condition'] == cond]
    if len(cond_data) > 0:
        cond_wins = len(cond_data[cond_data['correct'] == True])
        cond_rate = (cond_wins / len(cond_data)) * 100
        print(f"{cond:>12} {len(cond_data):>10.0f} {cond_wins:>6.0f} {cond_rate:>9.1f}%")

# Comparison
print(f"\n{'='*70}")
print("COMPARISON: SAME vs ADJACENT vs OPPOSITE")
print(f"{'='*70}")

same_rate = len(same_z[same_z['correct']==True]) / len(same_z) * 100 if len(same_z) > 0 else 0
adj_rate = len(adjacent_z[adjacent_z['correct']==True]) / len(adjacent_z) * 100 if len(adjacent_z) > 0 else 0
opp_rate = len(opposite_z[opposite_z['correct']==True]) / len(opposite_z) * 100 if len(opposite_z) > 0 else 0

print(f"\n{'Relationship':>20} {'Win Rate':>15} {'Advantage vs Different':>25}")
print("-"*60)

diff_z = valid[valid['zodiac_relationship'] == 'different']
diff_rate = len(diff_z[diff_z['correct']==True]) / len(diff_z) * 100 if len(diff_z) > 0 else 0

print(f"{'Same':>20} {same_rate:>14.1f}% {same_rate - diff_rate:>24.1f}pp")
print(f"{'Adjacent':>20} {adj_rate:>14.1f}% {adj_rate - diff_rate:>24.1f}pp")
print(f"{'Opposite':>20} {opp_rate:>14.1f}% {opp_rate - diff_rate:>24.1f}pp")
print(f"{'Different':>20} {diff_rate:>14.1f}% {0:>24.1f}pp")

# Conclusion
print(f"\n{'='*70}")
print("CONCLUSION")
print(f"{'='*70}")
print(f"\nZodiac relationships: {same_rate - diff_rate:.1f}pp advantage for SAME")
if abs(adj_rate - same_rate) < 3:
    print(f"Adjacent performs similarly to same ({adj_rate:.1f}%), suggesting no adjacent effect")
else:
    print(f"Adjacent shows different pattern: {adj_rate:.1f}% (diff of {adj_rate - same_rate:.1f}pp)")
