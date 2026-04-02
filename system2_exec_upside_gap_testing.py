"""
SYSTEM 2 Testing: Round Type × Exec/Upside × Gap × Condition
Tests player execution quality + momentum signals
"""

import pandas as pd
import numpy as np

df = pd.read_csv('ANALYSIS_v3_export.csv')

# Filter and prepare
df = df[df['tournament_type'] == 'S'].copy()
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['exec'] = pd.to_numeric(df['exec'], errors='coerce')
df['upside'] = pd.to_numeric(df['upside'], errors='coerce')
df['gap'] = pd.to_numeric(df['gap'], errors='coerce')
df['model_error'] = df['off_par'] - df['adj_his_par']
df = df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', 'exec', 'upside', 'gap'])

print("="*130)
print("SYSTEM 2: Round Type × Exec/Upside × Gap × Condition")
print("="*130)

# Define buckets
def bucket_exec(v):
    if pd.isna(v): return None
    if v < 25: return '0-25'
    if v < 50: return '25-50'
    if v < 75: return '50-75'
    return '75-100'

def bucket_upside(v):
    if pd.isna(v): return None
    if v < 25: return '0-25'
    if v < 50: return '25-50'
    if v < 75: return '50-75'
    return '75-100'

def bucket_gap(v):
    if pd.isna(v): return None
    if v >= 20: return '20+'
    if v >= 10: return '10-20'
    if v >= 0: return '0-10'
    if v >= -10: return '-10-0'
    if v >= -20: return '-20--10'
    return '<-20'

df['exec_bucket'] = df['exec'].apply(bucket_exec)
df['upside_bucket'] = df['upside'].apply(bucket_upside)
df['gap_bucket'] = df['gap'].apply(bucket_gap)

# Calculate stats
all_combos = []
for condition in ['Calm', 'Moderate', 'Tough']:
    data = df[df['condition'] == condition].copy()

    for rt in data['round_type'].dropna().unique():
        if rt in ['REMOVE', 'Mixed', 'Elimination']:
            continue

        for exec_b in data['exec_bucket'].dropna().unique():
            for upside_b in data['upside_bucket'].dropna().unique():
                for gap_b in data['gap_bucket'].dropna().unique():

                    mask = (
                        (data['round_type'] == rt) &
                        (data['exec_bucket'] == exec_b) &
                        (data['upside_bucket'] == upside_b) &
                        (data['gap_bucket'] == gap_b)
                    )

                    combo_data = data[mask]
                    if len(combo_data) < 2:
                        continue

                    good = len(combo_data[combo_data['model_error'] <= -2.0])
                    bad = len(combo_data[combo_data['model_error'] >= 2.0])
                    total = len(combo_data)

                    good_rate = good / total
                    bad_rate = bad / total
                    edge = (good_rate - bad_rate) * 100

                    # Bayesian shrinkage ROI (regularization=50)
                    roi = edge * (total / (total + 50))

                    if total >= 30:
                        conf = 'HIGH'
                    elif total >= 15:
                        conf = 'EXPLORATORY'
                    else:
                        conf = 'WEAK'

                    all_combos.append({
                        'condition': condition,
                        'round_type': rt,
                        'exec': exec_b,
                        'upside': upside_b,
                        'gap': gap_b,
                        'n': total,
                        'edge': edge,
                        'roi': roi,
                        'conf': conf,
                        'mean_error': combo_data['model_error'].mean()
                    })

df_combos = pd.DataFrame(all_combos)

# Filter positive ROI
positive = df_combos[df_combos['roi'] > 0].sort_values('roi', ascending=False)

print(f"\nTotal combos tested: {len(df_combos)}")
print(f"Positive ROI combos: {len(positive)} ({len(positive)/len(df_combos)*100:.1f}%)")
print(f"Negative ROI combos: {len(df_combos[df_combos['roi'] < 0])} ({len(df_combos[df_combos['roi'] < 0])/len(df_combos)*100:.1f}%)")
print(f"Zero ROI combos: {len(df_combos[df_combos['roi'] == 0])} ({len(df_combos[df_combos['roi'] == 0])/len(df_combos)*100:.1f}%)")
print(f"Average ROI (all): {df_combos['roi'].mean():.2f}%")
print(f"Average positive ROI: {positive['roi'].mean():.1f}%")
print(f"\nTOP 25 COMBINATIONS (Positive ROI):")
print("-"*130)
print(f"{'ROI':>6} {'N':>4} {'Edge':>6} {'Conf':>12} {'Round':<12} {'Exec':>8} {'Upside':>8} {'Gap':>10} {'Condition':<10}")
print("-"*130)

for _, r in positive.head(25).iterrows():
    print(f"{r['roi']:>5.1f}% {r['n']:>4} {r['edge']:>5.1f}% {r['conf']:>12} {r['round_type']:<12} {r['exec']:>8} {r['upside']:>8} {r['gap']:>10} {r['condition']:<10}")

# Save ALL combos (positive, negative, zero)
df_combos_sorted = df_combos.reindex(df_combos['roi'].abs().sort_values(ascending=False).index)
df_combos_sorted.to_csv('system2_exec_upside_gap_ALL_combos.csv', index=False)
print(f"\n[OK] Results saved to: system2_exec_upside_gap_ALL_combos.csv")

# Save positive-only for comparison
positive.to_csv('system2_exec_upside_gap_positive_only.csv', index=False)

# Summary by condition
print(f"\n\nBY CONDITION (Positive ROI only):")
print("-"*60)
for cond in ['Calm', 'Moderate', 'Tough']:
    subset = positive[positive['condition'] == cond]
    if len(subset) > 0:
        print(f"  {cond:<10}: {len(subset):>3} combos | Avg ROI: {subset['roi'].mean():>6.1f}% | Best: {subset['roi'].max():>6.1f}%")
    else:
        print(f"  {cond:<10}: NO POSITIVE ROI")

