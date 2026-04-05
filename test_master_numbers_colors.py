import pandas as pd
import numpy as np
from scipy import stats
import csv

# ============================================================================
# Load ANALYSIS (8) data
# ============================================================================

df = pd.read_csv("d:/Projects/luckify-me/DATA/Golf Historics v3 - ANALYSIS (8).csv")

print("=" * 140)
print("MASTER NUMBERS × COLORS ANALYSIS")
print("=" * 140)
print(f"\nDataset loaded: {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print()

# ============================================================================
# Identify correct column names (ANALYSIS v3 structure)
# ============================================================================

# Standardize column names (remove whitespace, lowercase for matching)
df.columns = df.columns.str.strip()

# Print actual columns to verify
print("First few rows:")
print(df.head(2))
print()

# Map expected columns (flexible naming)
col_color = None
col_pd = None
col_vs_avg = None
col_condition = None
col_round_type = None
col_tournament_type = None

for col in df.columns:
    col_lower = col.lower().strip()
    if col_lower == 'color':
        col_color = col
    if 'personal day' in col_lower or col_lower == 'pd':
        col_pd = col
    if col_lower == 'vs_avg':
        col_vs_avg = col
    if col_lower == 'condition':
        col_condition = col
    if col_lower == 'round_type' or col_lower == 'round type':
        col_round_type = col
    if col_lower == 'tournament_type' or col_lower == 'tournament type':
        col_tournament_type = col

print(f"Identified columns:")
print(f"  Color: {col_color}")
print(f"  Personal Day: {col_pd}")
print(f"  vs_avg: {col_vs_avg}")
print(f"  Condition: {col_condition}")
print(f"  Round Type: {col_round_type}")
print(f"  Tournament Type: {col_tournament_type}")
print()

if not all([col_color, col_pd, col_vs_avg, col_condition, col_round_type, col_tournament_type]):
    print("ERROR: Could not identify all required columns")
    print("Available columns:", list(df.columns))
    exit(1)

# ============================================================================
# Apply filters
# ============================================================================

print("Applying filters...")
print(f"  Before: {len(df)} rows")

# Tournament type: S or NS
df = df[df[col_tournament_type].isin(['S', 'NS'])]
print(f"  After tournament type filter (S, NS): {len(df)} rows")

# Condition: Calm, Moderate, Tough
df = df[df[col_condition].isin(['Calm', 'Moderate', 'Tough'])]
print(f"  After condition filter (Calm, Moderate, Tough): {len(df)} rows")

# Remove rows with missing vs_avg
df = df[df[col_vs_avg].notna()]
print(f"  After removing null vs_avg: {len(df)} rows")

# Remove rows with missing personal_day or color
df = df[df[col_pd].notna()]
df = df[df[col_color].notna()]
print(f"  After removing null PD/color: {len(df)} rows")

print()

# ============================================================================
# Convert types
# ============================================================================

df[col_vs_avg] = pd.to_numeric(df[col_vs_avg], errors='coerce')
df[col_pd] = pd.to_numeric(df[col_pd], errors='coerce')

# Remove any rows that failed conversion
df = df[df[col_vs_avg].notna() & df[col_pd].notna()]

print(f"After type conversion: {len(df)} rows\n")

# ============================================================================
# Helper functions
# ============================================================================

def cohen_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# ============================================================================
# LEVEL 1: Master Numbers Overall
# ============================================================================

print("=" * 140)
print("LEVEL 1: MASTER NUMBERS OVERALL (All Colors, All Round Types)")
print("=" * 140)
print()

baseline = df[~df[col_pd].isin([11, 22, 33])][col_vs_avg]
results_level1 = []

for master_num in [11, 22, 33]:
    master_data = df[df[col_pd] == master_num][col_vs_avg]

    if len(master_data) < 5:
        print(f"PD {master_num}: n={len(master_data)} (TOO SMALL, skipping)")
        continue

    mean_master = np.mean(master_data)
    mean_baseline = np.mean(baseline)
    diff = mean_master - mean_baseline
    std_master = np.std(master_data, ddof=1)
    std_baseline = np.std(baseline, ddof=1)

    t_stat, p_value = stats.ttest_ind(master_data, baseline)
    d = cohen_d(master_data, baseline)

    results_level1.append({
        'master_num': master_num,
        'n': len(master_data),
        'mean_vs_avg': mean_master,
        'std': std_master,
        'baseline_mean': mean_baseline,
        'baseline_std': std_baseline,
        'difference': diff,
        'p_value': p_value,
        'cohens_d': d,
    })

    significance = "PASS" if p_value < 0.10 else "FAIL"
    print(f"PD {master_num}:")
    print(f"  n={len(master_data)}, mean={mean_master:+.3f}±{std_master:.3f}")
    print(f"  vs Baseline (n={len(baseline)}): {mean_baseline:+.3f}±{std_baseline:.3f}")
    print(f"  Difference: {diff:+.3f}, t={t_stat:.3f}, p={p_value:.4f} {significance}")
    print(f"  Cohen's d: {d:.3f}")
    print()

# ============================================================================
# LEVEL 2: Color × Master Numbers (24 Combinations)
# ============================================================================

print("=" * 140)
print("LEVEL 2: COLOR × MASTER NUMBERS (24 Combinations)")
print("=" * 140)
print()

colors = sorted(df[col_color].unique())
colors = [c for c in colors if pd.notna(c)]  # Remove NaN

results_level2 = []

for color in colors:
    print(f"\n{color}:")
    color_data = df[df[col_color] == color]
    color_baseline = color_data[~color_data[col_pd].isin([11, 22, 33])][col_vs_avg]

    for master_num in [11, 22, 33]:
        combo_data = color_data[color_data[col_pd] == master_num][col_vs_avg]

        if len(combo_data) < 5:
            print(f"  PD {master_num}: n={len(combo_data)} (TOO SMALL)")
            continue

        if len(color_baseline) < 5:
            print(f"  PD {master_num}: baseline too small")
            continue

        mean_combo = np.mean(combo_data)
        mean_baseline_color = np.mean(color_baseline)
        diff = mean_combo - mean_baseline_color
        std_combo = np.std(combo_data, ddof=1)
        std_baseline_color = np.std(color_baseline, ddof=1)

        t_stat, p_value = stats.ttest_ind(combo_data, color_baseline)
        d = cohen_d(combo_data, color_baseline)

        results_level2.append({
            'color': color,
            'master_num': master_num,
            'n': len(combo_data),
            'mean_vs_avg': mean_combo,
            'std': std_combo,
            'baseline_mean': mean_baseline_color,
            'baseline_std': std_baseline_color,
            'difference': diff,
            'p_value': p_value,
            'cohens_d': d,
        })

        significance = "PASS" if p_value < 0.10 else "FAIL"
        print(f"  PD {master_num}: n={len(combo_data)}, mean={mean_combo:+.3f}±{std_combo:.3f}, p={p_value:.4f} {significance}")

print()

# ============================================================================
# LEVEL 3: By Round Type
# ============================================================================

print("=" * 140)
print("LEVEL 3: MASTER NUMBERS BY ROUND TYPE")
print("=" * 140)
print()

round_types = sorted(df[col_round_type].unique())
round_types = [r for r in round_types if pd.notna(r) and r != 'REMOVE']

results_level3 = []

for round_type in round_types:
    print(f"\n{round_type}:")
    rt_data = df[df[col_round_type] == round_type]
    baseline_rt = rt_data[~rt_data[col_pd].isin([11, 22, 33])][col_vs_avg]

    for master_num in [11, 22, 33]:
        combo_data = rt_data[rt_data[col_pd] == master_num][col_vs_avg]

        if len(combo_data) < 5:
            print(f"  PD {master_num}: n={len(combo_data)} (TOO SMALL)")
            continue

        if len(baseline_rt) < 5:
            print(f"  PD {master_num}: baseline too small")
            continue

        mean_combo = np.mean(combo_data)
        mean_baseline_rt = np.mean(baseline_rt)
        diff = mean_combo - mean_baseline_rt
        std_combo = np.std(combo_data, ddof=1)
        std_baseline_rt = np.std(baseline_rt, ddof=1)

        t_stat, p_value = stats.ttest_ind(combo_data, baseline_rt)
        d = cohen_d(combo_data, baseline_rt)

        results_level3.append({
            'round_type': round_type,
            'master_num': master_num,
            'n': len(combo_data),
            'mean_vs_avg': mean_combo,
            'std': std_combo,
            'baseline_mean': mean_baseline_rt,
            'baseline_std': std_baseline_rt,
            'difference': diff,
            'p_value': p_value,
            'cohens_d': d,
        })

        significance = "PASS" if p_value < 0.10 else "FAIL"
        print(f"  PD {master_num}: n={len(combo_data)}, mean={mean_combo:+.3f}±{std_combo:.3f}, p={p_value:.4f} {significance}")

print()

# ============================================================================
# Save Results to CSV
# ============================================================================

print("=" * 140)
print("SAVING RESULTS")
print("=" * 140)
print()

# Level 1
if results_level1:
    df_level1 = pd.DataFrame(results_level1)
    df_level1.to_csv("test_master_numbers_colors_LEVEL1.csv", index=False)
    print("[OK] Saved: test_master_numbers_colors_LEVEL1.csv")

# Level 2
if results_level2:
    df_level2 = pd.DataFrame(results_level2)
    df_level2.to_csv("test_master_numbers_colors_LEVEL2.csv", index=False)
    print("[OK] Saved: test_master_numbers_colors_LEVEL2.csv")

# Level 3
if results_level3:
    df_level3 = pd.DataFrame(results_level3)
    df_level3.to_csv("test_master_numbers_colors_LEVEL3.csv", index=False)
    print("[OK] Saved: test_master_numbers_colors_LEVEL3.csv")

print()
print("=" * 140)
print("Analysis complete.")
print("=" * 140)
