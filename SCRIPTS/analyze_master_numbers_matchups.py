import csv
from datetime import datetime
from collections import defaultdict

def reduce_to_single(num):
    if num <= 0:
        return None
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

def reduce_with_master(num):
    if num <= 0:
        return None
    if num in [11, 22, 33]:
        return num
    while num > 9:
        if num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num

# Read PLAYERS for birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        player = row[2].strip() if len(row) > 2 else ''
        birth = row[10].strip() if len(row) > 10 else ''
        if player and birth and player not in players_birth:
            try:
                birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                players_birth[player] = {'month': birth_obj.month, 'day': birth_obj.day, 'year': birth_obj.year}
            except:
                pass

print(f"Loaded {len(players_birth)} players\n")

# Read 2BMatchup sheet
matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

# Column indices
player_a_idx = 0
player_b_idx = 1
event_date_idx = 5
py_a_idx = 24
py_b_idx = 25
lp_score_idx = 52
lp_pick_idx = 53
wl_idx = 54

all_matchups = []
master_matchups = []
non_master_matchups = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 2):
        if not row or len(row) < wl_idx + 1:
            continue

        try:
            player_a = row[player_a_idx].strip() if player_a_idx < len(row) else ''
            player_b = row[player_b_idx].strip() if player_b_idx < len(row) else ''
            event_date = row[event_date_idx].strip() if event_date_idx < len(row) else ''

            try:
                py_a = int(row[py_a_idx].strip()) if py_a_idx < len(row) and row[py_a_idx].strip().isdigit() else None
                py_b = int(row[py_b_idx].strip()) if py_b_idx < len(row) and row[py_b_idx].strip().isdigit() else None
            except:
                continue

            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue
            lp_score = float(lp_score_str)

            lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
            if not lp_pick:
                continue

            wl = row[wl_idx].strip() if wl_idx < len(row) else ''
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            try:
                event_obj = datetime.strptime(event_date, '%m/%d/%Y')
                event_month = event_obj.month
                event_day = event_obj.day
            except:
                continue

            # Get player A info
            lp_a = None
            pd_a = None
            pm_a = None
            pd_a_master = None
            pm_a_master = None
            py_a_master = None

            if player_a in players_birth and py_a:
                birth_a = players_birth[player_a]
                py_a_calc = reduce_to_single(birth_a['month'] + birth_a['day'] + event_obj.year)
                pm_a = reduce_to_single(birth_a['month'] + event_month)
                pd_a = reduce_to_single(event_month + event_day + py_a_calc)

                py_a_master = reduce_with_master(birth_a['month'] + birth_a['day'] + event_obj.year)
                pm_a_master = reduce_with_master(birth_a['month'] + event_month)
                pd_a_master = reduce_with_master(event_month + event_day + py_a_calc)

            # Get player B info
            lp_b = None
            pd_b = None
            pm_b = None
            pd_b_master = None
            pm_b_master = None
            py_b_master = None

            if player_b in players_birth and py_b:
                birth_b = players_birth[player_b]
                py_b_calc = reduce_to_single(birth_b['month'] + birth_b['day'] + event_obj.year)
                pm_b = reduce_to_single(birth_b['month'] + event_month)
                pd_b = reduce_to_single(event_month + event_day + py_b_calc)

                py_b_master = reduce_with_master(birth_b['month'] + birth_b['day'] + event_obj.year)
                pm_b_master = reduce_with_master(birth_b['month'] + event_month)
                pd_b_master = reduce_with_master(event_month + event_day + py_b_calc)

            # Check if EITHER player has master numbers
            has_master_pd = (pd_a_master in [11, 22, 33]) or (pd_b_master in [11, 22, 33])
            has_master_pm = (pm_a_master in [11, 22, 33]) or (pm_b_master in [11, 22, 33])
            has_master_py = (py_a_master in [11, 22, 33]) or (py_b_master in [11, 22, 33])
            has_any_master = has_master_pd or has_master_pm or has_master_py

            record = {
                'player_a': player_a,
                'player_b': player_b,
                'event_date': event_date,
                'lp_score': lp_score,
                'is_win': is_win,
                'py_a': py_a,
                'py_b': py_b,
                'pd_a': pd_a,
                'pd_b': pd_b,
                'pm_a': pm_a,
                'pm_b': pm_b,
                'pd_a_master': pd_a_master,
                'pd_b_master': pd_b_master,
                'pm_a_master': pm_a_master,
                'pm_b_master': pm_b_master,
                'py_a_master': py_a_master,
                'py_b_master': py_b_master,
                'has_master_pd': has_master_pd,
                'has_master_pm': has_master_pm,
                'has_master_py': has_master_py,
                'has_any_master': has_any_master,
            }

            all_matchups.append(record)
            if has_any_master:
                master_matchups.append(record)
            else:
                non_master_matchups.append(record)

        except (ValueError, IndexError):
            continue

print(f"Total matchups: {len(all_matchups)}")
print(f"With master numbers: {len(master_matchups)} ({len(master_matchups)/len(all_matchups)*100:.1f}%)")
print(f"Without master numbers: {len(non_master_matchups)} ({len(non_master_matchups)/len(all_matchups)*100:.1f}%)\n")

