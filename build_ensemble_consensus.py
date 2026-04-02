"""
Ensemble Consensus Scorer — Combines 4 independent systems
Tests base combination agreement: Condition × Round Type

Systems:
1. Color × Element
2. Exec × Upside × Gap
3. Moon × Life Path
4. Tithi × Zodiac

Output:
- ensemble_consensus_scorecard.csv — Full results by base combo
- ensemble_high_conviction.csv — 4/4 and 3/4 agreement
- ensemble_betting_recommendations.md — Actionable signals
"""

import pandas as pd
import numpy as np
from collections import defaultdict

# Load all system results
print("Loading system results...")

try:
    df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')
    print(f"  System 1 (Color×Element): {len(df_s1)} combos")
except FileNotFoundError:
    print("  ERROR: System 1 file not found (combo_scoring_rce_all_combos.csv)")
    df_s1 = None

try:
    df_s2 = pd.read_csv('system2_exec_upside_gap_ALL_combos.csv')
    print(f"  System 2 (Exec×Upside×Gap): {len(df_s2)} combos")
except FileNotFoundError:
    print("  ERROR: System 2 file not found")
    df_s2 = None

try:
    df_s3 = pd.read_csv('system3_moon_lifepath_ALL_combos.csv')
    print(f"  System 3 (Moon×LifePath): {len(df_s3)} combos")
except FileNotFoundError:
    print("  ERROR: System 3 file not found")
    df_s3 = None

try:
    df_s4 = pd.read_csv('system4_tithi_zodiac_ALL_combos.csv')
    print(f"  System 4 (Tithi×Zodiac): {len(df_s4)} combos")
except FileNotFoundError:
    print("  ERROR: System 4 file not found")
    df_s4 = None

if not all([df_s1 is not None, df_s2 is not None, df_s3 is not None, df_s4 is not None]):
    print("\nERROR: Not all system results available. Run testing scripts first:")
    print("  python system2_exec_upside_gap_testing.py")
    print("  python system3_moon_lifepath_testing.py")
    print("  python system4_tithi_zodiac_testing.py")
    exit(1)

# Aggregate by base (condition, round_type)
print("\n" + "="*100)
print("ENSEMBLE CONSENSUS SCORECARD")
print("="*100)

consensus_results = []

# Get unique base combinations
base_combinations = set()
for df in [df_s1, df_s2, df_s3, df_s4]:
    for _, row in df.iterrows():
        base_combinations.add((row['condition'], row['round_type']))

base_combinations = sorted(list(base_combinations))
print(f"\nAnalyzing {len(base_combinations)} base combinations (Condition × Round Type)\n")

for condition, round_type in base_combinations:
    # Get combos for each system at this base
    s1_combos = df_s1[(df_s1['condition'] == condition) & (df_s1['round_type'] == round_type)]
    s2_combos = df_s2[(df_s2['condition'] == condition) & (df_s2['round_type'] == round_type)]
    s3_combos = df_s3[(df_s3['condition'] == condition) & (df_s3['round_type'] == round_type)]
    s4_combos = df_s4[(df_s4['condition'] == condition) & (df_s4['round_type'] == round_type)]

    # Calculate system statistics
    s1_has_positive = len(s1_combos[s1_combos['roi'] > 0]) > 0
    s2_has_positive = len(s2_combos[s2_combos['roi'] > 0]) > 0
    s3_has_positive = len(s3_combos[s3_combos['roi'] > 0]) > 0
    s4_has_positive = len(s4_combos[s4_combos['roi'] > 0]) > 0

    positive_count = sum([s1_has_positive, s2_has_positive, s3_has_positive, s4_has_positive])

    # System ROI metrics (use best positive combo per system, or median if all negative)
    def get_system_roi(df):
        if len(df) == 0:
            return np.nan
        positive = df[df['roi'] > 0]
        if len(positive) > 0:
            return positive['roi'].max()
        else:
            return df['roi'].median()

    s1_roi = get_system_roi(s1_combos)
    s2_roi = get_system_roi(s2_combos)
    s3_roi = get_system_roi(s3_combos)
    s4_roi = get_system_roi(s4_combos)

    # Calculate ensemble ROI (weighted by sample size)
    valid_rois = []
    total_n = 0
    for roi, combos in [(s1_roi, s1_combos), (s2_roi, s2_combos), (s3_roi, s3_combos), (s4_roi, s4_combos)]:
        if not np.isnan(roi) and len(combos) > 0:
            avg_n = combos['n'].mean()
            total_n += avg_n
            valid_rois.append((roi, avg_n))

    if valid_rois:
        ensemble_roi = sum(roi * n for roi, n in valid_rois) / sum(n for _, n in valid_rois)
    else:
        ensemble_roi = np.nan

    # Determine conviction level
    if positive_count == 4:
        conviction = "HIGH (4/4)"
    elif positive_count == 3:
        conviction = "MEDIUM (3/4)"
    elif positive_count == 2:
        conviction = "WEAK (2/4)"
    else:
        conviction = "LOW (0-1/4)"

    # Recommendation
    if positive_count >= 3:
        recommendation = "BET FOR"
    elif positive_count == 2:
        recommendation = "CONDITIONAL"
    else:
        recommendation = "SKIP/SHORT"

    # Total sample size across systems
    total_sample = len(s1_combos) + len(s2_combos) + len(s3_combos) + len(s4_combos)

    consensus_results.append({
        'condition': condition,
        'round_type': round_type,
        'positive_systems': positive_count,
        's1_best_roi': s1_roi,
        's2_best_roi': s2_roi,
        's3_best_roi': s3_roi,
        's4_best_roi': s4_roi,
        'ensemble_roi': ensemble_roi,
        'conviction': conviction,
        'recommendation': recommendation,
        'total_sample': total_sample
    })

