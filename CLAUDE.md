# Luckify Me — Project Reference for Claude

This file is auto-loaded at the start of every Claude Code session.
It is the single source of truth for the engine, sheet layout, conventions, and active work.

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
| AP–AS | COL_R1_AVG–R4_AVG | Field averages per round |
| AT | COL_YEAR | Year |

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
| AI–AL | 35–38 | COL_COURSE_AVG_R1–R4 | Field avg per round |
| AM–AP | 39–42 | COL_VS_AVG_R1–R4 | Score − course avg ("vs Avg") |
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

### ANALYSIS (cols A–O)
One row per round played. Source for all Python combo analysis.
| Col | Content |
|-----|---------|
| A | player_id |
| B | player_name |
| C | event_id |
| D | event_name |
| E | round_num (1–4) |
| F | score (actual strokes) |
| G | par |
| H | course_avg (field avg for that round) |
| I | diff_course_avg (score − course_avg = "vs Avg") |
| J | condition (Calm/Moderate/Tough) |
| K | color (Purple/Blue/Green/Yellow/Red/etc) |
| L | exec (0–100) |
| M | upside (0–100) |
| N | player_hist_par (player's historical avg vs par) |
| O | diff_player_hist_par |

**vs Avg definition:** score vs venue field average for that round — NOT vs par.

### RESULTS_RAW (cols A–K)
Raw scores by player + event. Used for ID-linked imports.

### Other Sheets
- `COURSES` — Course registry (course_id, name, location)
- `EVENTS_COURSES` — Event+course+year+par junction table
- `BIRTHDAY_VERIFY` — ESPN/Wikidata birthday verification results
- `RUN_LOGS` — Engine run history (timestamp, version, rows, duration, status)
- `ENGINE_SETTINGS` — Active engine version

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
