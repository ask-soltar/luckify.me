"""
CORRECTED ANALYSIS: Filter by Exec/Upside, then check ACTUAL finish position.
Actual finish = how they beat/missed field average across 4 rounds (vs_avg_mean).
"""

import pandas as pd
import numpy as np

# Load aggregated data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[df['round_type'] != 'REMOVE'].copy()

# Aggregate by player + venue
aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': 'mean',
    'upside': 'mean',
    'vs_avg': 'mean',  # This is ACTUAL tournament finish
    'score': 'sum',
    'par': 'sum',
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated['off_par'] = aggregated['score'] - aggregated['par']

print("=" * 130)
print("CORRECTED THRESHOLD ANALYSIS")
print("Filter by Avg Exec/Upside, check ACTUAL finish position (vs_avg_mean)")
print("=" * 130)

print(f"\nTotal player-tournaments: {len(aggregated)}")
print(f"Avg Exec range: {aggregated['exec'].min():.1f} - {aggregated['exec'].max():.1f} (mean: {aggregated['exec'].mean():.1f})")
print(f"Avg Upside range: {aggregated['upside'].min():.1f} - {aggregated['upside'].max():.1f} (mean: {aggregated['upside'].mean():.1f})")
print(f"vs_avg (finish quality): {aggregated['vs_avg'].min():.2f} - {aggregated['vs_avg'].max():.2f} (mean: {aggregated['vs_avg'].mean():.2f})")

# Test Exec thresholds
print(f"\n{'=' * 130}")
print("THRESHOLD ANALYSIS: Avg Exec (check ACTUAL finish position)")
print(f"{'=' * 130}\n")

exec_thresholds = [40, 45, 50, 55, 60, 65, 70]
exec_results = []

print(f"{'Exec >= ?':<12} {'Count':<10} {'Beat Avg %':<15} {'Top 40 %':<15} {'Avg Finish':<15}")
print("-" * 67)

