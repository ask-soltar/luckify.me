import pandas as pd
import numpy as np
from scipy import stats
import json

# ============================================================================
# Load data
# ============================================================================

df = pd.read_csv("d:/Projects/luckify-me/DATA/Golf Historics v3 - ANALYSIS (8).csv", low_memory=False)

print("=" * 140)
print("MASTER NUMBERS - DEEP PATTERN ANALYSIS (8 Alternative Approaches)")
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

# ============================================================================
# Pre-compute unique values for analysis
# ============================================================================

colors = sorted([c for c in df['color'].unique() if pd.notna(c)])
elements = sorted([e for e in df['wu_xing'].unique() if pd.notna(e)])

print(f"Colors found: {colors}")
print(f"Elements found: {elements}\n")

# ============================================================================
# Helper functions
# ============================================================================

def cohen_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# ============================================================================
# ANALYSIS 1: CONDITION BREAKDOWN (PD 22 by Calm/Moderate/Tough)
# ============================================================================

print("=" * 140)
print("ANALYSIS 1: CONDITION BREAKDOWN (Is PD 22 effect Calm-specific? Tough-specific?)")
print("=" * 140)
print()

results_cond = []

for condition in ['Calm', 'Moderate', 'Tough']:
    cond_data = df[df['condition'] == condition]
    pd22_data = cond_data[cond_data['Personal Day'] == 22]['vs_avg']
    baseline_data = cond_data[~cond_data['Personal Day'].isin([11, 22, 33])]['vs_avg']

    if len(pd22_data) < 5 or len(baseline_data) < 5:
        print(f"{condition}: n_pd22={len(pd22_data)}, n_baseline={len(baseline_data)} (TOO SMALL)")
        continue

    mean_pd22 = np.mean(pd22_data)
    mean_baseline = np.mean(baseline_data)
    diff = mean_pd22 - mean_baseline
    std_pd22 = np.std(pd22_data, ddof=1)
    std_baseline = np.std(baseline_data, ddof=1)

    t_stat, p_val = stats.ttest_ind(pd22_data, baseline_data)
    d = cohen_d(pd22_data, baseline_data)

    sig = "PASS" if p_val < 0.10 else "FAIL"
    print(f"{condition}: n={len(pd22_data)}, mean={mean_pd22:+.3f}±{std_pd22:.3f} vs {mean_baseline:+.3f}±{std_baseline:.3f}, diff={diff:+.3f}, p={p_val:.4f} {sig}")

    results_cond.append({
        'condition': condition,
        'n_pd22': len(pd22_data),
        'n_baseline': len(baseline_data),
        'mean_pd22': mean_pd22,
        'std_pd22': std_pd22,
        'mean_baseline': mean_baseline,
        'std_baseline': std_baseline,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

pd.DataFrame(results_cond).to_csv("analysis1_condition_breakdown.csv", index=False)
print("\n[OK] Saved: analysis1_condition_breakdown.csv\n")

# ============================================================================
# ANALYSIS 2: 3-WAY INTERACTION (Color × Master × Condition)
# ============================================================================

print("=" * 140)
print("ANALYSIS 2: 3-WAY INTERACTION (Color × Master × Condition)")
print("=" * 140)
print()

results_3way = []

for color in colors:
    color_df = df[df['color'] == color]
    color_baseline = color_df[~color_df['Personal Day'].isin([11, 22, 33])]['vs_avg']

    if len(color_baseline) < 5:
        continue

    print(f"\n{color}:")

    for master_num in [11, 22, 33]:
        for condition in ['Calm', 'Moderate', 'Tough']:
            combo_data = color_df[(color_df['Personal Day'] == master_num) & (color_df['condition'] == condition)]['vs_avg']

            if len(combo_data) < 5:
                continue

            color_cond_baseline = color_df[~color_df['Personal Day'].isin([11, 22, 33]) & (color_df['condition'] == condition)]['vs_avg']
            if len(color_cond_baseline) < 5:
                continue

            mean_combo = np.mean(combo_data)
            mean_base = np.mean(color_cond_baseline)
            diff = mean_combo - mean_base
            std_combo = np.std(combo_data, ddof=1)

            t_stat, p_val = stats.ttest_ind(combo_data, color_cond_baseline)
            d = cohen_d(combo_data, color_cond_baseline)

            sig = "PASS" if p_val < 0.10 else ""
            print(f"  PD{master_num}×{condition}: n={len(combo_data)}, mean={mean_combo:+.3f}±{std_combo:.3f}, p={p_val:.4f} {sig}")

            results_3way.append({
                'color': color,
                'master_num': master_num,
                'condition': condition,
                'n': len(combo_data),
                'mean_vs_avg': mean_combo,
                'std': std_combo,
                'baseline_mean': mean_base,
                'difference': diff,
                'p_value': p_val,
                'cohens_d': d,
            })

pd.DataFrame(results_3way).to_csv("analysis2_3way_interaction.csv", index=False)
print("\n[OK] Saved: analysis2_3way_interaction.csv\n")

# ============================================================================
# ANALYSIS 3: VARIANCE/STABILITY (Rank combos by lowest variance)
# ============================================================================

print("=" * 140)
print("ANALYSIS 3: VARIANCE/STABILITY (Which combos are most consistent?)")
print("=" * 140)
print()

results_var = []

for color in colors:
    color_df = df[df['color'] == color]
    for master_num in [11, 22, 33]:
        combo_data = color_df[color_df['Personal Day'] == master_num]['vs_avg']
        if len(combo_data) >= 5:
            results_var.append({
                'color': color,
                'master_num': master_num,
                'n': len(combo_data),
                'mean': np.mean(combo_data),
                'std': np.std(combo_data, ddof=1),
                'cv': np.std(combo_data, ddof=1) / abs(np.mean(combo_data)) if np.mean(combo_data) != 0 else np.inf,
            })

var_df = pd.DataFrame(results_var).sort_values('std')
print("Top 10 most consistent (lowest variance):")
print(var_df.head(10).to_string(index=False))
print()

var_df.to_csv("analysis3_variance_stability.csv", index=False)
print("[OK] Saved: analysis3_variance_stability.csv\n")

# ============================================================================
# ANALYSIS 4: ELEMENT LENS (Wu Xing × Master Numbers, not color)
# ============================================================================

print("=" * 140)
print("ANALYSIS 4: ELEMENT LENS (Wu Xing × Master Numbers)")
print("=" * 140)
print()

results_elem = []

for element in elements:
    elem_df = df[df['wu_xing'] == element]
    elem_baseline = elem_df[~elem_df['Personal Day'].isin([11, 22, 33])]['vs_avg']

    if len(elem_baseline) < 5:
        continue

    print(f"\n{element}:")

    for master_num in [11, 22, 33]:
        combo_data = elem_df[elem_df['Personal Day'] == master_num]['vs_avg']

        if len(combo_data) < 5:
            print(f"  PD {master_num}: n={len(combo_data)} (too small)")
            continue

        mean_combo = np.mean(combo_data)
        mean_base = np.mean(elem_baseline)
        diff = mean_combo - mean_base
        std_combo = np.std(combo_data, ddof=1)

        t_stat, p_val = stats.ttest_ind(combo_data, elem_baseline)
        d = cohen_d(combo_data, elem_baseline)

        sig = "PASS" if p_val < 0.10 else ""
        print(f"  PD {master_num}: n={len(combo_data)}, mean={mean_combo:+.3f}±{std_combo:.3f}, p={p_val:.4f} {sig}")

        results_elem.append({
            'element': element,
            'master_num': master_num,
            'n': len(combo_data),
            'mean_vs_avg': mean_combo,
            'std': std_combo,
            'baseline_mean': mean_base,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_elem).to_csv("analysis4_element_lens.csv", index=False)
print("\n[OK] Saved: analysis4_element_lens.csv\n")

# ============================================================================
# ANALYSIS 5: ROUND PROGRESSION (R1/R2/R3/R4 specific)
# ============================================================================

print("=" * 140)
print("ANALYSIS 5: ROUND PROGRESSION (PD 22 by specific round)")
print("=" * 140)
print()

results_round = []

for round_num in [1, 2, 3, 4]:
    round_df = df[df['round_num'] == round_num]
    pd22_data = round_df[round_df['Personal Day'] == 22]['vs_avg']
    baseline_data = round_df[~round_df['Personal Day'].isin([11, 22, 33])]['vs_avg']

    if len(pd22_data) < 5 or len(baseline_data) < 5:
        print(f"R{round_num}: n_pd22={len(pd22_data)}, n_baseline={len(baseline_data)} (too small)")
        continue

    mean_pd22 = np.mean(pd22_data)
    mean_baseline = np.mean(baseline_data)
    diff = mean_pd22 - mean_baseline
    std_pd22 = np.std(pd22_data, ddof=1)

    t_stat, p_val = stats.ttest_ind(pd22_data, baseline_data)
    d = cohen_d(pd22_data, baseline_data)

    sig = "PASS" if p_val < 0.10 else ""
    print(f"R{round_num}: n={len(pd22_data)}, mean={mean_pd22:+.3f}±{std_pd22:.3f}, p={p_val:.4f} {sig}")

    results_round.append({
        'round_num': round_num,
        'n_pd22': len(pd22_data),
        'n_baseline': len(baseline_data),
        'mean_pd22': mean_pd22,
        'std_pd22': std_pd22,
        'mean_baseline': mean_baseline,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

pd.DataFrame(results_round).to_csv("analysis5_round_progression.csv", index=False)
print("\n[OK] Saved: analysis5_round_progression.csv\n")

# ============================================================================
# ANALYSIS 6: TIME TREND (Year-by-year 2022-2026)
# ============================================================================

print("=" * 140)
print("ANALYSIS 6: TIME TREND (PD 22 effect by year)")
print("=" * 140)
print()

results_year = []

for year in sorted(df['year'].unique()):
    year_df = df[df['year'] == year]
    pd22_data = year_df[year_df['Personal Day'] == 22]['vs_avg']
    baseline_data = year_df[~year_df['Personal Day'].isin([11, 22, 33])]['vs_avg']

    if len(pd22_data) < 5 or len(baseline_data) < 5:
        print(f"{year}: n_pd22={len(pd22_data)}, n_baseline={len(baseline_data)} (too small)")
        continue

    mean_pd22 = np.mean(pd22_data)
    mean_baseline = np.mean(baseline_data)
    diff = mean_pd22 - mean_baseline
    std_pd22 = np.std(pd22_data, ddof=1)

    t_stat, p_val = stats.ttest_ind(pd22_data, baseline_data)
    d = cohen_d(pd22_data, baseline_data)

    sig = "PASS" if p_val < 0.10 else ""
    print(f"{year}: n={len(pd22_data)}, mean={mean_pd22:+.3f}±{std_pd22:.3f}, p={p_val:.4f} {sig}")

    results_year.append({
        'year': year,
        'n_pd22': len(pd22_data),
        'n_baseline': len(baseline_data),
        'mean_pd22': mean_pd22,
        'std_pd22': std_pd22,
        'mean_baseline': mean_baseline,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

pd.DataFrame(results_year).to_csv("analysis6_time_trend.csv", index=False)
print("\n[OK] Saved: analysis6_time_trend.csv\n")

# ============================================================================
# ANALYSIS 7: PLAYER CONSISTENCY (Distribution analysis)
# ============================================================================

print("=" * 140)
print("ANALYSIS 7: PLAYER CONSISTENCY (Are a few outliers driving PD 22 effect?)")
print("=" * 140)
print()

pd22_full = df[df['Personal Day'] == 22]['vs_avg']
baseline_full = df[~df['Personal Day'].isin([11, 22, 33])]['vs_avg']

print(f"PD 22 distribution (n={len(pd22_full)}):")
print(f"  Mean: {np.mean(pd22_full):+.3f}")
print(f"  Median: {np.median(pd22_full):+.3f}")
print(f"  Std: {np.std(pd22_full, ddof=1):.3f}")
print(f"  Min: {np.min(pd22_full):+.3f}, Max: {np.max(pd22_full):+.3f}")
print(f"  Q1-Q3: {np.percentile(pd22_full, 25):+.3f} to {np.percentile(pd22_full, 75):+.3f}")
print(f"  Beat field (vs_avg > 0): {(pd22_full > 0).sum()} / {len(pd22_full)} = {(pd22_full > 0).sum() / len(pd22_full) * 100:.1f}%")
print()

print(f"Baseline distribution (n={len(baseline_full)}):")
print(f"  Mean: {np.mean(baseline_full):+.3f}")
print(f"  Median: {np.median(baseline_full):+.3f}")
print(f"  Std: {np.std(baseline_full, ddof=1):.3f}")
print(f"  Min: {np.min(baseline_full):+.3f}, Max: {np.max(baseline_full):+.3f}")
print(f"  Q1-Q3: {np.percentile(baseline_full, 25):+.3f} to {np.percentile(baseline_full, 75):+.3f}")
print(f"  Beat field: {(baseline_full > 0).sum()} / {len(baseline_full)} = {(baseline_full > 0).sum() / len(baseline_full) * 100:.1f}%")
print()

# Bin analysis
pd22_bins = pd.cut(pd22_full, bins=[-np.inf, -2, -1, 0, 1, 2, np.inf], labels=['<-2', '-2 to -1', '-1 to 0', '0 to 1', '1 to 2', '>2'])
baseline_bins = pd.cut(baseline_full, bins=[-np.inf, -2, -1, 0, 1, 2, np.inf], labels=['<-2', '-2 to -1', '-1 to 0', '0 to 1', '1 to 2', '>2'])

print("Distribution by bin:")
print(f"PD 22:\n{pd22_bins.value_counts().sort_index()}\n")
print(f"Baseline:\n{baseline_bins.value_counts().sort_index()}\n")

# Outlier analysis: top/bottom 10 performers
print("Top 10 PD 22 performers (highest vs_avg):")
top_pd22 = df[df['Personal Day'] == 22].nlargest(10, 'vs_avg')[['player_name', 'event_name', 'vs_avg', 'color']]
print(top_pd22.to_string(index=False))
print()

print("Bottom 10 PD 22 performers (lowest vs_avg):")
bottom_pd22 = df[df['Personal Day'] == 22].nsmallest(10, 'vs_avg')[['player_name', 'event_name', 'vs_avg', 'color']]
print(bottom_pd22.to_string(index=False))
print()

results_dist = {
    'pd22_mean': np.mean(pd22_full),
    'pd22_median': np.median(pd22_full),
    'pd22_std': np.std(pd22_full, ddof=1),
    'pd22_beat_field_pct': (pd22_full > 0).sum() / len(pd22_full) * 100,
    'baseline_mean': np.mean(baseline_full),
    'baseline_beat_field_pct': (baseline_full > 0).sum() / len(baseline_full) * 100,
}

with open("analysis7_player_consistency.json", 'w') as f:
    json.dump(results_dist, f, indent=2)

print("[OK] Saved: analysis7_player_consistency.json\n")

# ============================================================================
# ANALYSIS 8: SYNERGY CHECK (Green+Yellow vs others × PD 22)
# ============================================================================

print("=" * 140)
print("ANALYSIS 8: SYNERGY CHECK (Warm Colors: Green+Yellow vs Others × PD 22)")
print("=" * 140)
print()

# Warm colors: Green, Yellow
warm_colors = ['Green', 'Yellow']
cool_colors = [c for c in colors if c not in warm_colors]

results_synergy = []

# Warm × PD 22
warm_pd22 = df[(df['color'].isin(warm_colors)) & (df['Personal Day'] == 22)]['vs_avg']
warm_baseline = df[(df['color'].isin(warm_colors)) & (~df['Personal Day'].isin([11, 22, 33]))]['vs_avg']

if len(warm_pd22) >= 5 and len(warm_baseline) >= 5:
    mean_warm_pd22 = np.mean(warm_pd22)
    mean_warm_base = np.mean(warm_baseline)
    diff = mean_warm_pd22 - mean_warm_base
    std_warm = np.std(warm_pd22, ddof=1)
    t_stat, p_val = stats.ttest_ind(warm_pd22, warm_baseline)
    d = cohen_d(warm_pd22, warm_baseline)

    sig = "PASS" if p_val < 0.10 else ""
    print(f"Warm (Green+Yellow) × PD 22: n={len(warm_pd22)}, mean={mean_warm_pd22:+.3f}±{std_warm:.3f}, p={p_val:.4f} {sig}")

    results_synergy.append({
        'group': 'Warm (Green+Yellow)',
        'n_pd22': len(warm_pd22),
        'n_baseline': len(warm_baseline),
        'mean_pd22': mean_warm_pd22,
        'std_pd22': std_warm,
        'mean_baseline': mean_warm_base,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

# Cool × PD 22
cool_pd22 = df[(df['color'].isin(cool_colors)) & (df['Personal Day'] == 22)]['vs_avg']
cool_baseline = df[(df['color'].isin(cool_colors)) & (~df['Personal Day'].isin([11, 22, 33]))]['vs_avg']

if len(cool_pd22) >= 5 and len(cool_baseline) >= 5:
    mean_cool_pd22 = np.mean(cool_pd22)
    mean_cool_base = np.mean(cool_baseline)
    diff = mean_cool_pd22 - mean_cool_base
    std_cool = np.std(cool_pd22, ddof=1)
    t_stat, p_val = stats.ttest_ind(cool_pd22, cool_baseline)
    d = cohen_d(cool_pd22, cool_baseline)

    sig = "PASS" if p_val < 0.10 else ""
    print(f"Cool (Others) × PD 22: n={len(cool_pd22)}, mean={mean_cool_pd22:+.3f}±{std_cool:.3f}, p={p_val:.4f} {sig}")

    results_synergy.append({
        'group': f'Cool ({len(cool_colors)} others)',
        'n_pd22': len(cool_pd22),
        'n_baseline': len(cool_baseline),
        'mean_pd22': mean_cool_pd22,
        'std_pd22': std_cool,
        'mean_baseline': mean_cool_base,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

pd.DataFrame(results_synergy).to_csv("analysis8_synergy_check.csv", index=False)
print("\n[OK] Saved: analysis8_synergy_check.csv\n")

# ============================================================================
# Summary
# ============================================================================

print("=" * 140)
print("ALL 8 ANALYSES COMPLETE")
print("=" * 140)
print("""
Results saved:
  1. analysis1_condition_breakdown.csv
  2. analysis2_3way_interaction.csv
  3. analysis3_variance_stability.csv
  4. analysis4_element_lens.csv
  5. analysis5_round_progression.csv
  6. analysis6_time_trend.csv
  7. analysis7_player_consistency.json
  8. analysis8_synergy_check.csv

Ready for interpretation.
""")
