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

/* =========================
   GOLF ANALYTICS SHEET CONFIG
   Column numbers for the Golf_Analytics sheet.
   K=11, L=12, M=13 etc. — never use raw numbers in logic.
========================= */

const GA = {
  SHEET: "Golf_Analytics",
  START_ROW: 2,

  COL_BIRTHDAY:     11,   // K
  COL_BDAY_GMT:     12,   // L
  COL_RD1:          13,   // M
  COL_RD2:          14,   // N
  COL_RD3:          15,   // O
  COL_RD4:          16,   // P
  COL_VENUE_GMT:    17,   // Q

  COL_COLOR_START:  18,   // R:S:T:U  (round colors)
  COL_SCORE_START:  22,   // V:AG     (exec/upside/peak)
  COL_BEST_ROUND:   34,   // AH

  READ_START_COL:   11,   // K  — first column we read
  READ_NUM_COLS:    7,    // K:Q — how many columns we read
  OUTPUT_NUM_COLS:  16,   // R:AG — how many columns we write

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
