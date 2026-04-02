"""
Analyze adj_his_par (adjusted historical par) performance for top 40 finishes.
Among Exec/Upside qualified players, how much does historical shrinkage matter?
"""

import pandas as pd
import numpy as np

# Load original ANALYSIS data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Filter: clean data
df_clean = df[df['round_type'] != 'REMOVE'].copy()

# Aggregate by player + venue
aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': 'mean',
    'upside': 'mean',
    'vs_avg': 'mean',
    'adj_his_par': 'mean',  # Shrinkage-adjusted historical par
    'player_hist_par': 'mean',  # Raw historical par
    'score': 'sum',
    'par': 'sum',
}).reset_index()

aggregated['off_par'] = aggregated['score'] - aggregated['par']

print("=" * 130)
print("ADJ_HIS_PAR PERFORMANCE ANALYSIS")
print("Among Exec/Upside qualified, how much does historical shrinkage predict top 40?")
print("=" * 130)

print(f"\nTotal player-tournaments: {len(aggregated)}")
print(f"adj_his_par range: {aggregated['adj_his_par'].min():.3f} - {aggregated['adj_his_par'].max():.3f}")
print(f"adj_his_par mean: {aggregated['adj_his_par'].mean():.3f}")

# First: filter by Exec/Upside thresholds (our validated model)
qualified = aggregated[
    (aggregated['exec'] >= 55) &
    (aggregated['upside'] >= 75)
].copy()

print(f"\nQualified by Exec >= 55 + Upside >= 75: {len(qualified)} player-tournaments")
print(f"Among qualified:")
print(f"  adj_his_par range: {qualified['adj_his_par'].min():.3f} - {qualified['adj_his_par'].max():.3f}")
print(f"  adj_his_par mean: {qualified['adj_his_par'].mean():.3f}")

# Analyze by adj_his_par deciles
print(f"\n{'=' * 130}")
print("ADJ_HIS_PAR DECILES (among Exec >= 55 + Upside >= 75 qualified players)")
print(f"{'=' * 130}\n")

# Create decile buckets
qualified['adj_his_par_decile'] = pd.qcut(qualified['adj_his_par'], q=10, labels=False, duplicates='drop')

decile_results = []

print(f"{'Decile':<10} {'Range':<25} {'Count':<8} {'Beat Avg %':<15} {'Top 40 %':<15} {'Avg Finish':<15}")
print("-" * 88)

