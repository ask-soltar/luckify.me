import csv
from collections import defaultdict

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"

# Store data by personal year and various dimensions
year_data = defaultdict(list)
year_by_color = defaultdict(lambda: defaultdict(list))
year_by_condition = defaultdict(lambda: defaultdict(list))
year_by_round = defaultdict(lambda: defaultdict(list))
year_by_color_condition = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    personal_year_idx = header.index('Personal Year')
    vs_avg_idx = header.index('vs_avg')
    color_idx = header.index('color')
    condition_idx = header.index('condition')
    round_num_idx = header.index('round_num')
    player_name_idx = header.index('player_name')

    for row in reader:
        if not row or row[player_name_idx].strip() == '':
            continue

        try:
            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or personal_year == '' or not personal_year.isdigit():
                continue

            py_num = int(personal_year)

            vs_avg = float(row[vs_avg_idx]) if vs_avg_idx < len(row) and row[vs_avg_idx] else None
            if vs_avg is None:
                continue

            color = row[color_idx].strip() if color_idx < len(row) else ''
            condition = row[condition_idx].strip() if condition_idx < len(row) else ''
            round_num = row[round_num_idx].strip() if round_num_idx < len(row) else ''

            round_data = {
                'vs_avg': vs_avg,
                'color': color,
                'condition': condition,
                'round_num': round_num
            }

            year_data[py_num].append(round_data)
            if color:
                year_by_color[py_num][color].append(round_data)
            if condition:
                year_by_condition[py_num][condition].append(round_data)
            if round_num:
                year_by_round[py_num][round_num].append(round_data)
            if color and condition:
                year_by_color_condition[py_num][color][condition].append(round_data)

        except (ValueError, IndexError):
            continue

def calculate_metrics(rounds):
    """Calculate win rate using ±2 threshold methodology"""
    if not rounds:
        return None

    beats_field = sum(1 for r in rounds if r['vs_avg'] < -2)
    misses_field = sum(1 for r in rounds if r['vs_avg'] > 2)
    threshold_rounds = beats_field + misses_field

    if threshold_rounds == 0:
        return None

    win_rate = (beats_field / threshold_rounds * 100) if threshold_rounds > 0 else 0

    return {
        'total_rounds': len(rounds),
        'beats_field': beats_field,
        'misses_field': misses_field,
        'threshold_rounds': threshold_rounds,
        'win_rate': win_rate,
        'avg_vs_avg': sum(r['vs_avg'] for r in rounds) / len(rounds) if rounds else 0
    }

# ============================================================
# FIRST: IDENTIFY BEST AND WORST YEARS
# ============================================================
print("\n" + "="*100)
print("PERSONAL YEARS RANKING (±2 vs_avg Threshold)")
print("="*100)

year_metrics = {}
for py_num in range(1, 10):
    metrics = calculate_metrics(year_data[py_num])
    if metrics:
        year_metrics[py_num] = metrics

print(f"\n{'Year':<5} {'Total':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<15} {'Win Rate':<12}")
print("-" * 90)

ranked = sorted(year_metrics.items(), key=lambda x: x[1]['win_rate'], reverse=True)
for rank, (py_num, m) in enumerate(ranked, 1):
    rank_mark = ""
    if rank == 1:
        rank_mark = " [BEST]"
    elif rank == 9:
        rank_mark = " [WORST]"
    print(f"{py_num:<5} {m['total_rounds']:<10} {m['beats_field']:<10} {m['misses_field']:<10} {m['threshold_rounds']:<15} {m['win_rate']:<11.1f}%{rank_mark}")

best_year = ranked[0][0]
worst_year = ranked[-1][0]

print(f"\n[OK] BEST YEAR: Year {best_year} ({year_metrics[best_year]['win_rate']:.1f}%)")
print(f"[X] WORST YEAR: Year {worst_year} ({year_metrics[worst_year]['win_rate']:.1f}%)")

