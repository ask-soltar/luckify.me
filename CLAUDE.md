# Luckify Me — Project Reference for Claude

> **Working on the React app?** Open `luckify-me/` as your root in VS Code.
> The `luckify-me/CLAUDE.md` inside that folder has everything you need.
> The rest of this file covers the **Google Apps Script / golf analytics system** only.

---

This file covers the GAS engine, sheet layout, conventions, and active work for the golf analytics system.

---

## What This Project Is

A Google Apps Script + Python analytics system for golf betting.
Core idea: combine BaZi (Chinese astrology) scoring with golf round conditions to find
player-day edges for 2-ball and 3-ball matchup betting.

**Primary workflow:**
1. PLAYERS sheet holds player birthdays → engine computes daily luck scores
2. EVENTS sheet holds round dates/conditions → engine assigns condition labels
3. Golf_Analytics sheet is the main computation surface (colors + exec/upside scores)
4. ANALYSIS sheet holds one row per round for model training/backtesting
5. Python scripts in the root read the ANALYSIS sheet (via Google Sheets API) for combo analysis

---

## Core Principles

**Every piece of work in this project follows three rules:**

1. **Transparency** — No hidden assumptions. Every formula, every decision, every threshold is documented in plain language. A newcomer reads the work log and understands why the data is the way it is.

2. **Verification** — No claim is true until it's checked. We use an audit framework with 5 layers (import → formula → derivation → analysis → betting). Each layer gates the next.

3. **Game Theory Alignment** — We structure incentives so the truth is always easier than covering it up. Traceability by design. Reversible changes. Immutable audit trails. Bad data is caught early, not after 6 months of betting gone wrong.

**This is not bureaucracy.** It's the opposite. By being transparent and auditable, we move *faster* because we don't waste time debugging hidden errors.

---

## Data Workflow (The Full Loop)

```
Raw Golf Data
    ↓
[DATA_INTAKE_CHECKLIST.md] — Human flags + validates import
    ↓
Golf_Analytics sheet — Paste validated data (formulas compute colors, scores, etc.)
    ↓
[Engine: 10_–14_ layers] — Computes exec/upside/peak per round
    ↓
ANALYSIS sheet — Derived columns (vs Avg, conditions, moon, etc.)
    ↓
[AUDIT_FRAMEWORK.md] — Spot-check sample rows, verify calculations
    ↓
Python combo scripts — Find signals (4D Element, gap patterns, etc.)
    ↓
FINAL_BETTING_SIGNALS.md — Document validated signals + deployment rules
    ↓
Live Betting — Execute + track outcomes
    ↓
P&L Review + Audit — Compare live results to model; if divergent, trace why
    ↓
Update CLAUDE.md + engine — Rinse, repeat
```

---

## Golf_Analytics Sheet: The Import Gateway

**What it is:** The single entry point for all raw golf tournament data. Every score, every player, every round enters here first.

**ID Columns (BP, BQ):** Contain INDEX/MATCH formulas (not populated values) that dynamically look up:
- **BP (player_id):** `=IFERROR(INDEX(PLAYERS!$A:$A, MATCH(C2, PLAYERS!$B:$B, 0)), "")`
- **BQ (event_id):** `=IFERROR(INDEX(EVENTS!$A:$A, MATCH(B2, EVENTS!$H:$H, 0)), "")`
- These formulas auto-update when PLAYERS/EVENTS sheets change. No repopulation needed.

**What it's not:** A computation engine. It's a holding tank. Raw data + human-verified formulas that pull from PLAYERS/EVENTS.

**Flow:**
1. New tournament results arrive (email, website scrape, API, manual copy-paste)
2. Fill out DATA_INTAKE_CHECKLIST.md template with the raw data
3. Validate all rows against PLAYERS + EVENTS sheets (exact name match)
4. Once checklist is **READY**, paste the data into Golf_Analytics
5. Engine runs overnight (or on-demand) and fills colors + scores
6. Audit Framework Layer 2 runs: spot-check 5+ rows, verify totals
7. Once audit passes, mark checklist as **LOCKED**

**Why this matters:**
- If we discover bad data months later, we trace it back to the original checklist
- No "where did this number come from?" questions
- Automation (future) will plug in here: flag new tournaments, auto-alert human to fill checklist

