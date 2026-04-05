"""
COLOR SCORING WITH FREQUENCY ADJUSTMENT
- Calculate color finish rates (as before)
- Calculate color frequency (how often it appears)
- Adjust scores: rare colors shrink toward mean (less reliable)
- Show both raw and adjusted scores
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[(df['round_type'] != 'REMOVE') & (df['tournament_type'] == 'S')].copy()

print("=" * 180)
print("COLOR SCORING WITH FREQUENCY ADJUSTMENT")
print("Rare colors shrink toward mean (less reliable than common colors)")
print("=" * 180)

df_roundlevel = df_clean[['event_name', 'year', 'round_num', 'color', 'vs_avg']].copy()
df_roundlevel = df_roundlevel[df_roundlevel['color'].notna()].copy()

# ============================================================================
# STEP 1: Calculate raw scores + frequency
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 1: RAW SCORES + FREQUENCY ANALYSIS")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    color_stats = []

    for event in df_clean['event_name'].unique():
        for year in df_clean[df_clean['event_name'] == event]['year'].unique():
            event_year_data = round_data[(round_data['event_name'] == event) & (round_data['year'] == year)]

            if len(event_year_data) < 30:
                continue

            # Calculate field size
            field_size = len(event_year_data)
            top40_pct = min(40 / field_size, 1.0)

            # Rank by vs_avg
            event_year_data = event_year_data.copy()
            event_year_data['rank_pct'] = event_year_data['vs_avg'].rank(pct=True)

            top40_cutoff = 1.0 - top40_pct
            top_performers = event_year_data[event_year_data['rank_pct'] >= top40_cutoff]

            # For each color, calculate finish rate
            for color in event_year_data['color'].unique():
                color_data = event_year_data[event_year_data['color'] == color]
                in_top = (top_performers['color'] == color).sum()
                finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

                color_stats.append({
                    'color': color,
                    'finish_rate': finish_rate,
                    'count': len(color_data),
                })

    # Aggregate by color
    if color_stats:
        stats_df = pd.DataFrame(color_stats)

        # Total count per color
        color_totals = stats_df.groupby('color').agg({
            'finish_rate': 'mean',
            'count': 'sum',
        }).reset_index()

        total_records = stats_df['count'].sum()

        # Calculate statistics
        results = []
        for _, row in color_totals.iterrows():
            color = row['color']
            finish_rate = row['finish_rate']
            count = row['count']
            frequency = count / total_records

            results.append({
                'color': color,
                'finish_rate': finish_rate,
                'count': count,
                'frequency': frequency,
            })

        results_df = pd.DataFrame(results).sort_values('count', ascending=False)

        mean_finish = results_df['finish_rate'].mean()

        print(f"\nROUND {round_num}:")
        print(f"  Total records: {total_records}")
        print(f"  Mean finish rate: {mean_finish:.1%}")
        print(f"  {'Color':<12} {'Count':<10} {'Freq':<10} {'Finish %':<12} {'vs Mean':<12}")
        print(f"  {'-' * 56}")
        for _, row in results_df.iterrows():
            raw_score = row['finish_rate'] - mean_finish
            print(f"  {str(row['color']):<12} {row['count']:<10.0f} {row['frequency']:<10.1%} {row['finish_rate']:<12.1%} {raw_score:+.2f}")

# ============================================================================
# STEP 2: Frequency-adjusted scoring
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 2: FREQUENCY-ADJUSTED SCORES")
print("=" * 180)

print(f"\nMethod: Shrinkage estimator")
print(f"Adjusted score = (raw_score * weight) + (0 * (1-weight))")
print(f"Weight = sqrt(frequency) — rare colors get 0-0.3 weight, common get 0.7-1.0 weight\n")

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    color_stats = []

    for event in df_clean['event_name'].unique():
        for year in df_clean[df_clean['event_name'] == event]['year'].unique():
            event_year_data = round_data[(round_data['event_name'] == event) & (round_data['year'] == year)]

            if len(event_year_data) < 30:
                continue

            field_size = len(event_year_data)
            top40_pct = min(40 / field_size, 1.0)

            event_year_data = event_year_data.copy()
            event_year_data['rank_pct'] = event_year_data['vs_avg'].rank(pct=True)

            top40_cutoff = 1.0 - top40_pct
            top_performers = event_year_data[event_year_data['rank_pct'] >= top40_cutoff]

            for color in event_year_data['color'].unique():
                color_data = event_year_data[event_year_data['color'] == color]
                in_top = (top_performers['color'] == color).sum()
                finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

                color_stats.append({
                    'color': color,
                    'finish_rate': finish_rate,
                    'count': len(color_data),
                })

    if color_stats:
        stats_df = pd.DataFrame(color_stats)
        color_totals = stats_df.groupby('color').agg({
            'finish_rate': 'mean',
            'count': 'sum',
        }).reset_index()

        total_records = stats_df['count'].sum()
        mean_finish = color_totals['finish_rate'].mean()

        # Calculate adjusted scores
        results = []
        for _, row in color_totals.iterrows():
            color = row['color']
            finish_rate = row['finish_rate']
            count = row['count']
            frequency = count / total_records

            # Raw score
            raw_score = finish_rate - mean_finish

            # Shrinkage weight (sqrt of frequency)
            # sqrt(0.5%) = 0.07, sqrt(30%) = 0.55, sqrt(100%) = 1.0
            weight = np.sqrt(frequency)

            # Adjusted score (shrink rare colors toward 0)
            adjusted_score = raw_score * weight

            results.append({
                'color': color,
                'finish_rate': finish_rate,
                'count': count,
                'frequency': frequency,
                'weight': weight,
                'raw_score': raw_score,
                'adjusted_score': adjusted_score,
            })

        results_df = pd.DataFrame(results).sort_values('adjusted_score', ascending=False)

        print(f"ROUND {round_num}:")
        print(f"  {'Color':<12} {'Count':<10} {'Freq':<10} {'Weight':<10} {'Raw':<10} {'Adjusted':<12}")
        print(f"  {'-' * 62}")
        for _, row in results_df.iterrows():
            print(f"  {str(row['color']):<12} {row['count']:<10.0f} {row['frequency']:<10.1%} {row['weight']:<10.2f} {row['raw_score']:+.2f}    {row['adjusted_score']:+.2f}")

        print()

# ============================================================================
# STEP 3: Comparison - Raw vs Adjusted
# ============================================================================

print(f"{'=' * 180}")
print("STEP 3: IMPACT OF FREQUENCY ADJUSTMENT")
print("=" * 180)

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    color_stats = []

    for event in df_clean['event_name'].unique():
        for year in df_clean[df_clean['event_name'] == event]['year'].unique():
            event_year_data = round_data[(round_data['event_name'] == event) & (round_data['year'] == year)]

            if len(event_year_data) < 30:
                continue

            field_size = len(event_year_data)
            top40_pct = min(40 / field_size, 1.0)

            event_year_data = event_year_data.copy()
            event_year_data['rank_pct'] = event_year_data['vs_avg'].rank(pct=True)

            top40_cutoff = 1.0 - top40_pct
            top_performers = event_year_data[event_year_data['rank_pct'] >= top40_cutoff]

            for color in event_year_data['color'].unique():
                color_data = event_year_data[event_year_data['color'] == color]
                in_top = (top_performers['color'] == color).sum()
                finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

                color_stats.append({
                    'color': color,
                    'finish_rate': finish_rate,
                    'count': len(color_data),
                })

    if color_stats:
        stats_df = pd.DataFrame(color_stats)
        color_totals = stats_df.groupby('color').agg({
            'finish_rate': 'mean',
            'count': 'sum',
        }).reset_index()

        total_records = stats_df['count'].sum()
        mean_finish = color_totals['finish_rate'].mean()

        results = []
        for _, row in color_totals.iterrows():
            color = row['color']
            finish_rate = row['finish_rate']
            count = row['count']
            frequency = count / total_records
            weight = np.sqrt(frequency)
            raw_score = finish_rate - mean_finish
            adjusted_score = raw_score * weight
            adjustment = adjusted_score - raw_score

            results.append({
                'color': color,
                'count': count,
                'frequency': frequency,
                'raw': raw_score,
                'adjusted': adjusted_score,
                'adjustment': adjustment,
            })

        results_df = pd.DataFrame(results).sort_values('count', ascending=False)

        print(f"\nROUND {round_num} - Adjustment Impact:")
        print(f"  {'Color':<12} {'Count':<8} {'Freq':<8} {'Raw':<8} {'Adjusted':<8} {'Change':<12}")
        print(f"  {'-' * 56}")
        for _, row in results_df.iterrows():
            print(f"  {str(row['color']):<12} {row['count']:<8.0f} {row['frequency']:<8.1%} {row['raw']:+.2f}  {row['adjusted']:+.2f}  {row['adjustment']:+.2f}")

print("\n")
