# Weekly Player Scoring Template

## How to Use the Player Scoring System

### Step 1: Determine Tournament Conditions
Before scoring, identify the expected tournament conditions:

```
Tournament: [Event Name]
Week: [Date]
Expected Condition: Calm / Moderate / Tough
Expected Round Types: Open / Survival / Positioning / Closing
Expected Color: Red / Blue / Green / Yellow / Purple / Orange
Expected Element: Fire / Earth / Wood / Metal / Water
```

### Step 2: Gather Player Data
For each player, you need:

| Field | Source | Values |
|-------|--------|--------|
| `name` | Player name | "Rory McIlroy" |
| `condition` | Tournament condition | Calm, Moderate, Tough |
| `round_type` | Round type | Open, Survival, Positioning, Closing |
| `color` | Feng shui color | Red, Blue, Green, Yellow, Purple, Orange |
| `element` | Wu Xing element | Fire, Earth, Wood, Metal, Water |
| `exec_bucket` | From Golf_Analytics | 0, 25, 50, 75 |
| `upside_bucket` | From Golf_Analytics | 0, 25, 50, 75 |
| `chinese_zodiac` | Birth year zodiac | Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig |

### Step 3: Run Scoring

**Option A: Python Script (Most Accurate)**
```python
from player_scoring_system import PlayerScorer

scorer = PlayerScorer()

players = [
    {
        'name': 'Rory McIlroy',
        'condition': 'Calm',
        'round_type': 'Positioning',
        'color': 'Green',
        'element': 'Metal',
        'exec_bucket': 75,
        'upside_bucket': 75,
        'chinese_zodiac': 'Rat',
    },
    # ... more players
]

# Score all players
tournament_scores = scorer.score_tournament(players)
print(tournament_scores)

# Get ranked 2-ball matchups
matchups = scorer.rank_matchups_2ball(players)
print(matchups.head(20))
```

**Option B: Manual Calculation**
1. For each player, look up (Condition, RoundType, Color, Element) in Element signals table
2. Get the win rate (e.g., 0.613 = 61.3% score)
3. Look up (Condition, RoundType, Exec, Upside, Zodiac) in Zodiac signals table
4. Get that win rate (e.g., 0.600 = 60.0% score)
5. Combined Score = (Element_Score × 0.6) + (Zodiac_Score × 0.4)
6. Convert to percentage (multiply by 100)

### Step 4: Identify Betting Opportunities

**For 2-Ball Matchups:**
```
Rank by Differential (larger = better):
+6.8 → Rory vs Jon Rahm (VERY CONFIDENT - only bet if <-110)
+4.8 → Rory vs Scottie (CONFIDENT - bet if <-115)
+3.0 → Rory vs Tiger (MODERATE - bet if <-120)
+1.5 → Tiger vs Max (WEAK - only bet if <-130)
+0.1 → Max vs Tiger (NO SIGNAL - pass)
```

**Betting Rules:**
- Only bet differentials > +2.5 points
- Larger differentials allow tighter odds (-110 vs -120)
- If BOTH players validate (overlap), increase confidence by 25%
- If NEITHER player validates, treat as neutral 50/50

**For Outrights:**
```
Rank by Combined Score:
56.8 → Rory (STRONG - overlay value)
53.8 → Max/Tiger (MEDIUM - fair value)
52.0 → Scottie (WEAK - avoid unless good odds)
50.0 → Jon Rahm (NEUTRAL - no edge)
```

### Step 5: Position Sizing

Use Kelly Criterion based on differential:

```
Differential | Confidence | Kelly % | Practical Sizing
    +6-7    |   Very High | 20-25%  | 25% of betting unit
    +4-5    |   High      | 15-20%  | 15-20% of betting unit
    +2-3    |   Medium    | 10-15%  | 10-15% of betting unit
    <+2     |   Low       | 0-5%    | Pass or tiny bet
```

---

## Validated Signal Tables

### Element Model Signals (60% weight)

Best combos (tested on 2025-2026 data):

| Condition | RoundType | Color | Element | Score |
|-----------|-----------|-------|---------|-------|
| Calm | Survival | Purple | Water | 61.5% |
| Calm | Positioning | Green | Metal | 61.3% |
| Calm | Closing | Blue | Fire | 58.1% |
| Calm | Closing | Yellow | Metal | 56.4% |
| Calm | Positioning | Green | Wood | 56.4% |
| Calm | Survival | Purple | Fire | 56.3% |
| Calm | Positioning | Purple | Wood | 56.0% |
| Calm | Closing | Green | Earth | 55.9% |

