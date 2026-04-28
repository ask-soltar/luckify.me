/****************************************************
 * 00_config.gs
 * LUCKIFY ME — Global Constants & Configuration
 *
 * RULE: This file contains ONLY constants and config objects.
 *       No functions. No logic. No Sheets access.
 *       Every other module reads from here.
 *
 * ENGINE VERSION: golf_v1.0
 ****************************************************/

/* =========================
   ENGINE VERSION
   Update this any time the scoring logic changes.
   Format: {domain}_v{major}.{minor}
========================= */

const ENGINE_VERSION = "golf_v1.0";

const SHEET_PLAYERS = "PLAYERS";
const SHEET_EVENTS  = "EVENTS";
const SHEET_GOLF    = "Golf_Analytics";
const SHEET_RESULTS = "RESULTS_RAW";
const SHEET_BIRTHDAY_VERIFY = "BIRTHDAY_VERIFY";

const ID_PREFIXES = {
  player: "PLY_",
  event:  "EVT_",
  result: "RES_",
  calc:   "CALC_"
};

/* =========================
   PLAYERS SHEET CONFIG (Birthdays)
   Column numbers for player registry.
========================= */

const PLAYERS = {
  SHEET: "PLAYERS",
  START_ROW: 2,

  COL_PLAYER_ID:    1,    // A  (to be filled with PLY_XXXX)
  COL_NAME:         2,    // B
  COL_BIRTHDAY:     3,    // C
  COL_BIRTHPLACE:   4,    // D
  COL_GMT:          5,    // E
  COL_HUMAN_CHECK:  6,    // F
  COL_ELEMENT:      7,    // G
  COL_HOROSCOPE:    8,    // H
  COL_HORO_BUCKET:  9,    // I
  COL_FIRST_RED:    10,   // J
  COL_PERS_CARD:    11,   // K
  COL_SOUL_CARD:    12,   // L
  COL_BC_PATTERN:   13,   // M
  COL_NUMER_BUCKET: 14,   // N
  COL_TITHI_NUM:    15,   // O
  COL_TITHI_TYPE:   16    // P
};

/* =========================
   EVENTS SHEET CONFIG (Event_Data)
   Column numbers for event registry.
========================= */

