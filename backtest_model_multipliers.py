#!/usr/bin/env python3
"""
Backtest Model-as-Multiplier Approach

Hypothesis: Apply model signals as adjustments to player historical baseline
- Base: Player's historical win rate in condition/roundtype (92% accurate)
- Multiplier: Model signal adjustment for specific element/zodiac combo
- Final: base_wr × (1 + model_adjustment)

Tests which multiplier strategy generates edge beyond the baseline 92%
"""

import pandas as pd
import numpy as np

print("="*100)
print("BACKTEST: MODEL AS MULTIPLIER ON PLAYER HISTORY")
print("="*100)
print()

# Load data
csv_path = 'D:\\Projects\\luckify-me\\analysis_v2_with_chinese_zodiac.csv'
df = pd.read_csv(csv_path)

df['diff_course_avg'] = pd.to_numeric(df['diff_course_avg'], errors='coerce')
df['exec_bucket'] = pd.to_numeric(df['exec_bucket'], errors='coerce')
df['upside_bucket'] = pd.to_numeric(df['upside_bucket'], errors='coerce')
df = df.dropna(subset=['player_name', 'diff_course_avg', 'condition', 'round_type'])

df['is_good'] = df['diff_course_avg'] <= -2.0

print(f"[OK] {len(df):,} records\n")

# Validated signals (strongest, most reliable)
ELEMENT_VALIDATED = {
    ('Calm', 'Positioning', 'Green', 'Metal'): 0.613,
    ('Calm', 'Closing', 'Blue', 'Fire'): 0.581,
    ('Calm', 'Closing', 'Yellow', 'Metal'): 0.564,
    ('Calm', 'Positioning', 'Green', 'Wood'): 0.564,
    ('Calm', 'Survival', 'Purple', 'Fire'): 0.563,
    ('Calm', 'Closing', 'Green', 'Earth'): 0.559,
    ('Calm', 'Survival', 'Purple', 'Water'): 0.615,
}

ZODIAC_VALIDATED = {
    ('Calm', 'Survival', 50, 75, 'Tiger'): 0.653,
    ('Calm', 'Open', 50, 75, 'Rat'): 0.643,
    ('Calm', 'Positioning', 50, 50, 'Rat'): 0.635,
    ('Calm', 'Open', 25, 75, 'Snake'): 0.633,
}

NEUTRAL = 0.50

# Load player history
p_hist = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition_roundtype.csv')
p_base = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_baseline.csv')

def get_player_hist(player, cond, rt):
    """Get player's historical win rate for condition x roundtype"""
    rows = p_hist[(p_hist['player_name']==player) & (p_hist['condition']==cond) & (p_hist['round_type']==rt)]
    if len(rows) > 0:
        return rows.iloc[0]['win_rate']
    rows = p_base[p_base['player_name']==player]
    if len(rows) > 0:
        return rows.iloc[0]['career_win_rate']
    return None

def get_model_signal(condition, round_type, color, element, exec_b, upside_b, zodiac):
    """Get model signal strength (as deviation from neutral 0.5)"""
    elem_k = (condition, round_type, color, element)
    elem_s = ELEMENT_VALIDATED.get(elem_k, NEUTRAL)
    elem_adj = elem_s - NEUTRAL  # e.g., 0.613 - 0.5 = +0.113

    zod_k = (condition, round_type, int(exec_b or 50), int(upside_b or 50), zodiac)
    zod_s = ZODIAC_VALIDATED.get(zod_k, NEUTRAL)
    zod_adj = zod_s - NEUTRAL

    # Average adjustment across both signals
    avg_adj = (elem_adj * 0.6) + (zod_adj * 0.4)
    return avg_adj

# Create matchups (same as before)
calm = df[df['condition']=='Calm'].copy()
calm = calm.reset_index(drop=True)

matchups = []

for idx in range(0, len(calm)-1, 2):
    r1 = calm.iloc[idx]
    r2 = calm.iloc[idx+1]

    if r1['player_name'] == r2['player_name'] or r1['is_good'] == r2['is_good']:
        continue

    actual = 1 if r1['is_good'] else 0

    # Get player histories
    p1_hist = get_player_hist(r1['player_name'], r1['condition'], r1['round_type'])
    p2_hist = get_player_hist(r2['player_name'], r2['condition'], r2['round_type'])

    if p1_hist is None or p2_hist is None:
        continue

    # Get model adjustments
    p1_adj = get_model_signal(r1['condition'], r1['round_type'], r1['color'], r1['element'],
                              r1['exec_bucket'], r1['upside_bucket'], r1['chinese_zodiac'])
    p2_adj = get_model_signal(r2['condition'], r2['round_type'], r2['color'], r2['element'],
                              r2['exec_bucket'], r2['upside_bucket'], r2['chinese_zodiac'])

    matchups.append({
        'p1': r1['player_name'],
        'p2': r2['player_name'],
        'actual_p1_wins': actual,
        'p1_hist': p1_hist,
        'p2_hist': p2_hist,
        'p1_adj': p1_adj,
        'p2_adj': p2_adj,
    })

