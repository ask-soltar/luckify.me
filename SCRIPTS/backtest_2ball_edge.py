#!/usr/bin/env python3
"""
Backtest 2-Ball Matchup Predictions: Model vs History vs Blend

Key question: Does our scoring better predict HEAD-TO-HEAD outcomes than 50/50?
Metric: Win rate on matchup predictions (who beats whom in pairs)
"""

import pandas as pd
import itertools
from collections import defaultdict

print("="*100)
print("BACKTEST: 2-BALL MATCHUP EDGE DETECTION")
print("="*100)
print()

# Load ANALYSIS_v2
csv_path = 'D:\\Projects\\luckify-me\\analysis_v2_with_chinese_zodiac.csv'
df = pd.read_csv(csv_path)

# Clean
df['diff_course_avg'] = pd.to_numeric(df['diff_course_avg'], errors='coerce')
df['exec_bucket'] = pd.to_numeric(df['exec_bucket'], errors='coerce')
df['upside_bucket'] = pd.to_numeric(df['upside_bucket'], errors='coerce')
df = df.dropna(subset=['player_name', 'diff_course_avg', 'condition', 'round_type'])

GOOD_THRESHOLD = -2.0
df['is_good'] = df['diff_course_avg'] <= GOOD_THRESHOLD

print(f"[OK] Loaded {len(df):,} records, {df['player_name'].nunique()} players")

# Model signals
ELEMENT_SIGNALS = {
    ('Calm', 'Survival', 'Purple', 'Water'): 0.615,
    ('Calm', 'Positioning', 'Green', 'Metal'): 0.613,
    ('Calm', 'Closing', 'Blue', 'Fire'): 0.581,
    ('Calm', 'Closing', 'Yellow', 'Metal'): 0.564,
    ('Calm', 'Positioning', 'Green', 'Wood'): 0.564,
    ('Calm', 'Survival', 'Purple', 'Fire'): 0.563,
    ('Calm', 'Positioning', 'Purple', 'Wood'): 0.560,
    ('Calm', 'Closing', 'Green', 'Earth'): 0.559,
    ('Calm', 'Closing', 'Orange', 'Wood'): 0.546,
    ('Calm', 'Closing', 'Purple', 'Fire'): 0.546,
    ('Calm', 'Closing', 'Orange', 'Water'): 0.527,
    ('Calm', 'Survival', 'Orange', 'Water'): 0.537,
    ('Calm', 'Closing', 'Purple', 'Water'): 0.533,
    ('Calm', 'Survival', 'Green', 'Earth'): 0.526,
}

ZODIAC_SIGNALS = {
    ('Calm', 'Survival', 50, 75, 'Tiger'): 0.653,
    ('Calm', 'Open', 50, 75, 'Rat'): 0.643,
    ('Calm', 'Survival', 25, 50, 'Goat'): 0.642,
    ('Calm', 'Survival', 50, 75, 'Snake'): 0.640,
    ('Calm', 'Positioning', 50, 50, 'Rat'): 0.635,
    ('Calm', 'Open', 25, 75, 'Snake'): 0.633,
    ('Calm', 'Open', 25, 50, 'Rooster'): 0.627,
    ('Calm', 'Survival', 25, 75, 'Rat'): 0.620,
    ('Calm', 'Positioning', 50, 75, 'Pig'): 0.618,
    ('Calm', 'Open', 50, 75, 'Pig'): 0.613,
    ('Calm', 'Survival', 75, 50, 'Rooster'): 0.606,
    ('Calm', 'Positioning', 25, 50, 'Pig'): 0.601,
}

NEUTRAL = 0.50

# Helper: get model score
def model_score(condition, round_type, color, element, exec_b, upside_b, zodiac):
    elem = ELEMENT_SIGNALS.get((condition, round_type, color, element), NEUTRAL)
    zodiac_key = (condition, round_type, int(exec_b) if exec_b else 50, int(upside_b) if upside_b else 50, zodiac)
    zodiac_s = ZODIAC_SIGNALS.get(zodiac_key, NEUTRAL)
    return (elem * 0.6) + (zodiac_s * 0.4)

