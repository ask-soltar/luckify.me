
/****************************************************
 * Golf Analytics — Apps Script (CLEANED + REVERTED GOLF MODEL)
 * Google Sheet: Golf_Analytics
 *
 * INPUT COLUMNS:
 *   K (11) = Birthday
 *   L (12) = Birthday GMT
 *   M (13) = Round 1 Date
 *   N (14) = Round 2 Date
 *   O (15) = Round 3 Date
 *   P (16) = Round 4 Date
 *   Q (17) = Venue GMT offset
 *
 * OUTPUT COLUMNS:
 *   R (18) = Round 1 Color
 *   S (19) = Round 2 Color
 *   T (20) = Round 3 Color
 *   U (21) = Round 4 Color
 *
 *   V  (22) = R1 Exec
 *   W  (23) = R1 Upside
 *   X  (24) = R1 Peak
 *   Y  (25) = R2 Exec
 *   Z  (26) = R2 Upside
 *   AA (27) = R2 Peak
 *   AB (28) = R3 Exec
 *   AC (29) = R3 Upside
 *   AD (30) = R3 Peak
 *   AE (31) = R4 Exec
 *   AF (32) = R4 Upside
 *   AG (33) = R4 Peak
 ****************************************************/

/* =========================
   CONFIG
========================= */

const GA = {
  SHEET: "Golf_Analytics",
  START_ROW: 2,

  COL_BIRTHDAY: 11,   // K
  COL_BDAY_GMT: 12,   // L
  COL_RD1: 13,        // M
  COL_RD2: 14,        // N
  COL_RD3: 15,        // O
  COL_RD4: 16,        // P
  COL_VENUE_GMT: 17,  // Q

  COL_COLOR_START: 18, // R:S:T:U
  COL_SCORE_START: 22, // V:AG
  COL_BEST_ROUND: 34,  // AH

  READ_START_COL: 11,   // K
  READ_NUM_COLS: 7,     // K:Q
  OUTPUT_NUM_COLS: 16,  // R:AG

  TEEOFF_TIME: "9:00",
  BOUNDARY: "ZI",
  PRESET: "CLASSIC"
};

/* =========================
   PERFORMANCE / STATE
========================= */

const CHUNK_SIZE = 200;
const TRIGGER_MINS = 1;
const MAX_RUN_MILLIS = 330000; // ~5.5 min

const PROP_PROGRESS = "GA_OVERNIGHT_ROW";
const PROP_FORCE = "GA_OVERNIGHT_FORCE";
const PROP_DO_COLORS = "GA_RUN_COLORS_ONLY";
const PROP_DO_SCORES = "GA_RUN_SCORES_ONLY";
const PROP_LAST_START = "GA_OVERNIGHT_LAST_START";
const PROP_LAST_DONE = "GA_OVERNIGHT_LAST_DONE";
const PROP_LAST_ERROR = "GA_OVERNIGHT_LAST_ERROR";

const TRIGGER_FN = "OVERNIGHT_CHUNK";

const _MEMO = {
  roundOutputs: Object.create(null),
  personEnv: Object.create(null),
  golfScores: Object.create(null)
};

/* =========================
   MENU
========================= */

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Golf Analytics")
    .addItem("▶ Fill Blank (Colors + Scores)", "FILL_ALL")
    .addSeparator()
    .addItem("🎨 Fill Blank Colors Only", "FILL_GOLF_COLORS")
    .addItem("📊 Fill Blank Scores Only", "FILL_GOLF_SCORES")
    .addSeparator()
    .addItem("🔁 Force Recompute Everything", "FORCE_RECOMPUTE_ALL")
    .addSeparator()
    .addItem("🏆 Mark Best Round (Upside)", "FILL_BEST_ROUND")
    .addSeparator()
    .addItem("🧪 Test Single Row", "TEST_SINGLE_ROW")
    .addItem("🔍 Debug Active Row", "DEBUG_ACTIVE_ROW")
    .addSeparator()
    .addItem("🌙 Start Overnight Run", "START_OVERNIGHT")
    .addItem("🌙 Start Overnight Force Run", "START_OVERNIGHT_FORCE")
    .addItem("🎨 Start Overnight Colors Only", "START_OVERNIGHT_COLORS_ONLY")
    .addItem("📊 Start Overnight Scores Only", "START_OVERNIGHT_SCORES_ONLY")
    .addItem("⏹ Stop Overnight Run", "STOP_OVERNIGHT")
    .addItem("📍 Overnight Status", "OVERNIGHT_STATUS")
    .addItem("🔄 Reset Overnight Progress", "RESET_OVERNIGHT")
    .addToUi();
}

/* =========================
   PRIMARY ENTRY POINTS
========================= */

function FILL_ALL() {
  _fillSheet_(false, true, true);
}

function FILL_GOLF_COLORS() {
  _fillSheet_(false, true, false);
}

function FILL_GOLF_SCORES() {
  _fillSheet_(false, false, true);
}

function FORCE_RECOMPUTE_ALL() {
  _fillSheet_(true, true, true);
}

/* =========================
   TEST / DEBUG / SINGLE ROW
========================= */

function TEST_SINGLE_ROW() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const row = sheet.getActiveRange().getRow();

  if (row < GA.START_ROW) {
    SpreadsheetApp.getUi().alert("Select a data row first (row 2 or below).");
    return;
  }

  _fillRow_(sheet, row, false);
  SpreadsheetApp.getUi().alert(
    "Test finished for row " + row + ".\nCheck R:AG and Apps Script logs if needed."
  );
}

function DEBUG_ACTIVE_ROW() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const row = sheet.getActiveRange().getRow();

  if (row < GA.START_ROW) {
    SpreadsheetApp.getUi().alert("Select a data row first (row 2 or below).");
    return;
  }

  const vals = sheet.getRange(row, GA.READ_START_COL, 1, GA.READ_NUM_COLS).getValues()[0];
  const birthday = vals[0];
  const bdayGMT = vals[1];
  const venueGMT = vals[6];
  const rounds = [vals[2], vals[3], vals[4], vals[5]];

  const lines = [];
  lines.push("Row " + row);
  lines.push("birthday = " + birthday);
  lines.push("bdayGMT = " + bdayGMT);
  lines.push("venueGMT = " + venueGMT);

  for (let idx = 0; idx < 4; idx++) {
    const eventDate = rounds[idx];
    if (!eventDate) {
      lines.push("R" + (idx + 1) + ": no event date");
      continue;
    }

    const computed = _computeRoundOutputs_(birthday, bdayGMT, eventDate, venueGMT);
    lines.push(
      "R" + (idx + 1) +
      " | date=" + eventDate +
      " | color=" + computed.color +
      " | exec=" + computed.exec +
      " | upside=" + computed.upside +
      " | peak=" + computed.peak +
      " | error=" + (computed.error || "—")
    );
  }

  Logger.log(lines.join("\n"));
  SpreadsheetApp.getUi().alert("Debug written to Apps Script logs for row " + row + ".");
}

