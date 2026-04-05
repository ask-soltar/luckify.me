import csv
from datetime import datetime

# Read PLAYERS sheet to get birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("Reading player birth dates...")

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find columns - look for 'Player' (player name) not just any player column
    player_name_idx = None
    birthday_idx = None

    for i, col in enumerate(header):
        col_clean = col.strip().lower()
        if col_clean == 'player':  # Exact match for player name column
            player_name_idx = i
        if 'birthday' in col_clean:
            birthday_idx = i

    if player_name_idx is None or birthday_idx is None:
        print(f"Warning: Could not find player name or birthday columns")
        print(f"Found: Player column {player_name_idx}, Birthday column {birthday_idx}")
    else:
        print(f"Found: Player column {player_name_idx}, Birthday column {birthday_idx}\n")

        row_count = 0
        for row in reader:
            if player_name_idx < len(row) and birthday_idx < len(row):
                player = row[player_name_idx].strip()
                birth = row[birthday_idx].strip()

                if player and birth and player not in players_birth:
                    # Try to parse birth date
                    try:
                        birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                        players_birth[player] = (birth_obj.month, birth_obj.day)
                        row_count += 1
                    except:
                        pass

        print(f"Loaded {row_count} player records with birth dates")

print(f"Loaded {len(players_birth)} players with birth dates\n")

# Sample output
if players_birth:
    for player, (month, day) in list(players_birth.items())[:5]:
        print(f"  {player}: {month}/{day}")

# Now process 2BMatchup sheet
matchup_file = "Golf Historics v3 - 2BMatchup (8).csv"

player_a_idx = 0           # Player A
player_b_idx = 1           # Player B
event_date_idx = 5         # Event Date
py_a_idx = 24              # PY [A]
py_b_idx = 25              # PY [B]
lp_score_idx = 52          # LP SCore
lp_pick_idx = 53           # LP Pick
wl_idx = 54                # W/L [LP]

personal_days = {i: [] for i in range(1, 10)}

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

            # Calculate Personal Day for both players and add to their categories
            if player_a in players_birth and py_a:
                birth_month, birth_day = players_birth[player_a]

                # Personal Day = Event Month + Event Day + Personal Year, reduce to 1-9
                pd = (event_month + event_day + py_a)
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))

                if 1 <= pd <= 9:
                    personal_days[pd].append(base_data)

            if player_b in players_birth and py_b:
                birth_month, birth_day = players_birth[player_b]

                # Personal Day = Event Month + Event Day + Personal Year, reduce to 1-9
                pd = (event_month + event_day + py_b)
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))

                if 1 <= pd <= 9:
                    personal_days[pd].append(base_data)

        except (ValueError, IndexError):
            continue

# Analysis function
def analyze_year(day_num, data):
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
        'day': day_num,
        'total_picks': len(data),
        'baseline_wr': wr,
        'best_threshold': best_threshold,
        'best_wr': best_wr,
        'best_picks': best_picks,
        'edge': (best_wr - wr) if best_wr > 0 else 0
    }

# Run analysis
print("\n" + "=" * 120)
print("PERSONAL DAY ANALYSIS - ALL DAYS (1-9)")
print("=" * 120)

pd_results = []
for day in range(1, 10):
    result = analyze_year(day, personal_days[day])
    if result:
        pd_results.append(result)

# Sort by edge
pd_results.sort(key=lambda x: x['edge'], reverse=True)

print(f"\n{'Day':<8} {'Picks':<10} {'Baseline':<12} {'Best T':<8} {'Best WR':<10} {'Edge':<10}")
print("-" * 90)

for r in pd_results:
    t_str = f"T{r['best_threshold']:+3d}" if r['best_threshold'] is not None else "N/A"
    edge_str = f"+{r['edge']:.1f}pp" if r['edge'] > 0 else f"{r['edge']:.1f}pp"
    print(f"{r['day']:<8} {r['total_picks']:<10} {r['baseline_wr']:>10.1f}% {t_str:<8} {r['best_wr']:<9.1f}% {edge_str:<10}")

# Ranking
print("\n" + "=" * 120)
print("RANKING - PERSONAL DAY")
print("=" * 120)

print("\nBY EDGE IMPROVEMENT:")
for i, r in enumerate(pd_results[:5], 1):
    print(f"  {i}. PD{r['day']}: +{r['edge']:.1f}pp ({r['baseline_wr']:.1f}% -> {r['best_wr']:.1f}% at T{r['best_threshold']:+d}, {r['best_picks']} picks)")

print("\nBY BASELINE WR:")
pd_by_baseline = sorted(pd_results, key=lambda x: x['baseline_wr'], reverse=True)
for i, r in enumerate(pd_by_baseline[:5], 1):
    print(f"  {i}. PD{r['day']}: {r['baseline_wr']:.1f}% ({r['total_picks']} picks)")
