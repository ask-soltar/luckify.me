"""
Detailed Betting Guide
Extracts specific combos (not just base aggregates) from each system
Shows exact Color+Element and Moon+Horoscope combinations to bet on
"""

import pandas as pd
import numpy as np

print("\n" + "="*140)
print("DETAILED BETTING GUIDE — SPECIFIC COMBOS BY BASE")
print("="*140)

# Load both system results
df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')
df_s2 = pd.read_csv('system_western_moon_horoscope_ALL_combos.csv')

# Load base scorecard for ranking
df_base = pd.read_csv('ensemble_2system_scorecard_very_high.csv').sort_values('ensemble_roi', ascending=False)

# For each base, extract top 5 combos from each system
detailed_results = []

for idx, base_row in df_base.iterrows():
    condition = base_row['condition']
    round_type = base_row['round_type']
    ensemble_roi = base_row['ensemble_roi']

    print(f"\n{'='*140}")
    print(f"BASE: {condition} × {round_type} | Ensemble ROI: +{ensemble_roi:.1f}%")
    print(f"{'='*140}")

    # System 1 top combos for this base
    s1_base = df_s1[(df_s1['condition'] == condition) & (df_s1['round_type'] == round_type)]
    s1_top = s1_base.nlargest(5, 'adjusted_roi')

    print(f"\nSYSTEM 1 (Color × Element) — Top 5:")
    print(f"{'ROI':>6} {'N':>4} {'Color':<10} {'Element':<10} {'Confidence':<12}")
    print("-"*50)
    for _, row in s1_top.iterrows():
        print(f"{row['adjusted_roi']:>5.1f}% {row['n']:>4} {str(row['color']):<10} {str(row['element']):<10} {row['confidence']:<12}")
        detailed_results.append({
            'condition': condition,
            'round_type': round_type,
            'ensemble_roi': ensemble_roi,
            'system': 'System 1',
            'dim1': row['color'],
            'dim2': row['element'],
            'system_roi': row['adjusted_roi'],
            'n': row['n'],
            'confidence': row['confidence']
        })

    # System 2 top combos for this base
    s2_base = df_s2[(df_s2['condition'] == condition) & (df_s2['round_type'] == round_type)]
    s2_top = s2_base.nlargest(5, 'roi')

    print(f"\nSYSTEM 2 (Western Moon × Horoscope) — Top 5:")
    print(f"{'ROI':>6} {'N':>4} {'Moon':<15} {'Horoscope':<12} {'Confidence':<12}")
    print("-"*50)
    for _, row in s2_top.iterrows():
        print(f"{row['roi']:>5.1f}% {row['n']:>4} {str(row['moonwest']):<15} {str(row['horoscope']):<12} {row['conf']:<12}")
        detailed_results.append({
            'condition': condition,
            'round_type': round_type,
            'ensemble_roi': ensemble_roi,
            'system': 'System 2',
            'dim1': row['moonwest'],
            'dim2': row['horoscope'],
            'system_roi': row['roi'],
            'n': row['n'],
            'confidence': row['conf']
        })

# Save detailed results
df_detailed = pd.DataFrame(detailed_results)
df_detailed.to_csv('betting_guide_specific_combos.csv', index=False)
print(f"\n\n[OK] Saved detailed combos to: betting_guide_specific_combos.csv ({len(detailed_results)} specific bets)")

# Summary
print("\n" + "="*140)
print("SUMMARY")
print("="*140)
print(f"\nTotal base signals: {len(df_base)}")
print(f"Total specific combos identified: {len(df_detailed)}")
print(f"  - System 1 (Color×Element): {len(df_detailed[df_detailed['system'] == 'System 1'])} combos")
print(f"  - System 2 (Moon×Horoscope): {len(df_detailed[df_detailed['system'] == 'System 2'])} combos")

print("\nTo deploy:")
print("1. Choose a base signal (e.g., 'Moderate × Positioning')")
print("2. Pick a specific combo from System 1 (e.g., Yellow × Fire)")
print("3. Pick a specific combo from System 2 (e.g., Full Moon × Leo)")
print("4. Both systems agree on the base → high conviction bet")

print("\n[OK] Detailed betting guide complete!")
