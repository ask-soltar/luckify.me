"""
Tier 1 Tests 1A & 1B: Orange Talent Equalizer Validation (2025/2026)
=====================================================================

Test 1A: Does the pattern hold on 2025/2026 out-of-sample data?
Test 1B: Is the pattern consistent across deciles (more granular than quartiles)?

Hypothesis: Elite players underperform vs own par more than weak players in Orange
- Elite (top 25%): underperformance ~0.32 strokes
- Weak (bottom 25%): underperformance ~0.09 strokes
- If pattern reverses/weakens in 2025/2026, it was an artifact

Key metrics:
- vs_own_par = off_par - adj_his_par (positive = lost to own average)
- Negative vs_own_par = beat own average (good)
- Positive vs_own_par = underperformed own average (bad)
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TIER 1 TESTS 1A & 1B: ORANGE TALENT EQUALIZER VALIDATION")
print("Out-of-Sample 2025/2026 Data")
print("=" * 80)
print()

# Load data
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)

# Filter to Orange + stroke play + 2025/2026 only
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['color'] = df['color'].astype(str).str.strip()
df['tournament_type'] = df['tournament_type'].astype(str).str.strip()
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['condition'] = df['condition'].astype(str).str.strip()

df_orange = df[
    (df['color'] == 'Orange') &
    (df['tournament_type'].isin(['S', 'NS'])) &
    (df['year'] >= 2025) &
    (df['round_type'] != 'REMOVE')
].copy()

df_orange['vs_own_par'] = df_orange['off_par'] - df_orange['adj_his_par']

n_total = len(df_orange)
n_clean = df_orange['vs_own_par'].notna().sum()

print(f"Data Loaded:")
print(f"  Orange + Stroke Play 2025/2026: {n_total} rows")
print(f"  vs_own_par available: {n_clean} rows")
print(f"  Years: 2025={len(df_orange[df_orange['year']==2025])}, 2026={len(df_orange[df_orange['year']==2026])}")
print()

# ============================================================================
# TEST 1A: QUARTILE ANALYSIS (4 TIERS)
# ============================================================================

print("=" * 80)
print("TEST 1A: QUARTILE SPLIT (4 Tiers by adj_his_par)")
print("=" * 80)
print()

df_clean = df_orange[df_orange['vs_own_par'].notna()].copy()

# Create quartiles
df_clean['skill_tier'] = pd.qcut(df_clean['adj_his_par'], q=4, labels=['Weakest', 'Weak', 'Elite', 'Elite Top 25%'], duplicates='drop')

print("Skill Tier Ranges (adj_his_par):")
for tier in ['Weakest', 'Weak', 'Elite', 'Elite Top 25%']:
    tier_data = df_clean[df_clean['skill_tier'] == tier]
    if len(tier_data) > 0:
        min_val = tier_data['adj_his_par'].min()
        max_val = tier_data['adj_his_par'].max()
        print(f"  {tier:20} n={len(tier_data):4} | adj_his_par range: {min_val:6.2f} to {max_val:6.2f}")

print()
print("Performance by Tier (vs_own_par):")
print()

tier_results = []
for tier in ['Weakest', 'Weak', 'Elite', 'Elite Top 25%']:
    tier_data = df_clean[df_clean['skill_tier'] == tier]['vs_own_par']

    if len(tier_data) == 0:
        continue

    mean_vs_own = tier_data.mean()
    std_vs_own = tier_data.std()
    median_vs_own = tier_data.median()
    beat_own_pct = 100 * (tier_data < 0).sum() / len(tier_data)

    result = {
        'tier': tier,
        'n': len(tier_data),
        'mean_vs_own_par': round(mean_vs_own, 4),
        'std': round(std_vs_own, 4),
        'median': round(median_vs_own, 4),
        'beat_own_pct': round(beat_own_pct, 1),
    }
    tier_results.append(result)

    print(f"{tier:20} n={len(tier_data):4} | mean={mean_vs_own:+6.4f} | "
          f"std={std_vs_own:6.4f} | beat_own={beat_own_pct:5.1f}%")

print()

# Check for monotonic trend
underperformance = [r['mean_vs_own_par'] for r in tier_results]
print("Underperformance trend (should increase from Weakest to Elite):")
for i, (tier, val) in enumerate(zip([r['tier'] for r in tier_results], underperformance)):
    print(f"  {tier:20} {val:+6.4f}")

is_monotonic = all(underperformance[i] <= underperformance[i+1] for i in range(len(underperformance)-1))
print(f"\nMonotonic increase? {is_monotonic}")
print()

# Calculate effect size (elite vs weak)
elite_data = df_clean[df_clean['skill_tier'] == 'Elite Top 25%']['vs_own_par']
weak_data = df_clean[df_clean['skill_tier'] == 'Weakest']['vs_own_par']

if len(elite_data) > 0 and len(weak_data) > 0:
    elite_mean = elite_data.mean()
    weak_mean = weak_data.mean()
    effect_size = elite_mean - weak_mean

    # T-test
    t_stat, p_val = stats.ttest_ind(elite_data, weak_data)

    print(f"Effect Size (Elite Top 25% vs Weakest):")
    print(f"  Elite mean: {elite_mean:+6.4f}")
    print(f"  Weak mean: {weak_mean:+6.4f}")
    print(f"  Difference: {effect_size:+6.4f} strokes")
    print(f"  t-statistic: {t_stat:7.4f}")
    print(f"  p-value: {p_val:.6f}")
    print(f"  Pass (p<0.05, |effect|>0.15)? {p_val < 0.05 and abs(effect_size) > 0.15}")

print()

# ============================================================================
# TEST 1B: DECILE ANALYSIS (10 TIERS)
# ============================================================================

print("=" * 80)
print("TEST 1B: DECILE SPLIT (10 Tiers by adj_his_par)")
print("=" * 80)
print()

df_clean['skill_decile'] = pd.qcut(df_clean['adj_his_par'], q=10, labels=False, duplicates='drop')

print("Performance by Decile (vs_own_par):")
print()
print("Decile | n      | adj_his_par range   | mean_vs_own | std     | beat_own%")
print("-------|--------|---------------------|-------------|---------|----------")

decile_results = []
for decile in sorted(df_clean['skill_decile'].unique()):
    decile_data = df_clean[df_clean['skill_decile'] == decile]
    vs_own = decile_data['vs_own_par']

    if len(vs_own) == 0:
        continue

    min_adj = decile_data['adj_his_par'].min()
    max_adj = decile_data['adj_his_par'].max()
    mean_vs_own = vs_own.mean()
    std_vs_own = vs_own.std()
    beat_own_pct = 100 * (vs_own < 0).sum() / len(vs_own)

    decile_results.append({
        'decile': decile,
        'n': len(vs_own),
        'adj_his_par_min': min_adj,
        'adj_his_par_max': max_adj,
        'mean_vs_own_par': mean_vs_own,
        'std': std_vs_own,
        'beat_own_pct': beat_own_pct,
    })

    label = f"D{decile+1}"
    print(f"{label:6} | {len(vs_own):6} | {min_adj:6.2f} to {max_adj:6.2f}  | "
          f"{mean_vs_own:+9.4f} | {std_vs_own:7.4f} | {beat_own_pct:7.1f}%")

print()

# Check monotonic trend for deciles
decile_underperformance = [r['mean_vs_own_par'] for r in decile_results]
is_decile_monotonic = all(decile_underperformance[i] <= decile_underperformance[i+1]
                          for i in range(len(decile_underperformance)-1))
print(f"Monotonic trend across deciles? {is_decile_monotonic}")
print()

# ============================================================================
# CONDITION BREAKDOWN
# ============================================================================

print("=" * 80)
print("CONDITION BREAKDOWN")
print("=" * 80)
print()

for condition in ['Calm', 'Moderate', 'Tough']:
    df_cond = df_clean[df_clean['condition'] == condition]

    if len(df_cond) == 0:
        continue

    print(f"{condition}:")
    print(f"  n={len(df_cond)}")

    # Quartile split
    if len(df_cond) >= 4:
        try:
            df_cond_split = df_cond.copy()
            df_cond_split['skill_tier'] = pd.qcut(df_cond_split['adj_his_par'], q=4,
                                                   labels=['Weakest', 'Weak', 'Elite', 'Elite Top 25%'],
                                                   duplicates='drop')

            for tier in ['Weakest', 'Elite Top 25%']:
                tier_data = df_cond_split[df_cond_split['skill_tier'] == tier]['vs_own_par']
                if len(tier_data) > 0:
                    mean_vs = tier_data.mean()
                    beat_own = 100 * (tier_data < 0).sum() / len(tier_data)
                    print(f"    {tier:20} n={len(tier_data):3} | mean={mean_vs:+7.4f} | beat_own={beat_own:5.1f}%")

            # Effect size for this condition
            elite = df_cond_split[df_cond_split['skill_tier'] == 'Elite Top 25%']['vs_own_par']
            weak = df_cond_split[df_cond_split['skill_tier'] == 'Weakest']['vs_own_par']

            if len(elite) > 0 and len(weak) > 0:
                effect = elite.mean() - weak.mean()
                t_stat, p_val = stats.ttest_ind(elite, weak)
                print(f"    Effect size: {effect:+7.4f} (p={p_val:.4f})")
        except:
            print(f"    [Insufficient sample for stratification]")

    print()

# ============================================================================
# REGRESSION: SKILL LEVEL PREDICTS UNDERPERFORMANCE?
# ============================================================================

print("=" * 80)
print("REGRESSION: DOES adj_his_par PREDICT vs_own_par?")
print("=" * 80)
print()

from scipy.stats import linregress

slope, intercept, r_value, p_value, std_err = linregress(df_clean['adj_his_par'], df_clean['vs_own_par'])

print(f"Linear regression: vs_own_par ~ adj_his_par")
print(f"  Slope: {slope:+8.4f} (each stroke worse in adj_his_par -> worse in vs_own_par)")
print(f"  Intercept: {intercept:+8.4f}")
print(f"  R-squared: {r_value**2:7.4f}")
print(f"  p-value: {p_value:.6f}")
print(f"  Interpretation: {'Elite players systematically underperform' if slope > 0 else 'No clear pattern'}")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("TIER 1 VALIDATION SUMMARY")
print("=" * 80)
print()

# Pass criteria
pass_monotonic = is_monotonic
pass_effect_size = abs(effect_size) > 0.15 if len(elite_data) > 0 and len(weak_data) > 0 else False
pass_p_value = p_val < 0.05 if len(elite_data) > 0 and len(weak_data) > 0 else False

print(f"Test 1A (Quartile) Results:")
print(f"  Monotonic increase (weakest to elite)? {pass_monotonic}")
print(f"  Effect size > 0.15 strokes? {pass_effect_size} (actual: {abs(effect_size):+.4f})")
print(f"  p-value < 0.05? {pass_p_value} (actual: {p_val:.6f})")
print()

test_1a_pass = pass_monotonic and pass_effect_size and pass_p_value
print(f"TEST 1A RESULT: {'HELD' if test_1a_pass else 'WEAKENED or REVERSED'}")
print()

print(f"Test 1B (Decile) Results:")
print(f"  Monotonic across 10 deciles? {is_decile_monotonic}")
print(f"  Interpretation: {'Clean talent gradient' if is_decile_monotonic else 'Noisy or reversed in some tiers'}")
print()

print(f"Overall Pattern (2025/2026):")
if test_1a_pass:
    print(f"  [VALIDATED] Talent equalizer pattern holds in recent data")
    print(f"  Elite underperform own par by {elite_mean:+.4f} strokes (vs {elite_mean:+.4f} historical)")
    print(f"  Weak underperform own par by {weak_mean:+.4f} strokes (vs {weak_mean:+.4f} historical)")
else:
    print(f"  [WEAKENED/REVERSED] Pattern does not hold robustly in 2025/2026")
    print(f"  This suggests the 2022-2024 finding may be condition-specific or sample-dependent")

print()
print("=" * 80)
