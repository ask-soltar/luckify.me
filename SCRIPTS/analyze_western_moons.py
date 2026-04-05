import csv
from collections import defaultdict
import sys
import io

# Fix Unicode on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"

# Store data by moon phase
moon_data = defaultdict(list)

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    moonwest_idx = header.index('moonwest')
    vs_avg_idx = header.index('vs_avg')
    round_num_idx = header.index('round_num')
    condition_idx = header.index('condition')
    player_name_idx = header.index('player_name')

    for row in reader:
        if not row or row[player_name_idx].strip() == '':
            continue

        try:
            vs_avg = float(row[vs_avg_idx]) if vs_avg_idx < len(row) and row[vs_avg_idx] else None
            if vs_avg is None:
                continue

            moonwest = row[moonwest_idx].strip() if moonwest_idx < len(row) else ''
            if not moonwest or moonwest == '':
                continue

            round_num = row[round_num_idx].strip() if round_num_idx < len(row) else ''
            condition = row[condition_idx].strip() if condition_idx < len(row) else ''

            moon_data[moonwest].append({
                'vs_avg': vs_avg,
                'round_num': round_num,
                'condition': condition
            })

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
    avg_vs_avg = sum(r['vs_avg'] for r in rounds) / len(rounds) if rounds else 0

    return {
        'total_rounds': len(rounds),
        'beats_field': beats_field,
        'misses_field': misses_field,
        'threshold_rounds': threshold_rounds,
        'win_rate': win_rate,
        'avg_vs_avg': avg_vs_avg
    }

# ============================================================
# ANALYSIS 1: Overall Moon Phase Rankings
# ============================================================
print("\n" + "="*120)
print("WESTERN MOON PHASES: OVERALL PERFORMANCE (±2 vs_avg Threshold)")
print("="*120)

moon_metrics = {}
for moon in sorted(moon_data.keys()):
    metrics = calculate_metrics(moon_data[moon])
    if metrics:
        moon_metrics[moon] = metrics

print(f"\n{'Moon Phase':<20} {'Total':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<12} {'Avg vs_avg':<12}")
print("-" * 110)

ranked = sorted(moon_metrics.items(), key=lambda x: x[1]['win_rate'], reverse=True)
for rank, (moon, m) in enumerate(ranked, 1):
    print(f"{rank:2d}. {moon:<17} {m['total_rounds']:<10} {m['beats_field']:<10} {m['misses_field']:<10} {m['threshold_rounds']:<12} {m['win_rate']:<11.1f}% {m['avg_vs_avg']:<11.3f}")

# ============================================================
# ANALYSIS 2: Moon Phase Groups - Correlations
# ============================================================
print("\n" + "="*120)
print("MOON PHASE GROUPING ANALYSIS")
print("Testing correlation between similar moon phases")
print("="*120)

# Define moon groups
waxing_phases = ['Waxing Crescent', 'Waxing Gibbous']
waning_phases = ['Waning Crescent', 'Waning Gibbous']
quarter_phases = ['First Quarter', 'Last Quarter']
extreme_phases = ['New Moon', 'Full Moon']

print("\n--- WAXING PHASES (Waxing Crescent vs Waxing Gibbous) ---")
waxing_corr = []
for phase in waxing_phases:
    if phase in moon_metrics:
        m = moon_metrics[phase]
        waxing_corr.append((phase, m['win_rate']))
        print(f"{phase:<20} {m['win_rate']:<7.1f}%")

if len(waxing_corr) == 2:
    diff = abs(waxing_corr[0][1] - waxing_corr[1][1])
    corr_level = "HIGH" if diff < 2 else "MODERATE" if diff < 5 else "LOW"
    print(f"→ Correlation: {corr_level} (difference: {diff:.1f} pp)")

print("\n--- WANING PHASES (Waning Crescent vs Waning Gibbous) ---")
waning_corr = []
for phase in waning_phases:
    if phase in moon_metrics:
        m = moon_metrics[phase]
        waning_corr.append((phase, m['win_rate']))
        print(f"{phase:<20} {m['win_rate']:<7.1f}%")

if len(waning_corr) == 2:
    diff = abs(waning_corr[0][1] - waning_corr[1][1])
    corr_level = "HIGH" if diff < 2 else "MODERATE" if diff < 5 else "LOW"
    print(f"→ Correlation: {corr_level} (difference: {diff:.1f} pp)")

print("\n--- QUARTER PHASES (First Quarter vs Last Quarter) ---")
quarter_corr = []
for phase in quarter_phases:
    if phase in moon_metrics:
        m = moon_metrics[phase]
        quarter_corr.append((phase, m['win_rate']))
        print(f"{phase:<20} {m['win_rate']:<7.1f}%")

if len(quarter_corr) == 2:
    diff = abs(quarter_corr[0][1] - quarter_corr[1][1])
    corr_level = "HIGH" if diff < 2 else "MODERATE" if diff < 5 else "LOW"
    print(f"→ Correlation: {corr_level} (difference: {diff:.1f} pp)")

print("\n--- EXTREME PHASES (New Moon vs Full Moon) ---")
extreme_corr = []
for phase in extreme_phases:
    if phase in moon_metrics:
        m = moon_metrics[phase]
        extreme_corr.append((phase, m['win_rate']))
        print(f"{phase:<20} {m['win_rate']:<7.1f}%")