# ============================================================================
# ANALYSIS 1: MASTER NUMBERS vs NON-MASTER
# ============================================================================

def analyze_winrate(data, label):
    if not data:
        return None
    wins = sum(1 for d in data if d['is_win'])
    wr = wins / len(data) * 100
    avg_score = sum(d['lp_score'] for d in data) / len(data)

    # Threshold analysis
    above_3 = len([d for d in data if d['lp_score'] > 3])
    below_1 = len([d for d in data if d['lp_score'] < 1])

    return {
        'label': label,
        'n': len(data),
        'wins': wins,
        'wr': wr,
        'avg_score': avg_score,
        'above_3_pct': above_3 / len(data) * 100 if data else 0,
        'below_1_pct': below_1 / len(data) * 100 if data else 0,
    }

print("=" * 140)
print("MASTER NUMBERS IMPACT ON MATCHUP PERFORMANCE")
print("=" * 140)

master_result = analyze_winrate(master_matchups, "With Master Numbers")
non_master_result = analyze_winrate(non_master_matchups, "Without Master Numbers")
all_result = analyze_winrate(all_matchups, "All Matchups")

print(f"\n{master_result['label']}:")
print(f"  Matchups: {master_result['n']}")
print(f"  Win Rate: {master_result['wr']:.1f}%")
print(f"  Avg LP Score: {master_result['avg_score']:.2f}")
print(f"  Above +3: {master_result['above_3_pct']:.1f}%")
print(f"  Below +1: {master_result['below_1_pct']:.1f}%")

print(f"\n{non_master_result['label']}:")
print(f"  Matchups: {non_master_result['n']}")
print(f"  Win Rate: {non_master_result['wr']:.1f}%")
print(f"  Avg LP Score: {non_master_result['avg_score']:.2f}")
print(f"  Above +3: {non_master_result['above_3_pct']:.1f}%")
print(f"  Below +1: {non_master_result['below_1_pct']:.1f}%")

print(f"\nDifference (Master - Non-Master):")
print(f"  WR: {master_result['wr'] - non_master_result['wr']:+.1f}pp")
print(f"  Score: {master_result['avg_score'] - non_master_result['avg_score']:+.2f}")

# ============================================================================
# ANALYSIS 2: MASTER NUMBER TYPES
# ============================================================================

print("\n\n" + "=" * 140)
print("BREAKDOWN BY MASTER NUMBER TYPE")
print("=" * 140)

pd_master = [d for d in master_matchups if d['has_master_pd']]
pm_master = [d for d in master_matchups if d['has_master_pm']]
py_master = [d for d in master_matchups if d['has_master_py']]

for data, label in [(pd_master, "Personal Day Master (11/22/33)"),
                     (pm_master, "Personal Month Master (11/22/33)"),
                     (py_master, "Personal Year Master (11/22/33)")]:
    result = analyze_winrate(data, label)
    if result and result['n'] > 0:
        print(f"\n{result['label']}:")
        print(f"  Matchups: {result['n']}")
        print(f"  Win Rate: {result['wr']:.1f}%")
        print(f"  Avg LP Score: {result['avg_score']:.2f}")

# ============================================================================
# ANALYSIS 3: LIFE PATH PATTERNING WITH MASTER NUMBERS
# ============================================================================

print("\n\n" + "=" * 140)
print("LIFE PATH PATTERNS IN MASTER NUMBER MATCHUPS")
print("=" * 140)

print("\nFiltering to Master Number matchups only, analyzing by Life Path value...\n")

lp_buckets = defaultdict(list)
for d in master_matchups:
    for py_val in [d['py_a'], d['py_b']]:
        if py_val and 1 <= py_val <= 9:
            lp_buckets[py_val].append(d)

print(f"{'LP':<5} {'Matchups':<12} {'Win Rate':<12} {'Avg Score':<12} {'Above+3':<10} {'Status':<20}")
print("-" * 80)

for lp_val in range(1, 10):
    data = lp_buckets[lp_val]
    if len(data) < 3:
        continue

    result = analyze_winrate(data, f"LP{lp_val}")
    wins_str = f"{result['wins']}/{result['n']}"

    # Status
    if result['wr'] >= 60:
        status = "STRONG"
    elif result['wr'] >= 55:
        status = "Good"
    elif result['wr'] >= 50:
        status = "Neutral"
    else:
        status = "WEAK"

    print(f"{lp_val:<5} {wins_str:<12} {result['wr']:>10.1f}% {result['avg_score']:>11.2f} {result['above_3_pct']:>9.1f}% {status:<20}")

# ============================================================================
# ANALYSIS 4: PERSONAL YEAR PATTERNS WITH MASTER NUMBERS
# ============================================================================

print("\n\n" + "=" * 140)
print("PERSONAL YEAR PATTERNS IN MASTER NUMBER MATCHUPS")
print("=" * 140)

print("\nMaster number matchups only, analyzing by Personal Year value...\n")

