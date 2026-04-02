# Player-Specific Layer Schema Design

## Overview

Three-tier schema to capture player statistics at increasing granularity:
1. **Tier 1:** Player baseline (career totals)
2. **Tier 2:** Player by single dimension (e.g., by condition, by color)
3. **Tier 3:** Player by combo dimensions (e.g., by condition×round_type, by color×element)

---

## TIER 1: Player Baseline Stats

**Table: `player_baseline`**

Stores career-level statistics for each player.

```sql
CREATE TABLE player_baseline (
  player_id INT PRIMARY KEY,
  player_name VARCHAR(255) UNIQUE,

  -- Career totals
  career_events INT,                    -- Total tournaments played
  career_avg_score FLOAT,               -- Average diff_course_avg
  career_median_score FLOAT,            -- Median diff_course_avg
  career_std_dev FLOAT,                 -- Std dev of scores

  -- Win rate metrics
  career_good_count INT,                -- Times diff <= -2.0
  career_bad_count INT,                 -- Times diff >= +2.0
  career_neutral_count INT,             -- Times -2.0 < diff < +2.0
  career_win_rate FLOAT,                -- good_count / career_events
  career_loss_rate FLOAT,               -- bad_count / career_events

  -- Consistency
  career_consistency FLOAT,             -- 1 - (std_dev / max_possible_range)

  -- Last updated
  updated_at TIMESTAMP,
  data_source VARCHAR(50)               -- "ANALYSIS_v2" or "live"
);
```

**Example:**
```
player_id: 1001
player_name: "Rory McIlroy"
career_events: 47
career_avg_score: 1.23
career_win_rate: 0.58
career_loss_rate: 0.24
career_consistency: 0.72
updated_at: 2026-03-28
```

---

## TIER 2: Player by Single Dimension

**Table: `player_by_condition`**

```sql
CREATE TABLE player_by_condition (
  player_id INT,
  condition VARCHAR(20),              -- "Calm", "Moderate", "Tough"

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, condition),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_round_type`**

```sql
CREATE TABLE player_by_round_type (
  player_id INT,
  round_type VARCHAR(20),            -- "Open", "Survival", "Positioning", "Closing"

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, round_type),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_color`**

```sql
CREATE TABLE player_by_color (
  player_id INT,
  color VARCHAR(20),                -- "Red", "Blue", "Green", "Yellow", "Purple", "Orange"

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, color),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_element`**

```sql
CREATE TABLE player_by_element (
  player_id INT,
  element VARCHAR(20),              -- "Fire", "Earth", "Wood", "Metal", "Water"

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, element),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_exec_upside`**

```sql
CREATE TABLE player_by_exec_upside (
  player_id INT,
  exec_bucket INT,                  -- 0, 25, 50, 75
  upside_bucket INT,                -- 0, 25, 50, 75

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, exec_bucket, upside_bucket),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_zodiac`**

```sql
CREATE TABLE player_by_zodiac (
  player_id INT,
  chinese_zodiac VARCHAR(20),       -- "Rat", "Ox", "Tiger", ..., "Pig"

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, chinese_zodiac),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Example (player_by_condition):**
```
player_id: 1001 (Rory)
condition: "Calm"
events: 28
avg_score: 2.14       -- Rory crushes Calm conditions
win_rate: 0.64        -- 64% win rate in Calm
good_count: 18
bad_count: 5
```

---

## TIER 3: Player by Composite Dimensions

**Table: `player_by_condition_roundtype`**

Most important combo table. Stores (Condition, RoundType) performance.

```sql
CREATE TABLE player_by_condition_roundtype (
  player_id INT,
  condition VARCHAR(20),
  round_type VARCHAR(20),

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, condition, round_type),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Example:**
```
player_id: 1001 (Rory)
condition: "Calm"
round_type: "Positioning"
events: 8
avg_score: 3.21       -- Very strong in this combo
win_rate: 0.75        -- 75% win rate
good_count: 6
bad_count: 1
```

**Table: `player_by_color_element`**

Stores (Color, Element) performance for environmental combo analysis.

```sql
CREATE TABLE player_by_color_element (
  player_id INT,
  color VARCHAR(20),
  element VARCHAR(20),

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, color, element),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Table: `player_by_exec_upside_zodiac`** (Optional, sparse)

```sql
CREATE TABLE player_by_exec_upside_zodiac (
  player_id INT,
  exec_bucket INT,
  upside_bucket INT,
  chinese_zodiac VARCHAR(20),

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, exec_bucket, upside_bucket, chinese_zodiac),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

---

## TIER 3B: High-Dimension Combos (Optional, Only Build if Needed)

These are sparse tables with potentially NULL values. Only populate if we have sufficient sample size (N >= 5).

**Table: `player_by_condition_roundtype_color_element`**

