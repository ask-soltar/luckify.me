import csv
from datetime import datetime

# Read PLAYERS sheet to get birth dates
players_file = "Golf Historics v3 - Golf_Analytics.csv"
players_birth = {}

print("Reading player birth dates from Golf_Analytics...")

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
                        players_birth[player] = {
                            'month': birth_obj.month,
                            'day': birth_obj.day,
                            'year': birth_obj.year
                        }
                    except:
                        pass

        print(f"Loaded {len(players_birth)} players with birth dates\n")

# Process ANALYSIS sheet
analysis_file = "ANALYSIS_v3_export.csv"

# Column indices for ANALYSIS sheet
player_idx = 1          # Player name
event_year_idx = 4      # Year
vs_avg_idx = 10         # vs Avg (column F in base + offset)
# Need to recalculate - let's find it in the header

data_by_metric = {
    'personal_day': [],
    'personal_month': [],
    'personal_year': [],
}

print("Reading ANALYSIS sheet...")

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    print(f"Header columns: {len(header)}")

    player_name_idx = None
    vs_avg_idx = None
    event_year_idx = None
    event_month_idx = None
    event_day_idx = None
    round_num_idx = None

    for i, col in enumerate(header):
        col_clean = col.strip().lower()
        if col_clean == 'player_name':
            player_name_idx = i
        if 'vs_avg' in col_clean or col_clean == 'vs avg':
            vs_avg_idx = i
        if col_clean == 'year':
            event_year_idx = i
        if 'event_name' in col_clean or col_clean == 'event name':
            event_name_idx = i
        if col_clean == 'round_num' or col_clean == 'round':
            round_num_idx = i

    print(f"Player: {player_name_idx}, vs_avg: {vs_avg_idx}, year: {event_year_idx}, round: {round_num_idx}")

    if player_name_idx is None:
        print("ERROR: Could not find player_name column")
        exit(1)

    # Need different approach - read Golf_Analytics instead
    print("\nSwitching to Golf_Analytics for comprehensive data...")

# Use Golf_Analytics as source - using known column positions
golf_analytics_file = "Golf Historics v3 - Golf_Analytics.csv"

print("Reading Golf_Analytics sheet for vs_avg analysis...")

data_by_metric = {
    'personal_day': [],
    'personal_month': [],
    'personal_year': [],
}

row_count = 0

