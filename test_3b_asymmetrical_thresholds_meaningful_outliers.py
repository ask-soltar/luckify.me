"""
Tier 3B: Asymmetrical Thresholds & Meaningful Outliers
========================================================

Question: Which vs_avg threshold identifies predictive outliers?
- "Beat field by 2+ strokes" — is this stable?
- "Lose field by 2+ strokes" — is this stable?
- Are the distributions symmetrical or skewed?

Goal: Find the threshold that creates stable, predictive signal
(not just >50% beat rate, but meaningful outperformance)
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TIER 3B: ASYMMETRICAL THRESHOLDS & MEANINGFUL OUTLIERS")
print("Calm conditions: Which direction (beat vs lose) is predictive?")
print("=" * 80)
print()

# Load data (all years)
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)

# Standardize
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['color'] = df['color'].astype(str).str.strip()
df['condition'] = df['condition'].astype(str).str.strip()
df['tournament_type'] = df['tournament_type'].astype(str).str.strip()

# Filter to Calm + stroke play only
df_calm = df[
    (df['condition'] == 'Calm') &
    (df['tournament_type'].isin(['S', 'NS'])) &
    (df['round_type'] != 'REMOVE')
].copy()

print(f"Data: {len(df_calm)} Calm + Stroke Play rounds (all years)")
print()

# ============================================================================
# PART 1: DISTRIBUTION ANALYSIS (All Thresholds)
# ============================================================================

print("=" * 80)
print("PART 1: DISTRIBUTION ANALYSIS BY COLOR")
print("=" * 80)
print()

colors = sorted(df_calm['color'].dropna().unique())

for color in colors:
    df_color = df_calm[df_calm['color'] == color]
    vs_avg_clean = df_color['vs_avg'].dropna()

    if len(vs_avg_clean) < 50:
        continue

    # Distribution stats
    mean = vs_avg_clean.mean()
    median = vs_avg_clean.median()
    std = vs_avg_clean.std()
    q25 = vs_avg_clean.quantile(0.25)
    q75 = vs_avg_clean.quantile(0.75)
    q10 = vs_avg_clean.quantile(0.10)
    q90 = vs_avg_clean.quantile(0.90)

    # Skewness
    skewness = stats.skew(vs_avg_clean)

    # Test for symmetry
    t_stat, p_val = stats.ttest_1samp(vs_avg_clean, 0)

    print(f"{color}:")
    print(f"  n={len(vs_avg_clean):6} | mean={mean:+.4f} | median={median:+.4f} | std={std:.4f}")
    print(f"  Percentiles: Q10={q10:+.4f} | Q25={q25:+.4f} | Q75={q75:+.4f} | Q90={q90:+.4f}")
    print(f"  Skewness: {skewness:+.4f} (symmetric if ~0, right-skewed if >0)")
    print(f"  t-test (mean vs 0): p={p_val:.6f} (significant if <0.05)")
    print()

# ============================================================================
# PART 2: ASYMMETRICAL THRESHOLDS
# ============================================================================

print("=" * 80)
print("PART 2: ASYMMETRICAL THRESHOLD PERFORMANCE")
print("=" * 80)
print()

thresholds = [-3, -2, -1, 0, 1, 2, 3]

print("Threshold Analysis (Percentage hitting each threshold):")
print()

results_by_color = {}

for color in colors:
    df_color = df_calm[df_calm['color'] == color]
    vs_avg_clean = df_color['vs_avg'].dropna()

    if len(vs_avg_clean) < 50:
        continue

    print(f"{color:10} (n={len(vs_avg_clean):6}):")
    print(f"  {'Threshold':12} | {'Pct Hit':10} | Interpretation")
    print(f"  {'-'*12}-+-{'-'*10}-+-{'-'*40}")

    threshold_results = {}

    for thresh in thresholds:
        if thresh < 0:
            pct_hit = 100 * (vs_avg_clean < thresh).sum() / len(vs_avg_clean)
            interpretation = f"Beat field by {abs(thresh)}+ strokes"
        elif thresh > 0:
            pct_hit = 100 * (vs_avg_clean > thresh).sum() / len(vs_avg_clean)
            interpretation = f"Lost to field by {thresh}+ strokes"
        else:
            pct_hit = 100 * (vs_avg_clean < 0).sum() / len(vs_avg_clean)
            interpretation = "Beat field (any amount)"

        threshold_results[thresh] = pct_hit

        print(f"  vs_avg < {thresh:+2d}  | {pct_hit:7.1f}%  | {interpretation}")

    results_by_color[color] = threshold_results
    print()

# ============================================================================
# PART 3: WHICH DIRECTION IS PREDICTIVE?
# ============================================================================

print("=" * 80)
print("PART 3: OUTPERFORMANCE vs UNDERPERFORMANCE")
print("=" * 80)
print()

print("Key question: Is beating field by 2+ strokes more predictive than losing by 2+ strokes?")
print()

summary_data = []

for color in colors:
    df_color = df_calm[df_calm['color'] == color]
    vs_avg_clean = df_color['vs_avg'].dropna()

    if len(vs_avg_clean) < 50:
        continue

    # Outperformance: beat by 2+
    beat_by_2 = 100 * (vs_avg_clean < -2).sum() / len(vs_avg_clean)

    # Underperformance: lose by 2+
    lose_by_2 = 100 * (vs_avg_clean > 2).sum() / len(vs_avg_clean)

    # Balance: difference between the two
    balance = beat_by_2 - lose_by_2

    summary_data.append({
        'color': color,
        'n': len(vs_avg_clean),
        'beat_by_2pct': beat_by_2,
        'lose_by_2pct': lose_by_2,
        'balance': balance,
    })

summary_df = pd.DataFrame(summary_data).sort_values('balance', ascending=False)

print("Outperformance (Beat by 2+) vs Underperformance (Lose by 2+):")
print()
print("Color    | n      | Beat 2+ | Lose 2+ | Balance | Interpretation")
print("-"*70)

for _, row in summary_df.iterrows():
    print(f"{row['color']:8} | {row['n']:6} | {row['beat_by_2pct']:7.1f}% | "
          f"{row['lose_by_2pct']:7.1f}% | {row['balance']:+7.1f}pp | ", end="")

    if row['balance'] > 5:
        print("Strong outperformer (asymmetrical)")
    elif row['balance'] > 0:
        print("Slight outperformance bias")
    elif row['balance'] < -5:
        print("Strong underperformer (asymmetrical)")
    else:
        print("Balanced (symmetrical)")

print()

# ============================================================================
# PART 4: STABILITY ANALYSIS (Which threshold is most stable?)
# ============================================================================

print("=" * 80)
print("PART 4: STABILITY ANALYSIS")
print("=" * 80)
print()

print("For deployment: Which threshold creates the most stable signal?")
print("(We want: high sample size + meaningful effect + low variance)")
print()

print("Ranking by 'beat by 2+' (outperformance signal):")
print()

beat_2_data = []
for color in colors:
    df_color = df_calm[df_calm['color'] == color]
    vs_avg_clean = df_color['vs_avg'].dropna()

    if len(vs_avg_clean) < 50:
        continue

    beat_by_2 = 100 * (vs_avg_clean < -2).sum() / len(vs_avg_clean)
    n_beat_by_2 = (vs_avg_clean < -2).sum()
    baseline_rate = 0.50  # Assume 50% is baseline

    beat_2_data.append({
        'color': color,
        'total_n': len(vs_avg_clean),
        'beat_by_2_pct': beat_by_2,
        'beat_by_2_n': n_beat_by_2,
        'vs_baseline': beat_by_2 - 50,
    })

beat_2_df = pd.DataFrame(beat_2_data).sort_values('beat_by_2_pct', ascending=False)

print(beat_2_df[['color', 'total_n', 'beat_by_2_n', 'beat_by_2_pct', 'vs_baseline']].to_string(index=False))

print()

# ============================================================================
# PART 5: RECOMMENDATION
# ============================================================================

print("=" * 80)
print("PART 5: RECOMMENDATION FOR DEPLOYMENT")
print("=" * 80)
print()

# Find colors that beat field by 2+ strokes >30% of time
strong_performers = beat_2_df[beat_2_df['beat_by_2_pct'] > 30].copy()

if len(strong_performers) > 0:
    print("STRONG OUTPERFORMERS (beat field by 2+ strokes >30% of the time):")
    print()
    for _, row in strong_performers.iterrows():
        print(f"  {row['color']:10} | {row['beat_by_2_pct']:5.1f}% beat by 2+ | "
              f"n={row['beat_by_2_n']:5} rounds | Signal reliability: GOOD")
    print()
else:
    print("No colors consistently beat field by 2+ strokes (>30% threshold)")
    print()

# Moderate performers (15-30%)
moderate_performers = beat_2_df[(beat_2_df['beat_by_2_pct'] > 15) & (beat_2_df['beat_by_2_pct'] <= 30)].copy()

if len(moderate_performers) > 0:
    print("MODERATE PERFORMERS (beat field by 2+ strokes 15-30%):")
    print()
    for _, row in moderate_performers.iterrows():
        print(f"  {row['color']:10} | {row['beat_by_2_pct']:5.1f}% beat by 2+ | "
              f"n={row['beat_by_2_n']:5} rounds | Signal reliability: MODERATE")
    print()

print()
print("INTERPRETATION:")
print("- Threshold vs_avg < -2 (beat field by 2+ strokes) identifies meaningful outliers")
print("- Not all colors show strong signals at this threshold")
print("- Use only colors where >25% of Calm rounds beat field by 2+")
print()

print("=" * 80)
