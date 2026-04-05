"""
Orange vs Adjusted Historical Par Analysis
===========================================

Theory: During Orange days, players should beat their OWN adjusted historical par
more often than they beat the field average.

Why? Orange amplifies talent. All PGA players are talented. So:
- vs_avg (field average) measures relative performance (vs other talented players)
- vs adj_his_par measures absolute performance (vs player's own capability)

Orange should show:
- Strong positive vs adj_his_par (player beats own average)
- Moderate negative vs vs_avg (beats field because of talent amplification)

This validates Soltar: Orange = talent amplifier, not luck amplifier
"""

import pandas as pd
import numpy as np
from scipy import stats

print("=" * 80)
print("ORANGE vs ADJUSTED HISTORICAL PAR ANALYSIS")
print("=" * 80)

# Load data
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)

# Ensure numeric columns
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['adj_his_par'] = pd.to_numeric(df['adj_his_par'], errors='coerce')
df['off_par'] = pd.to_numeric(df['off_par'], errors='coerce')

# Filter to Orange + stroke play
df_orange = df[(df['color'] == 'Orange') & (df['tournament_type'].isin(['S', 'NS']))].copy()
df_orange = df_orange[df_orange['round_type'] != 'REMOVE'].copy()

print(f"[OK] Loaded {len(df_orange)} Orange + stroke-play rounds")
print()

# Calculate vs adj_his_par
# CORRECT: adj_his_par - off_par (positive = beat own average)
df_orange['vs_adj_his_par'] = df_orange['adj_his_par'] - df_orange['off_par']

print("=" * 80)
print("KEY METRICS")
print("=" * 80)

# Exclude NaN values
vs_avg_clean = df_orange['vs_avg'].dropna()
vs_adj_hist_clean = df_orange['vs_adj_his_par'].dropna()

print(f"\nvs_avg (vs field average):")
print(f"  Mean: {vs_avg_clean.mean():7.4f}")
print(f"  Std:  {vs_avg_clean.std():7.4f}")
print(f"  Median: {vs_avg_clean.median():7.4f}")
print(f"  Beat field (n): {(vs_avg_clean < 0).sum()} / {len(vs_avg_clean)} ({100*(vs_avg_clean < 0).sum()/len(vs_avg_clean):.1f}%)")

print(f"\nvs_adj_his_par (vs own adjusted average):")
print(f"  Mean: {vs_adj_hist_clean.mean():7.4f}")
print(f"  Std:  {vs_adj_hist_clean.std():7.4f}")
print(f"  Median: {vs_adj_hist_clean.median():7.4f}")
print(f"  Beat own avg (n): {(vs_adj_hist_clean > 0).sum()} / {len(vs_adj_hist_clean)} ({100*(vs_adj_hist_clean > 0).sum()/len(vs_adj_hist_clean):.1f}%)")

# T-tests
t_stat_avg, p_val_avg = stats.ttest_1samp(vs_avg_clean, 0, nan_policy='omit')
t_stat_his, p_val_his = stats.ttest_1samp(vs_adj_hist_clean, 0, nan_policy='omit')

print(f"\nStatistical significance:")
print(f"  vs_avg vs 0: t={t_stat_avg:.4f}, p={p_val_avg:.6f}")
print(f"  vs_adj_his_par vs 0: t={t_stat_his:.4f}, p={p_val_his:.6f}")

# ============================================================================
# BREAKDOWN BY CONDITION
# ============================================================================

print("\n" + "=" * 80)
print("BY CONDITION")
print("=" * 80)

for cond in ['Calm', 'Moderate', 'Tough']:
    df_cond = df_orange[df_orange['condition'] == cond]

    vs_avg_cond = df_cond['vs_avg'].dropna()
    vs_his_cond = df_cond['vs_adj_his_par'].dropna()

    print(f"\n{cond}:")
    print(f"  vs_avg: mean={vs_avg_cond.mean():7.4f}, beat%={100*(vs_avg_cond < 0).sum()/len(vs_avg_cond):5.1f}%")
    print(f"  vs_his: mean={vs_his_cond.mean():7.4f}, beat%={100*(vs_his_cond > 0).sum()/len(vs_his_cond):5.1f}%")

# ============================================================================
# BREAKDOWN BY ROUND TYPE
# ============================================================================

print("\n" + "=" * 80)
print("BY ROUND TYPE")
print("=" * 80)

for rtype in sorted(df_orange['round_type'].dropna().unique()):
    df_rt = df_orange[df_orange['round_type'] == rtype]

    vs_avg_rt = df_rt['vs_avg'].dropna()
    vs_his_rt = df_rt['vs_adj_his_par'].dropna()

    if len(vs_avg_rt) > 30:  # Only show if sufficient sample
        print(f"\n{rtype} (n={len(vs_avg_rt)}):")
        print(f"  vs_avg: mean={vs_avg_rt.mean():7.4f}, beat%={100*(vs_avg_rt < 0).sum()/len(vs_avg_rt):5.1f}%")
        print(f"  vs_his: mean={vs_his_rt.mean():7.4f}, beat%={100*(vs_his_rt > 0).sum()/len(vs_his_rt):5.1f}%")