/* =========================
   OVERNIGHT CONTROL
========================= */

function START_OVERNIGHT() {
  _startOvernightRun_(false, true, true);
}

function START_OVERNIGHT_FORCE() {
  _startOvernightRun_(true, true, true);
}

function START_OVERNIGHT_COLORS_ONLY() {
  _startOvernightRun_(false, true, false);
}

function START_OVERNIGHT_SCORES_ONLY() {
  _startOvernightRun_(false, false, true);
}

function _startOvernightRun_(force, doColors, doScores) {
  _deleteOvernightTriggers_();

  const props = PropertiesService.getScriptProperties();
  props.setProperty(PROP_PROGRESS, String(GA.START_ROW));
  props.setProperty(PROP_FORCE, force ? "true" : "false");
  props.setProperty(PROP_DO_COLORS, doColors ? "true" : "false");
  props.setProperty(PROP_DO_SCORES, doScores ? "true" : "false");
  props.deleteProperty(PROP_LAST_START);
  props.deleteProperty(PROP_LAST_DONE);
  props.deleteProperty(PROP_LAST_ERROR);

  ScriptApp.newTrigger(TRIGGER_FN)
    .timeBased()
    .everyMinutes(TRIGGER_MINS)
    .create();

  SpreadsheetApp.getUi().alert(
    "🌙 Overnight run started.\n\n" +
    "Mode: " + (force ? "Force recompute" : "Fill missing only") + "\n" +
    "Colors: " + (doColors ? "Yes" : "No") + "\n" +
    "Scores: " + (doScores ? "Yes" : "No") + "\n" +
    "Writes to: R:AG\n" +
    "Chunk size: " + CHUNK_SIZE + "\n" +
    "Trigger interval: every " + TRIGGER_MINS + " minute"
  );
}

function STOP_OVERNIGHT() {
  _deleteOvernightTriggers_();

  const props = PropertiesService.getScriptProperties();
  props.deleteProperty(PROP_PROGRESS);
  props.deleteProperty(PROP_FORCE);
  props.deleteProperty(PROP_DO_COLORS);
  props.deleteProperty(PROP_DO_SCORES);

  SpreadsheetApp.getUi().alert("⏹ Overnight run stopped.");
}

function RESET_OVERNIGHT() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty(PROP_PROGRESS, String(GA.START_ROW));
  props.deleteProperty(PROP_LAST_ERROR);

  SpreadsheetApp.getUi().alert("🔄 Overnight progress reset to row " + GA.START_ROW + ".");
}

function OVERNIGHT_STATUS() {
  const props = PropertiesService.getScriptProperties();
  const currentRow = Number(props.getProperty(PROP_PROGRESS) || GA.START_ROW);
  const force = props.getProperty(PROP_FORCE) === "true";
  const doColors = props.getProperty(PROP_DO_COLORS) !== "false";
  const doScores = props.getProperty(PROP_DO_SCORES) !== "false";
  const lastStart = props.getProperty(PROP_LAST_START) || "—";
  const lastDone = props.getProperty(PROP_LAST_DONE) || "—";
  const lastError = props.getProperty(PROP_LAST_ERROR) || "—";

  const triggers = ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === TRIGGER_FN);

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const lastRow = sheet ? sheet.getLastRow() : 0;
  const done = lastRow > 0 && currentRow > lastRow;

  const pct = lastRow > GA.START_ROW
    ? Math.min(100, Math.round(((currentRow - GA.START_ROW) / (lastRow - GA.START_ROW)) * 100))
    : 0;

  const msg = [
    done ? "✅ COMPLETE" : "🔄 IN PROGRESS — " + pct + "%",
    "Current row: " + currentRow + " of " + lastRow,
    "Trigger active: " + (triggers.length > 0 ? "Yes" : "No"),
    "Mode: " + (force ? "Force recompute" : "Fill empty only"),
    "Colors: " + (doColors ? "Yes" : "No"),
    "Scores: " + (doScores ? "Yes" : "No"),
    "Writes to: R:AG",
    "Chunk size: " + CHUNK_SIZE,
    "Trigger interval: " + TRIGGER_MINS + " minute",
    "Last chunk start: " + lastStart,
    "Last chunk finish: " + lastDone,
    "Last error: " + lastError
  ].join("\n");

  SpreadsheetApp.getUi().alert(msg);
}

function _deleteOvernightTriggers_() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === TRIGGER_FN)
    .forEach(t => ScriptApp.deleteTrigger(t));
}

/* =========================
   OVERNIGHT WORKER
========================= */

function OVERNIGHT_CHUNK() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;

  try {
    const started = Date.now();
    const props = PropertiesService.getScriptProperties();
    props.setProperty(PROP_LAST_START, new Date().toISOString());
    props.deleteProperty(PROP_LAST_ERROR);

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
    const lastRow = sheet.getLastRow();

    let startRow = Number(props.getProperty(PROP_PROGRESS) || GA.START_ROW);
    const force = props.getProperty(PROP_FORCE) === "true";
    const doColors = props.getProperty(PROP_DO_COLORS) !== "false";
    const doScores = props.getProperty(PROP_DO_SCORES) !== "false";

    if (startRow > lastRow) {
      _deleteOvernightTriggers_();
      props.setProperty(PROP_LAST_DONE, new Date().toISOString());
      Logger.log("Overnight run complete.");
      return;
    }

    while (startRow <= lastRow && (Date.now() - started) < MAX_RUN_MILLIS) {
      const endRow = Math.min(startRow + CHUNK_SIZE - 1, lastRow);
      _processChunk_(sheet, startRow, endRow, force, doColors, doScores);
      startRow = endRow + 1;
      props.setProperty(PROP_PROGRESS, String(startRow));
    }

    props.setProperty(PROP_LAST_DONE, new Date().toISOString());

    if (startRow > lastRow) {
      _deleteOvernightTriggers_();
      Logger.log("Overnight run complete.");
    } else {
      Logger.log("Paused at row " + startRow + "; next trigger will continue.");
    }
  } catch (err) {
    PropertiesService.getScriptProperties().setProperty(
      PROP_LAST_ERROR,
      err && err.message ? err.message : String(err)
    );
    throw err;
  } finally {
    lock.releaseLock();
  }
}

function _processChunk_(sheet, startRow, endRow, forceAll, doColors, doScores) {
  const numRows = endRow - startRow + 1;
  if (numRows <= 0) return;

  const data = sheet.getRange(startRow, GA.READ_START_COL, numRows, GA.READ_NUM_COLS).getValues();

  let existing = null;
  if (!forceAll) {
    existing = sheet.getRange(startRow, GA.COL_COLOR_START, numRows, GA.OUTPUT_NUM_COLS).getValues();
  }

  const output = new Array(numRows);

  for (let i = 0; i < numRows; i++) {
    const sourceRow = data[i];
    const existingRow = existing ? existing[i] : null;
    output[i] = _buildOutputRow_(sourceRow, existingRow, forceAll, doColors, doScores, startRow + i);
  }

  sheet.getRange(startRow, GA.COL_COLOR_START, numRows, GA.OUTPUT_NUM_COLS).setValues(output);
}

