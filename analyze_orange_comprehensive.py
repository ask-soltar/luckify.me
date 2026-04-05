"""
Orange Comprehensive Analysis --- 15-Level Dimensional Study
Data Source: DATA/Golf Historics v3 - ANALYSIS (8).csv (2026-04-04)

Analyzes Orange players across:
- L1: Condition (Calm/Moderate/Tough)
- L2: Round Type (Open/Positioning/Closing/Survival/Elimination/Mixed)
- L3: Wu Xing Element (Earth/Fire/Metal/Water/Wood)
- L4: Exec bucket (0-25, 25-50, 50-75, 75-100)
- L5: Moon Western 8-phase (individual)
- L6: Moon Western 4-grouped (Waxing/Waning/Full/New)
- L7: Moon Vedic 10-category
- L8-L13: 3D interactions
- L14: Correlation analysis
- L15: Year trend

Sign Convention: vs_avg = score - course_avg
Negative = beats field (good), Positive = loses to field (bad)
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING
# ============================================================================

print("=" * 80)
print("ORANGE COMPREHENSIVE ANALYSIS --- Starting")
print("=" * 80)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Data Source: DATA/Golf Historics v3 - ANALYSIS (8).csv")
print()

# Load data
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig')
# Ensure numeric columns are actually numeric
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['exec'] = pd.to_numeric(df['exec'], errors='coerce')
df['upside'] = pd.to_numeric(df['upside'], errors='coerce')
df['Personal Year'] = pd.to_numeric(df['Personal Year'], errors='coerce')
print(f"[OK] Loaded {len(df)} total rows")

# Filter: Orange only, stroke play (S or NS)
df_orange = df[(df['color'] == 'Orange') & (df['tournament_type'].isin(['S', 'NS']))].copy()
print(f"[OK] Filtered to {len(df_orange)} Orange + stroke-play rows")
print()

# Data quality checks
print("Data Quality:")
print(f"  - vs_avg nulls: {df_orange['vs_avg'].isna().sum()}")
print(f"  - condition nulls: {df_orange['condition'].isna().sum()}")
print(f"  - round_type nulls: {df_orange['round_type'].isna().sum()}")
print(f"  - moon (Vedic) nulls: {df_orange['moon'].isna().sum()}")
print(f"  - moonwest nulls: {df_orange['moonwest'].isna().sum()}")
print()

# Remove REMOVE rounds (not comparable)
df_orange = df_orange[df_orange['round_type'] != 'REMOVE'].copy()
print(f"[OK] Removed REMOVE rounds: {len(df_orange)} rows remaining")
print()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def analyze_combo(df, dimension, value, combo_name=None):
    """Analyze a single dimension combo against baseline."""
    subset = df[df[dimension] == value]

    if len(subset) == 0:
        return None

    n = len(subset)
    mean_vs_avg = subset['vs_avg'].mean()
    std_vs_avg = subset['vs_avg'].std()
    beat_field_count = (subset['vs_avg'] < 0).sum()
    beat_field_pct = 100 * beat_field_count / n if n > 0 else 0

    # T-test vs 0
    t_stat, p_value = stats.ttest_1samp(subset['vs_avg'], 0, nan_policy='omit')

    # Baseline excess (vs rest)
    baseline_subset = df[df[dimension] != value]
    baseline_mean = baseline_subset['vs_avg'].mean()
    excess = mean_vs_avg - baseline_mean

    return {
        'combo': combo_name or f"{dimension}={value}",
        'dimension': dimension,
        'value': value,
        'n': n,
        'mean_vs_avg': round(mean_vs_avg, 4),
        'std': round(std_vs_avg, 4) if not pd.isna(std_vs_avg) else 0,
        'beat_field_pct': round(beat_field_pct, 1),
        'beat_field_count': beat_field_count,
        'p_value': round(p_value, 4),
        'excess_vs_baseline': round(excess, 4),
        'signal_quality': 'rock_solid' if (n >= 100 and p_value < 0.05 and abs(mean_vs_avg) >= 0.20) else 'acceptable' if (n >= 50 and p_value < 0.05) else 'weak'
    }

def analyze_2d_combo(df, dim1, val1, dim2, val2, combo_name=None):
    """Analyze a 2D combination."""
    subset = df[(df[dim1] == val1) & (df[dim2] == val2)]

    if len(subset) == 0:
        return None

    n = len(subset)
    mean_vs_avg = subset['vs_avg'].mean()
    std_vs_avg = subset['vs_avg'].std()
    beat_field_count = (subset['vs_avg'] < 0).sum()
    beat_field_pct = 100 * beat_field_count / n if n > 0 else 0

    t_stat, p_value = stats.ttest_1samp(subset['vs_avg'], 0, nan_policy='omit')

    baseline_subset = df[~((df[dim1] == val1) & (df[dim2] == val2))]
    baseline_mean = baseline_subset['vs_avg'].mean()
    excess = mean_vs_avg - baseline_mean

    return {
        'combo': combo_name or f"{dim1}={val1}, {dim2}={val2}",
        'dimension': f"{dim1} -- {dim2}",
        'value': f"{val1} -- {val2}",
        'n': n,
        'mean_vs_avg': round(mean_vs_avg, 4),
        'std': round(std_vs_avg, 4) if not pd.isna(std_vs_avg) else 0,
        'beat_field_pct': round(beat_field_pct, 1),
        'beat_field_count': beat_field_count,
        'p_value': round(p_value, 4),
        'excess_vs_baseline': round(excess, 4),
        'signal_quality': 'rock_solid' if (n >= 100 and p_value < 0.05 and abs(mean_vs_avg) >= 0.20) else 'acceptable' if (n >= 50 and p_value < 0.05) else 'weak'
    }

# ============================================================================
# LEVEL 1: CONDITION (Calm/Moderate/Tough)
# ============================================================================

print("=" * 80)
print("L1: CONDITION (Calm/Moderate/Tough)")
print("=" * 80)

l1_results = []
for cond in ['Calm', 'Moderate', 'Tough']:
    result = analyze_combo(df_orange, 'condition', cond)
    if result:
        l1_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {cond:12} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l1_df = pd.DataFrame(l1_results)
l1_df.to_csv('ORANGE_L1_condition.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L1_condition.csv\n")

# ============================================================================
# LEVEL 2: ROUND TYPE
# ============================================================================

print("=" * 80)
print("L2: ROUND TYPE")
print("=" * 80)

l2_results = []
for rtype in df_orange['round_type'].dropna().unique():
    result = analyze_combo(df_orange, 'round_type', rtype)
    if result:
        l2_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {rtype:15} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l2_df = pd.DataFrame(l2_results)
l2_df.to_csv('ORANGE_L2_round_type.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L2_round_type.csv\n")

# ============================================================================
# LEVEL 3: WU XING ELEMENT
# ============================================================================

print("=" * 80)
print("L3: WU XING ELEMENT (Earth/Fire/Metal/Water/Wood)")
print("=" * 80)

l3_results = []
for elem in ['Earth', 'Fire', 'Metal', 'Water', 'Wood']:
    result = analyze_combo(df_orange, 'wu_xing', elem)
    if result:
        l3_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {elem:12} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l3_df = pd.DataFrame(l3_results)
l3_df.to_csv('ORANGE_L3_element.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L3_element.csv\n")

# ============================================================================
# LEVEL 4: EXEC BUCKET
# ============================================================================

print("=" * 80)
print("L4: EXEC BUCKET (0-25, 25-50, 50-75, 75-100)")
print("=" * 80)

l4_results = []
for bucket in ['0-25', '25-50', '50-75', '75-100']:
    result = analyze_combo(df_orange, 'exec_bucket', bucket)
    if result:
        l4_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {bucket:12} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l4_df = pd.DataFrame(l4_results)
l4_df.to_csv('ORANGE_L4_exec_bucket.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L4_exec_bucket.csv\n")

# ============================================================================
# LEVEL 5: MOON WESTERN 8-PHASE (Individual)
# ============================================================================

print("=" * 80)
print("L5: MOON WESTERN 8-PHASE (Individual Phases)")
print("=" * 80)

l5_results = []
for phase in df_orange['moonwest'].dropna().unique():
    result = analyze_combo(df_orange, 'moonwest', phase)
    if result and result['n'] >= 20:  # Lower threshold for individual phases (diversity)
        l5_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {phase:20} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l5_df = pd.DataFrame(l5_results)
l5_df.to_csv('ORANGE_L5_moon_western_8phase.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L5_moon_western_8phase.csv\n")

# ============================================================================
# LEVEL 6: MOON WESTERN GROUPED (Waxing/Waning/Full/New)
# ============================================================================

print("=" * 80)
print("L6: MOON WESTERN GROUPED (Waxing/Waning/Full/New)")
print("=" * 80)

# Map moonwest to groups
def map_moon_group(phase):
    if pd.isna(phase):
        return None
    if phase in ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter']:
        return 'Waxing'
    elif phase in ['Waning Crescent', 'Waning Gibbous', 'Last Quarter']:
        return 'Waning'
    elif phase == 'Full Moon':
        return 'Full Moon'
    elif phase == 'New Moon':
        return 'New Moon'
    return None

df_orange['moon_group'] = df_orange['moonwest'].apply(map_moon_group)

l6_results = []
for group in ['Waxing', 'Waning', 'Full Moon', 'New Moon']:
    result = analyze_combo(df_orange, 'moon_group', group)
    if result:
        l6_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {group:15} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l6_df = pd.DataFrame(l6_results)
l6_df.to_csv('ORANGE_L6_moon_western_grouped.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L6_moon_western_grouped.csv\n")

# ============================================================================
# LEVEL 7: MOON VEDIC 10-CATEGORY
# ============================================================================

print("=" * 80)
print("L7: MOON VEDIC 10-CATEGORY")
print("=" * 80)

l7_results = []
for vedic_moon in df_orange['moon'].dropna().unique():
    result = analyze_combo(df_orange, 'moon', vedic_moon)
    if result and result['n'] >= 20:  # Lower threshold for diversity
        l7_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {vedic_moon:20} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l7_df = pd.DataFrame(l7_results)
l7_df.to_csv('ORANGE_L7_moon_vedic_10cat.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L7_moon_vedic_10cat.csv\n")

# ============================================================================
# LEVEL 8: CONDITION -- ROUND TYPE (2D)
# ============================================================================

print("=" * 80)
print("L8: CONDITION -- ROUND TYPE (2D Interaction)")
print("=" * 80)

l8_results = []
for cond in ['Calm', 'Moderate', 'Tough']:
    for rtype in df_orange['round_type'].dropna().unique():
        if rtype == 'REMOVE':
            continue
        result = analyze_2d_combo(df_orange, 'condition', cond, 'round_type', rtype,
                                 f"{cond} -- {rtype}")
        if result and result['n'] >= 15:
            l8_results.append(result)

l8_df = pd.DataFrame(l8_results).sort_values('mean_vs_avg')
# Print top signals only
print(f"Found {len(l8_df)} condition--round combos. Top 5 outperformers:")
for idx, row in l8_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")
print(f"Top 5 underperformers:")
for idx, row in l8_df.tail(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l8_df.to_csv('ORANGE_L8_condition_roundtype_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L8_condition_roundtype_2d.csv ({len(l8_df)} rows)\n")

# ============================================================================
# LEVEL 9: ELEMENT -- EXEC BUCKET (2D)
# ============================================================================

print("=" * 80)
print("L9: ELEMENT -- EXEC BUCKET (2D Interaction)")
print("=" * 80)

l9_results = []
for elem in ['Earth', 'Fire', 'Metal', 'Water', 'Wood']:
    for bucket in ['0-25', '25-50', '50-75', '75-100']:
        result = analyze_2d_combo(df_orange, 'wu_xing', elem, 'exec_bucket', bucket,
                                 f"{elem} -- {bucket}")
        if result and result['n'] >= 10:
            l9_results.append(result)

l9_df = pd.DataFrame(l9_results).sort_values('mean_vs_avg')
print(f"Found {len(l9_df)} element--exec combos. Top 5 outperformers:")
for idx, row in l9_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")
print(f"Top 5 underperformers:")
for idx, row in l9_df.tail(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l9_df.to_csv('ORANGE_L9_element_exec_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L9_element_exec_2d.csv ({len(l9_df)} rows)\n")

# ============================================================================
# LEVEL 10: MOON -- CONDITION (2D)
# ============================================================================

print("=" * 80)
print("L10: MOON WESTERN GROUP -- CONDITION (2D Interaction)")
print("=" * 80)

l10_results = []
for group in ['Waxing', 'Waning', 'Full Moon', 'New Moon']:
    for cond in ['Calm', 'Moderate', 'Tough']:
        result = analyze_2d_combo(df_orange, 'moon_group', group, 'condition', cond,
                                 f"{group} -- {cond}")
        if result and result['n'] >= 10:
            l10_results.append(result)

l10_df = pd.DataFrame(l10_results).sort_values('mean_vs_avg')
print(f"Found {len(l10_df)} moon--condition combos. Top 5 outperformers:")
for idx, row in l10_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l10_df.to_csv('ORANGE_L10_moon_condition_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L10_moon_condition_2d.csv ({len(l10_df)} rows)\n")

# ============================================================================
# LEVEL 11: MOON -- ROUND TYPE (2D)
# ============================================================================

print("=" * 80)
print("L11: MOON WESTERN GROUP -- ROUND TYPE (2D Interaction)")
print("=" * 80)

l11_results = []
for group in ['Waxing', 'Waning', 'Full Moon', 'New Moon']:
    for rtype in df_orange['round_type'].dropna().unique():
        if rtype == 'REMOVE':
            continue
        result = analyze_2d_combo(df_orange, 'moon_group', group, 'round_type', rtype,
                                 f"{group} -- {rtype}")
        if result and result['n'] >= 10:
            l11_results.append(result)

l11_df = pd.DataFrame(l11_results).sort_values('mean_vs_avg')
print(f"Found {len(l11_df)} moon--roundtype combos. Top 5 outperformers:")
for idx, row in l11_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l11_df.to_csv('ORANGE_L11_moon_roundtype_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L11_moon_roundtype_2d.csv ({len(l11_df)} rows)\n")

# ============================================================================
# LEVEL 12: MOON -- ELEMENT (2D)
# ============================================================================

print("=" * 80)
print("L12: MOON WESTERN GROUP -- ELEMENT (2D Interaction)")
print("=" * 80)

l12_results = []
for group in ['Waxing', 'Waning', 'Full Moon', 'New Moon']:
    for elem in ['Earth', 'Fire', 'Metal', 'Water', 'Wood']:
        result = analyze_2d_combo(df_orange, 'moon_group', group, 'wu_xing', elem,
                                 f"{group} -- {elem}")
        if result and result['n'] >= 10:
            l12_results.append(result)

l12_df = pd.DataFrame(l12_results).sort_values('mean_vs_avg')
print(f"Found {len(l12_df)} moon--element combos. Top 5 outperformers:")
for idx, row in l12_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l12_df.to_csv('ORANGE_L12_moon_element_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L12_moon_element_2d.csv ({len(l12_df)} rows)\n")

# ============================================================================
# LEVEL 13: MOON -- EXEC BUCKET (2D)
# ============================================================================

print("=" * 80)
print("L13: MOON WESTERN GROUP -- EXEC BUCKET (2D Interaction)")
print("=" * 80)

l13_results = []
for group in ['Waxing', 'Waning', 'Full Moon', 'New Moon']:
    for bucket in ['0-25', '25-50', '50-75', '75-100']:
        result = analyze_2d_combo(df_orange, 'moon_group', group, 'exec_bucket', bucket,
                                 f"{group} -- {bucket}")
        if result and result['n'] >= 10:
            l13_results.append(result)

l13_df = pd.DataFrame(l13_results).sort_values('mean_vs_avg')
print(f"Found {len(l13_df)} moon--exec combos. Top 5 outperformers:")
for idx, row in l13_df.head(5).iterrows():
    print(f"  {row['combo']:35} | n={row['n']:4} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

l13_df.to_csv('ORANGE_L13_moon_exec_2d.csv', index=False)
print(f"\n[OK] Saved: ORANGE_L13_moon_exec_2d.csv ({len(l13_df)} rows)\n")

# ============================================================================
# LEVEL 14: PERSONAL NUMEROLOGY (Personal Year, Month, Day)
# ============================================================================

print("=" * 80)
print("L14: PERSONAL NUMEROLOGY (Personal Year/Month/Day)")
print("=" * 80)

# Personal Year
print("Personal Year:")
l14_py_results = []
for py in sorted(df_orange['Personal Year'].dropna().unique()):
    result = analyze_combo(df_orange, 'Personal Year', py, f"Personal Year {int(py)}")
    if result and result['n'] >= 20:
        l14_py_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} Year {int(py):2} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l14_py_df = pd.DataFrame(l14_py_results)
l14_py_df.to_csv('ORANGE_L14_personal_year.csv', index=False)
print(f"[OK] Saved: ORANGE_L14_personal_year.csv\n")

# ============================================================================
# LEVEL 15: ZODIAC & HOROSCOPE
# ============================================================================

print("=" * 80)
print("L15: ZODIAC & HOROSCOPE")
print("=" * 80)

print("Chinese Zodiac:")
l15_zodiac_results = []
for zodiac in df_orange['zodiac'].dropna().unique():
    result = analyze_combo(df_orange, 'zodiac', zodiac)
    if result and result['n'] >= 20:
        l15_zodiac_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {zodiac:12} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l15_zodiac_df = pd.DataFrame(l15_zodiac_results)
l15_zodiac_df.to_csv('ORANGE_L15_zodiac.csv', index=False)
print(f"[OK] Saved: ORANGE_L15_zodiac.csv\n")

print("Western Horoscope:")
l15_horo_results = []
for horo in df_orange['horoscope'].dropna().unique():
    result = analyze_combo(df_orange, 'horoscope', horo)
    if result and result['n'] >= 15:
        l15_horo_results.append(result)
        signal = "[OK] SIGNAL" if result['signal_quality'] in ['rock_solid', 'acceptable'] else "---"
        print(f"{signal} {horo:12} | n={result['n']:5} | mean={result['mean_vs_avg']:7.4f} | beat%={result['beat_field_pct']:5.1f}% | p={result['p_value']:.4f}")

l15_horo_df = pd.DataFrame(l15_horo_results)
l15_horo_df.to_csv('ORANGE_L15_horoscope.csv', index=False)
print(f"[OK] Saved: ORANGE_L15_horoscope.csv\n")

# ============================================================================
# SIGNAL EXTRACTION & SUMMARY
# ============================================================================

print("=" * 80)
print("SIGNAL SUMMARY (All Levels Combined)")
print("=" * 80)

# Combine all results
all_results = []
for level_num, level_df in enumerate([l1_df, l2_df, l3_df, l4_df, l5_df, l6_df, l7_df,
                                      l8_df, l9_df, l10_df, l11_df, l12_df, l13_df,
                                      l14_py_df, l15_zodiac_df, l15_horo_df], 1):
    if 'level' not in level_df.columns:
        level_df['level'] = f"L{level_num}"
    all_results.append(level_df)

all_signals = pd.concat(all_results, ignore_index=True)

# Filter for strong signals
strong_signals = all_signals[
    (all_signals['n'] >= 100) &
    (all_signals['p_value'] < 0.05) &
    (abs(all_signals['mean_vs_avg']) >= 0.20)
].sort_values('mean_vs_avg')

print(f"\n[SIGNALS] ROCK SOLID SIGNALS (n---100, p<0.05, |mean|---0.20):")
print(f"Found {len(strong_signals)} signals\n")

if len(strong_signals) > 0:
    print("OUTPERFORMERS (beats field --- negative values):")
    outperformers = strong_signals[strong_signals['mean_vs_avg'] < 0].sort_values('mean_vs_avg')
    for idx, row in outperformers.iterrows():
        print(f"  [OK] {row['combo']:40} | n={row['n']:5} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

    print("\nUNDERPERFORMERS (loses to field --- positive values):")
    underperformers = strong_signals[strong_signals['mean_vs_avg'] > 0].sort_values('mean_vs_avg', ascending=False)
    for idx, row in underperformers.iterrows():
        print(f"  [FADE] {row['combo']:40} | n={row['n']:5} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")
else:
    print("No rock-solid signals found. Review acceptable-tier signals:\n")
    acceptable = all_signals[
        (all_signals['n'] >= 50) &
        (all_signals['p_value'] < 0.05)
    ].sort_values('mean_vs_avg')

    print(f"Found {len(acceptable)} acceptable-tier signals (n---50, p<0.05):")
    for idx, row in acceptable.head(15).iterrows():
        print(f"  {row['combo']:40} | n={row['n']:5} | mean={row['mean_vs_avg']:7.4f} | p={row['p_value']:.4f}")

# Save all signals
all_signals.to_csv('ORANGE_ALL_SIGNALS_COMPILED.csv', index=False)
strong_signals.to_csv('ORANGE_ROCK_SOLID_SIGNALS.csv', index=False)
print(f"\n[OK] Saved: ORANGE_ALL_SIGNALS_COMPILED.csv")
print(f"[OK] Saved: ORANGE_ROCK_SOLID_SIGNALS.csv")

# ============================================================================
# EXECUTION SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("EXECUTION COMPLETE")
print("=" * 80)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nFiles generated:")
print(f"  L1:  ORANGE_L1_condition.csv")
print(f"  L2:  ORANGE_L2_round_type.csv")
print(f"  L3:  ORANGE_L3_element.csv")
print(f"  L4:  ORANGE_L4_exec_bucket.csv")
print(f"  L5:  ORANGE_L5_moon_western_8phase.csv")
print(f"  L6:  ORANGE_L6_moon_western_grouped.csv")
print(f"  L7:  ORANGE_L7_moon_vedic_10cat.csv")
print(f"  L8:  ORANGE_L8_condition_roundtype_2d.csv")
print(f"  L9:  ORANGE_L9_element_exec_2d.csv")
print(f"  L10: ORANGE_L10_moon_condition_2d.csv")
print(f"  L11: ORANGE_L11_moon_roundtype_2d.csv")
print(f"  L12: ORANGE_L12_moon_element_2d.csv")
print(f"  L13: ORANGE_L13_moon_exec_2d.csv")
print(f"  L14: ORANGE_L14_personal_year.csv")
print(f"  L15: ORANGE_L15_zodiac.csv + horoscope.csv")
print(f"\nSignal Compilation:")
print(f"  ORANGE_ALL_SIGNALS_COMPILED.csv ({len(all_signals)} combos)")
print(f"  ORANGE_ROCK_SOLID_SIGNALS.csv ({len(strong_signals)} signals)")
print(f"\nNext: Review outputs and write ORANGE_DEEP_ANALYSIS_SUMMARY.md")
print("=" * 80)
