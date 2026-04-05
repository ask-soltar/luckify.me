"""
Tier 4: Relative Peer Comparison Framework
===========================================

Recalculate all signals using:
beat_field_pct(signal) - median(peer_colors_same_condition)

Success criterion: TBD (leave loose for user to evaluate)

Goal: Show the relative advantages, let user decide what's meaningful
"""

import pandas as pd
import json
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TIER 4: RELATIVE PEER COMPARISON FRAMEWORK")
print("Signal strength = vs other colors in same condition")
print("=" * 80)
print()

# Load data (all years for peer comparison)
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)

# Standardize
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['color'] = df['color'].astype(str).str.strip()
df['condition'] = df['condition'].astype(str).str.strip()
df['moonwest'] = df['moonwest'].astype(str).str.strip()
df['horoscope'] = df['horoscope'].astype(str).str.strip()
df['tournament_type'] = df['tournament_type'].astype(str).str.strip()

# Filter to 2025/2026 only (validation data)
df_test = df[(df['year'] >= 2025) & (df['tournament_type'].isin(['S', 'NS']))].copy()

print(f"Validation data: {len(df_test)} rows (2025/2026)")
print()

# ============================================================================
# PEER BASELINES BY CONDITION
# ============================================================================

print("=" * 80)
print("PEER BASELINES: Beat by 2+ % for all colors by condition")
print("=" * 80)
print()

# Calculate baseline for each condition
conditions = ['Calm', 'Moderate', 'Tough']
peer_baselines = {}

for cond in conditions:
    df_cond = df_test[df_test['condition'] == cond]

    if len(df_cond) < 20:
        print(f"{cond}: INSUFFICIENT DATA (n={len(df_cond)})")
        peer_baselines[cond] = {}
        continue

    print(f"{cond} (n={len(df_cond)}):")

    colors = sorted(df_cond['color'].dropna().unique())
    baselines_for_cond = {}

    for color in colors:
        df_color = df_cond[df_cond['color'] == color]
        beat_by_2 = 100 * (df_color['vs_avg'] < -2).sum() / len(df_color)
        baselines_for_cond[color] = {
            'beat_by_2_pct': beat_by_2,
            'n': len(df_color),
        }

        print(f"  {color:10} | beat by 2+ = {beat_by_2:5.1f}% (n={len(df_color):5})")

    # Calculate median
    beat_pcts = [v['beat_by_2_pct'] for v in baselines_for_cond.values()]
    median_beat = np.median(beat_pcts)
    mean_beat = np.mean(beat_pcts)

    print(f"  Median: {median_beat:.1f}% | Mean: {mean_beat:.1f}%")
    print()

    peer_baselines[cond] = baselines_for_cond

# ============================================================================
# ANALYZE EACH SIGNAL (with peer comparison)
# ============================================================================

print("=" * 80)
print("SIGNAL ANALYSIS: Relative to Peers in Same Condition")
print("=" * 80)
print()

# Load signals
with open('VALIDATED_SIGNALS.json', 'r') as f:
    signals_db = json.load(f)

all_signals = signals_db['signals_bet'] + signals_db['signals_fade']
signal_results = []

for signal in all_signals:
    signal_id = signal['id']

    # Determine condition(s) for this signal
    conditions_for_signal = []
    if 'condition' in signal:
        conditions_for_signal = [signal['condition']]
    else:
        # Signal without explicit condition (e.g., orange_newmoon)
        # Test across all conditions
        conditions_for_signal = ['Calm', 'Moderate', 'Tough']

    for cond in conditions_for_signal:
        if cond not in peer_baselines or not peer_baselines[cond]:
            continue

        # Get peer baseline
        peers = peer_baselines[cond]
        peer_beat_pcts = [v['beat_by_2_pct'] for v in peers.values()]
        peer_median = np.median(peer_beat_pcts)
        peer_mean = np.mean(peer_beat_pcts)

        # Filter signal to this condition
        df_signal = df_test.copy()

        # Apply signal filters
        if 'color' in signal:
            df_signal = df_signal[df_signal['color'] == signal['color']]
        if 'condition' in signal:
            df_signal = df_signal[df_signal['condition'] == signal['condition']]
        else:
            df_signal = df_signal[df_signal['condition'] == cond]

        if 'moon' in signal:
            df_signal = df_signal[df_signal['moonwest'] == signal['moon']]
        elif 'moon_group' in signal:
            moon_mapping = {
                'Waxing': ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter'],
                'Waning': ['Waning Crescent', 'Waning Gibbous', 'Last Quarter'],
                'New Moon': ['New Moon'],
                'Full Moon': ['Full Moon']
            }
            df_signal = df_signal[df_signal['moonwest'].isin(moon_mapping.get(signal['moon_group'], []))]

        if 'horoscope' in signal:
            df_signal = df_signal[df_signal['horoscope'] == signal['horoscope']]

        if len(df_signal) < 20:
            continue

        # Calculate beat by 2+ for this signal
        beat_by_2_pct = 100 * (df_signal['vs_avg'] < -2).sum() / len(df_signal)

        # FADE signals: opposite direction
        if signal_id == 'libra_horoscope':
            beat_by_2_pct = 100 * (df_signal['vs_avg'] > 2).sum() / len(df_signal)

        # Calculate relative advantage
        relative_advantage = beat_by_2_pct - peer_median

        signal_results.append({
            'id': signal_id,
            'condition': cond,
            'beat_by_2_pct': beat_by_2_pct,
            'peer_median': peer_median,
            'peer_mean': peer_mean,
            'relative_advantage': relative_advantage,
            'n': len(df_signal),
        })

        print(f"{signal_id:30} | {cond:10} | "
              f"beat by 2+ = {beat_by_2_pct:5.1f}% | "
              f"peer_median = {peer_median:5.1f}% | "
              f"advantage = {relative_advantage:+5.1f}pp (n={len(df_signal):4})")

