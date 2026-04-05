"""
CRITICAL AUDIT: Is color/moon analysis biased by distribution?

Tests two methodologies:
1. AGGREGATED (current): One row per player-event, color = mode
2. ROUND-LEVEL: One row per player-event-round (4x data), color = actual

Also checks distribution to see if rare colors get filtered out
"""

import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv('Golf Historics v3 - ANALYSIS (2).csv', low_memory=False)
df_clean = df[df['round_type'] != 'REMOVE'].copy()

print("=" * 180)
print("AUDIT: COLOR & MOON DISTRIBUTION BIAS")
print("=" * 180)

# ============================================================================
# PART 1: Check distribution of colors and moons
# ============================================================================

print(f"\n{'=' * 180}")
print("PART 1: DISTRIBUTION - How common is each color/moon?")
print("=" * 180)

print(f"\nCOLOR DISTRIBUTION (all {len(df_clean)} round records):")
color_dist = df_clean['color'].value_counts().sort_values(ascending=False)
color_pct = (color_dist / len(df_clean) * 100).round(1)
print(f"\n{'Color':<15} {'Count':<10} {'Percent':<10}")
print("-" * 35)
for color, count in color_dist.items():
    pct = color_pct[color]
    print(f"{str(color):<15} {count:<10} {pct:<10}%")

print(f"\nMOON (Vedic) DISTRIBUTION (all {len(df_clean)} round records):")
moon_dist = df_clean['moon'].value_counts().sort_values(ascending=False)
moon_pct = (moon_dist / len(df_clean) * 100).round(1)
print(f"\n{'Moon':<30} {'Count':<10} {'Percent':<10}")
print("-" * 50)
for moon, count in moon_dist.items():
    pct = moon_pct[moon]
    print(f"{str(moon):<30} {count:<10} {pct:<10}%")

print(f"\nMOON (Western) DISTRIBUTION (all {len(df_clean)} round records):")
moonwest_dist = df_clean['moonwest'].value_counts().sort_values(ascending=False)
moonwest_pct = (moonwest_dist / len(df_clean) * 100).round(1)
print(f"\n{'Moon':<30} {'Count':<10} {'Percent':<10}")
print("-" * 50)
for moon, count in moonwest_dist.items():
    pct = moonwest_pct[moon]
    print(f"{str(moon):<30} {count:<10} {pct:<10}%")

# ============================================================================
# PART 2: AGGREGATED APPROACH (current method)
# ============================================================================

print(f"\n{'=' * 180}")
print("PART 2: AGGREGATED APPROACH (one row per player-event, color=mode)")
print("=" * 180)

