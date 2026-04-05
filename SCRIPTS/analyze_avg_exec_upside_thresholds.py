"""
Test Avg Exec and Avg Upside thresholds for Top 40 prediction.
Show if accuracy scales with higher thresholds (linear signal or noise).
"""

import pandas as pd
import numpy as np

# Load aggregated data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[df['round_type'] != 'REMOVE'].copy()

# Aggregate by player + venue
aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': ['mean', 'sum'],
    'upside': ['mean', 'sum'],
    'vs_avg': 'mean',
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated.columns = ['venue', 'player', 'exec_avg', 'exec_sum', 'upside_avg', 'upside_sum', 'vs_avg_mean', 'element', 'color']

print("=" * 130)
print("AVG EXEC + AVG UPSIDE THRESHOLD ANALYSIS")
print("Testing if higher thresholds predict top 40 better (scaling)")
print("=" * 130)

print(f"\nTotal player-tournaments: {len(aggregated)}")
print(f"\nAvg Exec range: {aggregated['exec_avg'].min():.1f} - {aggregated['exec_avg'].max():.1f} (mean: {aggregated['exec_avg'].mean():.1f})")
print(f"Avg Upside range: {aggregated['upside_avg'].min():.1f} - {aggregated['upside_avg'].max():.1f} (mean: {aggregated['upside_avg'].mean():.1f})")

# Test individual thresholds
print(f"\n{'=' * 130}")
print("THRESHOLD ANALYSIS: Avg Exec")
print(f"{'=' * 130}\n")

exec_thresholds = list(range(40, 75, 5))
exec_results = []

print(f"{'Exec Avg >= ?':<15} {'Count':<10} {'Top 40 Rate':<15} {'Beat Avg %':<15} {'Scaling':<20}")
print("-" * 75)

baseline_accuracy = None

