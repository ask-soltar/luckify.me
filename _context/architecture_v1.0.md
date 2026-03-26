# LUCKIFY ME — Master Architecture Document

**Version 1.0 | Phase 1 Foundation**

*Confidential — Preston Lee / Soltar Systems*

---

This document is the single source of truth for the Luckify Me engine system. Every architectural decision, naming convention, data model, and build sequence lives here. Nothing gets built without it being represented here first.

## 1. Purpose & Scope

This document defines the complete foundation for the Luckify Me engine system — from the current Google Sheets implementation through to a scalable multi-domain platform serving every human on earth.

**What this document governs:**
- The architecture of the Apps Script codebase (Phase 1)
- The data model — entities, IDs, relationships, schema
- The engine layer — structure, versioning, domain extensibility
- The build sequence — what gets built, in what order, and why
- The migration path — from Sheets to a real backend
- Naming conventions — consistent across code, sheets, and future database

The engine is not a golf tool. Golf is the first domain. The engine computes timing and luck alignment for any human, across any domain, using BaZi as the primary signal system — extensible to any system that produces elemental or energetic signals.

## 2. Vision & Product Trajectory

Luckify Me is being built to be the canonical platform at the intersection of luck, timing, data science, and spirituality. The engine behind it — which computes personal energetic alignment against environmental conditions — is the core IP.

### 2.1 Product Forms at Scale
- **Consumer app** — anyone enters their birthday and gets domain-specific luck scores
- **B2B tool** — sports organisations, betting companies, and professional teams license the engine
- **API** — developers build products on top of the luck scoring layer
- **Subscription data product** — think Bloomberg for timing intelligence

### 2.2 Domains Roadmap

| Item | Detail |
|------|--------|
| Golf (current) | Exec / Upside / Peak scores per round |
| Sports betting | Timing alignment for bet placement decisions |
| Poker | Session timing, variance prediction, decision windows |
| Daily luck | Consumer-facing personal alignment scores by day |
| Business timing | Launch windows, negotiation timing, key decisions |
| Relationships | Compatibility and timing between two people |
| Horse racing | Per-race alignment for horse + jockey combinations |
| Trading / markets | Entry/exit timing alignment |

Every domain uses the same engine core. What changes is the scoring model layered on top — which elemental relationships matter, what the output labels mean, and how the scores map to decisions in that domain.

## 3. Current State Assessment

### 3.1 What Exists
- One Google Apps Script file (~1000 lines) doing everything
- Three logical datasets mixed into one or two sheets: players (birthday data), events (round dates / venue), results + engine outputs (golf analytics)
- Working engine: BaZi core, Lucky Day delta, color/category logic, golf scoring model (Exec / Upside / Peak)
- Overnight batch runner with trigger management
- No version control — working directly in Apps Script editor
- No entity IDs — players and events identified by name only

### 3.2 Core Problems Being Fixed

| Item | Detail |
|------|--------|
| One giant script | Hard to maintain, impossible to hand off, no separation of concerns |
| One giant sheet | Data, logic, and output are mixed — breaks when one changes |
| No IDs | Renaming a player or event breaks everything silently |
| No versioning | Cannot reproduce a past result or know what changed |
| No audit trail | No record of what was run, when, or with which engine version |
| Mixed responsibilities | Engine logic, UI logic, and data access are entangled |

## 4. Architecture

### 4.1 Four-Layer Model

Every component of this system belongs to exactly one of four layers. This is not optional — it is the structural rule that makes everything else work.

| Item | Detail |
|------|--------|
| ENGINE | Pure logic. No Sheets access. No UI. Deterministic. Given the same inputs, always produces the same outputs. This is the IP. |
| ORCHESTRATION | Coordinates batch runs, triggers, retries, and progress tracking. Talks to both Sheets and the Engine. |
| DATA | Reads from and writes to Sheets. Handles lookups, IDs, and data integrity. |
| INTERFACE | Menus, alerts, user-facing feedback. Currently Google Sheets. Eventually a web app or API. |

### 4.2 Layer Rules — Who Can Touch Sheets

| Module | Sheets Access | Responsibility |
|--------|---|---|
| Menu / Interface | YES | Shows menus, triggers actions, displays status alerts |
| Runner / Orch. | YES | Reads progress state, calls writers, manages triggers |
| Writer / Data | YES | Reads inputs from Sheets, writes outputs to Sheets |
| Engine | NO | Pure functions only. Zero Sheets dependency. Ever. |
| Utils | NO | Pure helper functions. Math, date, key formatting only. |

