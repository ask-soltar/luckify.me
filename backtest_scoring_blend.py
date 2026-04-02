#!/usr/bin/env python3
"""
Backtest Different Blending Ratios for Historical Data

Tests: Pure Model vs Pure History vs Various Blends (60/40, 70/30, 75/25, 80/20)
Metric: Win rate prediction accuracy on historical tournaments
"""

import pandas as pd
import duckdb
from datetime import datetime

print("="*100)
print("BACKTEST: SCORING BLEND OPTIMIZATION")
print("="*100)
print()

# Load ANALYSIS_v2 data
csv_path = 'D:\\Projects\\luckify-me\\analysis_v2_with_chinese_zodiac.csv'
df = pd.read_csv(csv_path)

# Clean data
df['diff_course_avg'] = pd.to_numeric(df['diff_course_avg'], errors='coerce')
df['exec_bucket'] = pd.to_numeric(df['exec_bucket'], errors='coerce')
df['upside_bucket'] = pd.to_numeric(df['upside_bucket'], errors='coerce')
df = df.dropna(subset=['player_name', 'diff_course_avg', 'condition', 'round_type'])

print(f"[OK] Loaded {len(df):,} rows from ANALYSIS_v2")
print()

# Define thresholds
GOOD_THRESHOLD = -2.0
BAD_THRESHOLD = 2.0

# Load validated signals (from player_scoring_system.py)
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
    ('Calm', 'REMOVE', 50, 50, 'Rabbit'): 0.636,
    ('Calm', 'Positioning', 50, 50, 'Rat'): 0.635,
    ('Calm', 'Open', 25, 75, 'Snake'): 0.633,
    ('Calm', 'Open', 25, 50, 'Rooster'): 0.627,
    ('Calm', 'Survival', 25, 75, 'Rat'): 0.620,
    ('Calm', 'Positioning', 50, 75, 'Pig'): 0.618,
    ('Calm', 'Open', 50, 75, 'Pig'): 0.613,
    ('Calm', 'Survival', 75, 50, 'Rooster'): 0.606,
    ('Calm', 'Positioning', 25, 50, 'Pig'): 0.601,
    ('Moderate', 'Closing', 25, 50, 'Dragon'): 0.596,
    ('Calm', 'Survival', 50, 50, 'Dog'): 0.591,
    ('Calm', 'Open', 75, 50, 'Dragon'): 0.579,
    ('Calm', 'Positioning', 50, 50, 'Goat'): 0.576,
    ('Calm', 'Survival', 50, 50, 'Leo'): 0.574,
    ('Calm', 'Closing', 50, 75, 'Monkey'): 0.572,
    ('Moderate', 'Survival', 25, 75, 'Tiger'): 0.569,
}

NEUTRAL_SCORE = 0.50

# Load player history tables
print("[*] Loading player history tables...")
player_baseline = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_baseline.csv')
player_by_cond_rt = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition_roundtype.csv')
player_by_condition = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_condition.csv')
player_by_roundtype = pd.read_csv('D:\\Projects\\luckify-me\\player_tables\\player_by_round_type.csv')

print(f"[OK] Loaded baseline for {len(player_baseline)} players")
print()

# Helper function: get model score
def get_model_score(condition, round_type, color, element, exec_bucket, upside_bucket, chinese_zodiac):
    """Blend Element + Zodiac model signals"""
    elem_key = (condition, round_type, color, element)
    elem_score = ELEMENT_SIGNALS.get(elem_key, NEUTRAL_SCORE)

    zodiac_key = (condition, round_type, exec_bucket, upside_bucket, chinese_zodiac)
    zodiac_score = ZODIAC_SIGNALS.get(zodiac_key, NEUTRAL_SCORE)

    return (elem_score * 0.6) + (zodiac_score * 0.4)

# Helper function: get player history score
def get_player_history_score(player_name, condition, round_type):
    """Get player's actual historical win rate for condition x roundtype"""
    rows = player_by_cond_rt[
        (player_by_cond_rt['player_name'] == player_name) &
        (player_by_cond_rt['condition'] == condition) &
        (player_by_cond_rt['round_type'] == round_type)
    ]

    if len(rows) > 0:
        return rows.iloc[0]['win_rate']

    # Fallback to condition only
    rows = player_by_condition[
        (player_by_condition['player_name'] == player_name) &
        (player_by_condition['condition'] == condition)
    ]
    if len(rows) > 0:
        return rows.iloc[0]['win_rate']

    # Fallback to baseline
    rows = player_baseline[player_baseline['player_name'] == player_name]
    if len(rows) > 0:
        return rows.iloc[0]['career_win_rate']

    return None

# Test on recent Calm events
print("[*] Filtering for Calm condition tournaments...")
calm_df = df[df['condition'] == 'Calm'].copy()
calm_df['is_good'] = calm_df['diff_course_avg'] <= GOOD_THRESHOLD

