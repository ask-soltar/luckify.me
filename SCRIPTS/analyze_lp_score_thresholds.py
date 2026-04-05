import csv
from collections import defaultdict
import statistics

# Read 2BMatchup file
matchup_file = "Golf Historics v3 - 2BMatchup (5).csv"

# Store data
matchup_data = []

with open(matchup_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    lp_score_idx = None
    lp_pick_idx = None
    wl_idx = None

    # Try to find columns (headers may vary)
    for i, col_name in enumerate(header):
        if 'LP SCore' in col_name or 'LP Score' in col_name:
            lp_score_idx = i
        elif col_name.strip() == 'LP Pick':
            lp_pick_idx = i
        elif col_name.strip() == 'W/L':
            wl_idx = i

    # If not found, search more broadly
    if lp_score_idx is None:
        for i, col_name in enumerate(header):
            if 'score' in col_name.lower() and 'lp' in col_name.lower():
                lp_score_idx = i
                break

    if wl_idx is None:
        for i, col_name in enumerate(header):
            if col_name.strip() in ['W/L', 'WL', 'Result']:
                wl_idx = i
                break

    print(f"DEBUG: Found columns:")
    print(f"  LP Score at index: {lp_score_idx}")
    print(f"  LP Pick at index: {lp_pick_idx}")
    print(f"  W/L at index: {wl_idx}")
    print(f"  Header length: {len(header)}")
    if lp_score_idx is not None:
        print(f"  LP Score header: '{header[lp_score_idx]}'")
    if wl_idx is not None:
        print(f"  W/L header: '{header[wl_idx]}'")

    for row in reader:
        if not row or len(row) < max(lp_score_idx + 1, wl_idx + 1):
            continue

        try:
            # Get LP Score
            lp_score_str = row[lp_score_idx].strip() if lp_score_idx < len(row) else ''
            if not lp_score_str or lp_score_str == '' or lp_score_str == '#REF!':
                continue

            lp_score = float(lp_score_str)

            # Get W/L result
            wl = row[wl_idx].strip() if wl_idx < len(row) else ''

            # Determine if win or loss
            is_win = None
            if '✅' in wl or 'Win' in wl or wl.upper() == 'WIN':
                is_win = True
            elif '❌' in wl or 'Lose' in wl or wl.upper() == 'LOSE' or wl.upper() == 'LOSS':
                is_win = False

            if is_win is None:
                continue

            matchup_data.append({
                'lp_score': lp_score,
                'result': is_win
            })

        except (ValueError, IndexError) as e:
            continue

print(f"\nTotal records parsed: {len(matchup_data)}")

if not matchup_data:
    print("ERROR: No data found! Check column indices.")
    exit(1)

# ============================================================
# ANALYSIS 1: Distribution of LP Scores
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 1: LP SCORE DISTRIBUTION")
print("="*100)

lp_scores = [d['lp_score'] for d in matchup_data]
wins = [d['lp_score'] for d in matchup_data if d['result']]
losses = [d['lp_score'] for d in matchup_data if not d['result']]

print(f"\nOverall LP Score Stats:")
print(f"  Total picks: {len(matchup_data)}")
print(f"  Wins: {len(wins)} ({len(wins)/len(matchup_data)*100:.1f}%)")
print(f"  Losses: {len(losses)} ({len(losses)/len(matchup_data)*100:.1f}%)")
print(f"  Overall win rate: {len(wins)/len(matchup_data)*100:.1f}%")

print(f"\nLP Score Statistics:")
print(f"  Min: {min(lp_scores):.2f}")
print(f"  Max: {max(lp_scores):.2f}")
print(f"  Mean: {statistics.mean(lp_scores):.2f}")
print(f"  Median: {statistics.median(lp_scores):.2f}")
print(f"  Stdev: {statistics.stdev(lp_scores) if len(lp_scores) > 1 else 0:.2f}")

print(f"\nWin LP Scores (when picks won):")
print(f"  Mean: {statistics.mean(wins) if wins else 0:.2f}")
print(f"  Median: {statistics.median(wins) if wins else 0:.2f}")

print(f"\nLoss LP Scores (when picks lost):")
print(f"  Mean: {statistics.mean(losses) if losses else 0:.2f}")
print(f"  Median: {statistics.median(losses) if losses else 0:.2f}")

# ============================================================
# ANALYSIS 2: Threshold Analysis
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 2: THRESHOLD FILTERING (Test Different Cutoff Scores)")
print("="*100)

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

print(f"\n{'TOP 10 THRESHOLDS BY WIN RATE:':<50}")
for i, result in enumerate(by_winrate[:10], 1):
    print(f"  {i}. Threshold {result['threshold']:>3.0f}: {result['win_rate']:>5.1f}% WR ({result['picks']} picks, {result['wins']}W-{result['losses']}L)")

# ============================================================
# ANALYSIS 3: Volume vs Quality Trade-off
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 3: VOLUME vs QUALITY TRADE-OFF")
print("="*100)

print(f"\n{'Threshold':<12} {'Volume':<10} {'Win Rate':<12} {'Expected Wins/100':<20} {'Quality Grade':<15}")
print("-" * 80)

for result in sorted(threshold_results, key=lambda x: x['threshold']):
    volume_pct = (result['picks'] / len(matchup_data) * 100)
    expected = result['win_rate']

    if expected >= 58:
        grade = "A+ (Excellent)"
    elif expected >= 55:
        grade = "A (Very Good)"
    elif expected >= 52:
        grade = "B (Good)"
    elif expected >= 50:
        grade = "C (Okay)"
    else:
        grade = "D (Poor)"

    print(f"{result['threshold']:>10.0f} {volume_pct:>8.1f}% {result['win_rate']:>11.1f}% {expected:>18.1f} {grade:<15}")

# ============================================================
# ANALYSIS 4: Recommended Thresholds
# ============================================================
print("\n" + "="*100)
print("ANALYSIS 4: RECOMMENDED FILTERING THRESHOLDS")
print("="*100)

print(f"\nBased on your data, here are the recommended thresholds:\n")

# Conservative: High quality, lower volume
conservative = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.05][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.05) else by_winrate[0]
print(f"[CONSERVATIVE] High Quality, Lower Volume:")
print(f"   Threshold: {conservative['threshold']:.0f}")
print(f"   Win Rate: {conservative['win_rate']:.1f}%")
print(f"   Volume: {conservative['picks']} picks ({conservative['picks']/len(matchup_data)*100:.1f}% of total)")
print(f"   Rating: Accept only top-tier signals")

