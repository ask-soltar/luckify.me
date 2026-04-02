"""
BUILD COLOR SCORING TABLE - BY YEAR AND VENUE
Correctly account for multiple years of same tournament
Calculate field sizes per (event, year) combination
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Filter: S-type tournaments only
df_clean = df[(df['round_type'] != 'REMOVE') & (df['tournament_type'] == 'S')].copy()

print("=" * 180)
print("COLOR SCORING TABLE - BY YEAR AND VENUE")
print("Correctly accounting for multiple years of same tournament")
print("=" * 180)

print(f"\nDataset: {len(df_clean)} records")
print(f"Events: {df_clean['event_name'].nunique()}")
print(f"Years: {df_clean['year'].nunique()} unique years")

# ============================================================================
# STEP 1: Analyze real field sizes (by event-year)
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 1: ACTUAL FIELD SIZES (by tournament instance)")
print("=" * 180)

field_stats = []

for event in df_clean['event_name'].unique():
    for year in df_clean[df_clean['event_name'] == event]['year'].unique():
        event_year_data = df_clean[(df_clean['event_name'] == event) & (df_clean['year'] == year)]

        # Count unique players per round
        r1_count = event_year_data[event_year_data['round_num'] == 1]['player_name'].nunique()
        r2_count = event_year_data[event_year_data['round_num'] == 2]['player_name'].nunique()
        r3_count = event_year_data[event_year_data['round_num'] == 3]['player_name'].nunique()
        r4_count = event_year_data[event_year_data['round_num'] == 4]['player_name'].nunique()

        if r1_count > 0:
            field_stats.append({
                'event': event,
                'year': year,
                'r1': r1_count,
                'r2': r2_count,
                'r3': r3_count,
                'r4': r4_count,
            })

field_df = pd.DataFrame(field_stats)

print(f"\nField size statistics (per tournament instance):")
print(f"  R1: Min {field_df['r1'].min():.0f}, Max {field_df['r1'].max():.0f}, Mean {field_df['r1'].mean():.0f}")
print(f"  R2: Min {field_df['r2'].min():.0f}, Max {field_df['r2'].max():.0f}, Mean {field_df['r2'].mean():.0f}")
print(f"  R3: Min {field_df['r3'].min():.0f}, Max {field_df['r3'].max():.0f}, Mean {field_df['r3'].mean():.0f}")
print(f"  R4: Min {field_df['r4'].min():.0f}, Max {field_df['r4'].max():.0f}, Mean {field_df['r4'].mean():.0f}")

print(f"\nSample tournaments:")
print(f"{'Event':<40} {'Year':<6} {'R1':<6} {'R2':<6} {'R3':<6} {'R4':<6}")
print(f"{'-' * 70}")
for _, row in field_df.head(15).iterrows():
    print(f"{row['event']:<40} {row['year']:<6.0f} {row['r1']:<6.0f} {row['r2']:<6.0f} {row['r3']:<6.0f} {row['r4']:<6.0f}")

# ============================================================================
# STEP 2: Per-tournament-year, per-round color analysis
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 2: COLOR PERFORMANCE (BY TOURNAMENT INSTANCE)")
print("=" * 180)

df_roundlevel = df_clean[['event_name', 'year', 'round_num', 'color', 'vs_avg']].copy()
df_roundlevel = df_roundlevel[df_roundlevel['color'].notna()].copy()

# For each (event, year, round), calculate color finish rates
round_results = {}

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    color_finish_rates = []

    for idx, row in field_df.iterrows():
        event = row['event']
        year = row['year']
        field_size = row[f'r{round_num}']

        if field_size < 30:  # Skip small fields
            continue

        event_year_data = round_data[(round_data['event_name'] == event) & (round_data['year'] == year)]

        if len(event_year_data) == 0:
            continue

        # Top 40 as percentile for THIS tournament
        top40_count = 40
        top40_pct = min(top40_count / field_size, 1.0) if field_size > 0 else 0

        if top40_pct == 0:
            continue

        # Rank by vs_avg within this tournament-round
        event_year_data = event_year_data.copy()
        event_year_data['rank_pct'] = event_year_data['vs_avg'].rank(pct=True)

        top40_cutoff = 1.0 - top40_pct
        top_performers = event_year_data[event_year_data['rank_pct'] >= top40_cutoff]

        # For each color, calculate finish rate
        for color in event_year_data['color'].unique():
            color_data = event_year_data[event_year_data['color'] == color]
            in_top = (top_performers['color'] == color).sum()
            finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

            color_finish_rates.append({
                'event': event,
                'year': year,
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

        round_results[round_num] = {
            'results': avg_by_color,
            'tournament_count': results_df['event'].nunique(),
            'avg_field': results_df['field_size'].mean(),
        }

        print(f"\nROUND {round_num}:")
        print(f"  Tournaments analyzed: {results_df['event'].nunique()}")
        print(f"  Avg field size: {results_df['field_size'].mean():.0f}")
        print(f"  {'Color':<15} {'Finish Rate':<15} {'Sample':<15}")
        print(f"  {'-' * 45}")
        for _, row in avg_by_color.iterrows():
            print(f"  {str(row['color']):<15} {row['finish_rate']:<15.1%} {row['count']:<15.0f}")

# ============================================================================
# STEP 3: Create scoring table
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 3: COLOR SCORING TABLE")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    if round_num not in round_results:
        continue

    results_df = round_results[round_num]['results']
    mean_rate = results_df['finish_rate'].mean()
    field_size = round_results[round_num]['avg_field']

    print(f"\nROUND {round_num} (Avg field: {field_size:.0f} players, Mean finish rate: {mean_rate:.1%})")
    print(f"{'Color':<15} {'Finish Rate':<15} {'Score':<15}")
    print(f"{'-' * 45}")

    sorted_df = results_df.sort_values('finish_rate', ascending=False)
    for _, row in sorted_df.iterrows():
        score = row['finish_rate'] - mean_rate
        print(f"{str(row['color']):<15} {row['finish_rate']:<15.1%} {score:+.2f}")

# ============================================================================
# STEP 4: Summary
# ============================================================================

print(f"\n{'=' * 180}")
print("SUMMARY: COLOR SCORING BY ROUND")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    if round_num not in round_results:
        continue

    results_df = round_results[round_num]['results']
    mean_rate = results_df['finish_rate'].mean()

    best = results_df.iloc[0]
    worst = results_df.iloc[-1]

    best_score = best['finish_rate'] - mean_rate
    worst_score = worst['finish_rate'] - mean_rate
    spread = best_score - worst_score

    print(f"\nR{round_num}: {best['color']} ({best_score:+.1%}) vs {worst['color']} ({worst_score:+.1%}), Spread {spread:.1%}")

print("\n")