for threshold in exec_thresholds:
    filtered = aggregated[aggregated['exec_avg'] >= threshold].copy()

    if len(filtered) < 10:
        continue

    # Calculate top 40 accuracy
    venue_accuracy = []

    for venue in filtered['venue'].unique():
        venue_all = aggregated[aggregated['venue'] == venue]
        venue_filtered = filtered[filtered['venue'] == venue]

        if len(venue_all) < 20 or len(venue_filtered) == 0:
            continue

        # Rank by exec_avg at venue
        venue_all_ranked = venue_all.copy()
        venue_all_ranked['rank'] = venue_all_ranked['exec_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        filtered_ranked = venue_all_ranked[venue_all_ranked['player'].isin(venue_filtered['player'])]

        if len(filtered_ranked) > 0:
            in_top40 = (filtered_ranked['rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(filtered_ranked)
            venue_accuracy.append(accuracy)

    if venue_accuracy:
        avg_accuracy = np.mean(venue_accuracy)
        beat_avg = (filtered['vs_avg_mean'] > 0).mean()

        if baseline_accuracy is None:
            baseline_accuracy = avg_accuracy
            scaling = "BASELINE"
        else:
            scaling_pct = (avg_accuracy / baseline_accuracy - 1) * 100
            scaling = f"{scaling_pct:+.1f}%" if scaling_pct != 0 else "Same"

        exec_results.append({
            'threshold': threshold,
            'count': len(filtered),
            'accuracy': avg_accuracy,
            'beat_avg': beat_avg
        })

        print(f"{threshold:<15} {len(filtered):<10} {avg_accuracy:<15.1%} {beat_avg:<15.1%} {scaling:<20}")

# Test Upside thresholds
print(f"\n{'=' * 130}")
print("THRESHOLD ANALYSIS: Avg Upside")
print(f"{'=' * 130}\n")

upside_thresholds = list(range(60, 90, 5))
upside_results = []

print(f"{'Upside Avg >= ?':<15} {'Count':<10} {'Top 40 Rate':<15} {'Beat Avg %':<15} {'Scaling':<20}")
print("-" * 75)

baseline_accuracy = None

for threshold in upside_thresholds:
    filtered = aggregated[aggregated['upside_avg'] >= threshold].copy()

    if len(filtered) < 10:
        continue

    venue_accuracy = []

    for venue in filtered['venue'].unique():
        venue_all = aggregated[aggregated['venue'] == venue]
        venue_filtered = filtered[filtered['venue'] == venue]

        if len(venue_all) < 20 or len(venue_filtered) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['rank'] = venue_all_ranked['upside_avg'].rank(ascending=False)

        field_size = len(venue_all_ranked)
        top40_cutoff = max(10, int(field_size * 0.33))

        filtered_ranked = venue_all_ranked[venue_all_ranked['player'].isin(venue_filtered['player'])]

        if len(filtered_ranked) > 0:
            in_top40 = (filtered_ranked['rank'] <= top40_cutoff).sum()
            accuracy = in_top40 / len(filtered_ranked)
            venue_accuracy.append(accuracy)

    if venue_accuracy:
        avg_accuracy = np.mean(venue_accuracy)
        beat_avg = (filtered['vs_avg_mean'] > 0).mean()

        if baseline_accuracy is None:
            baseline_accuracy = avg_accuracy
            scaling = "BASELINE"
        else:
            scaling_pct = (avg_accuracy / baseline_accuracy - 1) * 100
            scaling = f"{scaling_pct:+.1f}%" if scaling_pct != 0 else "Same"

        upside_results.append({
            'threshold': threshold,
            'count': len(filtered),
            'accuracy': avg_accuracy,
            'beat_avg': beat_avg
        })

        print(f"{threshold:<15} {len(filtered):<10} {avg_accuracy:<15.1%} {beat_avg:<15.1%} {scaling:<20}")

# Combined thresholds (grid search)
print(f"\n{'=' * 130}")
print("COMBINED THRESHOLDS: Avg Exec × Avg Upside (Grid Search)")
print(f"{'=' * 130}\n")

exec_grid = [50, 55, 60, 65, 70]
upside_grid = [65, 70, 75, 80]

combined_results = []

print(f"{'Exec >= ?':<12} {'Upside >= ?':<14} {'Count':<10} {'Top 40 Rate':<15}")
print("-" * 51)

for exec_thresh in exec_grid:
    for upside_thresh in upside_grid:
        filtered = aggregated[
            (aggregated['exec_avg'] >= exec_thresh) &
            (aggregated['upside_avg'] >= upside_thresh)
        ].copy()

        if len(filtered) < 10:
            continue

        venue_accuracy = []

        for venue in filtered['venue'].unique():
            venue_all = aggregated[aggregated['venue'] == venue]
            venue_filtered = filtered[filtered['venue'] == venue]

            if len(venue_all) < 20 or len(venue_filtered) == 0:
                continue

            # Rank by combination (exec + upside)
            venue_all_ranked = venue_all.copy()
            venue_all_ranked['combined_score'] = venue_all_ranked['exec_avg'] + venue_all_ranked['upside_avg']
            venue_all_ranked['rank'] = venue_all_ranked['combined_score'].rank(ascending=False)

            field_size = len(venue_all_ranked)
            top40_cutoff = max(10, int(field_size * 0.33))

            filtered_ranked = venue_all_ranked[venue_all_ranked['player'].isin(venue_filtered['player'])]

            if len(filtered_ranked) > 0:
                in_top40 = (filtered_ranked['rank'] <= top40_cutoff).sum()
                accuracy = in_top40 / len(filtered_ranked)
                venue_accuracy.append(accuracy)

        if venue_accuracy:
            avg_accuracy = np.mean(venue_accuracy)
            combined_results.append({
                'exec_thresh': exec_thresh,
                'upside_thresh': upside_thresh,
                'count': len(filtered),
                'accuracy': avg_accuracy
            })

            print(f"{exec_thresh:<12} {upside_thresh:<14} {len(filtered):<10} {avg_accuracy:<15.1%}")

# Summary and scaling analysis
print(f"\n{'=' * 130}")
print("SCALING ANALYSIS")
print(f"{'=' * 130}\n")

if exec_results:
    exec_df = pd.DataFrame(exec_results)
    print("AVG EXEC Scaling:")
    print(f"  Lowest threshold ({exec_df.iloc[0]['threshold']:.0f}): {exec_df.iloc[0]['accuracy']:.1%} top 40 rate")
    print(f"  Highest threshold ({exec_df.iloc[-1]['threshold']:.0f}): {exec_df.iloc[-1]['accuracy']:.1%} top 40 rate")
    improvement = (exec_df.iloc[-1]['accuracy'] - exec_df.iloc[0]['accuracy']) / exec_df.iloc[0]['accuracy'] * 100
    print(f"  Improvement: {improvement:+.1f}%")
    if improvement > 5:
        print(f"  [YES] SCALES WELL: Higher exec thresholds improve prediction")
    elif improvement > 0:
        print(f"  [MODEST] Modest scaling: Small improvement with higher thresholds")
    else:
        print(f"  [NO] NO SCALING: Higher exec doesn't improve prediction")

if upside_results:
    upside_df = pd.DataFrame(upside_results)
    print("\nAVG UPSIDE Scaling:")
    print(f"  Lowest threshold ({upside_df.iloc[0]['threshold']:.0f}): {upside_df.iloc[0]['accuracy']:.1%} top 40 rate")
    print(f"  Highest threshold ({upside_df.iloc[-1]['threshold']:.0f}): {upside_df.iloc[-1]['accuracy']:.1%} top 40 rate")
    improvement = (upside_df.iloc[-1]['accuracy'] - upside_df.iloc[0]['accuracy']) / upside_df.iloc[0]['accuracy'] * 100
    print(f"  Improvement: {improvement:+.1f}%")
    if improvement > 5:
        print(f"  [YES] SCALES WELL: Higher upside thresholds improve prediction")
    elif improvement > 0:
        print(f"  [MODEST] Modest scaling: Small improvement with higher thresholds")
    else:
        print(f"  ✗ NO SCALING: Higher upside doesn't improve prediction")

if combined_results:
    combined_df = pd.DataFrame(combined_results).sort_values('accuracy', ascending=False)
    print(f"\nCOMBINED MODEL (Exec + Upside):")
    print(f"  Best combination: Exec >= {combined_df.iloc[0]['exec_thresh']:.0f}, Upside >= {combined_df.iloc[0]['upside_thresh']:.0f}")
    print(f"  Accuracy: {combined_df.iloc[0]['accuracy']:.1%} ({combined_df.iloc[0]['count']:.0f} samples)")

print("\n")
