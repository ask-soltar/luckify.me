"""
SYSTEM: Round Type × Western Moon (8-cat) × Horoscope × Condition
Tests Western lunar cycle + Western astrological identity
"""

import pandas as pd
import numpy as np

df = pd.read_csv('ANALYSIS_v3_export.csv')

# Filter and prepare
df = df[df['tournament_type'] == 'S'].copy()
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['model_error'] = df['off_par'] - df['adj_his_par']

# Check available columns
print("Checking available columns...")
moonwest_col = None
horoscope_col = None

for col in df.columns:
    if 'moonwest' in col.lower():
        moonwest_col = col
    if 'horoscope' in col.lower():
        horoscope_col = col

print(f"Using Western moon column: {moonwest_col}")
print(f"Using horoscope column: {horoscope_col}")

if not moonwest_col or not horoscope_col:
    print("ERROR: Could not find moonwest or horoscope columns")
    available = [c for c in df.columns if any(x in c.lower() for x in ['moon', 'horoscope'])]
    print(f"Available: {available}")
    exit(1)

df = df.dropna(subset=['off_par', 'adj_his_par', 'condition', 'round_type', moonwest_col, horoscope_col])

print("="*130)
print(f"SYSTEM: Round Type × {moonwest_col} × {horoscope_col} × Condition")
print("="*130)

# Calculate stats
all_combos = []
for condition in ['Calm', 'Moderate', 'Tough']:
    data = df[df['condition'] == condition].copy()

    for rt in data['round_type'].dropna().unique():
        if rt in ['REMOVE', 'Mixed', 'Elimination']:
            continue

        for moonwest in data[moonwest_col].dropna().unique():
            for horoscope in data[horoscope_col].dropna().unique():

                mask = (
                    (data['round_type'] == rt) &
                    (data[moonwest_col] == moonwest) &
                    (data[horoscope_col] == horoscope)
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
                    'moonwest': moonwest,
                    'horoscope': horoscope,
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
    print(f"{'ROI':>6} {'N':>4} {'Edge':>6} {'Conf':>12} {'Round':<12} {'MoonWest':<15} {'Horoscope':<12} {'Condition':<10}")
    print("-"*130)

    for _, r in positive.head(25).iterrows():
        print(f"{r['roi']:>5.1f}% {r['n']:>4} {r['edge']:>5.1f}% {r['conf']:>12} {r['round_type']:<12} {str(r['moonwest']):<15} {str(r['horoscope']):<12} {r['condition']:<10}")

    # Save ALL combos
    df_combos_sorted = df_combos.reindex(df_combos['roi'].abs().sort_values(ascending=False).index)
    df_combos_sorted.to_csv('system_western_moon_horoscope_ALL_combos.csv', index=False)
    print(f"\n[OK] Results saved to: system_western_moon_horoscope_ALL_combos.csv")

    # Save positive-only
    positive.to_csv('system_western_moon_horoscope_positive_only.csv', index=False)

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

    # Save ALL combos anyway
    df_combos_sorted = df_combos.reindex(df_combos['roi'].abs().sort_values(ascending=False).index)
    df_combos_sorted.to_csv('system_western_moon_horoscope_ALL_combos.csv', index=False)
    print(f"\n[OK] Results saved to: system_western_moon_horoscope_ALL_combos.csv")
