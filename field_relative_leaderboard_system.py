"""
FIELD-RELATIVE LEADERBOARD SCORING SYSTEM
Score players relative to field strength, weighted by element performance at venue.
Tests if this predicts top 40 better than absolute scores.
"""

import pandas as pd
import numpy as np

# Load and aggregate
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[df['round_type'] != 'REMOVE'].copy()

aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': 'mean',
    'upside': 'mean',
    'vs_avg': 'mean',
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated['absolute_score'] = aggregated['exec'] + aggregated['upside']

print("=" * 150)
print("FIELD-RELATIVE LEADERBOARD SCORING SYSTEM")
print("Score players relative to field, weighted by element performance at venue")
print("=" * 150)

print(f"\nTotal player-tournaments: {len(aggregated)}")
print(f"Venues: {aggregated['event_name'].nunique()}")

# ============================================================================
# STEP 1: BUILD ELEMENT STRENGTH PROFILES BY VENUE
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 1: ELEMENT STRENGTH PROFILES (by venue)")
print("=" * 150)

element_strength_by_venue = {}

for venue in aggregated['event_name'].unique():
    venue_data = aggregated[aggregated['event_name'] == venue]

    # Field average
    field_exec = venue_data['exec'].mean()
    field_upside = venue_data['upside'].mean()
    field_score = field_exec + field_upside

    # Element strength at this venue
    element_strength = {}
    for element in venue_data['wu_xing'].unique():
        element_data = venue_data[venue_data['wu_xing'] == element]

        if len(element_data) < 2:
            element_strength[element] = 1.0  # Default if no data
            continue

        elem_score = (element_data['exec'].mean() + element_data['upside'].mean())
        strength_factor = elem_score / field_score if field_score > 0 else 1.0

        element_strength[element] = strength_factor

    element_strength_by_venue[venue] = {
        'field_score': field_score,
        'field_exec': field_exec,
        'field_upside': field_upside,
        'element_strength': element_strength
    }

# Display sample
print("\nSample venues and element strength factors:")
print(f"{'Venue':<40} {'Field Score':<15} {'Fire':<10} {'Water':<10} {'Earth':<10} {'Metal':<10} {'Wood':<10}")
print("-" * 105)

for venue in list(element_strength_by_venue.keys())[:10]:
    venue_info = element_strength_by_venue[venue]
    fire = venue_info['element_strength'].get('Fire', 1.0)
    water = venue_info['element_strength'].get('Water', 1.0)
    earth = venue_info['element_strength'].get('Earth', 1.0)
    metal = venue_info['element_strength'].get('Metal', 1.0)
    wood = venue_info['element_strength'].get('Wood', 1.0)

    print(f"{venue:<40} {venue_info['field_score']:<15.2f} {fire:<10.3f} {water:<10.3f} {earth:<10.3f} {metal:<10.3f} {wood:<10.3f}")

# ============================================================================
# STEP 2: CALCULATE FIELD-RELATIVE SCORES
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 2: FIELD-RELATIVE SCORING")
print("=" * 150)

aggregated['field_relative_score'] = 0.0
aggregated['element_strength_factor'] = 0.0
aggregated['percentile_rank'] = 0.0

for idx, row in aggregated.iterrows():
    venue = row['event_name']
    element = row['wu_xing']

    if venue not in element_strength_by_venue:
        aggregated.at[idx, 'field_relative_score'] = row['absolute_score']
        aggregated.at[idx, 'element_strength_factor'] = 1.0
        continue

    venue_info = element_strength_by_venue[venue]
    field_score = venue_info['field_score']
    strength_factor = venue_info['element_strength'].get(element, 1.0)

    # Field-relative score = absolute_score / field_avg, weighted by element strength
    relative_score = (row['absolute_score'] / field_score) * strength_factor

    aggregated.at[idx, 'field_relative_score'] = relative_score
    aggregated.at[idx, 'element_strength_factor'] = strength_factor

# Calculate percentile rank within each venue
for venue in aggregated['event_name'].unique():
    venue_mask = aggregated['event_name'] == venue
    venue_data = aggregated[venue_mask]

    # Rank by field_relative_score
    percentiles = (venue_data['field_relative_score'].rank(pct=True) * 100)
    aggregated.loc[venue_mask, 'percentile_rank'] = percentiles.values

print(f"Field-relative scores calculated:")
print(f"  Metric: (Player_Exec+Upside / Field_Avg) × Element_Strength_Factor")
print(f"  Percentile: Player's rank within venue (0-100)")

# ============================================================================
# STEP 3: TEST PREDICTION ACCURACY
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 3: MODEL COMPARISON - TOP 40 PREDICTION ACCURACY")
print("=" * 150)

# Model 1: Absolute score (Exec + Upside)
print(f"\nMODEL 1: Absolute Score (Exec + Upside)")
print("-" * 70)

absolute_accuracy = []

for venue in aggregated['event_name'].unique():
    venue_data = aggregated[aggregated['event_name'] == venue].copy()

    if len(venue_data) < 20:
        continue

    # Rank by absolute score
    venue_data['rank'] = venue_data['absolute_score'].rank(ascending=False)
    top40_cutoff = max(10, int(len(venue_data) * 0.33))

    # Check: do top 33% ranked actually beat field average?
    top33 = venue_data[venue_data['rank'] <= top40_cutoff]
    beat_avg = (top33['vs_avg'] > 0).sum() / len(top33) if len(top33) > 0 else 0

    absolute_accuracy.append(beat_avg)

