"""
Validate Signals on 2025-2026 Data (Out-of-Sample)
==================================================

Test if validated signals hold on recent 2025/2026 data.
- Historical signals were derived from 2022-2026 data
- This tests them on 2025-2026 specifically (newer data)
- Verify signal stability and out-of-sample performance

Data Source: Golf Historics v3 - ANALYSIS (8).csv
Filter: year >= 2025
"""

import pandas as pd
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("SIGNAL VALIDATION ON 2025-2026 DATA (OUT-OF-SAMPLE)")
print("=" * 80)

# Load data
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)
# Ensure numeric columns are actually numeric
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df_recent = df[df['year'] >= 2025].copy()
print(f"[OK] Loaded {len(df_recent)} rounds from 2025-2026")
print(f"      2025: {len(df_recent[df_recent['year']==2025])}")
print(f"      2026: {len(df_recent[df_recent['year']==2026])}")
print()

# Load signals
with open('VALIDATED_SIGNALS.json', 'r') as f:
    signals_db = json.load(f)

all_signals = signals_db['signals_bet'] + signals_db['signals_fade']
print(f"[OK] Loaded {len(all_signals)} signals to validate")
print()

# ============================================================================
# VALIDATION FUNCTION
# ============================================================================

def validate_signal(signal, df_test):
    """Test a single signal on 2025/2026 data."""

    # Build filter conditions
    filter_mask = pd.Series([True] * len(df_test), index=df_test.index)

    for key, value in signal.items():
        if key in ['id', 'tier', 'effect', 'n', 'p_value', 'description', 'source', 'note']:
            continue

        col_mapping = {
            'color': 'color',
            'condition': 'condition',
            'round_type': 'round_type',
            'element': 'wu_xing',
            'exec_bucket': 'exec_bucket',
            'moon': 'moonwest',
            'horoscope': 'horoscope',
            'zodiac': 'zodiac',
        }

        if key == 'moon_group':
            # Handle grouped moon phases
            moon_mapping = {
                'Waxing': ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter'],
                'Waning': ['Waning Crescent', 'Waning Gibbous', 'Last Quarter'],
                'New Moon': ['New Moon'],
                'Full Moon': ['Full Moon']
            }
            filter_mask &= df_test['moonwest'].isin(moon_mapping.get(value, []))
        elif key in col_mapping and col_mapping[key]:
            col = col_mapping[key]
            filter_mask &= (df_test[col] == value)

    # Apply filter
    subset = df_test[filter_mask]
    n = len(subset)

    if n < 20:  # Too few samples to validate
        return {
            'id': signal['id'],
            'n_expected': signal['n'],
            'n_actual': n,
            'historical_effect': signal['effect'],
            'actual_effect': None,
            'p_value': None,
            'beat_field_pct': None,
            'status': 'TOO_FEW_SAMPLES',
            'held': False
        }

    # Calculate actual effect on 2025/2026 data
    mean_vs_avg = subset['vs_avg'].mean()
    std_vs_avg = subset['vs_avg'].std()
    beat_field_count = (subset['vs_avg'] < 0).sum()
    beat_field_pct = 100 * beat_field_count / n

    # T-test: is effect significantly different from 0?
    t_stat, p_value = stats.ttest_1samp(subset['vs_avg'], 0, nan_policy='omit')

    # Did signal HOLD? (same direction, p<0.05)
    historical_effect = signal['effect']
    same_direction = (mean_vs_avg * historical_effect) > 0
    p_held = p_value < 0.05
    held = same_direction and p_held

    # Effect magnitude decay
    magnitude_decay = abs(mean_vs_avg) / abs(historical_effect) if historical_effect != 0 else 0

    return {
        'id': signal['id'],
        'tier': signal['tier'],
        'n_expected': signal['n'],
        'n_actual': n,
        'historical_effect': round(historical_effect, 4),
        'actual_effect': round(mean_vs_avg, 4),
        'effect_decay': round(magnitude_decay, 3),
        'std': round(std_vs_avg, 4),
        'beat_field_pct': round(beat_field_pct, 1),
        'beat_field_count': beat_field_count,
        'p_value': round(p_value, 4),
        'status': 'HELD' if held else ('WEAKENED' if same_direction else 'REVERSED'),
        'held': held
    }

# ============================================================================
# RUN VALIDATION
# ============================================================================

print("=" * 80)
print("TIER 1 SIGNALS (Maximum Conviction)")
print("=" * 80)

tier1_signals = [s for s in signals_db['signals_bet'] if s['tier'] == 1]
tier1_results = []

for signal in tier1_signals:
    result = validate_signal(signal, df_recent)
    tier1_results.append(result)

    status_icon = "[HELD]" if result['held'] else "[WEAK]"
    print(f"{status_icon} {result['id']:35} | n={result['n_actual']:4} | "
          f"hist={result['historical_effect']:7.4f} -> actual={result['actual_effect']:7.4f} | "
          f"p={result['p_value']:.4f}")

print()
print("=" * 80)
print("TIER 2 SIGNALS (Strong Conviction)")
print("=" * 80)

tier2_signals = [s for s in signals_db['signals_bet'] if s['tier'] == 2]
tier2_results = []

for signal in tier2_signals[:5]:  # Show first 5 for brevity
    result = validate_signal(signal, df_recent)
    tier2_results.append(result)

    status_icon = "[HELD]" if result['held'] else "[WEAK]"
    print(f"{status_icon} {result['id']:35} | n={result['n_actual']:4} | "
          f"hist={result['historical_effect']:7.4f} -> actual={result['actual_effect']:7.4f} | "
          f"p={result['p_value']:.4f}")

print(f"... and {len(tier2_signals)-5} more tier 2 signals")

print()
print("=" * 80)
print("FADE SIGNALS (Avoid)")
print("=" * 80)

fade_results = []
for signal in signals_db['signals_fade'][:3]:  # Show first 3
    result = validate_signal(signal, df_recent)
    fade_results.append(result)

    status_icon = "[HELD]" if result['held'] else "[WEAK]"
    print(f"{status_icon} {result['id']:35} | n={result['n_actual']:4} | "
          f"hist={result['historical_effect']:7.4f} -> actual={result['actual_effect']:7.4f} | "
          f"p={result['p_value']:.4f}")

# ============================================================================
# SUMMARY
# ============================================================================

all_results = tier1_results + tier2_results + fade_results
held_count = sum(1 for r in all_results if r['held'])
total_count = len(all_results)

print()
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print(f"\nSignals Tested: {total_count}")
print(f"Signals Held (p<0.05, same direction): {held_count}/{total_count} ({100*held_count/total_count:.1f}%)")
print()

# Save detailed results
results_df = pd.DataFrame(all_results)
results_df.to_csv('SIGNAL_VALIDATION_2025_2026.csv', index=False)
print(f"[OK] Saved detailed results to: SIGNAL_VALIDATION_2025_2026.csv")

print()
print("=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Review SIGNAL_VALIDATION_2025_2026.csv for detailed per-signal results
2. Identify any signals that REVERSED or WEAKENED significantly
3. Update VALIDATED_SIGNALS.json if needed (remove weak signals)
4. Monitor live 2026 results going forward
5. Revalidate quarterly as new data accumulates

Stability Expectation:
- Archetypal signals (moon, condition, element) should hold 80%+
- Combo signals (moon×condition) may decay but should maintain direction
- Any signal with p>0.05 in 2025/2026 is questionable
""")

print("=" * 80)
