"""
Tier 3: Color Uniqueness Test
==============================

Question: Is Orange special in Calm conditions, or do all colors perform similarly?

Hypothesis: Orange + Calm beats field 56.8%. But does Red/Green/Blue/etc also beat field ~57% in Calm?

If YES (all colors ~57%): Signal is CONDITION-driven, not color-driven
If NO (Orange > others): Signal is COLOR-specific, Orange is genuinely special

Test: For each color, calculate beat_field% in Calm conditions only
Compare to baseline (50%) and to Orange (56.8%)
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TIER 3: COLOR UNIQUENESS TEST — Is Orange special or is it Calm?")
print("=" * 80)
print()

# Load data (all years to maximize sample)
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
# TEST: EACH COLOR IN CALM CONDITIONS
# ============================================================================

print("=" * 80)
print("COLOR PERFORMANCE IN CALM CONDITIONS")
print("=" * 80)
print()

colors = sorted(df_calm['color'].dropna().unique())
results = []

for color in colors:
    df_color = df_calm[df_calm['color'] == color]
    vs_avg_clean = df_color['vs_avg'].dropna()

    if len(vs_avg_clean) < 20:
        continue

    mean_vs_avg = vs_avg_clean.mean()
    std_vs_avg = vs_avg_clean.std()
    beat_field_pct = 100 * (vs_avg_clean < 0).sum() / len(vs_avg_clean)

    # T-test vs 0 (is effect significant?)
    t_stat, p_val = stats.ttest_1samp(vs_avg_clean, 0, nan_policy='omit')

    # How much better/worse than Orange's 56.8%?
    diff_from_orange = beat_field_pct - 56.8

    results.append({
        'color': color,
        'n': len(vs_avg_clean),
        'mean_vs_avg': mean_vs_avg,
        'std': std_vs_avg,
        'beat_field_pct': beat_field_pct,
        'diff_from_orange': diff_from_orange,
        'p_value': p_val,
    })

    print(f"{color:10} | n={len(vs_avg_clean):6} | mean={mean_vs_avg:+.4f} | "
          f"beat%={beat_field_pct:5.1f}% | vs Orange: {diff_from_orange:+5.1f}pp | p={p_val:.6f}")

print()

# ============================================================================
# COMPARISON: ORANGE vs OTHERS
# ============================================================================

print("=" * 80)
print("STATISTICAL COMPARISON")
print("=" * 80)
print()

# Orange data
df_orange = df_calm[df_calm['color'] == 'Orange']
orange_vs_avg = df_orange['vs_avg'].dropna()

if len(orange_vs_avg) > 0:
    orange_mean = orange_vs_avg.mean()
    orange_beat_pct = 100 * (orange_vs_avg < 0).sum() / len(orange_vs_avg)
    print(f"Orange baseline: n={len(orange_vs_avg):6} | beat%={orange_beat_pct:5.1f}%")
    print()

    # T-test: Orange vs each other color
    print("T-tests: Orange vs each color (independent samples)")
    print()

    for result in results:
        if result['color'] == 'Orange':
            continue

        df_other = df_calm[df_calm['color'] == result['color']]
        other_vs_avg = df_other['vs_avg'].dropna()

        if len(other_vs_avg) < 20:
            continue

        t_stat, p_val = stats.ttest_ind(orange_vs_avg, other_vs_avg)

        effect_size = abs(orange_mean - result['mean_vs_avg'])

        print(f"{result['color']:10} vs Orange: t={t_stat:7.4f}, p={p_val:.6f}, "
              f"effect_size={effect_size:.4f}")

    print()

# ============================================================================
# INTERPRETATION
# ============================================================================

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

# Rank colors by beat%
results_sorted = sorted(results, key=lambda x: x['beat_field_pct'], reverse=True)

print("Ranking (best to worst):")
for i, r in enumerate(results_sorted, 1):
    status = ""
    if r['beat_field_pct'] > 55:
        status = " <- BEATS BASELINE (55%+)"
    elif r['beat_field_pct'] > 51:
        status = " <- Near baseline (51-55%)"
    else:
        status = " <- Below baseline (50%)"

    print(f"{i}. {r['color']:10} {r['beat_field_pct']:5.1f}%{status}")

print()

# Cluster analysis: are they all similar?
beat_pcts = [r['beat_field_pct'] for r in results]
mean_beat = np.mean(beat_pcts)
std_beat = np.std(beat_pcts)
max_beat = max(beat_pcts)
min_beat = min(beat_pcts)
spread = max_beat - min_beat

print(f"Color distribution statistics (beat%):")
print(f"  Mean: {mean_beat:.1f}%")
print(f"  Std Dev: {std_beat:.1f}%")
print(f"  Range: {min_beat:.1f}% to {max_beat:.1f}% (spread: {spread:.1f}pp)")
print()

if spread < 5:
    print("Interpretation: All colors behave SIMILARLY in Calm (spread < 5pp)")
    print("  Conclusion: Signal is CONDITION-driven, not color-specific")
    print("  Action: Could use any color + Calm, but Orange is slightly better")
elif spread > 10:
    print("Interpretation: Colors show DIFFERENT responses in Calm (spread > 10pp)")
    print("  Conclusion: Signal is COLOR-specific. Orange is genuinely unique")
    print("  Action: Use Orange specifically, don't generalize to other colors")
else:
    print(f"Interpretation: Colors show MODERATE differences (spread {spread:.1f}pp)")
    print("  Conclusion: Some color effect exists, but Calm also plays a role")
    print("  Action: Orange is best, but others are usable (with reduced confidence)")

print()

# ============================================================================
# PRACTICAL DEPLOYMENT IMPLICATION
# ============================================================================

print("=" * 80)
print("DEPLOYMENT IMPLICATION")
print("=" * 80)
print()

orange_result = [r for r in results if r['color'] == 'Orange'][0] if len(results) > 0 else None

if orange_result:
    orange_beat = orange_result['beat_field_pct']

    print(f"Orange + Calm: {orange_beat:.1f}% beat field (validated signal)")
    print()

    print("For deployment screener:")
    print("  Option A: Use only Orange (as currently designed)")
    print("            Pro: Single validated signal")
    print("            Con: Misses non-Orange Calm days")
    print()

    other_colors = [r for r in results if r['color'] != 'Orange']
    if other_colors:
        avg_other = np.mean([r['beat_field_pct'] for r in other_colors])
        print(f"  Option B: Accept any color in Calm (avg beat%={avg_other:.1f}%)")
        print("            Pro: More frequent matches")
        print(f"            Con: Lower accuracy (Orange is {orange_beat - avg_other:.1f}pp better)")
        print()

        print("  RECOMMENDATION:")
        if spread < 5:
            print("    -> Option B is reasonable. Condition matters more than color.")
            print("    -> Could add 'calm_any_color' as secondary signal (weaker)")
        else:
            print("    -> Stay with Option A. Orange specificity is validated.")
            print("    -> Don't generalize to other colors yet.")

print()

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("=" * 80)
print("SUMMARY TABLE (All Colors in Calm)")
print("=" * 80)
print()

summary_df = pd.DataFrame(results).sort_values('beat_field_pct', ascending=False)
print(summary_df[['color', 'n', 'beat_field_pct', 'mean_vs_avg', 'p_value']].to_string(index=False))

print()
print("=" * 80)