print(f"[OK] Found {len(calm_df):,} Calm condition records from {calm_df['player_name'].nunique()} unique players")
print(f"[OK] {calm_df['is_good'].sum():,} good performances ({calm_df['is_good'].mean()*100:.1f}% win rate baseline)")
print()

# Score each record
print("[*] Scoring all records with multiple blend ratios...")

blends = {
    'model_100': (1.0, 0.0),
    'blend_80_20': (0.8, 0.2),
    'blend_75_25': (0.75, 0.25),
    'blend_70_30': (0.7, 0.3),
    'blend_60_40': (0.6, 0.4),
    'history_100': (0.0, 1.0),
}

results = []

for idx, row in calm_df.iterrows():
    player_name = row['player_name']
    is_good = row['is_good']

    # Get model score
    model_score = get_model_score(
        row['condition'],
        row['round_type'],
        row['color'],
        row['element'],
        row['exec_bucket'],
        row['upside_bucket'],
        row['chinese_zodiac']
    )

    # Get history score
    history_score = get_player_history_score(player_name, row['condition'], row['round_type'])

    if history_score is None:
        history_score = 0.5  # Neutral

    record = {
        'player_name': player_name,
        'condition': row['condition'],
        'round_type': row['round_type'],
        'actual_result': 1 if is_good else 0,
        'model_score': model_score,
        'history_score': history_score,
    }

    # Calculate blended scores
    for blend_name, (model_weight, history_weight) in blends.items():
        blended = (model_score * model_weight) + (history_score * history_weight)
        record[f'{blend_name}_score'] = blended
        record[f'{blend_name}_pred'] = 1 if blended > 0.5 else 0

    results.append(record)

results_df = pd.DataFrame(results)

print(f"[OK] Scored {len(results_df):,} records")
print()

# Evaluate each blend
print("="*100)
print("BLEND EVALUATION")
print("="*100)
print()

eval_results = []

for blend_name in blends.keys():
    pred_col = f'{blend_name}_pred'
    correct = (results_df[pred_col] == results_df['actual_result']).sum()
    total = len(results_df)
    accuracy = correct / total

    # Calculate for 2-ball differentials (only when prediction > 0.5)
    high_conf = results_df[results_df[f'{blend_name}_score'] > 0.5]
    if len(high_conf) > 0:
        high_conf_accuracy = (high_conf[pred_col] == high_conf['actual_result']).sum() / len(high_conf)
        high_conf_count = len(high_conf)
    else:
        high_conf_accuracy = 0
        high_conf_count = 0

    eval_results.append({
        'blend': blend_name,
        'model_w': blends[blend_name][0],
        'history_w': blends[blend_name][1],
        'accuracy': accuracy,
        'high_conf_accuracy': high_conf_accuracy,
        'high_conf_count': high_conf_count,
    })

eval_df = pd.DataFrame(eval_results)
eval_df['accuracy_pct'] = (eval_df['accuracy'] * 100).round(2)
eval_df['hc_accuracy_pct'] = (eval_df['high_conf_accuracy'] * 100).round(2)

print(eval_df[['blend', 'model_w', 'history_w', 'accuracy_pct', 'hc_accuracy_pct', 'high_conf_count']].to_string(index=False))
print()

# Find best blend
best_overall = eval_df.loc[eval_df['accuracy'].idxmax()]
best_high_conf = eval_df.loc[eval_df['high_conf_accuracy'].idxmax()]

print("="*100)
print("RECOMMENDATION")
print("="*100)
print()
print(f"Best Overall Accuracy: {best_overall['blend']}")
print(f"  Model: {best_overall['model_w']:.0%} | History: {best_overall['history_w']:.0%}")
print(f"  All-predictions accuracy: {best_overall['accuracy_pct']:.2f}%")
print()
print(f"Best High-Confidence Accuracy: {best_high_conf['blend']}")
print(f"  Model: {best_high_conf['model_w']:.0%} | History: {best_high_conf['history_w']:.0%}")
print(f"  High-confidence accuracy: {best_high_conf['hc_accuracy_pct']:.2f}% ({int(best_high_conf['high_conf_count'])} records)")
print()

# Show some example predictions
print("="*100)
print("SAMPLE PREDICTIONS (Blend 70/30)")
print("="*100)
print()

sample = results_df[
    (results_df['player_name'].isin(['Rory McIlroy', 'Jon Rahm', 'Scottie Scheffler', 'Tiger Woods', 'Collin Morikawa']))
].head(20)

if len(sample) > 0:
    print(sample[['player_name', 'round_type', 'actual_result', 'model_score', 'history_score', 'blend_70_30_score', 'blend_70_30_pred']].to_string(index=False))
else:
    print("[*] Top players not found in Calm condition data. Showing random sample:")
    print(results_df[['player_name', 'round_type', 'actual_result', 'model_score', 'history_score', 'blend_70_30_score', 'blend_70_30_pred']].sample(10).to_string(index=False))

print()
print("="*100)