If combo not in table → use 50.0% (neutral)

### Zodiac Model Signals (40% weight)

Best combos (tested on 2025-2026 data):

| Condition | RoundType | Exec | Upside | Zodiac | Score |
|-----------|-----------|------|--------|--------|-------|
| Calm | Survival | 50 | 75 | Tiger | 65.3% |
| Calm | Open | 50 | 75 | Rat | 64.3% |
| Calm | Survival | 25 | 50 | Goat | 64.2% |
| Calm | Survival | 50 | 75 | Snake | 64.0% |
| Calm | REMOVE | 50 | 50 | Rabbit | 63.6% |
| Calm | Positioning | 50 | 50 | Rat | 63.5% |
| Calm | Open | 25 | 75 | Snake | 63.3% |
| Calm | Open | 25 | 50 | Rooster | 62.7% |

If combo not in table → use 50.0% (neutral)

---

## Example: PGA Championship Week

**Tournament:** PGA Championship
**Expected Conditions:** Calm (field is world-class, venue is tough but fair)
**Round Type by Round:**
- R1: Open (first round)
- R2: Survival (cut pressure)
- R3: Positioning (contention reshuffles)
- R4: Closing (final round drama)

**Player Data:**
```
Rory McIlroy (Born 1989-05-04 = Serpent/Snake in Chinese):
  - R3 Positioning: Color Green, Element Metal
  - Element: (Calm, Positioning, Green, Metal) = 61.3%
  - Zodiac: Exec75, Upside75, Snake = (Calm, Positioning, 75, 75, Snake) = NOT IN TABLE = 50%
  - Combined: (61.3 × 0.6) + (50.0 × 0.4) = 56.78%

Jon Rahm (Born 1994-11-21 = Dog):
  - R3 Positioning: Color Blue, Element Fire
  - Element: (Calm, Positioning, Blue, Fire) = NOT IN TABLE = 50%
  - Zodiac: Exec50, Upside50, Dog = (Calm, Positioning, 50, 50, Dog) = NOT IN TABLE = 50%
  - Combined: (50.0 × 0.6) + (50.0 × 0.4) = 50.00%

MATCHUP: Rory vs Jon (R3)
Differential: 56.78% - 50.00% = +6.78 points
Confidence: VERY HIGH (Rory validated by Element, Jon is neutral)
Betting Decision: BET RORY at -110 or better
```

---

## Weekly Workflow

**Monday:**
1. Identify tournament conditions and round types
2. Gather player field data (from Golf_Analytics)
3. Run scoring system for full field

**Tuesday-Wednesday:**
1. Review top differentials (>+3.0 points)
2. Check actual sportsbook odds
3. Place 2-ball bets on biggest differentials vs market
4. Track outright value (high scorers)

**Thursday-Sunday:**
1. Monitor 2-ball results daily
2. Adjust position sizing based on live performance
3. Compare predicted scores vs actual results
4. Update signal tables if patterns emerge

**Post-Tournament:**
1. Review which signals hit and which missed
2. Update confidence in Element/Zodiac models
3. Prepare for next tournament

---

## Tracking Template

Use this to track performance weekly:

```
Week of: [Date]
Tournament: [Name]
Condition: [Expected]

2-Ball Bets:
| Player 1 | Player 2 | Diff | Odds | Result | ROI |
|----------|----------|------|------|--------|-----|
| Rory     | Jon      | +6.8 | -110 | W      | +91 |
| Scottie  | Max      | +2.1 | -120 | L      | -120|
| ...      | ...      | ...  | ...  | ...    | ...  |

Win Rate: 2/3 = 66.7% ✓
ROI: +45 units ✓
Notes: Element signals hit harder than Zodiac this week
```

---

## Tips for Success

1. **Prioritize larger differentials** (+5+) = lower risk, higher confidence
2. **Look for overlaps** (both models validating same player) = bonus confidence
3. **Fade neutrals** (50% score) = no edge, pass the bet
4. **Track which models validate weekly** = refine weighting over time
5. **Compare to market** = only bet when your score gives real edge vs odds

---

## Data Sources Needed

To fully automate this system, you need:

- Tournament condition prediction (Calm/Moderate/Tough)
- Round type for each round
- Course color assignment (research from Golf_Analytics)
- Course element assignment (research from Golf_Analytics)
- Player Exec/Upside buckets (from Golf_Analytics columns)
- Player Chinese Zodiac (from birth date)

Once you have these, you can run the scoring system fully automated and bet the biggest differentials.

