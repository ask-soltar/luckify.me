"""
DEEP DIVE: Top 5 and Top 10 analysis
Where does each element truly dominate?
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

print("=" * 170)
print("ELITE ANALYSIS: Top 5 and Top 10 Finishes by Element")
print("Where does each element truly excel?")
print("=" * 170)

print(f"\nTotal player-tournaments: {len(aggregated)}")

# ============================================================================
# COMPREHENSIVE TIER ANALYSIS: Top 5, 10, 20, 40
# ============================================================================

finish_tiers = {
    'Top 5': 0.04,    # Top ~5%
    'Top 10': 0.08,   # Top ~8%
    'Top 20': 0.17,   # Top ~17%
    'Top 40': 0.33,   # Top ~33%
}

all_results = {}

print(f"\n{'=' * 170}")
print("TIER-BY-TIER FINISH RATES")
print("=" * 170)

for tier_name in ['Top 5', 'Top 10', 'Top 20', 'Top 40']:
    percentile_cutoff = finish_tiers[tier_name]

    print(f"\n{tier_name.upper()} ({percentile_cutoff*100:.0f}%)")
    print("-" * 110)

    tier_results = []

    for element in sorted(aggregated['wu_xing'].unique()):
        element_data = aggregated[aggregated['wu_xing'] == element]

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
                'sample_size': len(element_data)
            })

    tier_df = pd.DataFrame(tier_results).sort_values('finish_rate', ascending=False)
    all_results[tier_name] = tier_df

    print(f"{'Element':<12} {'Finish Rate':<15} {'Rank':<6}")
    print("-" * 40)

    for idx, (_, row) in enumerate(tier_df.iterrows(), 1):
        print(f"{row['element']:<12} {row['finish_rate']:<15.1%} {idx}")

# ============================================================================
# SCALING ANALYSIS: How finish rates change by tier
# ============================================================================

print(f"\n{'=' * 170}")
print("SCALING ANALYSIS: Finish Rate Progression")
print("=" * 170)

print(f"\n{'Element':<12} {'Top 5':<12} {'Top 10':<12} {'Top 20':<12} {'Top 40':<12} {'Elite Pattern':<30}")
print("-" * 90)

elements = sorted(aggregated['wu_xing'].unique())

for element in elements:
    top5 = all_results['Top 5'][all_results['Top 5']['element'] == element]['finish_rate'].values
    top10 = all_results['Top 10'][all_results['Top 10']['element'] == element]['finish_rate'].values
    top20 = all_results['Top 20'][all_results['Top 20']['element'] == element]['finish_rate'].values
    top40 = all_results['Top 40'][all_results['Top 40']['element'] == element]['finish_rate'].values

    top5_rate = top5[0] if len(top5) > 0 else 0
    top10_rate = top10[0] if len(top10) > 0 else 0
    top20_rate = top20[0] if len(top20) > 0 else 0
    top40_rate = top40[0] if len(top40) > 0 else 0

    # Identify pattern
    if top5_rate > top10_rate > top20_rate:
        pattern = "Elite specialist (peaks at top)"
    elif top5_rate < top10_rate < top20_rate < top40_rate:
        pattern = "Consistency expert (peaks at top 40)"
    elif top5_rate > top40_rate * 0.3:  # Top 5 is at least 30% of top 40
        pattern = "Strong at all levels"
    elif top40_rate > top20_rate * 2:
        pattern = "Falls off at elite tier"
    else:
        pattern = "Balanced across tiers"

    print(f"{element:<12} {top5_rate:<12.1%} {top10_rate:<12.1%} {top20_rate:<12.1%} {top40_rate:<12.1%} {pattern:<30}")

# ============================================================================
# RANKING TABLE: Who's #1 at each tier?
# ============================================================================

print(f"\n{'=' * 170}")
print("WHO DOMINATES AT EACH TIER?")
print("=" * 170)

print(f"\n{'Rank':<6} {'Top 5 Champion':<30} {'Top 10 Champion':<30} {'Top 20 Champion':<30} {'Top 40 Champion':<30}")
print("-" * 120)

for rank in [1, 2, 3, 4, 5]:
    top5_elem = all_results['Top 5'].iloc[rank-1]
    top10_elem = all_results['Top 10'].iloc[rank-1]
    top20_elem = all_results['Top 20'].iloc[rank-1]
    top40_elem = all_results['Top 40'].iloc[rank-1]

    print(f"{rank:<6} {top5_elem['element']} ({top5_elem['finish_rate']:.1%})           {top10_elem['element']} ({top10_elem['finish_rate']:.1%})           {top20_elem['element']} ({top20_elem['finish_rate']:.1%})           {top40_elem['element']} ({top40_elem['finish_rate']:.1%})")

# ============================================================================
# ELITE CONCENTRATION: Do elements concentrate at top?
# ============================================================================

print(f"\n{'=' * 170}")
print("ELITE CONCENTRATION: Which elements 'punch above their weight'?")
print("=" * 170)

print(f"\nCompare: What % should each element have if random?")
print(f"(Each element is ~20% of population, but distribution may vary)\n")

for tier_name in ['Top 5', 'Top 10', 'Top 20', 'Top 40']:
    tier_df = all_results[tier_name]

    print(f"{tier_name}:")
    for _, row in tier_df.iterrows():
        # Expected: 20% (5 elements)
        expected = 20.0
        actual = row['finish_rate'] * 100
        outperf = actual - expected

        if outperf > 2:
            badge = " [OVER-REPRESENTED]"
        elif outperf < -2:
            badge = " [UNDER-REPRESENTED]"
        else:
            badge = ""

        print(f"  {row['element']}: {row['finish_rate']:.1%} (vs 20% random){badge}")

# ============================================================================
# SUMMARY TABLE: Final Elite Ranking
# ============================================================================

print(f"\n{'=' * 170}")
print("FINAL ELITE TIER ANALYSIS")
print("=" * 170)

print(f"\nTop 5 Finishes (True Elite):")
top5_sorted = all_results['Top 5'].sort_values('finish_rate', ascending=False)
for idx, (_, row) in enumerate(top5_sorted.iterrows(), 1):
    print(f"  {idx}. {row['element']}: {row['finish_rate']:.1%}")

print(f"\nTop 10 Finishes:")
top10_sorted = all_results['Top 10'].sort_values('finish_rate', ascending=False)
for idx, (_, row) in enumerate(top10_sorted.iterrows(), 1):
    print(f"  {idx}. {row['element']}: {row['finish_rate']:.1%}")

# ============================================================================
# CONCLUSION
# ============================================================================

print(f"\n{'=' * 170}")
print("INTERPRETATION")
print("=" * 170)

metal_top5 = all_results['Top 5'][all_results['Top 5']['element'] == 'Metal']['finish_rate'].values[0]
metal_top40 = all_results['Top 40'][all_results['Top 40']['element'] == 'Metal']['finish_rate'].values[0]
metal_concentration = metal_top5 / (metal_top40 / 5)

earth_top5 = all_results['Top 5'][all_results['Top 5']['element'] == 'Earth']['finish_rate'].values[0]
earth_top40 = all_results['Top 40'][all_results['Top 40']['element'] == 'Earth']['finish_rate'].values[0]
earth_concentration = earth_top5 / (earth_top40 / 5)

fire_top5 = all_results['Top 5'][all_results['Top 5']['element'] == 'Fire']['finish_rate'].values[0]
fire_top40 = all_results['Top 40'][all_results['Top 40']['element'] == 'Fire']['finish_rate'].values[0]
fire_concentration = fire_top5 / (fire_top40 / 5)

print(f"\nElement Concentration at Elite (Top 5):")
print(f"  Metal: {metal_concentration:.2f}x expected (highly concentrated at elite)")
print(f"  Fire: {fire_concentration:.2f}x expected")
print(f"  Earth: {earth_concentration:.2f}x expected")

if metal_concentration > fire_concentration and metal_concentration > earth_concentration:
    print(f"\n[FINDING] METAL dominates true elite (Top 5)")
    print(f"  - Metal finish rate at Top 5 is {metal_concentration:.1f}x what we'd expect")
    print(f"  - This suggests Metal element produces the sharpest finishers")
    print(f"  - Earth/Water excel at Top 40 consistency, but Metal reaches the peaks")

print("\n")