# Load player history
player_by_cond_rt = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition_roundtype.csv')
player_by_condition = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition.csv')
player_baseline = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_baseline.csv')

def history_score(player_name, condition, round_type):
    """Get player's historical win rate"""
    rows = player_by_cond_rt[
        (player_by_cond_rt['player_name'] == player_name) &
        (player_by_cond_rt['condition'] == condition) &
        (player_by_cond_rt['round_type'] == round_type)
    ]
    if len(rows) > 0:
        return rows.iloc[0]['win_rate']

    rows = player_by_condition[
        (player_by_condition['player_name'] == player_name) &
        (player_by_condition['dimension_value'] == condition)
    ]
    if len(rows) > 0:
        return rows.iloc[0]['win_rate']

    rows = player_baseline[player_baseline['player_name'] == player_name]
    if len(rows) > 0:
        return rows.iloc[0]['career_win_rate']

    return 0.5

# Filter to Calm events
calm = df[df['condition'] == 'Calm'].copy()
print(f"[OK] {len(calm):,} Calm records\n")

# Group by tournament and round to find pairings
print("[*] Building 2-ball matchups from historical tournaments...")

matchups = []
pairing_count = defaultdict(int)

# Group by event and round
for (event, round_type), group in calm.groupby(['event_name', 'round_type']):
    players_in_round = list(group['player_name'].unique())

    if len(players_in_round) < 2:
        continue

    # Generate all pairings
    for p1, p2 in itertools.combinations(sorted(players_in_round), 2):
        p1_rows = group[group['player_name'] == p1]
        p2_rows = group[group['player_name'] == p2]

        if len(p1_rows) == 0 or len(p2_rows) == 0:
            continue

        # Use first record for each player in this event/round
        p1_row = p1_rows.iloc[0]
        p2_row = p2_rows.iloc[0]

        # Actual outcome (did p1 beat p2?)
        p1_good = p1_row['is_good']
        p2_good = p2_row['is_good']

        # If both good or both bad, skip (ambiguous)
        if p1_good == p2_good:
            continue

        actual_p1_wins = 1 if p1_good else 0

        # Get scores
        p1_model = model_score(p1_row['condition'], p1_row['round_type'], p1_row['color'],
                               p1_row['element'], p1_row['exec_bucket'], p1_row['upside_bucket'],
                               p1_row['chinese_zodiac'])
        p2_model = model_score(p2_row['condition'], p2_row['round_type'], p2_row['color'],
                               p2_row['element'], p2_row['exec_bucket'], p2_row['upside_bucket'],
                               p2_row['chinese_zodiac'])

        p1_history = history_score(p1, p1_row['condition'], p1_row['round_type'])
        p2_history = history_score(p2, p2_row['condition'], p2_row['round_type'])

        matchups.append({
            'p1': p1,
            'p2': p2,
            'round_type': round_type,
            'event': event,
            'actual_p1_wins': actual_p1_wins,
            'p1_model': p1_model,
            'p2_model': p2_model,
            'p1_history': p1_history,
            'p2_history': p2_history,
        })

        pairing_count[(p1, p2)] += 1

print(f"[OK] Found {len(matchups)} matchups across {len(pairing_count)} unique pairings\n")

# Evaluate different approaches
print("="*100)
print("2-BALL MATCHUP ACCURACY (Who wins head-to-head)")
print("="*100)
print()

results = {
    'random_50_50': [],
    'model_only': [],
    'history_only': [],
    'blend_70_30': [],
    'blend_60_40': [],
    'best_available': [],  # History if available, else model
}

