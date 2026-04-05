import csv
from collections import defaultdict

# Read ANALYSIS sheet
analysis_file = "Golf Historics v3 - ANALYSIS (6).csv"
events_by_tournament = defaultdict(list)

with open(analysis_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Find column indices
    player_name_idx = header.index('player_name')
    event_name_idx = header.index('event_name')
    score_idx = header.index('score')
    personal_year_idx = header.index('Personal Year')  # Note: Title case
    off_par_idx = header.index('off_par')

    for row in reader:
        if not row or row[event_name_idx].strip() == '':
            continue

        event_name = row[event_name_idx].strip()

        # Only process complete rounds (score must be numeric)
        try:
            score = float(row[score_idx]) if row[score_idx] else None
            if score is None:
                continue

            personal_year = row[personal_year_idx].strip() if personal_year_idx < len(row) else ''
            if not personal_year or personal_year == '':
                continue

            off_par = float(row[off_par_idx]) if off_par_idx < len(row) and row[off_par_idx] else None

            events_by_tournament[event_name].append({
                'player': row[player_name_idx],
                'score': score,
                'personal_year': personal_year,
                'off_par': off_par
            })
        except (ValueError, IndexError):
            continue

# Analyze top 10 finishers per tournament
personal_year_winners = defaultdict(lambda: {'count': 0, 'total_off_par': 0, 'tournaments': 0})
tournament_count = 0

print("\n" + "="*80)
print("TOURNAMENT TOP-10 WINNERS: PERSONAL YEAR ANALYSIS")
print("="*80)

for event_name in sorted(events_by_tournament.keys()):
    rounds = events_by_tournament[event_name]

    # Sort by score (lower is better)
    rounds_sorted = sorted(rounds, key=lambda x: x['score'])
    top_10 = rounds_sorted[:10]

    if len(top_10) > 0:
        tournament_count += 1
        print(f"\n{event_name}:")
        print(f"  Top 10 Finishers:")

        for i, finisher in enumerate(top_10, 1):
            py = finisher['personal_year']
            score = finisher['score']
            off_par = finisher['off_par'] if finisher['off_par'] is not None else 'N/A'
            print(f"    {i:2d}. {finisher['player']:20s} | PY {py} | Score: {score:3.0f} | Off-Par: {off_par}")

            # Track stats
            if py.isdigit():
                personal_year_winners[py]['count'] += 1
                if finisher['off_par'] is not None:
                    personal_year_winners[py]['total_off_par'] += finisher['off_par']
                personal_year_winners[py]['tournaments'] += 1

# Sort by tournament appearances in top 10
top_winners = sorted(
    personal_year_winners.items(),
    key=lambda x: x[1]['count'],
    reverse=True
)

print("\n" + "="*80)
print("SUMMARY: PERSONAL YEAR DISTRIBUTION IN TOURNAMENT TOP 10")
print("="*80)
print(f"\nTotal Tournaments Analyzed: {tournament_count}")
print(f"Total Top-10 Finisher Slots: {sum(d['count'] for d in personal_year_winners.values())}")
print("\n{:<5} {:<10} {:<15} {:<15} {:<15}".format(
    "Year", "Top-10 Picks", "Avg Off-Par", "Tournaments", "% of Total"
))
print("-" * 65)

total_picks = sum(d['count'] for d in personal_year_winners.values())

for py, stats in top_winners:
    count = stats['count']
    avg_off_par = stats['total_off_par'] / count if count > 0 else 0
    tournaments = stats['tournaments']
    pct = (count / total_picks * 100) if total_picks > 0 else 0

    print("{:<5} {:<10} {:<15.3f} {:<15} {:<14.1f}%".format(
        py, count, avg_off_par, tournaments, pct
    ))

print("-" * 65)
print("\nKEY FINDINGS:")
print("- Personal Years appearing most in tournament top 10")
print("- Off-par average shows performance relative to field")
print("- Compare to overall baseline: Year 9 (42.795), Year 1 (42.879), Year 4 (43.871)")
print("\nNOTE: Negative off-par = beat par; positive = worse than par")