print(f"[OK] Built {len(matchups)} matchups with both players in history\n")

# Test different multiplier strategies
print("="*100)
print("MULTIPLIER STRATEGIES")
print("="*100)
print()

strategies = {
    'baseline_history': {
        'desc': 'Pure history (no model)',
        'calc': lambda m: m['p1_hist'] > m['p2_hist'],
    },
    'additive_100': {
        'desc': 'History + 100% of model adjustment',
        'calc': lambda m: (m['p1_hist'] + m['p1_adj']) > (m['p2_hist'] + m['p2_adj']),
    },
    'additive_50': {
        'desc': 'History + 50% of model adjustment',
        'calc': lambda m: (m['p1_hist'] + m['p1_adj']*0.5) > (m['p2_hist'] + m['p2_adj']*0.5),
    },
    'additive_25': {
        'desc': 'History + 25% of model adjustment',
        'calc': lambda m: (m['p1_hist'] + m['p1_adj']*0.25) > (m['p2_hist'] + m['p2_adj']*0.25),
    },
    'multiplicative_110': {
        'desc': 'History × (1 + 100% of model adj)',
        'calc': lambda m: (m['p1_hist'] * (1 + m['p1_adj'])) > (m['p2_hist'] * (1 + m['p2_adj'])),
    },
    'multiplicative_50': {
        'desc': 'History × (1 + 50% of model adj)',
        'calc': lambda m: (m['p1_hist'] * (1 + m['p1_adj']*0.5)) > (m['p2_hist'] * (1 + m['p2_adj']*0.5)),
    },
    'multiplicative_25': {
        'desc': 'History × (1 + 25% of model adj)',
        'calc': lambda m: (m['p1_hist'] * (1 + m['p1_adj']*0.25)) > (m['p2_hist'] * (1 + m['p2_adj']*0.25)),
    },
    'when_aligned': {
        'desc': 'History only when model agrees, else neutral',
        'calc': lambda m: (m['p1_hist'] if (m['p1_adj'] > 0) == (m['p1_hist'] > m['p2_hist']) else 0.5) > (m['p2_hist'] if (m['p2_adj'] > 0) == (m['p2_hist'] > m['p1_hist']) else 0.5),
    },
}

results = {}

for strat_name, strat_info in strategies.items():
    correct = 0

    for m in matchups:
        pred_p1_wins = strat_info['calc'](m)
        pred = 1 if pred_p1_wins else 0

        if pred == m['actual_p1_wins']:
            correct += 1

    acc = correct / len(matchups)
    edge = (acc - 0.5) * 100
    results[strat_name] = (acc, edge)

    print(f"{strat_name:<20} {strat_info['desc']:<40} {acc*100:>6.2f}% ({edge:>+6.2f}pp)")

print()
print(f"[*] Baseline (history-only): {results['baseline_history'][0]*100:.2f}%")
print()

# Find best and compare to baseline
baseline_acc = results['baseline_history'][0]
best_name = max(results.items(), key=lambda x: x[1][0])

print("="*100)
print("ANALYSIS")
print("="*100)
print()

print(f"Baseline (history): {baseline_acc*100:.2f}%")
print(f"Best strategy: {best_name[0]} at {best_name[1][0]*100:.2f}%")
print(f"Improvement: {(best_name[1][0] - baseline_acc)*100:+.2f}pp")
print()

if best_name[1][0] > baseline_acc:
    print("SUCCESS: Model multiplier improves on pure history!")
    print(f"Apply {best_name[0]} to boost matchup predictions")
else:
    print("FINDING: Pure history is optimal")
    print("Model adjustments add noise to the 92% baseline")
    print()
    print("Implication for betting:")
    print("- Model signals DON'T improve 2-ball matchup prediction")
    print("- But they might identify SPECIFIC COMBOS where player outperforms")
    print("- Focus on: 'Does Rory play better in Calm+Positioning vs his Calm baseline?'")

print()
