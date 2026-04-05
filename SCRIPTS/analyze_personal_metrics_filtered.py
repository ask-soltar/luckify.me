import csv
from datetime import datetime

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

# Read Golf_Analytics with all filters
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"

# Column indices (from header inspection):
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
tournament_type_idx = 70

# Filter categories
filters = {
    'all': [],
    'calm': [],
    'moderate': [],
    'tough': [],
    'open': [],
    'positioning': [],
    'closing': [],
    'tournament_s': [],
    'tournament_ns': [],
}

print("Reading Golf_Analytics with filters...")

row_count = 0

with open(golf_analytics_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row_num, row in enumerate(reader, 2):
        if not row or len(row) < vs_avg_r4_idx + 1:
            continue

        try:
            player = row[player_idx].strip() if player_idx < len(row) else ''
            year = int(row[year_idx].strip()) if year_idx < len(row) and row[year_idx].strip().isdigit() else None

            if not player or not year or player not in players_birth:
                continue

            birth_info = players_birth[player]
            birth_month = birth_info['month']
            birth_day = birth_info['day']

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

                # Calculate metrics
                py = birth_month + birth_day + year
                while py > 9:
                    py = sum(int(d) for d in str(py))

                pm = birth_month + event_month
                while pm > 9:
                    pm = sum(int(d) for d in str(pm))

                pd = event_month + event_day + py
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))

                base_data = {
                    'pd': pd,
                    'pm': pm,
                    'py': py,
                    'vs_avg': vs_avg,
                    'condition': condition,
                    'round_type': round_type,
                    'tournament_type': tournament_type
                }

                # Add to all
                filters['all'].append(base_data)

                # Add to condition filters
                if 'calm' in condition.lower():
                    filters['calm'].append(base_data)
                elif 'moderate' in condition.lower():
                    filters['moderate'].append(base_data)
                elif 'tough' in condition.lower():
                    filters['tough'].append(base_data)

                # Add to round type filters
                if 'open' in round_type.lower():
                    filters['open'].append(base_data)
                elif 'positioning' in round_type.lower():
                    filters['positioning'].append(base_data)
                elif 'closing' in round_type.lower():
                    filters['closing'].append(base_data)

                # Add to tournament type filters
                if tournament_type in ['S', 'NS']:
                    if tournament_type == 'S':
                        filters['tournament_s'].append(base_data)
                    else:
                        filters['tournament_ns'].append(base_data)

                row_count += 1

        except (ValueError, IndexError):
            continue

print(f"Processed {row_count} valid score records\n")

# Analysis function
def analyze_filter(name, data, metric_name='pd'):
    if not data or len(data) < 10:
        return None

    # Get metric key
    if metric_name == 'pd':
        key = 'pd'
    elif metric_name == 'pm':
        key = 'pm'
    else:
        key = 'py'

    results = {}

    for value in range(1, 10):
        subset = [d for d in data if d[key] == value]
        if not subset or len(subset) < 5:
            continue

        # Calculate baseline
        baseline_vs_avg = sum(d['vs_avg'] for d in subset) / len(subset)

        # Test thresholds
        above_2 = [d for d in subset if d['vs_avg'] > 2]
        below_neg2 = [d for d in subset if d['vs_avg'] < -2]

        above_2_avg = sum(d['vs_avg'] for d in above_2) / len(above_2) if above_2 else 0
        below_neg2_avg = sum(d['vs_avg'] for d in below_neg2) / len(below_neg2) if below_neg2 else 0

        results[value] = {
            'total': len(subset),
            'baseline_vs_avg': baseline_vs_avg,
            'above_2_count': len(above_2),
            'above_2_avg': above_2_avg,
            'below_neg2_count': len(below_neg2),
            'below_neg2_avg': below_neg2_avg,
            'above_2_pct': len(above_2) / len(subset) * 100 if subset else 0,
            'below_neg2_pct': len(below_neg2) / len(subset) * 100 if subset else 0,
        }

    return results

# Run analysis for each filter
print("=" * 140)
print("PERSONAL METRICS ANALYSIS BY CONDITION, ROUND TYPE, AND TOURNAMENT TYPE")
print("=" * 140)

# By Course Condition
print("\n" + "=" * 140)
print("BY COURSE CONDITION")
print("=" * 140)

