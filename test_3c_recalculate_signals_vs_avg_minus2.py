"""
Recalculate All Validated Signals Using vs_avg < -2 Threshold
================================================================

Instead of "beat field by any amount" (vs_avg < 0),
use "beat field by 2+ strokes" (vs_avg < -2)

This applies to ALL signals:
- orange_calm
- orange_newmoon_calm
- orange_newmoon
- orange_fullmoon_calm
- orange_waxing_calm
- libra_horoscope (FADE direction reverses)
"""

import pandas as pd
import json
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("RECALCULATING SIGNALS WITH vs_avg < -2 THRESHOLD")
print("=" * 80)
print()

# Load data
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

# Load current signals database
with open('VALIDATED_SIGNALS.json', 'r') as f:
    signals_db = json.load(f)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def filter_by_signal(df, signal):
    """Apply signal filters to dataframe."""
    mask = pd.Series([True] * len(df), index=df.index)

    for key, value in signal.items():
        if key in ['id', 'tier', 'effect', 'effect_2025_2026', 'n', 'n_validated',
                   'p_value', 'p_value_2025_2026', 'description', 'source', 'note']:
            continue

        col_mapping = {
            'color': 'color',
            'condition': 'condition',
            'round_type': 'round_type',
            'element': 'wu_xing',
            'exec_bucket': 'exec_bucket',
            'moon': 'moonwest',
            'moon_group': None,
            'horoscope': 'horoscope',
            'zodiac': 'zodiac',
        }

        if key == 'moon_group':
            moon_mapping = {
                'Waxing': ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter'],
                'Waning': ['Waning Crescent', 'Waning Gibbous', 'Last Quarter'],
                'New Moon': ['New Moon'],
                'Full Moon': ['Full Moon']
            }
            mask &= df['moonwest'].isin(moon_mapping.get(value, []))
        elif key in col_mapping and col_mapping[key]:
            col = col_mapping[key]
            mask &= (df[col] == value)

    return df[mask]

def analyze_signal_new_threshold(signal, df_test):
    """Analyze signal using vs_avg < -2 threshold."""
    signal_id = signal['id']
    df_signal = filter_by_signal(df_test, signal)

    if len(df_signal) < 20:
        return None

    # NEW THRESHOLD: vs_avg < -2 (beat field by 2+ strokes)
    beat_by_2_pct = 100 * (df_signal['vs_avg'] < -2).sum() / len(df_signal)
    beat_by_2_count = (df_signal['vs_avg'] < -2).sum()

    # For FADE signals, reverse: want vs_avg > 2 (lose to field by 2+)
    if signal_id == 'libra_horoscope':
        beat_by_2_pct = 100 * (df_signal['vs_avg'] > 2).sum() / len(df_signal)
        beat_by_2_count = (df_signal['vs_avg'] > 2).sum()

    # Calculate mean vs_avg for context
    mean_vs_avg = df_signal['vs_avg'].mean()

    # T-test: is proportion significantly different from 50%?
    if signal_id != 'libra_horoscope':
        hit_count = (df_signal['vs_avg'] < -2).sum()
    else:
        hit_count = (df_signal['vs_avg'] > 2).sum()

    n = len(df_signal)

    # T-test vs 50% baseline
    # Use proportion test approximation
    prop = hit_count / n
    se = np.sqrt(0.5 * 0.5 / n)
    z_stat = (prop - 0.5) / se
    p_val = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return {
        'id': signal_id,
        'n_total': len(df_signal),
        'beat_by_2_count': beat_by_2_count,
        'beat_by_2_pct': beat_by_2_pct,
        'mean_vs_avg': mean_vs_avg,
        'p_value': p_val,
    }

# ============================================================================
# RECALCULATE ALL SIGNALS
# ============================================================================

print("=" * 80)
print("RECALCULATED SIGNAL PERFORMANCE (vs_avg < -2 threshold)")
print("=" * 80)
print()

all_signals = signals_db['signals_bet'] + signals_db['signals_fade']
results = []

