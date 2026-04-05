import csv
from datetime import datetime

# Read PLAYERS sheet to get birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("Reading player birth dates...")

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find columns
    player_name_idx = None
    birthday_idx = None

    for i, col in enumerate(header):
        col_clean = col.strip().lower()
        if col_clean == 'player':
            player_name_idx = i
        if 'birthday' in col_clean:
            birthday_idx = i

    if player_name_idx is None or birthday_idx is None:
        print(f"Warning: Could not find columns. Player: {player_name_idx}, Birthday: {birthday_idx}")
    else:
        row_count = 0
        for row in reader:
            if player_name_idx < len(row) and birthday_idx < len(row):
                player = row[player_name_idx].strip()
                birth = row[birthday_idx].strip()

                if player and birth and player not in players_birth:
                    try:
                        birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                        players_birth[player] = (birth_obj.month, birth_obj.day)
                        row_count += 1
                    except:
                        pass

        print(f"Loaded {len(players_birth)} players with birth dates\n")

# Process 2BMatchup sheet
matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

player_a_idx = 0           # Player A
player_b_idx = 1           # Player B
event_date_idx = 5         # Event Date
py_a_idx = 24              # PY [A]
py_b_idx = 25              # PY [B]
lp_score_idx = 52          # LP Score
lp_pick_idx = 53           # LP Pick
wl_idx = 54                # W/L [LP]

# Analysis categories
filters = {
    'all_picks': [],
    'pd_167_only': [],        # PD in [1,6,7]
    'py_167_only': [],        # PY in [1,6,7]
    'both_pd_and_py_167': []  # Both PD and PY in [1,6,7]
}

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 2):
        if not row or len(row) < wl_idx + 1:
            continue

        try:
            # Get players and dates
            player_a = row[player_a_idx].strip() if player_a_idx < len(row) else ''
            player_b = row[player_b_idx].strip() if player_b_idx < len(row) else ''
            event_date = row[event_date_idx].strip() if event_date_idx < len(row) else ''

            # Get PY values
            try:
                py_a = int(row[py_a_idx].strip()) if py_a_idx < len(row) and row[py_a_idx].strip().isdigit() else None
                py_b = int(row[py_b_idx].strip()) if py_b_idx < len(row) and row[py_b_idx].strip().isdigit() else None
            except:
                continue

            # Get LP Score
            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue
            lp_score = float(lp_score_str)

            # Get LP Pick
            lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
            if not lp_pick:
                continue

            # Get W/L
            wl = row[wl_idx].strip() if wl_idx < len(row) else ''
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            # Parse event date
            try:
                event_obj = datetime.strptime(event_date, '%m/%d/%Y')
                event_month = event_obj.month
                event_day = event_obj.day
            except:
                continue

            base_data = {'lp_score': lp_score, 'result': is_win}
            filters['all_picks'].append(base_data)

            # Calculate Personal Day for both players
            pds = []

            if player_a in players_birth and py_a:
                pd = (event_month + event_day + py_a)
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))
                pds.append(pd)

            if player_b in players_birth and py_b:
                pd = (event_month + event_day + py_b)
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))
                pds.append(pd)

            # Assign to filter categories
            has_pd_167 = any(pd in [1, 6, 7] for pd in pds) if pds else False
            has_py_167 = (py_a in [1, 6, 7]) or (py_b in [1, 6, 7]) if (py_a or py_b) else False

            if has_pd_167:
                filters['pd_167_only'].append(base_data)

            if has_py_167:
                filters['py_167_only'].append(base_data)

            if has_pd_167 and has_py_167:
                filters['both_pd_and_py_167'].append(base_data)

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
print("COMBINED PERSONAL DAY + PERSONAL YEAR ANALYSIS")
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
print(f"\n{'Filter':<35} {'Total':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Picks':<8} {'Edge':<10}")
print("-" * 100)

for r in results:
    edge = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    print(f"{r['name']:<35} {r['total_picks']:<10} {r['baseline_wr']:<11.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {r['best_picks']:<8} {edge:<10}")

# Detailed comparison
print("\n" + "=" * 120)
print("DETAILED ANALYSIS & COMPARISON")
print("=" * 120)

all_picks = [r for r in results if 'All Picks' in r['name']][0]
pd_only = [r for r in results if 'Pd 167' in r['name']][0]
py_only = [r for r in results if 'Py 167' in r['name']][0]
both = [r for r in results if 'Both' in r['name']][0]

print(f"\nALL PICKS (baseline):")
print(f"  Total: {all_picks['total_picks']}")
print(f"  Baseline WR: {all_picks['baseline_wr']:.1f}%")
print(f"  Best threshold: T{all_picks['best_threshold']:+d} -> {all_picks['best_wr']:.1f}% (+{all_picks['edge']:.1f}pp)")

print(f"\nPERSONAL DAY IN [1,6,7] ONLY:")
print(f"  Total: {pd_only['total_picks']} ({pd_only['total_picks']/all_picks['total_picks']*100:.1f}% of all picks)")
print(f"  Baseline WR: {pd_only['baseline_wr']:.1f}% (vs all {all_picks['baseline_wr']:.1f}%)")
print(f"  Best threshold: T{pd_only['best_threshold']:+d} -> {pd_only['best_wr']:.1f}% (+{pd_only['edge']:.1f}pp)")
print(f"  vs ALL baseline: {pd_only['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp")

