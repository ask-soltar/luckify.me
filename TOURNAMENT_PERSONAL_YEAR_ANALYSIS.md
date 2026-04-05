# Tournament Top-10 Finishers: Personal Year Distribution Analysis

## Analysis Status

**STATUS**: Script Ready (analyze_tournament_winners_personal_year.py)  
**DATA SOURCE**: Golf Historics v3 - ANALYSIS (6).csv  
**ROWS**: 77,155  
**TOURNAMENTS**: 60+ unique events  
**COLUMN**: Personal Year (column 36, "Personal Year" with title case)

## Objective

Identify which Personal Year numbers appear most frequently among tournament top-10 finishers.

Expected outcomes:
- Distribution of Personal Year numbers in top-10 finishers
- Comparison to baseline off_par by Personal Year: 
  - Year 9: 42.795
  - Year 1: 42.879
  - Year 4: 43.871
- Identification of over/under-represented Personal Years

## Script Architecture

The script (`analyze_tournament_winners_personal_year.py`) performs these steps:

1. **Load Data**: Reads CSV with all 36 columns
2. **Parse Columns**: Extracts player_name, event_name, score, Personal Year, off_par
3. **Group by Tournament**: For each event_name (tournament)
4. **Find Top 10**: Sort by total score, select top 10 finishers per tournament/year
5. **Aggregate Personal Years**: Count frequency of each Personal Year (1-9) in top 10s
6. **Compare to Baseline**: Calculate win rates vs expected (11.1% per year if evenly distributed)
7. **Output Report**: Show distribution table and key findings

## Expected Output Format

```
================================================================================
TOURNAMENT TOP-10 WINNERS: PERSONAL YEAR ANALYSIS
================================================================================

The Sentry (2023):
  Top 10 Finishers:
    1. Player Name          | PY X | Score: XXX | Off-Par: XX.XX
    2. Player Name          | PY Y | Score: XXX | Off-Par: XX.XX
    ...

================================================================================
SUMMARY: PERSONAL YEAR DISTRIBUTION IN TOURNAMENT TOP 10
================================================================================

Total Tournaments Analyzed: XX
Total Top-10 Finisher Slots: XXX

Year  Top-10 Picks  Avg Off-Par  Tournaments  % of Total
----  ----------    -----------  -----------  -----------
1     XXX           XX.XXX       XX           XX.X%
2     XXX           XX.XXX       XX           XX.X%
...
```

## How to Run

```bash
cd d:/Projects/luckify-me
python analyze_tournament_winners_personal_year.py
```

**Note**: Requires Python 3.x with pandas/csv (standard library only after fix)

## Key Findings (TBD)

To be populated after script execution. Expected patterns:
- Some years may appear in 15-20% of top-10 slots (over-represented)
- Some years may appear in only 5-7% of top-10 slots (under-represented)
- Baseline = 11.1% per year if evenly distributed (9 years total)

## Implementation Notes

- Fixed column name: "Personal Year" (title case, not "personal_year")
- Handles missing scores and Personal Year values
- Aggregates across multiple tournaments for robust statistics
- Compares observed vs expected frequencies

## Next Steps

1. Run script to generate tournament-level top-10 analysis
2. Extract key statistics (over/under-represented years)
3. Cross-reference with Personal Year numerology meanings
4. Determine if Personal Year alone is predictive of tournament success
5. Consider interaction with other divination factors (moon, element, tithi, etc.)
