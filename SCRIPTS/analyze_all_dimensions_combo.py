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
            # Parse values
            vs_avg = float(row[vs_avg_idx]) if vs_avg_idx < len(row) and row[vs_avg_idx] else None
            if vs_avg is None:
                continue

            tournament_type = row[tournament_type_idx].strip() if tournament_type_idx < len(row) else ''
            # Filter: Only S and NS tournaments
            if tournament_type not in ['S', 'NS']:
                continue

            condition = row[condition_idx].strip() if condition_idx < len(row) else ''
            if not condition:
                continue

            round_type = row[round_type_idx].strip() if round_type_idx < len(row) else ''
            if not round_type or round_type == 'REMOVE':
                continue

            life_path = row[life_path_idx].strip() if life_path_idx < len(row) else ''
            if not life_path or not life_path.isdigit():
                continue

            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or not personal_year.isdigit():
                continue

            # Create combo key
            combo_key = (condition, round_type, tournament_type, int(life_path), int(personal_year))

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
        condition, round_type, tournament_type, life_path, personal_year = combo_key
        combo_metrics.append({
            'condition': condition,
            'round_type': round_type,
            'tournament_type': tournament_type,
            'life_path': life_path,
            'personal_year': personal_year,
            'metrics': metrics
        })

# ============================================================
# OVERVIEW
# ============================================================
print("\n" + "="*120)
print("COMPREHENSIVE 5-DIMENSION ANALYSIS")
print("Condition × Round Type × Tournament Type × Life Path × Personal Year")
print("="*120)

print(f"\nTotal combos with data: {len(combo_metrics)}")
print(f"Combos with 10+ threshold rounds: {sum(1 for c in combo_metrics if c['metrics']['threshold_rounds'] >= 10)}")
print(f"Combos with 50+ threshold rounds: {sum(1 for c in combo_metrics if c['metrics']['threshold_rounds'] >= 50)}")
print(f"Combos with 100+ threshold rounds: {sum(1 for c in combo_metrics if c['metrics']['threshold_rounds'] >= 100)}")

# ============================================================
# TOP 50 COMBOS (by win rate, min 20 threshold rounds)
# ============================================================
print("\n" + "="*120)
print("TOP 50 COMBOS BY WIN RATE (minimum 20 threshold rounds)")
print("="*120)

top_combos = [c for c in combo_metrics if c['metrics']['threshold_rounds'] >= 20]
top_combos.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

print(f"\n{'Cond':<10} {'RType':<12} {'TType':<6} {'LP':<4} {'PY':<4} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 120)

for i, combo in enumerate(top_combos[:50], 1):
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['tournament_type']:<6} {combo['life_path']:<4} {combo['personal_year']:<4} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

# ============================================================
# BOTTOM 30 COMBOS (by win rate, min 20 threshold rounds)
# ============================================================
print("\n" + "="*120)
print("BOTTOM 30 COMBOS BY WIN RATE (minimum 20 threshold rounds)")
print("="*120)

bottom_combos = sorted(top_combos, key=lambda x: x['metrics']['win_rate'])

print(f"\n{'Cond':<10} {'RType':<12} {'TType':<6} {'LP':<4} {'PY':<4} {'Total':<8} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 120)

for combo in bottom_combos[:30]:
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['tournament_type']:<6} {combo['life_path']:<4} {combo['personal_year']:<4} {m['total_rounds']:<8} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

# ============================================================
# PATTERN 1: Best Condition
# ============================================================
print("\n" + "="*120)
print("PATTERN 1: CONDITION RANKING (all combos)")
print("="*120)

cond_stats = defaultdict(lambda: {'beats': 0, 'misses': 0})
for combo in combo_metrics:
    cond = combo['condition']
    m = combo['metrics']
    cond_stats[cond]['beats'] += m['beats_field']
    cond_stats[cond]['misses'] += m['misses_field']

