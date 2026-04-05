import csv
from collections import defaultdict
import statistics

matchup_file = "Golf Historics v3 - 2BMatchup (7).csv"

matchup_data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    lp_score_idx = 52   # LP SCore
    lp_pick_idx = 53    # LP Pick
    wl_lp_idx = 54      # W/L [LP]

    print(f"Columns:")
    print(f"  {lp_score_idx}: {header[lp_score_idx]}")
    print(f"  {lp_pick_idx}: {header[lp_pick_idx]}")
    print(f"  {wl_lp_idx}: {header[wl_lp_idx]}\n")

    for row in reader:
        if not row or len(row) < wl_lp_idx + 1:
            continue

        try:
            # Get LP Score
            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str in ['', '#REF!']:
                continue

            lp_score = float(lp_score_str)

            # Get LP Pick
            lp_pick = row[lp_pick_idx].strip() if lp_pick_idx < len(row) else ''
            if not lp_pick:
                continue

            # Get W/L result
            wl = row[wl_lp_idx].strip() if wl_lp_idx < len(row) else ''

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
                'pick': lp_pick,
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
print("LP SCORE THRESHOLD ANALYSIS")
print("=" * 100)

lp_scores = [d['lp_score'] for d in matchup_data]
wins = [d for d in matchup_data if d['result']]
losses = [d for d in matchup_data if not d['result']]

print(f"\nOverall Stats:")
print(f"  Total picks: {len(matchup_data)}")
print(f"  Wins: {len(wins)} ({len(wins)/len(matchup_data)*100:.1f}%)")
print(f"  Losses: {len(losses)} ({len(losses)/len(matchup_data)*100:.1f}%)")
print(f"  Overall win rate: {len(wins)/len(matchup_data)*100:.1f}%")

print(f"\nLP Score Statistics:")
print(f"  Min: {min(lp_scores):.2f}")
print(f"  Max: {max(lp_scores):.2f}")
print(f"  Mean: {statistics.mean(lp_scores):.2f}")
print(f"  Median: {statistics.median(lp_scores):.2f}")
print(f"  Stdev: {statistics.stdev(lp_scores):.2f}")

# ============================================================
# ANALYSIS 2: Threshold Analysis
# ============================================================
print("\n" + "=" * 100)
print("THRESHOLD FILTERING (Test Different Cutoff Scores)")
print("=" * 100)

thresholds = list(range(-10, 12))
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

print(f"\nTOP 15 THRESHOLDS BY WIN RATE:")
for i, result in enumerate(by_winrate[:15], 1):
    print(f"  {i:2d}. Threshold {result['threshold']:>3.0f}: {result['win_rate']:>5.1f}% WR ({result['picks']:3d} picks, {result['wins']:2d}W-{result['losses']:2d}L)")

# ============================================================
# ANALYSIS 3: Volume vs Quality
# ============================================================
print("\n" + "=" * 100)
print("VOLUME vs QUALITY TRADE-OFF")
print("=" * 100)

print(f"\n{'Threshold':<12} {'Volume':<10} {'Win Rate':<12} {'Grade':<15}")
print("-" * 60)

for result in sorted(threshold_results, key=lambda x: x['threshold']):
    volume_pct = (result['picks'] / len(matchup_data) * 100)
    wr = result['win_rate']

    if wr >= 65:
        grade = "A+ (Excellent)"
    elif wr >= 60:
        grade = "A (Very Good)"
    elif wr >= 55:
        grade = "B (Good)"
    else:
        grade = "C (Okay)"

    print(f"{result['threshold']:>10.0f} {volume_pct:>8.1f}% {wr:>11.1f}% {grade:<15}")

# ============================================================
# ANALYSIS 4: Recommendations
# ============================================================
print("\n" + "=" * 100)
print("RECOMMENDED FILTERING THRESHOLDS")
print("=" * 100)

conservative = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.05][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.05) else by_winrate[0]
moderate = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.25 and r['picks'] <= len(matchup_data) * 0.45][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.25) else by_winrate[len(by_winrate)//2]
aggressive = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.60][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.60) else by_winrate[-1]

print(f"\n[CONSERVATIVE] High Quality, Lower Volume:")
print(f"   Threshold: {conservative['threshold']:.0f}")
print(f"   Win Rate: {conservative['win_rate']:.1f}%")
print(f"   Volume: {conservative['picks']} picks ({conservative['picks']/len(matchup_data)*100:.1f}%)")
print(f"   - Accept only top-tier signals")

print(f"\n[MODERATE] Balanced Approach:")
print(f"   Threshold: {moderate['threshold']:.0f}")
print(f"   Win Rate: {moderate['win_rate']:.1f}%")
print(f"   Volume: {moderate['picks']} picks ({moderate['picks']/len(matchup_data)*100:.1f}%)")
print(f"   - Good balance of quality and volume")

print(f"\n[AGGRESSIVE] Maximum Volume:")
print(f"   Threshold: {aggressive['threshold']:.0f}")
print(f"   Win Rate: {aggressive['win_rate']:.1f}%")
print(f"   Volume: {aggressive['picks']} picks ({aggressive['picks']/len(matchup_data)*100:.1f}%)")
print(f"   - Maximum picks, slight quality trade-off")

print("\n" + "=" * 100)
print("RECOMMENDATION:")
print("=" * 100)
print(f"\nStart with MODERATE threshold ({moderate['threshold']:.0f}) -- ~{moderate['picks']} picks at {moderate['win_rate']:.1f}% WR")
print(f"Adjust based on your risk tolerance:")
print(f"  - Higher quality: Use CONSERVATIVE ({conservative['threshold']:.0f})")
print(f"  - More volume: Use AGGRESSIVE ({aggressive['threshold']:.0f})")