# ============================================================================
# BREAKDOWN BY EXEC BUCKET
# ============================================================================

print("\n" + "=" * 80)
print("BY EXEC BUCKET")
print("=" * 80)

for bucket in ['0-25', '25-50', '50-75', '75-100']:
    df_exec = df_orange[df_orange['exec_bucket'] == bucket]

    vs_avg_exec = df_exec['vs_avg'].dropna()
    vs_his_exec = df_exec['vs_adj_his_par'].dropna()

    if len(vs_avg_exec) > 20:
        beat_own = 100*(vs_his_exec > 0).sum()/len(vs_his_exec) if len(vs_his_exec) > 0 else 0
        beat_field = 100*(vs_avg_exec < 0).sum()/len(vs_avg_exec) if len(vs_avg_exec) > 0 else 0

        print(f"\n{bucket} (n={len(vs_avg_exec)}):")
        print(f"  vs_avg: mean={vs_avg_exec.mean():7.4f}, beat%={beat_field:5.1f}%")
        print(f"  vs_his: mean={vs_his_exec.mean():7.4f}, beat%={beat_own:5.1f}%")

# ============================================================================
# THEORY VALIDATION
# ============================================================================

print("\n" + "=" * 80)
print("THEORY VALIDATION")
print("=" * 80)

beat_own_pct = 100*(vs_adj_hist_clean > 0).sum()/len(vs_adj_hist_clean)
beat_field_pct = 100*(vs_avg_clean < 0).sum()/len(vs_avg_clean)

print(f"\nHypothesis: Orange players beat their OWN adjusted average more than field")
print(f"\nResults:")
print(f"  Beat own adjusted par: {beat_own_pct:.1f}%")
print(f"  Beat field average: {beat_field_pct:.1f}%")

if beat_own_pct > beat_field_pct:
    diff = beat_own_pct - beat_field_pct
    print(f"\n✓ CONFIRMED: {diff:.1f}% more often beat own average than field")
    print(f"  Interpretation: Orange amplifies talent relative to own baseline")
else:
    diff = beat_field_pct - beat_own_pct
    print(f"\n✗ NOT CONFIRMED: Actually beat field {diff:.1f}% MORE often")
    print(f"  Interpretation: Orange effect is relative to others, not absolute talent amplification")

print()

# ============================================================================
# CORRELATION: Do players with higher adj_his_par do better in Orange?
# ============================================================================

print("=" * 80)
print("CORRELATION ANALYSIS")
print("=" * 80)

df_clean = df_orange.dropna(subset=['adj_his_par', 'vs_avg', 'vs_adj_his_par'])

corr_adj_vs_avg = df_clean['adj_his_par'].corr(df_clean['vs_avg'])
corr_adj_vs_his = df_clean['adj_his_par'].corr(df_clean['vs_adj_his_par'])

print(f"\nCorrelation: adj_his_par vs other metrics")
print(f"  adj_his_par vs vs_avg (field): r={corr_adj_vs_avg:.4f}")
print(f"  adj_his_par vs vs_adj_his_par (own): r={corr_adj_vs_his:.4f}")

if abs(corr_adj_vs_his) > abs(corr_adj_vs_avg):
    print(f"\n✓ Higher adj_his_par players perform better vs THEIR OWN average")
    print(f"  Suggests: Talent amplification (good players benefit more from Orange)")
else:
    print(f"\n✗ Higher adj_his_par players perform better vs FIELD average")
    print(f"  Suggests: Relative advantage (field is weaker, good players beat weaker opposition)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
Orange Performance vs Baselines:

1. vs_avg (field average):
   - Mean: {vs_avg_clean.mean():.4f} (negative = beats field)
   - {beat_field_pct:.1f}% of rounds beat field

2. vs_adj_his_par (own adjusted average):
   - Mean: {vs_his_exec.mean():.4f} (positive = beats own average)
   - {beat_own_pct:.1f}% of rounds beat own average

Theory Status: {"CONFIRMED" if beat_own_pct > beat_field_pct else "NOT CONFIRMED"}

Interpretation:
- Orange players beat their own adjusted par {beat_own_pct:.1f}% of the time
- Orange players beat field average {beat_field_pct:.1f}% of the time
- Difference: {abs(beat_own_pct - beat_field_pct):.1f} percentage points

This suggests Orange is {"amplifying individual talent" if beat_own_pct > beat_field_pct else "creating relative advantage vs field"}
""")

print("=" * 80)
