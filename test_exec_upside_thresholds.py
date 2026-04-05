import pandas as pd
import numpy as np
from scipy import stats
import json

# ============================================================================
# Load data
# ============================================================================

df = pd.read_csv("d:/Projects/luckify-me/DATA/Golf Historics v3 - ANALYSIS (8).csv", low_memory=False)

print("=" * 140)
print("EXEC & UPSIDE SCORE THRESHOLDS AND PERFORMANCE (8 Alternative Approaches)")
print("=" * 140)
print(f"\nDataset: {len(df)} rows\n")

# Apply filters
df = df[df['tournament_type'].isin(['S', 'NS'])]
df = df[df['condition'].isin(['Calm', 'Moderate', 'Tough'])]
df = df[df['vs_avg'].notna()]
df = df[df['color'].notna()]
df = df[df['exec'].notna()]
df = df[df['upside'].notna()]
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['exec'] = pd.to_numeric(df['exec'], errors='coerce')
df['upside'] = pd.to_numeric(df['upside'], errors='coerce')
df = df[df['vs_avg'].notna() & df['exec'].notna() & df['upside'].notna()]

print(f"After filtering: {len(df)} rows\n")

# Create bucket definitions
def create_bucket(value, name):
    if value < 25:
        return f"{name}_0-25"
    elif value < 50:
        return f"{name}_25-50"
    elif value < 75:
        return f"{name}_50-75"
    else:
        return f"{name}_75-100"

df['upside_bucket'] = df['upside'].apply(lambda x: create_bucket(x, 'Upside'))
df['exec_bucket'] = df['exec'].apply(lambda x: create_bucket(x, 'Exec'))

# Pre-compute unique values
colors = sorted([c for c in df['color'].unique() if pd.notna(c)])
elements = sorted([e for e in df['wu_xing'].unique() if pd.notna(e)])
years = sorted(df['year'].unique())
upside_buckets = sorted(df['upside_bucket'].unique())
exec_buckets = sorted(df['exec_bucket'].unique())

print(f"Colors found: {colors}")
print(f"Elements found: {elements}")
print(f"Upside buckets: {upside_buckets}")
print(f"Exec buckets: {exec_buckets}\n")

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
# ANALYSIS 1: UPSIDE BUCKET BREAKDOWN (By Condition)
# ============================================================================

print("=" * 140)
print("ANALYSIS 1: UPSIDE BUCKET BREAKDOWN (Performance ladder by condition)")
print("=" * 140)
print()

results_cond = []
baseline_all = df['vs_avg']

