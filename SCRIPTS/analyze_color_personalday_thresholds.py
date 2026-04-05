"""
Analysis: Color & Personal Day frequency distributions by +2/-2 score thresholds
Input: Golf Historics v3 - ANALYSIS (7).csv
Output: 3 CSV files + console summary
"""

import duckdb
import pandas as pd
import numpy as np
import sys

# File paths
INPUT_CSV = r"d:\Projects\luckify-me\Golf Historics v3 - ANALYSIS (7).csv"
OUTPUT_DIR = r"d:\Projects\luckify-me"

print("=" * 80)
print("ANALYSIS: Color & Personal Day Frequency Distribution (+2/-2 Thresholds)")
print("=" * 80)
print()

# ============================================================================
# STEP 1: Load and filter data with DuckDB
# ============================================================================
print("[1/5] Loading and filtering data...")

conn = duckdb.connect(':memory:')

# Read CSV
df_raw = pd.read_csv(INPUT_CSV)
print(f"  Raw records: {len(df_raw):,}")

# Register as DuckDB table
conn.register('data', df_raw)

# Filter: condition (Calm/Moderate/Tough), round_type (Open/Positioning/Closing/Survival), tournament_type (S/NS)
query_filter = """
SELECT *,
       CAST(score AS FLOAT) - CAST(course_avg AS FLOAT) AS metric
FROM data
WHERE condition IN ('Calm', 'Moderate', 'Tough')
  AND round_type IN ('Open', 'Positioning', 'Closing', 'Survival')
  AND tournament_type IN ('S', 'NS')
  AND color IS NOT NULL
  AND "Personal Day" IS NOT NULL
  AND "Personal Day" != ''
"""

df_filtered = conn.execute(query_filter).fetchdf()
print(f"  After filtering: {len(df_filtered):,}")
print(f"  Conditions: {sorted(df_filtered['condition'].unique().tolist())}")
print(f"  Round types: {sorted(df_filtered['round_type'].unique().tolist())}")
print(f"  Tournament types: {sorted(df_filtered['tournament_type'].unique().tolist())}")
print()

# ============================================================================
# STEP 2: Bin into +2/-2 thresholds
# ============================================================================
print("[2/5] Binning metric into +2/-2 thresholds...")

def bin_metric(val):
    """Bin score_vs_avg into ranges"""
    if pd.isna(val):
        return None
    if val < -6:
        return "-6 to -4"
    elif val < -4:
        return "-6 to -4"
    elif val < -2:
        return "-4 to -2"
    elif val < 0:
        return "-2 to 0"
    elif val < 2:
        return "0 to 2"
    elif val < 4:
        return "2 to 4"
    elif val < 6:
        return "4 to 6"
    else:
        return "6+"

df_filtered['bin'] = df_filtered['metric'].apply(bin_metric)

# Order bins for output
BIN_ORDER = ["-6 to -4", "-4 to -2", "-2 to 0", "0 to 2", "2 to 4", "4 to 6", "6+"]
print(f"  Bins created: {sorted(df_filtered['bin'].unique().tolist())}")
print()

# ============================================================================
# STEP 3: Build frequency distribution by COLOR
# ============================================================================
print("[3/5] Building frequency distribution by COLOR...")

# Count total records
total_records = len(df_filtered)

# Build color distribution
color_freq = []
for color in sorted(df_filtered['color'].unique()):
    color_data = df_filtered[df_filtered['color'] == color]
    color_count = len(color_data)
    color_pct = (color_count / total_records) * 100

    mean_metric = color_data['metric'].mean()

    # Bin breakdown
    bin_breakdown = {}
    for bin_name in BIN_ORDER:
        bin_count = len(color_data[color_data['bin'] == bin_name])
        bin_pct = (bin_count / color_count * 100) if color_count > 0 else 0
        bin_breakdown[bin_name] = {'count': bin_count, 'pct': bin_pct}

    color_freq.append({
        'color': color,
        'count': color_count,
        'pct_of_population': color_pct,
        'mean_metric': round(mean_metric, 4),
        **{f'{bn}_count': bin_breakdown[bn]['count'] for bn in BIN_ORDER},
        **{f'{bn}_pct': round(bin_breakdown[bn]['pct'], 2) for bn in BIN_ORDER}
    })

