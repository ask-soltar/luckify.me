"""
BUILD COLOR SCORING TABLE - VENUE-FILTERED
- Group by venue/event for accurate field size
- Each venue calculates its own "top 40"
- Average color performance across venues
- Handle cuts properly
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Filter: S-type tournaments only
df_clean = df[(df['round_type'] != 'REMOVE') & (df['tournament_type'] == 'S')].copy()

print("=" * 180)
print("COLOR SCORING TABLE - VENUE-FILTERED ANALYSIS")
print("Each venue calculates 'top 40' based on ITS field size")
print("=" * 180)

print(f"\nDataset: {len(df_clean)} records from S-type tournaments")
venues = df_clean['event_name'].unique()
print(f"Venues: {len(venues)} events\n")

# ============================================================================
# STEP 1: Analyze field sizes per venue
# ============================================================================

print(f"{'=' * 180}")
print("STEP 1: FIELD SIZE BY VENUE")
print("=" * 180)

venue_fields = []

for event in venues:
    event_data = df_clean[df_clean['event_name'] == event]

    r1_count = event_data[event_data['round_num'] == 1].shape[0]
    r2_count = event_data[event_data['round_num'] == 2].shape[0]
    r3_count = event_data[event_data['round_num'] == 3].shape[0]
    r4_count = event_data[event_data['round_num'] == 4].shape[0]

    venue_fields.append({
        'event': event,
        'r1': r1_count,
        'r2': r2_count,
        'r3': r3_count,
        'r4': r4_count,
    })

venue_df = pd.DataFrame(venue_fields)

print(f"\nField size distribution across venues:")
print(f"  R1: Min {venue_df['r1'].min()}, Max {venue_df['r1'].max()}, Mean {venue_df['r1'].mean():.0f}")
print(f"  R2: Min {venue_df['r2'].min()}, Max {venue_df['r2'].max()}, Mean {venue_df['r2'].mean():.0f}")
print(f"  R3: Min {venue_df['r3'].min()}, Max {venue_df['r3'].max()}, Mean {venue_df['r3'].mean():.0f}")
print(f"  R4: Min {venue_df['r4'].min()}, Max {venue_df['r4'].max()}, Mean {venue_df['r4'].mean():.0f}")

print(f"\nSample venues:")
print(f"{'Event':<40} {'R1':<8} {'R2':<8} {'R3':<8} {'R4':<8}")
print(f"{'-' * 64}")
for _, row in venue_df.head(10).iterrows():
    print(f"{row['event']:<40} {row['r1']:<8.0f} {row['r2']:<8.0f} {row['r3']:<8.0f} {row['r4']:<8.0f}")

# ============================================================================
# STEP 2: Per-venue, per-round color analysis
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 2: COLOR PERFORMANCE (PER-VENUE ANALYSIS)")
print("=" * 180)

# Round-level data
df_roundlevel = df_clean[['event_name', 'round_num', 'color', 'score', 'par', 'vs_avg']].copy()
df_roundlevel = df_roundlevel[df_roundlevel['color'].notna()].copy()

# For each venue, each round, calculate color finish rates
round_results = {}

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    color_finish_rates = []

    for event in venues:
        event_venue_data = round_data[round_data['event_name'] == event]

        if len(event_venue_data) == 0:
            continue

        # Field size for this event at this round
        field_size = len(event_venue_data)

        # Top 40 as percentile for THIS field
        top40_count = 40
        top40_pct = top40_count / field_size if field_size > 0 else 0

        # Skip if field too small
        if field_size < 40:
            continue

        # Rank by vs_avg within this event
        event_venue_data = event_venue_data.copy()
        event_venue_data['rank_pct'] = event_venue_data['vs_avg'].rank(pct=True)

        top40_cutoff = 1.0 - top40_pct
        top_performers = event_venue_data[event_venue_data['rank_pct'] >= top40_cutoff]

        # For each color, calculate finish rate
        for color in event_venue_data['color'].unique():
            color_data = event_venue_data[event_venue_data['color'] == color]
            in_top = (top_performers['color'] == color).sum()
            finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

            color_finish_rates.append({
                'event': event,
                'field_size': field_size,
                'color': color,
                'finish_rate': finish_rate,
                'count': len(color_data),
            })

    # Average by color
    if color_finish_rates:
        results_df = pd.DataFrame(color_finish_rates)

        avg_by_color = results_df.groupby('color').agg({
            'finish_rate': 'mean',
            'count': 'sum',
        }).reset_index()
        avg_by_color = avg_by_color.sort_values('finish_rate', ascending=False)

        round_results[round_num] = avg_by_color

        print(f"\nROUND {round_num}:")
        print(f"  Venues included: {results_df['event'].nunique()}")
        print(f"  Avg field size: {results_df['field_size'].mean():.0f}")
        print(f"  {'Color':<15} {'Finish Rate':<15} {'Sample Size':<15}")
        print(f"  {'-' * 45}")
        for _, row in avg_by_color.iterrows():
            print(f"  {str(row['color']):<15} {row['finish_rate']:<15.1%} {row['count']:<15.0f}")

# ============================================================================
# STEP 3: Create scoring table (relative to mean)
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 3: COLOR SCORING TABLE (VENUE-FILTERED)")
print("=" * 180)

print(f"\nScore = finish_rate - mean_finish_rate\n")

final_scores = {}

for round_num in [1, 2, 3, 4]:
    if round_num not in round_results:
        continue

    results_df = round_results[round_num]
    mean_rate = results_df['finish_rate'].mean()

    scores = {}
    for _, row in results_df.iterrows():
        color = row['color']
        score = row['finish_rate'] - mean_rate
        scores[color] = score

    final_scores[round_num] = scores

    print(f"ROUND {round_num} (Mean finish rate: {mean_rate:.1%})")
    print(f"{'Color':<15} {'Finish Rate':<15} {'Score':<15} {'Rating':<20}")
    print(f"{'-' * 65}")

    sorted_colors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for color, score in sorted_colors:
        rate = results_df[results_df['color'] == color]['finish_rate'].values[0]

        if score > 0.05:
            rating = "STRONG"
        elif score > 0.02:
            rating = "Above Average"
        elif score > -0.02:
            rating = "Average"
        elif score > -0.05:
            rating = "Below Average"
        else:
            rating = "WEAK"

        print(f"{str(color):<15} {rate:<15.1%} {score:+.2f}      {rating:<20}")

    print()

# ============================================================================
# STEP 4: Summary
# ============================================================================

print(f"{'=' * 180}")
print("SUMMARY: COLOR SCORING BY ROUND (VENUE-FILTERED)")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    if round_num not in final_scores:
        continue

    scores = final_scores[round_num]
    best = max(scores.items(), key=lambda x: x[1])
    worst = min(scores.items(), key=lambda x: x[1])
    spread = best[1] - worst[1]

    print(f"\nR{round_num}: Best {best[0]} ({best[1]:+.1%}), Worst {worst[0]} ({worst[1]:+.1%}), Spread {spread:.1%}")

# ============================================================================
# Final table for reference
# ============================================================================

print(f"\n{'=' * 180}")
print("READY-TO-USE SCORING TABLE")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    if round_num not in final_scores:
        continue

    scores = final_scores[round_num]
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print(f"\nROUND {round_num}:")
    for color, score in sorted_scores:
        if score >= 0:
            print(f"  {color}: {score:+.1%}")
        else:
            print(f"  {color}: {score:+.1%}")

print("\n")