**Critical Rule:** The Engine layer must never import SpreadsheetApp or access any sheet. This is the single most important rule for long-term scalability — it is what makes the engine portable to any backend.

## 5. Module Structure (Apps Script Files)

The single script gets split into the following files. Zero logic changes in Phase 1 — this is purely structural reorganisation.

| Item | Detail |
|------|--------|
| 00_config.gs | All constants: sheet names, column indices, engine config objects (GA, GOLF_CFG, LUCKY_CFG, etc.) |
| 01_menu.gs | onOpen() and all menu handler stubs (FILL_ALL, FORCE_RECOMPUTE, etc.) |
| 02_runner_overnight.gs | Overnight trigger management: START_OVERNIGHT, STOP, RESET, STATUS, OVERNIGHT_CHUNK, _processChunk_ |
| 03_writer_golf_analytics.gs | _fillSheet_, _fillRow_, _buildOutputRow_, _processChunk_ write path, _hasRequiredInputs_, _needsColor_, _needsScores_ |
| 04_best_round.gs | FILL_BEST_ROUND — isolated because it will expand per domain |
| 05_lookup_players.gs | Player data access layer — reads Birthday sheet, returns player objects by ID or name |
| 06_lookup_events.gs | Event data access layer — reads event_data sheet, returns event objects by ID |
| 10_engine_lucky_day.gs | LUCKY_DAY_DELTA, _luckyDayDeltaFromWindow_, _personEnvScore_, _cachedPersonEnvScore_ |
| 11_engine_categories.gs | LUCKY_CATEGORY_ALT_FROM_DELTA, _categoryFromDeltaAlt_, LUCKY_CATEGORY_COLOR, LUCKY_DELTA_COLOR |
| 12_engine_golf.gs | GOLF_LUCK_SCORES_NO_BIRTH_TIME, _GOLF_envBlend_, _GOLF_scoreDual_, _GOLF_hiddenMult_, _GOLF_plateauBonus_, labels. Accepts optional conditions modifier when CONDITIONS layer is present. |
| 13_engine_bazi_core.gs | All BaZi primitives: BAZI_FULL_PILLARS, BAZI_DAY_STEM_OBJ, BAZI_DAY_BRANCH_OBJ, _sexagenaryDayNumbers_, solar longitude, seasonal multipliers, element accumulators |
| 14_engine_conditions.gs | CONDITIONS_CALCULATE_ (pure scoring: wind/gusts/precip/temp → Calm/Moderate/Tough). Zero API calls. Zero Sheets access. Input: a data object. Output: a string label + numeric severity score. |
| 07_fetcher_conditions.gs | All Open-Meteo API calls: CONDITIONS_FETCH_ARCHIVE_, CONDITIONS_FETCH_FORECAST_BATCH_, cache layer, rate-limit handling. Abstracted behind a clean interface so swapping to a paid API means changing this file only. |
| 08_writer_conditions.gs | CONDITIONS batch runner: CONDITIONS_PROCESS_BATCH_, CONDITIONS_FILL_ALL_REMAINING_, CONDITIONS_REFRESH_ROW_, trigger management, progress tracking. Writes Calm/Moderate/Tough to Event_Data AG:AJ. |
| 20_utils_dates.gs | _coerceDate_, _buildLocalDateTime_, localToUTC, _WD_buildLocalDT_, _WD_normTime_, jdFromDate, CONDITIONS_GET_LOCAL_DATE_STR_, CONDITIONS_GET_LOCAL_TODAY_ |
| 21_utils_elements_math.gs | _toVec01_, _dotRel_, _shape_, _entropy_, _peakiness_, _vecToPct_, _controllerOf_, _dominantEl_, element relationship helpers (_WD_wealthEl_ etc.) |
| 22_utils_keys.gs | _safeKey_ and any future ID / key generation utilities |
| 23_utils_general.gs | Miscellaneous shared utilities that don't fit elsewhere |
| 90_debug_tests.gs | TEST_SINGLE_ROW, DEBUG_ACTIVE_ROW, and all future test/debug functions |

