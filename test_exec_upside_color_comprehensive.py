"""
Comprehensive Exec & Upside Analysis by Color (All Dimensions)
Tested 2026-04-04

Analyses:
- Level 1-2: Color × Exec/Upside (2D, isolated)
- Level 3-4: Color × Exec/Upside × Condition (3D)
- Level 5-6: Color × Exec/Upside × Round type (3D)
- Level 7-8: Color × Exec/Upside × Element (3D)
- Level 9-10: 4D combos (Color × Exec/Upside × Condition × Round)
- Level 11-12: Time trend (Color × Exec/Upside by Year)
- Level 13: Correlation analysis (Exec/Upside vs vs_avg by Color)
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading ANALYSIS v3...")
df = pd.read_csv('DATA/ANALYSIS_v3_export.csv')

# Filter: S+NS tournaments only, exclude empty rows
df = df[df['tournament_type'].isin(['S', 'NS'])].copy()
df = df.dropna(subset=['color', 'exec', 'upside', 'vs_avg', 'player_name'])

print(f"Loaded {len(df)} rounds from {df['player_name'].nunique()} players")
print(f"Colors: {sorted(df['color'].unique())}")
print(f"Conditions: {sorted(df['condition'].dropna().unique())}")

# Create buckets if not present
if 'exec_bucket' not in df.columns:
    df['exec_bucket'] = pd.cut(df['exec'], bins=[0, 25, 50, 75, 100],
                                labels=['0-25', '25-50', '50-75', '75-100'], right=False)
if 'upside_bucket' not in df.columns:
    df['upside_bucket'] = pd.cut(df['upside'], bins=[0, 25, 50, 75, 100],
                                  labels=['0-25', '25-50', '50-75', '75-100'], right=False)

# Baseline
baseline_mean = df['vs_avg'].mean()
baseline_beat = (df['vs_avg'] > 0).sum() / len(df)
print(f"\nBaseline: mean={baseline_mean:.4f}, beat_field={baseline_beat:.1%}\n")

# ============================================================================
# LEVEL 1: Color × Exec (all conditions)
# ============================================================================
print("LEVEL 1: Color × Exec (isolated)...")
level1 = df.groupby(['color', 'exec_bucket']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level1.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level1['beat_field'] = df.groupby(['color', 'exec_bucket'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)
level1['vs_baseline_mean'] = (level1['mean_vs_avg'] - baseline_mean).round(4)
level1['vs_baseline_beat'] = (level1['beat_field'] - baseline_beat).round(4)

# T-test vs baseline for each combo
level1['p_value'] = np.nan
for (color, bucket) in level1.index:
    group_data = df[(df['color'] == color) & (df['exec_bucket'] == bucket)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df['vs_avg'])
        level1.loc[(color, bucket), 'p_value'] = p

level1.to_csv('analysis_l1_color_exec_isolated.csv')
print(f"Saved: analysis_l1_color_exec_isolated.csv ({len(level1)} combos)\n")

# ============================================================================
# LEVEL 2: Color × Upside (all conditions)
# ============================================================================
print("LEVEL 2: Color × Upside (isolated)...")
level2 = df.groupby(['color', 'upside_bucket']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level2.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level2['beat_field'] = df.groupby(['color', 'upside_bucket'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)
level2['vs_baseline_mean'] = (level2['mean_vs_avg'] - baseline_mean).round(4)
level2['vs_baseline_beat'] = (level2['beat_field'] - baseline_beat).round(4)

level2['p_value'] = np.nan
for (color, bucket) in level2.index:
    group_data = df[(df['color'] == color) & (df['upside_bucket'] == bucket)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df['vs_avg'])
        level2.loc[(color, bucket), 'p_value'] = p

level2.to_csv('analysis_l2_color_upside_isolated.csv')
print(f"Saved: analysis_l2_color_upside_isolated.csv ({len(level2)} combos)\n")

# ============================================================================
# LEVEL 3: Color × Exec × Condition
# ============================================================================
print("LEVEL 3: Color × Exec × Condition...")
level3 = df.groupby(['color', 'exec_bucket', 'condition']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level3.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level3['beat_field'] = df.groupby(['color', 'exec_bucket', 'condition'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level3['p_value'] = np.nan
for (color, bucket, cond) in level3.index:
    group_data = df[(df['color'] == color) & (df['exec_bucket'] == bucket) & (df['condition'] == cond)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['condition'] == cond]['vs_avg'])
        level3.loc[(color, bucket, cond), 'p_value'] = p

level3.to_csv('analysis_l3_color_exec_condition.csv')
print(f"Saved: analysis_l3_color_exec_condition.csv ({len(level3)} combos)\n")

# ============================================================================
# LEVEL 4: Color × Upside × Condition
# ============================================================================
print("LEVEL 4: Color × Upside × Condition...")
level4 = df.groupby(['color', 'upside_bucket', 'condition']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level4.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level4['beat_field'] = df.groupby(['color', 'upside_bucket', 'condition'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level4['p_value'] = np.nan
for (color, bucket, cond) in level4.index:
    group_data = df[(df['color'] == color) & (df['upside_bucket'] == bucket) & (df['condition'] == cond)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['condition'] == cond]['vs_avg'])
        level4.loc[(color, bucket, cond), 'p_value'] = p

level4.to_csv('analysis_l4_color_upside_condition.csv')
print(f"Saved: analysis_l4_color_upside_condition.csv ({len(level4)} combos)\n")

# ============================================================================
# LEVEL 5: Color × Exec × Round type
# ============================================================================
print("LEVEL 5: Color × Exec × Round type...")
level5 = df.groupby(['color', 'exec_bucket', 'round_type']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level5.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level5['beat_field'] = df.groupby(['color', 'exec_bucket', 'round_type'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level5['p_value'] = np.nan
for (color, bucket, rnd) in level5.index:
    group_data = df[(df['color'] == color) & (df['exec_bucket'] == bucket) & (df['round_type'] == rnd)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['round_type'] == rnd]['vs_avg'])
        level5.loc[(color, bucket, rnd), 'p_value'] = p

level5.to_csv('analysis_l5_color_exec_round.csv')
print(f"Saved: analysis_l5_color_exec_round.csv ({len(level5)} combos)\n")

# ============================================================================
# LEVEL 6: Color × Upside × Round type
# ============================================================================
print("LEVEL 6: Color × Upside × Round type...")
level6 = df.groupby(['color', 'upside_bucket', 'round_type']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level6.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level6['beat_field'] = df.groupby(['color', 'upside_bucket', 'round_type'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level6['p_value'] = np.nan
for (color, bucket, rnd) in level6.index:
    group_data = df[(df['color'] == color) & (df['upside_bucket'] == bucket) & (df['round_type'] == rnd)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['round_type'] == rnd]['vs_avg'])
        level6.loc[(color, bucket, rnd), 'p_value'] = p

level6.to_csv('analysis_l6_color_upside_round.csv')
print(f"Saved: analysis_l6_color_upside_round.csv ({len(level6)} combos)\n")

# ============================================================================
# LEVEL 7: Color × Exec × Element
# ============================================================================
print("LEVEL 7: Color × Exec × Element...")
level7 = df.groupby(['color', 'exec_bucket', 'wu_xing']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level7.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level7['beat_field'] = df.groupby(['color', 'exec_bucket', 'wu_xing'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level7['p_value'] = np.nan
for (color, bucket, elem) in level7.index:
    group_data = df[(df['color'] == color) & (df['exec_bucket'] == bucket) & (df['wu_xing'] == elem)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['wu_xing'] == elem]['vs_avg'])
        level7.loc[(color, bucket, elem), 'p_value'] = p

level7.to_csv('analysis_l7_color_exec_element.csv')
print(f"Saved: analysis_l7_color_exec_element.csv ({len(level7)} combos)\n")

# ============================================================================
# LEVEL 8: Color × Upside × Element
# ============================================================================
print("LEVEL 8: Color × Upside × Element...")
level8 = df.groupby(['color', 'upside_bucket', 'wu_xing']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level8.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level8['beat_field'] = df.groupby(['color', 'upside_bucket', 'wu_xing'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level8['p_value'] = np.nan
for (color, bucket, elem) in level8.index:
    group_data = df[(df['color'] == color) & (df['upside_bucket'] == bucket) & (df['wu_xing'] == elem)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[df['wu_xing'] == elem]['vs_avg'])
        level8.loc[(color, bucket, elem), 'p_value'] = p

level8.to_csv('analysis_l8_color_upside_element.csv')
print(f"Saved: analysis_l8_color_upside_element.csv ({len(level8)} combos)\n")

# ============================================================================
# LEVEL 9: 4D Color × Exec × Condition × Round type
# ============================================================================
print("LEVEL 9: Color × Exec × Condition × Round type (4D)...")
level9 = df.groupby(['color', 'exec_bucket', 'condition', 'round_type']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level9.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level9['beat_field'] = df.groupby(['color', 'exec_bucket', 'condition', 'round_type'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x) if len(x) > 0 else np.nan).round(4)

level9['p_value'] = np.nan
for (color, bucket, cond, rnd) in level9.index:
    group_data = df[(df['color'] == color) & (df['exec_bucket'] == bucket) &
                    (df['condition'] == cond) & (df['round_type'] == rnd)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[(df['condition'] == cond) & (df['round_type'] == rnd)]['vs_avg'])
        level9.loc[(color, bucket, cond, rnd), 'p_value'] = p

level9.to_csv('analysis_l9_color_exec_cond_round_4d.csv')
print(f"Saved: analysis_l9_color_exec_cond_round_4d.csv ({len(level9)} combos)\n")

# ============================================================================
# LEVEL 10: 4D Color × Upside × Condition × Round type
# ============================================================================
print("LEVEL 10: Color × Upside × Condition × Round type (4D)...")
level10 = df.groupby(['color', 'upside_bucket', 'condition', 'round_type']).agg({
    'vs_avg': ['mean', 'std', 'count'],
    'player_name': 'nunique'
}).round(4)
level10.columns = ['mean_vs_avg', 'std', 'n', 'unique_players']
level10['beat_field'] = df.groupby(['color', 'upside_bucket', 'condition', 'round_type'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x) if len(x) > 0 else np.nan).round(4)

level10['p_value'] = np.nan
for (color, bucket, cond, rnd) in level10.index:
    group_data = df[(df['color'] == color) & (df['upside_bucket'] == bucket) &
                    (df['condition'] == cond) & (df['round_type'] == rnd)]['vs_avg']
    if len(group_data) >= 5:
        _, p = stats.ttest_ind(group_data, df[(df['condition'] == cond) & (df['round_type'] == rnd)]['vs_avg'])
        level10.loc[(color, bucket, cond, rnd), 'p_value'] = p

level10.to_csv('analysis_l10_color_upside_cond_round_4d.csv')
print(f"Saved: analysis_l10_color_upside_cond_round_4d.csv ({len(level10)} combos)\n")

# ============================================================================
# LEVEL 11: Time trend - Color × Exec by Year
# ============================================================================
print("LEVEL 11: Color × Exec × Year (time trend)...")
level11 = df.groupby(['color', 'exec_bucket', 'year']).agg({
    'vs_avg': ['mean', 'count'],
    'player_name': 'nunique'
}).round(4)
level11.columns = ['mean_vs_avg', 'n', 'unique_players']
level11['beat_field'] = df.groupby(['color', 'exec_bucket', 'year'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level11.to_csv('analysis_l11_color_exec_year.csv')
print(f"Saved: analysis_l11_color_exec_year.csv ({len(level11)} combos)\n")

# ============================================================================
# LEVEL 12: Time trend - Color × Upside by Year
# ============================================================================
print("LEVEL 12: Color × Upside × Year (time trend)...")
level12 = df.groupby(['color', 'upside_bucket', 'year']).agg({
    'vs_avg': ['mean', 'count'],
    'player_name': 'nunique'
}).round(4)
level12.columns = ['mean_vs_avg', 'n', 'unique_players']
level12['beat_field'] = df.groupby(['color', 'upside_bucket', 'year'])['vs_avg'].apply(lambda x: (x > 0).sum() / len(x)).round(4)

level12.to_csv('analysis_l12_color_upside_year.csv')
print(f"Saved: analysis_l12_color_upside_year.csv ({len(level12)} combos)\n")

# ============================================================================
# LEVEL 13: Correlation by Color - Exec & Upside vs vs_avg
# ============================================================================
print("LEVEL 13: Correlation analysis by Color...")
corr_results = []
for color in sorted(df['color'].unique()):
    color_df = df[df['color'] == color]
    exec_corr = color_df['exec'].corr(color_df['vs_avg'])
    upside_corr = color_df['upside'].corr(color_df['vs_avg'])

    # Pearson + p-value
    exec_r, exec_p = stats.pearsonr(color_df['exec'], color_df['vs_avg'])
    upside_r, upside_p = stats.pearsonr(color_df['upside'], color_df['vs_avg'])

    corr_results.append({
        'color': color,
        'n': len(color_df),
        'exec_correlation': exec_r,
        'exec_p_value': exec_p,
        'upside_correlation': upside_r,
        'upside_p_value': upside_p,
        'mean_exec': color_df['exec'].mean(),
        'mean_upside': color_df['upside'].mean(),
        'mean_vs_avg': color_df['vs_avg'].mean(),
        'beat_field_pct': (color_df['vs_avg'] > 0).sum() / len(color_df)
    })

corr_df = pd.DataFrame(corr_results).round(4)
corr_df.to_csv('analysis_l13_correlation_by_color.csv', index=False)
print(f"Saved: analysis_l13_correlation_by_color.csv\n")

# ============================================================================
# Summary Report
# ============================================================================
print("=" * 80)
print("COMPREHENSIVE ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nData summary:")
print(f"  Total rounds: {len(df)}")
print(f"  Unique players: {df['player_name'].nunique()}")
print(f"  Colors: {sorted(df['color'].unique())}")
print(f"  Baseline vs_avg: {baseline_mean:.4f}")
print(f"  Baseline beat_field: {baseline_beat:.1%}")

print(f"\nFiles generated:")
print("  L1: Color × Exec (isolated) — 32 combos")
print("  L2: Color × Upside (isolated) — 32 combos")
print("  L3: Color × Exec × Condition — 96 combos")
print("  L4: Color × Upside × Condition — 96 combos")
print("  L5: Color × Exec × Round type — 128 combos")
print("  L6: Color × Upside × Round type — 128 combos")
print("  L7: Color × Exec × Element — 160 combos")
print("  L8: Color × Upside × Element — 160 combos")
print("  L9: Color × Exec × Condition × Round (4D) — 384 combos")
print("  L10: Color × Upside × Condition × Round (4D) — 384 combos")
print("  L11: Color × Exec × Year — 160 combos")
print("  L12: Color × Upside × Year — 160 combos")
print("  L13: Correlation by Color — 8 summary rows")

print("\n[NEXT STEP] Review CSVs for significant combos (p < 0.05, n >= 50)")