const EVENTS = {
  SHEET: "EVENTS",
  START_ROW: 2,

  COL_EVENT_ID:     1,    // A  (to be filled with EVT_XXXX)
  COL_TOUR:         2,    // B
  COL_R1_DATE:      3,    // C
  COL_R2_DATE:      4,    // D
  COL_R3_DATE:      5,    // E
  COL_R4_DATE:      6,    // F
  COL_GMT:          7,    // G
  COL_EVENT_TITLE:  8,    // H
  COL_VENUE:        9,    // I
  COL_LOCATION:     10,   // J
  COL_START_TIME:   11,   // K  (tee-off time for the event)
  COL_LATITUDE:     12,   // L
  COL_LONGITUDE:    13,   // M
  COL_MOON_R1_10C:  14,   // N
  COL_MOON_R2_10C:  15,   // O
  COL_MOON_R3_10C:  16,   // P
  COL_MOON_R4_10C:  17,   // Q
  COL_MOON_R1_8C:   18,   // R
  COL_MOON_R2_8C:   19,   // S
  COL_MOON_R3_8C:   20,   // T
  COL_MOON_R4_8C:   21,   // U
  COL_TITHI_R1:     22,   // V
  COL_TITHI_R2:     23,   // W
  COL_TITHI_R3:     24,   // X
  COL_TITHI_R4:     25,   // Y
  COL_TYPE_R1:      26,   // Z
  COL_TYPE_R2:      27,   // AA
  COL_TYPE_R3:      28,   // AB
  COL_TYPE_R4:      29,   // AC
  COL_ASCDEC_R1:    30,   // AD
  COL_ASCDEC_R2:    31,   // AE
  COL_ASCDEC_R3:    32,   // AF
  COL_ASCDEC_R4:    33,   // AG
  // DEPRECATED: COL_WS_D1–D4 were superseded by COL_COND_R1–R4 (same columns).
  // Kept as aliases only — do not use in new code.
  COL_WS_D1:        34,   // AH — now Conditions R1
  COL_WS_D2:        35,   // AI — now Conditions R2
  COL_WS_D3:        36,   // AJ — now Conditions R3
  COL_WS_D4:        37,   // AK — now Conditions R4
  COL_RND1_BUCKET:  38,   // AL
  COL_RND2_BUCKET:  39,   // AM
  COL_RND3_BUCKET:  40,   // AN
  COL_RND4_BUCKET:  41,   // AO
  COL_R1_AVG:       42,   // AP
  COL_R2_AVG:       43,   // AQ
  COL_R3_AVG:       44,   // AR
  COL_R4_AVG:       45,   // AS
  COL_YEAR:         46,   // AT

  // Average scores by condition (Calm/Moderate/Tough)
  COL_R1_AVG_CALM:  47,   // AU
  COL_R2_AVG_CALM:  48,   // AV
  COL_R3_AVG_CALM:  49,   // AW
  COL_R4_AVG_CALM:  50,   // AX
  COL_R1_AVG_MOD:   51,   // AY
  COL_R2_AVG_MOD:   52,   // AZ
  COL_R3_AVG_MOD:   53,   // BA
  COL_R4_AVG_MOD:   54,   // BB
  COL_R1_AVG_TOU:   55,   // BC
  COL_R2_AVG_TOU:   56,   // BD
  COL_R3_AVG_TOU:   57,   // BE
  COL_R4_AVG_TOU:   58,   // BF

  // CONDITIONS — Calm/Moderate/Tough labels for each round.
  // These occupy cols 34–37 (AH–AK), which previously held COL_WS_D1–D4.
  // COL_WS_D1–D4 above are now stale aliases pointing to the same slots.
  // Do not use COL_WS_D* in new code — use COL_COND_R* instead.
  COL_COND_R1:      34,   // AH
  COL_COND_R2:      35,   // AI
  COL_COND_R3:      36,   // AJ
  COL_COND_R4:      37    // AK
};

/* =========================
   RESULTS_RAW SHEET CONFIG (new)
   Column numbers for raw golf scores / results.
========================= */

const RESULTS_RAW = {
  SHEET: "RESULTS_RAW",
  START_ROW: 2,

  COL_RESULT_ID:   1,    // A
  COL_PLAYER_ID:   2,    // B
  COL_EVENT_ID:    3,    // C
  COL_R1_SCORE:    4,    // D
  COL_R2_SCORE:    5,    // E
  COL_R3_SCORE:    6,    // F
  COL_R4_SCORE:    7,    // G
  COL_TOTAL:       8,    // H
  COL_STATUS:      9,    // I
  COL_NOTES:       10,   // J
  COL_CREATED_AT:  11    // K
};

/* =========================
   BIRTHDAY_VERIFY SHEET CONFIG
   Column numbers for birthday verification / ESPN lookup results.
========================= */

const BIRTHDAY_VERIFY = {
  SHEET: "BIRTHDAY_VERIFY",
  START_ROW: 2,

  COL_PLAYER_ID:           1,    // A
  COL_NAME:                2,    // B
  COL_CURRENT_BDAY:        3,    // C
  COL_ESPN_BDAY:           4,    // D
  COL_WIKIDATA_BDAY:       5,    // E
  COL_BDAY_STATUS:         6,    // F
  COL_CURRENT_BIRTHPLACE:  7,    // G
  COL_ESPN_BIRTHPLACE:     8,    // H
  COL_WIKIDATA_BIRTHPLACE: 9,    // I
  COL_BIRTHPLACE_STATUS:   10,   // J
  COL_ESPN_ID:             11,   // K
  COL_ACTION_BDAY:         12,   // L  (UPDATE / KEEP / SKIP)
  COL_ACTION_BIRTHPLACE:   13,   // M  (UPDATE / KEEP / SKIP)
  COL_NOTES:               14    // N
};

