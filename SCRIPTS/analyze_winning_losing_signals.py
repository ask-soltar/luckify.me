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

            tournament_type = row[tournament_type_idx].strip() if tournament_type_idx < len(row) else ''
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

# Categorize by thresholds
winning_combos = [c for c in combo_metrics if c['metrics']['win_rate'] >= 58.0]
neutral_combos = [c for c in combo_metrics if 42.0 < c['metrics']['win_rate'] < 58.0]
losing_combos = [c for c in combo_metrics if c['metrics']['win_rate'] <= 42.0]

# ============================================================
# OVERVIEW
# ============================================================
print("\n" + "="*120)
print("WINNING vs LOSING SIGNALS (±2 vs_avg threshold)")
print("="*120)

print(f"\nSignal Categorization:")
print(f"  WINNING:  58%+ win rate — {len(winning_combos)} combos")
print(f"  NEUTRAL:  42-58% win rate — {len(neutral_combos)} combos")
print(f"  LOSING:   42% or worse — {len(losing_combos)} combos")

winning_with_samples = [c for c in winning_combos if c['metrics']['threshold_rounds'] >= 20]
losing_with_samples = [c for c in losing_combos if c['metrics']['threshold_rounds'] >= 20]

print(f"\nWith 20+ threshold rounds:")
print(f"  WINNING:  {len(winning_with_samples)} combos")
print(f"  LOSING:   {len(losing_with_samples)} combos")

# ============================================================
# WINNING SIGNALS (58%+)
# ============================================================
print("\n" + "="*120)
print("WINNING SIGNALS (58%+ Win Rate, Min 20 Threshold Rounds)")
print("="*120)

winning_with_samples.sort(key=lambda x: x['metrics']['win_rate'], reverse=True)

print(f"\n{'Cond':<10} {'RType':<12} {'LP':<4} {'PY':<4} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 110)

for combo in winning_with_samples[:50]:
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['life_path']:<4} {combo['personal_year']:<4} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

print(f"\n... and {len(winning_with_samples) - 50} more winning combos" if len(winning_with_samples) > 50 else "")

# ============================================================
# LOSING SIGNALS (42% or worse)
# ============================================================
print("\n" + "="*120)
print("LOSING SIGNALS (42% or Worse Win Rate, Min 20 Threshold Rounds)")
print("="*120)

losing_with_samples.sort(key=lambda x: x['metrics']['win_rate'])

print(f"\n{'Cond':<10} {'RType':<12} {'LP':<4} {'PY':<4} {'Beats':<8} {'Misses':<8} {'Thresh':<8} {'WR%':<8}")
print("-" * 110)

for combo in losing_with_samples[:50]:
    m = combo['metrics']
    print(f"{combo['condition']:<10} {combo['round_type']:<12} {combo['life_path']:<4} {combo['personal_year']:<4} {m['beats_field']:<8} {m['misses_field']:<8} {m['threshold_rounds']:<8} {m['win_rate']:<7.1f}%")

print(f"\n... and {len(losing_with_samples) - 50} more losing combos" if len(losing_with_samples) > 50 else "")

# ============================================================
# PATTERN ANALYSIS: Winning Conditions
# ============================================================
print("\n" + "="*120)
print("WINNING PATTERNS BY DIMENSION")
print("="*120)

# Condition in winning combos
cond_in_winning = defaultdict(int)
for combo in winning_with_samples:
    cond_in_winning[combo['condition']] += 1

print(f"\n{'Condition':<15} {'Count in Winning Signals':<25} {'% of Winning':<15}")
print("-" * 55)
total_w = len(winning_with_samples)
for cond in sorted(cond_in_winning.keys(), key=lambda x: cond_in_winning[x], reverse=True):
    pct = (cond_in_winning[cond] / total_w * 100) if total_w > 0 else 0
    print(f"{cond:<15} {cond_in_winning[cond]:<25} {pct:<14.1f}%")

# Round Type in winning combos
rtype_in_winning = defaultdict(int)
for combo in winning_with_samples:
    rtype_in_winning[combo['round_type']] += 1