/* =========================
   CORE BATCH WRITER
========================= */

function _fillSheet_(forceAll, doColors, doScores) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
    const lastRow = sheet.getLastRow();
    if (lastRow < GA.START_ROW) return;

    _processChunk_(sheet, GA.START_ROW, lastRow, forceAll, doColors, doScores);
  } finally {
    lock.releaseLock();
  }
}

function _fillRow_(sheet, row, fillBlanksOnly) {
  const sourceRow = sheet.getRange(row, GA.READ_START_COL, 1, GA.READ_NUM_COLS).getValues()[0];
  const existingRow = sheet.getRange(row, GA.COL_COLOR_START, 1, GA.OUTPUT_NUM_COLS).getValues()[0];

  const outputRow = _buildOutputRow_(
    sourceRow,
    existingRow,
    !fillBlanksOnly,
    true,
    true,
    row
  );

  let changed = false;
  for (let i = 0; i < GA.OUTPUT_NUM_COLS; i++) {
    if (outputRow[i] !== existingRow[i]) {
      changed = true;
      break;
    }
  }

  if (changed) {
    sheet.getRange(row, GA.COL_COLOR_START, 1, GA.OUTPUT_NUM_COLS).setValues([outputRow]);
  }
}

function _buildOutputRow_(sourceRow, existingRow, forceAll, doColors, doScores, rowNumber) {
  const birthday = sourceRow[0];
  const bdayGMT = sourceRow[1];
  const venueGMT = sourceRow[6];
  const rounds = [sourceRow[2], sourceRow[3], sourceRow[4], sourceRow[5]];

  const outRow = existingRow ? existingRow.slice() : new Array(GA.OUTPUT_NUM_COLS).fill("");

  if (!_hasRequiredInputs_(birthday, bdayGMT, venueGMT)) {
    Logger.log(
      "Row " + rowNumber +
      " skipped: missing required input" +
      " | birthday=" + birthday +
      " | bdayGMT=" + bdayGMT +
      " | venueGMT=" + venueGMT
    );
    return outRow;
  }

  for (let idx = 0; idx < 4; idx++) {
    const eventDate = rounds[idx];
    if (!eventDate) continue;

    const colorCol = idx;
    const scoreOffset = 4 + idx * 3;

    const needColor = doColors && _needsColor_(existingRow, colorCol, forceAll);
    const needScores = doScores && _needsScores_(existingRow, scoreOffset, forceAll);

    if (!needColor && !needScores) continue;

    const computed = _computeRoundOutputs_(birthday, bdayGMT, eventDate, venueGMT);

    if (computed.error) {
      Logger.log(
        "Row " + rowNumber +
        " Round " + (idx + 1) +
        " error: " + computed.error +
        " | birthday=" + birthday +
        " | bdayGMT=" + bdayGMT +
        " | eventDate=" + eventDate +
        " | venueGMT=" + venueGMT
      );
    }

    if (needColor && computed.color !== "") {
      outRow[colorCol] = computed.color;
    }

    if (needScores) {
      if (computed.exec !== "") outRow[scoreOffset] = computed.exec;
      if (computed.upside !== "") outRow[scoreOffset + 1] = computed.upside;
      if (computed.peak !== "") outRow[scoreOffset + 2] = computed.peak;
    }
  }

  return outRow;
}

function _hasRequiredInputs_(birthday, bdayGMT, venueGMT) {
  return !!birthday && bdayGMT !== "" && bdayGMT != null && venueGMT !== "" && venueGMT != null;
}

function _needsColor_(existingRow, colorCol, forceAll) {
  return forceAll || !existingRow || existingRow[colorCol] === "" || existingRow[colorCol] == null;
}

function _needsScores_(existingRow, scoreOffset, forceAll) {
  return forceAll || !existingRow ||
    existingRow[scoreOffset] === "" || existingRow[scoreOffset] == null ||
    existingRow[scoreOffset + 1] === "" || existingRow[scoreOffset + 1] == null ||
    existingRow[scoreOffset + 2] === "" || existingRow[scoreOffset + 2] == null;
}

/* =========================
   HELPERS
========================= */

function _safeKey_(v) {
  if (v instanceof Date) return v.toISOString();
  if (typeof v === "number") return String(v);
  return String(v || "");
}

/* =========================
   COMPUTE ONCE / REUSE
========================= */

function _computeRoundOutputs_(birthday, bdayGMT, eventDate, venueGMT) {
  const key = [
    _safeKey_(birthday),
    String(bdayGMT),
    _safeKey_(eventDate),
    String(venueGMT),
    GA.TEEOFF_TIME,
    GA.BOUNDARY,
    GA.PRESET
  ].join("|");

  if (_MEMO.roundOutputs[key]) return _MEMO.roundOutputs[key];

  let color = "";
  let exec = "";
  let upside = "";
  let peak = "";
  let error = "";

  try {
    const delta = LUCKY_DAY_DELTA(
      birthday,
      bdayGMT,
      eventDate,
      venueGMT,
      9,
      0,
      null,
      GA.BOUNDARY,
      GA.PRESET
    );
    const cat = LUCKY_CATEGORY_ALT_FROM_DELTA(delta);
    color = LUCKY_CATEGORY_COLOR(cat);
  } catch (e) {
    error += "[COLOR] " + (e && e.message ? e.message : e) + " ";
  }

  try {
    const result = GOLF_LUCK_SCORES_NO_BIRTH_TIME(
      birthday,
      bdayGMT,
      eventDate,
      GA.TEEOFF_TIME,
      venueGMT,
      GA.BOUNDARY,
      GA.PRESET
    );
    exec = result[0][0];
    upside = result[0][1];
    peak = result[0][2];
  } catch (e) {
    error += "[SCORES] " + (e && e.message ? e.message : e);
  }

  const out = { color, exec, upside, peak, error: error.trim() };
  _MEMO.roundOutputs[key] = out;
  return out;
}

/* =========================
   BEST ROUND MARKER
========================= */

function FILL_BEST_ROUND() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const lastRow = sheet.getLastRow();
  const numRows = lastRow - GA.START_ROW + 1;
  if (numRows < 1) return;

  const scores = sheet.getRange(GA.START_ROW, GA.COL_SCORE_START, numRows, 12).getValues();

  const results = scores.map(function(row) {
    const upsides = [row[1], row[4], row[7], row[10]];
    const labels = ["R1", "R2", "R3", "R4"];
    let best = -Infinity;
    let bestLabel = "";

    upsides.forEach(function(u, i) {
      if (u !== "" && u != null && !isNaN(Number(u)) && Number(u) > best) {
        best = Number(u);
        bestLabel = labels[i];
      }
    });

    return [bestLabel];
  });

  sheet.getRange(GA.START_ROW, GA.COL_BEST_ROUND, numRows, 1).setValues(results);
}

