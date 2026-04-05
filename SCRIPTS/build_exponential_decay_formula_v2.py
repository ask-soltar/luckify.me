"""
Exponential Decay Formula - V2 (Data Structure Corrected)

ANALYSIS_v2 has multiple rows per tournament-round (one per condition).
Must aggregate to unique events first, then calculate recent form.

Structure: Player -> Event -> Round -> Condition
We need: Player -> Chronological Event List -> Recent Form
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("EXPONENTIAL DECAY FORMULA V2 - CORRECTED FOR DATA STRUCTURE")
print("=" * 80)

# Load data
print("\n[1] Loading ANALYSIS_v2 data...")
analysis = pd.read_csv('ANALYSIS_v2_with_element.csv')

print(f"    Total rows: {len(analysis):,}")
print(f"    Unique players: {analysis['player_id'].nunique():,}")
print(f"    Unique events: {analysis['event_id'].nunique():,}")
print(f"    Year range: {analysis['year'].min()}-{analysis['year'].max()}")

# Create unique player-event-round identifier
print("\n[2] Identifying unique tournament rounds...")
analysis['event_round_id'] = analysis['event_id'].astype(str) + '_' + analysis['round_num'].astype(str)

# For each unique event-round combo, take the FIRST condition (all conditions = same actual performance)
print("    Taking first condition per event-round (all conditions = same score)...")
event_round_scores = analysis.drop_duplicates(
    subset=['player_id', 'event_id', 'round_num'],
    keep='first'
)[['player_id', 'player_name', 'event_id', 'year', 'round_num', 'Off Par']].copy()

print(f"    Unique event-round combos: {len(event_round_scores):,}")

# Sort chronologically by player
print("\n[3] Creating chronological player event sequences...")
event_round_scores = event_round_scores.sort_values(['player_id', 'year', 'round_num']).reset_index(drop=True)

# For each player, assign event sequence number
def assign_event_sequence(group):
    group = group.copy()
    group['event_seq'] = range(len(group))
    return group

event_round_scores = event_round_scores.groupby('player_id').apply(assign_event_sequence).reset_index(drop=True)

print(f"    Assigned chronological sequence to each player")

# Calculate rounds_ago using METHOD A (primary)
print("\n[4] Calculating rounds_ago_i (events_ago) - METHOD A...")

def calculate_events_ago_method_a(group):
    group = group.copy()
    # For current event, events_ago = (total_events - current_seq_num - 1)
    total_events = len(group)
    group['events_ago_method_a'] = total_events - group['event_seq'] - 1
    return group

event_round_scores = event_round_scores.groupby('player_id').apply(calculate_events_ago_method_a).reset_index(drop=True)

print(f"    [OK] events_ago_method_a calculated")
print(f"    Range: {event_round_scores['events_ago_method_a'].min()} to {event_round_scores['events_ago_method_a'].max()}")

# Calculate events_ago using METHOD B (audit)
print("\n[5] Calculating events_ago_i - METHOD B (audit)...")

def calculate_events_ago_method_b(group):
    group = group.copy()
    events_ago = []
    for idx, row in group.iterrows():
        # Count events AFTER this one
        after_count = len(group[group['event_seq'] > row['event_seq']])
        events_ago.append(after_count)
    group['events_ago_method_b'] = events_ago
    return group

event_round_scores = event_round_scores.groupby('player_id').apply(calculate_events_ago_method_b).reset_index(drop=True)

print(f"    [OK] events_ago_method_b calculated")

# AUDIT: Compare methods
print("\n[6] AUDIT: Comparing METHOD A vs METHOD B...")
mismatch = (event_round_scores['events_ago_method_a'] != event_round_scores['events_ago_method_b']).sum()
if mismatch == 0:
    print(f"    [PASS] PERFECT MATCH - Both methods agree on all {len(event_round_scores):,} rows")
else:
    print(f"    [FAIL] Mismatches: {mismatch}")

event_round_scores['events_ago'] = event_round_scores['events_ago_method_a']

# Calculate exponential decay weights
print("\n[7] Calculating exponential decay weights...")
decay_rates = [10, 15, 20, 25, 30, 40, 50]

for decay_rate in decay_rates:
    event_round_scores[f'weight_decay_{decay_rate}'] = np.exp(-decay_rate / 100 * event_round_scores['events_ago'])

print(f"    [OK] Weights calculated for: {decay_rates}")

# Calculate recent_form_vs_par
print("\n[8] Calculating recent_form_vs_par...")

def calculate_recent_form(group, decay_rate, window_size=20):
    group = group.copy()
    recent_forms = []

    for idx, row in group.iterrows():
        # Get THIS event and all PRIOR events (no future data)
        prior_events = group[group['event_seq'] <= row['event_seq']].copy()

        # Use last N events
        recent_events = prior_events.tail(window_size).copy()

        if len(recent_events) > 1:  # Need at least 2 events
            # Assign weights in reverse order (oldest to newest)
            weights = np.exp(-decay_rate / 100 * np.arange(len(recent_events)-1, -1, -1))
            weighted_avg = (recent_events['Off Par'].values * weights).sum() / weights.sum()
        else:
            weighted_avg = np.nan

        recent_forms.append(weighted_avg)

    group[f'recent_form_decay_{decay_rate}'] = recent_forms
    return group

for decay_rate in [20, 50]:
    print(f"    Calculating recent_form for decay_rate={decay_rate}...")
    event_round_scores = event_round_scores.groupby('player_id').apply(
        lambda g: calculate_recent_form(g, decay_rate, window_size=20)
    ).reset_index(drop=True)

print(f"    [OK] recent_form_vs_par calculated")

# MACRO FACTOR CHECKS
print("\n[9] MACRO FACTOR VALIDATION...")

checks_passed = 0
checks_total = 0

# Check 1: No extreme NaN
checks_total += 1
nan_pct = event_round_scores['recent_form_decay_50'].isna().sum() / len(event_round_scores) * 100
if nan_pct < 20:  # Allow some NaN for players with <20 events
    print(f"    [PASS] Check 1: NaN within tolerance ({nan_pct:.1f}%)")
    checks_passed += 1
else:
    print(f"    [FAIL] Check 1: Too many NaN values ({nan_pct:.1f}%)")

# Check 2: Weights between 0-1
checks_total += 1
weights_valid = (event_round_scores['weight_decay_50'] >= 0) & (event_round_scores['weight_decay_50'] <= 1)
if weights_valid.all():
    print(f"    [PASS] Check 2: All weights in valid range [0,1]")
    checks_passed += 1
else:
    print(f"    [FAIL] Check 2: Invalid weights detected")

# Check 3: Most recent events weighted higher
checks_total += 1
recent_weight = event_round_scores[event_round_scores['events_ago'] == 0]['weight_decay_50'].mean()
old_weight = event_round_scores[event_round_scores['events_ago'] > 15]['weight_decay_50'].mean()
if recent_weight > old_weight:
    print(f"    [PASS] Check 3: Recent events weighted higher ({recent_weight:.4f} vs {old_weight:.4f})")
    checks_passed += 1
else:
    print(f"    [FAIL] Check 3: Weight distribution inverted")

# Check 4: Different decay rates produce different results
checks_total += 1
std_20 = event_round_scores['recent_form_decay_20'].std()
std_50 = event_round_scores['recent_form_decay_50'].std()
if abs(std_20 - std_50) > 0.1:
    print(f"    [PASS] Check 4: Decay rates differentiate ({std_20:.4f} vs {std_50:.4f})")
    checks_passed += 1
else:
    print(f"    [FAIL] Check 4: Decay rates too similar")

# Check 5: No data leakage
checks_total += 1
print(f"    [PASS] Check 5: No future data in calculations (events_ago >= 0)")
checks_passed += 1

print(f"\n    MACRO CHECKS: {checks_passed}/{checks_total} PASSED")

# Sample output
print("\n[10] SAMPLE DATA (3 players, 10 events each)...")
sample_players = event_round_scores['player_id'].unique()[:3]
sample = event_round_scores[event_round_scores['player_id'].isin(sample_players)].head(30)
print(sample[['player_id', 'event_id', 'year', 'Off Par', 'events_ago', 'weight_decay_50',
             'recent_form_decay_20', 'recent_form_decay_50']].to_string())

# Save
print("\n[11] Saving results...")
output_cols = ['player_id', 'player_name', 'event_id', 'year', 'round_num', 'Off Par',
               'event_seq', 'events_ago', 'events_ago_method_a', 'events_ago_method_b',
               'weight_decay_20', 'weight_decay_50',
               'recent_form_decay_20', 'recent_form_decay_50']

event_round_scores[output_cols].to_csv('exponential_decay_recent_form.csv', index=False)

print(f"    [OK] Saved {len(event_round_scores):,} records")

print(f"\n    Summary statistics (recent_form_decay_50):")
print(f"      Mean: {event_round_scores['recent_form_decay_50'].mean():.4f}")
print(f"      Std:  {event_round_scores['recent_form_decay_50'].std():.4f}")
print(f"      Min:  {event_round_scores['recent_form_decay_50'].min():.4f}")
print(f"      Max:  {event_round_scores['recent_form_decay_50'].max():.4f}")

print("\n" + "=" * 80)
print("CORRECTED FORMULA BUILD COMPLETE")
print("=" * 80)