for signal in all_signals:
    result = analyze_signal_new_threshold(signal, df_test)

    if result:
        results.append(result)

        signal_type = "BET" if signal['id'] != 'libra_horoscope' else "FADE"
        print(f"{signal['id']:30} ({signal_type:4}) | n={result['n_total']:4} | "
              f"beat_by_2={result['beat_by_2_pct']:5.1f}% (n={result['beat_by_2_count']:3}) | "
              f"p={result['p_value']:.6f}")

print()

# ============================================================================
# ANALYSIS: WHICH SIGNALS HOLD UP?
# ============================================================================

print("=" * 80)
print("SIGNAL VALIDITY CHECK (vs_avg < -2 threshold)")
print("=" * 80)
print()

print("For a signal to be valid at this threshold:")
print("- Must have meaningful sample (n >= 20)")
print("- Beat by 2+ rate should be > 25% (better than baseline)")
print("- p < 0.05 preferred (but relaxed for rare conditions)")
print()

valid_signals = []
weak_signals = []

for result in results:
    if result['beat_by_2_pct'] > 25:
        valid_signals.append(result)
        print(f"VALID: {result['id']:30} | {result['beat_by_2_pct']:5.1f}% beat by 2+")
    else:
        weak_signals.append(result)
        print(f"WEAK:  {result['id']:30} | {result['beat_by_2_pct']:5.1f}% beat by 2+ (below 25%)")

print()

# ============================================================================
# INTERPRETATION
# ============================================================================

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

if len(valid_signals) > 0:
    print(f"VALID SIGNALS ({len(valid_signals)}):")
    for sig in valid_signals:
        print(f"  {sig['id']:30} | {sig['beat_by_2_pct']:5.1f}% qualify (n={sig['beat_by_2_count']:3})")
    print()
else:
    print("NO SIGNALS meet the 25% threshold for beat by 2+")
    print()

if len(weak_signals) > 0:
    print(f"WEAK SIGNALS ({len(weak_signals)}):")
    for sig in weak_signals:
        print(f"  {sig['id']:30} | {sig['beat_by_2_pct']:5.1f}% qualify (n={sig['beat_by_2_count']:3})")
    print()

# ============================================================================
# COMPARISON: OLD vs NEW THRESHOLD
# ============================================================================

print("=" * 80)
print("COMPARISON: vs_avg < 0 (OLD) vs vs_avg < -2 (NEW)")
print("=" * 80)
print()

print("Signal Name                    | Old Threshold | New Threshold | Difference")
print("                                (beat any%)    (beat 2+%)     ")
print("-" * 75)

for signal in signals_db['signals_bet'][:3]:
    df_signal = filter_by_signal(df_test, signal)

    if len(df_signal) < 20:
        continue

    # Old metric
    old_beat_pct = 100 * (df_signal['vs_avg'] < 0).sum() / len(df_signal)

    # New metric
    new_beat_pct = 100 * (df_signal['vs_avg'] < -2).sum() / len(df_signal)

    diff = old_beat_pct - new_beat_pct

    print(f"{signal['id']:30} | {old_beat_pct:6.1f}%       | {new_beat_pct:6.1f}%       | {diff:+6.1f}pp")

print()

# ============================================================================
# RECOMMENDATION
# ============================================================================

print("=" * 80)
print("DEPLOYMENT DECISION")
print("=" * 80)
print()

if len(valid_signals) > 0:
    print("RECOMMENDATION: Update signals database to use vs_avg < -2 threshold")
    print()
    print("Benefits:")
    print("  - More conservative (captures only meaningful outliers)")
    print("  - Higher quality matches (fewer false positives)")
    print("  - Asymmetrical signal is clearer (beat by 2+ > lose by 2+)")
    print()
    print("Trade-off:")
    print("  - Fewer matches (~29% vs ~57%)")
    print("  - But higher confidence in each match")
    print()
else:
    print("WARNING: No signals meet 25% threshold with vs_avg < -2")
    print("Options:")
    print("  1. Lower threshold to 20% (weakens confidence)")
    print("  2. Use vs_avg < -1 instead (compromise)")
    print("  3. Revert to vs_avg < 0 (original)")

print()
print("=" * 80)