with open(golf_analytics_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Known column indices (from header inspection):
    # Col 1 (idx 0): Year
    # Col 3 (idx 2): Player
    # Col 4-7 (idx 3-6): R1-R4 scores
    # Col 13-16 (idx 12-15): Rd1-Rd4 dates
    # Col 35-38 (idx 34-37): Course Avg R1-R4
    # Col 39-42 (idx 38-41): R1-R4 vs Avg

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

    print(f"Using fixed column indices...")

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

            # Process each round
            round_configs = [
                (rd1_idx, vs_avg_r1_idx, rd1_date_idx, 1),
                (rd2_idx, vs_avg_r2_idx, rd2_date_idx, 2),
                (rd3_idx, vs_avg_r3_idx, rd3_date_idx, 3),
                (rd4_idx, vs_avg_r4_idx, rd4_date_idx, 4),
            ]

            for score_idx, vs_avg_idx, date_idx, rnd_num in round_configs:
                if score_idx >= len(row) or vs_avg_idx >= len(row) or date_idx >= len(row):
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

                # Get event date
                date_str = row[date_idx].strip() if date_idx < len(row) else ''
                event_month = None
                event_day = None

                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                        event_month = date_obj.month
                        event_day = date_obj.day
                    except:
                        pass

                if event_month is None or event_day is None:
                    continue

                # Calculate Personal Year
                py = birth_month + birth_day + year
                while py > 9:
                    py = sum(int(d) for d in str(py))

                # Calculate Personal Month
                pm = birth_month + event_month
                while pm > 9:
                    pm = sum(int(d) for d in str(pm))

                # Calculate Personal Day
                pd = event_month + event_day + py
                while pd > 9:
                    pd = sum(int(d) for d in str(pd))

                # Record data for each metric
                data_by_metric['personal_day'].append({'metric_value': pd, 'vs_avg': vs_avg})
                data_by_metric['personal_month'].append({'metric_value': pm, 'vs_avg': vs_avg})
                data_by_metric['personal_year'].append({'metric_value': py, 'vs_avg': vs_avg})

                row_count += 1

        except (ValueError, IndexError):
            continue

print(f"Processed {row_count} valid score records\n")

# Analysis function - using vs_avg thresholds
def analyze_metric(metric_name, data):
    if not data or len(data) < 10:
        return None

    results = {}

    for value in range(1, 10):
        subset = [d for d in data if d['metric_value'] == value]
        if not subset or len(subset) < 5:
            continue

        # Calculate baseline (all scores for this metric value)
        baseline_vs_avg = sum(d['vs_avg'] for d in subset) / len(subset)

        # Test thresholds
        above_2 = [d for d in subset if d['vs_avg'] > 2]
        below_neg2 = [d for d in subset if d['vs_avg'] < -2]
        between = [d for d in subset if -2 <= d['vs_avg'] <= 2]

        above_2_avg = sum(d['vs_avg'] for d in above_2) / len(above_2) if above_2 else 0
        below_neg2_avg = sum(d['vs_avg'] for d in below_neg2) / len(below_neg2) if below_neg2 else 0
        between_avg = sum(d['vs_avg'] for d in between) / len(between) if between else 0

        results[value] = {
            'total': len(subset),
            'baseline_vs_avg': baseline_vs_avg,
            'above_2_count': len(above_2),
            'above_2_avg': above_2_avg,
            'below_neg2_count': len(below_neg2),
            'below_neg2_avg': below_neg2_avg,
            'between_count': len(between),
            'between_avg': between_avg,
            'above_2_pct': len(above_2) / len(subset) * 100,
            'below_neg2_pct': len(below_neg2) / len(subset) * 100,
            'between_pct': len(between) / len(subset) * 100,
        }

    return results

# Run analysis for each metric
print("=" * 120)
print("PERSONAL METRICS ANALYSIS: vs_avg +2/-2 Thresholds")
print("=" * 120)

all_results = {}

for metric_name, data in data_by_metric.items():
    print(f"\n{metric_name.upper().replace('_', ' ')} ({len(data)} total rounds)")
    print("-" * 120)

    results = analyze_metric(metric_name, data)
    all_results[metric_name] = results

    if not results:
        print("  No data")
        continue

    print(f"\n{'Value':<8} {'Total':<10} {'Baseline':<12} {'Above+2':<12} {'Below-2':<12} {'Between':<12}")
    print(f"{'':8} {'Rounds':<10} {'vs_avg':<12} {'Count/Avg':<12} {'Count/Avg':<12} {'Count/Avg':<12}")
    print("-" * 120)

    for value in range(1, 10):
        if value not in results:
            continue

        r = results[value]
        a2_str = f"{r['above_2_count']}/{r['above_2_avg']:.2f}" if r['above_2_count'] > 0 else "-"
        bn2_str = f"{r['below_neg2_count']}/{r['below_neg2_avg']:.2f}" if r['below_neg2_count'] > 0 else "-"
        bet_str = f"{r['between_count']}/{r['between_avg']:.2f}" if r['between_count'] > 0 else "-"

        print(f"{value:<8} {r['total']:<10} {r['baseline_vs_avg']:>+.2f}      {a2_str:<12} {bn2_str:<12} {bet_str:<12}")

# Detailed comparison
print("\n" + "=" * 120)
print("SUMMARY: DISTRIBUTION BY THRESHOLD")
print("=" * 120)

for metric_name in ['personal_day', 'personal_month', 'personal_year']:
    results = all_results[metric_name]

    total_rounds = sum(r['total'] for r in results.values())
    total_above_2 = sum(r['above_2_count'] for r in results.values())
    total_below_neg2 = sum(r['below_neg2_count'] for r in results.values())
    total_between = sum(r['between_count'] for r in results.values())

    avg_above_2 = sum(r['above_2_avg'] * r['above_2_count'] for r in results.values()) / total_above_2 if total_above_2 > 0 else 0
    avg_below_neg2 = sum(r['below_neg2_avg'] * r['below_neg2_count'] for r in results.values()) / total_below_neg2 if total_below_neg2 > 0 else 0
    avg_between = sum(r['between_avg'] * r['between_count'] for r in results.values()) / total_between if total_between > 0 else 0

    print(f"\n{metric_name.upper().replace('_', ' ')}")
    print(f"  Total rounds: {total_rounds}")
    print(f"  Above +2:     {total_above_2:>5} ({total_above_2/total_rounds*100:>5.1f}%) avg vs_avg: {avg_above_2:>+.2f}")
    print(f"  Below -2:     {total_below_neg2:>5} ({total_below_neg2/total_rounds*100:>5.1f}%) avg vs_avg: {avg_below_neg2:>+.2f}")
    print(f"  Between:      {total_between:>5} ({total_between/total_rounds*100:>5.1f}%) avg vs_avg: {avg_between:>+.2f}")

print("\n" + "=" * 120)
print("TOP PERFORMERS BY METRIC VALUE")
print("=" * 120)

for metric_name in ['personal_day', 'personal_month', 'personal_year']:
    results = all_results[metric_name]

    print(f"\n{metric_name.upper().replace('_', ' ')}")
    print("-" * 80)

    # Sort by baseline vs_avg
    sorted_values = sorted(results.items(), key=lambda x: x[1]['baseline_vs_avg'], reverse=True)

    for value, data in sorted_values[:5]:
        print(f"  {metric_name.split('_')[1].upper()}{value}: {data['baseline_vs_avg']:>+.2f} vs_avg ({data['total']} rounds)")
        print(f"    Above +2: {data['above_2_count']} ({data['above_2_pct']:.0f}%) @ {data['above_2_avg']:>+.2f}")
        print(f"    Below -2: {data['below_neg2_count']} ({data['below_neg2_pct']:.0f}%) @ {data['below_neg2_avg']:>+.2f}")

print("\n")