if len(extreme_corr) == 2:
    diff = abs(extreme_corr[0][1] - extreme_corr[1][1])
    corr_level = "HIGH" if diff < 2 else "MODERATE" if diff < 5 else "LOW"
    print(f"→ Correlation: {corr_level} (difference: {diff:.1f} pp)")

# ============================================================
# ANALYSIS 3: Moon Phase Categories (Waxing vs Waning)
# ============================================================
print("\n" + "="*120)
print("BROAD CATEGORY ANALYSIS: Waxing vs Waning vs Other")
print("="*120)

all_waxing = ['Waxing Crescent', 'Waxing Gibbous', 'First Quarter', 'New Moon']
all_waning = ['Waning Crescent', 'Waning Gibbous', 'Last Quarter', 'Full Moon']

waxing_combined = {'beats': 0, 'misses': 0, 'total': 0}
waning_combined = {'beats': 0, 'misses': 0, 'total': 0}

for moon in moon_data.keys():
    m = moon_metrics[moon]
    if moon in all_waxing:
        waxing_combined['beats'] += m['beats_field']
        waxing_combined['misses'] += m['misses_field']
        waxing_combined['total'] += m['total_rounds']
    elif moon in all_waning:
        waning_combined['beats'] += m['beats_field']
        waning_combined['misses'] += m['misses_field']
        waning_combined['total'] += m['total_rounds']

waxing_wr = (waxing_combined['beats'] / (waxing_combined['beats'] + waxing_combined['misses']) * 100) if (waxing_combined['beats'] + waxing_combined['misses']) > 0 else 0
waning_wr = (waning_combined['beats'] / (waning_combined['beats'] + waning_combined['misses']) * 100) if (waning_combined['beats'] + waning_combined['misses']) > 0 else 0

print(f"\n{'Category':<20} {'Total':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<12}")
print("-" * 80)
print(f"{'WAXING':<20} {waxing_combined['total']:<10} {waxing_combined['beats']:<10} {waxing_combined['misses']:<10} {waxing_combined['beats'] + waxing_combined['misses']:<12} {waxing_wr:<11.1f}%")
print(f"{'WANING':<20} {waning_combined['total']:<10} {waning_combined['beats']:<10} {waning_combined['misses']:<10} {waning_combined['beats'] + waning_combined['misses']:<12} {waning_wr:<11.1f}%")

diff = abs(waxing_wr - waning_wr)
print(f"\n→ Difference: {diff:.1f} pp")
if diff < 2:
    print("→ Assessment: No meaningful difference between Waxing and Waning overall")
elif diff < 5:
    print("→ Assessment: Slight difference, could collapse with minimal loss")
else:
    print("→ Assessment: Significant difference, should keep separate")

# ============================================================
# ANALYSIS 4: Moon Phase by Round Type
# ============================================================
print("\n" + "="*120)
print("MOON PHASE PERFORMANCE BY ROUND TYPE")
print("="*120)

moon_by_round = defaultdict(lambda: defaultdict(list))
for moon in moon_data.keys():
    for round_data in moon_data[moon]:
        round_num = round_data['round_num']
        moon_by_round[moon][round_num].append(round_data)

print("\nTop performers by round:")
for round_type in ['1', '2', '3', '4']:
    print(f"\nROUND {round_type}:")
    round_results = []
    for moon in moon_metrics.keys():
        if round_type in moon_by_round[moon] and moon_by_round[moon][round_type]:
            metrics = calculate_metrics(moon_by_round[moon][round_type])
            if metrics and metrics['threshold_rounds'] >= 10:
                round_results.append((moon, metrics['win_rate'], metrics['threshold_rounds']))

    round_results.sort(key=lambda x: x[1], reverse=True)
    print(f"  {'Moon Phase':<20} {'Win Rate':<12} {'Threshold Rounds':<15}")
    print("  " + "-" * 50)
    for moon, wr, thresh in round_results[:5]:
        print(f"  {moon:<20} {wr:<11.1f}% {thresh:<15}")

# ============================================================
# ANALYSIS 5: Moon Phase by Condition
# ============================================================
print("\n" + "="*120)
print("MOON PHASE PERFORMANCE BY CONDITION")
print("="*120)

moon_by_cond = defaultdict(lambda: defaultdict(list))
for moon in moon_data.keys():
    for cond_data in moon_data[moon]:
        condition = cond_data['condition']
        moon_by_cond[moon][condition].append(cond_data)

for condition in ['Calm', 'Moderate', 'Tough']:
    print(f"\n{condition.upper()} CONDITIONS:")
    cond_results = []
    for moon in moon_metrics.keys():
        if condition in moon_by_cond[moon] and moon_by_cond[moon][condition]:
            metrics = calculate_metrics(moon_by_cond[moon][condition])
            if metrics and metrics['threshold_rounds'] >= 10:
                cond_results.append((moon, metrics['win_rate'], metrics['threshold_rounds']))

    cond_results.sort(key=lambda x: x[1], reverse=True)
    print(f"  {'Moon Phase':<20} {'Win Rate':<12} {'Threshold Rounds':<15}")
    print("  " + "-" * 50)
    for moon, wr, thresh in cond_results[:5]:
        print(f"  {moon:<20} {wr:<11.1f}% {thresh:<15}")

print("\n" + "="*120)
print("ANALYSIS COMPLETE")
print("="*120)