for m in matchups:
    # Random 50/50
    results['random_50_50'].append(1 if m['actual_p1_wins'] == 0.5 else (1 if m['actual_p1_wins'] else 0))

    # Model: predict p1 wins if p1_model > p2_model
    model_p1_wins = 1 if m['p1_model'] > m['p2_model'] else 0
    results['model_only'].append(1 if model_p1_wins == m['actual_p1_wins'] else 0)

    # History: predict p1 wins if p1_history > p2_history
    history_p1_wins = 1 if m['p1_history'] > m['p2_history'] else 0
    results['history_only'].append(1 if history_p1_wins == m['actual_p1_wins'] else 0)

    # Blend 70/30
    blend_p1 = (m['p1_model'] * 0.7) + (m['p1_history'] * 0.3)
    blend_p2 = (m['p2_model'] * 0.7) + (m['p2_history'] * 0.3)
    blend_p1_wins = 1 if blend_p1 > blend_p2 else 0
    results['blend_70_30'].append(1 if blend_p1_wins == m['actual_p1_wins'] else 0)

    # Blend 60/40
    blend_p1 = (m['p1_model'] * 0.6) + (m['p1_history'] * 0.4)
    blend_p2 = (m['p2_model'] * 0.6) + (m['p2_history'] * 0.4)
    blend_p1_wins = 1 if blend_p1 > blend_p2 else 0
    results['blend_60_40'].append(1 if blend_p1_wins == m['actual_p1_wins'] else 0)

    # Best available: use history if both players have it, else model
    if m['p1_history'] != 0.5 and m['p2_history'] != 0.5:
        best_p1_wins = 1 if m['p1_history'] > m['p2_history'] else 0
    else:
        best_p1_wins = 1 if m['p1_model'] > m['p2_model'] else 0
    results['best_available'].append(1 if best_p1_wins == m['actual_p1_wins'] else 0)

# Print results
print(f"{'Approach':<20} {'Win Rate':<12} {'Edge vs 50/50':<15}")
print("-" * 50)

baseline = sum(results['random_50_50']) / len(results['random_50_50'])

for approach in ['random_50_50', 'model_only', 'history_only', 'blend_70_30', 'blend_60_40', 'best_available']:
    win_rate = sum(results[approach]) / len(results[approach])
    edge = (win_rate - baseline) * 100
    print(f"{approach:<20} {win_rate*100:>6.2f}%       {edge:>+6.2f}pp")

print()
print(f"[*] Testing on {len(matchups)} head-to-head matchups")
print(f"[*] Baseline (random): {baseline*100:.2f}%")
print()

# Show high-edge matchups
print("="*100)
print("HIGH-EDGE MATCHUPS (Model predicts +3pp or more)")
print("="*100)
print()

high_edge = []
for m in matchups:
    model_diff = abs(m['p1_model'] - m['p2_model'])
    if model_diff >= 0.03:
        model_p1_wins = 1 if m['p1_model'] > m['p2_model'] else 0
        correct = 1 if model_p1_wins == m['actual_p1_wins'] else 0
        high_edge.append({
            'p1': m['p1'],
            'p2': m['p2'],
            'p1_model': m['p1_model'] * 100,
            'p2_model': m['p2_model'] * 100,
            'diff': model_diff * 100,
            'p1_history': m['p1_history'] * 100,
            'p2_history': m['p2_history'] * 100,
            'actual_p1_wins': m['actual_p1_wins'],
            'model_prediction_correct': correct,
        })

high_edge_df = pd.DataFrame(high_edge)
high_edge_accuracy = high_edge_df['model_prediction_correct'].mean()

print(f"{len(high_edge)} matchups with +3pp model edge")
print(f"Model accuracy on these: {high_edge_accuracy*100:.2f}%")
print()
print(high_edge_df[['p1', 'p2', 'p1_model', 'p2_model', 'diff', 'actual_p1_wins', 'model_prediction_correct']].head(15).to_string(index=False))

print()
print("="*100)