/* =========================
   ANALYSIS SHEET CONFIG
   Benchmark & threshold analysis layer.
   One row per round played.
========================= */

const COURSES = {
  SHEET: "COURSES",
  START_ROW: 2,

  COL_COURSE_ID:     1,    // A
  COL_COURSE_NAME:   2,    // B
  COL_LOCATION:      3,    // C
  COL_NOTES:         4     // D
};

const EVENTS_COURSES = {
  SHEET: "EVENTS_COURSES",
  START_ROW: 2,

  COL_EVENT_ID:         1,    // A
  COL_COURSE_ID:        2,    // B
  COL_YEAR:             3,    // C
  COL_PAR:              4,    // D
  COL_COURSE_SEQUENCE:  5,    // E (1st course, 2nd course, etc.)
  COL_NOTES:            6,    // F
  COL_STATUS:           7     // G (Confirmed / Pending / etc.)
};

const ANALYSIS = {
  SHEET: "ANALYSIS",
  START_ROW: 2,

  COL_PLAYER_ID:           1,    // A
  COL_PLAYER_NAME:         2,    // B
  COL_EVENT_ID:            3,    // C
  COL_EVENT_NAME:          4,    // D
  COL_ROUND_NUM:           5,    // E
  COL_SCORE:               6,    // F
  COL_PAR:                 7,    // G
  COL_COURSE_AVG:          8,    // H
  COL_DIFF_COURSE_AVG:     9,    // I
  COL_CONDITION:           10,   // J
  COL_COLOR:               11,   // K
  COL_EXEC:                12,   // L
  COL_UPSIDE:              13,   // M
  COL_PLAYER_HIST_PAR:     14,   // N
  COL_DIFF_PLAYER_HIST_PAR: 15   // O
};

/* =========================
   ANALYSIS v3 SHEET CONFIG (Expanded)
   Full data export — one row per round played.
   24 columns A–X: all available scoring, divination, and event data.
========================= */

const ANALYSIS_V3 = {
  SHEET: "ANALYSIS",
  START_ROW: 2,

  // Basic identifiers
  COL_PLAYER_ID:        1,    // A
  COL_PLAYER_NAME:      2,    // B
  COL_EVENT_ID:         3,    // C
  COL_EVENT_NAME:       4,    // D
  COL_YEAR:             5,    // E
  COL_ROUND_NUM:        6,    // F

  // Core scoring
  COL_SCORE:            7,    // G
  COL_PAR:              8,    // H
  COL_COURSE_AVG:       9,    // I
  COL_VS_AVG:           10,   // J

  // Round conditions & engine output
  COL_CONDITION:        11,   // K  (Calm/Moderate/Tough)
  COL_ROUND_TYPE:       12,   // L  (Open/Positioning/Closing/REMOVE)
  COL_COLOR:            13,   // M  (Purple/Blue/Green/etc.)
  COL_EXEC:             14,   // N  (0–100)
  COL_UPSIDE:           15,   // O  (0–100)
  COL_PEAK:             16,   // P  (0.0–1.0)

  // Divination & cosmic data
  COL_MOON:             17,   // Q  (Moon phase 10-cat)
  COL_WU_XING:          18,   // R  (Wu Xing element)
  COL_ZODIAC:           19,   // S  (Chinese zodiac)
  COL_LIFE_PATH:        20,   // T  (Numerology)
  COL_TITHI:            21,   // U  (Hindu lunar day)

  // Other signals
  COL_GAP:              22,   // V  (vs field in R1 only, blank for R2–R4)
  COL_TOUR:             23,   // W  (PGA Tour / LIV Golf / DP World Tour)
  COL_IS_BEST_ROUND:    24,   // X  (1 if this is best upside round, else 0)

  // Populated data columns (Y–Z): horoscope, moonwest
  // (No constants needed; populated directly by _populateAnalysisV3Batch_)
  // COL_HOROSCOPE:      25,   // Y (Western horoscope from PLAYERS)
  // COL_MOONWEST:       26,   // Z (Western moon phase per-round, 8-cat)

  // Formula columns (added via ADD_ANALYSIS_V3_FORMULAS)
  COL_PLAYER_HIST_PAR:  27,   // AA (formula: player's avg vs_avg by condition)
  COL_PLAYER_HIS_CNT:   28,   // AB (formula: count of player's rounds by condition)
  COL_OFF_PAR:          29,   // AC (formula: score - par)
  COL_EXEC_BUCKET:      30,   // AD (formula: exec binned by 25s)
  COL_UPSIDE_BUCKET:    31,   // AE (formula: upside binned by 25s)
  COL_GAP_BUCKET:       32,   // AF (formula: gap binned by 10s)
  COL_ADJ_HIS_PAR:      33    // AG (formula: adjusted historical par with shrinkage)
};

