"""
Isolate high-scoring Fire elements and measure top 40 finish prediction.
Find optimal thresholds for Exec/Upside that predict top 40.
"""

import pandas as pd
import numpy as np

# Load rescored data
df = pd.read_csv('ANALYSIS_v3_RESCORED.csv', low_memory=False)

# Filter: Fire elements only, remove REMOVE rounds, have scorer data
df_fire = df[
    (df['wu_xing'] == 'Fire') &
    (df['round_type'] != 'REMOVE') &
    (df['predicted_score'].notna())
].copy()

print("=" * 120)
print("HIGH-SCORING FIRE ELEMENTS: TOP 40 FINISH ANALYSIS")
print("=" * 120)

print(f"\nTotal Fire element rounds: {len(df_fire)}")
print(f"Venues: {df_fire['event_name'].nunique()}")
print(f"Fire players: {df_fire['player_name'].nunique()}")

# Exec and upside stats for Fire
print(f"\nFire Element Score Distribution:")
print(f"  Exec:    {df_fire['exec'].min():.1f} - {df_fire['exec'].max():.1f} (mean: {df_fire['exec'].mean():.1f})")
print(f"  Upside:  {df_fire['upside'].min():.1f} - {df_fire['upside'].max():.1f} (mean: {df_fire['upside'].mean():.1f})")

# Define thresholds to test
exec_thresholds = [55, 60, 65, 70, 75]
upside_thresholds = [65, 70, 75, 80]

print(f"\n{'=' * 120}")
print("THRESHOLD ANALYSIS: Testing different Exec/Upside combinations")
print(f"{'=' * 120}\n")

results = []

for exec_thresh in exec_thresholds:
    print(f"\n{'-' * 120}")
    print(f"EXEC THRESHOLD >= {exec_thresh}")
    print("-" * 120)
    print(f"{'Upside >= ?':<12} {'Count':<8} {'Beat Avg':<10} {'Accuracy':<12} {'Avg Exec':<10} {'Avg Upside':<12}")
    print("-" * 90)

    for upside_thresh in upside_thresholds:
        # Filter Fire players meeting both thresholds
        high_fire = df_fire[
            (df_fire['exec'] >= exec_thresh) &
            (df_fire['upside'] >= upside_thresh)
        ].copy()

        if len(high_fire) < 5:  # Skip if too few samples
            print(f"{upside_thresh:<12} {'n < 5':<8} {'-':<10} {'-':<12}")
            continue

        # For each venue, rank players and see if these high-fire players finish top 40
        top40_accuracy = []
        beat_avg_count = 0
        total_count = 0

        for venue in high_fire['event_name'].unique():
            venue_fire = high_fire[high_fire['event_name'] == venue]
            venue_all = df_fire[df_fire['event_name'] == venue]

            if len(venue_all) < 20:
                continue

            # Get all players at venue, rank by predicted score
            players_at_venue = venue_all.groupby('player_name').agg({
                'predicted_score': 'mean',
                'vs_avg': 'mean',
                'exec': 'mean',
                'upside': 'mean'
            }).reset_index()

            field_size = len(players_at_venue)
            top40_cutoff = max(10, int(field_size * 0.33))

            # Rank by predicted score
            players_at_venue['rank'] = players_at_venue['predicted_score'].rank(ascending=False)
            players_at_venue['in_top40'] = players_at_venue['rank'] <= top40_cutoff

            # Check: of the high-fire players at this venue, how many are in top 40?
            high_fire_at_venue = players_at_venue[
                players_at_venue['player_name'].isin(venue_fire['player_name'].unique())
            ]

            if len(high_fire_at_venue) > 0:
                in_top40 = high_fire_at_venue['in_top40'].sum()
                beat_avg = (high_fire_at_venue['vs_avg'] > 0).sum()

                top40_accuracy.append(in_top40 / len(high_fire_at_venue))
                beat_avg_count += beat_avg
                total_count += len(high_fire_at_venue)

        if len(top40_accuracy) > 0:
            avg_accuracy = np.mean(top40_accuracy)
            beat_avg_pct = beat_avg_count / total_count if total_count > 0 else 0

            avg_exec = high_fire['exec'].mean()
            avg_upside = high_fire['upside'].mean()

            results.append({
                'exec_threshold': exec_thresh,
                'upside_threshold': upside_thresh,
                'count': len(high_fire),
                'accuracy': avg_accuracy,
                'beat_avg': beat_avg_pct,
                'avg_exec': avg_exec,
                'avg_upside': avg_upside
            })

            print(f"{upside_thresh:<12} {len(high_fire):<8} {beat_avg_pct:<10.1%} {avg_accuracy:<12.1%} {avg_exec:<10.1f} {avg_upside:<12.1f}")