for condition in ['Calm', 'Moderate', 'Tough']:
    print(f"\n{condition}:")
    cond_data = df[df['condition'] == condition]
    baseline_cond = cond_data['vs_avg']

    for bucket in upside_buckets:
        bucket_data = cond_data[cond_data['upside_bucket'] == bucket]['vs_avg']

        if len(bucket_data) < 5:
            print(f"  {bucket}: n={len(bucket_data)} (TOO SMALL)")
            continue

        mean_bucket = np.mean(bucket_data)
        mean_baseline = np.mean(baseline_cond)
        diff = mean_bucket - mean_baseline
        std_bucket = np.std(bucket_data, ddof=1)
        wr = (bucket_data > 0).sum() / len(bucket_data) * 100

        t_stat, p_val = stats.ttest_ind(bucket_data, baseline_cond)
        d = cohen_d(bucket_data, baseline_cond)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
        print(f"  {bucket}: n={len(bucket_data)}, mean={mean_bucket:+.3f}±{std_bucket:.3f}, diff={direction}{diff:+.3f}, WR={wr:.1f}%, p={p_val:.4f} {sig}")

        results_cond.append({
            'condition': condition,
            'upside_bucket': bucket,
            'n': len(bucket_data),
            'mean_vs_avg': mean_bucket,
            'std': std_bucket,
            'win_rate': wr,
            'baseline_mean': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_cond).to_csv("analysis1_upside_bucket_condition.csv", index=False)
print("\n[OK] Saved: analysis1_upside_bucket_condition.csv\n")

# ============================================================================
# ANALYSIS 2: EXEC BUCKET BREAKDOWN (By Condition)
# ============================================================================

print("=" * 140)
print("ANALYSIS 2: EXEC BUCKET BREAKDOWN (Performance ladder by condition)")
print("=" * 140)
print()

results_exec = []

for condition in ['Calm', 'Moderate', 'Tough']:
    print(f"\n{condition}:")
    cond_data = df[df['condition'] == condition]
    baseline_cond = cond_data['vs_avg']

    for bucket in exec_buckets:
        bucket_data = cond_data[cond_data['exec_bucket'] == bucket]['vs_avg']

        if len(bucket_data) < 5:
            print(f"  {bucket}: n={len(bucket_data)} (TOO SMALL)")
            continue

        mean_bucket = np.mean(bucket_data)
        mean_baseline = np.mean(baseline_cond)
        diff = mean_bucket - mean_baseline
        std_bucket = np.std(bucket_data, ddof=1)
        wr = (bucket_data > 0).sum() / len(bucket_data) * 100

        t_stat, p_val = stats.ttest_ind(bucket_data, baseline_cond)
        d = cohen_d(bucket_data, baseline_cond)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
        print(f"  {bucket}: n={len(bucket_data)}, mean={mean_bucket:+.3f}±{std_bucket:.3f}, diff={direction}{diff:+.3f}, WR={wr:.1f}%, p={p_val:.4f} {sig}")

        results_exec.append({
            'condition': condition,
            'exec_bucket': bucket,
            'n': len(bucket_data),
            'mean_vs_avg': mean_bucket,
            'std': std_bucket,
            'win_rate': wr,
            'baseline_mean': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_exec).to_csv("analysis2_exec_bucket_condition.csv", index=False)
print("\n[OK] Saved: analysis2_exec_bucket_condition.csv\n")

# ============================================================================
# ANALYSIS 3: 3-WAY INTERACTION (Color × Upside Bucket × Condition)
# ============================================================================

print("=" * 140)
print("ANALYSIS 3: 3-WAY INTERACTION (Color × Upside × Condition)")
print("=" * 140)
print()

results_3way = []

for color in colors:
    color_data = df[df['color'] == color]
    if len(color_data) < 5:
        continue

    print(f"\n{color}:")

    for bucket in upside_buckets:
        bucket_color = color_data[color_data['upside_bucket'] == bucket]
        if len(bucket_color) < 5:
            continue

        for condition in ['Calm', 'Moderate', 'Tough']:
            combo_data = bucket_color[bucket_color['condition'] == condition]['vs_avg']
            baseline_combo = color_data[(color_data['condition'] == condition)]['vs_avg']

            if len(combo_data) < 5 or len(baseline_combo) < 5:
                continue

            mean_combo = np.mean(combo_data)
            mean_base = np.mean(baseline_combo)
            diff = mean_combo - mean_base
            std_combo = np.std(combo_data, ddof=1)
            wr = (combo_data > 0).sum() / len(combo_data) * 100

            t_stat, p_val = stats.ttest_ind(combo_data, baseline_combo)
            d = cohen_d(combo_data, baseline_combo)

            direction = "+" if diff > 0 else ""
            sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
            print(f"  {bucket}×{condition}: n={len(combo_data)}, mean={mean_combo:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

            results_3way.append({
                'color': color,
                'upside_bucket': bucket,
                'condition': condition,
                'n': len(combo_data),
                'mean_vs_avg': mean_combo,
                'std': std_combo,
                'win_rate': wr,
                'baseline_mean': mean_base,
                'difference': diff,
                'p_value': p_val,
                'cohens_d': d,
            })

pd.DataFrame(results_3way).to_csv("analysis3_upside_3way_interaction.csv", index=False)
print("\n[OK] Saved: analysis3_upside_3way_interaction.csv\n")

# ============================================================================
# ANALYSIS 4: VARIANCE/STABILITY (Consistency by bucket)
# ============================================================================

print("=" * 140)
print("ANALYSIS 4: VARIANCE/STABILITY (Upside bucket consistency)")
print("=" * 140)
print()

results_var = []

for bucket in upside_buckets:
    bucket_data = df[df['upside_bucket'] == bucket]['vs_avg']
    if len(bucket_data) >= 5:
        results_var.append({
            'upside_bucket': bucket,
            'n': len(bucket_data),
            'mean': np.mean(bucket_data),
            'std': np.std(bucket_data, ddof=1),
        })

var_df = pd.DataFrame(results_var).sort_values('std')
print("Upside buckets ranked by consistency (lowest variance):")
print(var_df.to_string(index=False))
print()

var_df.to_csv("analysis4_upside_variance_stability.csv", index=False)
print("[OK] Saved: analysis4_upside_variance_stability.csv\n")

# ============================================================================
# ANALYSIS 5: ELEMENT LENS (Wu Xing × Upside Bucket)
# ============================================================================

print("=" * 140)
print("ANALYSIS 5: ELEMENT LENS (Wu Xing × Upside)")
print("=" * 140)
print()

results_elem = []

for bucket in upside_buckets:
    print(f"\n{bucket}:")
    bucket_data = df[df['upside_bucket'] == bucket]
    baseline_all_data = df['vs_avg']

    for element in elements:
        elem_bucket = bucket_data[bucket_data['wu_xing'] == element]['vs_avg']

        if len(elem_bucket) < 5:
            continue

        mean_elem = np.mean(elem_bucket)
        mean_base = np.mean(baseline_all_data)
        diff = mean_elem - mean_base
        std_elem = np.std(elem_bucket, ddof=1)

        t_stat, p_val = stats.ttest_ind(elem_bucket, baseline_all_data)
        d = cohen_d(elem_bucket, baseline_all_data)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
        print(f"  {element}: n={len(elem_bucket)}, mean={mean_elem:+.3f}, diff={direction}{diff:+.3f}, p={p_val:.4f} {sig}")

        results_elem.append({
            'upside_bucket': bucket,
            'element': element,
            'n': len(elem_bucket),
            'mean_vs_avg': mean_elem,
            'std': std_elem,
            'baseline_mean': mean_base,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_elem).to_csv("analysis5_upside_element_lens.csv", index=False)
print("\n[OK] Saved: analysis5_upside_element_lens.csv\n")

# ============================================================================
# ANALYSIS 6: ROUND PROGRESSION (Upside effect by round)
# ============================================================================

print("=" * 140)
print("ANALYSIS 6: ROUND PROGRESSION (Upside buckets by round)")
print("=" * 140)
print()

results_round = []

for bucket in upside_buckets:
    print(f"\n{bucket}:")
    bucket_data = df[df['upside_bucket'] == bucket]

    for round_num in [1, 2, 3, 4]:
        round_data = bucket_data[bucket_data['round_num'] == round_num]['vs_avg']
        baseline_round = df[df['round_num'] == round_num]['vs_avg']

        if len(round_data) < 5 or len(baseline_round) < 5:
            print(f"  R{round_num}: n={len(round_data)} (too small)")
            continue

        mean_bucket = np.mean(round_data)
        mean_baseline = np.mean(baseline_round)
        diff = mean_bucket - mean_baseline
        std_bucket = np.std(round_data, ddof=1)
        wr = (round_data > 0).sum() / len(round_data) * 100

        t_stat, p_val = stats.ttest_ind(round_data, baseline_round)
        d = cohen_d(round_data, baseline_round)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
        print(f"  R{round_num}: n={len(round_data)}, mean={mean_bucket:+.3f}, diff={direction}{diff:+.3f}, WR={wr:.1f}%, p={p_val:.4f} {sig}")

        results_round.append({
            'upside_bucket': bucket,
            'round_num': round_num,
            'n': len(round_data),
            'mean_vs_avg': mean_bucket,
            'std': std_bucket,
            'win_rate': wr,
            'baseline_mean': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_round).to_csv("analysis6_upside_round_progression.csv", index=False)
print("\n[OK] Saved: analysis6_upside_round_progression.csv\n")

# ============================================================================
# ANALYSIS 7: TIME TREND (Upside effect by year)
# ============================================================================

print("=" * 140)
print("ANALYSIS 7: TIME TREND (Upside buckets by year)")
print("=" * 140)
print()

results_year = []

for bucket in upside_buckets:
    print(f"\n{bucket}:")
    bucket_data = df[df['upside_bucket'] == bucket]

    for year in years:
        year_bucket = bucket_data[bucket_data['year'] == year]['vs_avg']
        baseline_year = df[df['year'] == year]['vs_avg']

        if len(year_bucket) < 5 or len(baseline_year) < 5:
            print(f"  {year}: n={len(year_bucket)} (too small)")
            continue

        mean_bucket = np.mean(year_bucket)
        mean_baseline = np.mean(baseline_year)
        diff = mean_bucket - mean_baseline
        std_bucket = np.std(year_bucket, ddof=1)
        wr = (year_bucket > 0).sum() / len(year_bucket) * 100

        t_stat, p_val = stats.ttest_ind(year_bucket, baseline_year)
        d = cohen_d(year_bucket, baseline_year)

        direction = "+" if diff > 0 else ""
        sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
        print(f"  {year}: n={len(year_bucket)}, mean={mean_bucket:+.3f}, diff={direction}{diff:+.3f}, WR={wr:.1f}%, p={p_val:.4f} {sig}")

        results_year.append({
            'upside_bucket': bucket,
            'year': year,
            'n': len(year_bucket),
            'mean_vs_avg': mean_bucket,
            'std': std_bucket,
            'win_rate': wr,
            'baseline_mean': mean_baseline,
            'difference': diff,
            'p_value': p_val,
            'cohens_d': d,
        })

pd.DataFrame(results_year).to_csv("analysis7_upside_time_trend.csv", index=False)
print("\n[OK] Saved: analysis7_upside_time_trend.csv\n")

# ============================================================================
# ANALYSIS 8: UPSIDE × EXEC SYNERGY
# ============================================================================

print("=" * 140)
print("ANALYSIS 8: UPSIDE × EXEC SYNERGY (High on both)")
print("=" * 140)
print()

results_synergy = []

# High Upside (75-100) + High Exec (75-100)
high_both = df[(df['upside_bucket'] == 'Upside_75-100') & (df['exec_bucket'] == 'Exec_75-100')]['vs_avg']
high_upside_only = df[(df['upside_bucket'] == 'Upside_75-100') & (df['exec_bucket'] != 'Exec_75-100')]['vs_avg']
high_exec_only = df[(df['upside_bucket'] != 'Upside_75-100') & (df['exec_bucket'] == 'Exec_75-100')]['vs_avg']
baseline_low = df[(df['upside_bucket'] == 'Upside_0-25') & (df['exec_bucket'] == 'Exec_0-25')]['vs_avg']

for group_name, group_data in [
    ('High_Upside_75-100', high_upside_only),
    ('High_Exec_75-100', high_exec_only),
    ('High_Both_75-100', high_both),
]:
    if len(group_data) < 5:
        print(f"{group_name}: n={len(group_data)} (too small)")
        continue

    if len(baseline_low) < 5:
        continue

    mean_group = np.mean(group_data)
    mean_base = np.mean(baseline_low)
    diff = mean_group - mean_base
    std_group = np.std(group_data, ddof=1)
    wr = (group_data > 0).sum() / len(group_data) * 100

    t_stat, p_val = stats.ttest_ind(group_data, baseline_low)
    d = cohen_d(group_data, baseline_low)

    direction = "+" if diff > 0 else ""
    sig = "PASS" if (p_val < 0.05 and diff > 0) else ""
    print(f"{group_name}: n={len(group_data)}, mean={mean_group:+.3f}, diff={direction}{diff:+.3f}, WR={wr:.1f}%, p={p_val:.4f} {sig}")

    results_synergy.append({
        'group': group_name,
        'n': len(group_data),
        'mean_vs_avg': mean_group,
        'std': std_group,
        'win_rate': wr,
        'baseline_mean': mean_base,
        'difference': diff,
        'p_value': p_val,
        'cohens_d': d,
    })

pd.DataFrame(results_synergy).to_csv("analysis8_upside_exec_synergy.csv", index=False)
print("\n[OK] Saved: analysis8_upside_exec_synergy.csv\n")

# ============================================================================
# Correlation Analysis
# ============================================================================

print("=" * 140)
print("CORRELATION ANALYSIS (Upside/Exec vs Performance)")
print("=" * 140)
print()

for condition in ['Calm', 'Moderate', 'Tough', 'All']:
    if condition == 'All':
        cond_data = df
    else:
        cond_data = df[df['condition'] == condition]

    r_upside, p_upside = stats.pearsonr(cond_data['upside'], cond_data['vs_avg'])
    r_exec, p_exec = stats.pearsonr(cond_data['exec'], cond_data['vs_avg'])

    print(f"\n{condition}:")
    print(f"  Upside correlation: r={r_upside:+.4f}, p={p_upside:.4f}")
    print(f"  Exec correlation:   r={r_exec:+.4f}, p={p_exec:.4f}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 140)
print("ALL 8 ANALYSES COMPLETE")
print("=" * 140)
print("""
Results saved:
  1. analysis1_upside_bucket_condition.csv
  2. analysis2_exec_bucket_condition.csv
  3. analysis3_upside_3way_interaction.csv
  4. analysis4_upside_variance_stability.csv
  5. analysis5_upside_element_lens.csv
  6. analysis6_upside_round_progression.csv
  7. analysis7_upside_time_trend.csv
  8. analysis8_upside_exec_synergy.csv

Key focus: PERFORMANCE LADDER
Expected: Higher bucket = better performance (positive difference)
Expected: Upside 75-100 should outperform Upside 0-25 significantly

Ready for interpretation.
""")