/* =========================
   GOLF ANALYTICS SHEET CONFIG
   Column numbers for the Golf_Analytics sheet.
   Mapping to current actual layout.
========================= */

const GA = {
  SHEET: "Golf_Analytics",
  START_ROW: 2,

  // ── Display columns (A:J) — engine never writes these ──
  COL_YEAR:         1,    // A  Year
  COL_VENUE:        2,    // B  Event name (match key → EVENTS.COL_EVENT_TITLE)
  COL_PLAYER:       3,    // C  Player name (match key → PLAYERS.COL_NAME)
  COL_R1:           4,    // D  Actual R1 score
  COL_R2:           5,    // E  Actual R2 score
  COL_R3:           6,    // F  Actual R3 score
  COL_R4:           7,    // G  Actual R4 score
  COL_TOT:          8,    // H  Total score
  COL_STATUS:       9,    // I  Finish / Withdrawn / CUT
  COL_DEDUPE_KEY:   10,   // J  Deduplication key

  // ── Input columns (K:Q) — engine reads these ──
  COL_BIRTHDAY:     11,   // K  =VLOOKUP player birthday from PLAYERS
  COL_BDAY_GMT:     12,   // L  =VLOOKUP birth GMT from PLAYERS
  COL_RD1:          13,   // M  =INDEX/MATCH R1 date from EVENTS
  COL_RD2:          14,   // N  =INDEX/MATCH R2 date from EVENTS
  COL_RD3:          15,   // O  =INDEX/MATCH R3 date from EVENTS
  COL_RD4:          16,   // P  =INDEX/MATCH R4 date from EVENTS
  COL_VENUE_GMT:    17,   // Q  =INDEX/MATCH venue GMT from EVENTS

  // ── Engine output (R:AH) — engine writes these ──
  COL_COLOR_START:  18,   // R  R1 Rhythm (color); S=R2, T=R3, U=R4
  COL_SCORE_START:  22,   // V  R1 Exec; W=R1 Upside; X=R1 Peak
                          // Y=R2 Exec; Z=R2 Upside; AA=R2 Peak
                          // AB=R3 Exec; AC=R3 Upside; AD=R3 Peak
                          // AE=R4 Exec; AF=R4 Upside; AG=R4 Peak
  COL_BEST_ROUND:   34,   // AH Best Upside round label

  // ── Post-engine reference columns (AI:AP) — filled by analysis scripts ──
  COL_COURSE_AVG_R1: 35,  // AI Course Avg R1 (field average for that round)
  COL_COURSE_AVG_R2: 36,  // AJ Course Avg R2
  COL_COURSE_AVG_R3: 37,  // AK Course Avg R3
  COL_COURSE_AVG_R4: 38,  // AL Course Avg R4
  COL_VS_AVG_R1:    39,   // AM R1 vs Avg (score − course avg)
  COL_VS_AVG_R2:    40,   // AN R2 vs Avg
  COL_VS_AVG_R3:    41,   // AO R3 vs Avg
  COL_VS_AVG_R4:    42,   // AP R4 vs Avg

  // ── Conditions (AQ:AT) — Calm / Moderate / Tough per round ──
  COL_COND_R1:      43,   // AQ R1 Course Condition
  COL_COND_R2:      44,   // AR R2 Course Condition
  COL_COND_R3:      45,   // AS R3 Course Condition
  COL_COND_R4:      46,   // AT R4 Course Condition

  // ── Round type (AU:AX) — Open / Positioning / Closing / REMOVE ──
  COL_TYPE_R1:      47,   // AU Round Type R1
  COL_TYPE_R2:      48,   // AV Round Type R2
  COL_TYPE_R3:      49,   // AW Round Type R3
  COL_TYPE_R4:      50,   // AX Round Type R4

  // ── Moon phase 10-cat (AY:BB) ──
  COL_MOON_R1:      51,   // AY Moon R1
  COL_MOON_R2:      52,   // AZ Moon R2
  COL_MOON_R3:      53,   // BA Moon R3
  COL_MOON_R4:      54,   // BB Moon R4

  // ── Divination columns (BC:BL) — player-level, same value every round ──
  COL_WU_XING:      55,   // BC Wu Xing Element
  COL_ZODIAC:       56,   // BD Chinese Zodiac
  COL_DESTINY_CARD: 57,   // BE Destiny Card
  COL_HOROSCOPE:    58,   // BF Horoscope (Western)
  COL_MOONWEST_R1:  59,   // BG MoonWest R1 (8-cat)
  COL_MOONWEST_R2:  60,   // BH MoonWest R2 (8-cat)
  COL_MOONWEST_R3:  61,   // BI MoonWest R3 (8-cat)
  COL_MOONWEST_R4:  62,   // BJ MoonWest R4 (8-cat)
  COL_LIFE_PATH:    63,   // BK Life Path
  COL_TITHI:        64,   // BL Tithi

  // ── Other signals ──
  COL_GAP_R1:       65,   // BM R1 GAP
  COL_ROUND_WD:     66,   // BN Round Withdrawn
  COL_TOUR:         67,   // BO Tour (PGA Tour / LIV Golf / DP World Tour / other)

  // ── ID columns (BP:BQ) — for linking to PLAYERS and EVENTS ──
  COL_PLAYER_ID:    68,   // BP Player ID (PLY_XXXX)
  COL_EVENT_ID:     69,   // BQ Event ID (EVT_XXXX)
  COL_COURSE_PAR:   70,   // BR Course Par

  // ── Event dates & Personal Day columns (BT:CB) — numerology analysis ──
  COL_EVENT_DAY_R1: 72,   // BT Event day for Round 1 (from EVENTS.R1_DATE)
  COL_EVENT_DAY_R2: 73,   // BU Event day for Round 2 (from EVENTS.R2_DATE)
  COL_EVENT_DAY_R3: 74,   // BV Event day for Round 3 (from EVENTS.R3_DATE)
  COL_EVENT_DAY_R4: 75,   // BW Event day for Round 4 (from EVENTS.R4_DATE)
  COL_EVENT_GMT:    76,   // BX Event GMT (from EVENTS.GMT)
  COL_PERSONAL_DAY_R1: 77, // BY Personal Day for Round 1 (numerology: PY + month + day)
  COL_PERSONAL_DAY_R2: 78, // BZ Personal Day for Round 2 (numerology: PY + month + day)
  COL_PERSONAL_DAY_R3: 79, // CA Personal Day for Round 3 (numerology: PY + month + day)
  COL_PERSONAL_DAY_R4: 80, // CB Personal Day for Round 4 (numerology: PY + month + day)

  // ── Engine read/write range metadata ──
  READ_START_COL:   11,   // K  — first column read by engine
  READ_NUM_COLS:    7,    // K:Q — columns read (7 total)
  OUTPUT_NUM_COLS:  16,   // R:AH — columns written by engine (16 total)

  TEEOFF_TIME:  "9:00",
  BOUNDARY:     "ZI",
  PRESET:       "CLASSIC"
};

