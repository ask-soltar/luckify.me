import csv
from collections import defaultdict
from datetime import datetime
import statistics

def reduce_with_master(num):
    """Reduce to single digit or preserve master numbers"""
    if num <= 0:
        return None
    if num in [11, 22, 33]:
        return num
    while num > 9:
        if num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num

# ============================================================================
# Load player birth data first
# ============================================================================
print("=" * 140)
print("MASTER NUMBER 22 (Personal Day) — ANALYSIS SHEET PERFORMANCE vs AVERAGE")
print("=" * 140)
print()

players_birth = {}
with open("Golf Historics v3 - Golf_Analytics.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        player = row[2].strip() if len(row) > 2 else ''
        birth = row[10].strip() if len(row) > 10 else ''
        if player and birth and player not in players_birth:
            try:
                birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                players_birth[player] = {'month': birth_obj.month, 'day': birth_obj.day, 'year': birth_obj.year}
            except:
                pass

print(f"Loaded {len(players_birth)} players with birth data\n")

# ============================================================================
# Read ANALYSIS v3 sheet and extract PD22 vs baseline
# ============================================================================

analysis_data = []
pd22_data = []

with open("ANALYSIS_v3_export.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    try:
        player_idx = header.index("player_name")
        event_idx = header.index("event_name")
        year_idx = header.index("year")
        vs_avg_idx = header.index("vs_avg")
        off_par_idx = header.index("off_par")
        condition_idx = header.index("condition")
        round_type_idx = header.index("round_type")
    except ValueError as e:
        print(f"ERROR: Column not found: {e}")
        print(f"Available columns: {header}")
        exit(1)

    for row in reader:
        if not row or len(row) < max(vs_avg_idx, off_par_idx, round_type_idx) + 1:
            continue

        try:
            player = row[player_idx].strip() if player_idx < len(row) else ''
            event = row[event_idx].strip() if event_idx < len(row) else ''
            year_str = row[year_idx].strip() if year_idx < len(row) else ''
            vs_avg_str = row[vs_avg_idx].strip() if vs_avg_idx < len(row) else ''
            off_par_str = row[off_par_idx].strip() if off_par_idx < len(row) else ''
            condition = row[condition_idx].strip() if condition_idx < len(row) else ''
            round_type = row[round_type_idx].strip() if round_type_idx < len(row) else ''

            if not player or not vs_avg_str or player not in players_birth:
                continue

            vs_avg = float(vs_avg_str) if vs_avg_str and vs_avg_str not in ['#REF!', ''] else None
            off_par = float(off_par_str) if off_par_str and off_par_str not in ['#REF!', ''] else None

            if vs_avg is None:
                continue

            # Calculate Personal Day
            birth_info = players_birth[player]
            year = int(year_str) if year_str and year_str.isdigit() else None

            # We don't have event_date in ANALYSIS, so we can't calculate PD precisely
            # Instead, we'll need to estimate or skip - for now, skip rows without PD data
            # Actually, let's calculate from what we can infer or use a proxy
            # Since we don't have the event date, we can't calculate PD accurately
            # Let's skip this approach and instead rely on getting event dates another way

            # For now, let's work with what we have - we need event dates
            # which should be in the EVENTS sheet or we need to add them to ANALYSIS
            continue

        except (ValueError, IndexError):
            continue

print(f"Total ANALYSIS records loaded: {len(analysis_data)}")
print(f"PD22 records found: {len(pd22_data)}\n")

# ============================================================================
# Calculate baseline (all data) vs PD22
# ============================================================================

baseline_vs_avg = statistics.mean([r['vs_avg'] for r in analysis_data])
baseline_off_par = statistics.mean([r['off_par'] for r in analysis_data if r['off_par'] is not None])

pd22_vs_avg = statistics.mean([r['vs_avg'] for r in pd22_data])
pd22_off_par = statistics.mean([r['off_par'] for r in pd22_data if r['off_par'] is not None])

print("=" * 140)
print("OVERALL PERFORMANCE")
print("=" * 140)
print(f"\nBaseline (All Rounds):")
print(f"  vs_avg: {baseline_vs_avg:+.3f}")
print(f"  off_par: {baseline_off_par:+.3f}")

print(f"\nPD22 Performance:")
print(f"  vs_avg: {pd22_vs_avg:+.3f}")
print(f"  off_par: {pd22_off_par:+.3f}")

print(f"\nPD22 vs Baseline:")
print(f"  vs_avg edge: {pd22_vs_avg - baseline_vs_avg:+.3f} ({(pd22_vs_avg - baseline_vs_avg) / abs(baseline_vs_avg) * 100:+.1f}%)")
if baseline_off_par:
    print(f"  off_par edge: {pd22_off_par - baseline_off_par:+.3f} ({(pd22_off_par - baseline_off_par) / abs(baseline_off_par) * 100:+.1f}%)")

# ============================================================================
# Win rate analysis (vs_avg > 0)
# ============================================================================

baseline_wins = sum(1 for r in analysis_data if r['vs_avg'] > 0)
baseline_wr = baseline_wins / len(analysis_data) * 100 if analysis_data else 0

pd22_wins = sum(1 for r in pd22_data if r['vs_avg'] > 0)
pd22_wr = pd22_wins / len(pd22_data) * 100 if pd22_data else 0

print(f"\nWin Rate (vs_avg > 0):")
print(f"  Baseline: {baseline_wins} / {len(analysis_data)} = {baseline_wr:.1f}%")
print(f"  PD22: {pd22_wins} / {len(pd22_data)} = {pd22_wr:.1f}%")
print(f"  Edge: {pd22_wr - baseline_wr:+.1f}pp")

# ============================================================================
# Breakdown by Condition
# ============================================================================

print("\n" + "=" * 140)
print("BY CONDITION")
print("=" * 140)

for condition in ['Calm', 'Moderate', 'Tough']:
    baseline_cond = [r for r in analysis_data if r['condition'] == condition]
    pd22_cond = [r for r in pd22_data if r['condition'] == condition]

    if not baseline_cond or not pd22_cond:
        continue

    baseline_avg = statistics.mean([r['vs_avg'] for r in baseline_cond])
    pd22_avg = statistics.mean([r['vs_avg'] for r in pd22_cond])

    baseline_wr_cond = sum(1 for r in baseline_cond if r['vs_avg'] > 0) / len(baseline_cond) * 100
    pd22_wr_cond = sum(1 for r in pd22_cond if r['vs_avg'] > 0) / len(pd22_cond) * 100

    print(f"\n{condition}:")
    print(f"  Baseline: vs_avg={baseline_avg:+.3f}, WR={baseline_wr_cond:.1f}% (n={len(baseline_cond)})")
    print(f"  PD22:     vs_avg={pd22_avg:+.3f}, WR={pd22_wr_cond:.1f}% (n={len(pd22_cond)})")
    print(f"  Edge:     {pd22_avg - baseline_avg:+.3f} ({pd22_wr_cond - baseline_wr_cond:+.1f}pp WR)")

# ============================================================================
# Breakdown by Round Type
# ============================================================================

print("\n" + "=" * 140)
print("BY ROUND TYPE")
print("=" * 140)

for rtype in ['Open', 'Positioning', 'Closing']:
    baseline_rt = [r for r in analysis_data if r['round_type'] == rtype]
    pd22_rt = [r for r in pd22_data if r['round_type'] == rtype]

    if not baseline_rt or not pd22_rt:
        continue

    baseline_avg = statistics.mean([r['vs_avg'] for r in baseline_rt])
    pd22_avg = statistics.mean([r['vs_avg'] for r in pd22_rt])

    baseline_wr_rt = sum(1 for r in baseline_rt if r['vs_avg'] > 0) / len(baseline_rt) * 100
    pd22_wr_rt = sum(1 for r in pd22_rt if r['vs_avg'] > 0) / len(pd22_rt) * 100

    print(f"\n{rtype}:")
    print(f"  Baseline: vs_avg={baseline_avg:+.3f}, WR={baseline_wr_rt:.1f}% (n={len(baseline_rt)})")
    print(f"  PD22:     vs_avg={pd22_avg:+.3f}, WR={pd22_wr_rt:.1f}% (n={len(pd22_rt)})")
    print(f"  Edge:     {pd22_avg - baseline_avg:+.3f} ({pd22_wr_rt - baseline_wr_rt:+.1f}pp WR)")

# ============================================================================
# Breakdown by Condition + Round Type (2D matrix)
# ============================================================================

print("\n" + "=" * 140)
print("BY CONDITION + ROUND TYPE")
print("=" * 140)

print(f"\n{'Condition':<12} {'Round Type':<15} {'Baseline (vs_avg)':<20} {'PD22 (vs_avg)':<20} {'Edge':<12} {'PD22 WR%':<10} {'n':<6}")
print("-" * 140)

for condition in ['Calm', 'Moderate', 'Tough']:
    for rtype in ['Open', 'Positioning', 'Closing']:
        baseline_combo = [r for r in analysis_data if r['condition'] == condition and r['round_type'] == rtype]
        pd22_combo = [r for r in pd22_data if r['condition'] == condition and r['round_type'] == rtype]

        if not baseline_combo or not pd22_combo:
            continue

        baseline_avg = statistics.mean([r['vs_avg'] for r in baseline_combo])
        pd22_avg = statistics.mean([r['vs_avg'] for r in pd22_combo])
        edge = pd22_avg - baseline_avg

        pd22_wr_combo = sum(1 for r in pd22_combo if r['vs_avg'] > 0) / len(pd22_combo) * 100

        print(f"{condition:<12} {rtype:<15} {baseline_avg:>+8.3f}             {pd22_avg:>+8.3f}             {edge:>+7.3f}      {pd22_wr_combo:>6.1f}%    {len(pd22_combo):<6}")

# ============================================================================
# Summary Statistics
# ============================================================================

print("\n" + "=" * 140)
print("SUMMARY")
print("=" * 140)
print(f"""
Master Number 22 (Personal Day 22) in ANALYSIS Sheet:

SAMPLE SIZE:
  Total rounds analyzed: {len(analysis_data)}
  PD22 rounds: {len(pd22_data)} ({len(pd22_data) / len(analysis_data) * 100:.1f}%)

PROFITABILITY (vs Field Average):
  Baseline: {baseline_vs_avg:+.3f} vs_avg, {baseline_wr:.1f}% WR
  PD22:     {pd22_vs_avg:+.3f} vs_avg, {pd22_wr:.1f}% WR
  Edge:     {pd22_vs_avg - baseline_vs_avg:+.3f} ({pd22_wr - baseline_wr:+.1f}pp)

  Status: {'✓ POSITIVE EDGE' if pd22_vs_avg > baseline_vs_avg else '✗ NEGATIVE EDGE'}

CONSISTENCY (vs Own Par):
  Baseline: {baseline_off_par:+.3f} off_par
  PD22:     {pd22_off_par:+.3f} off_par
  Edge:     {pd22_off_par - baseline_off_par:+.3f}

  Status: {'✓ BEATS OWN PAR' if pd22_off_par > baseline_off_par else '✗ UNDERPERFORMS PAR'}

INTERPRETATION:
- PD22 shows {'POSITIVE' if pd22_vs_avg > baseline_vs_avg else 'NEGATIVE'} edge vs field average
- PD22 {'beats' if pd22_off_par > baseline_off_par else 'underperforms'} their own historical par
- Best performance in: [Check breakdown tables above]
""")
