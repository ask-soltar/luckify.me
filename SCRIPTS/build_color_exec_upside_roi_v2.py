"""
Rebuild Color × Exec and Color × Upside ROI Tables
From ANALYSIS v3 with: Condition, Round Type, Tournament Type, Color
"""

import pandas as pd
import numpy as np

print("\nLoading ANALYSIS v3 data...")
try:
    df = pd.read_csv('ANALYSIS_v3_export.csv')
    print(f"Loaded {len(df)} rows")
except FileNotFoundError:
    print("ERROR: ANALYSIS_v3_export.csv not found")
    exit(1)

# Show columns to verify what we have
print(f"\nColumns available: {list(df.columns)[:30]}...")

# Filter for stroke play only
print("\nFiltering and preparing data...")
df = df[df['tournament_type'] == 'S'].copy()

# Coerce to numeric
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['exec'] = pd.to_numeric(df['exec'], errors='coerce')
df['upside'] = pd.to_numeric(df['upside'], errors='coerce')

# Model error
df['model_error'] = df['off_par'] - df['adj_his_par']

# Drop rows with missing data
df = df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', 'color', 'exec', 'upside'])

print(f"After filtering (stroke play only): {len(df)} rows")

# Bucket exec and upside into 25-point ranges
def bucket_score(score):
    if pd.isna(score):
        return None
    if score < 25:
        return "0-25"
    elif score < 50:
        return "25-50"
    elif score < 75:
        return "50-75"
    else:
        return "75-100"

df['exec_bucket'] = df['exec'].apply(bucket_score)
df['upside_bucket'] = df['upside'].apply(bucket_score)

print("\n" + "="*130)
print("BUILDING COLOR × EXEC ROI TABLE (by Condition, Round Type, Color)")
print("="*130)

# Build Color × Exec Bucket table
exec_combos = []
for condition in sorted(df['condition'].unique()):
    for rt in sorted(df[df['condition']==condition]['round_type'].unique()):
        for color in sorted(df[(df['condition']==condition) & (df['round_type']==rt)]['color'].unique()):
            for exec_b in ["0-25", "25-50", "50-75", "75-100"]:
                mask = (
                    (df['condition'] == condition) &
                    (df['round_type'] == rt) &
                    (df['color'] == color) &
                    (df['exec_bucket'] == exec_b)
                )
                subset = df[mask]

                if len(subset) < 2:
                    continue

                good = len(subset[subset['model_error'] <= -2.0])
                bad = len(subset[subset['model_error'] >= 2.0])
                total = len(subset)

                good_rate = good / total * 100
                bad_rate = bad / total * 100
                edge = good_rate - bad_rate

                # Bayesian shrinkage ROI
                roi = edge * (total / (total + 50))

                if total >= 30:
                    conf = 'HIGH'
                elif total >= 15:
                    conf = 'EXPLORATORY'
                else:
                    conf = 'WEAK'

                exec_combos.append({
                    'condition': condition,
                    'round_type': rt,
                    'color': color,
                    'exec_bucket': exec_b,
                    'n': total,
                    'good': good,
                    'bad': bad,
                    'good_rate': good_rate,
                    'bad_rate': bad_rate,
                    'edge': edge,
                    'roi': roi,
                    'confidence': conf,
                    'mean_error': subset['model_error'].mean()
                })

df_exec = pd.DataFrame(exec_combos)
df_exec = df_exec.sort_values('roi', ascending=False)

print(f"\nTotal Color × Exec combos: {len(df_exec)}")
print(f"Positive ROI: {len(df_exec[df_exec['roi'] > 0])}")
print(f"Mean ROI: {df_exec['roi'].mean():.2f}%")

print(f"\nTop 15 Color × Exec combos:")
print(df_exec[['condition', 'round_type', 'color', 'exec_bucket', 'n', 'roi', 'confidence']].head(15).to_string())

df_exec.to_csv('color_exec_bucket_roi_v2.csv', index=False)
print(f"\n[OK] Saved to: color_exec_bucket_roi_v2.csv")

# Build Color × Upside Bucket table
print("\n" + "="*130)
print("BUILDING COLOR × UPSIDE ROI TABLE (by Condition, Round Type, Color)")
print("="*130)

upside_combos = []
for condition in sorted(df['condition'].unique()):
    for rt in sorted(df[df['condition']==condition]['round_type'].unique()):
        for color in sorted(df[(df['condition']==condition) & (df['round_type']==rt)]['color'].unique()):
            for upside_b in ["0-25", "25-50", "50-75", "75-100"]:
                mask = (
                    (df['condition'] == condition) &
                    (df['round_type'] == rt) &
                    (df['color'] == color) &
                    (df['upside_bucket'] == upside_b)
                )
                subset = df[mask]

                if len(subset) < 2:
                    continue

                good = len(subset[subset['model_error'] <= -2.0])
                bad = len(subset[subset['model_error'] >= 2.0])
                total = len(subset)

                good_rate = good / total * 100
                bad_rate = bad / total * 100
                edge = good_rate - bad_rate

                # Bayesian shrinkage ROI
                roi = edge * (total / (total + 50))

                if total >= 30:
                    conf = 'HIGH'
                elif total >= 15:
                    conf = 'EXPLORATORY'
                else:
                    conf = 'WEAK'

                upside_combos.append({
                    'condition': condition,
                    'round_type': rt,
                    'color': color,
                    'upside_bucket': upside_b,
                    'n': total,
                    'good': good,
                    'bad': bad,
                    'good_rate': good_rate,
                    'bad_rate': bad_rate,
                    'edge': edge,
                    'roi': roi,
                    'confidence': conf,
                    'mean_error': subset['model_error'].mean()
                })

df_upside = pd.DataFrame(upside_combos)
df_upside = df_upside.sort_values('roi', ascending=False)

print(f"\nTotal Color × Upside combos: {len(df_upside)}")
print(f"Positive ROI: {len(df_upside[df_upside['roi'] > 0])}")
print(f"Mean ROI: {df_upside['roi'].mean():.2f}%")

print(f"\nTop 15 Color × Upside combos:")
print(df_upside[['condition', 'round_type', 'color', 'upside_bucket', 'n', 'roi', 'confidence']].head(15).to_string())

df_upside.to_csv('color_upside_bucket_roi_v2.csv', index=False)
print(f"\n[OK] Saved to: color_upside_bucket_roi_v2.csv")

# Summary
print("\n" + "="*130)
print("SUMMARY")
print("="*130)
print(f"\nColor × Exec Bucket ROI table: {len(df_exec)} combos (mean ROI: {df_exec['roi'].mean():.2f}%)")
print(f"Color × Upside Bucket ROI table: {len(df_upside)} combos (mean ROI: {df_upside['roi'].mean():.2f}%)")

print("\n[OK] Tables ready for matchup screener")