/* =========================
   TOURNAMENT SCORE SHEET CONFIG
   Column numbers for the Tournament Score sheet.
   Similar to Golf_Analytics but single event per row (4 rounds per row).
========================= */

const TS = {
  SHEET: "tournament score",
  START_ROW: 4,

  // ── Input columns (C:O) — engine reads these ──
  COL_BIRTHDAY:     3,    // C  Player birthday
  COL_BDAY_GMT:     4,    // D  Birth GMT offset
  COL_ELEMENT:      5,    // E  Wu Xing element (for reference)
  COL_TITHI_TYPE:   6,    // F  Tithi type (for reference)
  COL_ZODIAC:       7,    // G  Chinese zodiac (for reference)
  COL_HOROSCOPE:    8,    // H  Western horoscope (for reference)
  COL_LIFE_PATH:    9,    // I  Life path number (for reference)
  COL_PERSONAL_YEAR: 10,  // J  Personal year (for reference)
  COL_EVENT_GMT:    11,   // K  Event venue GMT (constant for all 4 rounds)
  COL_R1_DATE:      12,   // L  Round 1 date
  COL_R2_DATE:      13,   // M  Round 2 date
  COL_R3_DATE:      14,   // N  Round 3 date
  COL_R4_DATE:      15,   // O  Round 4 date

  // ── Engine output (P:AE) — engine writes these ──
  COL_COLOR_START:  16,   // P  R1 Color; Q=R2, R=R3, S=R4
  COL_SCORE_START:  20,   // T  R1 Exec; U=R1 Upside; V=R1 Peak
                          // W=R2 Exec; X=R2 Upside; Y=R2 Peak
                          // Z=R3 Exec; AA=R3 Upside; AB=R3 Peak
                          // AC=R4 Exec; AD=R4 Upside; AE=R4 Peak

  READ_START_COL:   3,    // C (birthday)
  READ_NUM_COLS:    13,   // C:O — columns read (13 total)
  OUTPUT_NUM_COLS:  16,   // P:AE — columns written by engine (16 total)

  TEEOFF_TIME:  "9:00",
  BOUNDARY:     "ZI",
  PRESET:       "CLASSIC"
};