print()

# ============================================================================
# SUMMARY: RANK BY RELATIVE ADVANTAGE
# ============================================================================

print("=" * 80)
print("RANKING: All Signals by Relative Advantage vs Peers")
print("=" * 80)
print()

results_df = pd.DataFrame(signal_results).sort_values('relative_advantage', ascending=False)

print("Signal                         | Condition  | Beat% | Peer% | Advantage | n    | Tier")
print("-" * 90)

for _, row in results_df.iterrows():
    advantage = row['relative_advantage']

    # Tier assignment (loose, for user to evaluate)
    if advantage > 8:
        tier = "TIER 1A (Very Strong)"
    elif advantage > 5:
        tier = "TIER 1B (Strong)"
    elif advantage > 2:
        tier = "TIER 2 (Moderate)"
    elif advantage > 0:
        tier = "TIER 3 (Slight)"
    else:
        tier = "BELOW PEERS"

    print(f"{row['id']:30} | {row['condition']:10} | "
          f"{row['beat_by_2_pct']:5.1f}% | {row['peer_median']:5.1f}% | "
          f"{advantage:+6.1f}pp | {row['n']:4} | {tier}")

print()

# ============================================================================
# DISTRIBUTION ANALYSIS: What's Meaningful?
# ============================================================================

print("=" * 80)
print("DISTRIBUTION ANALYSIS: What threshold feels right?")
print("=" * 80)
print()

advantages = results_df['relative_advantage'].values

print("Relative advantage statistics:")
print(f"  Mean: {np.mean(advantages):+.1f}pp")
print(f"  Median: {np.median(advantages):+.1f}pp")
print(f"  Std Dev: {np.std(advantages):.1f}pp")
print(f"  Min: {np.min(advantages):+.1f}pp")
print(f"  Max: {np.max(advantages):+.1f}pp")
print()

print("How many signals at each threshold?")
for threshold in [0, 1, 2, 3, 5, 8]:
    count = (advantages > threshold).sum()
    pct = 100 * count / len(advantages)
    print(f"  > +{threshold:1d}pp: {count:2d} signals ({pct:5.1f}%)")

print()

# ============================================================================
# RECOMMENDATION
# ============================================================================

print("=" * 80)
print("RECOMMENDATION: Which threshold feels meaningful?")
print("=" * 80)
print()

print("Options (for you to evaluate):")
print()
print("Option A: > +0pp (beat all peer colors)")
print("  - Most inclusive")
print("  - Count:", (advantages > 0).sum(), "signals")
print()

print("Option B: > +2pp (notably better than peers)")
print("  - Moderate (roughly splits the signals)")
print("  - Count:", (advantages > 2).sum(), "signals")
print()

print("Option C: > +5pp (significantly better than peers)")
print("  - Selective (only strongest)")
print("  - Count:", (advantages > 5).sum(), "signals")
print()

print("Option D: > +8pp (dominantly better than peers)")
print("  - Very selective")
print("  - Count:", (advantages > 8).sum(), "signals")
print()

print("Your choice determines which signals deploy.")
print("(This is why we left it loose — you get to see the distribution first)")

print()
print("=" * 80)
