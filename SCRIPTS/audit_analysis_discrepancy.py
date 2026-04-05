"""
Audit: Where does the ANALYSIS_v2 discrepancy come from?

Compare:
1. Golf_Analytics combos (player-event-year)
2. ANALYSIS_v2 rows
3. Expected vs actual

This will show exactly what's driving the 22k row difference.
"""

import pandas as pd

print("=" * 80)
print("AUDIT: ANALYSIS_v2 Row Discrepancy")
print("=" * 80)

# Load Golf_Analytics to get unique combos
print("\n[1] Reading Golf_Analytics...")
ga = pd.read_csv('ANALYSIS_v2_with_element.csv')  # This is derived from Golf_Analytics

print(f"    Total rows in ANALYSIS_v2: {len(ga):,}")

# Count unique player-event-year combos
print("\n[2] Analyzing unique combos...")
combos = ga.groupby(['player_name', 'event_name', 'year']).agg({
    'round_num': 'count',
    'round_type': lambda x: list(x)
}).reset_index()
combos.columns = ['player_name', 'event_name', 'year', 'rounds_per_combo', 'round_types']

print(f"    Unique player-event-year combos: {len(combos):,}")
print(f"    Expected rows (if all have 4 rounds): {len(combos) * 4:,}")
print(f"    Actual rows: {len(ga):,}")

# Calculate expected rounds per combo
print("\n[3] Rounds per combo breakdown...")
rounds_distribution = combos['rounds_per_combo'].value_counts().sort_index()
print(rounds_distribution)

# Where are the "REMOVE" rounds?
print("\n[4] REMOVE round analysis...")
remove_count = (ga['round_type'] == 'Remove').sum()
remove_rows_per_combo = ga[ga['round_type'] == 'Remove'].groupby(['player_name', 'event_name', 'year']).size()

print(f"    Total REMOVE rounds: {remove_count:,}")
print(f"    Combos with REMOVE rounds: {len(remove_rows_per_combo):,}")

if len(remove_rows_per_combo) > 0:
    print(f"    Remove distribution:")
    print(remove_rows_per_combo.value_counts().sort_index())

# Withdrawn rounds (score is blank)
print("\n[5] Withdrawn/incomplete rounds...")
blank_score = (ga['score'] == '').sum()
print(f"    Rounds with blank score: {blank_score:,}")

# Rounds by type
print("\n[6] Round type distribution...")
print(ga['round_type'].value_counts())

# Calculate what the discrepancy actually is
print("\n[7] Discrepancy analysis...")
expected_if_all_4_rounds = len(combos) * 4
actual_rows = len(ga)
difference = expected_if_all_4_rounds - actual_rows

print(f"    Expected (all 4 rounds per combo): {expected_if_all_4_rounds:,}")
print(f"    Actual rows: {actual_rows:,}")
print(f"    Difference: {difference:,}")
print(f"    Average rounds per combo: {actual_rows / len(combos):.2f}")

# Find combos with less than 4 rounds
print("\n[8] Combos with < 4 rounds...")
incomplete = combos[combos['rounds_per_combo'] < 4]
print(f"    Count: {len(incomplete):,}")
if len(incomplete) > 0:
    print(f"\n    Sample of incomplete combos:")
    for idx, row in incomplete.head(10).iterrows():
        print(f"      {row['player_name']:20} {row['event_name']:30} {row['year']} ({int(row['rounds_per_combo'])} rounds) — {row['round_types']}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"""
ANALYSIS_v2 has {len(combos):,} unique tournaments but {actual_rows:,} rows.

This means {difference:,} "missing" rounds from the maximum possible {expected_if_all_4_rounds:,}.

Likely causes:
  1. Some tournaments have < 4 rounds (withdrawn, cut, incomplete)
  2. REMOVE rounds are marked but rows still created
  3. Newly added events with incomplete data
  4. Events that only had 1, 2, or 3 scoring rounds

Action: Check which events were added recently or have incomplete scoring.
""")

print("=" * 80)