/* =========================
   OVERNIGHT RUNNER — PERFORMANCE & STATE
   Controls batch size, timing, and property key names.
========================= */

const CHUNK_SIZE     = 200;
const TRIGGER_MINS   = 1;
const MAX_RUN_MILLIS = 330000; // ~5.5 minutes safety window

// Property keys — used to save/read progress between trigger runs
const PROP_PROGRESS   = "GA_OVERNIGHT_ROW";
const PROP_FORCE      = "GA_OVERNIGHT_FORCE";
const PROP_DO_COLORS  = "GA_RUN_COLORS_ONLY";
const PROP_DO_SCORES  = "GA_RUN_SCORES_ONLY";
const PROP_LAST_START = "GA_OVERNIGHT_LAST_START";
const PROP_LAST_DONE  = "GA_OVERNIGHT_LAST_DONE";
const PROP_LAST_ERROR = "GA_OVERNIGHT_LAST_ERROR";

// Name of the trigger function (must match the function name in 02_runner_overnight.gs)
const TRIGGER_FN = "OVERNIGHT_CHUNK";

/* =========================
   MEMO CACHE
   In-memory cache to avoid recomputing the same values
   within a single script run.
========================= */

const _MEMO = {
  roundOutputs: Object.create(null),
  personEnv:    Object.create(null),
  golfScores:   Object.create(null)
};

/* =========================
   LUCKY DAY ENGINE CONFIG
   Weights and thresholds for the personal/environment
   alignment scoring system.
========================= */

