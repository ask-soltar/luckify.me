"""
AUDIT: Is Model B circular logic or real signal?
Check: am I ranking by the same metric I filtered on?
"""

import pandas as pd
import numpy as np

# Load and aggregate
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[df['round_type'] != 'REMOVE'].copy()

aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': 'mean',
    'upside': 'mean',
    'adj_his_par': 'mean',
    'vs_avg': 'mean',
}).reset_index()

# Create Model B score
aggregated['model_b_score'] = (aggregated['exec'] + aggregated['upside']) + (aggregated['adj_his_par'] * 2)

print("=" * 130)
print("AUDIT: MODEL B CIRCULAR LOGIC CHECK")
print("=" * 130)

# Test threshold
threshold = 128.2
filtered = aggregated[aggregated['model_b_score'] >= threshold].copy()

print(f"\nFiltered by Model B score >= {threshold}: {len(filtered)} players")
print(f"Model B score range (filtered): {filtered['model_b_score'].min():.2f} - {filtered['model_b_score'].max():.2f}")
print(f"vs_avg (actual) range (filtered): {filtered['vs_avg'].min():.3f} - {filtered['vs_avg'].max():.3f}")

# ============================================================
# TEST 1: Rank by Model B score (WRONG - circular)
# ============================================================

print(f"\n{'=' * 130}")
print("TEST 1: CIRCULAR LOGIC (Rank by Model B score)")
print("=" * 130)

circular_accuracy = []

for venue in aggregated['event_name'].unique():
    venue_all = aggregated[aggregated['event_name'] == venue].copy()
    venue_filtered = filtered[filtered['event_name'] == venue].copy()

    if len(venue_all) < 20 or len(venue_filtered) == 0:
        continue

    # WRONG: Rank by model_b_score
    venue_all['rank_by_model'] = venue_all['model_b_score'].rank(ascending=False)

    field_size = len(venue_all)
    top40_cutoff = max(10, int(field_size * 0.33))

    filtered_ranked = venue_all[venue_all['player_name'].isin(venue_filtered['player_name'])]

    if len(filtered_ranked) > 0:
        in_top40 = (filtered_ranked['rank_by_model'] <= top40_cutoff).sum()
        accuracy = in_top40 / len(filtered_ranked)
        circular_accuracy.append(accuracy)

if circular_accuracy:
    print(f"Accuracy (Rank by Model B): {np.mean(circular_accuracy):.1%}")
    print("^ This is CIRCULAR - filtering by Model B then ranking by Model B!")

# ============================================================
# TEST 2: Rank by ACTUAL FINISH (vs_avg) - CORRECT
# ============================================================

print(f"\n{'=' * 130}")
print("TEST 2: CORRECT LOGIC (Rank by actual finish: vs_avg)")
print("=" * 130)

correct_accuracy = []

for venue in aggregated['event_name'].unique():
    venue_all = aggregated[aggregated['event_name'] == venue].copy()
    venue_filtered = filtered[filtered['event_name'] == venue].copy()

    if len(venue_all) < 20 or len(venue_filtered) == 0:
        continue

    # CORRECT: Rank by actual finish (vs_avg_mean)
    venue_all['rank_by_actual'] = venue_all['vs_avg'].rank(ascending=False)

    field_size = len(venue_all)
    top40_cutoff = max(10, int(field_size * 0.33))

    filtered_ranked = venue_all[venue_all['player_name'].isin(venue_filtered['player_name'])]

    if len(filtered_ranked) > 0:
        in_top40 = (filtered_ranked['rank_by_actual'] <= top40_cutoff).sum()
        accuracy = in_top40 / len(filtered_ranked)
        correct_accuracy.append(accuracy)

if correct_accuracy:
    print(f"Accuracy (Rank by actual vs_avg): {np.mean(correct_accuracy):.1%}")
    print("^ This is CORRECT - filtering by model, ranking by actual finish")

# ============================================================
# DETAIL: Show what's happening at one venue
# ============================================================

print(f"\n{'=' * 130}")
print("DETAIL: Single Venue Example (showing the difference)")
print("=" * 130)

# Pick a venue with enough data
sample_venue = aggregated.groupby('event_name').size().sort_values(ascending=False).index[0]
sample_all = aggregated[aggregated['event_name'] == sample_venue].copy()
sample_filtered = filtered[filtered['event_name'] == sample_venue].copy()

if len(sample_filtered) > 0:
    print(f"\nVenue: {sample_venue}")
    print(f"Total players: {len(sample_all)}")
    print(f"Filtered (Model B >= {threshold}): {len(sample_filtered)}")
    print(f"Top 40 cutoff: {max(10, int(len(sample_all) * 0.33))}")

    # Show filtered players
    print(f"\nFiltered players (Model B >= {threshold}):")
    print(f"{'Player':<30} {'Model B Score':<15} {'vs_avg (actual)':<15} {'Rank (Actual)':<15}")
    print("-" * 75)

    sample_all['rank_actual'] = sample_all['vs_avg'].rank(ascending=False)

    for _, row in sample_filtered.head(10).iterrows():
        actual_rank = sample_all[sample_all['player_name'] == row['player_name']]['rank_actual'].values[0]
        in_top40 = "YES" if actual_rank <= max(10, int(len(sample_all) * 0.33)) else "NO"
        print(f"{row['player_name']:<30} {row['model_b_score']:<15.2f} {row['vs_avg']:<15.3f} {actual_rank:<15.0f}")

# ============================================================
# SUMMARY
# ============================================================

print(f"\n{'=' * 130}")
print("AUDIT CONCLUSION")
print("=" * 130)

if len(circular_accuracy) > 0 and len(correct_accuracy) > 0:
    circular_result = np.mean(circular_accuracy)
    correct_result = np.mean(correct_accuracy)

    print(f"\nCircular (Wrong) Accuracy: {circular_result:.1%}")
    print(f"Correct Accuracy: {correct_result:.1%}")
    print(f"Difference: {circular_result - correct_result:.1%}")

    if circular_result > correct_result + 0.20:
        print(f"\n[ERROR] Model B has CIRCULAR LOGIC!")
        print(f"The 99% accuracy was from ranking by the same metric used to filter.")
        print(f"Real accuracy is only {correct_result:.1%}.")
    else:
        print(f"\n[OK] Model B logic is sound.")
        print(f"Difference is small; the model has real predictive power.")

print("\n")