print(f"\nPERSONAL YEAR IN [1,6,7] ONLY:")
print(f"  Total: {py_only['total_picks']} ({py_only['total_picks']/all_picks['total_picks']*100:.1f}% of all picks)")
print(f"  Baseline WR: {py_only['baseline_wr']:.1f}% (vs all {all_picks['baseline_wr']:.1f}%)")
print(f"  Best threshold: T{py_only['best_threshold']:+d} -> {py_only['best_wr']:.1f}% (+{py_only['edge']:.1f}pp)")
print(f"  vs ALL baseline: {py_only['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp")

print(f"\nBOTH PERSONAL DAY AND PERSONAL YEAR IN [1,6,7]:")
print(f"  Total: {both['total_picks']} ({both['total_picks']/all_picks['total_picks']*100:.1f}% of all picks)")
print(f"  Baseline WR: {both['baseline_wr']:.1f}% (vs all {all_picks['baseline_wr']:.1f}%)")
print(f"  Best threshold: T{both['best_threshold']:+d} -> {both['best_wr']:.1f}% (+{both['edge']:.1f}pp)")
print(f"  vs ALL baseline: {both['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp")

# Synergy analysis
print("\n" + "=" * 120)
print("SYNERGY ANALYSIS")
print("=" * 120)

print(f"\nIndividual metrics (baseline WR vs all picks):")
print(f"  PD[1,6,7]:        {pd_only['baseline_wr']:6.1f}% ({pd_only['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp)")
print(f"  PY[1,6,7]:        {py_only['baseline_wr']:6.1f}% ({py_only['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp)")
print(f"  Combined (both):  {both['baseline_wr']:6.1f}% ({both['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp)")

# Check if synergistic or additive
expected_additive = pd_only['baseline_wr'] + py_only['baseline_wr'] - all_picks['baseline_wr']
synergy = both['baseline_wr'] - expected_additive
print(f"\nExpected if additive: {expected_additive:.1f}%")
print(f"Actual combined: {both['baseline_wr']:.1f}%")
print(f"Synergy effect: {synergy:+.1f}pp {'(SYNERGISTIC - both stronger together)' if synergy > 0 else '(subadditive - overlap penalty)'}")

# Threshold performance comparison
print("\n" + "=" * 120)
print("EDGE IMPROVEMENT COMPARISON (Threshold Optimization)")
print("=" * 120)

print(f"\n{'Filter':<30} {'Baseline':<12} {'Best Threshold':<15} {'Best WR':<12} {'Edge':<10} {'Pick Count':<10}")
print("-" * 90)

all_t = f"T{all_picks['best_threshold']:+d}"
all_e = f"+{all_picks['edge']:.1f}pp"
print(f"{'All Picks':<30} {all_picks['baseline_wr']:>10.1f}% {all_t:<15} {all_picks['best_wr']:>10.1f}% {all_e:<10} {all_picks['best_picks']:<10}")

pd_t = f"T{pd_only['best_threshold']:+d}"
pd_e = f"+{pd_only['edge']:.1f}pp"
print(f"{'PD [1,6,7] Only':<30} {pd_only['baseline_wr']:>10.1f}% {pd_t:<15} {pd_only['best_wr']:>10.1f}% {pd_e:<10} {pd_only['best_picks']:<10}")

py_t = f"T{py_only['best_threshold']:+d}"
py_e = f"+{py_only['edge']:.1f}pp"
print(f"{'PY [1,6,7] Only':<30} {py_only['baseline_wr']:>10.1f}% {py_t:<15} {py_only['best_wr']:>10.1f}% {py_e:<10} {py_only['best_picks']:<10}")

both_t = f"T{both['best_threshold']:+d}"
both_e = f"+{both['edge']:.1f}pp"
print(f"{'Both PD & PY [1,6,7]':<30} {both['baseline_wr']:>10.1f}% {both_t:<15} {both['best_wr']:>10.1f}% {both_e:<10} {both['best_picks']:<10}")

# Detailed threshold breakdown for combined filter
print("\n" + "=" * 120)
print("THRESHOLD DETAIL: BOTH PD & PY [1,6,7]")
print("=" * 120)
print(f"\n{'Threshold':<12} {'Win Rate':<12} {'Picks':<10} {'Status':<20}")
print("-" * 60)

for threshold in range(-2, 9):
    filtered = [d for d in both['data'] if d['lp_score'] > threshold]
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
print("CONCLUSION")
print("=" * 120)

if both['baseline_wr'] > max(pd_only['baseline_wr'], py_only['baseline_wr']):
    print(f"\nCOMBINED [1,6,7] shows STRONGEST baseline: {both['baseline_wr']:.1f}%")
    print(f"  This suggests SYNERGISTIC effect — picks with BOTH metrics boost performance beyond either alone")
elif both['baseline_wr'] > all_picks['baseline_wr']:
    print(f"\nCOMBINED [1,6,7] shows improvement: {both['baseline_wr']:.1f}% vs {all_picks['baseline_wr']:.1f}% all")
    print(f"  Effectiveness: {both['baseline_wr'] - all_picks['baseline_wr']:+.1f}pp boost")
else:
    print(f"\nCOMBINED [1,6,7] shows no improvement: {both['baseline_wr']:.1f}% (worse than all picks {all_picks['baseline_wr']:.1f}%)")

print(f"\nRecommendation: Filter by {'BOTH metrics [1,6,7]' if both['baseline_wr'] > py_only['baseline_wr'] else 'the stronger individual metric'}")
print()