const LUCKY_CFG = {
  AM_HOUR:  10,
  PM_HOUR:  19,
  MINUTE:   0,

  DEFAULT_BOUNDARY: "MIDNIGHT",
  DEFAULT_PRESET:   "CLASSIC",

  // Pillar weights for natal chart
  NATAL_W:          { year: 1, month: 2, day: 3, hour: 1 },
  NATAL_YEAR_MULT:  1.5,

  // Environment blend weights
  ENV_W_DAY:        0.7,
  ENV_W_YEAR:       0.3,

  ENV_COUNTER_BOOST: 0.08,

  // Score shaping
  SHAPE_TANH_K:     1.2,
  PEAK_ENV_GAIN:    0.25,

  STABLE_MAX:       0.30,
  SWINGY_MIN:       0.45,

  // 5x5 element interaction matrix
  ENV_MATRIX: [
    [1,    0.35, 0,   -0.9, 0.85],
    [0.85, 1,    0.35, 0.85, -0.9],
    [0,    0.85, 1,    0.35, 0.85],
    [-0.9, 0,    0.85, 1,    0.35],
    [0.35,-0.9,  0,    0.85, 1]
  ]
};

const LUCKY_BASELINE = 72;

/* =========================
   GOLF ENGINE CONFIG
   Scoring weights for Exec and Upside calculations.
========================= */

const GOLF_CFG = {
  ENV_W_DAY:   0.70,
  ENV_W_YEAR:  0.30,
  ENV_W_MONTH: 0.00,

  HIDDEN_DAMP_START: 0.55,
  HIDDEN_DAMP_END:   0.80,

  EXEC: {
    base:            50,
    resourceStem:    18,
    resourceHidden:  7,
    powerStem:       16,
    powerHidden:     6,
    outputStem:      6,
    wealthStem:      3,
    peerStem:        -12,
    peakPenaltyK:    20
  },

  UPSIDE: {
    base:                 50,
    outputStem:           20,
    outputHidden:         7,
    wealthStem:           9,
    wealthHidden:         5,
    resourceStem:         7,
    powerStem:            5,
    peerStem:             -10,
    peakPlateauBonusK:    16,
    peakExtremePenaltyK:  14,
    extremeStart:         0.68
  },

  POWER_SUPPORT: {
    noResourcePenaltyExec:    -6,
    noResourcePenaltyUpside:  -10,
    supportedBonusExec:       4
  }
};

/* =========================
   BAZI CORE — LOOKUP TABLES
   Static reference data for the BaZi system.
   Do not modify unless the system itself changes.
========================= */

const EL_ORDER    = ["Wood", "Fire", "Earth", "Metal", "Water"];
const STEM_KEYS   = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"];
const BRANCH_KEYS = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"];

const BRANCH_ANIMALS = {
  Zi:"Rat", Chou:"Ox", Yin:"Tiger", Mao:"Rabbit", Chen:"Dragon",
  Si:"Snake", Wu:"Horse", Wei:"Goat", Shen:"Monkey", You:"Rooster",
  Xu:"Dog", Hai:"Pig"
};

const STEMS = [
  {key:"Jia",  yin:false, element:"Wood"},
  {key:"Yi",   yin:true,  element:"Wood"},
  {key:"Bing", yin:false, element:"Fire"},
  {key:"Ding", yin:true,  element:"Fire"},
  {key:"Wu",   yin:false, element:"Earth"},
  {key:"Ji",   yin:true,  element:"Earth"},
  {key:"Geng", yin:false, element:"Metal"},
  {key:"Xin",  yin:true,  element:"Metal"},
  {key:"Ren",  yin:false, element:"Water"},
  {key:"Gui",  yin:true,  element:"Water"}
];

