import csv
from datetime import datetime
from collections import defaultdict
import statistics

def reduce_with_master(num):
    """Reduce to single digit or preserve master numbers 11, 22, 33"""
    if num <= 0:
        return None
    if num in [11, 22, 33]:
        return num
    while num > 9:
        if num in [11, 22, 33]:
            return num
        num = sum(int(d) for d in str(num))
    return num

# ============================================================================
# Read PLAYERS for birth data
# ============================================================================
players_birth = {}
with open("Golf Historics v3 - Golf_Analytics.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        player = row[2].strip() if len(row) > 2 else ''
        birth = row[10].strip() if len(row) > 10 else ''
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

print(f"Loaded {len(players_birth)} players\n")

# ============================================================================
# Read ANALYSIS sheet for adjusted historical par (AG column)
# ============================================================================
analysis_adj_his_par = defaultdict(list)  # player -> list of adj_his_par values

with open("ANALYSIS_v3_export.csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        if not row or len(row) < 33:
            continue
        try:
            player_name = row[1].strip() if len(row) > 1 else ''
            adj_his_par_str = row[32].strip() if len(row) > 32 else ''

            if player_name and adj_his_par_str and adj_his_par_str not in ['', '#REF!']:
                try:
                    adj_his_par = float(adj_his_par_str)
                    analysis_adj_his_par[player_name].append(adj_his_par)
                except:
                    pass
        except (ValueError, IndexError):
            continue

print(f"Loaded adj_his_par data for {len(analysis_adj_his_par)} players from ANALYSIS sheet\n")

# ============================================================================
# Read 2BMatchup sheet and filter for PD22
# ============================================================================
matchup_data = []

with open("Golf Historics v3 - 2BMatchup (6).csv", 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    try:
        player_a_idx = header.index("Player A")
        player_b_idx = header.index("Player B")
        event_date_idx = header.index("Event Date")

        # Use verified columns from actual sheet structure
        # Column 22 (index 21) = "Winner" (contains winner name or "Push")
        # Column 30 (index 29) = "Score [A]" (Player A's round score)
        winner_idx = 21  # Column 22 - Winner
        score_a_idx = 29  # Column 30 - Score [A]

        for row in reader:
            if not row or len(row) < 55:
                continue

            try:
                player_a = row[player_a_idx].strip()
                player_b = row[player_b_idx].strip()
                event_date_str = row[event_date_idx].strip()

                if not player_a or not player_b or not event_date_str:
                    continue
                if player_a not in players_birth or player_b not in players_birth:
                    continue

                event_date = datetime.strptime(event_date_str, '%m/%d/%Y')
                event_year = event_date.year
                event_month = event_date.month
                event_day = event_date.day

                # Calculate Personal Days (both players)
                py_a = reduce_with_master(
                    players_birth[player_a]['month'] +
                    players_birth[player_a]['day'] +
                    event_year
                )
                py_b = reduce_with_master(
                    players_birth[player_b]['month'] +
                    players_birth[player_b]['day'] +
                    event_year
                )

                pd_a = reduce_with_master(event_month + event_day + py_a) if py_a else None
                pd_b = reduce_with_master(event_month + event_day + py_b) if py_b else None

                # Get score and winner result
                try:
                    score_a_val = float(row[score_a_idx]) if score_a_idx < len(row) and row[score_a_idx].strip() else None
                    winner = row[winner_idx].strip() if winner_idx < len(row) else ''

                    # Determine outcome for Player A
                    if winner == "Push":
                        outcome = "Push"
                    elif winner == player_a:
                        outcome = "Win"
                    elif winner == player_b:
                        outcome = "Lose"
                    else:
                        outcome = ""  # Unknown
                except:
                    continue

                # Only include if either player has PD22
                if (pd_a == 22 or pd_b == 22) and outcome:  # Only include if we have an outcome
                    matchup_data.append({
                        'player_a': player_a,
                        'player_b': player_b,
                        'pd_a': pd_a,
                        'pd_b': pd_b,
                        'score_a': score_a_val,
                        'outcome': outcome,  # Win/Lose/Push for Player A
                        'date': event_date_str,
                        'winner': winner,
                    })

            except (ValueError, IndexError):
                continue

    except ValueError as e:
        print(f"ERROR finding columns: {e}")
        print(f"Available columns: {header}")

print(f"Found {len(matchup_data)} matchups with PD22\n")

# ============================================================================
# Analyze by player
# ============================================================================
player_stats = defaultdict(lambda: {
    'matchups': [],
    'wins': 0,
    'losses': 0,
    'push': 0,
    'scores': [],
    'adj_his_par': []
})

for matchup in matchup_data:
    player_a = matchup['player_a']
    player_b = matchup['player_b']

    # If player A has PD22
    if matchup['pd_a'] == 22:
        player_stats[player_a]['matchups'].append(matchup)
        if matchup['score_a'] is not None:
            player_stats[player_a]['scores'].append(matchup['score_a'])

        if matchup['outcome'] == 'Win':
            player_stats[player_a]['wins'] += 1
        elif matchup['outcome'] == 'Lose':
            player_stats[player_a]['losses'] += 1
        elif matchup['outcome'] == 'Push':
            player_stats[player_a]['push'] += 1

    # If player B has PD22 (outcome is from A's perspective, so we reverse)
    if matchup['pd_b'] == 22:
        player_stats[player_b]['matchups'].append(matchup)
        if matchup['score_a'] is not None:
            # For player B, we'd need player B's score, but we only have A's score
            # Skip adding score for player B for now
            pass

        if matchup['outcome'] == 'Win':
            player_stats[player_b]['losses'] += 1  # Reversed: A wins = B loses
        elif matchup['outcome'] == 'Lose':
            player_stats[player_b]['wins'] += 1    # Reversed: A loses = B wins
        elif matchup['outcome'] == 'Push':
            player_stats[player_b]['push'] += 1

# Add adj_his_par data
for player, stats in player_stats.items():
    if player in analysis_adj_his_par:
        stats['adj_his_par'] = analysis_adj_his_par[player]

# ============================================================================
# Report: PD22 PLAYERS - PROFITABILITY & CONSISTENCY
# ============================================================================
print("=" * 140)
print("MASTER NUMBER 22 (Personal Day) — PROFITABILITY & CONSISTENCY ANALYSIS")
print("=" * 140)
print()

sorted_players = sorted(player_stats.items(),
                       key=lambda x: len(x[1]['matchups']),
                       reverse=True)

print(f"{'Player':<25} {'Matchups':<10} {'Wins':<6} {'Losses':<6} {'Push':<6} {'WR%':<8} {'Avg Score':<12} {'Consistency':<15} {'Adj His Par':<15} {'Consistency Metric':<20}")
print("-" * 140)

for player, stats in sorted_players:
    n = len(stats['matchups'])
    if n < 3:
        continue

    wins = stats['wins']
    losses = stats['losses']
    pushes = stats['push']

    # Profitability: Win Rate
    win_rate = (wins / (wins + losses)) * 100 if (wins + losses) > 0 else 0

    # Average Score
    avg_score = sum(stats['scores']) / len(stats['scores']) if stats['scores'] else None
    avg_score_str = f"{avg_score:+.2f}" if avg_score is not None else "N/A"

    # Consistency: Adjusted Historical Par
    adj_his_par_vals = stats['adj_his_par']
    if adj_his_par_vals:
        adj_his_par_mean = statistics.mean(adj_his_par_vals)
        adj_his_par_stdev = statistics.stdev(adj_his_par_vals) if len(adj_his_par_vals) > 1 else 0
        consistency_str = f"{adj_his_par_mean:+.2f} ±{adj_his_par_stdev:.2f}"
        # Lower std dev = more consistent
        consistency_metric = adj_his_par_stdev
    else:
        consistency_str = "N/A"
        consistency_metric = None

    consistency_metric_str = f"{consistency_metric:.2f}" if consistency_metric is not None else "N/A"

    print(f"{player:<25} {n:<10} {wins:<6} {losses:<6} {pushes:<6} {win_rate:<7.1f}% {avg_score_str:<12} {consistency_str:<15} {adj_his_par_mean:+.2f}      {consistency_metric_str:<20}")

# ============================================================================
# Summary Statistics
# ============================================================================
print("\n" + "=" * 140)
print("SUMMARY STATISTICS")
print("=" * 140)

total_players = len([p for p, s in player_stats.items() if len(s['matchups']) >= 3])
total_matchups = sum(len(s['matchups']) for s in player_stats.values())
total_wins = sum(s['wins'] for s in player_stats.values())
total_losses = sum(s['losses'] for s in player_stats.values())
overall_wr = (total_wins / (total_wins + total_losses)) * 100 if (total_wins + total_losses) > 0 else 0

print(f"""
Total PD22 Players (3+ matchups):  {total_players}
Total PD22 Matchups:               {total_matchups}
Overall Win Rate (PD22):           {total_wins} wins, {total_losses} losses = {overall_wr:.1f}% WR

Most Consistent (Lowest Std Dev):  [Check table above]
Most Profitable (Highest WR):      [Check table above]
""")

# ============================================================================
# Findings
# ============================================================================
print("\n" + "=" * 140)
print("INTERPRETATION")
print("=" * 140)
print("""
PROFITABILITY METRICS:
- Win Rate % shows matchup-level edge for PD22 players
- Avg Score shows round-by-round performance vs baseline

CONSISTENCY METRICS (Adjusted Historical Par):
- Mean (Adj His Par): Average player historical par adjusted by tour condition
  - Positive = Player beats his historical average (good sign)
  - Negative = Player underperforms his historical average
- Std Dev (±): Variability in performance across rounds
  - Lower = More consistent (predictable, reliable)
  - Higher = More volatile (feast/famine, hard to model)

COMBINED SIGNAL:
- Players with HIGH win rate + LOW std dev = Best candidates (profitable + reliable)
- Players with HIGH win rate + HIGH std dev = Profitable but risky (volatile)
- Players with LOW win rate + LOW std dev = Consistent but wrong (lose reliably)
""")