df_color_freq = pd.DataFrame(color_freq).sort_values('count', ascending=False)
print(f"  {len(df_color_freq)} unique colors")
print()

# ============================================================================
# STEP 4: Build frequency distribution by PERSONAL DAY
# ============================================================================
print("[4/5] Building frequency distribution by PERSONAL DAY...")

personalday_freq = []
for pd_val in sorted(df_filtered['Personal Day'].dropna().unique()):
    pd_val_str = str(int(pd_val)) if isinstance(pd_val, (int, float)) and not pd.isna(pd_val) else str(pd_val)
    pd_data = df_filtered[df_filtered['Personal Day'].astype(str) == pd_val_str]
    pd_count = len(pd_data)
    pd_pct = (pd_count / total_records) * 100

    mean_metric = pd_data['metric'].mean()

    # Bin breakdown
    bin_breakdown = {}
    for bin_name in BIN_ORDER:
        bin_count = len(pd_data[pd_data['bin'] == bin_name])
        bin_pct = (bin_count / pd_count * 100) if pd_count > 0 else 0
        bin_breakdown[bin_name] = {'count': bin_count, 'pct': bin_pct}

    personalday_freq.append({
        'personal_day': pd_val_str,
        'count': pd_count,
        'pct_of_population': pd_pct,
        'mean_metric': round(mean_metric, 4),
        **{f'{bn}_count': bin_breakdown[bn]['count'] for bn in BIN_ORDER},
        **{f'{bn}_pct': round(bin_breakdown[bn]['pct'], 2) for bn in BIN_ORDER}
    })

df_pd_freq = pd.DataFrame(personalday_freq).sort_values('count', ascending=False)
print(f"  {len(df_pd_freq)} unique personal days (1-31)")
print()

# ============================================================================
# STEP 5: Create summary table and identify key findings
# ============================================================================
print("[5/5] Generating summary and identifying key findings...")

# Overall bin distribution
overall_bins = {}
for bin_name in BIN_ORDER:
    bin_count = len(df_filtered[df_filtered['bin'] == bin_name])
    bin_pct = (bin_count / total_records) * 100
    overall_bins[bin_name] = {'count': bin_count, 'pct': bin_pct}

# Summary table
summary_data = {
    'Total Records': total_records,
    'Unique Colors': len(df_color_freq),
    'Unique Personal Days': len(df_pd_freq),
    'Overall Mean Metric': round(df_filtered['metric'].mean(), 4),
    'Overall Median Metric': round(df_filtered['metric'].median(), 4),
    'Overall Std Dev': round(df_filtered['metric'].std(), 4),
}

print()
print("SUMMARY STATISTICS:")
print("-" * 50)
for key, val in summary_data.items():
    print(f"  {key}: {val}")

print()
print("OVERALL BIN DISTRIBUTION:")
print("-" * 50)
for bin_name in BIN_ORDER:
    print(f"  {bin_name:12} {overall_bins[bin_name]['count']:6,} ({overall_bins[bin_name]['pct']:5.2f}%)")

# ============================================================================
# KEY FINDINGS: Colors with strongest +2 and -2 bias
# ============================================================================
print()
print("KEY FINDINGS BY COLOR:")
print("-" * 80)

# Define positive range: 0 to 2, 2 to 4, 4 to 6, 6+
# Define negative range: < 0

df_color_freq['positive_bias'] = df_color_freq[[f'{bn}_pct' for bn in ['0 to 2', '2 to 4', '4 to 6', '6+']]].sum(axis=1)
df_color_freq['negative_bias'] = df_color_freq[[f'{bn}_pct' for bn in ['-6 to -4', '-4 to -2', '-2 to 0']]].sum(axis=1)
df_color_freq['strong_positive'] = df_color_freq[['2 to 4_pct', '4 to 6_pct', '6+_pct']].sum(axis=1)
df_color_freq['strong_negative'] = df_color_freq[['-6 to -4_pct', '-4 to -2_pct']].sum(axis=1)