for condition_name in ['calm', 'moderate', 'tough']:
    data = filters[condition_name]
    if not data:
        print(f"\n{condition_name.upper()}: No data")
        continue

    print(f"\n{condition_name.upper()} ({len(data)} rounds)")
    print("-" * 140)

    # Analyze Personal Day
    pd_results = analyze_filter(f"{condition_name} PD", data, 'pd')

    if pd_results:
        print(f"{'PD':<5} {'Total':<10} {'Baseline':<12} {'Above+2':<15} {'Below-2':<15}")
        print(f"{'':5} {'Rounds':<10} {'vs_avg':<12} {'Ct/Avg':<15} {'Ct/Avg':<15}")
        print("-" * 80)

        for value in sorted(pd_results.keys()):
            r = pd_results[value]
            a2 = f"{r['above_2_count']}/{r['above_2_avg']:.2f}" if r['above_2_count'] > 0 else "-"
            b2 = f"{r['below_neg2_count']}/{r['below_neg2_avg']:.2f}" if r['below_neg2_count'] > 0 else "-"
            print(f"{value:<5} {r['total']:<10} {r['baseline_vs_avg']:>+.2f}      {a2:<15} {b2:<15}")

# By Round Type
print("\n" + "=" * 140)
print("BY ROUND TYPE")
print("=" * 140)

for rtype_name in ['open', 'positioning', 'closing']:
    data = filters[rtype_name]
    if not data:
        print(f"\n{rtype_name.upper()}: No data")
        continue

    print(f"\n{rtype_name.upper()} ({len(data)} rounds)")
    print("-" * 140)

    pd_results = analyze_filter(f"{rtype_name} PD", data, 'pd')

    if pd_results:
        print(f"{'PD':<5} {'Total':<10} {'Baseline':<12} {'Above+2':<15} {'Below-2':<15}")
        print(f"{'':5} {'Rounds':<10} {'vs_avg':<12} {'Ct/Avg':<15} {'Ct/Avg':<15}")
        print("-" * 80)

        for value in sorted(pd_results.keys()):
            r = pd_results[value]
            a2 = f"{r['above_2_count']}/{r['above_2_avg']:.2f}" if r['above_2_count'] > 0 else "-"
            b2 = f"{r['below_neg2_count']}/{r['below_neg2_avg']:.2f}" if r['below_neg2_count'] > 0 else "-"
            print(f"{value:<5} {r['total']:<10} {r['baseline_vs_avg']:>+.2f}      {a2:<15} {b2:<15}")

# By Tournament Type
print("\n" + "=" * 140)
print("BY TOURNAMENT TYPE (S = Standard, NS = Non-Standard)")
print("=" * 140)

for ttype_name, ttype_label in [('tournament_s', 'Standard (S)'), ('tournament_ns', 'Non-Standard (NS)')]:
    data = filters[ttype_name]
    if not data:
        print(f"\n{ttype_label}: No data")
        continue

    print(f"\n{ttype_label} ({len(data)} rounds)")
    print("-" * 140)

    pd_results = analyze_filter(f"{ttype_label} PD", data, 'pd')

    if pd_results:
        print(f"{'PD':<5} {'Total':<10} {'Baseline':<12} {'Above+2':<15} {'Below-2':<15}")
        print(f"{'':5} {'Rounds':<10} {'vs_avg':<12} {'Ct/Avg':<15} {'Ct/Avg':<15}")
        print("-" * 80)

        for value in sorted(pd_results.keys()):
            r = pd_results[value]
            a2 = f"{r['above_2_count']}/{r['above_2_avg']:.2f}" if r['above_2_count'] > 0 else "-"
            b2 = f"{r['below_neg2_count']}/{r['below_neg2_avg']:.2f}" if r['below_neg2_count'] > 0 else "-"
            print(f"{value:<5} {r['total']:<10} {r['baseline_vs_avg']:>+.2f}      {a2:<15} {b2:<15}")

# Summary table
print("\n" + "=" * 140)
print("SUMMARY TABLE")
print("=" * 140)

summary_data = []

for filter_name in ['all', 'calm', 'moderate', 'tough', 'open', 'positioning', 'closing', 'tournament_s', 'tournament_ns']:
    data = filters[filter_name]
    if not data:
        continue

    # Find best performing PD
    pd_results = analyze_filter(f"{filter_name}", data, 'pd')
    if not pd_results:
        continue

    best_pd = max(pd_results.items(), key=lambda x: x[1]['baseline_vs_avg'])
    worst_pd = min(pd_results.items(), key=lambda x: x[1]['baseline_vs_avg'])

    summary_data.append({
        'filter': filter_name.replace('_', ' ').title(),
        'total': len(data),
        'best_pd': best_pd[0],
        'best_vs_avg': best_pd[1]['baseline_vs_avg'],
        'worst_pd': worst_pd[0],
        'worst_vs_avg': worst_pd[1]['baseline_vs_avg'],
    })

print(f"\n{'Filter':<25} {'Total':<10} {'Best PD':<12} {'Best vs_avg':<15} {'Worst PD':<12} {'Worst vs_avg':<15}")
print("-" * 100)

for s in summary_data:
    print(f"{s['filter']:<25} {s['total']:<10} PD{s['best_pd']:<11} {s['best_vs_avg']:>+.2f}      PD{s['worst_pd']:<11} {s['worst_vs_avg']:>+.2f}")

print("\n")
