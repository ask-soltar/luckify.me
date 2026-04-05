"""
BUILD COLOR SCORING TABLE BY ROUND TYPE
- Score colors relative to field average
- Account for field size (top 40 = different percentiles for different fields)
- Handle cuts (R3/R4 have smaller fields)
- Filter to S-type tournaments (Standard Stroke Play, comparable)
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)

# Filter: S-type tournaments only (Standard Stroke Play = comparable)
df_clean = df[(df['round_type'] != 'REMOVE') & (df['tournament_type'] == 'S')].copy()

print("=" * 180)
print("COLOR SCORING TABLE BY ROUND TYPE")
print("Scoring relative to field, accounting for field size and cuts")
print("=" * 180)

print(f"\nDataset: {len(df_clean)} records from S-type tournaments")
print(f"Events: {df_clean['event_name'].nunique()}")

# ============================================================================
# STEP 1: Analyze field sizes by round
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 1: FIELD SIZE ANALYSIS")
print("=" * 180)

# For each event, count players per round
field_sizes = []

for event in df_clean['event_name'].unique():
    event_data = df_clean[df_clean['event_name'] == event]

    # Count non-null scores per round (players who played that round)
    r1_players = event_data[event_data['round_num'] == 1].shape[0]
    r2_players = event_data[event_data['round_num'] == 2].shape[0]
    r3_players = event_data[event_data['round_num'] == 3].shape[0]
    r4_players = event_data[event_data['round_num'] == 4].shape[0]

    field_sizes.append({
        'event': event,
        'r1_count': r1_players,
        'r2_count': r2_players,
        'r3_count': r3_players,
        'r4_count': r4_players,
    })

field_df = pd.DataFrame(field_sizes)

print(f"\nField Size Summary (across all S-type tournaments):")
print(f"  Round 1: Avg {field_df['r1_count'].mean():.0f} players (min {field_df['r1_count'].min()}, max {field_df['r1_count'].max()})")
print(f"  Round 2: Avg {field_df['r2_count'].mean():.0f} players (min {field_df['r2_count'].min()}, max {field_df['r2_count'].max()})")
print(f"  Round 3: Avg {field_df['r3_count'].mean():.0f} players (min {field_df['r3_count'].min()}, max {field_df['r3_count'].max()})")
print(f"  Round 4: Avg {field_df['r4_count'].mean():.0f} players (min {field_df['r4_count'].min()}, max {field_df['r4_count'].max()})")

avg_r1 = field_df['r1_count'].mean()
avg_r2 = field_df['r2_count'].mean()
avg_r3 = field_df['r3_count'].mean()
avg_r4 = field_df['r4_count'].mean()

# Calculate what percentile = "top 40"
top40_pct_r1 = 40 / avg_r1
top40_pct_r2 = 40 / avg_r2
top40_pct_r3 = 40 / avg_r3
top40_pct_r4 = 40 / avg_r4

print(f"\nTop 40 as percentile (accounting for field size):")
print(f"  Round 1: Top 40 of {avg_r1:.0f} = {top40_pct_r1:.1%}")
print(f"  Round 2: Top 40 of {avg_r2:.0f} = {top40_pct_r2:.1%}")
print(f"  Round 3: Top 40 of {avg_r3:.0f} = {top40_pct_r3:.1%}")
print(f"  Round 4: Top 40 of {avg_r4:.0f} = {top40_pct_r4:.1%}")

print(f"\nObservation: Cut effect detected")
print(f"  R1->R2 change: {avg_r1:.0f} -> {avg_r2:.0f} ({(avg_r2/avg_r1-1)*100:+.1f}%)")
print(f"  R2->R3 change: {avg_r2:.0f} -> {avg_r3:.0f} ({(avg_r3/avg_r2-1)*100:+.1f}%) [CUT LINE]")
print(f"  R3->R4 change: {avg_r3:.0f} -> {avg_r4:.0f} ({(avg_r4/avg_r3-1)*100:+.1f}%)")

# ============================================================================
# STEP 2: Round-level analysis (keep all 4 rounds of data)
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 2: COLOR PERFORMANCE BY ROUND (ROUND-LEVEL DATA)")
print("=" * 180)

# Use round-level data (4 rows per player-event)
df_roundlevel = df_clean[['event_name', 'round_num', 'color', 'score', 'par', 'vs_avg']].copy()
df_roundlevel = df_roundlevel[df_roundlevel['color'].notna()].copy()

# For each round, create a scoring metric
# Within each event-round, rank by vs_avg (actual finish)
scoring_by_round = []

for round_num in [1, 2, 3, 4]:
    round_data = df_roundlevel[df_roundlevel['round_num'] == round_num].copy()

    # Rank within each event
    round_data['rank_pct'] = round_data.groupby('event_name')['vs_avg'].rank(pct=True)

    # Determine percentile cutoff for "top 40"
    if round_num in [1, 2]:
        cutoff = top40_pct_r1 if round_num == 1 else top40_pct_r2
    else:
        cutoff = top40_pct_r3 if round_num == 3 else top40_pct_r4

    top_cutoff = 1.0 - cutoff
    top_performers = round_data[round_data['rank_pct'] >= top_cutoff]

    # Calculate finish rate for each color
    results = []
    for color in sorted(round_data['color'].unique()):
        color_data = round_data[round_data['color'] == color]
        in_top = (top_performers['color'] == color).sum()
        finish_rate = in_top / len(color_data) if len(color_data) > 0 else 0

        results.append({
            'round': round_num,
            'color': color,
            'count': len(color_data),
            'finish_rate': finish_rate,
        })

    results_df = pd.DataFrame(results).sort_values('finish_rate', ascending=False)

    print(f"\nROUND {round_num} - Top {cutoff:.1%} percentile cutoff")
    print(f"  Avg field: {[avg_r1, avg_r2, avg_r3, avg_r4][round_num-1]:.0f} players")
    print(f"  Top 40 = {cutoff:.1%} of field")
    print(f"  {'Color':<15} {'Count':<10} {'Finish Rate':<15}")
    print(f"  {'-' * 40}")

    for _, row in results_df.iterrows():
        print(f"  {str(row['color']):<15} {row['count']:<10.0f} {row['finish_rate']:<15.1%}")

    scoring_by_round.append(results_df)

# ============================================================================
# STEP 3: Create scoring table (relative to mean)
# ============================================================================

print(f"\n{'=' * 180}")
print("STEP 3: COLOR SCORING TABLE (relative to mean)")
print("=" * 180)

print(f"\nScoring method: score = finish_rate - mean_finish_rate")
print(f"Interpretation: +0.10 = +10pp advantage over average color\n")

all_scores = {}

for round_num in [1, 2, 3, 4]:
    results_df = scoring_by_round[round_num - 1]

    # Mean finish rate for this round
    mean_rate = results_df['finish_rate'].mean()

    # Create scores
    scores = {}
    for _, row in results_df.iterrows():
        color = row['color']
        score = row['finish_rate'] - mean_rate
        scores[color] = score

    all_scores[round_num] = scores

    print(f"\nROUND {round_num} Scoring Table:")
    print(f"  (Mean finish rate: {mean_rate:.1%})")
    print(f"  {'Color':<15} {'Finish Rate':<15} {'Score':<15} {'Rating':<20}")
    print(f"  {'-' * 65}")

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

        print(f"  {str(color):<15} {rate:<15.1%} {score:+.2f}      {rating:<20}")

# ============================================================================
# STEP 4: Create final scoring table
# ============================================================================

print(f"\n{'=' * 180}")
print("FINAL COLOR SCORING TABLE (READY TO USE)")
print("=" * 180)

print(f"\nFormat: For each round and round_type, score = color's advantage over mean\n")

# Create a comprehensive table
final_table = []

for round_num in [1, 2, 3, 4]:
    results_df = scoring_by_round[round_num - 1]
    mean_rate = results_df['finish_rate'].mean()

    for color in sorted(results_df['color'].unique()):
        rate = results_df[results_df['color'] == color]['finish_rate'].values[0]
        score = rate - mean_rate

        final_table.append({
            'round': round_num,
            'color': color,
            'finish_rate': rate,
            'score': score,
            'vs_mean': f"{score:+.1%}",
        })

final_df = pd.DataFrame(final_table)

print(f"{'Round':<8} {'Color':<15} {'Finish Rate':<15} {'Score (vs Mean)':<20}")
print(f"{'-' * 58}")

for round_num in [1, 2, 3, 4]:
    round_colors = final_df[final_df['round'] == round_num].sort_values('score', ascending=False)

    for _, row in round_colors.iterrows():
        print(f"{row['round']:<8} {str(row['color']):<15} {row['finish_rate']:<15.1%} {row['score']:+.1%}")

    print()

# ============================================================================
# STEP 5: Summary & recommendations
# ============================================================================

print(f"{'=' * 180}")
print("SUMMARY: KEY INSIGHTS")
print("=" * 180)

# Find best and worst per round
for round_num in [1, 2, 3, 4]:
    round_colors = final_df[final_df['round'] == round_num].sort_values('score', ascending=False)
    best = round_colors.iloc[0]
    worst = round_colors.iloc[-1]
    spread = best['score'] - worst['score']

    print(f"\nROUND {round_num}:")
    print(f"  Best:  {best['color']} ({best['score']:+.1%})")
    print(f"  Worst: {worst['color']} ({worst['score']:+.1%})")
    print(f"  Spread: {spread:.1%} (signal strength)")

# Overall patterns
r1_best = final_df[final_df['round'] == 1].nlargest(1, 'score').iloc[0]
r4_best = final_df[final_df['round'] == 4].nlargest(1, 'score').iloc[0]

print(f"\n\nCUT EFFECT ANALYSIS:")
print(f"  R1 favorite: {r1_best['color']} ({r1_best['score']:+.1%})")
print(f"  R4 favorite: {r4_best['color']} ({r4_best['score']:+.1%})")
if r1_best['color'] != r4_best['color']:
    print(f"  -> Color advantage CHANGES from R1 to R4 (cut affects strategy)")
else:
    print(f"  -> Color advantage is CONSISTENT across rounds")

print("\n")
