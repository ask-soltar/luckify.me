#!/usr/bin/env python3
"""
Zodiac match (same + adjacent combined) with sample matchups by range.
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

# Create zodiac_match flag (same or adjacent)
valid['zodiac_match'] = valid['zodiac_relationship'].isin(['same', 'adjacent'])

# Filter to zodiac matches
zodiac_match = valid[valid['zodiac_match'] == True].copy()

print("="*80)
print("ZODIAC MATCH (Same + Adjacent): RANGES WITH SAMPLES")
print("="*80)

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
]

print(f"\nTotal zodiac match matchups: {len(zodiac_match)}\n")

print(f"{'Range':>12} {'Matchups':>10} {'Wins':>6} {'Win Rate':>10} {'Status':>10}")
print("-"*80)

results = []

for min_diff, max_diff in ranges:
    in_range = zodiac_match[(zodiac_match['difference'] >= min_diff) & (zodiac_match['difference'] < max_diff)]

    if len(in_range) > 0:
        wins = len(in_range[in_range['correct'] == True])
        win_rate = (wins / len(in_range)) * 100
        status = "WIN" if win_rate > 54 else ""

        results.append({
            'range': f"{min_diff:.1f}-{max_diff:.1f}",
            'matchups': len(in_range),
            'wins': wins,
            'win_rate': win_rate,
            'data': in_range
        })

        print(f"{min_diff:5.1f}-{max_diff:5.1f}  {len(in_range):10.0f} {wins:6.0f} {win_rate:9.1f}% {status:>10}")

# Show samples for each range
print(f"\n{'='*80}")
print("SAMPLE MATCHUPS BY RANGE")
print(f"{'='*80}")

for result in results:
    range_name = result['range']
    range_data = result['data']

    if len(range_data) == 0:
        continue

    wins = result['wins']
    losses = len(range_data) - wins

    print(f"\n{range_name} ({result['matchups']} total, {wins} wins, {result['win_rate']:.1f}%)")
    print("-" * 80)

    # Show up to 2 wins
    winning = range_data[range_data['correct'] == True]
    print(f"WIN examples (first 2):")
    for idx, (_, row) in enumerate(winning.head(2).iterrows(), 1):
        rel = row['zodiac_relationship']
        print(f"  {idx}. {row['Player A']} ({row['zodiac_a']}) vs {row['Player B']} ({row['zodiac_b']}) [{rel}]")
        print(f"     Diff: {row['difference']:.2f} | Condition: {row['condition']} | Round: {row['round_type']}")

    # Show up to 2 losses
    if losses > 0:
        losing = range_data[range_data['correct'] == False]
        print(f"LOSS examples (first 2):")
        for idx, (_, row) in enumerate(losing.head(2).iterrows(), 1):
            rel = row['zodiac_relationship']
            print(f"  {idx}. {row['Player A']} ({row['zodiac_a']}) vs {row['Player B']} ({row['zodiac_b']}) [{rel}]")
            print(f"     Diff: {row['difference']:.2f} | Condition: {row['condition']} | Round: {row['round_type']}")

# Summary statistics
print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")

df_results = pd.DataFrame(results)

# Ranges >54%
winning_ranges = df_results[df_results['win_rate'] > 54]
print(f"\nRanges >54%: {len(winning_ranges)} out of {len(df_results)}")
if len(winning_ranges) > 0:
    print(f"Ranges: {', '.join(winning_ranges['range'].tolist())}")

# Overall
total_matches = len(zodiac_match)
total_wins = len(zodiac_match[zodiac_match['correct'] == True])
overall_rate = (total_wins / total_matches) * 100
print(f"\nOVERALL: {total_wins}/{total_matches} = {overall_rate:.1f}%")

# Best and worst ranges
if len(df_results) > 0:
    best = df_results.loc[df_results['win_rate'].idxmax()]
    worst = df_results.loc[df_results['win_rate'].idxmin()]
    print(f"\nBest range: {best['range']} @ {best['win_rate']:.1f}% ({best['wins']}/{best['matchups']})")
    print(f"Worst range: {worst['range']} @ {worst['win_rate']:.1f}% ({worst['wins']}/{worst['matchups']})")

# Cumulative thresholds
print(f"\n{'='*80}")
print("CUMULATIVE: Minimum Threshold Performance")
print(f"{'='*80}")

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Win Rate':>10}")
print("-"*70)

for threshold in thresholds:
    above = zodiac_match[zodiac_match['difference'] >= threshold]
    if len(above) > 0:
        wins = len(above[above['correct'] == True])
        win_rate = (wins / len(above)) * 100
        print(f"    >= {threshold:5.1f}   {len(above):10.0f} {wins:6.0f} {win_rate:9.1f}%")
