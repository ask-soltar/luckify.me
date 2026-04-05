"""
COMPREHENSIVE DIVINATION TIER ANALYSIS
Test ALL divination attributes across Top 5, 10, 20, 40 tiers
Compare which divination system shows strongest signal at each tier
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
    'zodiac': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'horoscope': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'life_path': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'tithi': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'moon': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'moonwest': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
    'color': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
}).reset_index()

aggregated['absolute_score'] = aggregated['exec'] + aggregated['upside']

print("=" * 180)
print("COMPREHENSIVE DIVINATION TIER ANALYSIS")
print("Testing all divination attributes across Top 5, 10, 20, 40")
print("=" * 180)

print(f"\nDataset: {len(aggregated)} player-tournaments from {aggregated['event_name'].nunique()} venues")

# ============================================================================
# Define tiers
# ============================================================================

finish_tiers = {
    'Top 5': 0.04,
    'Top 10': 0.08,
    'Top 20': 0.17,
    'Top 40': 0.33,
}

# ============================================================================
# Define divination attributes to test
# ============================================================================

divination_attrs = {
    'wu_xing': 'Wu Xing (Element)',
    'zodiac': 'Chinese Zodiac',
    'horoscope': 'Western Horoscope',
    'life_path': 'Life Path (Numerology)',
    'tithi': 'Tithi (Vedic Lunar Day)',
    'moon': 'Moon Phase (Vedic 10-cat)',
    'moonwest': 'Moon Phase (Western 8-cat)',
    'color': 'Color (Rhythm)',
}

# ============================================================================
# Test each divination attribute
# ============================================================================

all_results = {}

for attr_key, attr_name in divination_attrs.items():
    print(f"\n{'=' * 180}")
    print(f"TESTING: {attr_name}")
    print("=" * 180)

    # Check if column exists and has data
    if attr_key not in aggregated.columns:
        print(f"  [SKIP] Column not found in data")
        continue

    attr_data = aggregated[aggregated[attr_key].notna()].copy()
    if len(attr_data) == 0:
        print(f"  [SKIP] No non-null values")
        continue

    unique_vals = attr_data[attr_key].nunique()
    print(f"  Data: {len(attr_data)} records, {unique_vals} unique values")

    tier_results = {}

    for tier_name, percentile_cutoff in finish_tiers.items():
        results = []

        for attr_val in sorted(attr_data[attr_key].unique()):
            if pd.isna(attr_val):
                continue

            attr_subset = attr_data[attr_data[attr_key] == attr_val]
            venue_rates = []

            for venue in attr_subset['event_name'].unique():
                venue_all = aggregated[aggregated['event_name'] == venue].copy()

                if len(venue_all) < 20:
                    continue

                venue_attr = attr_subset[attr_subset['event_name'] == venue]

                if len(venue_attr) == 0:
                    continue

                # Rank by absolute_score
                venue_all['rank'] = venue_all['absolute_score'].rank(ascending=False, pct=True)

                # Top X% cutoff
                cutoff = 1.0 - percentile_cutoff
                top_x = venue_all[venue_all['rank'] >= cutoff]

                # How many of this attr_val are in top X%?
                attr_in_top = (top_x[attr_key] == attr_val).sum()
                attr_finish_rate = attr_in_top / len(venue_attr) if len(venue_attr) > 0 else 0

                venue_rates.append(attr_finish_rate)

            if venue_rates:
                avg_rate = np.mean(venue_rates)
                results.append({
                    'value': str(attr_val),
                    'finish_rate': avg_rate,
                    'sample_size': len(attr_subset),
                })

        results_df = pd.DataFrame(results).sort_values('finish_rate', ascending=False)
        tier_results[tier_name] = results_df

        # Print top 5 for this tier
        print(f"\n  {tier_name} Top Performers:")
        print(f"  {'Rank':<6} {'Value':<25} {'Finish Rate':<15}")
        print(f"  {'-' * 46}")
        for idx, (_, row) in enumerate(results_df.head(5).iterrows(), 1):
            print(f"  {idx:<6} {row['value']:<25} {row['finish_rate']:<15.1%}")

    all_results[attr_key] = tier_results

# ============================================================================
# SUMMARY: Compare divination systems
# ============================================================================

print(f"\n{'=' * 180}")
print("SUMMARY: Signal Strength by Divination System and Tier")
print("=" * 180)

print(f"\nMetric: Max finish rate minus Min finish rate (spread = signal strength)\n")

summary_data = []

for attr_key, attr_name in divination_attrs.items():
    if attr_key not in all_results:
        continue

    print(f"\n{attr_name}:")
    print(f"  {'Tier':<12} {'Best Value':<25} {'Rate':<12} {'Spread':<12}")
    print(f"  {'-' * 61}")

    tier_spreads = {}

    for tier_name in ['Top 5', 'Top 10', 'Top 20', 'Top 40']:
        if tier_name not in all_results[attr_key]:
            continue

        tier_df = all_results[attr_key][tier_name]
        if len(tier_df) == 0:
            continue

        best_rate = tier_df.iloc[0]['finish_rate']
        worst_rate = tier_df.iloc[-1]['finish_rate']
        spread = best_rate - worst_rate
        best_value = tier_df.iloc[0]['value']

        tier_spreads[tier_name] = spread

        print(f"  {tier_name:<12} {best_value:<25} {best_rate:<12.1%} {spread:<12.1%}")

    summary_data.append({
        'attribute': attr_name,
        'top5_spread': tier_spreads.get('Top 5', 0),
        'top10_spread': tier_spreads.get('Top 10', 0),
        'top20_spread': tier_spreads.get('Top 20', 0),
        'top40_spread': tier_spreads.get('Top 40', 0),
    })

# ============================================================================
# Ranking by signal strength
# ============================================================================

print(f"\n{'=' * 180}")
print("DIVINATION SYSTEMS RANKED BY SIGNAL STRENGTH")
print("=" * 180)

summary_df = pd.DataFrame(summary_data)

print(f"\nBest Signal at TOP 5 (Elite Peak):")
print(f"  {'Rank':<6} {'System':<40} {'Spread':<12}")
print(f"  {'-' * 58}")
top5_ranked = summary_df.sort_values('top5_spread', ascending=False)
for idx, (_, row) in enumerate(top5_ranked.head(5).iterrows(), 1):
    print(f"  {idx:<6} {row['attribute']:<40} {row['top5_spread']:<12.1%}")

print(f"\nBest Signal at TOP 10 (Upper Elite):")
print(f"  {'Rank':<6} {'System':<40} {'Spread':<12}")
print(f"  {'-' * 58}")
top10_ranked = summary_df.sort_values('top10_spread', ascending=False)
for idx, (_, row) in enumerate(top10_ranked.head(5).iterrows(), 1):
    print(f"  {idx:<6} {row['attribute']:<40} {row['top10_spread']:<12.1%}")

print(f"\nBest Signal at TOP 20 (Competitive):")
print(f"  {'Rank':<6} {'System':<40} {'Spread':<12}")
print(f"  {'-' * 58}")
top20_ranked = summary_df.sort_values('top20_spread', ascending=False)
for idx, (_, row) in enumerate(top20_ranked.head(5).iterrows(), 1):
    print(f"  {idx:<6} {row['attribute']:<40} {row['top20_spread']:<12.1%}")

print(f"\nBest Signal at TOP 40 (Broad Success):")
print(f"  {'Rank':<6} {'System':<40} {'Spread':<12}")
print(f"  {'-' * 58}")
top40_ranked = summary_df.sort_values('top40_spread', ascending=False)
for idx, (_, row) in enumerate(top40_ranked.head(5).iterrows(), 1):
    print(f"  {idx:<6} {row['attribute']:<40} {row['top40_spread']:<12.1%}")

# ============================================================================
# CONCLUSION
# ============================================================================

print(f"\n{'=' * 180}")
print("CONCLUSION: Which Divination System Has Strongest Predictive Power?")
print("=" * 180)

best_top5 = top5_ranked.iloc[0]
best_top10 = top10_ranked.iloc[0]
best_top20 = top20_ranked.iloc[0]
best_top40 = top40_ranked.iloc[0]

print(f"\nStrongest at each tier:")
print(f"  Top 5:  {best_top5['attribute']} (spread: {best_top5['top5_spread']:.1%})")
print(f"  Top 10: {best_top10['attribute']} (spread: {best_top10['top10_spread']:.1%})")
print(f"  Top 20: {best_top20['attribute']} (spread: {best_top20['top20_spread']:.1%})")
print(f"  Top 40: {best_top40['attribute']} (spread: {best_top40['top40_spread']:.1%})")

# Overall best
avg_spread = summary_df[['top5_spread', 'top10_spread', 'top20_spread', 'top40_spread']].mean(axis=1)
best_overall_idx = avg_spread.idxmax()
best_overall = summary_df.iloc[best_overall_idx]

print(f"\nOverall strongest (average spread across all tiers):")
print(f"  {best_overall['attribute']}")
print(f"    Top 5:  {best_overall['top5_spread']:.1%}")
print(f"    Top 10: {best_overall['top10_spread']:.1%}")
print(f"    Top 20: {best_overall['top20_spread']:.1%}")
print(f"    Top 40: {best_overall['top40_spread']:.1%}")

print("\n")
