# Golf_Analytics Data Dictionary

Complete reference for every column in the Golf_Analytics sheet.
Use this to understand what goes where, validate new data, and troubleshoot.

---

## Legend

| Field | Meaning |
|-------|---------|
| **Col** | Excel column letter(s) + number |
| **Name** | Column header in Golf_Analytics sheet |
| **Type** | text / number / date / formula / label |
| **Source** | manual / VLOOKUP / INDEX/MATCH / engine / derived |
| **Required** | Yes/No for data to be valid |
| **Example** | Sample value |
| **Validation** | Rules to check before importing |
| **Notes** | Edge cases, caveats |

---

## Section A: Display & Status (A–J)

### A | Year | number | manual | Yes | 2023
- Tournament year
- Usually 4 digits (2023, 2024, 2025)
- Used for filtering historical data
- **Validation:** Must match EVENTS sheet year

### B | Venue | text | manual | Yes | The Sentry
- Event name (tournament title)
- **Must match exactly** with EVENTS sheet column H (COL_EVENT_TITLE)
- Used as match key for INDEX/MATCH formulas
- **Validation:** Case-sensitive; cross-check EVENTS.H for exact spelling

### C | Player | text | manual | Yes | Chad Ramey
- Player name
- **Must match exactly** with PLAYERS sheet column B (COL_NAME)
- Used as match key for VLOOKUP formulas
- **Validation:** Case-sensitive; if name not found, check PLAYERS sheet for spelling

### D–G | R1, R2, R3, R4 | number | manual | See notes | 71, 76, 72, 71
- Actual golf scores (strokes) for each round
- Integer 0–100 (though typically 65–80 for tour players)
- **Required:** At least one round must have a score (R1 mandatory if finished)
- **Validation:**
  - Must be numeric
  - If Status = "Withdrawn" and round < withdrawal round, leave blank
  - If Status = "Finish", all 4 must be populated
  - Score should be ≥ par-5 and ≤ par+10 (course dependent; ~70±15)

### H | ToT | number | formula | Yes | -2
- Total score (sum of R1+R2+R3+R4 relative to par)
- Negative = under par (good); Positive = over par
- **Auto-calculated:** Should equal (R1+R2+R3+R4) − (par×4)
- **Validation:** Manually calculate; if mismatch, check individual rounds

### I | Status | text | manual | Yes | Finish / Withdrawn
- Tournament completion status
- **Valid values:** "Finish", "Withdrawn", "CUT", "DQ" (disqualified)
- **Rules:**
  - "Finish" = all 4 rounds played
  - "Withdrawn" = stopped playing (R3+R4 blank)
  - "CUT" = missed cut after R2 (R3+R4 blank)
  - "DQ" = disqualified (mark which round)
- **Validation:** Must be one of the above

### J | Dedupe_Key | text | formula/manual | Yes | RES_2023_401465512_10057
- Unique ID for this player-result combination
- Format: `RES_[Year]_[Event_ID]_[Player_ID]`
- Used to prevent duplicate imports
- **Validation:** No two rows should have the same Dedupe_Key
- **Notes:** Can be auto-generated if player_id + event_id available, else manually created

---

## Section B: Input (K–Q) — Read by Engine

These columns are read by the engine to compute colors + scores.
They use VLOOKUP/INDEX/MATCH formulas pulling from PLAYERS and EVENTS sheets.

### K | Birthday | date | VLOOKUP | Yes | 8/3/1992
- Player's birth date
- **Formula:** `=IFERROR(VLOOKUP(C2,PLAYERS!B:E,2,0),"")`
- Pulls from PLAYERS sheet column C (COL_BIRTHDAY)
- **Validation:** Date should be reasonable (1960–2010 for tour players)
- **Type:** Date in M/D/YYYY or similar

### L | GMT | number | VLOOKUP | Yes | -6
- Player's birth timezone offset (GMT hours)
- **Formula:** `=IFERROR(VLOOKUP(C2,PLAYERS!B:E,4,0),"")`
- Pulls from PLAYERS sheet column E (COL_GMT)
- **Range:** -12 to +14 (valid UTC offsets)
- **Type:** Number (can be decimal, e.g., 5.5 for India)
- **Validation:** Must be within ±14

### M–P | Rd1 Date, Rd2 Date, Rd3 Date, Rd4 Date | date | INDEX/MATCH | Yes | 1/5/2023
- Round dates (when the round was played)
- **Formula (example for M):** `=IFERROR(INDEX(EVENTS!C:C,MATCH(B2,EVENTS!H:H,0)),"")`
- Pulls from EVENTS sheet (COL_R1_DATE, COL_R2_DATE, etc.)
- **Validation:**
  - Must be valid dates
  - R1 ≤ R2 ≤ R3 ≤ R4 (increasing order)
  - Dates should be 1–7 days apart (typical tournament)