/* =========================
   BAZI CORE + ALL SHARED FUNCTIONS
   (self-contained — no external dependencies)
========================= */

const LUCKY_CFG = {
  AM_HOUR: 10,
  PM_HOUR: 19,
  MINUTE: 0,

  DEFAULT_BOUNDARY: "MIDNIGHT",
  DEFAULT_PRESET: "CLASSIC",

  NATAL_W: { year: 1, month: 2, day: 3, hour: 1 },
  NATAL_YEAR_MULT: 1.5,

  ENV_W_DAY: 0.7,
  ENV_W_YEAR: 0.3,

  ENV_COUNTER_BOOST: 0.08,

  SHAPE_TANH_K: 1.2,
  PEAK_ENV_GAIN: 0.25,

  STABLE_MAX: 0.30,
  SWINGY_MIN: 0.45,

  ENV_MATRIX: [
    [1,    0.35, 0,   -0.9, 0.85],
    [0.85, 1,    0.35, 0.85, -0.9],
    [0,    0.85, 1,    0.35, 0.85],
    [-0.9, 0,    0.85, 1,    0.35],
    [0.35,-0.9,  0,    0.85, 1]
  ]
};

const EL_ORDER    = ["Wood","Fire","Earth","Metal","Water"];
const STEM_KEYS   = ["Jia","Yi","Bing","Ding","Wu","Ji","Geng","Xin","Ren","Gui"];
const BRANCH_KEYS = ["Zi","Chou","Yin","Mao","Chen","Si","Wu","Wei","Shen","You","Xu","Hai"];
const BRANCH_ANIMALS = {Zi:"Rat",Chou:"Ox",Yin:"Tiger",Mao:"Rabbit",Chen:"Dragon",Si:"Snake",Wu:"Horse",Wei:"Goat",Shen:"Monkey",You:"Rooster",Xu:"Dog",Hai:"Pig"};

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
  {key:"Zi",  animal:"Rat"},
  {key:"Chou",animal:"Ox"},
  {key:"Yin", animal:"Tiger"},
  {key:"Mao", animal:"Rabbit"},
  {key:"Chen",animal:"Dragon"},
  {key:"Si",  animal:"Snake"},
  {key:"Wu",  animal:"Horse"},
  {key:"Wei", animal:"Goat"},
  {key:"Shen",animal:"Monkey"},
  {key:"You", animal:"Rooster"},
  {key:"Xu",  animal:"Dog"},
  {key:"Hai", animal:"Pig"}
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

const HIDDEN_WEIGHTS_BY_COUNT = { 1:[1.00], 2:[0.70,0.30], 3:[0.70,0.20,0.10] };

const SEASONAL_PRESETS = {
  CLASSIC: { 旺:1.00, 相:0.85, 休:0.70, 囚:0.50, 死:0.30 },
  TWELVE:  { 旺:1.00, 相:0.90, 休:0.75, 囚:0.55, 死:0.30 }
};

const GEN_CYCLE = ["Wood","Fire","Earth","Metal","Water"];
const KE_CYCLE  = ["Wood","Earth","Water","Fire","Metal"];

const GOLF_CFG = {
  ENV_W_DAY: 0.70,
  ENV_W_YEAR: 0.30,
  ENV_W_MONTH: 0.00,

  HIDDEN_DAMP_START: 0.55,
  HIDDEN_DAMP_END: 0.80,

  EXEC: {
    base: 50,
    resourceStem: 18,
    resourceHidden: 7,
    powerStem: 16,
    powerHidden: 6,
    outputStem: 6,
    wealthStem: 3,
    peerStem: -12,
    peakPenaltyK: 20
  },

  UPSIDE: {
    base: 50,
    outputStem: 20,
    outputHidden: 7,
    wealthStem: 9,
    wealthHidden: 5,
    resourceStem: 7,
    powerStem: 5,
    peerStem: -10,
    peakPlateauBonusK: 16,
    peakExtremePenaltyK: 14,
    extremeStart: 0.68
  },

  POWER_SUPPORT: {
    noResourcePenaltyExec: -6,
    noResourcePenaltyUpside: -10,
    supportedBonusExec: 4
  }
};

const LUCKY_BASELINE = 72;

/* ---- Date + TZ helpers ---- */

function _coerceDate_(value) {
  if (value instanceof Date) return new Date(value.getTime());
  if (typeof value === "number") return new Date(Math.round((value - 25569) * 86400000));
  const d = new Date(value);
  if (!isNaN(d)) return d;
  throw new Error("Invalid date: " + value);
}

function _buildLocalDateTime_(dayDate, hour, minute) {
  const d = _coerceDate_(dayDate);
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), hour, minute, 0);
}

function localToUTC(dateLocal, tzHours) {
  const tz = Number(tzHours);
  if (!isFinite(tz)) throw new Error("localToUTC: tzHours must be numeric");
  return new Date((+_coerceDate_(dateLocal)) - tz * 3600000);
}

function _envGMTFromTZIDorOffset_(envTZ, whenLocal) {
  if (envTZ == null || envTZ === "") throw new Error("Missing envTZ.");
  if (typeof envTZ === "number") return Number(envTZ);
  const s = String(envTZ).trim();
  if (/^[+-]?\d+(\.\d+)?$/.test(s)) return Number(s);
  return _gmtOffsetFromTZID_(s, whenLocal);
}

function _gmtOffsetFromTZID_(tzid, whenLocal) {
  const d = _coerceDate_(whenLocal);
  const z = Utilities.formatDate(d, String(tzid), "Z");
  const sign = z.startsWith("-") ? -1 : 1;
  const hh = parseInt(z.substring(1,3), 10);
  const mm = parseInt(z.substring(3,5), 10);
  return sign * (hh + mm/60);
}

function _WD_normTime_(t, defaultTime) {
  if (t == null || t === "") return defaultTime;
  const s = String(t).trim();
  if (s === "") return defaultTime;
  const parts = s.split(":");
  if (parts.length === 2) return `${String(parseInt(parts[0],10)).padStart(2,"0")}:${String(parseInt(parts[1],10)).padStart(2,"0")}`;
  return defaultTime;
}

function _WD_buildLocalDT_(dayDate, hhmm) {
  const [hh, mm] = hhmm.split(":").map(Number);
  return _buildLocalDateTime_(dayDate, Number(hh), Number(mm));
}

/* ---- Solar longitude ---- */

