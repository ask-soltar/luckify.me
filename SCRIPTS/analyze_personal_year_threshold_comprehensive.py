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

            # Overall by year
            year_data[py_num].append(round_data)

            # By color
            if color:
                year_by_color[py_num][color].append(round_data)

            # By condition
            if condition:
                year_by_condition[py_num][condition].append(round_data)

            # By round
            if round_num:
                year_by_round[py_num][round_num].append(round_data)

            # By color + condition
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
# ANALYSIS 1: Personal Years Overall (±2 Threshold)
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 1: PERSONAL YEARS 1-9 OVERALL (±2 vs_avg Threshold)")
print("="*100)

year_metrics = {}
for py_num in range(1, 10):
    metrics = calculate_metrics(year_data[py_num])
    if metrics:
        year_metrics[py_num] = metrics

print(f"\n{'Year':<5} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12} {'Avg vs_avg':<12}")
print("-" * 90)

for py_num in range(1, 10):
    if py_num in year_metrics:
        m = year_metrics[py_num]
        print(f"{py_num:<5} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}% {m['avg_vs_avg']:<12.3f}")

# ============================================================
# ANALYSIS 2: Personal Year 7 by Color
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 2: PERSONAL YEAR 7 BY COLOR (±2 vs_avg Threshold)")
print("="*100)

py7_color_metrics = {}
for color in sorted(year_by_color[7].keys()):
    metrics = calculate_metrics(year_by_color[7][color])
    if metrics:
        py7_color_metrics[color] = metrics

print(f"\n{'Color':<15} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12} {'Avg vs_avg':<12}")
print("-" * 90)

for color in sorted(py7_color_metrics.keys(), key=lambda x: py7_color_metrics[x]['win_rate'], reverse=True):
    m = py7_color_metrics[color]
    print(f"{color:<15} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}% {m['avg_vs_avg']:<12.3f}")

# ============================================================
# ANALYSIS 3: Personal Year 7 by Condition
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 3: PERSONAL YEAR 7 BY CONDITION (±2 vs_avg Threshold)")
print("="*100)

py7_cond_metrics = {}
for cond in sorted(year_by_condition[7].keys()):
    metrics = calculate_metrics(year_by_condition[7][cond])
    if metrics:
        py7_cond_metrics[cond] = metrics

print(f"\n{'Condition':<15} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12} {'Avg vs_avg':<12}")
print("-" * 90)

for cond in sorted(py7_cond_metrics.keys(), key=lambda x: py7_cond_metrics[x]['win_rate'], reverse=True):
    m = py7_cond_metrics[cond]
    print(f"{cond:<15} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}% {m['avg_vs_avg']:<12.3f}")

# ============================================================
# ANALYSIS 4: Personal Year 7 by Round
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 4: PERSONAL YEAR 7 BY ROUND (±2 vs_avg Threshold)")
print("="*100)

py7_round_metrics = {}
for round_num in sorted(year_by_round[7].keys()):
    metrics = calculate_metrics(year_by_round[7][round_num])
    if metrics:
        py7_round_metrics[round_num] = metrics

print(f"\n{'Round':<8} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12} {'Avg vs_avg':<12}")
print("-" * 90)

for round_num in sorted(py7_round_metrics.keys()):
    m = py7_round_metrics[round_num]
    print(f"R{round_num:<7} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}% {m['avg_vs_avg']:<12.3f}")

# ============================================================
# ANALYSIS 5: Personal Year 7 + Color + Condition
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 5: PERSONAL YEAR 7 BY COLOR + CONDITION (±2 vs_avg Threshold)")
print("="*100)

print("\nBest Combinations (top 15):")
combo_metrics = []
for color in year_by_color_condition[7].keys():
    for condition in year_by_color_condition[7][color].keys():
        metrics = calculate_metrics(year_by_color_condition[7][color][condition])
        if metrics and metrics['threshold_rounds'] >= 10:  # Only include combos with 10+ threshold rounds
            combo_metrics.append({
                'color': color,
                'condition': condition,
                'metrics': metrics
            })

combo_metrics.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

print(f"\n{'Color':<12} {'Condition':<12} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
print("-" * 85)

for i, combo in enumerate(combo_metrics[:15], 1):
    m = combo['metrics']
    print(f"{combo['color']:<12} {combo['condition']:<12} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

# ============================================================
# ANALYSIS 6: Compare Year 7 vs All Other Years
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 6: PERSONAL YEAR 7 vs ALL OTHER YEARS (±2 vs_avg Threshold)")
print("="*100)

year7_metrics = year_metrics.get(7)
other_years_combined = defaultdict()
other_years_combined['total_rounds'] = sum(m['total_rounds'] for py, m in year_metrics.items() if py != 7)
other_years_combined['beats_field'] = sum(m['beats_field'] for py, m in year_metrics.items() if py != 7)
other_years_combined['misses_field'] = sum(m['misses_field'] for py, m in year_metrics.items() if py != 7)
other_years_combined['threshold_rounds'] = other_years_combined['beats_field'] + other_years_combined['misses_field']
other_years_combined['win_rate'] = (other_years_combined['beats_field'] / other_years_combined['threshold_rounds'] * 100) if other_years_combined['threshold_rounds'] > 0 else 0

print(f"\n{'Group':<20} {'Total':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<15} {'Win Rate':<12}")
print("-" * 85)
print(f"{'Year 7':<20} {year7_metrics['total_rounds']:<10} {year7_metrics['beats_field']:<10} {year7_metrics['misses_field']:<10} {year7_metrics['threshold_rounds']:<15} {year7_metrics['win_rate']:<11.1f}%")
print(f"{'Years 1-6, 8-9':<20} {other_years_combined['total_rounds']:<10} {other_years_combined['beats_field']:<10} {other_years_combined['misses_field']:<10} {other_years_combined['threshold_rounds']:<15} {other_years_combined['win_rate']:<11.1f}%")
print(f"{'DIFFERENCE':<20} {'':10} {'':10} {'':10} {'':15} {year7_metrics['win_rate'] - other_years_combined['win_rate']:+.1f}%")

# ============================================================
# ANALYSIS 7: All Years by Color
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 7: ALL PERSONAL YEARS BY COLOR (±2 vs_avg Threshold)")
print("="*100)

all_colors = set()
for py in range(1, 10):
    all_colors.update(year_by_color[py].keys())

for color in sorted(all_colors):
    print(f"\n{color.upper()}:")
    print(f"  {'Year':<5} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
    print("  " + "-" * 70)

    for py_num in range(1, 10):
        metrics = calculate_metrics(year_by_color[py_num].get(color, []))
        if metrics:
            print(f"  {py_num:<5} {metrics['total_rounds']:<8} {metrics['beats_field']:<8} {metrics['misses_field']:<8} {metrics['threshold_rounds']:<12} {metrics['win_rate']:<11.1f}%")

# ============================================================
# ANALYSIS 8: Year 7 + Color + Round
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 8: PERSONAL YEAR 7 BY COLOR + ROUND (±2 vs_avg Threshold - Top 20)")
print("="*100)

color_round_metrics = []
for color in year_by_color[7].keys():
    # Get all rounds for this color in Year 7
    all_color_rounds = year_by_color[7][color]

    # Group by round
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

print(f"\n{'Color':<12} {'Round':<7} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<12}")
print("-" * 85)

for item in color_round_metrics[:20]:
    m = item['metrics']
    print(f"{item['color']:<12} R{item['round']:<6} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}%")

print("\n" + "="*100)
print("Analysis Complete")
print("="*100)
