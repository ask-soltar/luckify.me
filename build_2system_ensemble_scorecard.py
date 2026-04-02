"""
2-System Ensemble Scorecard Builder
Combines: System 1 (Color × Element) + Western Moon + Horoscope
Game theory approach: Agreement across orthogonal systems = conviction
"""

import pandas as pd
import numpy as np

print("\n" + "="*120)
print("2-SYSTEM ENSEMBLE SCORECARD BUILDER")
print("="*120)

# Load both system results
print("\nLoading system results...")

try:
    df_s1 = pd.read_csv('combo_scoring_rce_all_combos.csv')
    print(f"  System 1 (Color×Element): {len(df_s1)} combos")
except FileNotFoundError:
    print("  ERROR: System 1 file not found")
    exit(1)

try:
    df_s2 = pd.read_csv('system_western_moon_horoscope_ALL_combos.csv')
    print(f"  System 2 (Western Moon×Horoscope): {len(df_s2)} combos")
except FileNotFoundError:
    print("  ERROR: System 2 file not found")
    exit(1)

# Calculate system-level statistics
print("\n" + "="*120)
print("SYSTEM STATISTICS")
print("="*120)

print(f"\nSystem 1 (Color × Element):")
print(f"  Total combos: {len(df_s1)}")
print(f"  Positive: {len(df_s1[df_s1['edge'] > 0])} ({len(df_s1[df_s1['edge'] > 0])/len(df_s1)*100:.1f}%)")
print(f"  Mean edge: {df_s1['edge'].mean():.2f}%")
print(f"  Mean ROI: {df_s1.get('roi', df_s1.get('adjusted_roi', pd.Series())).mean() if 'roi' in df_s1.columns or 'adjusted_roi' in df_s1.columns else 'N/A'}")
s1_roi_col = 'roi' if 'roi' in df_s1.columns else 'adjusted_roi'
print(f"  Using ROI column: {s1_roi_col}")
print(f"  Std dev: {df_s1[s1_roi_col].std():.2f}%")

print(f"\nSystem 2 (Western Moon × Horoscope):")
print(f"  Total combos: {len(df_s2)}")
print(f"  Positive: {len(df_s2[df_s2['roi'] > 0])} ({len(df_s2[df_s2['roi'] > 0])/len(df_s2)*100:.1f}%)")
print(f"  Mean edge: {df_s2['edge'].mean():.2f}%")
print(f"  Mean ROI: {df_s2['roi'].mean():.2f}%")
print(f"  Std dev: {df_s2['roi'].std():.2f}%")

# Build consensus by base (Condition × Round Type)
print("\n" + "="*120)
print("BUILDING ENSEMBLE CONSENSUS BY BASE COMBINATION")
print("="*120)

consensus_results = []

# Get unique bases
bases = set()
for _, row in df_s1.iterrows():
    bases.add((row['condition'], row['round_type']))
for _, row in df_s2.iterrows():
    bases.add((row['condition'], row['round_type']))

bases = sorted(list(bases))
print(f"\nAnalyzing {len(bases)} base combinations (Condition × Round Type)\n")

for condition, round_type in bases:
    # Get combos for each system at this base
    s1_combos = df_s1[(df_s1['condition'] == condition) & (df_s1['round_type'] == round_type)]
    s2_combos = df_s2[(df_s2['condition'] == condition) & (df_s2['round_type'] == round_type)]

    if len(s1_combos) == 0 or len(s2_combos) == 0:
        continue

    # Get best combos from each system
    s1_best = s1_combos[s1_combos[s1_roi_col] == s1_combos[s1_roi_col].max()].iloc[0] if len(s1_combos) > 0 else None
    s2_best = s2_combos[s2_combos['roi'] == s2_combos['roi'].max()].iloc[0] if len(s2_combos) > 0 else None

    s1_roi = s1_best[s1_roi_col] if s1_best is not None else np.nan
    s2_roi = s2_best['roi'] if s2_best is not None else np.nan
    s1_n = s1_best['n'] if s1_best is not None else 0
    s2_n = s2_best['n'] if s2_best is not None else 0

    # Check agreement (both positive)
    both_positive = (s1_roi > 0) and (s2_roi > 0)
    s1_positive = s1_roi > 0
    s2_positive = s2_roi > 0
    positive_count = sum([s1_positive, s2_positive])

    # Calculate ensemble ROI (weighted by sample size)
    if not np.isnan(s1_roi) and not np.isnan(s2_roi):
        # Inverse variance weighting: weight by (n / std_dev^2)
        s1_weight = s1_n / (df_s1[s1_roi_col].std() ** 2 + 1e-6)
        s2_weight = s2_n / (df_s2['roi'].std() ** 2 + 1e-6)
        total_weight = s1_weight + s2_weight

        ensemble_roi = (s1_roi * s1_weight + s2_roi * s2_weight) / total_weight
    else:
        ensemble_roi = np.nan

    # Determine conviction level
    if both_positive:
        conviction = "VERY HIGH (2/2)"
    elif positive_count == 1:
        conviction = "MEDIUM (1/2)"
    else:
        conviction = "LOW (0/2)"

    # Recommendation
    if both_positive:
        recommendation = "BET FOR (Strong)"
    elif positive_count == 1:
        recommendation = "CONDITIONAL"
    else:
        recommendation = "AVOID"

    # Get sample size info
    total_sample = len(s1_combos) + len(s2_combos)

    consensus_results.append({
        'condition': condition,
        'round_type': round_type,
        's1_best_roi': s1_roi,
        's1_best_n': s1_n,
        's2_best_roi': s2_roi,
        's2_best_n': s2_n,
        'both_positive': both_positive,
        'positive_systems': positive_count,
        'ensemble_roi': ensemble_roi,
        'conviction': conviction,
        'recommendation': recommendation,
        's1_combos_total': len(s1_combos),
        's2_combos_total': len(s2_combos),
    })

