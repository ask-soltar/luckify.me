import csv
from collections import defaultdict

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"

# Store all combos
all_combos = defaultdict(list)

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    vs_avg_idx = header.index('vs_avg')
    condition_idx = header.index('condition')
    round_type_idx = header.index('round_type')
    tournament_type_idx = header.index('tournament_type')
    life_path_idx = header.index('life_path')
    personal_year_idx = header.index('Personal Year')
    player_name_idx = header.index('player_name')

    for row in reader:
        if not row or row[player_name_idx].strip() == '':
            continue

        try:
            vs_avg = float(row[vs_avg_idx]) if vs_avg_idx < len(row) and row[vs_avg_idx] else None
            if vs_avg is None:
                continue

            # Merge tournament types (S + NS both = "Stroke Play")
            tournament_type = row[tournament_type_idx].strip() if tournament_type_idx < len(row) else ''
            if tournament_type not in ['S', 'NS']:
                continue
            tournament_merged = 'StrokePlay'  # Merge both into single category

            # Collapse condition to Calm vs Non-Calm
            condition = row[condition_idx].strip() if condition_idx < len(row) else ''
            if not condition:
                continue
            condition_collapsed = 'Calm' if condition == 'Calm' else 'Non-Calm'

            round_type = row[round_type_idx].strip() if round_type_idx < len(row) else ''
            if not round_type or round_type == 'REMOVE':
                continue

            life_path = row[life_path_idx].strip() if life_path_idx < len(row) else ''
            if not life_path or not life_path.isdigit():
                continue

            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or not personal_year.isdigit():
                continue

            combo_key = (condition_collapsed, round_type, int(life_path), int(personal_year))
            all_combos[combo_key].append({'vs_avg': vs_avg})

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
        'win_rate': win_rate
    }

# Calculate metrics for all combos
combo_metrics = []
for combo_key, rounds in all_combos.items():
    metrics = calculate_metrics(rounds)
    if metrics:
        condition, round_type, life_path, personal_year = combo_key
        combo_metrics.append({
            'condition': condition,
            'round_type': round_type,
            'life_path': life_path,
            'personal_year': personal_year,
            'metrics': metrics
        })

# Categorize
winning_combos = [c for c in combo_metrics if c['metrics']['win_rate'] >= 58.0]
neutral_combos = [c for c in combo_metrics if 42.0 < c['metrics']['win_rate'] < 58.0]
losing_combos = [c for c in combo_metrics if c['metrics']['win_rate'] <= 42.0]

# ============================================================
# OVERVIEW
# ============================================================
print("\n" + "="*120)
print("COLLAPSED DIMENSIONS ANALYSIS (Option 3 & 4)")
print("Condition: Calm vs Non-Calm | Tournament: Stroke Play (merged S+NS)")
print("Life Path: 1-9 | Personal Year: 1-9 | Round Type: 4 types")
print("="*120)

print(f"\nDimensionality:")
print(f"  Before: 3 conditions x 4 round types x 2 tournaments x 9 LP x 9 PY = 1,944 theoretical")
print(f"  After:  2 conditions x 4 round types x 1 tournament x 9 LP x 9 PY = 648 theoretical")
print(f"  Actual combos with data: {len(combo_metrics)}")

print(f"\nSignal Distribution:")
print(f"  WINNING (58%+):  {len(winning_combos)} combos")
print(f"  NEUTRAL (42-58%): {len(neutral_combos)} combos")
print(f"  LOSING (<=42%):   {len(losing_combos)} combos")

# Filter for meaningful samples
winning_min20 = [c for c in winning_combos if c['metrics']['threshold_rounds'] >= 20]
losing_min20 = [c for c in losing_combos if c['metrics']['threshold_rounds'] >= 20]

print(f"\nWith 20+ threshold rounds:")
print(f"  WINNING: {len(winning_min20)} combos")
print(f"  LOSING:  {len(losing_min20)} combos")

# Average sample sizes
if winning_combos:
    avg_winning = sum(c['metrics']['total_rounds'] for c in winning_combos) / len(winning_combos)
    print(f"\nAverage sample size:")
    print(f"  Winning combos: {avg_winning:.0f} total rounds per combo")

if losing_combos:
    avg_losing = sum(c['metrics']['total_rounds'] for c in losing_combos) / len(losing_combos)
    print(f"  Losing combos:  {avg_losing:.0f} total rounds per combo")

# ============================================================
# TOP 30 WINNING SIGNALS
# ============================================================
print("\n" + "="*120)
print("TOP 30 WINNING SIGNALS (58%+ Win Rate)")
print("="*120)

winning_combos.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

print(f"\n{'Cond':<10} {'RType':<12} {'LP':<4} {'PY':<4} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 110)

for combo in winning_combos[:30]:
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['life_path']:<4} {combo['personal_year']:<4} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

# ============================================================
# TOP 30 LOSING SIGNALS
# ============================================================
print("\n" + "="*120)
print("TOP 30 LOSING SIGNALS (42% or Worse Win Rate)")
print("="*120)