**Columns in Golf_Analytics:**
See the full map in the [Golf_Analytics (GA) section](#golf_analytics-ga) below.
Engine writes R–AH (colors + scores). Humans fill AI–BN (derived reference columns).

---

## Engine Architecture (Google Apps Script)

Scripts are numbered by layer. Load order matters.

```
00_config.gs         — All constants. No logic. No Sheets. Read-only.
01_menu.gs           — UI menu wiring only. Delegates to writers.
02_runner_overnight.gs — Trigger management + chunked batch runner.
03_writer_golf_analytics.gs — Reads/writes Golf_Analytics. Calls engines.
03b_writer_run_logs.gs — Appends to RUN_LOGS sheet after each run.
03c_writer_engine_settings.gs — Manages ENGINE_SETTINGS sheet + version.

05_lookup_players.gs — Cached PLAYERS sheet reader. Returns player objects.
06_lookup_events.gs  — Cached EVENTS sheet reader. Returns event objects.

07_fetcher_conditions.gs    — Weather API fetch + writes to EVENTS sheet.
07c_fetcher_espn_players.gs — ESPN player lookup for birthday verification.
07d_fetcher_wikidata.gs     — Wikidata lookup for birthday verification.
08_gmt_finder.gs            — Timezone/GMT resolution helpers.
08_writer_conditions.gs     — Writes fetched conditions to EVENTS.
09_writer_birthday_verify.gs — Writes ESPN/Wikidata results to BIRTHDAY_VERIFY.

10_engine_lucky_day.gs  — Lucky Day delta scoring. Pure math only.
10_analysis_baseline.gs — ANALYSIS sheet population + COURSES/EVENTS_COURSES setup.
11_engine_categories.gs — Delta → category → color mapping. Pure math only.
12_engine_golf.gs       — Exec/Upside/Peak scoring. Pure math only.
13_engine_bazi_core.gs  — BaZi pillars, solar longitude, sexagenary math. Core IP.
14_engine_conditions.gs — Weather score → Calm/Moderate/Tough label. Pure math only.

20_utils_dates.gs        — Date coercion, localToUTC, timezone helpers.
21_utils_elements_math.gs — Vector math, peakiness, element relationships.
22_utils_keys.gs         — _safeKey_(), generateId_().
23_utils_general.gs      — Placeholder for misc shared helpers.

90_debug_tests.gs    — TEST_SINGLE_ROW, DEBUG_ACTIVE_ROW. Never called in production.
96_wire_golf_analytics.gs — One-time: writes VLOOKUP/INDEX formulas to Golf_Analytics K:Q.
97_import_results_raw.gs  — One-time: imports Golf_Analytics scores into RESULTS_RAW.
98_auto_add_missing_players.gs — Scans Golf_Analytics and auto-adds missing players.
99_helpers_id_gen.gs  — ID generation helpers.
```

### Core Rule: Layer Discipline

- `10_`–`14_` engine files: **ZERO Sheets access**. Pure functions only.
- `05_`–`09_` fetchers/lookups: **read-only** Sheets access.
- `03_` writers: **read + write** Sheets access. Call engines, never contain logic.
- `00_config.gs`: **no functions, no logic, constants only**.

Violating these rules breaks testability and memo caching.

---

## Sheet Structure

### PLAYERS (cols A–P)
| Col | Constant | Content |
|-----|----------|---------|
| A | COL_PLAYER_ID | PLY_XXXX |
| B | COL_NAME | Player name |
| C | COL_BIRTHDAY | Birth date |
| D | COL_BIRTHPLACE | Birth city |
| E | COL_GMT | GMT offset |
| F | COL_HUMAN_CHECK | Verified flag |
| G | COL_ELEMENT | Wu Xing element |
| H | COL_HOROSCOPE | Western horoscope |
| I | COL_HORO_BUCKET | Horoscope bucket |
| J | COL_FIRST_RED | First red day |
| K | COL_PERS_CARD | Personality card |
| L | COL_SOUL_CARD | Soul card |
| M | COL_BC_PATTERN | BC pattern |
| N | COL_NUMER_BUCKET | Numerology bucket |
| O | COL_TITHI_NUM | Tithi number |
| P | COL_TITHI_TYPE | Tithi type |

### EVENTS (cols A–AS)
Key columns:
| Col | Constant | Content |
|-----|----------|---------|
| A | COL_EVENT_ID | EVT_XXXX |
| B | COL_TOUR | Tour name |
| C–F | COL_R1_DATE–R4_DATE | Round dates |
| G | COL_GMT | Venue GMT |
| H | COL_EVENT_TITLE | Event name (match key) |
| I | COL_VENUE | Course name |
| J | COL_LOCATION | City/State |
| K | COL_COURSE_ID | FK → COURSES sheet |
| L | COL_LATITUDE | Lat |
| M | COL_LONGITUDE | Lon |
| N–Q | COL_MOON_R1_10C–R4_10C | Moon phase (10-cat) |
| R–U | COL_MOON_R1_8C–R4_8C | Moon phase (8-cat) |
| V–Y | COL_TITHI_R1–R4 | Tithi per round |
| Z–AC | COL_TYPE_R1–R4 | Round type |
| AD–AG | COL_ASCDEC_R1–R4 | Asc/Dec |
| AH–AK | COL_COND_R1–R4 | **Conditions: Calm/Moderate/Tough** |
| AL–AO | COL_RND1_BUCKET–R4_BUCKET | Round buckets |
| AP–AS | COL_R1_AVG–R4_AVG | Field averages per round (withdrawn-adjusted) |
| AT | COL_YEAR | Year |
| AU | COL_TOURNAMENT_TYPE | Tournament scoring type |

**Field Averages (AP–AS):** Exclude withdrawn rounds from calculation
- **AP (R1 avg):** `=AVERAGE(FILTER(Golf_Analytics!D2:D,(Golf_Analytics!B2:B=H2)*(Golf_Analytics!I2:I<>"Withdrawn")*(Golf_Analytics!BN2:BN<>1)))`
- **AQ (R2 avg):** `=AVERAGE(FILTER(Golf_Analytics!E2:E,(Golf_Analytics!B2:B=H2)*(Golf_Analytics!I2:I<>"Withdrawn")*(Golf_Analytics!BN2:BN<>2)))`
- **AR (R3 avg):** `=AVERAGE(FILTER(Golf_Analytics!F2:F,(Golf_Analytics!B2:B=H2)*(Golf_Analytics!I2:I<>"Withdrawn")*(Golf_Analytics!BN2:BN<>3)))`
- **AS (R4 avg):** `=AVERAGE(FILTER(Golf_Analytics!G2:G,(Golf_Analytics!B2:B=H2)*(Golf_Analytics!I2:I<>"Withdrawn")*(Golf_Analytics!BN2:BN<>4)))`

Why: Withdrawn rounds distort field averages and are not comparable to completed scores. Only completed rounds are included.

**Tournament Type values (AU):**
- `S` = Standard Stroke Play (comparable, use for off_par)
- `NS` = Non-Standard Stroke Play (caution: different rules)
- `T` = Team format (not directly comparable)
- `P` = Points-based (e.g., Barracuda — different scoring system)
- `M` = Match play (not comparable to stroke play)

**Note:** COL_WS_D1–D4 (formerly wind-speed) is deprecated — same columns as COL_COND_R1–R4.

### Golf_Analytics (GA)
Full column map — verified against actual sheet headers (2026-03-30).

| Col | # | Constant | Content |
|-----|---|----------|---------|
| A | 1 | COL_YEAR | Year |
| B | 2 | COL_VENUE | Event name (match key → EVENTS) |
| C | 3 | COL_PLAYER | Player name (match key → PLAYERS) |
| D–G | 4–7 | COL_R1–R4 | Actual round scores |
| H | 8 | COL_TOT | Total score |
| I | 9 | COL_STATUS | Finish / Withdrawn / CUT |
| J | 10 | COL_DEDUPE_KEY | Deduplication key |
| K | 11 | COL_BIRTHDAY | =VLOOKUP birthday from PLAYERS |
| L | 12 | COL_BDAY_GMT | =VLOOKUP birth GMT from PLAYERS |
| M–P | 13–16 | COL_RD1–RD4 | =INDEX/MATCH round dates from EVENTS |
| Q | 17 | COL_VENUE_GMT | =INDEX/MATCH venue GMT from EVENTS |
| R–U | 18–21 | COL_COLOR_START | **Engine writes:** R1–R4 Rhythm (color) |
| V–AG | 22–33 | COL_SCORE_START | **Engine writes:** Exec/Upside/Peak × 4 rounds |
| AH | 34 | COL_BEST_ROUND | **Engine writes:** Best Upside round label |
| AI–AL | 35–38 | COL_COURSE_AVG_R1–R4 | Field avg per round (exclude withdrawn) |
| AM–AP | 39–42 | COL_VS_AVG_R1–R4 | Score − course avg (withdrawn-adjusted) |
| AQ–AT | 43–46 | COL_COND_R1–R4 | **Conditions: Calm / Moderate / Tough** |
| AU–AX | 47–50 | COL_TYPE_R1–R4 | Round Type: Open / Positioning / Closing / REMOVE |
| AY–BB | 51–54 | COL_MOON_R1–R4 | Moon phase (10-cat) |
| BC | 55 | COL_WU_XING | Wu Xing Element |
| BD | 56 | COL_ZODIAC | Chinese Zodiac |
| BE | 57 | COL_DESTINY_CARD | Destiny Card |
| BF | 58 | COL_HOROSCOPE | Western Horoscope |
| BG–BJ | 59–62 | COL_MOONWEST_R1–R4 | MoonWest phase (8-cat) per round |
| BK | 63 | COL_LIFE_PATH | Life Path number |
| BL | 64 | COL_TITHI | Tithi |
| BM | 65 | COL_GAP_R1 | R1 GAP score |
| BN | 66 | COL_ROUND_WD | Round Withdrawn number |
| BO | 67 | COL_TOUR | Tour (PGA Tour / LIV Golf / DP World Tour / other) |
| BP | 68 | COL_PLAYER_ID | =INDEX/MATCH lookup player_id from PLAYERS |
| BQ | 69 | COL_EVENT_ID | =INDEX/MATCH lookup event_id from EVENTS |
| BR | 70 | COL_COURSE_PAR | =INDEX/MATCH lookup par from EVENTS_COURSES by event_id + year |
| BT–BW | 72–75 | COL_EVENT_DAY_R1–R4 | Event calendar day per round (from EVENTS.R1–R4_DATE) |
| BX | 76 | COL_EVENT_GMT | Event GMT offset (from EVENTS.GMT) |
| BY–CB | 77–80 | COL_PERSONAL_DAY_R1–R4 | **Numerology:** Personal Day per round (PY + month + day, with Master Number logic) |

**BR (course_par) formula:**
```
=IFERROR(INDEX(EVENTS_COURSES!D:D,MATCH(1,(EVENTS_COURSES!A:A=BQ2)*(EVENTS_COURSES!C:C=A2),0)),"")
```
Used by EVENTS sheet field average formulas (AP–AS) to validate withdrawn rounds.

**BT–BW (Event Day per round) formula example (BT for R1):**
```
=IFERROR(INDEX(EVENTS!C:G, MATCH(BQ2, EVENTS!A:A, 0), ), "")
```
Looks up event dates (EVENTS columns C–G: R1–R4 dates) by matching event_id. Similar formulas for BU–BW with column offset for R2–R4.

**BY–CB (Personal Day numerology) formula example (BY for R1):**
```
=IF(OR($K2="",BT2=""),"",
LET(
  birthMonth, MONTH($K2),
  birthDay, DAY($K2),
  currentYear, YEAR(BT2),
  currentMonth, MONTH(BT2),
  currentDay, DAY(BT2),

  yearDigitSum, SUMPRODUCT(MID(currentYear&"", SEQUENCE(LEN(currentYear&"")), 1)*1),

  personalYearRaw, birthMonth + birthDay + yearDigitSum,
  personalYear, IF(OR(personalYearRaw=11, personalYearRaw=22, personalYearRaw=33),
    personalYearRaw,
    IF(personalYearRaw>9, MOD(personalYearRaw-1,9)+1, personalYearRaw)
  ),

  personalMonthRaw, personalYear + currentMonth,
  personalMonth, IF(OR(personalMonthRaw=11, personalMonthRaw=22, personalMonthRaw=33),
    personalMonthRaw,
    IF(personalMonthRaw>9, MOD(personalMonthRaw-1,9)+1, personalMonthRaw)
  ),

  personalDayRaw, personalMonth + currentDay,
  personalDay, IF(OR(personalDayRaw=11, personalDayRaw=22, personalDayRaw=33),
    personalDayRaw,
    IF(personalDayRaw>9, MOD(personalDayRaw-1,9)+1, personalDayRaw)
  ),

  personalDay
))
```
Calculates Personal Day as: Personal Year + event month + event day (with Master Number preservation: 11, 22, 33 stay as is; all others reduce to single digit via modulo logic). Similar logic for BZ–CB with BU–BW date references.

**AM–AP (vs_avg R1–R4 with withdrawn adjustment):**
For withdrawn rounds, use `(player_avg + 4) - course_avg` instead of actual score.

- **AM (R1):** `=IF(D2="","",IF(BN2=1,AVERAGEIFS($D$2:$D,$C$2:$C,C2,$BN$2:$BN,"<>1")+4-AI2,D2-AI2))`
- **AN (R2):** `=IF(E2="","",IF(BN2=2,AVERAGEIFS($E$2:$E,$C$2:$C,C2,$BN$2:$BN,"<>2")+4-AJ2,E2-AJ2))`
- **AO (R3):** `=IF(F2="","",IF(BN2=3,AVERAGEIFS($F$2:$F,$C$2:$C,C2,$BN$2:$BN,"<>3")+4-AK2,F2-AK2))`
- **AP (R4):** `=IF(G2="","",IF(BN2=4,AVERAGEIFS($G$2:$G,$C$2:$C,C2,$BN$2:$BN,"<>4")+4-AL2,G2-AL2))`

**Withdrawn logic:** If round_withdrawn matches this round (BN=round_num), calculate player's historical avg for that round (excluding other withdrawals), add +4 penalty, subtract course_avg. Otherwise use actual score − course_avg.

---

### ANALYSIS v3 Off-Par Logic (AC column)
**AC (off_par) excludes non-stroke-play tournaments:**
```
=IFERROR(IF(OR(AH2="T",AH2="P",AH2="M"),"",G2-H2),"")
```
If tournament_type (AH) is Team (T), Points (P), or Match play (M) → leave blank. These formats are not comparable to stroke play.
Only S (Standard Stroke Play) and NS (Non-Standard Stroke Play) get off_par values.

### ANALYSIS v3 (cols A–AO)
One row per round played. Source for all Python combo analysis. 41 columns with all divination + calculated metrics.

**Core columns (A–X, direct data):**
| Col | Content |
|-----|---------|
| A–C | player_id, player_name, event_id |
| D–E | event_name, year |
| F–P | round_num, score, par, course_avg, vs_avg, condition, round_type, color, exec, upside, peak |
| Q–X | moon, wu_xing, zodiac, life_path, tithi, gap, tour, is_best_round |

**Divination + West (Y–Z):**
| Col | Content |
|-----|---------|
| Y | horoscope (Western sun sign) |
| Z | moonwest (8-cat Western moon per round) |

**Historical player metrics (AA–AB, formulas):**
| Col | Content | Formula |
|-----|---------|---------|
| AA | player_hist_par | AVERAGEIFS off_par by player + condition |
| AB | player_his_cnt | COUNTIFS rounds by player + condition |

**Performance metrics (AC–AG, formulas):**
| Col | Content | Formula |
|-----|---------|---------|
| AC | off_par | score − par (blank if tournament_type = T/P/M — not comparable) |
| AD | exec_bucket | exec binned by 25s (0-25, 25-50, 50-75, 75-100) |
| AE | upside_bucket | upside binned by 25s |
| AF | gap_bucket | gap binned by 10s (20-30, 10-20, 0-10, -10-0, -20--10, <-20) |
| AG | adj_his_par | adjusted historical par with shrinkage (player_hist_par blended with tour avg) |

**Tournament metadata (AH):**
| Col | Content |
|-----|---------|
| AH | tournament_type | tournament type (S/NS/T/P/M) from EVENTS |

**Numerology + birth (AI–AM, formulas):**
| Col | Content | Formula |
|-----|---------|---------|
| AI | Birthday | =XLOOKUP(player_id, PLAYERS!A:A, PLAYERS!C:C) — player birth date from PLAYERS |
| AJ | Personal Year | Birth month + birth day + current year, reduced 1-9 (Master Numbers 11/22/33 preserved) |
| AK | Event Date | =INDEX(EVENTS, MATCH(event_id, EVENTS!A:A), round_num) — round date from EVENTS |
| AL | Personal Month | Personal Year + current month, reduced 1-9 (Master Numbers preserved) |
| AM | Personal Day | Personal Month + current day, reduced 1-9 (Master Numbers preserved) |

**Moon grouping + Universal (AN–AO):**
| Col | Content | Formula |
|-----|---------|---------|
| AN | Moon Bucket (6) | Groups moonwest into: Waxing, Waning, Full Moon, New Moon (+ variants) |
| AO | Universal Day | =INDEX(EVENTS!BI:BI/BJ:BJ/BK:BK/BL:BL, MATCH(event_id, EVENTS!A:A), round_num) — universal day per round from EVENTS |

**Definition notes:**
- **vs Avg:** score vs venue field average for that round — NOT vs par
- **Master Numbers:** 11, 22, 33 preserved in numerology; all others reduced to single digit via modulo logic
- **Universal Day:** Event-level numerology metric indexed by round (R1→BI, R2→BJ, R3→BK, R4→BL in EVENTS)

### RESULTS_RAW (cols A–K)
Raw scores by player + event. Used for ID-linked imports.

### Other Sheets
- `COURSES` — Course registry (course_id, name, location)
- `EVENTS_COURSES` — Event+course+year+par junction table
- `BIRTHDAY_VERIFY` — ESPN/Wikidata birthday verification results
- `RUN_LOGS` — Engine run history (timestamp, version, rows, duration, status)
- `ENGINE_SETTINGS` — Active engine version
- `TOUR_STATS` — Tour-level averages by condition (built from ANALYSIS v3)
  - Column A: Condition (Calm, Moderate, Tough)
  - Column B: Tour average off_par for that condition
  - **Built by:** Menu → 📊 ANALYSIS v3 → "📊 Build TOUR_STATS"
  - **Used by:** AG formula (adj_his_par shrinkage)

---

## Key Scoring Constants (00_config.gs)

### Lucky Day Engine (LUCKY_CFG)
- Natal pillar weights: year×1.5, month×2, day×3, hour×1
- Environment blend: 70% day pillar, 30% year pillar
- Score shaped via tanh(1.2×x), mapped to 0–100
- Baseline = 72; delta = total − 72

### Category → Color (11_engine_categories.gs)
| Delta | Category | Color |
|-------|----------|-------|
| ≥14 | Noise | Pink |
| ≥7 | Prime | Orange |
| ≥4 | Sub-Prime | Blue |
| ≥2 | Edge | Yellow |
| ≥-4 | Survivor | Green |
| ≥-9 | Identity | Purple |
| ≥-13 | Growth | Green |
| ≥-15 | Variance/Stable Swing | Blue |
| ≥-29 | Unstable Swing | Red |
| ≥-40 | Luck | Brown |

### Golf Engine (GOLF_CFG)
- Exec base: 50 + resource/power/output/wealth stems − peer penalty − peak penalty
- Upside base: 50 + output/wealth stems + plateau bonus − extreme peak penalty
- Peak = peakiness of environment element distribution (0=flat, 1=extreme)
- Plateau bonus peaks at p=0.45–0.65, drops sharply above 0.65

### Conditions (14_engine_conditions.gs)
- Wind ≥25 mph, gusts ≥35, temp <40°F, precip ≥10mm = Tough (score≥6)
- Moderate = score 3–5; Calm = score 0–2

---

## Validated Betting Signals (as of 2026-03-28)

From 4D Element combo analysis. All are **Closing round** signals:

| Priority | Combo | Edge |
|----------|-------|------|
| PRIMARY | Calm × Closing × Purple × Fire | +4.6% |
| SECONDARY | Calm × Closing × Green × Earth | +5.9% (best stability) |
| TERTIARY | Moderate × Closing × Blue × Water | +5.5% |

See `FINAL_BETTING_SIGNALS.md` for full implementation guide.
Baseline win rate: 62.57%.

---

## Python Scripts (Root + engine/)

Key production scripts:
- `matchup_screener_v3.py` — Main screener with market-based edge + Kelly sizing
- `matchup_report_v3.py` — Report generator
- `player_scoring_system_v2.py` — Player scoring + shrinkage
- `phase_5_par_outcomes_optimized.py` — Par outcome model

Analysis scripts (engine/): `combo_analysis_4d_element.py` and variants —
run these to validate signals. Use DuckDB for aggregation queries.

---

## Conventions

- **IDs:** PLY_XXXX (players), EVT_XXXX (events), RES_XXXX (results), CALC_XXXX (calcs)
- **Engine version:** `golf_v{major}.{minor}` — update `ENGINE_VERSION` in `00_config.gs` when scoring logic changes
- **Memo cache:** `_MEMO` in `00_config.gs` caches within a single script execution. Not persisted. Safe to ignore.
- **Overnight run:** CHUNK_SIZE=200 rows, 1-minute trigger intervals, ~5.5 min safety window per chunk
- **Sheet name case:** match exactly — `"PLAYERS"`, `"EVENTS"`, `"Golf_Analytics"`, `"ANALYSIS"`, `"BIRTHDAY_VERIFY"`, `"RESULTS_RAW"`, `"COURSES"`, `"EVENTS_COURSES"`

---

## Work Log

Format for entries:
```
### YYYY-MM-DD — [title]
**Status:** Done / In Progress / Blocked
**What changed:** ...
**Why:** ...
**Next step:** ...
```

---

### 2026-04-04 — Build VALIDATED_INSIGHTS System (Math Proves Theory Framework)
**Status:** Done
**What changed:**
- Created `/VALIDATED_INSIGHTS/` folder structure with 5 confidence levels (LIVE_THEORY, NEEDS_TESTING, PARTIALLY_BACKED, VALIDATED, REJECTED)
- Built complete system for fusing intuitive/spiritual theory with mathematical validation
- Created 4 core documents:
  - `INDEX.md` — Central registry + how to use
  - `HOW_TO_ADD_INSIGHT.md` — 5-stage workflow (Live Theory → Design Test → Run Analysis → Approve Validation → Apply)
  - `RUBBER_STAMP_CHECKLIST.md` — 5 validation gates (statistical significance, sample size, effect size, stability, not luck) with flexible real-world scientific standards
  - `README.md` in each subfolder — Purpose + process for each level
- Created memory file: `VALIDATED_INSIGHTS_FOUNDATION.md` documenting system + user/Claude roles

**Why:** User explicitly requested: "Math proves theory" validation framework where insights pass both mathematical and theoretical gates. System needed flexible gates (not overly rigid), clear workflow, and separation of user's domain intuition from structural discipline.

**Key Design Decisions:**
- 5 gates are flexible by context (exploratory p<0.10 vs. primary p<0.05)
- Relative not absolute thresholds (different sample sizes for different analyses)
- Real-world scientific standards (accepted by math/statistics community)
- Claude enforces structure, user provides domain knowledge
- Rejected theories kept for learning (not deletion)

**How It Works:**
1. User submits theory → Claude creates LIVE_THEORY file
2. User approves test plan → Claude designs Python analysis
3. Claude runs test → fills RUBBER_STAMP_CHECKLIST with all 5 gate results
4. File moves to VALIDATED/PARTIALLY_BACKED/REJECTED based on results
5. VALIDATED insights feed into FINAL_BETTING_SIGNALS.md and player profiling

**Folder Structure Ready:**
```
/VALIDATED_INSIGHTS/
├── INDEX.md, HOW_TO_ADD_INSIGHT.md, RUBBER_STAMP_CHECKLIST.md
├── /LIVE_THEORY/ → /NEEDS_TESTING/ → /VALIDATED or /REJECTED or /PARTIALLY_BACKED
```

**Next step:** User submits first theory (e.g., "Purple players close stronger", "Personal Day 22 has a closing bonus"). Claude will create file, design test, run analysis, apply gates.

**Files created:**
- `/VALIDATED_INSIGHTS/INDEX.md`
- `/VALIDATED_INSIGHTS/HOW_TO_ADD_INSIGHT.md`
- `/VALIDATED_INSIGHTS/RUBBER_STAMP_CHECKLIST.md`
- `/VALIDATED_INSIGHTS/LIVE_THEORY/README.md`
- `/VALIDATED_INSIGHTS/NEEDS_TESTING/README.md`
- `/VALIDATED_INSIGHTS/PARTIALLY_BACKED/README.md`
- `/VALIDATED_INSIGHTS/VALIDATED/README.md`
- `/VALIDATED_INSIGHTS/REJECTED/README.md`
- Memory: `VALIDATED_INSIGHTS_FOUNDATION.md`

---

### 2026-03-31 — Fix System Testing Scripts: Save ALL Combos (Not Just Positive)
**Status:** Done
**What changed:**
- Fixed `system2_exec_upside_gap_testing.py`: Now saves `system2_exec_upside_gap_ALL_combos.csv` (all tested combos, not filtered)
- Fixed `system3_moon_lifepath_testing.py`: Now saves `system3_moon_lifepath_ALL_combos.csv` (all tested combos, not filtered)
- Fixed `system4_tithi_zodiac_testing.py`: Now saves `system4_tithi_zodiac_ALL_combos.csv` (all tested combos, not filtered)
- All three now report realistic distributions: positive%, negative%, zero% ROI (not 100% positive)
- Each system also saves `*_positive_only.csv` backup for reference
- Updated reporting to show: total combos, positive count/%, negative count/%, zero count/%, mean ROI across all

**Why:** Root cause of "100% positive ROI" bug was filtering on save: `positive.to_csv()` instead of `df_combos.to_csv()`. System 3 tested 882 combos but saved only 336 positive ones, hiding 502 negative combos (56.9%). This made all systems appear universally positive (100%), which is statistically impossible.

**Impact:** Now have accurate data for building consensus scorer. Realistic distributions expected: 30-60% positive across systems (varies by signal quality).

**Next step:** User runs all 3 systems, then runs `build_ensemble_consensus.py` to combine into consensus scorer

**Files created:**
- `SYSTEM_TESTING_FIXES.md` — Detailed explanation of problem + solution
- `ENSEMBLE_CONSENSUS_SCORER.md` — Architecture for 4-system ensemble combiner
- `build_ensemble_consensus.py` — Script to build consensus scorecard
- `NEXT_STEPS_SYSTEM_TESTING.md` — Checklist for user to complete analysis

---

### 2026-03-30 — Engine Audit & Cleanup
**Status:** Done
**What changed:**
- `02_runner_overnight.gs`: hoisted `startRow` above try block so catch can reference it without ReferenceError
- `00_config.gs`: fixed `BIRTHDAY_VERIFY.SHEET` from `"VERIFICATION"` to `"BIRTHDAY_VERIFY"` (was silently failing)
- `00_config.gs`: removed duplicate `COL_START_TIME = 11` (same as `COL_COURSE_ID`); flagged col 11 for verification
- `00_config.gs`: deprecated `COL_WS_D1–D4`; added comments clarifying `COL_COND_R1–R4` owns those columns now
- `97_import_results_raw.gs`: fixed `getRange(..., 200)` → `getRange(..., 9)` (reads only needed columns)
- `12_engine_golf.gs`: added comment explaining intentional plateau bonus drop above peak=0.65
- `06_lookup_events.gs`: updated `start_time` field to use `COL_COURSE_ID` (col 11) with a verify comment

**Why:** Audit found 2 bugs (startRow scope, sheet name mismatch) + 4 config/perf issues.

### 2026-03-30 — Golf_Analytics column audit & full column map
**Status:** Done
**What changed:**
- `00_config.gs` GA block: `COL_COND_R1–R4` corrected from 44–47 → 43–46 (AQ–AT). Was reading conditions from the wrong column (shifted by 1).
- `00_config.gs` GA block: Added 28 missing reference column constants (AI–BN): Course Avg, vs Avg, Round Type, Moon, Wu Xing, Zodiac, Destiny Card, Horoscope, MoonWest, Life Path, Tithi, GAP, Round Withdrawn.
- `CLAUDE.md` Golf_Analytics table: rebuilt with verified col numbers for all 66 columns.
**Why:** Actual sheet has conditions at AQ–AT (cols 43–46); config said AR–AU (44–47). Off by 1.

### 2026-03-30 — Add Tour column (BO) to Golf_Analytics
**Status:** Done
**What changed:**
- Added `COL_TOUR: 67` (BO) to GA config in `00_config.gs`
- Column pulls tour name from EVENTS sheet (PGA Tour, LIV Golf, DP World Tour, etc.)
- Updated CLAUDE.md Golf_Analytics table to include Tour column
**Why:** Need to track which tour each tournament is part of for future analysis bucketing by tour
**Next step:** Later — separate analysis by tour when LIV + DP World data is imported + integrated. Flag: some signals may be tour-specific (PGA vs LIV vs DP World Tour dynamics differ).

### 2026-03-30 — Add "Start Overnight from Row X" menu item
**Status:** Done
**What changed:**
- Added menu item: "🌙 Start Overnight from Row X" in `01_menu.gs`
- New function `START_OVERNIGHT_FROM_ROW()` prompts user for starting row
- Sets `PROP_PROGRESS` to that row before triggering overnight run
- Skips scanning rows 2–X-1, goes straight to new data
**Why:** Large sheets (24,000+ rows) were scanning every row to find blanks. User can now jump directly to new data (e.g., row 24,658) and skip overhead.
**How:** Menu → "🌙 Start Overnight from Row X" → enter row number → run
**Validation:** Checks that row ≥ GA.START_ROW (2), otherwise alerts error

### 2026-03-30 — Bug fix: preserve custom start row (don't reset to 2)
**Status:** Done
**Bug:** `_startOvernightRun_()` was unconditionally resetting PROP_PROGRESS to row 2, overwriting the custom row set by `START_OVERNIGHT_FROM_ROW()`.
**Fix:**
- Modified `_startOvernightRun_(force, doColors, doScores, resetProgress = true)` to accept optional `resetProgress` parameter
- If `resetProgress = false`, progress row is preserved (used by START_OVERNIGHT_FROM_ROW)
- If `resetProgress = true` (default), progress resets to row 2 (used by START_OVERNIGHT)
- Updated `START_OVERNIGHT_FROM_ROW()` to call `_startOvernightRun_(..., false)` after setting custom row
**Verification:** Overnight Status should now show correct starting row (e.g., 24658, not 2)
**Commit:** `d4e9964`

### 2026-03-30 — Config Audit: EVENTS, PLAYERS, COURSES, EVENTS_COURSES sheets
**Status:** Done — config updated
**Findings:**
- **PLAYERS:** ✓ All 16 columns match config perfectly
- **COURSES:** ✓ All 4 columns match config perfectly
- **EVENTS_COURSES:** ✓ Found 1 extra column (COL_STATUS at col 7) — added to config
- **EVENTS:** ✓ Fixed COL_START_TIME (col 11, not COL_COURSE_ID) + added 12 missing average columns (cols 47–58: R1–R4 avg_calm/avg_mod/avg_tou)
**Changes:**
- `00_config.gs` EVENTS: Changed col 11 from COL_COURSE_ID → COL_START_TIME; added COL_R1–R4_AVG_CALM (47–50), COL_R1–R4_AVG_MOD (51–54), COL_R1–R4_AVG_TOU (55–58)
- `00_config.gs` EVENTS_COURSES: Added COL_STATUS (7)
- `06_lookup_events.gs`: Updated start_time field to use COL_START_TIME instead of COL_COURSE_ID
**Next:** ANALYSIS sheet config audit (already verified earlier to be correct)

### 2026-03-30 — Debug & verify "Start Overnight from Row X" functionality
**Status:** Done
**Finding:** Feature is working correctly. Issue was not a bug but missing data.
**What happened:**
- User reported "Start Overnight from Row X" was resetting to row 2 instead of keeping custom row
- Added debug logging to trace the issue
- Execution logs showed: DEBUG logs confirmed `resetProgress=false` was working, PROP_PROGRESS was set to 24658 and preserved
- Root cause: New rows (24658+) had missing/invalid birthday data (columns K, L blank or "N/A")
- Engine correctly skipped those rows and logged "missing required input"
**Resolution:**
- Removed debug logging (cleanup)
- Feature is production-ready
- User must fill columns K (Birthday) + L (GMT offset) for new rows before engine can fill colors/scores
**Commit:** cleanup pushed

### 2026-03-31 — TOUR_STATS builder + ANALYSIS v3 tournament type
**Status:** Done
**What changed:**
- Added `BUILD_TOUR_STATS()` function to `10_analysis_baseline.gs` — calculates Calm/Moderate/Tough averages from ANALYSIS v3 off_par (AC) column
- Added "📊 Build TOUR_STATS" menu item under ANALYSIS v3 submenu
- Updated AG (adj_his_par) formula documentation to clarify TOUR_STATS dependency
- Added AH (tournament_type) column to ANALYSIS v3 (indexes T/P/M tournaments for exclusion)
- Updated AC (off_par) formula to exclude non-stroke-play tournaments: `=IF(OR(AH2="T",AH2="P",AH2="M"),"",G2-H2)`

**Why:** TOUR_STATS was static; now automatically rebuilds from current ANALYSIS data. Tournament type flagging ensures off_par calculations only use comparable stroke-play data.

**How to use:**
1. Populate ANALYSIS v3 completely (run "➕ Add Formulas")
2. Menu → 📊 ANALYSIS v3 → "📊 Build TOUR_STATS"
3. TOUR_STATS sheet updates with Calm/Moderate/Tough averages
4. AG formula (adj_his_par) now uses current tour stats

**Next step:** K-value optimization for AG shrinkage parameter (currently 50).

---

### 2026-03-31 — K-Optimization Analysis (Statistical Method)
**Status:** Done
**What changed:**
- Created `k_optimization_statistical_analysis.py` — analyzes how k values (10–100) affect adj_his_par distribution
- Method: Statistical sensitivity analysis (variance, skewness, range, distribution shape)
- Uses 2025-2026 test data without match outcomes

**Why this method:**
- No match outcomes available yet (cannot measure prediction accuracy)
- Analyzes statistical properties instead
- Provides guidance on k choice: minimum variance, normalized distribution, domain intuition

**LIMITATION (flagged for future work):**
- This is NOT validation of prediction accuracy
- Cannot measure ROI or win rate without ground truth
- When match outcomes become available (2025-2026 results), upgrade to Option A: true backtesting

**How to use:**
1. Export ANALYSIS v3 as CSV (`ANALYSIS_v3_export.csv`)
2. Run: `python k_optimization_statistical_analysis.py`
3. Output: `k_optimization_report.json` with distribution stats per k value
4. Choose k based on: minimum variance, minimum skewness, domain intuition

**Future optimization (Option A):**
- Blocked on: Match outcome data collection
- When available: Backtest each k against actual results, measure win rate + ROI
- Will be much more accurate than current statistical analysis

**Owner:** TBD
**Priority:** High (revisit when 2025-2026 match results are available)

---

### 2026-03-31 — K-Optimization Validated via Leave-One-Out CV
**Status:** Done
**What changed:**
- Ran Leave-One-Out Cross-Validation on 2022-2024 training data (73,364 prediction tests)
- Tested k values 10–100
- Found: **K=10 minimizes prediction error** (MAE=2.5892, 0.7% better than current K=50)
- Interpretation: Player history more predictive than tour average for this dataset

**Key Results:**
- Best K by MAE: K=10 (2.5892)
- Best K by RMSE: K=10 (3.5098)
- Best K by Median: K=20 (2.1076)
- Current (K=50): MAE=2.6070
- Improvement: 0.7% error reduction

**Data Breakdown:**
- Calm: 42,724 rounds (avg off_par -0.986)
- Moderate: 28,320 rounds (avg off_par -0.334)
- Tough: 2,320 rounds (avg off_par -0.191)

**Why this validates K choice:**
- LOO CV tests actual prediction accuracy
- No match outcomes needed (cross-validation is ground truth)
- 73K+ test cases provides statistical significance
- K=10 consistently best across MAE, RMSE, median error

**Next step:** Update AG formula from K=50 to K=10 in engine, push to Google Apps Script

**Blocking:** None (ready to implement)
**Owner:** Claude (can do now)
**Priority:** High

---

### 2026-04-02 — Personal Year Tournament Winner Analysis
**Status:** Done
**What changed:**
- Created `analyze_tournament_winners_personal_year.py` — analyzes Personal Year distribution in tournament top-10 finishers across 64 PGA tournaments
- Analyzed 77,155 golf rounds, identified 636 top-10 finisher slots (10 per tournament × 64 events)
- Found: **Personal Year 7 is statistically significant** (χ² p < 0.05, 14.8% vs 11.1% baseline, +32.5% excess)

**Key Findings:**
- **Tier 1 (Boost):** Year 7 (+30%, 94 finishers, 14.8%) | Year 9 (+15%, 84 finishers, 13.2%)
- **Tier 2 (Baseline):** Years 1, 5, 6, 8 (near 11.1% baseline)
- **Tier 3 (Penalty):** Year 2 (-15%, 55 finishers, 8.6%) | Year 3 (-20%, 53 finishers, 8.3%)
- **Special:** Year 4 has best quality (-14.18 off-par) but lowest frequency (9.9%)

**Why:** Tournament winners show non-random Personal Year distribution. Year 7 players win ~32.5% more often than expected by chance. Year 3 players win ~32.5% less often.

**Integration:** Updated BETTING_FRAMEWORK_2BALL.md to add "BONUS TIER: PERSONAL YEAR TOURNAMENT SIGNALS" with 3-tier weighting system for 2-ball matchups.

**Files Generated:**
- `analyze_tournament_winners_personal_year.py` (reusable script)
- `PERSONAL_YEAR_TOURNAMENT_ANALYSIS.md` (full technical report)
- `PERSONAL_YEAR_QUICK_REFERENCE.txt` (summary + deployment guide)
- `INDEX_PERSONAL_YEAR_ANALYSIS.md` (navigation)

**Next step:** Validate Year 7 signal on 2025-2026 tournaments (out-of-sample test). Consider testing Year 7 + other signals (Calm × Year 7, Element + Year 7 combos) for enhancement.

**Priority:** Medium (signal is strong but needs out-of-sample validation before live deployment)

---

**Open item:** Verify whether `start_time` truly lives in col K of EVENTS, or if it has moved.
If it has its own column, add `COL_START_TIME: <correct_col>` back to `00_config.gs` EVENTS block
and update `06_lookup_events.gs` accordingly.

---

## 🚩 Flagged for Later (Known Future Work)

These are not blocking current work but need to be addressed before the next major phase:

### Tour-Based Bucketing
**When:** After LIV Golf + DP World Tour data is imported and integrated (non-blocking)
**What:** Separate combo analysis by tour. PGA Tour, LIV Golf, and DP World Tour have different field compositions, formats, and dynamics.
**Why:** A signal valid for PGA Tour (e.g., "Calm + Purple" = +4.6%) may not hold for LIV (smaller field, different players). Need tour-stratified signals.
**How:** Filter ANALYSIS sheet by COL_TOUR before running combo scripts. Generate separate FINAL_BETTING_SIGNALS_BY_TOUR.md.
**Owner:** TBD
**Priority:** Medium (after core PGA signals are validated)

### `start_time` Column Resolution
**What:** Column K (EVENTS sheet) is ambiguous — assigned to both COL_COURSE_ID and COL_START_TIME.
**Why:** Config has a note flagging this for verification.
**How:** Check actual EVENTS sheet layout; if start_time has its own column, update `00_config.gs` EVENTS block + `06_lookup_events.gs`.
**Owner:** TBD
**Priority:** Low (not used in current analysis)

---

---

## Documentation Map

All project documents and their purposes:

| Document | Purpose |
|----------|---------|
| **[CLAUDE.md](CLAUDE.md)** | You are here. Project overview, architecture, core principles. |
| **[GOLF_ANALYTICS_DATA_DICTIONARY.md](GOLF_ANALYTICS_DATA_DICTIONARY.md)** | Reference for all 67 columns in Golf_Analytics (A–BO): purpose, type, source, validation, examples. |
| **[00_config.gs](engine/00_config.gs)** | Canonical constants + column mappings. Single source of truth for sheet layout. |
| **[DATA_INTAKE_CHECKLIST.md](DATA_INTAKE_CHECKLIST.md)** | Process for flagging + validating new tournament imports (Layer 1 of audit). |
| **[AUDIT_FRAMEWORK.md](AUDIT_FRAMEWORK.md)** | Complete 5-layer verification system: import → formula → derivation → analysis → betting. |
| **[FINAL_BETTING_SIGNALS.md](FINAL_BETTING_SIGNALS.md)** | Validated signals ready for live betting. Includes confidence intervals + deployment rules. |

---

## How to Resume Work (for Claude or human)

**Start here before touching anything:**

1. Read **this file** (CLAUDE.md) — architecture overview + current state
2. Read **[GOLF_ANALYTICS_DATA_DICTIONARY.md](GOLF_ANALYTICS_DATA_DICTIONARY.md)** to understand columns
3. Read **[AUDIT_FRAMEWORK.md](AUDIT_FRAMEWORK.md)** if you're changing data or logic
4. Read **[DATA_INTAKE_CHECKLIST.md](DATA_INTAKE_CHECKLIST.md)** if new tournament data is arriving
5. Check the Work Log section above for open items and recent context

**When making changes:**

- For engine changes: identify which layer (pure engine vs writer vs config) before editing
- Never put logic in `00_config.gs`. Never put Sheets access in `10_`–`14_` files
- After any scoring formula change, bump `ENGINE_VERSION` in `00_config.gs`
- After changes, run `TEST_SINGLE_ROW` from the menu to validate a single row end-to-end
- **Before committing:** Use the Standard Audit Checklist in AUDIT_FRAMEWORK.md
- **After completing:** Log your work in the Work Log section below with what/why/next-step format

**Never silent changes.** Everything gets logged, audited, and documented in plain language.