```sql
CREATE TABLE player_by_condition_roundtype_color_element (
  player_id INT,
  condition VARCHAR(20),
  round_type VARCHAR(20),
  color VARCHAR(20),
  element VARCHAR(20),

  events INT,
  avg_score FLOAT,
  win_rate FLOAT,
  good_count INT,
  bad_count INT,

  PRIMARY KEY (player_id, condition, round_type, color, element),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Note:** This is very granular. Example:
```
(Rory, Calm, Positioning, Green, Metal): 8 events, 75% win rate
```

Only build if you want ultra-personalized scoring for specific scenario combos.

---

## TIER 4: Trend/Form Tables

**Table: `player_recent_form`**

Tracks rolling averages for form calculation.

```sql
CREATE TABLE player_recent_form (
  player_id INT,

  -- Last N events
  last_4_avg_score FLOAT,
  last_4_win_rate FLOAT,
  last_4_events INT,

  last_8_avg_score FLOAT,
  last_8_win_rate FLOAT,
  last_8_events INT,

  last_12_avg_score FLOAT,
  last_12_win_rate FLOAT,
  last_12_events INT,

  -- Momentum (recent vs career)
  momentum_4 FLOAT,                 -- last_4_avg - career_avg
  momentum_8 FLOAT,                 -- last_8_avg - career_avg
  momentum_12 FLOAT,                -- last_12_avg - career_avg

  -- Trend direction
  trend_direction VARCHAR(10),      -- "UP", "DOWN", "FLAT"
  trend_strength FLOAT,             -- 0-1 (how strong is the trend)

  updated_at TIMESTAMP,

  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player_baseline(player_id)
);
```

**Example:**
```
player_id: 1001 (Rory)
last_4_avg_score: 2.85
last_4_win_rate: 0.75
momentum_4: 2.85 - 1.23 = 1.62    -- Running very hot
trend_direction: "UP"
trend_strength: 0.8                -- Strong upward trend
```

---

## TIER 5: Matchup History (Optional)

**Table: `player_head_to_head`**

Stores 2-ball matchup history between players.

```sql
CREATE TABLE player_head_to_head (
  player_a_id INT,
  player_b_id INT,

  -- A vs B record
  a_wins INT,
  b_wins INT,
  ties INT,
  total_matchups INT,
  a_win_rate FLOAT,                 -- a_wins / total_matchups

  -- Last occurrence
  last_matchup_date DATE,

  -- Recency weight (recent matchups matter more)
  recency_weight FLOAT,             -- 0-1 (1 = very recent)

  PRIMARY KEY (player_a_id, player_b_id),
  FOREIGN KEY (player_a_id) REFERENCES player_baseline(player_id),
  FOREIGN KEY (player_b_id) REFERENCES player_baseline(player_id)
);
```

**Example:**
```
player_a_id: 1001 (Rory)
player_b_id: 1002 (Jon)
a_wins: 8
b_wins: 5
total_matchups: 13
a_win_rate: 0.615
last_matchup_date: 2026-03-15
recency_weight: 0.9                -- Recent
```

---

## Data Population Strategy

### Priority 1: Minimum Viable (Week 1)
- player_baseline
- player_by_condition
- player_by_round_type
- player_by_condition_roundtype

**Time:** ~2 hours from ANALYSIS_v2 data

### Priority 2: Full Tier 2 (Week 1-2)
- Add: player_by_color, player_by_element, player_by_exec_upside, player_by_zodiac
- Add: player_recent_form

**Time:** ~3 hours

### Priority 3: Tier 3B & Matchup (Week 2-3, Optional)
- Add: player_by_condition_roundtype_color_element (if sparse enough)
- Add: player_head_to_head

**Time:** ~4 hours

---

## Indexing Strategy

```sql
-- Speed up common queries
CREATE INDEX idx_player_condition ON player_by_condition(player_id, condition);
CREATE INDEX idx_player_roundtype ON player_by_round_type(player_id, round_type);
CREATE INDEX idx_player_cond_rt ON player_by_condition_roundtype(player_id, condition, round_type);
CREATE INDEX idx_player_color_elem ON player_by_color_element(player_id, color, element);
CREATE INDEX idx_recent_form_momentum ON player_recent_form(player_id, momentum_4);
```

---

## Query Examples

### Get Rory's Calm×Positioning Performance
```sql
SELECT * FROM player_by_condition_roundtype
WHERE player_id = 1001 AND condition = 'Calm' AND round_type = 'Positioning';
-- Result: 8 events, 75% win rate, +3.21 avg score
```

### Get Rory's Recent Form
```sql
SELECT * FROM player_recent_form WHERE player_id = 1001;
-- Result: Last 4 avg = +2.85, momentum = +1.62, trend = "UP"
```

### Rory vs Jon Head-to-Head
```sql
SELECT * FROM player_head_to_head
WHERE (player_a_id = 1001 AND player_b_id = 1002)
   OR (player_a_id = 1002 AND player_b_id = 1001);
-- Result: Rory wins 61.5% of the time
```

---

## Implementation Roadmap

**SQL Setup (30 min):**
1. Create all tables
2. Add indices
3. Set up foreign keys

**Data Population (2-3 hours):**
1. Extract from ANALYSIS_v2
2. Calculate aggregates (avg, win_rate, etc.)
3. Populate Tier 1 + Priority 1 tables
4. Verify data quality (spot-check vs raw)

**Integration (1 hour):**
1. Update player_scoring_system.py to query these tables
2. Blend model scores with player historical scores
3. Test on example tournament

**Total Time:** 3.5-4.5 hours to full MVP

---

## Should I build this in SQL or CSV/JSON?

**SQL Advantages:**
- Fast queries (indexing)
- Easy updates (incrementally add new events)
- Scalable (100s of players, 1000s of combos)
- Easy to blend with other data

**CSV/JSON Advantages:**
- Simple, no database setup
- Portable (use in Python directly)
- Quick to get started

**Recommendation:** Start with **CSV files** (faster setup), migrate to **SQL** once you hit 100+ weekly players.

---

Want me to:
1. Build the CSV schema + Python population script?
2. Build the SQL schema + queries?
3. Integrate into the scoring system?