**Module Rule:** If a function accesses SpreadsheetApp anywhere, it belongs in 03_, 04_, 05_, or 06_. If it is pure logic, it belongs in 10_–13_ or 20_–23_. When in doubt, ask: could this function run in a Node.js environment with no Google services? If yes — it is engine or utils.

### 4a. CONDITIONS Layer — Weather as Engine Input

CONDITIONS is not a display feature — it is an engine input. Weather conditions (wind, gusts, precipitation, temperature) affect the golf scoring model. Calm / Moderate / Tough modifies Exec and Upside scores. This makes the weather layer part of the engine pipeline, not just data enrichment.

#### Architecture Decision: Three-Part Separation

| Item | Detail |
|------|--------|
| 14_engine_conditions.gs | PURE LOGIC ONLY. CONDITIONS_CALCULATE_(data) takes a weather data object and returns a label + severity score. No API calls. No Sheets. Portable to any backend. This is the engine piece. |
| 07_fetcher_conditions.gs | API LAYER ONLY. All Open-Meteo calls live here — archive and forecast endpoints, caching, rate-limit handling. Abstracted so swapping to a paid API (e.g. Tomorrow.io, WeatherAPI) means changing this one file only. |
| 08_writer_conditions.gs | SHEETS LAYER ONLY. Batch runner, trigger management, progress tracking. Reads Event_Data, calls the fetcher, writes Calm/Moderate/Tough back to AG:AJ. |

#### Data Flow

| Item | Detail |
|------|--------|
| Step 1 | 08_writer_conditions.gs reads lat/lon/gmt/dates from Event_Data |
| Step 2 | Calls 07_fetcher_conditions.gs to get raw weather data (cached per location+date) |
| Step 3 | Calls 14_engine_conditions.gs CONDITIONS_CALCULATE_(data) — pure function, returns label |
| Step 4 | Writes result to Event_Data AG:AJ |
| Step 5 | Golf_Analytics reads the conditions label from Event_Data via VLOOKUP or direct reference |
| Step 6 | 12_engine_golf.gs accepts optional conditionsSeverity parameter — adjusts Exec/Upside accordingly |

**API swap rule:** when upgrading from Open-Meteo to a paid weather API, only 07_fetcher_conditions.gs changes. The engine (14_), writer (08_), and all golf scoring logic are completely untouched. This is why the fetcher is its own file.

#### CONDITIONS Score Thresholds (Current)

| Item | Detail |
|------|--------|
| Wind speed | 0–6 mph: +0 \| 7–11: +1 \| 12–17: +2 \| 18–24: +3 \| 25+: +4 |
| Gusts | Under 25: +0 \| 25–34: +1 \| 35+: +2 |
| Avg temp | 55–90°F: +0 \| 40–54°F: +1 \| Under 40°F: +2 \| Over 90°F: +1 |
| Precipitation | Under 3mm: +0 \| 3–9mm: +1 \| 10+mm: +2 |
| Labels | Total 0–2: Calm \| 3–5: Moderate \| 6+: Tough |

These thresholds are configurable constants — they will move into 00_config.gs as CONDITIONS_CFG.

## 6. Data Model

The system manages four core entity types. Each gets a stable unique ID. Names are display labels — IDs are the source of truth.

### 6.1 Players

Any person whose luck scores are being computed. Domain-agnostic — the same player record is used whether computing golf scores, poker timing, or daily luck.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| player_id | string | PLY_0001 | Stable unique ID. Never changes. Format: PLY_XXXX |
| name | string | Scottie Scheffler | Display name. Can be updated without breaking anything. |
| birthday | date | 1996-06-21 | Required for all engine calculations. |
| birth_gmt | number | -5 | GMT offset at time of birth. Not current timezone. |
| source | string | manual / scraped | How this record was created. |
| domain_tags | string[] | golf, poker | Which domains this player is active in. |
| notes | string | PGA Tour | Optional free text. |
| created_at | datetime | 2025-01-15 | Record creation timestamp. |

### 6.2 Events

A competition, session, or context window that has a date, location, and timezone. Domain-specific — a golf tournament and a poker series are both events.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| event_id | string | EVT_0001 | Stable unique ID. Format: EVT_XXXX |
| name | string | Masters 2025 | Display name. |
| domain | string | golf | Which domain this event belongs to. |
| year | number | 2025 | Year of the event. |
| venue | string | Augusta National | Venue name. |
| lat | number | 33.5031 | Latitude of venue. Required for CONDITIONS fetcher. |
| lon | number | -82.0197 | Longitude of venue. Required for CONDITIONS fetcher. |
| venue_gmt | number | -4 | GMT offset of the venue location. |
| round_dates | date[] | [2025-04-10, ...] | Array of round/session dates. Up to 4 for golf. |
| notes | string | | Optional. |
| created_at | datetime | 2025-01-15 | Record creation timestamp. |