if absolute_accuracy:
    print(f"Accuracy (top 33% by absolute score beat avg): {np.mean(absolute_accuracy):.1%}")

# Model 2: Field-relative score with element weighting
print(f"\nMODEL 2: Field-Relative Score (weighted by element strength)")
print("-" * 70)

relative_accuracy = []

for venue in aggregated['event_name'].unique():
    venue_data = aggregated[aggregated['event_name'] == venue].copy()

    if len(venue_data) < 20:
        continue

    # Rank by field_relative_score
    venue_data['rank'] = venue_data['field_relative_score'].rank(ascending=False)
    top40_cutoff = max(10, int(len(venue_data) * 0.33))

    # Check: do top 33% ranked actually beat field average?
    top33 = venue_data[venue_data['rank'] <= top40_cutoff]
    beat_avg = (top33['vs_avg'] > 0).sum() / len(top33) if len(top33) > 0 else 0

    relative_accuracy.append(beat_avg)

if relative_accuracy:
    print(f"Accuracy (top 33% by field-relative score beat avg): {np.mean(relative_accuracy):.1%}")

# Model 3: Percentile threshold
print(f"\nMODEL 3: Percentile Threshold (top 33% by percentile)")
print("-" * 70)

percentile_accuracy = []

for venue in aggregated['event_name'].unique():
    venue_data = aggregated[aggregated['event_name'] == venue].copy()

    if len(venue_data) < 20:
        continue

    # Top 33% by percentile
    top33 = venue_data[venue_data['percentile_rank'] >= 67]  # Top 33%
    if len(top33) > 0:
        beat_avg = (top33['vs_avg'] > 0).sum() / len(top33)
        percentile_accuracy.append(beat_avg)

if percentile_accuracy:
    print(f"Accuracy (top 33% by percentile beat avg): {np.mean(percentile_accuracy):.1%}")

# ============================================================================
# STEP 4: LEADERBOARD EXAMPLE
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 4: LEADERBOARD EXAMPLE")
print("=" * 150)

# Pick a venue
sample_venue = aggregated.groupby('event_name').size().sort_values(ascending=False).index[0]
sample_data = aggregated[aggregated['event_name'] == sample_venue].copy()

print(f"\nVenue: {sample_venue}")
print(f"Field size: {len(sample_data)}")
print(f"Field avg Exec+Upside: {sample_data['absolute_score'].mean():.2f}")
print(f"Top 40 cutoff: {max(10, int(len(sample_data) * 0.33))} players\n")

# Rank by field-relative score
sample_data['rank'] = sample_data['field_relative_score'].rank(ascending=False)

# Show top 20
print(f"{'Rank':<6} {'Player':<30} {'Exec+Upside':<15} {'Element':<12} {'Element Factor':<15} {'Field-Rel Score':<18} {'vs_avg (Actual)':<15} {'Top 40?':<8}")
print("-" * 130)

for idx, (_, row) in enumerate(sample_data.nsmallest(20, 'rank').iterrows(), 1):
    in_top40 = "YES" if row['rank'] <= max(10, int(len(sample_data) * 0.33)) else "NO"
    beat_avg = "BEAT" if row['vs_avg'] > 0 else "MISS"

    print(f"{row['rank']:<6.0f} {row['player_name']:<30} {row['absolute_score']:<15.2f} {row['wu_xing']:<12} {row['element_strength_factor']:<15.3f} {row['field_relative_score']:<18.3f} {row['vs_avg']:<15.3f} {beat_avg:<8}")

# ============================================================================
# STEP 5: ELEMENT IMPACT ANALYSIS
# ============================================================================

print(f"\n{'=' * 150}")
print("STEP 5: ELEMENT IMPACT ON TOP 40 PREDICTION")
print("=" * 150)

print(f"\nWhich elements finish top 40 most often?\n")
print(f"{'Element':<12} {'Top 40 Rate':<15} {'Avg Exec+Upside':<18} {'Sample Size':<12}")
print("-" * 57)

for element in aggregated['wu_xing'].unique():
    element_data = aggregated[aggregated['wu_xing'] == element]

    # Check top 40 rate
    top40_rate = []

    for venue in element_data['event_name'].unique():
        venue_all = aggregated[aggregated['event_name'] == venue]
        venue_elem = element_data[element_data['event_name'] == venue]

        if len(venue_all) < 20 or len(venue_elem) == 0:
            continue

        venue_all_ranked = venue_all.copy()
        venue_all_ranked['rank'] = venue_all_ranked['field_relative_score'].rank(ascending=False)
        top40_cutoff = max(10, int(len(venue_all_ranked) * 0.33))

        elem_ranked = venue_all_ranked[venue_all_ranked['player_name'].isin(venue_elem['player_name'])]

        if len(elem_ranked) > 0:
            in_top40 = (elem_ranked['rank'] <= top40_cutoff).sum() / len(elem_ranked)
            top40_rate.append(in_top40)

    if top40_rate:
        avg_rate = np.mean(top40_rate)
        avg_score = element_data['absolute_score'].mean()

        print(f"{element:<12} {avg_rate:<15.1%} {avg_score:<18.2f} {len(element_data):<12.0f}")

print("\n")
