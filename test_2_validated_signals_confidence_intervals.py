"""
Tier 2: Validated Signals Deep Dive — Confidence Intervals & Stability
========================================================================

Goal: Build deployment rules for signals that ALREADY VALIDATED in 2025/2026
- orange_newmoon_calm
- orange_newmoon
- orange_calm
- orange_fullmoon_calm
- orange_waxing_calm
- libra_horoscope (FADE)

For each signal:
1. Calculate 95% CI (bootstrap)
2. Test stability across conditions/round types
3. Find minimum sample threshold for deployment
4. Estimate true effect vs measurement error
"""

import pandas as pd
import json
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("TIER 2: VALIDATED SIGNALS — CONFIDENCE INTERVALS & DEPLOYMENT RULES")
print("=" * 80)
print()

# Load data
df = pd.read_csv('DATA/Golf Historics v3 - ANALYSIS (8).csv', encoding='utf-8-sig', low_memory=False)

# Standardize columns
df['vs_avg'] = pd.to_numeric(df['vs_avg'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['color'] = df['color'].astype(str).str.strip()
df['condition'] = df['condition'].astype(str).str.strip()
df['round_type'] = df['round_type'].astype(str).str.strip()
df['moonwest'] = df['moonwest'].astype(str).str.strip()
df['horoscope'] = df['horoscope'].astype(str).str.strip()
df['tournament_type'] = df['tournament_type'].astype(str).str.strip()

# Filter to 2025/2026 only
df_test = df[(df['year'] >= 2025) & (df['tournament_type'].isin(['S', 'NS']))].copy()

print(f"Test data: {len(df_test)} rows (2025/2026, stroke play)")
print()

# Load validated signals
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

def bootstrap_ci(data, n_bootstrap=10000, ci=95):
    """Calculate bootstrap confidence interval."""
    if len(data) < 5:
        return None, None, None, None

    means = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        means.append(np.mean(sample))

    lower = np.percentile(means, (100 - ci) / 2)
    upper = np.percentile(means, 100 - (100 - ci) / 2)
    point = np.mean(data)

    return point, lower, upper, np.std(means)

def analyze_signal(signal, df_test):
    """Analyze single signal: effect, CI, stability, n threshold."""
    signal_id = signal['id']
    df_signal = filter_by_signal(df_test, signal)
    vs_avg_clean = df_signal['vs_avg'].dropna()

    if len(vs_avg_clean) < 20:
        return {
            'id': signal_id,
            'n': 0,
            'status': 'INSUFFICIENT_SAMPLE',
            'mean': None,
            'ci_lower': None,
            'ci_upper': None,
            'p_value': None,
            'beat_field_pct': None,
        }

    # T-test vs 0
    t_stat, p_val = stats.ttest_1samp(vs_avg_clean, 0, nan_policy='omit')

    # Bootstrap CI
    point, ci_lower, ci_upper, se = bootstrap_ci(vs_avg_clean)

    beat_field = 100 * (vs_avg_clean < 0).sum() / len(vs_avg_clean)

    return {
        'id': signal_id,
        'n': len(vs_avg_clean),
        'mean': round(point, 4),
        'ci_lower': round(ci_lower, 4),
        'ci_upper': round(ci_upper, 4),
        'se': round(se, 4),
        'p_value': round(p_val, 6),
        'beat_field_pct': round(beat_field, 1),
        'status': 'VALIDATED' if p_val < 0.05 else 'WEAKENED',
    }

# ============================================================================
# ANALYZE EACH VALIDATED SIGNAL
# ============================================================================

all_signals = signals_db['signals_bet'] + signals_db['signals_fade']
results = []

print("=" * 80)
print("SIGNAL CONFIDENCE INTERVALS (2025/2026 Data)")
print("=" * 80)
print()

for signal in all_signals:
    result = analyze_signal(signal, df_test)
    results.append(result)

    if result['status'] != 'INSUFFICIENT_SAMPLE':
        ci_str = f"[{result['ci_lower']:+.4f}, {result['ci_upper']:+.4f}]"
        print(f"{result['id']:30} | n={result['n']:4} | mean={result['mean']:+.4f} | "
              f"95% CI {ci_str} | p={result['p_value']:.6f} | beat%={result['beat_field_pct']:5.1f}%")
    else:
        print(f"{result['id']:30} | n={result['n']:4} | INSUFFICIENT SAMPLE")

print()

# ============================================================================
# SIGNAL STABILITY ACROSS CONDITIONS
# ============================================================================

print("=" * 80)
print("SIGNAL STABILITY BY CONDITION")
print("=" * 80)
print()

for signal in signals_db['signals_bet'][:3]:  # Show top 3 BET signals
    signal_id = signal['id']
    df_signal = filter_by_signal(df_test, signal)

    print(f"{signal_id}:")

    for cond in ['Calm', 'Moderate', 'Tough']:
        df_cond = df_signal[df_signal['condition'] == cond]
        vs_avg_cond = df_cond['vs_avg'].dropna()

        if len(vs_avg_cond) >= 10:
            mean_vs = vs_avg_cond.mean()
            beat_pct = 100 * (vs_avg_cond < 0).sum() / len(vs_avg_cond)
            t_stat, p_val = stats.ttest_1samp(vs_avg_cond, 0, nan_policy='omit')
            print(f"  {cond:10} n={len(vs_avg_cond):4} | mean={mean_vs:+.4f} | beat%={beat_pct:5.1f}% | p={p_val:.4f}")

    print()

# ============================================================================
# SIGNAL STABILITY ACROSS ROUND TYPES
# ============================================================================

print("=" * 80)
print("SIGNAL STABILITY BY ROUND TYPE")
print("=" * 80)
print()

for signal in signals_db['signals_bet'][:3]:
    signal_id = signal['id']
    df_signal = filter_by_signal(df_test, signal)

    print(f"{signal_id}:")

    for rtype in sorted(df_signal['round_type'].dropna().unique()):
        df_rt = df_signal[df_signal['round_type'] == rtype]
        vs_avg_rt = df_rt['vs_avg'].dropna()

        if len(vs_avg_rt) >= 10:
            mean_vs = vs_avg_rt.mean()
            beat_pct = 100 * (vs_avg_rt < 0).sum() / len(vs_avg_rt)
            t_stat, p_val = stats.ttest_1samp(vs_avg_rt, 0, nan_policy='omit')
            print(f"  {rtype:15} n={len(vs_avg_rt):4} | mean={mean_vs:+.4f} | beat%={beat_pct:5.1f}% | p={p_val:.4f}")

    print()

# ============================================================================
# DEPLOYMENT RULE: SAMPLE SIZE THRESHOLD
# ============================================================================

print("=" * 80)
print("DEPLOYMENT READINESS: MINIMUM SAMPLE THRESHOLDS")
print("=" * 80)
print()

for signal in signals_db['signals_bet'][:3]:
    signal_id = signal['id']
    df_signal = filter_by_signal(df_test, signal)
    vs_avg_clean = df_signal['vs_avg'].dropna()

    if len(vs_avg_clean) >= 20:
        # What n is needed for 95% CI to not cross 0?
        mean = vs_avg_clean.mean()
        se = vs_avg_clean.std() / np.sqrt(len(vs_avg_clean))
        ci_half = 1.96 * se

        print(f"{signal_id}:")
        print(f"  Current n: {len(vs_avg_clean)}")
        print(f"  Current 95% CI: [{mean - ci_half:+.4f}, {mean + ci_half:+.4f}]")

        if mean - ci_half < 0 and mean + ci_half > 0:
            print(f"  Status: CI crosses 0 (margin to 0: {min(abs(mean - ci_half), abs(mean + ci_half)):+.4f})")
            print(f"  Recommendation: Needs more data or narrower filter")
        else:
            print(f"  Status: CI does NOT cross 0 (robust)")
            print(f"  Recommendation: Ready for deployment")

        print()

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print()

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('n', ascending=False)

print(results_df[['id', 'n', 'mean', 'p_value', 'beat_field_pct', 'status']].to_string(index=False))

print()
print("=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Signals with p < 0.05 are validated for deployment
2. Check 95% CI — if it doesn't cross 0, signal is robust
3. Stability tests show which conditions/round types are safest
4. Use minimum n threshold when applying signal in live screener
5. Monitor actual matchup outcomes against these forecasts
""")

print("=" * 80)
