import csv
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
# Load player birth data
# ============================================================================
print("=" * 140)
print("MASTER NUMBER 22 (Personal Day) — GOLF_ANALYTICS PERFORMANCE vs AVERAGE")
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
# Read Golf_Analytics and calculate PD for each round
# ============================================================================

analysis_data = []
pd22_data = []

with open("Golf Historics v3 - Golf_Analytics.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Map column indices
    player_idx = 2        # C - Player name
    r1_date_idx = 12      # M - Round 1 Date
    r1_score_idx = 3      # D - R1 Score
    r1_vs_avg_idx = 38    # AM - R1 vs Avg
    r1_cond_idx = 42      # AQ - R1 Condition
    r1_rtype_idx = 46     # AU - R1 Round Type
    r1_par_idx = 8        # I - Par (or use from EVENTS)

    for row in reader:
        if not row or len(row) < max(r1_date_idx, r1_vs_avg_idx) + 1:
            continue

        try:
            player = row[player_idx].strip() if player_idx < len(row) else ''
            if not player or player not in players_birth:
                continue

            # Process all 4 rounds
            for round_num in range(1, 5):
                # Calculate column indices for this round
                score_offset = round_num - 1
                date_idx = 12 + round_num  # M=12, N=13, O=14, P=15
                score_idx = 3 + score_offset  # D, E, F, G
                vs_avg_idx = 38 + round_num  # AM, AN, AO, AP
                cond_idx = 42 + round_num  # AQ, AR, AS, AT
                rtype_idx = 46 + round_num  # AU, AV, AW, AX

                # Get data
                date_str = row[date_idx].strip() if date_idx < len(row) else ''
                score_str = row[score_idx].strip() if score_idx < len(row) else ''
                vs_avg_str = row[vs_avg_idx].strip() if vs_avg_idx < len(row) else ''
                condition = row[cond_idx].strip() if cond_idx < len(row) else ''
                rtype = row[rtype_idx].strip() if rtype_idx < len(row) else ''

                # Skip invalid rows
                if not date_str or not vs_avg_str or score_str in ['', '#REF!', 'Withdrawn', 'Cut']:
                    continue
                if vs_avg_str in ['', '#REF!']:
                    continue

                try:
                    score = float(score_str)
                    vs_avg = float(vs_avg_str)
                    event_date = datetime.strptime(date_str, '%m/%d/%Y')
                except:
                    continue

                # Calculate Personal Day
                birth_info = players_birth[player]
                py = reduce_with_master(birth_info['month'] + birth_info['day'] + event_date.year)
                if not py:
                    continue

                pd = reduce_with_master(event_date.month + event_date.day + py)

                record = {
                    'player': player,
                    'vs_avg': vs_avg,
                    'score': score,
                    'condition': condition,
                    'round_type': rtype,
                    'pd': pd,
                    'date': date_str,
                }

                analysis_data.append(record)

                if pd == 22:
                    pd22_data.append(record)

        except (ValueError, IndexError):
            continue

print(f"Total Golf_Analytics records loaded: {len(analysis_data)}")
print(f"PD22 records found: {len(pd22_data)}\n")

if not analysis_data or not pd22_data:
    print("ERROR: No data found to analyze")
    exit(1)

# ============================================================================
# Calculate baseline (all data) vs PD22
# ============================================================================

baseline_vs_avg = statistics.mean([r['vs_avg'] for r in analysis_data])
pd22_vs_avg = statistics.mean([r['vs_avg'] for r in pd22_data])

print("=" * 140)
print("OVERALL PERFORMANCE")
print("=" * 140)
print(f"\nBaseline (All Rounds):")
print(f"  vs_avg: {baseline_vs_avg:+.3f}")
print(f"  n: {len(analysis_data)}")

print(f"\nPD22 Performance:")
print(f"  vs_avg: {pd22_vs_avg:+.3f}")
print(f"  n: {len(pd22_data)}")

edge = pd22_vs_avg - baseline_vs_avg
pct_edge = (edge / abs(baseline_vs_avg) * 100) if baseline_vs_avg != 0 else 0

print(f"\nPD22 vs Baseline:")
print(f"  Edge: {edge:+.3f} ({pct_edge:+.1f}%)")

# ============================================================================
# Win rate analysis (vs_avg > 0)
# ============================================================================

baseline_wins = sum(1 for r in analysis_data if r['vs_avg'] > 0)
baseline_wr = baseline_wins / len(analysis_data) * 100

pd22_wins = sum(1 for r in pd22_data if r['vs_avg'] > 0)
pd22_wr = pd22_wins / len(pd22_data) * 100

print(f"\nWin Rate (vs_avg > 0):")
print(f"  Baseline: {baseline_wins:>5} / {len(analysis_data):<5} = {baseline_wr:>6.1f}%")
print(f"  PD22:     {pd22_wins:>5} / {len(pd22_data):<5} = {pd22_wr:>6.1f}%")
print(f"  Edge:     {pd22_wr - baseline_wr:>6.1f}pp")

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
    edge_cond = pd22_avg - baseline_avg

    baseline_wr_cond = sum(1 for r in baseline_cond if r['vs_avg'] > 0) / len(baseline_cond) * 100
    pd22_wr_cond = sum(1 for r in pd22_cond if r['vs_avg'] > 0) / len(pd22_cond) * 100

    print(f"\n{condition}:")
    print(f"  Baseline: vs_avg={baseline_avg:>+.3f}, WR={baseline_wr_cond:>6.1f}% (n={len(baseline_cond):<5})")
    print(f"  PD22:     vs_avg={pd22_avg:>+.3f}, WR={pd22_wr_cond:>6.1f}% (n={len(pd22_cond):<5})")
    print(f"  Edge:     {edge_cond:>+.3f}         {pd22_wr_cond - baseline_wr_cond:>+6.1f}pp")

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
    edge_rt = pd22_avg - baseline_avg

    baseline_wr_rt = sum(1 for r in baseline_rt if r['vs_avg'] > 0) / len(baseline_rt) * 100
    pd22_wr_rt = sum(1 for r in pd22_rt if r['vs_avg'] > 0) / len(pd22_rt) * 100

    print(f"\n{rtype}:")
    print(f"  Baseline: vs_avg={baseline_avg:>+.3f}, WR={baseline_wr_rt:>6.1f}% (n={len(baseline_rt):<5})")
    print(f"  PD22:     vs_avg={pd22_avg:>+.3f}, WR={pd22_wr_rt:>6.1f}% (n={len(pd22_rt):<5})")
    print(f"  Edge:     {edge_rt:>+.3f}         {pd22_wr_rt - baseline_wr_rt:>+6.1f}pp")

# ============================================================================
# Breakdown by Condition + Round Type (2D matrix)
# ============================================================================

print("\n" + "=" * 140)
print("BY CONDITION + ROUND TYPE (2D ANALYSIS)")
print("=" * 140)

print(f"\n{'Condition':<12} {'Round Type':<15} {'Baseline':<15} {'PD22':<15} {'Edge':<12} {'WR Edge':<10} {'n':<6}")
print("-" * 140)

for condition in ['Calm', 'Moderate', 'Tough']:
    for rtype in ['Open', 'Positioning', 'Closing']:
        baseline_combo = [r for r in analysis_data if r['condition'] == condition and r['round_type'] == rtype]
        pd22_combo = [r for r in pd22_data if r['condition'] == condition and r['round_type'] == rtype]

        if not baseline_combo or not pd22_combo:
            continue

        baseline_avg = statistics.mean([r['vs_avg'] for r in baseline_combo])
        pd22_avg = statistics.mean([r['vs_avg'] for r in pd22_combo])
        edge_combo = pd22_avg - baseline_avg

        pd22_wr_combo = sum(1 for r in pd22_combo if r['vs_avg'] > 0) / len(pd22_combo) * 100
        baseline_wr_combo = sum(1 for r in baseline_combo if r['vs_avg'] > 0) / len(baseline_combo) * 100
        wr_edge = pd22_wr_combo - baseline_wr_combo

        print(f"{condition:<12} {rtype:<15} {baseline_avg:>+8.3f}     {pd22_avg:>+8.3f}     {edge_combo:>+7.3f}    {wr_edge:>+6.1f}pp  {len(pd22_combo):<6}")

# ============================================================================
# Summary
# ============================================================================

print("\n" + "=" * 140)
print("SUMMARY")
print("=" * 140)
print(f"""
MASTER NUMBER 22 (Personal Day) ANALYSIS

SAMPLE SIZE:
  Total rounds: {len(analysis_data)}
  PD22 rounds:  {len(pd22_data)} ({len(pd22_data) / len(analysis_data) * 100:.1f}%)

PROFITABILITY (vs Field Average):
  Baseline: {baseline_vs_avg:+.3f} vs_avg, {baseline_wr:.1f}% WR
  PD22:     {pd22_vs_avg:+.3f} vs_avg, {pd22_wr:.1f}% WR
  Edge:     {edge:+.3f} vs_avg ({pct_edge:+.1f}%), {pd22_wr - baseline_wr:+.1f}pp WR

  Status: {'✓ POSITIVE EDGE' if edge > 0 else '✗ NEGATIVE EDGE'}

TOP PERFORMING DIMENSIONS:
  [Check 2D analysis table above for best Condition + Round Type combo]

CONCLUSION:
Master Number 22 (Personal Day) shows a {('POSITIVE' if edge > 0 else 'NEGATIVE')} edge of {edge:+.3f} vs_avg
across {len(pd22_data)} rounds compared to baseline of {baseline_vs_avg:+.3f}.
""")