### 6.3 Results

Actual performance data for a player at an event. Optional — engine calculations run without this. Required for backtesting and validation.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| result_id | string | RES_0001 | Stable unique ID. Format: RES_XXXX |
| player_id | string | PLY_0001 | Foreign key → Players |
| event_id | string | EVT_0001 | Foreign key → Events |
| scores | number[] | [68, 71, 69, 70] | Actual scores per round/session. |
| total | number | 278 | Total score or aggregate result. |
| status | string | CUT / WD / WON | Completion status. |
| created_at | datetime | 2025-01-15 | |

### 6.4 Calculations

Engine output for a specific player + event combination. This is the audit trail. Every run produces a record here.

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| calc_id | string | CALC_0001 | Stable unique ID. Format: CALC_XXXX |
| player_id | string | PLY_0001 | Foreign key → Players |
| event_id | string | EVT_0001 | Foreign key → Events |
| engine_version | string | golf_v1.0 | Which engine version produced this. Critical for reproducibility. |
| round_outputs | object[] | [{exec, upside, peak, color}] | Per-round engine outputs. |
| conditions | string[] | ['Calm','Tough','Moderate','Calm'] | Per-round CONDITIONS label at time of calculation. Snapshotted so changing weather data doesn't alter historical records. |
| run_timestamp | datetime | 2025-04-10T14:00Z | When this calculation was run. |
| inputs_snapshot | string | JSON blob | Snapshot of inputs used. Enables full reproducibility. |
| notes | string | | Optional. |

The inputs_snapshot field is the answer to the audit trail question. Even if you update a player's birthday or an event's date, you always know exactly what was fed into the engine for a given calc_id. This is what makes results reproducible forever.

## 7. Engine Versioning

Every engine output must be traceable to the exact version of logic that produced it. This is non-negotiable for a system where results must be reproducible forever.

### 7.1 Version Constant

Every engine module declares its version at the top of the file:

```
const ENGINE_VERSION = "golf_v1.0";
```

### 7.2 Version Naming Convention

| Item | Detail |
|------|--------|
| Format | {domain}_v{major}.{minor} |
| Example | golf_v1.0 / golf_v1.1 / poker_v1.0 |
| Major bump | Any change to scoring weights, thresholds, or model structure |
| Minor bump | Bug fixes, label changes, non-material tweaks |
| New domain | Always starts at v1.0 with its own prefix |

### 7.3 What Gets Logged Per Run

- engine_version — which version ran
- run_timestamp — when it ran
- inputs_snapshot — birthday, birthGMT, eventDate, venueGMT, teeoff time, boundary, preset
- outputs — exec, upside, peak, color per round
- rows_processed / errors — operational metadata

**Decision deferred:** whether every individual row calculation gets its own calc record, or just each batch run gets a summary log. Revisit this in Phase 2 when RUN_LOGS sheet is introduced.

## 8. Google Sheets Structure

Sheets are the interface layer only — not the system. The goal is clean separation: one sheet per entity type, no mixed responsibilities.

| Item | Detail |
|------|--------|
| PLAYERS | Canonical player registry. player_id, name, birthday, birth_gmt, domain_tags. One row per player. Never delete — archive instead. |
| EVENTS | Canonical event registry. event_id, name, domain, year, venue, venue_gmt, round dates. One row per event. |
| GOLF_ANALYTICS | Current working sheet. Will be refactored to be purely an output/analysis view — not a data store. Inputs read from PLAYERS + EVENTS. |
| RESULTS_RAW | Actual performance data. Populated manually or by import. Optional per row. |
| RUN_LOGS | (Phase 2) Operational log of every batch run: start time, end time, rows processed, engine version, errors. |
| ENGINE_SETTINGS | (Phase 2) Active engine version, feature flags, notes. Single-row config sheet. |
| ARCHIVE | Soft-deleted records. Never hard-delete anything. |