for threshold in exec_thresholds:
    filtered = aggregated[aggregated['exec'] >= threshold].copy()

    if len(filtered) < 10:
        continue

    # Count how many beat field average (positive vs_avg)
    beat_avg = (filtered['vs_avg'] > 0).sum() / len(filtered)

    # Venue-by-venue: rank all by actual finish, see how many filtered players are top 40
    top40_accuracy = []

    for venue in aggregated['event_name'].unique():
        venue_all = aggregated[aggregated['event_name'] == venue]
        venue_filtered = filtered[filtered['event_name'] == venue]

        if len(venue_all) < 20 or len(venue_filtered) == 0:
            continue

        # Rank by ACTUAL finish (vs_avg)
        venue_all_ranked = venue_all.copy()
        venue_all_ranked['finish_rank'] = venue_all_ranked['vs_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        # Check how many filtered players are in top 40 of actual finish
        filtered_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_filtered['player_name'])]

        if len(filtered_ranked) > 0:
            in_top40 = (filtered_ranked['finish_rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(filtered_ranked)
            top40_accuracy.append(accuracy)

    if top40_accuracy:
        avg_accuracy = np.mean(top40_accuracy)
        avg_finish = filtered['vs_avg'].mean()

        exec_results.append({
            'threshold': threshold,
            'count': len(filtered),
            'beat_avg': beat_avg,
            'top40_accuracy': avg_accuracy,
            'avg_finish': avg_finish
        })

        print(f"{threshold:<12} {len(filtered):<10} {beat_avg:<15.1%} {avg_accuracy:<15.1%} {avg_finish:<15.3f}")

# Test Upside thresholds
print(f"\n{'=' * 130}")
print("THRESHOLD ANALYSIS: Avg Upside (check ACTUAL finish position)")
print(f"{'=' * 130}\n")

upside_thresholds = [60, 65, 70, 75, 80, 85]
upside_results = []

print(f"{'Upside >= ?':<12} {'Count':<10} {'Beat Avg %':<15} {'Top 40 %':<15} {'Avg Finish':<15}")
print("-" * 67)

for threshold in upside_thresholds:
    filtered = aggregated[aggregated['upside'] >= threshold].copy()

    if len(filtered) < 10:
        continue

    beat_avg = (filtered['vs_avg'] > 0).sum() / len(filtered)

    top40_accuracy = []

    for venue in aggregated['event_name'].unique():
        venue_all = aggregated[aggregated['event_name'] == venue]
        venue_filtered = filtered[filtered['event_name'] == venue]

        if len(venue_all) < 20 or len(venue_filtered) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['finish_rank'] = venue_all_ranked['vs_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        filtered_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_filtered['player_name'])]

        if len(filtered_ranked) > 0:
            in_top40 = (filtered_ranked['finish_rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(filtered_ranked)
            top40_accuracy.append(accuracy)

    if top40_accuracy:
        avg_accuracy = np.mean(top40_accuracy)
        avg_finish = filtered['vs_avg'].mean()

        upside_results.append({
            'threshold': threshold,
            'count': len(filtered),
            'beat_avg': beat_avg,
            'top40_accuracy': avg_accuracy,
            'avg_finish': avg_finish
        })

        print(f"{threshold:<12} {len(filtered):<10} {beat_avg:<15.1%} {avg_accuracy:<15.1%} {avg_finish:<15.3f}")

# Combined thresholds
print(f"\n{'=' * 130}")
print("COMBINED THRESHOLDS: Avg Exec × Avg Upside (check ACTUAL finish)")
print(f"{'=' * 130}\n")

combined_results = []

print(f"{'Exec >= ?':<12} {'Upside >= ?':<14} {'Count':<10} {'Beat Avg %':<15} {'Top 40 %':<15}")
print("-" * 66)

for exec_thresh in [50, 55, 60, 65]:
    for upside_thresh in [65, 70, 75, 80]:
        filtered = aggregated[
            (aggregated['exec'] >= exec_thresh) &
            (aggregated['upside'] >= upside_thresh)
        ].copy()

        if len(filtered) < 10:
            continue

        beat_avg = (filtered['vs_avg'] > 0).sum() / len(filtered)

        top40_accuracy = []

        for venue in aggregated['event_name'].unique():
            venue_all = aggregated[aggregated['event_name'] == venue]
            venue_filtered = filtered[filtered['event_name'] == venue]

            if len(venue_all) < 20 or len(venue_filtered) == 0:
                continue

            venue_all_ranked = venue_all.copy()
            venue_all_ranked['finish_rank'] = venue_all_ranked['vs_avg'].rank(ascending=False)

            field_size = len(venue_all_ranked)
            top40_cutoff = max(10, int(field_size * 0.33))

            filtered_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_filtered['player_name'])]

            if len(filtered_ranked) > 0:
                in_top40 = (filtered_ranked['finish_rank'] <= top40_cutoff).sum()
                accuracy = in_top40 / len(filtered_ranked)
                top40_accuracy.append(accuracy)

        if top40_accuracy:
            avg_accuracy = np.mean(top40_accuracy)

            combined_results.append({
                'exec': exec_thresh,
                'upside': upside_thresh,
                'count': len(filtered),
                'beat_avg': beat_avg,
                'top40_accuracy': avg_accuracy
            })

            print(f"{exec_thresh:<12} {upside_thresh:<14} {len(filtered):<10} {beat_avg:<15.1%} {avg_accuracy:<15.1%}")

# Summary
print(f"\n{'=' * 130}")
print("SUMMARY & INTERPRETATION")
print(f"{'=' * 130}\n")

if exec_results:
    exec_df = pd.DataFrame(exec_results)
    print("AVG EXEC Scaling:")
    print(f"  Lowest threshold (40): {exec_df.iloc[0]['top40_accuracy']:.1%} in top 40")
    print(f"  Highest threshold (70): {exec_df.iloc[-1]['top40_accuracy']:.1%} in top 40")
    improvement = (exec_df.iloc[-1]['top40_accuracy'] - exec_df.iloc[0]['top40_accuracy'])
    print(f"  Improvement: {improvement:+.1%}")

if upside_results:
    upside_df = pd.DataFrame(upside_results)
    print("\nAVG UPSIDE Scaling:")
    print(f"  Lowest threshold (60): {upside_df.iloc[0]['top40_accuracy']:.1%} in top 40")
    print(f"  Highest threshold (85): {upside_df.iloc[-1]['top40_accuracy']:.1%} in top 40")
    improvement = (upside_df.iloc[-1]['top40_accuracy'] - upside_df.iloc[0]['top40_accuracy'])
    print(f"  Improvement: {improvement:+.1%}")

if combined_results:
    combined_df = pd.DataFrame(combined_results).sort_values('top40_accuracy', ascending=False)
    print(f"\nBest Combination:")
    best = combined_df.iloc[0]
    print(f"  Exec >= {best['exec']:.0f}, Upside >= {best['upside']:.0f}")
    print(f"  Top 40 accuracy: {best['top40_accuracy']:.1%} ({best['count']:.0f} samples)")
    print(f"  Beat avg: {best['beat_avg']:.1%}")

print("\n")