### Q | GMT (Venue) | number | INDEX/MATCH | Yes | -10
- Venue/course timezone offset (GMT hours)
- **Formula:** `=IFERROR(INDEX(EVENTS!G:G,MATCH(B2,EVENTS!H:H,0)),"")`
- Pulls from EVENTS sheet column G (COL_GMT)
- **Range:** -12 to +14
- **Type:** Number
- **Validation:** Must be within ±14; typically matches geography of venue

---

## Section C: Engine Output (R–AH) — Written by Engine

Engine computes these during overnight run. Do NOT manually edit.

### R–U | R1 Rhythm, R2 Rhythm, R3 Rhythm, R4 Rhythm | text | engine | Auto | Purple
- **Actual column:** R (R1), S (R2), T (R3), U (R4)
- Color label representing lucky day delta for that round
- **Valid values:** Purple, Blue, Green, Yellow, Orange, Pink, Red, Brown (or variations)
- **Engine computes:** Via LUCKY_DAY_DELTA() + LUCKY_CATEGORY_COLOR()
- **Validation:** Should be non-empty if all inputs (K, L, M–P, Q) are filled
- **Notes:** "Rhythm" = colloquial for "daily luck color"

### V–AG | Exec/Upside/Peak × Rounds | number | engine | Auto | 44, 96, 0.62
- **Actual columns:**
  - R1: V (Exec), W (Upside), X (Peak)
  - R2: Y (Exec), Z (Upside), AA (Peak)
  - R3: AB (Exec), AC (Upside), AD (Peak)
  - R4: AE (Exec), AF (Upside), AG (Peak)

#### Exec (Execute)
- 0–100 score representing "clean execution" potential
- Higher = more likely to play steady, avoid mistakes
- **Calculation:** Base 50 + resource/power/output/wealth adjustments − peer penalty − peak penalty
- **Engine:** GOLF_CFG.EXEC weights in 12_engine_golf.gs

#### Upside
- 0–100 score representing "best-case scenario" ceiling
- Higher = more likely to catch fire, score low
- **Calculation:** Base 50 + output/wealth bonuses + plateau bonus − extreme peak penalty
- **Engine:** GOLF_CFG.UPSIDE weights in 12_engine_golf.gs

#### Peak
- 0–1.0 decimal: environmental "peakiness" (concentration of elements)
- Higher = more volatile environment (one element dominates)
- Lower = balanced environment (all elements equally present)
- **Calculation:** Entropy-based; 0 = perfectly flat distribution, 1 = one element at 100%
- **Engine:** _peakiness_() in 21_utils_elements_math.gs