const BRANCHES = [
  {key:"Zi",   animal:"Rat"},
  {key:"Chou", animal:"Ox"},
  {key:"Yin",  animal:"Tiger"},
  {key:"Mao",  animal:"Rabbit"},
  {key:"Chen", animal:"Dragon"},
  {key:"Si",   animal:"Snake"},
  {key:"Wu",   animal:"Horse"},
  {key:"Wei",  animal:"Goat"},
  {key:"Shen", animal:"Monkey"},
  {key:"You",  animal:"Rooster"},
  {key:"Xu",   animal:"Dog"},
  {key:"Hai",  animal:"Pig"}
];

const BRANCH_HIDDEN_STEMS = {
  Rat:     ["Gui"],
  Ox:      ["Ji","Xin","Gui"],
  Tiger:   ["Jia","Bing","Wu"],
  Rabbit:  ["Yi"],
  Dragon:  ["Wu","Yi","Gui"],
  Snake:   ["Bing","Geng","Wu"],
  Horse:   ["Ding","Ji"],
  Goat:    ["Ji","Yi","Ding"],
  Monkey:  ["Geng","Ren","Wu"],
  Rooster: ["Xin"],
  Dog:     ["Wu","Xin","Ding"],
  Pig:     ["Ren","Jia"]
};

const HIDDEN_WEIGHTS_BY_COUNT = {
  1: [1.00],
  2: [0.70, 0.30],
  3: [0.70, 0.20, 0.10]
};

const SEASONAL_PRESETS = {
  CLASSIC: { 旺:1.00, 相:0.85, 休:0.70, 囚:0.50, 死:0.30 },
  TWELVE:  { 旺:1.00, 相:0.90, 休:0.75, 囚:0.55, 死:0.30 }
};

const GEN_CYCLE = ["Wood","Fire","Earth","Metal","Water"];
const KE_CYCLE  = ["Wood","Earth","Water","Fire","Metal"];

const TIGER_MONTH_STEM_BASE_BY_YEAR_GROUP = { 0:3, 1:5, 2:7, 3:9, 4:1 };

/* =========================
   3BMATCHUP SHEET CONFIG
   Three-ball matchup betting data.
   One row per matchup, three players (A/B/C).
   Engine computes color + scores (V:AG) for each player.
========================= */

const SHEET_3BMATCHUP = "3BMatchup";
const PROP_PROGRESS_3BM    = "3BM_OVERNIGHT_ROW";
const PROP_FORCE_3BM       = "3BM_OVERNIGHT_FORCE";
const PROP_DO_COLORS_3BM   = "3BM_RUN_COLORS_ONLY";
const PROP_DO_SCORES_3BM   = "3BM_RUN_SCORES_ONLY";
const PROP_LAST_START_3BM  = "3BM_OVERNIGHT_LAST_START";
const PROP_LAST_DONE_3BM   = "3BM_OVERNIGHT_LAST_DONE";
const PROP_LAST_ERROR_3BM  = "3BM_OVERNIGHT_LAST_ERROR";

const TRIGGER_FN_3BM = "OVERNIGHT_CHUNK_3BM";

const COLS_3BM = {
  EVENT_DATE:   5,      // E
  EVENT_GMT:    6,      // F
  PLAYER_A:     8,      // H
  PLAYER_B:     9,      // I
  PLAYER_C:     10,     // J
  BIRTHDAY_A:   14,     // N
  GMT_A:        15,     // O
  BIRTHDAY_B:   16,     // P
  GMT_B:        17,     // Q
  BIRTHDAY_C:   18,     // R
  GMT_C:        19,     // S
  CONDITION:    20,     // T
  ROUND_TYPE:   21,     // U
  COLOR_A:      23,     // W
  EXEC_A:       24,     // X
  UPSIDE_A:     25,     // Y
  PEAK_A:       26,     // Z
  COLOR_B:      27,     // AA
  EXEC_B:       28,     // AB
  UPSIDE_B:     29,     // AC
  PEAK_B:       30,     // AD
  COLOR_C:      31,     // AE
  EXEC_C:       32,     // AF
  UPSIDE_C:     33,     // AG
  PEAK_C:       34      // AH
};
