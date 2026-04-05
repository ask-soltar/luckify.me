import csv
from collections import defaultdict
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (6).csv"

matchup_data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find correct column indices
    lp_score_idx = 52  # LP SCore
    bb_idx = 53         # Player/pick names (blank header)
    wl_idx = 47         # W/L results

    print(f"Using columns:")
    print(f"  Col {lp_score_idx}: LP Score")
    print(f"  Col {bb_idx}: Player picks (blank header)")
    print(f"  Col {wl_idx}: W/L results\n")

    for row in reader:
        if not row or len(row) < max(lp_score_idx + 1, wl_idx + 1, bb_idx + 1):
            continue

        try:
            # Get LP Score
            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str == '' or lp_score_str == '#REF!':
                continue

            lp_score = float(lp_score_str)

            # Get player pick name
            bb_val = row[bb_idx].strip() if bb_idx < len(row) else ''
            if not bb_val:
                continue

            # Get W/L result
            wl = row[wl_idx].strip() if wl_idx < len(row) else ''

            # Determine if win or loss
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or 'Loss' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            matchup_data.append({
                'lp_score': lp_score,
                'player': bb_val,
                'result': is_win
            })

        except (ValueError, IndexError):
            continue

print(f"Total records parsed: {len(matchup_data)}\n")

if not matchup_data:
    print("ERROR: No data found!")
    exit(1)

# ============================================================
# ANALYSIS 1: Distribution
# ============================================================
print("=" * 100)
print("LP SCORE THRESHOLD ANALYSIS (with W/L results)")
print("=" * 100)

lp_scores = [d['lp_score'] for d in matchup_data]
wins = [d['lp_score'] for d in matchup_data if d['result']]
losses = [d['lp_score'] for d in matchup_data if not d['result']]

print(f"\nOverall Stats:")
print(f"  Total picks with W/L: {len(matchup_data)}")
print(f"  Wins: {len(wins)} ({len(wins)/len(matchup_data)*100:.1f}%)")
print(f"  Losses: {len(losses)} ({len(losses)/len(matchup_data)*100:.1f}%)")
print(f"  Overall win rate: {len(wins)/len(matchup_data)*100:.1f}%")

print(f"\nLP Score Statistics:")
print(f"  Min: {min(lp_scores):.2f}")
print(f"  Max: {max(lp_scores):.2f}")
print(f"  Mean: {statistics.mean(lp_scores):.2f}")
print(f"  Median: {statistics.median(lp_scores):.2f}")

# ============================================================
# ANALYSIS 2: Threshold Analysis
# ============================================================
print("\n" + "=" * 100)
print("THRESHOLD FILTERING (Test Different Cutoff Scores)")
print("=" * 100)

thresholds = [-10, -5, 0, 1, 2, 3, 4, 5, 6, 7, 8, 10]
threshold_results = []

for threshold in sorted(thresholds):
    filtered = [d for d in matchup_data if d['lp_score'] > threshold]

    if not filtered:
        continue

    wins_above = sum(1 for d in filtered if d['result'])
    losses_above = sum(1 for d in filtered if not d['result'])
    win_rate = (wins_above / len(filtered) * 100) if filtered else 0

    threshold_results.append({
        'threshold': threshold,
        'picks': len(filtered),
        'wins': wins_above,
        'losses': losses_above,
        'win_rate': win_rate
    })

print(f"\n{'Threshold':<12} {'Picks':<10} {'Wins':<10} {'Losses':<10} {'Win Rate':<12}")
print("-" * 65)

for result in sorted(threshold_results, key=lambda x: x['threshold']):
    print(f"{result['threshold']:>10.0f} {result['picks']:<10} {result['wins']:<10} {result['losses']:<10} {result['win_rate']:<11.1f}%")

# Find best thresholds
by_winrate = sorted(threshold_results, key=lambda x: x['win_rate'], reverse=True)

print(f"\nTOP 10 THRESHOLDS BY WIN RATE:")
for i, result in enumerate(by_winrate[:10], 1):
    print(f"  {i}. Threshold {result['threshold']:>3.0f}: {result['win_rate']:>5.1f}% WR ({result['picks']} picks, {result['wins']}W-{result['losses']}L)")

# ============================================================
# ANALYSIS 3: Recommendations
# ============================================================
print("\n" + "=" * 100)
print("RECOMMENDED THRESHOLDS")
print("=" * 100)

conservative = by_winrate[0]
moderate = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.30 and r['picks'] <= len(matchup_data) * 0.50]
moderate = moderate[0] if moderate else by_winrate[len(by_winrate)//2]
aggressive = by_winrate[-1]

print(f"\n[CONSERVATIVE] High Quality, Lower Volume:")
print(f"   Threshold: {conservative['threshold']:.0f}")
print(f"   Win Rate: {conservative['win_rate']:.1f}%")
print(f"   Volume: {conservative['picks']} picks ({conservative['picks']/len(matchup_data)*100:.1f}%)")

print(f"\n[MODERATE] Balanced Approach:")
print(f"   Threshold: {moderate['threshold']:.0f}")
print(f"   Win Rate: {moderate['win_rate']:.1f}%")
print(f"   Volume: {moderate['picks']} picks ({moderate['picks']/len(matchup_data)*100:.1f}%)")

print(f"\n[AGGRESSIVE] Maximum Volume:")
print(f"   Threshold: {aggressive['threshold']:.0f}")
print(f"   Win Rate: {aggressive['win_rate']:.1f}%")
print(f"   Volume: {aggressive['picks']} picks ({aggressive['picks']/len(matchup_data)*100:.1f}%)")
