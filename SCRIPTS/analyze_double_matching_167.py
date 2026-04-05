import csv
from datetime import datetime

# Read PLAYERS sheet to get birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("Reading player birth dates...")

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    player_name_idx = None
    birthday_idx = None

    for i, col in enumerate(header):
        col_clean = col.strip().lower()
        if col_clean == 'player':
            player_name_idx = i
        if 'birthday' in col_clean:
            birthday_idx = i

    if player_name_idx is None or birthday_idx is None:
        print(f"Warning: Could not find columns")
    else:
        for row in reader:
            if player_name_idx < len(row) and birthday_idx < len(row):
                player = row[player_name_idx].strip()
                birth = row[birthday_idx].strip()

                if player and birth and player not in players_birth:
                    try:
                        birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                        players_birth[player] = (birth_obj.month, birth_obj.day)
                    except:
                        pass

        print(f"Loaded {len(players_birth)} players with birth dates\n")

# Process 2BMatchup sheet
matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

player_a_idx = 0
player_b_idx = 1
event_date_idx = 5
py_a_idx = 24
py_b_idx = 25
lp_score_idx = 52
lp_pick_idx = 53
wl_idx = 54

# Analysis categories
filters = {
    'all_picks': [],
    'both_pd_same_1': [],    # Both players have PD=1
    'both_pd_same_6': [],    # Both players have PD=6
    'both_pd_same_7': [],    # Both players have PD=7
    'both_py_same_1': [],    # Both players have PY=1
    'both_py_same_6': [],    # Both players have PY=6
    'both_py_same_7': [],    # Both players have PY=7
}

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

            base_data = {'lp_score': lp_score, 'result': is_win}
            filters['all_picks'].append(base_data)

            # Calculate PD for both players
            pd_a = None
            pd_b = None

            if player_a in players_birth and py_a:
                pd_a = (event_month + event_day + py_a)
                while pd_a > 9:
                    pd_a = sum(int(d) for d in str(pd_a))

            if player_b in players_birth and py_b:
                pd_b = (event_month + event_day + py_b)
                while pd_b > 9:
                    pd_b = sum(int(d) for d in str(pd_b))

            # Check for matching doubles
            if pd_a is not None and pd_b is not None and pd_a == pd_b:
                if pd_a == 1:
                    filters['both_pd_same_1'].append(base_data)
                elif pd_a == 6:
                    filters['both_pd_same_6'].append(base_data)
                elif pd_a == 7:
                    filters['both_pd_same_7'].append(base_data)

            if py_a is not None and py_b is not None:
                if py_a == py_b:
                    if py_a == 1:
                        filters['both_py_same_1'].append(base_data)
                    elif py_a == 6:
                        filters['both_py_same_6'].append(base_data)
                    elif py_a == 7:
                        filters['both_py_same_7'].append(base_data)

        except (ValueError, IndexError):
            continue

# Analysis function
def analyze_filter(name, data):
    if not data or len(data) < 5:
        return None

    wins = sum(1 for d in data if d['result'])
    wr = (wins / len(data) * 100)

    thresholds = list(range(-2, 9))
    best_threshold = None
    best_wr = 0
    best_picks = 0

    for threshold in thresholds:
        filtered = [d for d in data if d['lp_score'] > threshold]
        if len(filtered) >= 5:
            wins_f = sum(1 for d in filtered if d['result'])
            wr_f = (wins_f / len(filtered) * 100)
            if wr_f > best_wr:
                best_wr = wr_f
                best_threshold = threshold
                best_picks = len(filtered)

    return {
        'name': name,
        'total_picks': len(data),
        'baseline_wr': wr,
        'best_threshold': best_threshold,
        'best_wr': best_wr,
        'best_picks': best_picks,
        'edge': (best_wr - wr) if best_wr > 0 else 0,
        'data': data
    }

# Run analysis
print("=" * 120)
print("DOUBLE MATCHING ANALYSIS: Both Players Same Personal Day/Year in [1,6,7]")
print("=" * 120)

results = []
for filter_name, filter_data in filters.items():
    result = analyze_filter(filter_name.replace('_', ' ').title(), filter_data)
    if result:
        results.append(result)

# Summary table
print("\n" + "=" * 120)
print("SUMMARY TABLE")
print("=" * 120)
print(f"\n{'Filter':<35} {'Total':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Edge':<10}")
print("-" * 90)

for r in sorted(results, key=lambda x: x['edge'], reverse=True):
    edge = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    print(f"{r['name']:<35} {r['total_picks']:<10} {r['baseline_wr']:<11.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {edge:<10}")

# Separate by PD and PY
all_picks = [r for r in results if 'All Picks' in r['name']][0]
pd_results = [r for r in results if 'Both Pd' in r['name']]
py_results = [r for r in results if 'Both Py' in r['name']]