**Multi-domain decision (currently open):** whether poker players and golf players share the PLAYERS sheet (recommended — same engine core) or get separate sheets. Default recommendation: one PLAYERS sheet with a domain_tags column. Revisit when poker is being actively built.

## 9. Engine Extensibility

The BaZi core is the signal source. Domain-specific scoring models are layered on top. Adding a new domain means adding a new engine file — not modifying the core.

### 9.1 Signal System Design

| Item | Detail |
|------|--------|
| Primary system | BaZi — the current engine. Produces elemental alignment scores between a person's natal chart and the environmental day/year pillars. |
| Secondary systems | Architecture supports any system that can produce a signal vector (5-element or otherwise): Western astrology, numerology, human design, etc. |
| Extensibility rule | New signal systems plug in at the env-blend layer. They do not modify BaZi core functions. |
| Output format | All signal systems must produce a normalised vector that can be scored against the person's natal profile. |

### 9.2 Adding a New Domain (Pattern)

1. Create 12_engine_{domain}.gs — e.g. 12_engine_poker.gs
2. Define domain-specific config constants at the top (equivalent to GOLF_CFG)
3. Implement the main scoring function: {DOMAIN}_LUCK_SCORES_NO_BIRTH_TIME(...)
4. Define output labels relevant to the domain
5. Add a writer file: 03_writer_{domain}_analytics.gs
6. Add menu items in 01_menu.gs
7. Register the new engine version constant

The BaZi core, Lucky Day delta, and all utils are shared across all domains. Zero duplication.

## 10. Build Sequence

Phases are sequenced so each one produces a working, stable system before the next begins. No phase starts until the previous one is solid.

| Phase | What | Deliverable | Gate |
|-------|------|-------------|------|
| P1 | Split the single Apps Script into the module structure defined in Section 5. Zero logic changes. Pure reorganisation. | 10 .gs files. System runs identically to before. | All existing outputs match pre-split outputs exactly. |
| P2 | Add ENGINE_VERSION constant. Add entity IDs to PLAYERS and EVENTS sheets. Add player_id and event_id columns to GOLF_ANALYTICS. | Versioned engine. ID-referenced data. | Every row in GOLF_ANALYTICS has a valid player_id and event_id. |
| P3 | Add RUN_LOGS sheet. Add ENGINE_SETTINGS sheet. Log engine version + timestamp on every overnight run. | Operational audit trail begins. | Can answer: what version ran on date X? |
| P4 | Introduce RESULTS_RAW sheet. Begin separating actual scores from engine outputs in GOLF_ANALYTICS. | Clean entity separation. | No raw scores stored in the same columns as engine outputs. |
| P5 | Set up Git version control via clasp (Google Apps Script CLI). Push all .gs files to a GitHub repo. | Code is versioned. Safe to experiment. | First commit includes all Phase 1–4 work. |
| P6 | Build poker engine module (12_engine_poker.gs). Add POKER_ANALYTICS sheet. | Second domain live. | Poker scores computable for any player with birthday on any session date. |
| P7 | Define Postgres database schema. No build yet — just the written spec. | Migration blueprint ready. | Schema doc reviewed and signed off. |
| P8 | Migrate engine layer to Node.js / TypeScript. Sheets becomes admin UI only. | Backend engine running independently of Sheets. | API endpoint returns luck scores for any birthday + date combination. |

## 11. Naming Conventions

Consistent naming across Sheets, Apps Script, and future database. These are permanent — changing them later is expensive.

| Item | Detail |
|------|--------|
| Entity IDs | PLY_XXXX (players), EVT_XXXX (events), RES_XXXX (results), CALC_XXXX (calculations). Zero-padded to 4 digits. |
| Sheet names | ALL_CAPS_UNDERSCORED. PLAYERS, EVENTS, GOLF_ANALYTICS, RUN_LOGS, ENGINE_SETTINGS. |
| Apps Script files | NN_layer_description.gs — two-digit prefix determines load order and layer. |
| Engine functions | UPPER_SNAKE_CASE for public API: LUCKY_DAY_DELTA, GOLF_LUCK_SCORES_NO_BIRTH_TIME. _lower_snake_case_ with leading/trailing underscores for private helpers. |
| Config objects | ALL_CAPS short name: GA (Golf Analytics config), GOLF_CFG, LUCKY_CFG, POKER_CFG. |
| Engine versions | {domain}_v{major}.{minor} — e.g. golf_v1.0, poker_v1.0, lucky_day_v2.1. |
| Column constants | COL_{NAME} — e.g. COL_BIRTHDAY, COL_VENUE_GMT. Never use magic numbers in logic. |
| Property keys | GA_{PURPOSE} — e.g. GA_OVERNIGHT_ROW, GA_OVERNIGHT_FORCE. Namespace all script properties. |
| Domain tags | lowercase singular: golf, poker, betting, daily, business, relationships. |
| Future DB tables | lowercase_underscored plural: players, events, results, calculations, engine_versions, run_logs. |

