import pandas as pd
import numpy as np
from scipy import stats
import json

# ============================================================================
# Load data
# ============================================================================

df = pd.read_csv("d:/Projects/luckify-me/DATA/Golf Historics v3 - ANALYSIS (8).csv", low_memory=False)

print("=" * 140)
print("PERSONAL NUMBERS 1 & 6 STABILITY ANALYSIS (8 Alternative Approaches)")
print("=" * 140)
print(f"\nDataset: {len(df)} rows\n")

# Apply filters
df = df[df['tournament_type'].isin(['S', 'NS'])]
df = df[df['condition'].isin(['Calm', 'Moderate', 'Tough'])]
df = df[df['vs_avg'].notna()]
df = df[df['Personal Day'].notna()]
df = df[df['color'].notna()]
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['Personal Day'] = pd.to_numeric(df['Personal Day'], errors='coerce')
df = df[df['vs_avg'].notna() & df['Personal Day'].notna()]

print(f"After filtering: {len(df)} rows\n")

# Pre-compute unique values
colors = sorted([c for c in df['color'].unique() if pd.notna(c)])
elements = sorted([e for e in df['wu_xing'].unique() if pd.notna(e)])
years = sorted(df['year'].unique())

print(f"Colors found: {colors}")
print(f"Elements found: {elements}\n")

# ============================================================================
# Helper functions
# ============================================================================

def cohen_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return 0
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# ============================================================================
# ANALYSIS 1: CONDITION BREAKDOWN (PD 1, PD 6 by Calm/Moderate/Tough)
# ============================================================================

print("=" * 140)
print("ANALYSIS 1: CONDITION BREAKDOWN (PD 1 & 6 stability by condition)")
print("=" * 140)
print()

results_cond = []
baseline_all = df[~df['Personal Day'].isin([1, 6])]['vs_avg']