print(f"\n{'Round Type':<15} {'Count in Winning Signals':<25} {'% of Winning':<15}")
print("-" * 55)
for rtype in sorted(rtype_in_winning.keys(), key=lambda x: rtype_in_winning[x], reverse=True):
    pct = (rtype_in_winning[rtype] / total_w * 100) if total_w > 0 else 0
    print(f"{rtype:<15} {rtype_in_winning[rtype]:<25} {pct:<14.1f}%")

# Life Path in winning combos
lp_in_winning = defaultdict(int)
for combo in winning_with_samples:
    lp_in_winning[combo['life_path']] += 1

print(f"\n{'Life Path':<15} {'Count in Winning Signals':<25} {'% of Winning':<15}")
print("-" * 55)
for lp in sorted(lp_in_winning.keys(), key=lambda x: lp_in_winning[x], reverse=True):
    pct = (lp_in_winning[lp] / total_w * 100) if total_w > 0 else 0
    print(f"{lp:<15} {lp_in_winning[lp]:<25} {pct:<14.1f}%")

# Personal Year in winning combos
py_in_winning = defaultdict(int)
for combo in winning_with_samples:
    py_in_winning[combo['personal_year']] += 1

print(f"\n{'Personal Year':<15} {'Count in Winning Signals':<25} {'% of Winning':<15}")
print("-" * 55)
for py in sorted(py_in_winning.keys(), key=lambda x: py_in_winning[x], reverse=True):
    pct = (py_in_winning[py] / total_w * 100) if total_w > 0 else 0
    print(f"{py:<15} {py_in_winning[py]:<25} {pct:<14.1f}%")

# ============================================================
# PATTERN ANALYSIS: Losing Conditions
# ============================================================
print("\n" + "="*120)
print("LOSING PATTERNS BY DIMENSION")
print("="*120)

# Condition in losing combos
cond_in_losing = defaultdict(int)
for combo in losing_with_samples:
    cond_in_losing[combo['condition']] += 1

print(f"\n{'Condition':<15} {'Count in Losing Signals':<25} {'% of Losing':<15}")
print("-" * 55)
total_l = len(losing_with_samples)
for cond in sorted(cond_in_losing.keys(), key=lambda x: cond_in_losing[x], reverse=True):
    pct = (cond_in_losing[cond] / total_l * 100) if total_l > 0 else 0
    print(f"{cond:<15} {cond_in_losing[cond]:<25} {pct:<14.1f}%")

# Round Type in losing combos
rtype_in_losing = defaultdict(int)
for combo in losing_with_samples:
    rtype_in_losing[combo['round_type']] += 1

print(f"\n{'Round Type':<15} {'Count in Losing Signals':<25} {'% of Losing':<15}")
print("-" * 55)
for rtype in sorted(rtype_in_losing.keys(), key=lambda x: rtype_in_losing[x], reverse=True):
    pct = (rtype_in_losing[rtype] / total_l * 100) if total_l > 0 else 0
    print(f"{rtype:<15} {rtype_in_losing[rtype]:<25} {pct:<14.1f}%")

# Life Path in losing combos
lp_in_losing = defaultdict(int)
for combo in losing_with_samples:
    lp_in_losing[combo['life_path']] += 1

print(f"\n{'Life Path':<15} {'Count in Losing Signals':<25} {'% of Losing':<15}")
print("-" * 55)
for lp in sorted(lp_in_losing.keys(), key=lambda x: lp_in_losing[x], reverse=True):
    pct = (lp_in_losing[lp] / total_l * 100) if total_l > 0 else 0
    print(f"{lp:<15} {lp_in_losing[lp]:<25} {pct:<14.1f}%")

# Personal Year in losing combos
py_in_losing = defaultdict(int)
for combo in losing_with_samples:
    py_in_losing[combo['personal_year']] += 1

print(f"\n{'Personal Year':<15} {'Count in Losing Signals':<25} {'% of Losing':<15}")
print("-" * 55)
for py in sorted(py_in_losing.keys(), key=lambda x: py_in_losing[x], reverse=True):
    pct = (py_in_losing[py] / total_l * 100) if total_l > 0 else 0
    print(f"{py:<15} {py_in_losing[py]:<25} {pct:<14.1f}%")

print("\n" + "="*120)
print("ANALYSIS COMPLETE")
print("="*120)
