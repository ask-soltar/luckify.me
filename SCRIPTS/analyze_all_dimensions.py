import csv
from datetime import datetime
from collections import defaultdict

# Helper function for numerology reduction
def reduce_to_single(num):
    """Reduce to single digit 1-9"""
    if num <= 0:
        return None
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

# Read PLAYERS sheet to get birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("Reading player birth dates...")

with open(players_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    player_idx = 2
    birthday_idx = 10

    for row in reader:
        if player_idx < len(row) and birthday_idx < len(row):
            player = row[player_idx].strip()
            birth = row[birthday_idx].strip()

            if player and birth and player not in players_birth:
                try:
                    birth_obj = datetime.strptime(birth, '%m/%d/%Y')
                    players_birth[player] = {
                        'month': birth_obj.month,
                        'day': birth_obj.day,
                        'year': birth_obj.year
                    }
                except:
                    pass

print(f"Loaded {len(players_birth)} players\n")

# Read Golf_Analytics with all dimensions
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"

# Column indices
year_idx = 0
player_idx = 2
rd1_idx = 3
rd2_idx = 4
rd3_idx = 5
rd4_idx = 6
rd1_date_idx = 12
rd2_date_idx = 13
rd3_date_idx = 14
rd4_date_idx = 15
vs_avg_r1_idx = 38
vs_avg_r2_idx = 39
vs_avg_r3_idx = 40
vs_avg_r4_idx = 41
cond_r1_idx = 42
cond_r2_idx = 43
cond_r3_idx = 44
cond_r4_idx = 45
type_r1_idx = 46
type_r2_idx = 47
type_r3_idx = 48
type_r4_idx = 49
life_path_idx = 62
tournament_type_idx = 70

# Data structure: {(condition, tournament_type, round_type): [records]}
data_by_dimensions = defaultdict(list)
all_records = []

print("Reading Golf_Analytics with all dimensions...")

with open(golf_analytics_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 2):
        if not row or len(row) < max(vs_avg_r4_idx, tournament_type_idx) + 1:
            continue

        try:
            player = row[player_idx].strip() if player_idx < len(row) else ''
            year = int(row[year_idx].strip()) if year_idx < len(row) and row[year_idx].strip().isdigit() else None

            if not player or not year or player not in players_birth:
                continue

            birth_info = players_birth[player]
            birth_month = birth_info['month']
            birth_day = birth_info['day']

            # Get Life Path
            life_path_str = row[life_path_idx].strip() if life_path_idx < len(row) else ''
            try:
                life_path = int(life_path_str) if life_path_str and life_path_str.isdigit() else None
            except:
                life_path = None

            # Get tournament type
            tournament_type = row[tournament_type_idx].strip() if tournament_type_idx < len(row) else ''

            # Process each round
            round_configs = [
                (rd1_idx, vs_avg_r1_idx, rd1_date_idx, cond_r1_idx, type_r1_idx, 1),
                (rd2_idx, vs_avg_r2_idx, rd2_date_idx, cond_r2_idx, type_r2_idx, 2),
                (rd3_idx, vs_avg_r3_idx, rd3_date_idx, cond_r3_idx, type_r3_idx, 3),
                (rd4_idx, vs_avg_r4_idx, rd4_date_idx, cond_r4_idx, type_r4_idx, 4),
            ]

            for score_idx, vs_avg_idx, date_idx, cond_idx, type_idx, rnd_num in round_configs:
                if score_idx >= len(row) or vs_avg_idx >= len(row):
                    continue

                score_str = row[score_idx].strip() if score_idx < len(row) else ''
                vs_avg_str = row[vs_avg_idx].strip() if vs_avg_idx < len(row) else ''

                if not score_str or score_str in ['', '#REF!', 'Withdrawn', 'Cut']:
                    continue
                if not vs_avg_str or vs_avg_str in ['', '#REF!']:
                    continue

                try:
                    score = float(score_str)
                    vs_avg = float(vs_avg_str)
                except:
                    continue

                # Get date
                date_str = row[date_idx].strip() if date_idx < len(row) else ''
                if not date_str:
                    continue

                try:
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    event_month = date_obj.month
                    event_day = date_obj.day
                except:
                    continue

                # Get condition and round type
                condition = row[cond_idx].strip() if cond_idx < len(row) else ''
                round_type = row[type_idx].strip() if type_idx < len(row) else ''

                # Skip if no condition or round type
                if not condition or not round_type:
                    continue

                # Normalize tournament type (S or NS, group other types)
                if tournament_type not in ['S', 'NS']:
                    ttype = 'Other'
                else:
                    ttype = tournament_type

                # Normalize condition
                if 'calm' in condition.lower():
                    cond = 'Calm'
                elif 'moderate' in condition.lower():
                    cond = 'Moderate'
                elif 'tough' in condition.lower():
                    cond = 'Tough'
                else:
                    continue

                # Normalize round type
                if 'open' in round_type.lower():
                    rtype = 'Open'
                elif 'positioning' in round_type.lower():
                    rtype = 'Positioning'
                elif 'closing' in round_type.lower():
                    rtype = 'Closing'
                else:
                    continue

                # Calculate metrics
                py = reduce_to_single(birth_month + birth_day + year)
                pm = reduce_to_single(birth_month + event_month)
                pd = reduce_to_single(event_month + event_day + py)

                record = {
                    'lp': life_path,
                    'pm': pm,
                    'pd': pd,
                    'py': py,
                    'vs_avg': vs_avg,
                }

                # Add to all records
                all_records.append(record)

                # Add to dimension-specific records
                key = (cond, ttype, rtype)
                data_by_dimensions[key].append(record)

        except (ValueError, IndexError):
            continue

print(f"Processed {len(all_records)} records across {len(data_by_dimensions)} dimension combinations\n")

# Analysis function
def analyze_metric(data, metric_name):
    """Analyze a single metric across values 1-9"""
    if not data:
        return None

    if metric_name == 'lp':
        key = 'lp'
    elif metric_name == 'pm':
        key = 'pm'
    elif metric_name == 'pd':
        key = 'pd'
    else:
        key = 'py'

    results = {}

    for value in range(1, 10):
        subset = [d for d in data if d[key] == value]
        if not subset or len(subset) < 3:
            continue

        baseline = sum(d['vs_avg'] for d in subset) / len(subset)
        above_2 = len([d for d in subset if d['vs_avg'] > 2])
        below_neg2 = len([d for d in subset if d['vs_avg'] < -2])

        results[value] = {
            'count': len(subset),
            'baseline': baseline,
            'above_2_pct': above_2 / len(subset) * 100,
            'below_neg2_pct': below_neg2 / len(subset) * 100,
        }

    return results

# Generate comprehensive report
print("=" * 150)
print("COMPREHENSIVE ANALYSIS: Course Condition x Tournament Type x Round Type")
print("=" * 150)

# Organize by condition, then tournament type, then round type
conditions = ['Calm', 'Moderate', 'Tough']
tournament_types = ['S', 'NS', 'Other']
round_types = ['Open', 'Positioning', 'Closing']

for condition in conditions:
    print(f"\n\n{'='*150}")
    print(f"COURSE CONDITION: {condition.upper()}")
    print(f"{'='*150}")

    for ttype in tournament_types:
        print(f"\n{'-'*150}")
        print(f"Tournament Type: {ttype}")
        print(f"{'-'*150}")

        for rtype in round_types:
            key = (condition, ttype, rtype)
            data = data_by_dimensions[key]

            if not data or len(data) < 10:
                print(f"\n  {rtype}: No data (n={len(data)})")
                continue

            print(f"\n  {rtype.upper()} (n={len(data)} rounds)")
            print(f"  {'-'*140}")

            # Analyze each metric
            for metric_name, metric_label in [('lp', 'Life Path'), ('pm', 'Personal Month'), ('pd', 'Personal Day'), ('py', 'Personal Year')]:
                results = analyze_metric(data, metric_name)

                if not results:
                    print(f"    {metric_label}: No data")
                    continue

                # Find best and worst
                best = max(results.items(), key=lambda x: x[1]['baseline'])
                worst = min(results.items(), key=lambda x: x[1]['baseline'])

                print(f"    {metric_label:<18} Best: {metric_label[0]}{best[0]} ({best[1]['baseline']:>+.2f}), Worst: {metric_label[0]}{worst[0]} ({worst[1]['baseline']:>+.2f}), Spread: {best[1]['baseline']-worst[1]['baseline']:.2f}")

# Summary table across all dimensions
print(f"\n\n{'='*150}")
print("SUMMARY TABLE: Best Performers by Dimension")
print(f"{'='*150}")

summary_rows = []

for condition in conditions:
    for ttype in tournament_types:
        for rtype in round_types:
            key = (condition, ttype, rtype)
            data = data_by_dimensions[key]

            if not data or len(data) < 10:
                continue

            best_metrics = {}
            for metric_name, metric_label in [('lp', 'LP'), ('pm', 'PM'), ('pd', 'PD'), ('py', 'PY')]:
                results = analyze_metric(data, metric_name)
                if results:
                    best = max(results.items(), key=lambda x: x[1]['baseline'])
                    best_metrics[metric_label] = (best[0], best[1]['baseline'])

            summary_rows.append({
                'condition': condition,
                'ttype': ttype,
                'rtype': rtype,
                'count': len(data),
                'best_metrics': best_metrics,
            })

print(f"\n{'Condition':<12} {'TType':<6} {'RType':<12} {'Rounds':<8} {'LP Best':<10} {'PM Best':<10} {'PD Best':<10} {'PY Best':<10}")
print("-" * 140)

for row in summary_rows:
    lp_str = f"{row['best_metrics'].get('LP', ('', ''))[0]}/{row['best_metrics'].get('LP', ('', ''))[1]:+.2f}" if 'LP' in row['best_metrics'] else "N/A"
    pm_str = f"{row['best_metrics'].get('PM', ('', ''))[0]}/{row['best_metrics'].get('PM', ('', ''))[1]:+.2f}" if 'PM' in row['best_metrics'] else "N/A"
    pd_str = f"{row['best_metrics'].get('PD', ('', ''))[0]}/{row['best_metrics'].get('PD', ('', ''))[1]:+.2f}" if 'PD' in row['best_metrics'] else "N/A"
    py_str = f"{row['best_metrics'].get('PY', ('', ''))[0]}/{row['best_metrics'].get('PY', ('', ''))[1]:+.2f}" if 'PY' in row['best_metrics'] else "N/A"

    print(f"{row['condition']:<12} {row['ttype']:<6} {row['rtype']:<12} {row['count']:<8} {lp_str:<10} {pm_str:<10} {pd_str:<10} {py_str:<10}")

print("\n")
