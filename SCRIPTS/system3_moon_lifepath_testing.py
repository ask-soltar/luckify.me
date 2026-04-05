"""
SYSTEM 3 Testing: Round Type × Moon Phase (10-cat) × Life Path × Condition
Tests celestial timing + personal destiny signals
"""

import pandas as pd
import numpy as np

df = pd.read_csv('ANALYSIS_v3_export.csv')

# Filter and prepare
df = df[df['tournament_type'] == 'S'].copy()
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['model_error'] = df['off_par'] - df['adj_his_par']

# Check available columns for moon and life path
# From our previous work: moon_10c or moon, life_path
print("Checking available columns...")
print(f"Columns: {[c for c in df.columns if 'moon' in c.lower() or 'life' in c.lower()]}")

# Use the column that exists
moon_col = None
for col in df.columns:
    if 'moon' in col.lower() and '10' in col.lower():
        moon_col = col
        break
if not moon_col:
    # Try generic moon
    for col in df.columns:
        if col == 'moon':
            moon_col = col
            break

life_col = None
for col in df.columns:
    if 'life' in col.lower() and 'path' in col.lower():
        life_col = col
        break

print(f"Using moon column: {moon_col}")
print(f"Using life path column: {life_col}")

if not moon_col or not life_col:
    print("ERROR: Could not find moon or life_path columns")
    print(f"Available columns: {df.columns.tolist()}")
    exit(1)

df = df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', moon_col, life_col])

print("="*130)
print(f"SYSTEM 3: Round Type × {moon_col} × {life_col} × Condition")
print("="*130)

# Calculate stats
all_combos = []
for condition in ['Calm', 'Moderate', 'Tough']:
    data = df[df['condition'] == condition].copy()

    for rt in data['round_type'].dropna().unique():
        if rt in ['REMOVE', 'Mixed', 'Elimination']:
            continue

        for moon in data[moon_col].dropna().unique():
            for life_path in data[life_col].dropna().unique():

                mask = (
                    (data['round_type'] == rt) &
                    (data[moon_col] == moon) &
                    (data[life_col] == life_path)
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

                # Bayesian shrinkage ROI
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
                    'moon': moon,
                    'life_path': life_path,
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
if len(positive) > 0:
    print(f"Average positive ROI: {positive['roi'].mean():.1f}%")
    print(f"\nTOP 25 COMBINATIONS (Positive ROI):")
    print("-"*130)
    print(f"{'ROI':>6} {'N':>4} {'Edge':>6} {'Conf':>12} {'Round':<12} {'Moon':>8} {'Life Path':>10} {'Condition':<10}")
    print("-"*130)

    for _, r in positive.head(25).iterrows():
        print(f"{r['roi']:>5.1f}% {r['n']:>4} {r['edge']:>5.1f}% {r['conf']:>12} {r['round_type']:<12} {str(r['moon']):>8} {str(r['life_path']):>10} {r['condition']:<10}")

    # Save ALL combos (positive, negative, zero)
    df_combos_sorted = df_combos.reindex(df_combos['roi'].abs().sort_values(ascending=False).index)
    df_combos_sorted.to_csv('system3_moon_lifepath_ALL_combos.csv', index=False)
    print(f"\n[OK] Results saved to: system3_moon_lifepath_ALL_combos.csv")

    # Save positive-only for comparison
    positive.to_csv('system3_moon_lifepath_positive_only.csv', index=False)

    # Summary by condition
    print(f"\n\nBY CONDITION (Positive ROI only):")
    print("-"*60)
    for cond in ['Calm', 'Moderate', 'Tough']:
        subset = positive[positive['condition'] == cond]
        if len(subset) > 0:
            print(f"  {cond:<10}: {len(subset):>3} combos | Avg ROI: {subset['roi'].mean():>6.1f}% | Best: {subset['roi'].max():>6.1f}%")
        else:
            print(f"  {cond:<10}: NO POSITIVE ROI")
else:
    print("\nNO POSITIVE ROI COMBOS FOUND")
    print("Showing top 25 by edge (including negative):")
    print("-"*130)
    top = df_combos.sort_values('edge', ascending=False).head(25)
    for _, r in top.iterrows():
        print(f"{r['roi']:>5.1f}% ROI | {r['edge']:>5.1f}% edge | {r['round_type']:<12} × Moon {str(r['moon']):>8} × Life Path {str(r['life_path']):>3} ({r['condition']:<10}) | N={r['n']:>3}")