## 12. Future Migration Path

Sheets is the interface for now. The engine is being built to migrate cleanly. This section is a map — not a commitment.

| Item | Detail |
|------|--------|
| Target stack | Postgres (database) + Supabase (hosted) + Prisma (schema/migrations) + Node.js / TypeScript (engine layer) |
| Migration trigger | When Sheets becomes the bottleneck — either in volume, multi-user needs, or latency. |
| What migrates | Engine layer (10_–13_ files) ports directly to TypeScript with minimal changes. Data migrates from Sheets to Postgres. Sheets becomes read-only admin view or is replaced by a web UI. |
| What stays | The BaZi math, the scoring models, the config objects. These are permanent IP. |
| Preparation now | Clean module boundaries, entity IDs, engine versioning, input snapshots. These are the migration prerequisites. |

The reason to do Phase 1–5 carefully is exactly this: a clean, modular, ID-referenced, versioned system migrates to a backend in days. A tangled spreadsheet migrates in months — if ever.

## 13. Open Decisions & Decision Log

Decisions made, and decisions still open. This section gets updated as calls are made.

### 13.1 Decisions Made

| Item | Detail |
|------|--------|
| Phase 1 scope | Clean module split only. Zero logic changes. |
| Audit requirement | Results must be reproducible forever. Inputs snapshot required on all calculations. |
| Engine signal systems | BaZi primary. Architecture open to additional signal systems. They plug in at the env-blend layer. |
| Output model | Domain-specific scores. Consumer sees scores relevant to their context, not a generic luck number. |
| Interface (current) | Google Sheets only. No web app until Phase 8. |
| Version control | Git via clasp. Introduced in Phase 5. |
| ID format | PLY_XXXX, EVT_XXXX, RES_XXXX, CALC_XXXX. |

### 13.2 Open Decisions

| Item | Detail |
|------|--------|
| Weather API upgrade | Open-Meteo is the current fetcher. Plan to upgrade to a paid API (Tomorrow.io or similar) for higher reliability and more data points. Only 07_fetcher_conditions.gs changes when this happens. |
| CONDITIONS → engine coupling | Currently: Calm/Moderate/Tough label is fetched separately from golf scoring. Future: 12_engine_golf.gs accepts conditionsSeverity as a parameter and applies it directly to Exec/Upside. Wiring up this connection is a Phase 2 task. |
| Multi-domain data model | Do poker players and golf players share one PLAYERS sheet? Default: yes (domain_tags column). Revisit at Phase 6. |
| Calc-level audit granularity | Does every individual row get a CALC record, or just each batch run? Revisit at Phase 3. |
| inputs_snapshot storage | JSON blob in a hidden sheet column, or a dedicated CALCULATIONS sheet? Decision due at Phase 2. |
| env_peak visibility | Currently baked into scores. Show in debug only, or surface in output? Decision due at Phase 2. |

## 14. Standing Rules

These are non-negotiable. They do not get overridden to ship faster.

- The engine layer never touches SpreadsheetApp. Ever.
- The fetcher layer (07_) never touches the engine layer directly — it only returns data objects.
- Swapping the weather API means changing 07_fetcher_conditions.gs only. Nothing else.
- Every output is traceable to an engine version and an inputs snapshot.
- Entity IDs are never recycled. If a record is deleted, its ID is retired.
- Never hard-delete data. Archive it.
- Column indices are always referenced by named constants. No magic numbers.
- New domains always start as a new engine file. The existing engine files are not modified to accommodate them.
- Phase N does not start until Phase N-1 outputs are stable and tested.
- This document is updated before code is written — not after.

The architecture exists to serve the vision: a system that every human on earth can use to understand their timing. Every decision made here is in service of that destination.

---

**Luckify Me | Master Architecture Document | Version 1.0 | Confidential**
