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
  COL_START_TIME:   11,   // K
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
  COL_WS_D1:        34,   // AH
  COL_WS_D2:        35,   // AI
  COL_WS_D3:        36,   // AJ
  COL_WS_D4:        37,   // AK
  COL_RND1_BUCKET:  38,   // AL
  COL_RND2_BUCKET:  39,   // AM
  COL_RND3_BUCKET:  40,   // AN
  COL_RND4_BUCKET:  41,   // AO
  COL_R1_AVG:       42,   // AP
  COL_R2_AVG:       43,   // AQ
  COL_R3_AVG:       44,   // AR
  COL_R4_AVG:       45,   // AS
  COL_YEAR:         46,   // AT

  // CONDITIONS (moved from far-right to dedicated columns)
  COL_COND_R1:      34,   // AH (Calm/Moderate/Tough for R1)
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
   GOLF ANALYTICS SHEET CONFIG
   Column numbers for the Golf_Analytics sheet.
   Mapping to current actual layout.
========================= */

const GA = {
  SHEET: "Golf_Analytics",
  START_ROW: 2,

  // Input columns (read by engine) — columns K:Q
  COL_BIRTHDAY:     11,   // K
  COL_BDAY_GMT:     12,   // L
  COL_RD1:          13,   // M
  COL_RD2:          14,   // N
  COL_RD3:          15,   // O
  COL_RD4:          16,   // P
  COL_VENUE_GMT:    17,   // Q

  // Output columns (written by engine)
  COL_COLOR_START:  18,   // R:U (round 1-4 colors)
  COL_SCORE_START:  22,   // V:AH (exec/upside/peak for rounds 1-4)
  COL_BEST_ROUND:   34,   // AH (best upside round label)

  // Display/reference columns (already in sheet, engine doesn't touch)
  COL_YEAR:         1,    // A
  COL_VENUE:        2,    // B
  COL_PLAYER:       3,    // C
  COL_R1:           4,    // D (actual score R1)
  COL_R2:           5,    // E
  COL_R3:           6,    // F
  COL_R4:           7,    // G
  COL_TOT:          8,    // H
  COL_STATUS:       9,    // I
  COL_DEDUPE_KEY:   10,   // J

  // Conditions pulled from Event_Data
  COL_COND_R1:      44,   // AR
  COL_COND_R2:      45,   // AS
  COL_COND_R3:      46,   // AT
  COL_COND_R4:      47,   // AU

  READ_START_COL:   11,   // K  — first column we read for engine
  READ_NUM_COLS:    7,    // K:Q — how many columns we read
  OUTPUT_NUM_COLS:  16,   // R:AH — how many columns we write

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