# Convert to DataFrame and sort by ensemble ROI
df_consensus = pd.DataFrame(consensus_results)
df_consensus_sorted = df_consensus.sort_values('ensemble_roi', ascending=False, na_position='last')

# Print results
print(f"{'Ensemble':>8} {'Conv':>15} {'Round':<12} {'Condition':<10} {'Sys1 ROI':>8} {'Sys2 ROI':>8} {'Sys1 N':>5} {'Sys2 N':>5}")
print("-"*110)

for _, row in df_consensus_sorted.iterrows():
    if pd.isna(row['ensemble_roi']):
        continue
    sign = "+" if row['ensemble_roi'] > 0 else ""
    s1_sign = "+" if row['s1_best_roi'] > 0 else ""
    s2_sign = "+" if row['s2_best_roi'] > 0 else ""

    print(f"{sign}{row['ensemble_roi']:>7.1f}% {row['conviction']:<15} {row['round_type']:<12} {row['condition']:<10} {s1_sign}{row['s1_best_roi']:>7.1f}% {s2_sign}{row['s2_best_roi']:>7.1f}% {row['s1_best_n']:>5.0f} {row['s2_best_n']:>5.0f}")

# Save full results
df_consensus_sorted.to_csv('ensemble_2system_scorecard_all.csv', index=False)
print(f"\n[OK] Saved all combos to: ensemble_2system_scorecard_all.csv")

# Filter for high/medium conviction
df_high = df_consensus_sorted[df_consensus_sorted['positive_systems'] >= 1]
if len(df_high) > 0:
    df_high.to_csv('ensemble_2system_scorecard_high.csv', index=False)
    print(f"[OK] Saved high/medium conviction to: ensemble_2system_scorecard_high.csv ({len(df_high)} combos)")

# Filter for VERY HIGH conviction (both systems agree)
df_very_high = df_consensus_sorted[df_consensus_sorted['both_positive'] == True]
if len(df_very_high) > 0:
    df_very_high.to_csv('ensemble_2system_scorecard_very_high.csv', index=False)
    print(f"[OK] Saved VERY HIGH conviction to: ensemble_2system_scorecard_very_high.csv ({len(df_very_high)} combos)")

# Generate markdown betting guide
print("\n" + "="*120)
print("BETTING RECOMMENDATIONS")
print("="*120 + "\n")

print("## BET FOR (Very High Conviction - Both Systems Agree)\n")
if len(df_very_high) > 0:
    for _, row in df_very_high.sort_values('ensemble_roi', ascending=False).iterrows():
        print(f"### {row['condition']} × {row['round_type']}")
        print(f"- **Ensemble ROI:** +{row['ensemble_roi']:.1f}%")
        print(f"- **System 1:** +{row['s1_best_roi']:.1f}% (N={row['s1_best_n']:.0f})")
        print(f"- **System 2:** +{row['s2_best_roi']:.1f}% (N={row['s2_best_n']:.0f})")
        print(f"- **Action:** Deploy with full sizing\n")
else:
    print("No very high conviction signals found.\n")

print("\n## CONDITIONAL (Medium Conviction - One System Agrees)\n")
df_medium = df_consensus_sorted[(df_consensus_sorted['positive_systems'] == 1) & (df_consensus_sorted['positive_systems'] != 0)]
if len(df_medium) > 0:
    for _, row in df_medium.sort_values('ensemble_roi', ascending=False).head(10).iterrows():
        print(f"### {row['condition']} × {row['round_type']}")
        if row['s1_best_roi'] > 0:
            print(f"- **System 1:** +{row['s1_best_roi']:.1f}% (N={row['s1_best_n']:.0f})")
            print(f"- **System 2:** {row['s2_best_roi']:+.1f}%")
        else:
            print(f"- **System 1:** {row['s1_best_roi']:+.1f}%")
            print(f"- **System 2:** +{row['s2_best_roi']:.1f}% (N={row['s2_best_n']:.0f})")
        print(f"- **Ensemble ROI:** {row['ensemble_roi']:+.1f}%")
        print(f"- **Action:** Deploy at reduced sizing\n")
else:
    print("No medium conviction signals found.\n")

# Summary statistics
print("\n" + "="*120)
print("SUMMARY STATISTICS")
print("="*120 + "\n")

print(f"Total base combinations analyzed: {len(df_consensus)}")
print(f"Very High conviction (2/2): {len(df_very_high)}")
print(f"Medium conviction (1/2): {len(df_medium)}")
print(f"Low conviction (0/2): {len(df_consensus[df_consensus['positive_systems'] == 0])}")

if len(df_very_high) > 0:
    print(f"\nVery High Conviction Stats:")
    print(f"  Mean ensemble ROI: {df_very_high['ensemble_roi'].mean():+.1f}%")
    print(f"  Best ensemble ROI: {df_very_high['ensemble_roi'].max():+.1f}%")
    print(f"  Median ensemble ROI: {df_very_high['ensemble_roi'].median():+.1f}%")

if len(df_high) > 0:
    print(f"\nHigh + Medium Conviction Stats:")
    print(f"  Mean ensemble ROI: {df_high['ensemble_roi'].mean():+.1f}%")
    print(f"  Best ensemble ROI: {df_high['ensemble_roi'].max():+.1f}%")

print("\n[OK] 2-System ensemble scorecard complete!")