**Validation:**
- Exec + Upside should both be 0–100
- Peak should be 0.0–1.0 (3 decimals)
- Usually: Exec + Upside ≈ 100 (they're balanced)
- If any is blank, check that K, L, M–P, Q are filled

### AH | Best Upside Round | text | engine | Auto | R4
- Label of which round (R1, R2, R3, R4) has the highest Upside score
- **Engine logic:** Compares Upside values; returns round with max
- **Validation:** Should match one of {R1, R2, R3, R4} or be blank if no rounds
- **Example:** "R2" means Round 2 has the best upside

---

## Section D: Post-Engine Reference (AI–AP)

Filled by analysis scripts or manual entry. NOT written by engine.

### AI–AL | Course Avg R1, R2, R3, R4 | number | derived | Yes | 69.39, 68.08, 68.97, 67.70
- **Columns:** AI (R1), AJ (R2), AK (R3), AL (R4)
- Field average score for that round at that course
- Used to compute "vs Avg" (difference from field)
- **Source:** Calculated from RESULTS_RAW or ANALYSIS sheet (average of all players that round)
- **Type:** Decimal (usually 66–72 for tour courses)
- **Validation:** Should be 60–75 (typical tour course range)
- **Notes:** Excludes withdrawn players; only counts finished rounds

### AM–AP | R1 vs Avg, R2 vs Avg, R3 vs Avg, R4 vs Avg | number | formula | Yes | 1.61, 7.92, 3.03, 3.30
- **Columns:** AM (R1), AN (R2), AO (R3), AP (R4)
- Difference between player's score and field average
- **Formula:** `=D2−AI2` (Player R1 − Course Avg R1)
- **Type:** Decimal (can be negative or positive)
- **Range:** Typically −10 to +15 (rare to be more extreme)
- **Interpretation:**
  - Negative = better than field (outperformed)
  - Positive = worse than field (underperformed)
  - 0 = exactly at field average
- **Validation:** vs Avg = Score − Course Avg (hand-check 2–3 rows)

---

## Section E: Conditions & Round Info (AQ–AX)

Pulled from EVENTS sheet or manually entered.

### AQ–AT | R1 Cond, R2 Cond, R3 Cond, R4 Cond | text | EVENTS | Yes | Calm, Calm, Calm, Moderate
- **Columns:** AQ (R1), AR (R2), AS (R3), AT (R4)
- Weather/course difficulty condition for that round
- **Valid values:** "Calm", "Moderate", "Tough"
- **Definition:**
  - Calm: wind <7 mph, temp 55–90°F, no precip → score 0–2
  - Moderate: wind 7–24 mph, temp 40–55 or >90°F, light precip → score 3–5
  - Tough: wind ≥25 mph, temp <40°F, precip ≥3mm, gusts ≥35 → score 6+
- **Engine:** CONDITIONS_CALCULATE_() in 14_engine_conditions.gs
- **Validation:** Must be one of the three above; pulled from EVENTS sheet or fetched via weather API

### AU–AX | Round Type R1, R2, R3, R4 | text | manual | Sometimes | Open, REMOVE, Positioning, Closing
- **Columns:** AU (R1), AV (R2), AW (R3), AX (R4)
- Tournament structure classification
- **Valid values:** "Open", "Positioning", "Closing", "REMOVE"
- **Definition:**
  - Open: First round(s); everyone still in contention; all skill levels visible
  - Positioning: Mid-rounds; field spread widens; strong players separate
  - Closing: Final round(s); high-stakes, tight leaderboard; pressure increases
  - REMOVE: Anomalous format (rare); exclude from combo analysis
- **Source:** Manually assigned or inferred from tournament structure
- **Validation:** Must be one of the four; TBD: auto-populate based on tournament type
- **Notes:** PGA Tour typically: R1=Open, R2=Open, R3=Positioning, R4=Closing

---

## Section F: Moon & Lunar (AY–BB)

Lunar phase classifications. Two systems: 10-cat and 8-cat (see MoonWest).

### AY–BB | Moon R1, R2, R3, R4 | text | manual/formula | Sometimes | Shukla Bhadra, Shukla Nanda, Krishna Purna, Krishna Rikta
- **Columns:** AY (R1), AZ (R2), BA (R3), BB (R4)
- **System:** 10-category lunar phase (Hindu/Vedic calendar — Tithi)
- **Categories:** Shukla Bhadra, Shukla Nanda, Shukla Pratipada, ... Krishna Rikta (various phases)
- **Type:** Text (phase name)
- **Source:** Calculated from round date + astro algorithm (solar-lunar calendar)
- **Validation:** Must be one of ~10 valid Tithi names
- **Notes:** Part of broader divination analysis; correlates with energy/luck in some models
- **TBD:** Link to actual lunar phase calculation (currently manual/lookup)

---

## Section G: Divination & Numerology (BC–BL)

Player-level attributes (same value every round). Used for pattern detection.

### BC | Wu Xing Element | text | manual/VLOOKUP | Sometimes | Water
- **Column:** BC
- **System:** Wu Xing (Five Elements) — Chinese philosophy
- **Valid values:** Wood, Fire, Earth, Metal, Water
- **Derivation:** Calculated from player's birth date (stems + branches in BaZi)
- **Source:** Pulled from PLAYERS sheet (or calculated on import)
- **Notes:** Each element has associations (personality, luck cycles, strengths)
- **Validation:** Must be one of the five

### BD | Chinese Zodiac | text | manual/formula | Sometimes | Monkey
- **Column:** BD
- **Valid values:** Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig (12 animals)
- **Derivation:** Birth year modulo 12
- **Notes:** Used to detect player-condition matching patterns
- **Validation:** Must be one of the 12

### BE | Destiny Card | text | manual/lookup | Sometimes | Six of Wands
- **Column:** BE
- **System:** Tarot (Destiny Card based on numerology)
- **Valid values:** 22 Major Arcana cards (Fool, Magician, High Priestess, ..., World)
- **Derivation:** Name-based numerology → tarot correspondence
- **Notes:** Experimental; used in some combo analyses
- **Validation:** Must be valid Tarot card name

### BF | Horoscope | text | manual/VLOOKUP | Sometimes | LEO
- **Column:** BF
- **System:** Western zodiac
- **Valid values:** ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES
- **Derivation:** Birth date month/day
- **Source:** Pulled from PLAYERS sheet
- **Validation:** Must be one of the 12 signs

### BG–BJ | MoonWest R1, R2, R3, R4 (8C) | text | manual/formula | Sometimes | Waxing Crescent, New Moon, New Moon, Waning Crescent
- **Columns:** BG (R1), BH (R2), BI (R3), BJ (R4)
- **System:** Western 8-category lunar phase (round-level, not player-level)
- **Valid values:** New Moon, Waxing Crescent, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Waning Crescent
- **Derivation:** Calculated from round date using solar-lunar angle
- **Notes:** Same value for all players in a round (environmental)
- **Validation:** Must be one of the 8

### BK | Life Path | number | manual/formula | Sometimes | 5
- **Column:** BK
- **System:** Numerology (Life Path number)
- **Valid values:** 1–9 (or master numbers 11, 22, 33)
- **Derivation:** Summed digits of birth date until single digit (numerological reduction)
- **Notes:** Each number has meaning (1=leader, 2=partner, etc.)
- **Validation:** Must be 1–9 (or 11, 22, 33)

### BL | Tithi | number or text | manual/formula | Sometimes | 10
- **Column:** BL
- **System:** Hindu lunar calendar (Tithi — lunar day)
- **Valid values:** 1–30 (lunar month) or Tithi names
- **Derivation:** Calculated from round date + lunar phase algorithm
- **Notes:** Part of Vedic astrology; finer granularity than Moon R1–R4 above
- **Validation:** If numeric: 1–30. If text: must match valid Tithi name

---

## Section H: Other Signals (BM–BO)

### BM | R1 GAP | number | formula | Sometimes | -52
- **Column:** BM
- **Definition:** How much player outperformed field in Round 1
- **Formula:** `=D2−AI2` (same as vs Avg, but flagged as "gap" for pattern detection)
- **Type:** Decimal (can be negative)
- **Interpretation:**
  - Positive = player beat field (good sign of form)
  - Negative = player underperformed field
- **Notes:** Used to detect momentum/consistency patterns across rounds
- **Validation:** Should equal R1 − Course Avg R1

### BN | Round Withdrawn | number | manual | Sometimes | 2
- **Column:** BN
- **Definition:** If player withdrew, which round did they withdraw after?
- **Valid values:** Blank (finished), or 1, 2, 3, 4 (withdrew after that round)
- **Type:** Number
- **Interpretation:**
  - 1 = withdrew after R1 (e.g., injury after first round)
  - 2 = withdrew after R2 (missed cut)
  - 3 = withdrew after R3
  - Blank = finished all 4 rounds
- **Validation:** If Status = "Withdrawn", this should be filled; if Status = "Finish", should be blank

### BO | Tour | text | manual/VLOOKUP | Yes | PGA Tour
- **Column:** BO
- **Valid values:** "PGA Tour", "LIV Golf", "DP World Tour", or other (as expanded)
- **Source:** Pulled from EVENTS sheet (COL_TOUR)
- **Type:** Text
- **Validation:** Must be one of known tour values
- **Notes:** Used for future tour-based bucketing and signal stratification
- **Future work:** Separate combo analyses by tour once LIV + DP World data integrated

---

## Summary Validation Rules

**Before importing a row, check:**

1. ✓ Dedupe_Key is unique (no duplicate player-event-year)
2. ✓ Player name (C) matches PLAYERS sheet exactly
3. ✓ Event/Venue (B) matches EVENTS sheet exactly
4. ✓ Year (A) matches EVENTS sheet
5. ✓ Scores (D–G) are numeric, make sense (60–85 range typical)
6. ✓ Total (H) = R1+R2+R3+R4 − par×4
7. ✓ Status is one of {Finish, Withdrawn, CUT, DQ}
8. ✓ If Status = Finish, all 4 rounds populated
9. ✓ If Status = Withdrawn, only rounds up to withdrawal are filled
10. ✓ Round dates (M–P) are in order and spaced 1–7 days apart
11. ✓ GMT offsets (L, Q) are reasonable (−12 to +14)

---

## See Also

- [CLAUDE.md](CLAUDE.md) — Architecture + workflow
- [00_config.gs](engine/00_config.gs) — GA config constants
- [DATA_INTAKE_CHECKLIST.md](DATA_INTAKE_CHECKLIST.md) — Import validation process
- [AUDIT_FRAMEWORK.md](AUDIT_FRAMEWORK.md) — Verification layers
