/****************************************************
 * 02_runner_overnight.gs
 * LUCKIFY ME — Overnight Runner & Trigger Management
 *
 * RULE: Touches Sheets for progress tracking only.
 *       Delegates all data processing to 03_writer_golf_analytics.gs
 *       Delegates all engine work to 10_–14_ engine files.
 ****************************************************/

/* =========================
   OVERNIGHT CONTROL — PUBLIC MENU HANDLERS
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

/* =========================
   OVERNIGHT WORKER
   Called by the time-based trigger every TRIGGER_MINS minutes.
========================= */

function OVERNIGHT_CHUNK() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;

  // Hoisted so catch block can reference it even if the error fires early
  let startRow = GA.START_ROW;

  try {
    const started = Date.now();
    const props = PropertiesService.getScriptProperties();
    props.setProperty(PROP_LAST_START, new Date().toISOString());
    props.deleteProperty(PROP_LAST_ERROR);

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
    const lastRow = sheet.getLastRow();

    startRow = Number(props.getProperty(PROP_PROGRESS) || GA.START_ROW);
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

    logRun_(getEngineVersion_(), started, Date.now(), startRow - GA.START_ROW, "");
  } catch (err) {
    const errMsg = err && err.message ? err.message : String(err);
    PropertiesService.getScriptProperties().setProperty(PROP_LAST_ERROR, errMsg);
    logRun_(getEngineVersion_(), started, Date.now(), startRow - GA.START_ROW, errMsg);
    throw err;
  } finally {
    lock.releaseLock();
  }
}

/* =========================
   PRIVATE HELPERS
========================= */

function _startOvernightRun_(force, doColors, doScores, resetProgress = true) {
  _deleteOvernightTriggers_();

  const props = PropertiesService.getScriptProperties();
  // Only reset progress if not coming from START_OVERNIGHT_FROM_ROW
  if (resetProgress) {
    props.setProperty(PROP_PROGRESS, String(GA.START_ROW));
  }

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

function _deleteOvernightTriggers_() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === TRIGGER_FN)
    .forEach(t => ScriptApp.deleteTrigger(t));
}