# Convert to DataFrame and sort
df_consensus = pd.DataFrame(consensus_results)
df_consensus_sorted = df_consensus.sort_values('ensemble_roi', ascending=False)

# Print results
print(f"{'ROI':>6} {'Pos':>3} {'Conviction':<15} {'Round':<12} {'Condition':<10} {'Sys1':>6} {'Sys2':>6} {'Sys3':>6} {'Sys4':>6} {'N':>5}")
print("-"*100)

for _, row in df_consensus_sorted.iterrows():
    sign = "+" if row['ensemble_roi'] > 0 else ""
    s1 = f"{row['s1_best_roi']:>5.1f}%" if not np.isnan(row['s1_best_roi']) else "  — "
    s2 = f"{row['s2_best_roi']:>5.1f}%" if not np.isnan(row['s2_best_roi']) else "  — "
    s3 = f"{row['s3_best_roi']:>5.1f}%" if not np.isnan(row['s3_best_roi']) else "  — "
    s4 = f"{row['s4_best_roi']:>5.1f}%" if not np.isnan(row['s4_best_roi']) else "  — "

    print(f"{sign}{row['ensemble_roi']:>5.1f}% {row['positive_systems']:>3} {row['conviction']:<15} {row['round_type']:<12} {row['condition']:<10} {s1} {s2} {s3} {s4} {row['total_sample']:>5.0f}")

# Save results
df_consensus_sorted.to_csv('ensemble_consensus_scorecard.csv', index=False)
print(f"\n[OK] Saved all combos to: ensemble_consensus_scorecard.csv")

# Filter for high/medium conviction
df_high_conviction = df_consensus_sorted[df_consensus_sorted['positive_systems'] >= 3]
if len(df_high_conviction) > 0:
    df_high_conviction.to_csv('ensemble_high_conviction.csv', index=False)
    print(f"[OK] Saved {len(df_high_conviction)} high/medium conviction combos to: ensemble_high_conviction.csv")
else:
    print("[WARNING] No high/medium conviction combos found")

# Generate markdown recommendations
print("\n" + "="*100)
print("ENSEMBLE BETTING RECOMMENDATIONS")
print("="*100 + "\n")

if len(df_high_conviction) > 0:
    print("## BET FOR (High Confidence)")
    print()
    for _, row in df_high_conviction[df_high_conviction['recommendation'] == 'BET FOR'].iterrows():
        print(f"### {row['condition']} × {row['round_type']}")
        print(f"- **Ensemble ROI:** +{row['ensemble_roi']:.1f}%")
        print(f"- **Agreement:** {row['conviction']}")
        print(f"- **System signals:** ")
        if not np.isnan(row['s1_best_roi']):
            print(f"  - System 1 (Color×Element): +{row['s1_best_roi']:.1f}%")
        if not np.isnan(row['s2_best_roi']):
            print(f"  - System 2 (Exec×Upside): +{row['s2_best_roi']:.1f}%")
        if not np.isnan(row['s3_best_roi']):
            print(f"  - System 3 (Moon×LifePath): +{row['s3_best_roi']:.1f}%")
        if not np.isnan(row['s4_best_roi']):
            print(f"  - System 4 (Tithi×Zodiac): +{row['s4_best_roi']:.1f}%")
        print(f"- **Action:** Deploy with full sizing")
        print()

    conditional = df_high_conviction[df_high_conviction['recommendation'] == 'CONDITIONAL']
    if len(conditional) > 0:
        print("\n## CONDITIONAL (Medium Confidence)")
        print()
        for _, row in conditional.iterrows():
            print(f"### {row['condition']} × {row['round_type']}")
            print(f"- **Ensemble ROI:** {row['ensemble_roi']:+.1f}%")
            print(f"- **Agreement:** {row['conviction']}")
            print(f"- **Action:** Deploy at reduced sizing")
            print()
else:
    print("No high-conviction signals found. Review system results.")

print("\n[OK] Ensemble consensus analysis complete!")