print(f"\n{'Condition':<12} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 60)

for cond in sorted(cond_stats.keys(), key=lambda x: cond_stats[x]['beats'] / (cond_stats[x]['beats'] + cond_stats[x]['misses']), reverse=True):
    beats = cond_stats[cond]['beats']
    misses = cond_stats[cond]['misses']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{cond:<12} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 2: Best Round Type
# ============================================================
print("\n" + "="*120)
print("PATTERN 2: ROUND TYPE RANKING (all combos)")
print("="*120)

rtype_stats = defaultdict(lambda: {'beats': 0, 'misses': 0})
for combo in combo_metrics:
    rtype = combo['round_type']
    m = combo['metrics']
    rtype_stats[rtype]['beats'] += m['beats_field']
    rtype_stats[rtype]['misses'] += m['misses_field']

print(f"\n{'Round Type':<15} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 60)

for rtype in sorted(rtype_stats.keys(), key=lambda x: rtype_stats[x]['beats'] / (rtype_stats[x]['beats'] + rtype_stats[x]['misses']), reverse=True):
    beats = rtype_stats[rtype]['beats']
    misses = rtype_stats[rtype]['misses']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{rtype:<15} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 3: Best Life Path
# ============================================================
print("\n" + "="*120)
print("PATTERN 3: LIFE PATH RANKING (all combos)")
print("="*120)

lp_stats = defaultdict(lambda: {'beats': 0, 'misses': 0})
for combo in combo_metrics:
    lp = combo['life_path']
    m = combo['metrics']
    lp_stats[lp]['beats'] += m['beats_field']
    lp_stats[lp]['misses'] += m['misses_field']

print(f"\n{'Life Path':<12} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 60)

for lp in sorted(lp_stats.keys(), key=lambda x: lp_stats[x]['beats'] / (lp_stats[x]['beats'] + lp_stats[x]['misses']), reverse=True):
    beats = lp_stats[lp]['beats']
    misses = lp_stats[lp]['misses']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{lp:<12} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 4: Best Personal Year
# ============================================================
print("\n" + "="*120)
print("PATTERN 4: PERSONAL YEAR RANKING (all combos)")
print("="*120)

py_stats = defaultdict(lambda: {'beats': 0, 'misses': 0})
for combo in combo_metrics:
    py = combo['personal_year']
    m = combo['metrics']
    py_stats[py]['beats'] += m['beats_field']
    py_stats[py]['misses'] += m['misses_field']

print(f"\n{'Personal Year':<15} {'Beats':<10} {'Misses':<10} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 60)

for py in sorted(py_stats.keys(), key=lambda x: py_stats[x]['beats'] / (py_stats[x]['beats'] + py_stats[x]['misses']), reverse=True):
    beats = py_stats[py]['beats']
    misses = py_stats[py]['misses']
    wr = (beats / (beats + misses) * 100) if (beats + misses) > 0 else 0
    print(f"{py:<15} {beats:<10} {misses:<10} {beats + misses:<12} {wr:<9.1f}%")

# ============================================================
# PATTERN 5: Best Life Path + Personal Year
# ============================================================
print("\n" + "="*120)
print("PATTERN 5: LIFE PATH + PERSONAL YEAR (top 30 combos, min 50 rounds)")
print("="*120)

lp_py_combos = []
for combo in combo_metrics:
    lp = combo['life_path']
    py = combo['personal_year']
    m = combo['metrics']
    if m['threshold_rounds'] >= 50:
        lp_py_combos.append({
            'lp': lp,
            'py': py,
            'metrics': m
        })

lp_py_combos.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

print(f"\n{'LP':<4} {'PY':<4} {'Beats':<8} {'Misses':<8} {'Threshold':<12} {'Win Rate':<10}")
print("-" * 60)

for combo in lp_py_combos[:30]:
    m = combo['metrics']
    print(f"{combo['lp']:<4} {combo['py']:<4} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<12} {m['win_rate']:<9.1f}%")

print("\n" + "="*120)
print("ANALYSIS COMPLETE")
print("="*120)