py_buckets = defaultdict(list)
for d in master_matchups:
    for py_val in [d['py_a'], d['py_b']]:
        if py_val and 1 <= py_val <= 9:
            py_buckets[py_val].append(d)

print(f"{'PY':<5} {'Matchups':<12} {'Win Rate':<12} {'Avg Score':<12} {'Above+3':<10} {'Status':<20}")
print("-" * 80)

for py_val in range(1, 10):
    data = py_buckets[py_val]
    if len(data) < 3:
        continue

    result = analyze_winrate(data, f"PY{py_val}")
    wins_str = f"{result['wins']}/{result['n']}"

    if result['wr'] >= 60:
        status = "STRONG"
    elif result['wr'] >= 55:
        status = "Good"
    elif result['wr'] >= 50:
        status = "Neutral"
    else:
        status = "WEAK"

    print(f"{py_val:<5} {wins_str:<12} {result['wr']:>10.1f}% {result['avg_score']:>11.2f} {result['above_3_pct']:>9.1f}% {status:<20}")

# ============================================================================
# ANALYSIS 5: PERSONAL DAY PATTERNS WITH MASTER NUMBERS
# ============================================================================

print("\n\n" + "=" * 140)
print("PERSONAL DAY PATTERNS IN MASTER NUMBER MATCHUPS")
print("=" * 140)

print("\nMaster number matchups only, analyzing by Personal Day value (including master 11/22/33)...\n")

pd_buckets = defaultdict(list)
for d in master_matchups:
    for pd_val in [d['pd_a_master'], d['pd_b_master']]:
        if pd_val and (1 <= pd_val <= 9 or pd_val in [11, 22, 33]):
            pd_buckets[pd_val].append(d)

print(f"{'PD':<5} {'Matchups':<12} {'Win Rate':<12} {'Avg Score':<12} {'Above+3':<10} {'Status':<20}")
print("-" * 80)

pd_values = sorted(list(set(pd_buckets.keys())))
for pd_val in pd_values:
    data = pd_buckets[pd_val]
    if len(data) < 3:
        continue

    result = analyze_winrate(data, f"PD{pd_val}")
    wins_str = f"{result['wins']}/{result['n']}"

    label = f"PD{pd_val}{'*' if pd_val in [11,22,33] else ''}"

    if result['wr'] >= 60:
        status = "STRONG"
    elif result['wr'] >= 55:
        status = "Good"
    elif result['wr'] >= 50:
        status = "Neutral"
    else:
        status = "WEAK"

    print(f"{label:<5} {wins_str:<12} {result['wr']:>10.1f}% {result['avg_score']:>11.2f} {result['above_3_pct']:>9.1f}% {status:<20}")

print("\n* = Master Number (11, 22, or 33)")

# ============================================================================
# ANALYSIS 6: COMBO ANALYSIS (Master + Specific LP/PY/PD)
# ============================================================================

print("\n\n" + "=" * 140)
print("MASTER NUMBER COMBOS: Best Performing Combinations")
print("=" * 140)

combo_results = []

for pd_val in pd_values:
    pd_data = pd_buckets[pd_val]

    for lp_val in range(1, 10):
        lp_data = lp_buckets[lp_val]

        # Find intersection
        combo_data = [d for d in master_matchups if
                      (d['pd_a_master'] == pd_val or d['pd_b_master'] == pd_val) and
                      (d['py_a'] == lp_val or d['py_b'] == lp_val)]

        if len(combo_data) >= 3:
            wins = sum(1 for d in combo_data if d['is_win'])
            wr = wins / len(combo_data) * 100
            avg_score = sum(d['lp_score'] for d in combo_data) / len(combo_data)

            combo_results.append({
                'combo': f"PD{pd_val}+PY{lp_val}",
                'n': len(combo_data),
                'wr': wr,
                'avg_score': avg_score,
                'wins': wins,
            })

# Sort by win rate
combo_results = sorted(combo_results, key=lambda x: x['wr'], reverse=True)

print(f"\n{'Combo':<15} {'Matchups':<12} {'Win Rate':<12} {'Avg Score':<12}")
print("-" * 60)

for combo in combo_results[:15]:
    print(f"{combo['combo']:<15} {combo['n']:<12} {combo['wr']:>10.1f}% {combo['avg_score']:>11.2f}")

print("\n" + "=" * 140)
print("SUMMARY")
print("=" * 140)

print(f"""
Master Numbers in Matchups:
  Total matchups analyzed: {len(all_matchups)}
  With master numbers: {len(master_matchups)} ({len(master_matchups)/len(all_matchups)*100:.1f}%)

Master Number Impact:
  Win Rate with masters: {master_result['wr']:.1f}%
  Win Rate without masters: {non_master_result['wr']:.1f}%
  Difference: {master_result['wr'] - non_master_result['wr']:+.1f}pp

Avg LP Score:
  With masters: {master_result['avg_score']:+.2f}
  Without masters: {non_master_result['avg_score']:+.2f}
  Difference: {master_result['avg_score'] - non_master_result['avg_score']:+.2f}
""")