for condition in ['Calm', 'Moderate', 'Tough']:
    cond_data = df[df['condition'] == condition]
    baseline_cond = cond_data[~cond_data['Personal Day'].isin([1, 6])]['vs_avg']

    for pd_num in [1, 6]:
        pd_data = cond_data[cond_data['Personal Day'] == pd_num]['vs_avg']

        if len(pd_data) < 5 or len(baseline_cond) < 5:
            print(f"PD {pd_num} × {condition}: n={len(pd_data)}, n_baseline={len(baseline_cond)} (TOO SMALL)")
            continue

        mean_pd = np.mean(pd_data)
        mean_baseline = np.mean(baseline_cond)
        diff = mean_pd - mean_baseline
        std_pd = np.std(pd_data, ddof=1)
        std_baseline = np.std(baseline_cond, ddof=1)

        t_stat, p_val = stats.ttest_ind(pd_data, baseline_cond)
        d = cohen_d(pd_data, baseline_cond)

        direction = "POSITIVE" if diff > 0 else "NEGATIVE"
        sig = "PASS" if (p_val < 0.10 and diff > 0) else "FAIL"
        print(f"PD {pd_num} × {condition}: n={len(pd_data)}, mean={mean_pd:+.3f}±{std_pd:.3f} vs {mean_baseline:+.3f}, diff={diff:+.3f} ({direction}), p={p_val:.4f} {sig}")

        results_cond.append({
            'pd_num': pd_num,
            'condition': condition,
            'n_pd': len(pd_data),
            'n_baseline': len(baseline_cond),
            'mean_pd': mean_pd,
            'std_pd': std_pd,
            'mean_baseline': mean_baseline,
            'std_baseline': std_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_cond).to_csv("analysis1_pd1_6_condition_breakdown.csv", index=False)
print("\n[OK] Saved: analysis1_pd1_6_condition_breakdown.csv\n")

# ============================================================================
# ANALYSIS 2: 3-WAY INTERACTION (Color × PD × Condition)
# ============================================================================

print("=" * 140)
print("ANALYSIS 2: 3-WAY INTERACTION (Color × PD 1/6 × Condition)")
print("=" * 140)
print()

results_3way = []

for pd_num in [1, 6]:
    print(f"\nPD {pd_num}:")
    pd_full_data = df[df['Personal Day'] == pd_num]

    for color in colors:
        color_pd_data = pd_full_data[pd_full_data['color'] == color]
        if len(color_pd_data) < 5:
            continue

        for condition in ['Calm', 'Moderate', 'Tough']:
            combo_data = color_pd_data[color_pd_data['condition'] == condition]['vs_avg']
            baseline_combo = df[(df['color'] == color) & (~df['Personal Day'].isin([1, 6])) & (df['condition'] == condition)]['vs_avg']

            if len(combo_data) < 5 or len(baseline_combo) < 5:
                continue

            mean_combo = np.mean(combo_data)
            mean_base = np.mean(baseline_combo)
            diff = mean_combo - mean_base
            std_combo = np.std(combo_data, ddof=1)

            t_stat, p_val = stats.ttest_ind(combo_data, baseline_combo)
            d = cohen_d(combo_data, baseline_combo)

            direction = "+" if diff > 0 else ""
            sig = "PASS" if (p_val < 0.10 and diff > 0) else ""
            print(f"  {color}×{condition}: n={len(combo_data)}, mean={mean_combo:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

            results_3way.append({
                'pd_num': pd_num,
                'color': color,
                'condition': condition,
                'n': len(combo_data),
                'mean_pd_color_cond': mean_combo,
                'std': std_combo,
                'baseline_mean': mean_base,
                'difference': diff,
                'p_value': p_val,
                'cohens_d': d,
            })

pd.DataFrame(results_3way).to_csv("analysis2_pd1_6_3way_interaction.csv", index=False)
print("\n[OK] Saved: analysis2_pd1_6_3way_interaction.csv\n")

# ============================================================================
# ANALYSIS 3: VARIANCE/STABILITY
# ============================================================================

print("=" * 140)
print("ANALYSIS 3: VARIANCE/STABILITY (Consistency ranking)")
print("=" * 140)
print()

results_var = []

for pd_num in [1, 6]:
    pd_full = df[df['Personal Day'] == pd_num]
    for color in colors:
        color_pd = pd_full[pd_full['color'] == color]['vs_avg']
        if len(color_pd) >= 5:
            results_var.append({
                'pd_num': pd_num,
                'color': color,
                'n': len(color_pd),
                'mean': np.mean(color_pd),
                'std': np.std(color_pd, ddof=1),
            })

var_df = pd.DataFrame(results_var).sort_values('std')
print("Top 10 most consistent (lowest variance):")
print(var_df.head(10).to_string(index=False))
print()

var_df.to_csv("analysis3_pd1_6_variance_stability.csv", index=False)
print("[OK] Saved: analysis3_pd1_6_variance_stability.csv\n")

# ============================================================================
# ANALYSIS 4: ELEMENT LENS (Wu Xing × PD)
# ============================================================================

print("=" * 140)
print("ANALYSIS 4: ELEMENT LENS (Wu Xing × PD 1/6)")
print("=" * 140)
print()

results_elem = []

for pd_num in [1, 6]:
    print(f"\nPD {pd_num}:")
    pd_full = df[df['Personal Day'] == pd_num]
    pd_baseline = df[~df['Personal Day'].isin([1, 6])]

    for element in elements:
        elem_pd = pd_full[pd_full['wu_xing'] == element]['vs_avg']
        elem_baseline = pd_baseline[pd_baseline['wu_xing'] == element]['vs_avg']

        if len(elem_pd) < 5 or len(elem_baseline) < 5:
            continue

        mean_pd = np.mean(elem_pd)
        mean_base = np.mean(elem_baseline)
        diff = mean_pd - mean_base
        std_pd = np.std(elem_pd, ddof=1)

        t_stat, p_val = stats.ttest_ind(elem_pd, elem_baseline)
        d = cohen_d(elem_pd, elem_baseline)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.10 and diff > 0) else ""
        print(f"  {element}: n={len(elem_pd)}, mean={mean_pd:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

        results_elem.append({
            'pd_num': pd_num,
            'element': element,
            'n': len(elem_pd),
            'mean_pd': mean_pd,
            'std': std_pd,
            'baseline_mean': mean_base,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_elem).to_csv("analysis4_pd1_6_element_lens.csv", index=False)
print("\n[OK] Saved: analysis4_pd1_6_element_lens.csv\n")

# ============================================================================
# ANALYSIS 5: ROUND PROGRESSION
# ============================================================================

print("=" * 140)
print("ANALYSIS 5: ROUND PROGRESSION (PD 1/6 by R1-R4)")
print("=" * 140)
print()

results_round = []

for pd_num in [1, 6]:
    print(f"\nPD {pd_num}:")
    for round_num in [1, 2, 3, 4]:
        round_df = df[df['round_num'] == round_num]
        pd_data = round_df[round_df['Personal Day'] == pd_num]['vs_avg']
        baseline_data = round_df[~round_df['Personal Day'].isin([1, 6])]['vs_avg']

        if len(pd_data) < 5 or len(baseline_data) < 5:
            print(f"  R{round_num}: n={len(pd_data)} (too small)")
            continue

        mean_pd = np.mean(pd_data)
        mean_baseline = np.mean(baseline_data)
        diff = mean_pd - mean_baseline
        std_pd = np.std(pd_data, ddof=1)

        t_stat, p_val = stats.ttest_ind(pd_data, baseline_data)
        d = cohen_d(pd_data, baseline_data)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.10 and diff > 0) else ""
        print(f"  R{round_num}: n={len(pd_data)}, mean={mean_pd:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

        results_round.append({
            'pd_num': pd_num,
            'round_num': round_num,
            'n_pd': len(pd_data),
            'n_baseline': len(baseline_data),
            'mean_pd': mean_pd,
            'std_pd': std_pd,
            'mean_baseline': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_round).to_csv("analysis5_pd1_6_round_progression.csv", index=False)
print("\n[OK] Saved: analysis5_pd1_6_round_progression.csv\n")

# ============================================================================
# ANALYSIS 6: TIME TREND
# ============================================================================

print("=" * 140)
print("ANALYSIS 6: TIME TREND (PD 1/6 by year)")
print("=" * 140)
print()

results_year = []

for pd_num in [1, 6]:
    print(f"\nPD {pd_num}:")
    for year in years:
        year_df = df[df['year'] == year]
        pd_data = year_df[year_df['Personal Day'] == pd_num]['vs_avg']
        baseline_data = year_df[~year_df['Personal Day'].isin([1, 6])]['vs_avg']

        if len(pd_data) < 5 or len(baseline_data) < 5:
            print(f"  {year}: n={len(pd_data)} (too small)")
            continue

        mean_pd = np.mean(pd_data)
        mean_baseline = np.mean(baseline_data)
        diff = mean_pd - mean_baseline
        std_pd = np.std(pd_data, ddof=1)

        t_stat, p_val = stats.ttest_ind(pd_data, baseline_data)
        d = cohen_d(pd_data, baseline_data)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.10 and diff > 0) else ""
        print(f"  {year}: n={len(pd_data)}, mean={mean_pd:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

        results_year.append({
            'pd_num': pd_num,
            'year': year,
            'n_pd': len(pd_data),
            'n_baseline': len(baseline_data),
            'mean_pd': mean_pd,
            'std_pd': std_pd,
            'mean_baseline': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_year).to_csv("analysis6_pd1_6_time_trend.csv", index=False)
print("\n[OK] Saved: analysis6_pd1_6_time_trend.csv\n")

# ============================================================================
# ANALYSIS 7: PLAYER CONSISTENCY
# ============================================================================

print("=" * 140)
print("ANALYSIS 7: PLAYER CONSISTENCY (Distribution analysis)")
print("=" * 140)
print()

for pd_num in [1, 6]:
    pd_full = df[df['Personal Day'] == pd_num]['vs_avg']
    baseline_full = df[~df['Personal Day'].isin([1, 6])]['vs_avg']

    print(f"\nPD {pd_num} (n={len(pd_full)}):")
    print(f"  Mean: {np.mean(pd_full):+.3f} vs baseline {np.mean(baseline_full):+.3f} (diff: {np.mean(pd_full) - np.mean(baseline_full):+.3f})")
    print(f"  Median: {np.median(pd_full):+.3f}")
    print(f"  Std: {np.std(pd_full, ddof=1):.3f}")
    print(f"  Beat field: {(pd_full > 0).sum()} / {len(pd_full)} = {(pd_full > 0).sum() / len(pd_full) * 100:.1f}% (vs baseline {(baseline_full > 0).sum() / len(baseline_full) * 100:.1f}%)")

results_dist = {
    'pd1_mean': float(np.mean(df[df['Personal Day'] == 1]['vs_avg'])),
    'pd1_n': int(len(df[df['Personal Day'] == 1])),
    'pd6_mean': float(np.mean(df[df['Personal Day'] == 6]['vs_avg'])),
    'pd6_n': int(len(df[df['Personal Day'] == 6])),
    'baseline_mean': float(np.mean(df[~df['Personal Day'].isin([1, 6])]['vs_avg'])),
    'baseline_n': int(len(df[~df['Personal Day'].isin([1, 6])])),
}

with open("analysis7_pd1_6_player_consistency.json", 'w') as f:
    json.dump(results_dist, f, indent=2)

print("\n[OK] Saved: analysis7_pd1_6_player_consistency.json\n")

# ============================================================================
# ANALYSIS 8: SYNERGY CHECK (Element combination)
# ============================================================================

print("=" * 140)
print("ANALYSIS 8: SYNERGY CHECK (Best element × PD combo)")
print("=" * 140)
print()

results_synergy = []

for pd_num in [1, 6]:
    for element in elements:
        pd_elem = df[(df['Personal Day'] == pd_num) & (df['wu_xing'] == element)]['vs_avg']
        baseline_elem = df[(~df['Personal Day'].isin([1, 6])) & (df['wu_xing'] == element)]['vs_avg']

        if len(pd_elem) >= 5 and len(baseline_elem) >= 5:
            mean_pd = np.mean(pd_elem)
            mean_base = np.mean(baseline_elem)
            diff = mean_pd - mean_base
            std_pd = np.std(pd_elem, ddof=1)

            t_stat, p_val = stats.ttest_ind(pd_elem, baseline_elem)
            d = cohen_d(pd_elem, baseline_elem)

            direction = "+" if diff > 0 else ""
            sig = "PASS" if (p_val < 0.10 and diff > 0) else ""
            print(f"PD {pd_num} × {element}: n={len(pd_elem)}, mean={mean_pd:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

            results_synergy.append({
                'pd_num': pd_num,
                'element': element,
                'n_pd': len(pd_elem),
                'n_baseline': len(baseline_elem),
                'mean_pd': mean_pd,
                'std_pd': std_pd,
                'mean_baseline': mean_base,
                'difference': diff,
                'p_value': p_val,
                'cohens_d': d,
            })

pd.DataFrame(results_synergy).to_csv("analysis8_pd1_6_synergy_check.csv", index=False)
print("\n[OK] Saved: analysis8_pd1_6_synergy_check.csv\n")

# ============================================================================
# Summary
# ============================================================================

print("=" * 140)
print("ALL 8 ANALYSES COMPLETE")
print("=" * 140)
print("""
Results saved:
  1. analysis1_pd1_6_condition_breakdown.csv
  2. analysis2_pd1_6_3way_interaction.csv
  3. analysis3_pd1_6_variance_stability.csv
  4. analysis4_pd1_6_element_lens.csv
  5. analysis5_pd1_6_round_progression.csv
  6. analysis6_pd1_6_time_trend.csv
  7. analysis7_pd1_6_player_consistency.json
  8. analysis8_pd1_6_synergy_check.csv

Key focus: POSITIVE effect expected (outperformance)
Direction: PD 1/6 should beat baseline (diff > 0)

Ready for interpretation.
""")
