#!/usr/bin/env python3
"""
Show how same element win rates progress with increasing thresholds.
Identify "tiers" of profitability.
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
print("SAME ELEMENT: THRESHOLD PROGRESSION ANALYSIS")
print("="*70)

thresholds = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]

print(f"\n{'Threshold':>10} {'Qualified':>10} {'Wins':>6} {'Losses':>6} {'Win Rate':>10} {'Change':>8} {'Tier':>12}")
print("-"*70)

results = []
prev_rate = None

for threshold in thresholds:
    above = same[same['difference'] >= threshold]

    if len(above) > 0:
        wins = len(above[above['correct'] == True])
        losses = len(above) - wins
        win_rate = (wins / len(above)) * 100

        # Calculate change from previous
        if prev_rate is not None:
            change = win_rate - prev_rate
            change_str = f"{change:+.1f}pp"
        else:
            change = 0
            change_str = "—"

        # Determine tier
        if win_rate >= 75:
            tier = "ELITE"
        elif win_rate >= 70:
            tier = "STRONG"
        elif win_rate >= 60:
            tier = "SOLID"
        else:
            tier = "WEAK"

        results.append({
            'threshold': threshold,
            'qualified': len(above),
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'change': change,
            'tier': tier
        })

        print(f"    >= {threshold:5.1f}   {len(above):10.0f} {wins:6.0f} {losses:6.0f} {win_rate:9.1f}% {change_str:>8} {tier:>12}")

        prev_rate = win_rate

# Analysis
print(f"\n{'='*70}")
print("TIER ANALYSIS")
print(f"{'='*70}")

df_results = pd.DataFrame(results)

# Find peaks
peak_rows = df_results[df_results['win_rate'] == df_results['win_rate'].max()]
print(f"\nPeaks:")
for _, row in peak_rows.iterrows():
    print(f"  >= {row['threshold']:.1f}: {row['win_rate']:.1f}% ({row['qualified']:.0f} qualified) - {row['tier']}")

# Find valleys
valley_rows = df_results[df_results['win_rate'] == df_results['win_rate'].min()]
print(f"\nValleys:")
for _, row in valley_rows.iterrows():
    print(f"  >= {row['threshold']:.1f}: {row['win_rate']:.1f}% ({row['qualified']:.0f} qualified) - {row['tier']}")

# Tier breakdown
print(f"\nThreshold Ranges by Tier:")

elite = df_results[df_results['tier'] == 'ELITE'].sort_values('threshold')
if len(elite) > 0:
    min_t = elite.iloc[0]['threshold']
    max_t = elite.iloc[-1]['threshold']
    print(f"  ELITE (>=75%): >= {min_t:.1f} to >= {max_t:.1f}")
    for _, row in elite.iterrows():
        print(f"    >= {row['threshold']:.1f}: {row['win_rate']:.1f}% ({row['qualified']:.0f} qualified)")

strong = df_results[df_results['tier'] == 'STRONG'].sort_values('threshold')
if len(strong) > 0:
    print(f"  STRONG (70-75%): {len(strong)} thresholds")

solid = df_results[df_results['tier'] == 'SOLID'].sort_values('threshold')
if len(solid) > 0:
    print(f"  SOLID (60-70%): {len(solid)} thresholds")

# Transition points
print(f"\n{'='*70}")
print("TRANSITION POINTS (Tier Changes)")
print(f"{'='*70}")

print(f"\nThreshold path:")
for idx, (_, row) in enumerate(df_results.iterrows()):
    if idx == 0:
        print(f"  >= {row['threshold']:.1f}: {row['tier']} ({row['win_rate']:.1f}%)")
    elif row['tier'] != df_results.iloc[idx-1]['tier']:
        prev_tier = df_results.iloc[idx-1]['tier']
        print(f"  >= {row['threshold']:.1f}: {prev_tier} -> {row['tier']} ({row['win_rate']:.1f}%)")
    elif idx == len(df_results) - 1:
        print(f"  >= {row['threshold']:.1f}: {row['tier']} ({row['win_rate']:.1f}%)")

# Profitability zones
print(f"\n{'='*70}")
print("PROFITABILITY ZONES")
print(f"{'='*70}")

print(f"\nZone 1: 0.0-1.5")
zone1 = df_results[df_results['threshold'] < 1.5]
if len(zone1) > 0:
    zone1_data = zone1.iloc[-1]
    print(f"  Peak at >= {zone1_data['threshold']:.1f}: {zone1_data['win_rate']:.1f}%")
    print(f"  Qualified: {zone1_data['qualified']:.0f}")

print(f"\nZone 2: 1.5-4.0")
zone2 = df_results[(df_results['threshold'] >= 1.5) & (df_results['threshold'] < 4.0)]
if len(zone2) > 0:
    worst_zone2 = zone2['win_rate'].min()
    best_zone2 = zone2['win_rate'].max()
    print(f"  Range: {worst_zone2:.1f}% to {best_zone2:.1f}%")
    print(f"  Note: Dip zone - declining from 1.5 peak")

print(f"\nZone 3: 4.0+")
zone3 = df_results[df_results['threshold'] >= 4.0]
if len(zone3) > 0:
    print(f"  Climbing zone - consistent improvement")
    for _, row in zone3.iterrows():
        print(f"    >= {row['threshold']:.1f}: {row['win_rate']:.1f}% ({row['qualified']:.0f} qualified)")

# Volume vs quality tradeoff
print(f"\n{'='*70}")
print("VOLUME vs QUALITY TRADEOFF")
print(f"{'='*70}")

print(f"\nHigh Volume, Good Quality:")
hv = df_results[(df_results['qualified'] >= 50) & (df_results['win_rate'] >= 65)]
for _, row in hv.iterrows():
    print(f"  >= {row['threshold']:.1f}: {row['win_rate']:.1f}% win rate, {row['qualified']:.0f} qualified")

print(f"\nLow Volume, High Quality:")
lv = df_results[(df_results['qualified'] < 50) & (df_results['win_rate'] >= 75)]
for _, row in lv.iterrows():
    print(f"  >= {row['threshold']:.1f}: {row['win_rate']:.1f}% win rate, {row['qualified']:.0f} qualified")