function jdFromDate(date) {
  let d = date;
  if (!(d instanceof Date)) d = new Date(d);
  if (isNaN(d)) throw new Error("jdFromDate: invalid Date");
  return d.getTime() / 86400000 + 2440587.5;
}

function norm360(x) { x = x % 360; return x < 0 ? x + 360 : x; }

function solarLongitudeUTC(utcDate) {
  if (!(utcDate instanceof Date) || isNaN(utcDate)) throw new Error("solarLongitudeUTC: invalid Date");
  const JD = jdFromDate(utcDate);
  const T  = (JD - 2451545.0) / 36525.0;
  const L0 = norm360(280.46646 + 36000.76983*T + 0.0003032*T*T);
  const M  = norm360(357.52911 + 35999.05029*T - 0.0001537*T*T);
  const Mr = M * Math.PI/180;
  const C  = (1.914602 - 0.004817*T - 0.000014*T*T) * Math.sin(Mr)
           + (0.019993 - 0.000101*T) * Math.sin(2*Mr)
           + 0.000289 * Math.sin(3*Mr);
  const trueLong = L0 + C;
  const omega    = 125.04 - 1934.136*T;
  const lambda   = trueLong - 0.00569 - 0.00478 * Math.sin(omega * Math.PI/180);
  return norm360(lambda);
}

function SOLAR_LON(dateSerialOrDate, tzHours) {
  const local = _coerceDate_(dateSerialOrDate);
  const tz = Number(tzHours);
  if (!isFinite(tz)) return "";
  return solarLongitudeUTC(localToUTC(local, tz));
}

/* ---- BaZi pillars ---- */

function _pillarFromStemBranchIdx_(stemIdx, branchIdx) {
  const stemKey   = STEM_KEYS[stemIdx-1];
  const branchKey = BRANCH_KEYS[branchIdx-1];
  const stem      = STEMS.find(s => s.key === stemKey) || {};
  return { stemIdx, branchIdx, stemKey, stemElement: stem.element, branchKey, branchAnimal: BRANCH_ANIMALS[branchKey] };
}

function _stemIndexFromYear_(y)   { return 1 + ((y-4)%10 + 10)%10; }
function _branchIndexFromYear_(y) { return 1 + ((y-4)%12 + 12)%12; }

function _adjustedYearForLichun_(d, tz) {
  const y = d.getFullYear();
  const sunLon = SOLAR_LON(d, tz);
  const m = d.getMonth();
  const after = (m>1) || (m===1 && d.getDate()>=4) || (sunLon>=315 || sunLon<45);
  return after ? y : y-1;
}

const TIGER_MONTH_STEM_BASE_BY_YEAR_GROUP = {0:3,1:5,2:7,3:9,4:1};

function _monthBranchIndexFromSunLon_(sunLon) {
  const lon = ((+sunLon % 360) + 360) % 360;
  const k   = Math.floor(((lon - 315 + 360) % 360) / 30);
  return (k % 12) + 1;
}

function _monthStemIndexFromYearStemAndMonthBranch_(ys, mb) {
  const group = Math.floor((ys-1)/2);
  const base  = TIGER_MONTH_STEM_BASE_BY_YEAR_GROUP[group];
  return 1 + ((base - 1 + (mb - 1)) % 10);
}

function _hourBranchIndexFromLocalTime_(d) {
  const h = d.getHours() + d.getMinutes()/60;
  return Math.floor(((h + 1) % 24) / 2) + 1;
}

function _hourStemIndexFromDayStemAndHourBranch_(ds, hb) {
  const baseByDayGroup = [1,3,5,7,9];
  const g = Math.floor((ds-1)/2);
  return 1 + ((baseByDayGroup[g] - 1 + (hb - 1)) % 10);
}

function _stemKeyToElement_(key) {
  const s = STEMS.find(x => x.key === key);
  return s ? s.element : "";
}

function _seasonElementFromLon_(lon) {
  lon = ((+lon%360)+360)%360;
  if (lon>=315 || lon<45)  return "Wood";
  if (lon>=45 && lon<135)  return "Fire";
  if (lon>=135 && lon<225) return "Metal";
  return "Water";
}

function _statusForElementRelativeToSeason_(el, seasonEl) {
  if (el === seasonEl) return "旺";
  const sIdx = GEN_CYCLE.indexOf(seasonEl);
  if (el === GEN_CYCLE[(sIdx+1)%5]) return "相";
  if (el === GEN_CYCLE[(sIdx+4)%5]) return "休";
  const kIdx = KE_CYCLE.indexOf(seasonEl);
  if (el === KE_CYCLE[(kIdx+1)%5]) return "囚";
  return "死";
}

function _seasonalMultiplier_(el, sunLon, preset) {
  const seasonEl = _seasonElementFromLon_(sunLon);
  const status = _statusForElementRelativeToSeason_(el, seasonEl);
  const table = SEASONAL_PRESETS[(preset||"CLASSIC").toUpperCase()] || SEASONAL_PRESETS.CLASSIC;
  return table[status] || 1.0;
}

function _accumulatePillar_(totals, pillar, weight, sunLon, preset) {
  totals[pillar.stemElement] += weight * _seasonalMultiplier_(pillar.stemElement, sunLon, preset);
  const hidden = BRANCH_HIDDEN_STEMS[pillar.branchAnimal] || [];
  const splits = HIDDEN_WEIGHTS_BY_COUNT[hidden.length] || [];
  for (let i=0;i<hidden.length;i++) {
    const el = _stemKeyToElement_(hidden[i]);
    totals[el] += (splits[i] || 0) * weight * _seasonalMultiplier_(el, sunLon, preset);
  }
}

function BAZI_FULL_PILLARS(dateSerialOrDate, tzHours, boundary) {
  const local = _coerceDate_(dateSerialOrDate);
  const tz = Number(tzHours);
  const sunLon = SOLAR_LON(local, tz);
  const adjYear = _adjustedYearForLichun_(local, tz);
  const yStem = _stemIndexFromYear_(adjYear);
  const yBranch = _branchIndexFromYear_(adjYear);
  const year = _pillarFromStemBranchIdx_(yStem, yBranch);
  const mBranch = _monthBranchIndexFromSunLon_(sunLon);
  const mStem = _monthStemIndexFromYearStemAndMonthBranch_(yStem, mBranch);
  const month = _pillarFromStemBranchIdx_(mStem, mBranch);
  const dStemObj = BAZI_DAY_STEM_OBJ(local, tz, boundary);
  const dBranchObj = BAZI_DAY_BRANCH_OBJ(local, tz, boundary);
  const dStem = STEM_KEYS.indexOf(dStemObj.key) + 1;
  const dBranch = BRANCH_KEYS.indexOf(dBranchObj.key) + 1;
  const day = _pillarFromStemBranchIdx_(dStem, dBranch);
  const hBranch = _hourBranchIndexFromLocalTime_(local);
  const hStem = _hourStemIndexFromDayStemAndHourBranch_(dStem, hBranch);
  const hour = _pillarFromStemBranchIdx_(hStem, hBranch);
  return { year, month, day, hour, sunLon };
}

function BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(dateSerialOrDate, tzHours, boundary, preset, pillarWeights) {
  const P = BAZI_FULL_PILLARS(dateSerialOrDate, tzHours, boundary);
  if (!P) return "";
  const sunLon = P.sunLon;
  const W = Object.assign({year:1,month:2,day:3,hour:1}, pillarWeights || {});
  const totals = {Wood:0,Fire:0,Earth:0,Metal:0,Water:0};
  _accumulatePillar_(totals, P.year, W.year, sunLon, preset);
  _accumulatePillar_(totals, P.month, W.month, sunLon, preset);
  _accumulatePillar_(totals, P.day, W.day, sunLon, preset);
  _accumulatePillar_(totals, P.hour, W.hour, sunLon, preset);
  const sum = Object.values(totals).reduce((a,b)=>a+b,0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el]/sum)*100);
  return out;
}

function BAZI_DAY_STEM_OBJ(dateSerialOrDate, tzHours, boundary) {
  const nums = _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary);
  if (!nums) return "";
  const stem = STEMS[nums.stemNum-1];
  return { key: stem.key, element: stem.element, yin: stem.yin };
}

function BAZI_DAY_BRANCH_OBJ(dateSerialOrDate, tzHours, boundary) {
  const nums = _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary);
  if (!nums) return "";
  const br = BRANCHES[nums.branchNum-1];
  return { key: br.key, animal: br.animal };
}

function BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(dateSerialOrDate, tzHours, boundary, preset) {
  const s = BAZI_DAY_STEM_OBJ(dateSerialOrDate, tzHours, boundary);
  const b = BAZI_DAY_BRANCH_OBJ(dateSerialOrDate, tzHours, boundary);
  if (!s || !b) return "";
  const sunLon = SOLAR_LON(dateSerialOrDate, tzHours);
  const totals = {Wood:0,Fire:0,Earth:0,Metal:0,Water:0};
  totals[s.element] += 1 * _seasonalMultiplier_(s.element, sunLon, preset);
  const hidden = BRANCH_HIDDEN_STEMS[b.animal] || [];
  const weights = HIDDEN_WEIGHTS_BY_COUNT[hidden.length] || [];
  for (let i=0;i<hidden.length;i++) {
    const el = _stemKeyToElement_(hidden[i]);
    totals[el] += (weights[i] || 0) * _seasonalMultiplier_(el, sunLon, preset);
  }
  const sum = Object.values(totals).reduce((a,b)=>a+b,0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el]/sum)*100);
  return out;
}

function _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary) {
  if (dateSerialOrDate == null || tzHours == null) return null;
  const tz = Number(tzHours);
  const localDT = _coerceDate_(dateSerialOrDate);
  let y = localDT.getFullYear(), m = localDT.getMonth(), d = localDT.getDate();

  if (String(boundary||"MIDNIGHT").toUpperCase() === "ZI") {
    const hrs = localDT.getHours() + localDT.getMinutes()/60;
    if (hrs >= 23) {
      const next = new Date(localDT.getTime() + 86400000);
      y = next.getFullYear();
      m = next.getMonth();
      d = next.getDate();
    }
  }

  const localMid = new Date(y, m, d, 0, 0, 0);
  const utcMid = localToUTC(localMid, tz);
  const JD0 = jdFromDate(utcMid);
  const JDN = Math.floor(JD0 + 0.5);

  return {
    stemNum: 1 + ((JDN + 9) % 10 + 10) % 10,
    branchNum: 1 + ((JDN + 1) % 12 + 12) % 12
  };
}

/* ---- Lucky Day core ---- */

function _toVec01_(pctObj) {
  return EL_ORDER.map(el => (pctObj && pctObj[el] != null ? Number(pctObj[el]) : 0) / 100);
}

function _dotRel_(from, to, M) {
  const left = new Array(5).fill(0);
  for (let i=0;i<5;i++) {
    let s = 0;
    for (let j=0;j<5;j++) s += from[j] * M[j][i];
    left[i] = s;
  }
  let out = 0;
  for (let i=0;i<5;i++) out += left[i] * to[i];
  return out;
}

function _shape_(x) { return Math.tanh(LUCKY_CFG.SHAPE_TANH_K * x); }

function _entropy_(v) {
  const eps = 1e-9;
  let H = 0;
  for (let i=0;i<5;i++) {
    const p = Math.max(eps, v[i]);
    H -= p * Math.log(p);
  }
  return H;
}

function _peakiness_(v) {
  const Hmax = Math.log(5);
  return (Hmax - _entropy_(v)) / Hmax;
}

function _controllerOf_(el) {
  return { Wood:"Metal", Fire:"Water", Earth:"Wood", Metal:"Fire", Water:"Earth" }[el] || null;
}

function _dominantEl_(pctObj) {
  let best = "Wood", bestV = -1;
  for (const el of EL_ORDER) {
    const v = Number(pctObj[el] || 0);
    if (v > bestV) { bestV = v; best = el; }
  }
  return best;
}

function _vecToPct_(vec01) {
  const out = {};
  for (let i=0;i<5;i++) out[EL_ORDER[i]] = Math.round((vec01[i] || 0) * 100);
  return out;
}

function _cachedPersonEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts) {
  const key = JSON.stringify(["LDv1", _safeKey_(birthDT), birthGMT, _safeKey_(envLocalDT), envGMT, opts]);
  if (_MEMO.personEnv[key]) return _MEMO.personEnv[key];
  const r = _personEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts);
  _MEMO.personEnv[key] = r;
  return r;
}

