# Player Screener - Input Format Guide

## Format 1: SINGLE PLAYER SCORES

Copy this template, fill in your data, save as `players.csv`:

```csv
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
Player Name,Calm,Open,Yellow,Earth,50,50,Rat
```

### Full Example (Copy & Paste Ready):

```csv
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
Rory McIlroy,Calm,Open,Yellow,Earth,75,75,Snake
Jon Rahm,Calm,Closing,Blue,Fire,50,50,Dog
Scottie Scheffler,Calm,Closing,Purple,Water,75,50,Tiger
Max Homa,Calm,Closing,Yellow,Metal,50,50,Snake
```

Then run:
```bash
python player_screener.py players.csv
```

**Output:**
```
Scottie Scheffler     57.1%
Jon Rahm              49.3%
Rory McIlroy          49.6%
Max Homa              45.8%

2-BALL MATCHUPS:
Scottie vs Jon Rahm   +7.8pp differential
```

---

## Format 2: 2-BALL MATCHUP SCORING

For head-to-head matchups, you need BOTH players' data in the same file:

### Template (2-Ball Format):

```csv
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac,matchup_id
Player A,Calm,Open,Yellow,Earth,75,75,Snake,1
Player B,Calm,Open,Blue,Fire,50,50,Dog,1
Player C,Calm,Closing,Purple,Water,75,50,Tiger,2
Player D,Calm,Closing,Yellow,Metal,50,50,Snake,2
```

The `matchup_id` groups players into 2-ball pairings (both players with id=1, both with id=2, etc.)

### Real Example:

```csv
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac,matchup_id
Rory McIlroy,Calm,Open,Yellow,Earth,75,75,Snake,1
Jon Rahm,Calm,Open,Blue,Fire,50,50,Dog,1
Scottie Scheffler,Calm,Closing,Purple,Water,75,50,Tiger,2
Max Homa,Calm,Closing,Yellow,Metal,50,50,Snake,2
Tiger Woods,Calm,Survival,Purple,Fire,50,25,Monkey,3
Collin Morikawa,Calm,Survival,Green,Wood,50,50,Rat,3
```

**This creates 3 matchups:**
- Matchup 1: Rory vs Jon
- Matchup 2: Scottie vs Max
- Matchup 3: Tiger vs Collin

**Output:**
```
MATCHUP 1: Rory McIlroy (49.6%) vs Jon Rahm (49.3%)
  Differential: +0.3pp (LOW confidence)
  No specialization bonuses

MATCHUP 2: Scottie Scheffler (57.1%) vs Max Homa (45.8%)
  Differential: +11.3pp (HIGH confidence)
  Scottie has specialization bonus

MATCHUP 3: Tiger Woods (37.6%) vs Collin Morikawa (52.2%)
  Differential: +14.6pp (HIGH confidence)
```

---

## Valid Values Reference

### condition
- `Calm`
- `Moderate`
- `Tough`

### round_type
- `Open`
- `Survival`
- `Positioning`
- `Closing`

### color
- `Red`
- `Blue`
- `Green`
- `Yellow`
- `Purple`
- `Orange`

### element
- `Fire`
- `Earth`
- `Wood`
- `Metal`
- `Water`

### exec_bucket & upside_bucket
Valid: `0`, `25`, `50`, `75`
(If you input 12, it auto-rounds to nearest: 0)

### chinese_zodiac
- `Rat`
- `Ox`
- `Tiger`
- `Rabbit`
- `Dragon`
- `Snake`
- `Horse`
- `Goat`
- `Monkey`
- `Rooster`
- `Dog`
- `Pig`

---

## Quick Paste Templates

### Template A: Single Player
```
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
```

### Template B: 3 Players (Screen All)
```
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
Player 1,Calm,Open,Yellow,Earth,50,50,Rat
Player 2,Calm,Closing,Blue,Fire,50,50,Dog
Player 3,Calm,Positioning,Green,Metal,75,75,Snake
```

### Template C: 2-Ball Matchup
```
name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac,matchup_id
Player A,Calm,Open,Yellow,Earth,75,75,Snake,1
Player B,Calm,Open,Blue,Fire,50,50,Dog,1
```

---

## How to Submit to Me

Just paste the CSV data in the format above, and say:
- **"Score these 3 players"** → I'll run single screener
- **"Score these 2-ball matchups"** → I'll parse matchup_id and give differentials

Example:
```
Score these players:

name,condition,round_type,color,element,exec_bucket,upside_bucket,chinese_zodiac
Rory McIlroy,Calm,Open,Yellow,Earth,75,75,Snake
Jon Rahm,Calm,Open,Blue,Fire,50,50,Dog
```

I'll respond with:
```
RESULTS:
Rory McIlroy    49.6%
Jon Rahm        49.3%

MATCHUP: Rory vs Jon = +0.3pp (LOW)
```