print("\n" + "=" * 120)
print("PERSONAL DAY DOUBLES (Both Players Same PD in 1/6/7)")
print("=" * 120)
print(f"\n{'Filter':<30} {'Picks':<10} {'Baseline':<12} {'Best Threshold':<15} {'Best WR':<10} {'Edge':<10}")
print("-" * 85)

for r in sorted(pd_results, key=lambda x: x['edge'], reverse=True):
    edge = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    print(f"{r['name']:<30} {r['total_picks']:<10} {r['baseline_wr']:<11.1f}% {t_str:<15} {r['best_wr']:<9.1f}% {edge:<10}")

print(f"\nBest PD double: {max(pd_results, key=lambda x: x['edge'] if x['edge'] else -999)['name']} with +{max(pd_results, key=lambda x: x['edge'] if x['edge'] else -999)['edge']:.1f}pp edge")
avg_pd_baseline = sum(r['baseline_wr'] for r in pd_results) / len(pd_results) if pd_results else 0
print(f"Average PD double baseline: {avg_pd_baseline:.1f}% (vs all picks {all_picks['baseline_wr']:.1f}%)")

print("\n" + "=" * 120)
print("PERSONAL YEAR DOUBLES (Both Players Same PY in 1/6/7)")
print("=" * 120)
print(f"\n{'Filter':<30} {'Picks':<10} {'Baseline':<12} {'Best Threshold':<15} {'Best WR':<10} {'Edge':<10}")
print("-" * 85)

for r in sorted(py_results, key=lambda x: x['edge'], reverse=True):
    edge = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    print(f"{r['name']:<30} {r['total_picks']:<10} {r['baseline_wr']:<11.1f}% {t_str:<15} {r['best_wr']:<9.1f}% {edge:<10}")

print(f"\nBest PY double: {max(py_results, key=lambda x: x['edge'] if x['edge'] else -999)['name']} with +{max(py_results, key=lambda x: x['edge'] if x['edge'] else -999)['edge']:.1f}pp edge")
avg_py_baseline = sum(r['baseline_wr'] for r in py_results) / len(py_results) if py_results else 0
print(f"Average PY double baseline: {avg_py_baseline:.1f}% (vs all picks {all_picks['baseline_wr']:.1f}%)")

# Top performers detailed
print("\n" + "=" * 120)
print("TOP 3 PERFORMERS - DETAILED THRESHOLD ANALYSIS")
print("=" * 120)

top3 = sorted(results, key=lambda x: x['edge'], reverse=True)[:3]
for idx, r in enumerate(top3, 1):
    if not r or r['total_picks'] < 5:
        continue

    print(f"\n{idx}. {r['name'].upper()}")
    print(f"Total: {r['total_picks']} picks | Baseline: {r['baseline_wr']:.1f}%")
    print("-" * 90)
    print(f"{'Threshold':<12} {'Win Rate':<12} {'Picks':<10} {'Status':<20}")
    print("-" * 60)

    for threshold in range(-2, 9):
        filtered = [d for d in r['data'] if d['lp_score'] > threshold]
        if not filtered or len(filtered) < 5:
            continue

        wins = sum(1 for d in filtered if d['result'])
        wr = (wins / len(filtered) * 100)

        if wr >= 60:
            status = "STRONG"
        elif wr >= 55:
            status = "Very Good"
        elif wr >= 50:
            status = "Good"
        else:
            status = "WEAK"

        print(f"T{threshold:+3d}        {wr:>6.1f}%        {len(filtered):>6d}       {status:<20}")

print("\n" + "=" * 120)
print("INTERPRETATION")
print("=" * 120)

best = sorted(results, key=lambda x: x['edge'], reverse=True)[0]
if 'all_picks' not in best['name'].lower():
    print(f"\nSTRONGEST DOUBLE MATCH: {best['name']}")
    print(f"  Baseline: {best['baseline_wr']:.1f}% ({best['total_picks']} picks)")
    if best['best_threshold'] is not None:
        print(f"  Threshold T{best['best_threshold']:+d} -> {best['best_wr']:.1f}% (+{best['edge']:.1f}pp)")
        print(f"  Sample size: {best['best_picks']} picks at threshold")
    print(f"  vs All Picks: {best['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp")

if pd_results:
    pd_best = max(pd_results, key=lambda x: x['edge'] if x['edge'] else -999)
    print(f"\nPD DOUBLES: {len([r for r in pd_results if r['total_picks'] >= 5])} viable signals out of 3")
    print(f"  Best: {pd_best['name']} at {pd_best['baseline_wr']:.1f}% (+{pd_best['edge']:.1f}pp, {pd_best['total_picks']} picks)")

if py_results:
    py_best = max(py_results, key=lambda x: x['edge'] if x['edge'] else -999)
    print(f"\nPY DOUBLES: {len([r for r in py_results if r['total_picks'] >= 5])} viable signals out of 3")
    print(f"  Best: {py_best['name']} at {py_best['baseline_wr']:.1f}% (+{py_best['edge']:.1f}pp, {py_best['total_picks']} picks)")

print()