# Best thresholds
print(f"\n{'=' * 120}")
print("BEST THRESHOLD COMBINATIONS (Top 10 by Top 40 Accuracy)")
print(f"{'=' * 120}\n")

if results:
    results_df = pd.DataFrame(results).sort_values('accuracy', ascending=False)

    print(f"{'Exec >= ?':<12} {'Upside >= ?':<14} {'Count':<8} {'Top 40 Accuracy':<18} {'Beat Avg %':<12} {'Notes':<30}")
    print("-" * 104)

    for i, row in results_df.head(10).iterrows():
        notes = ""
        if row['count'] > 1000:
            notes = "Large sample"
        elif row['count'] < 100:
            notes = "Small sample"

        print(f"{row['exec_threshold']:<12} {row['upside_threshold']:<14} {row['count']:<8} {row['accuracy']:<18.1%} {row['beat_avg']:<12.1%} {notes:<30}")

# Threshold zones recommendation
print(f"\n{'=' * 120}")
print("RECOMMENDED THRESHOLDS FOR HIGH-CONFIDENCE FIRE ELEMENT TOP 40 PREDICTIONS")
print(f"{'=' * 120}\n")

best = results_df.iloc[0]

print(f"PRIMARY THRESHOLD:")
print(f"  Exec >= {best['exec_threshold']:.0f}")
print(f"  Upside >= {best['upside_threshold']:.0f}")
print(f"  Prediction: {best['accuracy']:.1%} of these Fire players finish top 40")
print(f"  Sample size: {best['count']:.0f} rounds")

# Show what this means
print(f"\nINTERPRETATION:")
print(f"  - Fire elements with Exec >= {best['exec_threshold']:.0f} AND Upside >= {best['upside_threshold']:.0f}")
print(f"  - These are the highest-quality Fire players")
print(f"  - Estimated {best['accuracy']:.0%} of them will finish top 40")
print(f"  - Baseline for all Fire: {(df_fire['vs_avg'] > 0).mean():.1%} beat field average")

# Detailed breakdown by venue for best threshold
print(f"\n{'=' * 120}")
print(f"VENUE-BY-VENUE BREAKDOWN: Fire with Exec >= {best['exec_threshold']:.0f}, Upside >= {best['upside_threshold']:.0f}")
print(f"{'=' * 120}\n")

high_fire_best = df_fire[
    (df_fire['exec'] >= best['exec_threshold']) &
    (df_fire['upside'] >= best['upside_threshold'])
].copy()

venue_breakdown = []

for venue in sorted(high_fire_best['event_name'].unique()):
    venue_fire = high_fire_best[high_fire_best['event_name'] == venue]
    venue_all = df_fire[df_fire['event_name'] == venue]

    if len(venue_all) < 20:
        continue

    # Rank all players at venue
    players_at_venue = venue_all.groupby('player_name').agg({
        'predicted_score': 'mean',
        'vs_avg': 'mean',
        'exec': 'mean'
    }).reset_index()

    field_size = len(players_at_venue)
    top40_cutoff = max(10, int(field_size * 0.33))

    players_at_venue['rank'] = players_at_venue['predicted_score'].rank(ascending=False)
    players_at_venue['in_top40'] = players_at_venue['rank'] <= top40_cutoff

    high_fire_at_venue = players_at_venue[
        players_at_venue['player_name'].isin(venue_fire['player_name'].unique())
    ]

    if len(high_fire_at_venue) > 0:
        in_top40 = high_fire_at_venue['in_top40'].sum()
        accuracy = in_top40 / len(high_fire_at_venue)

        venue_breakdown.append({
            'venue': venue,
            'field_size': field_size,
            'high_fire_count': len(high_fire_at_venue),
            'top40_count': in_top40,
            'accuracy': accuracy,
            'avg_rank': high_fire_at_venue['rank'].mean()
        })

venue_breakdown_df = pd.DataFrame(venue_breakdown).sort_values('accuracy', ascending=False)

print(f"{'Venue':<40} {'Field':<7} {'High Fire':<11} {'Top 40':<7} {'Accuracy':<12} {'Avg Rank':<10}")
print("-" * 97)

for _, row in venue_breakdown_df.head(20).iterrows():
    print(f"{row['venue']:<40} {row['field_size']:<7} {row['high_fire_count']:<11} {row['top40_count']:<7} {row['accuracy']:<12.1%} {row['avg_rank']:<10.0f}")

print("\n")