for decile in sorted(qualified['adj_his_par_decile'].dropna().unique()):
    decile_data = qualified[qualified['adj_his_par_decile'] == decile]

    if len(decile_data) < 1:
        continue

    adj_min = decile_data['adj_his_par'].min()
    adj_max = decile_data['adj_his_par'].max()

    beat_avg = (decile_data['vs_avg'] > 0).sum() / len(decile_data)

    # Top 40 accuracy
    venue_top40 = []

    for venue in decile_data['event_name'].unique():
        venue_all = aggregated[aggregated['event_name'] == venue]
        venue_decile = decile_data[decile_data['event_name'] == venue]

        if len(venue_all) < 20 or len(venue_decile) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['finish_rank'] = venue_all_ranked['vs_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        decile_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_decile['player_name'])]

        if len(decile_ranked) > 0:
            in_top40 = (decile_ranked['finish_rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(decile_ranked)
            venue_top40.append(accuracy)

    if venue_top40:
        avg_accuracy = np.mean(venue_top40)
        avg_finish = decile_data['vs_avg'].mean()

        decile_results.append({
            'decile': decile,
            'min': adj_min,
            'max': adj_max,
            'count': len(decile_data),
            'beat_avg': beat_avg,
            'top40_accuracy': avg_accuracy,
            'avg_finish': avg_finish
        })

        range_str = f"{adj_min:.3f}-{adj_max:.3f}"
        print(f"{decile:<10} {range_str:<25} {len(decile_data):<8} {beat_avg:<15.1%} {avg_accuracy:<15.1%} {avg_finish:<15.3f}")

# Analysis by tertiles (thirds)
print(f"\n{'=' * 130}")
print("ADJ_HIS_PAR TERTILES: Low vs Mid vs High (among Exec >= 55 + Upside >= 75)")
print(f"{'=' * 130}\n")

qualified['adj_his_par_tertile'] = pd.qcut(qualified['adj_his_par'], q=3, labels=['Low', 'Mid', 'High'], duplicates='drop')

tertile_results = []

print(f"{'Tertile':<12} {'Range':<25} {'Count':<8} {'Beat Avg %':<15} {'Top 40 %':<15} {'Avg Finish':<15}")
print("-" * 90)

for tertile in ['Low', 'Mid', 'High']:
    tertile_data = qualified[qualified['adj_his_par_tertile'] == tertile]

    if len(tertile_data) < 1:
        continue

    adj_min = tertile_data['adj_his_par'].min()
    adj_max = tertile_data['adj_his_par'].max()

    beat_avg = (tertile_data['vs_avg'] > 0).sum() / len(tertile_data)

    venue_top40 = []

    for venue in tertile_data['event_name'].unique():
        venue_all = aggregated[aggregated['event_name'] == venue]
        venue_tertile = tertile_data[tertile_data['event_name'] == venue]

        if len(venue_all) < 20 or len(venue_tertile) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['finish_rank'] = venue_all_ranked['vs_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        tertile_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_tertile['player_name'])]

        if len(tertile_ranked) > 0:
            in_top40 = (tertile_ranked['finish_rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(tertile_ranked)
            venue_top40.append(accuracy)

    if venue_top40:
        avg_accuracy = np.mean(venue_top40)
        avg_finish = tertile_data['vs_avg'].mean()

        tertile_results.append({
            'tertile': tertile,
            'min': adj_min,
            'max': adj_max,
            'count': len(tertile_data),
            'beat_avg': beat_avg,
            'top40_accuracy': avg_accuracy,
            'avg_finish': avg_finish
        })

        range_str = f"{adj_min:.3f}-{adj_max:.3f}"
        print(f"{tertile:<12} {range_str:<25} {len(tertile_data):<8} {beat_avg:<15.1%} {avg_accuracy:<15.1%} {avg_finish:<15.3f}")

# Summary
print(f"\n{'=' * 130}")
print("SUMMARY & INTERPRETATION")
print(f"{'=' * 130}\n")

if tertile_results:
    tertile_df = pd.DataFrame(tertile_results)

    low = tertile_df[tertile_df['tertile'] == 'Low'].iloc[0]
    high = tertile_df[tertile_df['tertile'] == 'High'].iloc[0]

    print(f"LOW adj_his_par ({low['min']:.3f} to {low['max']:.3f}):")
    print(f"  Top 40 finish rate: {low['top40_accuracy']:.1%}")
    print(f"  Beat avg: {low['beat_avg']:.1%}")
    print(f"  Avg vs_avg: {low['avg_finish']:.3f}")
    print(f"  Sample: {low['count']:.0f} player-tournaments")

    print(f"\nHIGH adj_his_par ({high['min']:.3f} to {high['max']:.3f}):")
    print(f"  Top 40 finish rate: {high['top40_accuracy']:.1%}")
    print(f"  Beat avg: {high['beat_avg']:.1%}")
    print(f"  Avg vs_avg: {high['avg_finish']:.3f}")
    print(f"  Sample: {high['count']:.0f} player-tournaments")

    improvement = (high['top40_accuracy'] - low['top40_accuracy'])
    print(f"\nDifference (High vs Low):")
    print(f"  Top 40 rate improvement: {improvement:+.1%}")
    print(f"  Finish quality improvement: {high['avg_finish'] - low['avg_finish']:+.3f}")

    if improvement > 0.05:
        print(f"\n[YES] Historical par matters: High adj_his_par significantly better")
    elif improvement > 0.01:
        print(f"\n[MODEST] Historical par has small effect")
    else:
        print(f"\n[NO] Historical par doesn't add much: Exec/Upside dominates")

print("\n")