print()
print("  TOP COLORS - STRONGEST +2 BIAS (positive skew):")
for idx, row in df_color_freq.nlargest(5, 'positive_bias').iterrows():
    print(f"    {row['color']:12} {row['positive_bias']:6.2f}% in positive range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP COLORS - STRONGEST -2 BIAS (negative skew):")
for idx, row in df_color_freq.nlargest(5, 'negative_bias').iterrows():
    print(f"    {row['color']:12} {row['negative_bias']:6.2f}% in negative range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP COLORS - STRONGEST STRONG POSITIVE BIAS (+2 to +6+):")
for idx, row in df_color_freq.nlargest(5, 'strong_positive').iterrows():
    print(f"    {row['color']:12} {row['strong_positive']:6.2f}% in +2 to +6+ range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP COLORS - STRONGEST STRONG NEGATIVE BIAS (-6 to -2):")
for idx, row in df_color_freq.nlargest(5, 'strong_negative').iterrows():
    print(f"    {row['color']:12} {row['strong_negative']:6.2f}% in -6 to -2 range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

# ============================================================================
# KEY FINDINGS: Personal Days with strongest +2 and -2 bias
# ============================================================================
print()
print("KEY FINDINGS BY PERSONAL DAY:")
print("-" * 80)

df_pd_freq['positive_bias'] = df_pd_freq[[f'{bn}_pct' for bn in ['0 to 2', '2 to 4', '4 to 6', '6+']]].sum(axis=1)
df_pd_freq['negative_bias'] = df_pd_freq[[f'{bn}_pct' for bn in ['-6 to -4', '-4 to -2', '-2 to 0']]].sum(axis=1)
df_pd_freq['strong_positive'] = df_pd_freq[['2 to 4_pct', '4 to 6_pct', '6+_pct']].sum(axis=1)
df_pd_freq['strong_negative'] = df_pd_freq[['-6 to -4_pct', '-4 to -2_pct']].sum(axis=1)

print()
print("  TOP PERSONAL DAYS - STRONGEST +2 BIAS (positive skew):")
for idx, row in df_pd_freq.nlargest(5, 'positive_bias').iterrows():
    print(f"    Day {row['personal_day']:2}  {row['positive_bias']:6.2f}% in positive range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP PERSONAL DAYS - STRONGEST -2 BIAS (negative skew):")
for idx, row in df_pd_freq.nlargest(5, 'negative_bias').iterrows():
    print(f"    Day {row['personal_day']:2}  {row['negative_bias']:6.2f}% in negative range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP PERSONAL DAYS - STRONGEST STRONG POSITIVE BIAS (+2 to +6+):")
for idx, row in df_pd_freq.nlargest(5, 'strong_positive').iterrows():
    print(f"    Day {row['personal_day']:2}  {row['strong_positive']:6.2f}% in +2 to +6+ range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

print()
print("  TOP PERSONAL DAYS - STRONGEST STRONG NEGATIVE BIAS (-6 to -2):")
for idx, row in df_pd_freq.nlargest(5, 'strong_negative').iterrows():
    print(f"    Day {row['personal_day']:2}  {row['strong_negative']:6.2f}% in -6 to -2 range | "
          f"mean={row['mean_metric']:+6.3f} | n={row['count']:5,}")

# ============================================================================
# SAVE OUTPUT FILES
# ============================================================================
print()
print("=" * 80)
print("SAVING OUTPUT FILES")
print("=" * 80)

# 1. Summary table
summary_table = {
    'Metric': list(summary_data.keys()),
    'Value': list(summary_data.values())
}
df_summary = pd.DataFrame(summary_table)
output_path_1 = f"{OUTPUT_DIR}/analysis_color_personalday_filtered.csv"
df_summary.to_csv(output_path_1, index=False)
print(f"[OK] {output_path_1}")

# 2. By-color frequency
output_path_2 = f"{OUTPUT_DIR}/frequency_by_color.csv"
df_color_freq.to_csv(output_path_2, index=False)
print(f"[OK] {output_path_2}")

# 3. By-personal-day frequency
output_path_3 = f"{OUTPUT_DIR}/frequency_by_personalday.csv"
df_pd_freq.to_csv(output_path_3, index=False)
print(f"[OK] {output_path_3}")

print()
print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