aggregated = df_clean.groupby(['event_name', 'player_name']).agg({
    'exec': 'mean',
    'upside': 'mean',
    'vs_avg': 'mean',
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'moon': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'moonwest': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated['absolute_score'] = aggregated['exec'] + aggregated['upside']
aggregated = aggregated[aggregated['color'].notna()].copy()

print(f"\nDataset size: {len(aggregated)} player-events (after removing NaN colors)")
print(f"Color distribution (aggregated level):")
agg_color_dist = aggregated['color'].value_counts().sort_values(ascending=False)
agg_color_pct = (agg_color_dist / len(aggregated) * 100).round(1)
print(f"\n{'Color':<15} {'Count':<10} {'Percent':<10}")
print("-" * 35)
for color, count in agg_color_dist.items():
    pct = agg_color_pct[color]
    print(f"{str(color):<15} {count:<10} {pct:<10}%")

# Calculate Top 40 for aggregated
aggregated['rank'] = aggregated['absolute_score'].rank(ascending=False, pct=True)
agg_top40_cutoff = 0.67
agg_top40 = aggregated[aggregated['rank'] >= agg_top40_cutoff]

print(f"\nTop 40 (aggregated) by color:")
print(f"{'Color':<15} {'Count in Top 40':<20} {'Finish Rate':<15}")
print("-" * 50)
for color in sorted(aggregated['color'].unique()):
    color_data = aggregated[aggregated['color'] == color]
    in_top40 = (agg_top40['color'] == color).sum()
    rate = in_top40 / len(color_data) if len(color_data) > 0 else 0
    print(f"{str(color):<15} {len(color_data):<20} {rate:<15.1%}")

# ============================================================================
# PART 3: ROUND-LEVEL APPROACH (alternative method)
# ============================================================================

print(f"\n{'=' * 180}")
print("PART 3: ROUND-LEVEL APPROACH (4 rows per player-event, color=actual)")
print("=" * 180)

# For round-level, we need score for that round, not 4-round aggregate
# Let's create a round-level dataset

# Assuming columns D-G are R1-R4 scores, and we need to calculate vs_avg per round
# This is more complex, let me use a simpler approach:
# Rank by average score but keep round-level colors/moons

print(f"\nRound-level dataset size: {len(df_clean)} records (4x aggregated)")

# Group by event + player, but keep all round records
df_roundlevel = df_clean[['event_name', 'player_name', 'exec', 'upside', 'vs_avg', 'color', 'moon', 'moonwest']].copy()
df_roundlevel = df_roundlevel[df_roundlevel['color'].notna()].copy()
df_roundlevel['absolute_score'] = df_roundlevel['exec'] + df_roundlevel['upside']

# Rank within each event
df_roundlevel['rank_within_event'] = df_roundlevel.groupby('event_name')['absolute_score'].rank(ascending=False, pct=True)

# Top 40 cutoff
rl_top40_cutoff = 0.67
rl_top40 = df_roundlevel[df_roundlevel['rank_within_event'] >= rl_top40_cutoff]

print(f"\nTop 40 (round-level) by color:")
print(f"{'Color':<15} {'Count in Top 40':<20} {'Finish Rate':<15}")
print("-" * 50)
for color in sorted(df_roundlevel['color'].unique()):
    color_rounds = df_roundlevel[df_roundlevel['color'] == color]
    in_top40 = (rl_top40['color'] == color).sum()
    rate = in_top40 / len(color_rounds) if len(color_rounds) > 0 else 0
    print(f"{str(color):<15} {len(color_rounds):<20} {rate:<15.1%}")

# ============================================================================
# PART 4: COMPARISON - Do results differ?
# ============================================================================

print(f"\n{'=' * 180}")
print("PART 4: METHODOLOGY COMPARISON")
print("=" * 180)

print(f"\nTOP 40 FINISH RATES: Aggregated vs Round-Level\n")
print(f"{'Color':<15} {'Aggregated':<20} {'Round-Level':<20} {'Difference':<15}")
print("-" * 70)

for color in sorted(df_roundlevel['color'].unique()):
    # Aggregated
    agg_color = aggregated[aggregated['color'] == color]
    agg_rate = (agg_top40['color'] == color).sum() / len(agg_color) if len(agg_color) > 0 else 0

    # Round-level
    rl_color = df_roundlevel[df_roundlevel['color'] == color]
    rl_rate = (rl_top40['color'] == color).sum() / len(rl_color) if len(rl_color) > 0 else 0

    diff = agg_rate - rl_rate

    print(f"{str(color):<15} {agg_rate:<20.1%} {rl_rate:<20.1%} {diff:+.1%}")

# ============================================================================
# PART 5: BIAS DETECTION
# ============================================================================

print(f"\n{'=' * 180}")
print("PART 5: IS THERE BIAS?")
print("=" * 180)

print(f"\nQuestion: Are rare colors over-represented or under-represented in Top 40?\n")

# Expected vs actual
total_colors = len(df_roundlevel)
for color in sorted(df_roundlevel['color'].unique()):
    color_count = len(df_roundlevel[df_roundlevel['color'] == color])
    expected_pct = color_count / total_colors * 100

    actual_top40 = (rl_top40['color'] == color).sum()
    actual_pct = actual_top40 / len(rl_top40) * 100 if len(rl_top40) > 0 else 0

    bias = actual_pct - expected_pct

    print(f"{str(color):<15} Expected: {expected_pct:>6.1f}%  Actual: {actual_pct:>6.1f}%  Bias: {bias:+6.1f}pp")

# ============================================================================
# PART 6: CONCLUSION
# ============================================================================

print(f"\n{'=' * 180}")
print("CONCLUSION")
print("=" * 180)

print(f"""
Question 1: Are rare colors biased?
- If expected % = actual %, NO BIAS (color is truly predictive)
- If actual % > expected %, YES BIAS FAVORING that color (over-represented)
- If actual % < expected %, YES BIAS AGAINST that color (under-represented)

Question 2: Do aggregated vs round-level approaches give different results?
- If rates are similar: Method doesn't matter (both valid)
- If rates differ significantly: Need to choose correct method

Question 3: Should we use round-level data?
- Pro: Each round has its own color/moon (captures 4 chances per player)
- Pro: No artificial aggregation (mode) losing information
- Con: More data (4x), might be correlated (same player appears 4x)
- Answer: Depends on question - are we predicting player performance or round performance?
""")

# Check if there's a big difference
max_agg = (agg_top40['color'] == color).sum() / len(agg_color) if len(agg_color) > 0 else 0
min_agg = 0
for color in sorted(aggregated['color'].unique()):
    agg_color = aggregated[aggregated['color'] == color]
    rate = (agg_top40['color'] == color).sum() / len(agg_color) if len(agg_color) > 0 else 0
    min_agg = min(min_agg, rate)

agg_spread = max_agg - min_agg

max_rl = 0
min_rl = 1
for color in sorted(df_roundlevel['color'].unique()):
    rl_color = df_roundlevel[df_roundlevel['color'] == color]
    rate = (rl_top40['color'] == color).sum() / len(rl_color) if len(rl_color) > 0 else 0
    max_rl = max(max_rl, rate)
    min_rl = min(min_rl, rate)

rl_spread = max_rl - min_rl

print(f"\nSignal strength comparison:")
print(f"  Aggregated method: {agg_spread:.1%} spread (max - min)")
print(f"  Round-level method: {rl_spread:.1%} spread (max - min)")
print(f"  Difference: {abs(agg_spread - rl_spread):.1%}")

if abs(agg_spread - rl_spread) < 0.05:
    print(f"  → Methods agree. Current approach is valid.")
else:
    print(f"  → Methods DISAGREE. Need to reconsider methodology.")

print("\n")