function _personEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts) {
  opts = opts || {};
  const boundary = String(opts.boundary || LUCKY_CFG.DEFAULT_BOUNDARY).toUpperCase();
  const preset = String(opts.preset || LUCKY_CFG.DEFAULT_PRESET).toUpperCase();
  const W = Object.assign({}, LUCKY_CFG.NATAL_W);
  W.year *= LUCKY_CFG.NATAL_YEAR_MULT;

  const personPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(birthDT, Number(birthGMT), boundary, preset, W);
  if (!personPct) return null;
  const envDayPct = BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(envLocalDT, Number(envGMT), boundary, preset);
  if (!envDayPct) return null;
  const envYearPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(envLocalDT, Number(envGMT), boundary, preset, {year:1,month:0,day:0,hour:0});
  if (!envYearPct) return null;

  const ed = _toVec01_(envDayPct);
  const ey = _toVec01_(envYearPct);
  const P = BAZI_FULL_PILLARS(envLocalDT, Number(envGMT), boundary);
  const yearStemEl = (P && P.year && P.year.stemElement) ? P.year.stemElement : "Earth";
  const counterEl = _controllerOf_(yearStemEl);

  let eblend = new Array(5);
  for (let i=0;i<5;i++) eblend[i] = LUCKY_CFG.ENV_W_DAY*ed[i] + LUCKY_CFG.ENV_W_YEAR*ey[i];
  if (counterEl) {
    const idx = EL_ORDER.indexOf(counterEl);
    if (idx >= 0) eblend[idx] += LUCKY_CFG.ENV_COUNTER_BOOST;
  }
  const sumE = eblend.reduce((a,b)=>a + Math.max(0,b), 0) || 1;
  for (let i=0;i<5;i++) eblend[i] = Math.max(0, eblend[i]) / sumE;

  const a = _toVec01_(personPct);
  const e = eblend;
  const env_peak = _peakiness_(e);
  const raw = _shape_(_dotRel_(e, a, LUCKY_CFG.ENV_MATRIX) * (1 + LUCKY_CFG.PEAK_ENV_GAIN * env_peak));
  const total = Math.round((raw * 0.5 + 0.5) * 100);
  const edge50 = total - 50;
  const stability = (env_peak <= LUCKY_CFG.STABLE_MAX) ? "Stable"
                  : (env_peak >= LUCKY_CFG.SWINGY_MIN) ? "Swingy" : "Normal";
  const label = _labelFromTotal_(total);

  return {
    total, edge50, label, stability, env_peak, yearStemEl,
    person: personPct, env_vec: e,
    dom_person: _dominantEl_(personPct),
    dom_env: _dominantEl_(_vecToPct_(e))
  };
}

function _labelFromTotal_(total) {
  if (total >= 80) return "Greenlight++";
  if (total >= 65) return "Greenlight+";
  if (total >= 50) return "Neutral";
  if (total >= 35) return "Friction";
  return "Red";
}

/* ---- Lucky Day public ---- */

function LUCKY_DAY_DELTA(birthDT, birthGMT, dayDate, envTZ, hour, minute, baseline, boundary, preset) {
  const base = (baseline === undefined || baseline === null || baseline === "") ? LUCKY_BASELINE : Number(baseline);
  return _luckyDayDeltaFromWindow_(birthDT, birthGMT, dayDate, envTZ, Number(hour || LUCKY_CFG.AM_HOUR), Number(minute || 0), boundary, preset, base);
}

function _luckyDayDeltaFromWindow_(birthDT, birthGMT, dayDate, envTZ, hour, minute, boundary, preset, baselineOverride) {
  const envLocalDT = _buildLocalDateTime_(dayDate, Number(hour), Number(minute));
  const envGMT = _envGMTFromTZIDorOffset_(envTZ, envLocalDT);
  const r = _cachedPersonEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, {
    boundary: boundary || LUCKY_CFG.DEFAULT_BOUNDARY,
    preset: preset || LUCKY_CFG.DEFAULT_PRESET
  });
  if (!r) return "";
  const baseline = (baselineOverride === undefined || baselineOverride === null) ? LUCKY_BASELINE : Number(baselineOverride);
  if (!isFinite(baseline)) throw new Error("Baseline must be numeric.");
  return r.total - baseline;
}

/* ---- Day stem helpers ---- */

function _WD_dayStemElement_(localDT, tzHours, boundary) {
  const s = BAZI_DAY_STEM_OBJ(localDT, tzHours, boundary);
  if (!s || !s.element) throw new Error("Could not compute day stem element.");
  return s.element;
}

function _WD_hiddenElementsFromDayBranch_(localDT, tzHours, boundary) {
  const b = BAZI_DAY_BRANCH_OBJ(localDT, tzHours, boundary);
  if (!b || !b.animal) return [];
  return (BRANCH_HIDDEN_STEMS[b.animal] || []).map(k => _stemKeyToElement_(k)).filter(Boolean);
}

function _WD_wealthEl_(dmEl)   { return ({Wood:"Earth",Fire:"Metal",Earth:"Water",Metal:"Wood",Water:"Fire"})[dmEl] || null; }
function _WD_resourceEl_(dmEl) { return ({Wood:"Water",Fire:"Wood",Earth:"Fire",Metal:"Earth",Water:"Metal"})[dmEl] || null; }
function _WD_outputEl_(dmEl)   { return ({Wood:"Fire",Fire:"Earth",Earth:"Metal",Metal:"Water",Water:"Wood"})[dmEl] || null; }
function _WD_powerEl_(dmEl)    { return _controllerOf_(dmEl); }

/* ---- Category + Color ---- */

function LUCKY_CATEGORY_ALT_FROM_DELTA(d) {
  if (d == null || d === "") return "";
  const n = Number(d);
  if (!isFinite(n)) return "";
  return _categoryFromDeltaAlt_(n);
}

function _categoryFromDeltaAlt_(d) {
  if (d >= 14)  return "Noise";
  if (d >= 7)   return "Prime";
  if (d >= 4)   return "Sub-Prime";
  if (d >= 2)   return "Edge";
  if (d === 0)  return "Neutral";
  if (d >= -1)  return "No Tax";
  if (d >= -2)  return "Null Edge";
  if (d >= -4)  return "Survivor";
  if (d >= -5)  return "Unstable Identity";
  if (d >= -8)  return "Identity";
  if (d >= -9)  return "Stable Identity";
  if (d >= -11) return "Growth";
  if (d >= -13) return "Variance";
  if (d >= -15) return "Stable Swing";
  if (d >= -29) return "Unstable Swing";
  if (d >= -40) return "Luck";
  return "Break Point";
}

function LUCKY_CATEGORY_COLOR(cat) {
  if (cat == null || cat === "") return "";
  const MAP = {
    "Noise":             "Pink",
    "Prime":             "Orange",
    "Sub-Prime":         "Blue",
    "Edge":              "Yellow",
    "No Tax":            "Yellow",
    "Neutral":           "Yellow",
    "Null Edge":         "Yellow",
    "Survivor":          "Green",
    "Unstable Identity": "Purple",
    "Identity":          "Purple",
    "Stable Identity":   "Purple",
    "Growth":            "Green",
    "Variance":          "Blue",
    "Stable Swing":      "Blue",
    "Unstable Swing":    "Red",
    "Luck":              "Brown"
  };
  return MAP[String(cat).trim()] || "";
}

function LUCKY_DELTA_COLOR(d) {
  return LUCKY_CATEGORY_COLOR(LUCKY_CATEGORY_ALT_FROM_DELTA(d));
}

/* ---- Golf Luck Scores ---- */