losing_combos.sort(key=lambda x: x['metrics']['win_rate'])

print(f"\n{'Cond':<10} {'RType':<12} {'LP':<4} {'PY':<4} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 110)

for combo in losing_combos[:30]:
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['life_path']:<4} {combo['personal_year']:<4} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

# ============================================================
# PATTERN 1: Condition
# ============================================================
print("\n" + "="*120)
print("PATTERN 1: CONDITION (Calm vs Non-Calm)")
print("="*120)

cond_stats = defaultdict(lambda: {'beats': 0, 'misses': 0, 'combos': 0})
for combo in combo_metrics:
    cond = combo['condition']
    m = combo['metrics']
    cond_stats[cond]['beats'] += m['beats_field']
    cond_stats[cond]['misses'] += m['misses_field']
    cond_stats[cond]['combos'] += 1

print(f"\n{'Condition':<15} {'Combos':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 70)

for cond in sorted(cond_stats.keys(), key=lambda x: cond_stats[x]['beats'] / (cond_stats[x]['beats'] + cond_stats[x]['misses']), reverse=True):
    beats = cond_stats[cond]['beats']
    misses = cond_stats[cond]['misses']
    combos = cond_stats[cond]['combos']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{cond:<15} {combos:<10} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 2: Round Type
# ============================================================
print("\n" + "="*120)
print("PATTERN 2: ROUND TYPE")
print("="*120)

rtype_stats = defaultdict(lambda: {'beats': 0, 'misses': 0, 'combos': 0})
for combo in combo_metrics:
    rtype = combo['round_type']
    m = combo['metrics']
    rtype_stats[rtype]['beats'] += m['beats_field']
    rtype_stats[rtype]['misses'] += m['misses_field']
    rtype_stats[rtype]['combos'] += 1

print(f"\n{'Round Type':<15} {'Combos':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 70)

for rtype in sorted(rtype_stats.keys(), key=lambda x: rtype_stats[x]['beats'] / (rtype_stats[x]['beats'] + rtype_stats[x]['misses']), reverse=True):
    beats = rtype_stats[rtype]['beats']
    misses = rtype_stats[rtype]['misses']
    combos = rtype_stats[rtype]['combos']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{rtype:<15} {combos:<10} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 3: Life Path
# ============================================================
print("\n" + "="*120)
print("PATTERN 3: LIFE PATH (1-9)")
print("="*120)

lp_stats = defaultdict(lambda: {'beats': 0, 'misses': 0, 'combos': 0})
for combo in combo_metrics:
    lp = combo['life_path']
    m = combo['metrics']
    lp_stats[lp]['beats'] += m['beats_field']
    lp_stats[lp]['misses'] += m['misses_field']
    lp_stats[lp]['combos'] += 1

print(f"\n{'Life Path':<12} {'Combos':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 70)

for lp in sorted(lp_stats.keys(), key=lambda x: lp_stats[x]['beats'] / (lp_stats[x]['beats'] + lp_stats[x]['misses']), reverse=True):
    beats = lp_stats[lp]['beats']
    misses = lp_stats[lp]['misses']
    combos = lp_stats[lp]['combos']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{lp:<12} {combos:<10} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 4: Personal Year
# ============================================================
print("\n" + "="*120)
print("PATTERN 4: PERSONAL YEAR (1-9)")
print("="*120)

py_stats = defaultdict(lambda: {'beats': 0, 'misses': 0, 'combos': 0})
for combo in combo_metrics:
    py = combo['personal_year']
    m = combo['metrics']
    py_stats[py]['beats'] += m['beats_field']
    py_stats[py]['misses'] += m['misses_field']
    py_stats[py]['combos'] += 1

print(f"\n{'Personal Year':<15} {'Combos':<10} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 70)

for py in sorted(py_stats.keys(), key=lambda x: py_stats[x]['beats'] / (py_stats[x]['beats'] + py_stats[x]['misses']), reverse=True):
    beats = py_stats[py]['beats']
    misses = py_stats[py]['misses']
    combos = py_stats[py]['combos']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{py:<15} {combos:<10} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 5: Calm vs Non-Calm by Round Type
# ============================================================
print("\n" + "="*120)
print("PATTERN 5: CONDITION × ROUND TYPE (Sample Sizes)")
print("="*120)

combo_samples = defaultdict(lambda: defaultdict(int))
for combo in combo_metrics:
    cond = combo['condition']
    rtype = combo['round_type']
    m = combo['metrics']
    combo_samples[cond][rtype] += 1

print(f"\n{'Condition':<15} {'Open':<15} {'Positioning':<15} {'Closing':<15} {'Survival':<15}")
print("-" * 70)

for cond in ['Calm', 'Non-Calm']:
    counts = [combo_samples[cond][rtype] for rtype in ['Open', 'Positioning', 'Closing', 'Survival']]
    print(f"{cond:<15} {counts[0]:<15} {counts[1]:<15} {counts[2]:<15} {counts[3]:<15}")

print("\n" + "="*120)
print("ANALYSIS COMPLETE")
print("="*120)
