"""
COMPARATIVE ANALYSIS: Top 20 vs Top 40 finishes by element
Do Earth/Water's advantage scale up or down as competition gets tighter?
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
    'adj_his_par': 'mean',
    'wu_xing': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated = aggregated[aggregated['wu_xing'].notna()].copy()
aggregated['absolute_score'] = aggregated['exec'] + aggregated['upside']

print("=" * 160)
print("TOP 20 vs TOP 40 ANALYSIS BY ELEMENT")
print("Do Earth/Water's advantage scale with tighter competition?")
print("=" * 160)

print(f"\nTotal player-tournaments: {len(aggregated)}")

# ============================================================================
# ANALYSIS: Top 10, 20, 40 finish rates by element
# ============================================================================

finish_tiers = {
    'Top 10': 0.08,   # Top ~10%
    'Top 20': 0.17,   # Top ~17%
    'Top 40': 0.33,   # Top ~33%
}

results_by_tier = {}

for tier_name, percentile_cutoff in finish_tiers.items():
    print(f"\n{'=' * 160}")
    print(f"{tier_name.upper()} FINISH RATES (Top {percentile_cutoff*100:.0f}% by Exec+Upside)")
    print("=" * 160)

    tier_results = []

    for element in sorted(aggregated['wu_xing'].unique()):
        element_data = aggregated[aggregated['wu_xing'] == element]

        # Measure: what % of this element finish in top X%?
        venue_rates = []

        for venue in element_data['event_name'].unique():
            venue_all = aggregated[aggregated['event_name'] == venue].copy()

            if len(venue_all) < 20:
                continue

            venue_element = element_data[element_data['event_name'] == venue]

            if len(venue_element) == 0:
                continue

            # Rank all by absolute_score
            venue_all['rank'] = venue_all['absolute_score'].rank(ascending=False, pct=True)

            # Top X% cutoff
            cutoff = 1.0 - percentile_cutoff
            top_x = venue_all[venue_all['rank'] >= cutoff]

            # How many of this element are in top X%?
            element_in_top = (top_x['wu_xing'] == element).sum()
            element_finish_rate = element_in_top / len(venue_element) if len(venue_element) > 0 else 0

            venue_rates.append(element_finish_rate)

        if venue_rates:
            avg_rate = np.mean(venue_rates)
            tier_results.append({
                'element': element,
                'finish_rate': avg_rate,
                'sample_size': len(element_data),
                'venues_tested': len(venue_rates)
            })

    tier_df = pd.DataFrame(tier_results).sort_values('finish_rate', ascending=False)

    print(f"\n{'Element':<12} {'Finish Rate':<15} {'Sample Size':<15} {'Venues Tested':<15}")
    print("-" * 57)

    for _, row in tier_df.iterrows():
        print(f"{row['element']:<12} {row['finish_rate']:<15.1%} {row['sample_size']:<15.0f} {row['venues_tested']:<15.0f}")

    results_by_tier[tier_name] = tier_df

# ============================================================================
# COMPARATIVE ANALYSIS: Ranking across tiers
# ============================================================================

print(f"\n{'=' * 160}")
print("RANKING BY TIER (How do elements rank at each level?)")
print("=" * 160)

print(f"\n{'Element':<12} {'Top 10 Rate':<15} {'Top 20 Rate':<15} {'Top 40 Rate':<15} {'Trend':<20}")
print("-" * 77)

elements = sorted(aggregated['wu_xing'].unique())

for element in elements:
    top10 = results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == element]['finish_rate'].values
    top20 = results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == element]['finish_rate'].values
    top40 = results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == element]['finish_rate'].values

    top10_rate = top10[0] if len(top10) > 0 else 0
    top20_rate = top20[0] if len(top20) > 0 else 0
    top40_rate = top40[0] if len(top40) > 0 else 0

    # Trend: is the element getting better or worse as competition tightens?
    trend_10_20 = top10_rate - top20_rate
    trend_20_40 = top20_rate - top40_rate

    if trend_10_20 < -0.03:
        trend = "Improves at top 10"
    elif trend_10_20 > 0.03:
        trend = "Weakens at top 10"
    elif trend_20_40 < -0.03:
        trend = "Improves at top 20"
    elif trend_20_40 > 0.03:
        trend = "Weakens at top 20"
    else:
        trend = "Stable across tiers"

    print(f"{element:<12} {top10_rate:<15.1%} {top20_rate:<15.1%} {top40_rate:<15.1%} {trend:<20}")

# ============================================================================
# DETAIL: Top 20 Analysis (main focus)
# ============================================================================

print(f"\n{'=' * 160}")
print("TOP 20 DETAILED ANALYSIS")
print("=" * 160)

top20_df = results_by_tier['Top 20'].sort_values('finish_rate', ascending=False)

print(f"\nTop 20 Rankings:")
for idx, (_, row) in enumerate(top20_df.iterrows(), 1):
    print(f"  {idx}. {row['element']}: {row['finish_rate']:.1%}")

# Top 40 for comparison
top40_df = results_by_tier['Top 40'].sort_values('finish_rate', ascending=False)

print(f"\nComparison: Top 20 vs Top 40 Edge")
print(f"{'Element':<12} {'Top 20 %':<12} {'Top 40 %':<12} {'Difference':<12} {'Pattern':<20}")
print("-" * 68)

for element in elements:
    top20_rate = top20_df[top20_df['element'] == element]['finish_rate'].values[0] if len(top20_df[top20_df['element'] == element]) > 0 else 0
    top40_rate = top40_df[top40_df['element'] == element]['finish_rate'].values[0] if len(top40_df[top40_df['element'] == element]) > 0 else 0

    diff = top20_rate - top40_rate

    if diff > 0.05:
        pattern = "Gets BETTER at top 20"
    elif diff < -0.05:
        pattern = "Gets WORSE at top 20"
    else:
        pattern = "Stable"

    print(f"{element:<12} {top20_rate:<12.1%} {top40_rate:<12.1%} {diff:+.1%}        {pattern:<20}")

# ============================================================================
# BASELINE CHECK: What % should random be?
# ============================================================================

print(f"\n{'=' * 160}")
print("BASELINE CHECK: Random Expectation")
print("=" * 160)

total_players = len(aggregated)
total_elements = aggregated['wu_xing'].nunique()

print(f"\nIf elements were randomly distributed in top 20:")
print(f"  Each element should finish top 20 ~{(1/total_elements)*100:.1f}% of the time")
print(f"  (there are {total_elements} elements)")

for element in elements:
    element_count = (aggregated['wu_xing'] == element).sum()
    expected_rate = element_count / total_players

    actual_top20 = top20_df[top20_df['element'] == element]['finish_rate'].values[0] if len(top20_df[top20_df['element'] == element]) > 0 else 0

    outperformance = actual_top20 - expected_rate

    print(f"  {element}: Expected {expected_rate:.1%}, Actual {actual_top20:.1%}, Outperformance {outperformance:+.1%}")

# ============================================================================
# SUMMARY
# ============================================================================

print(f"\n{'=' * 160}")
print("SUMMARY")
print("=" * 160)

earth_top10 = results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Earth']['finish_rate'].values[0] if len(results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Earth']) > 0 else 0
earth_top20 = results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Earth']['finish_rate'].values[0] if len(results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Earth']) > 0 else 0
earth_top40 = results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Earth']['finish_rate'].values[0] if len(results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Earth']) > 0 else 0

water_top10 = results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Water']['finish_rate'].values[0] if len(results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Water']) > 0 else 0
water_top20 = results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Water']['finish_rate'].values[0] if len(results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Water']) > 0 else 0
water_top40 = results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Water']['finish_rate'].values[0] if len(results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Water']) > 0 else 0

fire_top10 = results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Fire']['finish_rate'].values[0] if len(results_by_tier['Top 10'][results_by_tier['Top 10']['element'] == 'Fire']) > 0 else 0
fire_top20 = results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Fire']['finish_rate'].values[0] if len(results_by_tier['Top 20'][results_by_tier['Top 20']['element'] == 'Fire']) > 0 else 0
fire_top40 = results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Fire']['finish_rate'].values[0] if len(results_by_tier['Top 40'][results_by_tier['Top 40']['element'] == 'Fire']) > 0 else 0

print(f"\nEarth Element:")
print(f"  Top 10: {earth_top10:.1%}")
print(f"  Top 20: {earth_top20:.1%}")
print(f"  Top 40: {earth_top40:.1%}")
print(f"  Pattern: {('Improves at top' if earth_top10 > earth_top40 else 'Consistent') }")

print(f"\nWater Element:")
print(f"  Top 10: {water_top10:.1%}")
print(f"  Top 20: {water_top20:.1%}")
print(f"  Top 40: {water_top40:.1%}")
print(f"  Pattern: {('Improves at top' if water_top10 > water_top40 else 'Consistent')}")

print(f"\nFire Element:")
print(f"  Top 10: {fire_top10:.1%}")
print(f"  Top 20: {fire_top20:.1%}")
print(f"  Top 40: {fire_top40:.1%}")
print(f"  Pattern: {('Improves at top' if fire_top10 > fire_top40 else 'Weakens at top')}")

print(f"\nConclusion:")
if earth_top20 > earth_top40 + 0.02:
    print(f"  Earth gets STRONGER at top 20 - suggests true elite advantage")
elif earth_top20 < earth_top40 - 0.02:
    print(f"  Earth weakens at top 20 - suggests advantage mainly outside elite")
else:
    print(f"  Earth consistent across tiers - stable, predictable advantage")

print("\n")