function GOLF_LUCK_SCORES_NO_BIRTH_TIME(birthDate, birthGMT, envDate, envTime, envTZ, boundary, preset) {
  const b            = String(boundary || "ZI").toUpperCase();
  const p            = String(preset   || "CLASSIC").toUpperCase();
  const birthLocalDT = _WD_buildLocalDT_(birthDate, "12:00");
  const envLocalDT   = _WD_buildLocalDT_(envDate, _WD_normTime_(envTime, "12:00"));
  const envGMT       = _envGMTFromTZIDorOffset_(envTZ, envLocalDT);
  const dmEl         = _WD_dayStemElement_(birthLocalDT, Number(birthGMT), b);
  const envStemEl    = _WD_dayStemElement_(envLocalDT, Number(envGMT), b);
  const envHiddenEls = _WD_hiddenElementsFromDayBranch_(envLocalDT, Number(envGMT), b);
  const env          = _GOLF_envBlend_(envLocalDT, Number(envGMT), b, p);
  const out          = _GOLF_scoreDual_(dmEl, envStemEl, envHiddenEls, env.peak);

  return [[out.execScore, out.upsideScore, +env.peak.toFixed(3)]];
}

function _GOLF_envBlend_(envLocalDT, envGMT, boundary, preset) {
  const dayPct  = BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(envLocalDT, envGMT, boundary, preset);
  const yearPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(
    envLocalDT,
    envGMT,
    boundary,
    preset,
    { year: 1, month: 0, day: 0, hour: 0 }
  );

  const vd = dayPct  ? _toVec01_(dayPct)  : [0,0,0,0,0];
  const vy = yearPct ? _toVec01_(yearPct) : [0,0,0,0,0];

  const v = new Array(5).fill(0);
  for (let i = 0; i < 5; i++) {
    v[i] = GOLF_CFG.ENV_W_DAY * vd[i] + GOLF_CFG.ENV_W_YEAR * vy[i];
  }

  const sum = v.reduce((a, b) => a + Math.max(0, b), 0) || 1;
  for (let i = 0; i < 5; i++) {
    v[i] = Math.max(0, v[i]) / sum;
  }

  return { vec: v, peak: _peakiness_(v) };
}

function _GOLF_scoreDual_(dmEl, envStemEl, envHiddenEls, env_peak) {
  const resourceEl = _WD_resourceEl_(dmEl);
  const outputEl   = _WD_outputEl_(dmEl);
  const powerEl    = _WD_powerEl_(dmEl);
  const wealthEl   = _WD_wealthEl_(dmEl);

  let exec = GOLF_CFG.EXEC.base;
  let up   = GOLF_CFG.UPSIDE.base;

  const peak = Math.max(0, Math.min(1, Number(env_peak || 0)));
  const hiddenMult = _GOLF_hiddenMult_(peak);

  if (envStemEl === resourceEl) exec += GOLF_CFG.EXEC.resourceStem;
  if (envHiddenEls.includes(resourceEl)) exec += GOLF_CFG.EXEC.resourceHidden * hiddenMult;

  if (envStemEl === powerEl) exec += GOLF_CFG.EXEC.powerStem;
  if (envHiddenEls.includes(powerEl)) exec += GOLF_CFG.EXEC.powerHidden * hiddenMult;

  if (envStemEl === outputEl) exec += GOLF_CFG.EXEC.outputStem;
  if (envStemEl === wealthEl) exec += GOLF_CFG.EXEC.wealthStem;
  if (envStemEl === dmEl) exec += GOLF_CFG.EXEC.peerStem;

  const powerPresent    = (envStemEl === powerEl) || envHiddenEls.includes(powerEl);
  const resourcePresent = (envStemEl === resourceEl) || envHiddenEls.includes(resourceEl);

  if (powerPresent && !resourcePresent) {
    exec += GOLF_CFG.POWER_SUPPORT.noResourcePenaltyExec;
  }
  if (powerPresent && resourcePresent) {
    exec += GOLF_CFG.POWER_SUPPORT.supportedBonusExec;
  }

  exec -= GOLF_CFG.EXEC.peakPenaltyK * peak;

  if (envStemEl === outputEl) up += GOLF_CFG.UPSIDE.outputStem;
  if (envHiddenEls.includes(outputEl)) up += GOLF_CFG.UPSIDE.outputHidden * hiddenMult;

  if (envStemEl === wealthEl) up += GOLF_CFG.UPSIDE.wealthStem;
  if (envHiddenEls.includes(wealthEl)) up += GOLF_CFG.UPSIDE.wealthHidden * hiddenMult;

  if (envStemEl === resourceEl) up += GOLF_CFG.UPSIDE.resourceStem;
  if (envStemEl === powerEl) up += GOLF_CFG.UPSIDE.powerStem;
  if (envStemEl === dmEl) up += GOLF_CFG.UPSIDE.peerStem;

  if (powerPresent && !resourcePresent) {
    up += GOLF_CFG.POWER_SUPPORT.noResourcePenaltyUpside;
  }

  up += GOLF_CFG.UPSIDE.peakPlateauBonusK * _GOLF_plateauBonus_(peak);

  if (peak > GOLF_CFG.UPSIDE.extremeStart) {
    const t = (peak - GOLF_CFG.UPSIDE.extremeStart) / (1 - GOLF_CFG.UPSIDE.extremeStart);
    up -= GOLF_CFG.UPSIDE.peakExtremePenaltyK * Math.max(0, Math.min(1, t));
  }

  exec = Math.max(0, Math.min(100, Math.round(exec)));
  up   = Math.max(0, Math.min(100, Math.round(up)));

  return {
    execScore: exec,
    upsideScore: up,
    execRaw: +exec.toFixed(2),
    upsideRaw: +up.toFixed(2),
    execLabel: _GOLF_execLabel_(exec),
    upsideLabel: _GOLF_upsideLabel_(up)
  };
}

function _GOLF_hiddenMult_(peak) {
  const p = Math.max(0, Math.min(1, Number(peak || 0)));
  const a = GOLF_CFG.HIDDEN_DAMP_START;
  const b = GOLF_CFG.HIDDEN_DAMP_END;

  if (p <= a) return 1;
  if (p >= b) return 0.35;

  const t = (p - a) / (b - a);
  return 1 - (0.65 * t);
}

function _GOLF_plateauBonus_(peak) {
  const p = Math.max(0, Math.min(1, Number(peak || 0)));

  if (p <= 0.20) return p / 0.20 * 0.35;
  if (p <= 0.45) return 0.35 + ((p - 0.20) / 0.25) * 0.65;
  if (p <= 0.65) return 1.0;
  if (p <= 0.82) return 1.0 - ((p - 0.65) / 0.17) * 0.55;

  return 0.45;
}

function _GOLF_execLabel_(score) {
  if (score >= 80) return "Locked In";
  if (score >= 65) return "Clean";
  if (score >= 50) return "Playable";
  if (score >= 35) return "Messy";
  return "Avoid Force";
}

function _GOLF_upsideLabel_(score) {
  if (score >= 80) return "Heater Potential";
  if (score >= 65) return "Birdie Runs";
  if (score >= 50) return "Neutral";
  if (score >= 35) return "Grind Mode";
  return "Blow-Up Risk";
}