# Moderate: Balanced
moderate = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.20 and r['picks'] <= len(matchup_data) * 0.40][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.20) else by_winrate[5]
print(f"\n[MODERATE] Balanced Approach:")
print(f"   Threshold: {moderate['threshold']:.0f}")
print(f"   Win Rate: {moderate['win_rate']:.1f}%")
print(f"   Volume: {moderate['picks']} picks ({moderate['picks']/len(matchup_data)*100:.1f}% of total)")
print(f"   Rating: Good balance of quality and volume")

# Aggressive: Higher volume, accept slightly lower WR
aggressive = [r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.50][0] if any(r for r in by_winrate if r['picks'] >= len(matchup_data) * 0.50) else by_winrate[-1]
print(f"\n[AGGRESSIVE] Higher Volume, Lower Threshold:")
print(f"   Threshold: {aggressive['threshold']:.0f}")
print(f"   Win Rate: {aggressive['win_rate']:.1f}%")
print(f"   Volume: {aggressive['picks']} picks ({aggressive['picks']/len(matchup_data)*100:.1f}% of total)")
print(f"   Rating: Maximum picks, accept lower win rate")

print("\n" + "="*100)
print("RECOMMENDATION:")
print("="*100)
print(f"\nStart with the MODERATE threshold ({moderate['threshold']:.0f}) for filtering BB (unfiltered picks).")
print(f"This will give you ~{moderate['picks']} picks with a {moderate['win_rate']:.1f}% win rate.")
print(f"\nAdjust based on your risk tolerance:")
print(f"  - Want higher quality? Use CONSERVATIVE threshold ({conservative['threshold']:.0f})")
print(f"  - Want more volume? Use AGGRESSIVE threshold ({aggressive['threshold']:.0f})")