# Helper function to run 8-angle analysis
def run_8_angle_analysis(py_num, py_label):
    print("\n\n" + "="*100)
    print(f"COMPREHENSIVE ANALYSIS: {py_label}")
    print("="*100)

    # ANGLE 1: By Color
    print(f"\n{'ANGLE 1: By Color':<100}")
    print(f"{'Color':<15} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("-" * 90)

    color_metrics = {}
    for color in sorted(year_by_color[py_num].keys()):
        metrics = calculate_metrics(year_by_color[py_num][color])
        if metrics:
            color_metrics[color] = metrics

    for color in sorted(color_metrics.keys(), key=lambda x: color_metrics[x]['win_rate'], reverse=True):
        m = color_metrics[color]
        print(f"{color:<15} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

    # ANGLE 2: By Condition
    print(f"\n{'ANGLE 2: By Condition':<100}")
    print(f"{'Condition':<15} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("-" * 90)

    cond_metrics = {}
    for cond in sorted(year_by_condition[py_num].keys()):
        metrics = calculate_metrics(year_by_condition[py_num][cond])
        if metrics:
            cond_metrics[cond] = metrics

    for cond in sorted(cond_metrics.keys(), key=lambda x: cond_metrics[x]['win_rate'], reverse=True):
        m = cond_metrics[cond]
        print(f"{cond:<15} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

    # ANGLE 3: By Round
    print(f"\n{'ANGLE 3: By Round':<100}")
    print(f"{'Round':<8} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("-" * 90)

    round_metrics = {}
    for round_num in sorted(year_by_round[py_num].keys()):
        metrics = calculate_metrics(year_by_round[py_num][round_num])
        if metrics:
            round_metrics[round_num] = metrics

    for round_num in sorted(round_metrics.keys()):
        m = round_metrics[round_num]
        print(f"R{round_num:<7} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

    # ANGLE 4: Color + Condition (Top 15)
    print(f"\n{'ANGLE 4: Top Color + Condition Combos (min 10 threshold rounds)':<100}")
    print(f"{'Color':<12} {'Condition':<12} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("-" * 90)

    combo_metrics = []
    for color in year_by_color_condition[py_num].keys():
        for condition in year_by_color_condition[py_num][color].keys():
            metrics = calculate_metrics(year_by_color_condition[py_num][color][condition])
            if metrics and metrics['threshold_rounds'] >= 10:
                combo_metrics.append({
                    'color': color,
                    'condition': condition,
                    'metrics': metrics
                })

    combo_metrics.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

    for combo in combo_metrics[:15]:
        m = combo['metrics']
        print(f"{combo['color']:<12} {combo['condition']:<12} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

    # ANGLE 5: Color + Round (Top 15)
    print(f"\n{'ANGLE 5: Top Color + Round Combos (min 5 threshold rounds)':<100}")
    print(f"{'Color':<12} {'Round':<8} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("-" * 90)

    color_round_metrics = []
    for color in year_by_color[py_num].keys():
        all_color_rounds = year_by_color[py_num][color]
        for round_num in ['1', '2', '3', '4']:
            round_specific = [r for r in all_color_rounds if r['round_num'] == round_num]
            metrics = calculate_metrics(round_specific)
            if metrics and metrics['threshold_rounds'] >= 5:
                color_round_metrics.append({
                    'color': color,
                    'round': round_num,
                    'metrics': metrics
                })

    color_round_metrics.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

    for item in color_round_metrics[:15]:
        m = item['metrics']
        print(f"{item['color']:<12} R{item['round']:<7} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

# Run analysis for Year 6
run_8_angle_analysis(6, f"PERSONAL YEAR 6 (Best Year: {year_metrics[6]['win_rate']:.1f}% WR)")

# Run analysis for Worst Year
run_8_angle_analysis(worst_year, f"PERSONAL YEAR {worst_year} (Worst Year: {year_metrics[worst_year]['win_rate']:.1f}% WR)")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)
