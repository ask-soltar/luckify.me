/****************************************************
 * 02b_runner_overnight_3bmatchup.gs
 * LUCKIFY ME — 3BMatchup Overnight Runner & Trigger Management
 *
 * RULE: Manages triggers + progress for 3BMatchup sheet only.
 *       Delegates all data processing to 04_writer_3bmatchup.gs
 *       Uses separate property keys to avoid conflicts with Golf_Analytics runner.
 ****************************************************/

/* =========================
   OVERNIGHT CONTROL — PUBLIC MENU HANDLERS
========================= */

function START_OVERNIGHT_3BM() {
  _startOvernightRun3BM_(false, true, true);
}

function START_OVERNIGHT_3BM_FORCE() {
  _startOvernightRun3BM_(true, true, true);
}

function START_OVERNIGHT_3BM_COLORS_ONLY() {
  _startOvernightRun3BM_(false, true, false);
}

function START_OVERNIGHT_3BM_SCORES_ONLY() {
  _startOvernightRun3BM_(false, false, true);
}

function STOP_OVERNIGHT_3BM() {
  _deleteOvernightTriggers3BM_();

  const props = PropertiesService.getScriptProperties();
  props.deleteProperty(PROP_PROGRESS_3BM);
  props.deleteProperty(PROP_FORCE_3BM);
  props.deleteProperty(PROP_DO_COLORS_3BM);
  props.deleteProperty(PROP_DO_SCORES_3BM);

  SpreadsheetApp.getUi().alert("⏹ 3BMatchup overnight run stopped.");
}

function RESET_OVERNIGHT_3BM() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty(PROP_PROGRESS_3BM, "2");
  props.deleteProperty(PROP_LAST_ERROR_3BM);

  SpreadsheetApp.getUi().alert("🔄 3BMatchup overnight progress reset to row 2.");
}

function OVERNIGHT_STATUS_3BM() {
  const props = PropertiesService.getScriptProperties();
  const currentRow = Number(props.getProperty(PROP_PROGRESS_3BM) || 2);
  const force = props.getProperty(PROP_FORCE_3BM) === "true";
  const doColors = props.getProperty(PROP_DO_COLORS_3BM) !== "false";
  const doScores = props.getProperty(PROP_DO_SCORES_3BM) !== "false";
  const lastStart = props.getProperty(PROP_LAST_START_3BM) || "—";
  const lastDone = props.getProperty(PROP_LAST_DONE_3BM) || "—";
  const lastError = props.getProperty(PROP_LAST_ERROR_3BM) || "—";

  const triggers = ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === TRIGGER_FN_3BM);

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_3BMATCHUP);
  const lastRow = sheet ? sheet.getLastRow() : 0;
  const done = lastRow > 0 && currentRow > lastRow;

  const pct = lastRow > 2
    ? Math.min(100, Math.round(((currentRow - 2) / (lastRow - 2)) * 100))
    : 0;

  const msg = [
    done ? "✅ COMPLETE" : "🔄 IN PROGRESS — " + pct + "%",
    "Current row: " + currentRow + " of " + lastRow,
    "Trigger active: " + (triggers.length > 0 ? "Yes" : "No"),
    "Mode: " + (force ? "Force recompute" : "Fill empty only"),
    "Colors: " + (doColors ? "Yes" : "No"),
    "Scores: " + (doScores ? "Yes" : "No"),
    "Writes to: W:AH (3 players × 4 cols)",
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

function OVERNIGHT_CHUNK_3BM() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;

  // Hoisted so catch block can reference it even if the error fires early
  let startRow = 2;

  try {
    const started = Date.now();
    const props = PropertiesService.getScriptProperties();
    props.setProperty(PROP_LAST_START_3BM, new Date().toISOString());
    props.deleteProperty(PROP_LAST_ERROR_3BM);

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_3BMATCHUP);
    if (!sheet) {
      throw new Error("3BMatchup sheet not found");
    }

    const lastRow = sheet.getLastRow();

    startRow = Number(props.getProperty(PROP_PROGRESS_3BM) || 2);
    const force = props.getProperty(PROP_FORCE_3BM) === "true";
    const doColors = props.getProperty(PROP_DO_COLORS_3BM) !== "false";
    const doScores = props.getProperty(PROP_DO_SCORES_3BM) !== "false";

    if (startRow > lastRow) {
      _deleteOvernightTriggers3BM_();
      props.setProperty(PROP_LAST_DONE_3BM, new Date().toISOString());
      Logger.log("3BMatchup overnight run complete.");
      return;
    }

    while (startRow <= lastRow && (Date.now() - started) < MAX_RUN_MILLIS) {
      const endRow = Math.min(startRow + CHUNK_SIZE - 1, lastRow);
      _process3BMatchupChunk_(sheet, startRow, endRow, force, doColors, doScores);
      startRow = endRow + 1;
      props.setProperty(PROP_PROGRESS_3BM, String(startRow));
    }

    props.setProperty(PROP_LAST_DONE_3BM, new Date().toISOString());

    if (startRow > lastRow) {
      _deleteOvernightTriggers3BM_();
      Logger.log("3BMatchup overnight run complete.");
    } else {
      Logger.log("3BMatchup paused at row " + startRow + "; next trigger will continue.");
    }

    logRun3BM_(getEngineVersion_(), started, Date.now(), startRow - 2, "");
  } catch (err) {
    const errMsg = err && err.message ? err.message : String(err);
    PropertiesService.getScriptProperties().setProperty(PROP_LAST_ERROR_3BM, errMsg);
    logRun3BM_(getEngineVersion_(), started, Date.now(), startRow - 2, errMsg);
    throw err;
  } finally {
    lock.releaseLock();
  }
}

/* =========================
   PRIVATE HELPERS
========================= */

function _startOvernightRun3BM_(force, doColors, doScores) {
  _deleteOvernightTriggers3BM_();

  const props = PropertiesService.getScriptProperties();
  props.setProperty(PROP_PROGRESS_3BM, "2");
  props.setProperty(PROP_FORCE_3BM, force ? "true" : "false");
  props.setProperty(PROP_DO_COLORS_3BM, doColors ? "true" : "false");
  props.setProperty(PROP_DO_SCORES_3BM, doScores ? "true" : "false");
  props.deleteProperty(PROP_LAST_START_3BM);
  props.deleteProperty(PROP_LAST_DONE_3BM);
  props.deleteProperty(PROP_LAST_ERROR_3BM);

  ScriptApp.newTrigger(TRIGGER_FN_3BM)
    .timeBased()
    .everyMinutes(TRIGGER_MINS)
    .create();

  SpreadsheetApp.getUi().alert(
    "🌙 3BMatchup overnight run started.\n\n" +
    "Mode: " + (force ? "Force recompute" : "Fill missing only") + "\n" +
    "Colors: " + (doColors ? "Yes" : "No") + "\n" +
    "Scores: " + (doScores ? "Yes" : "No") + "\n" +
    "Writes to: W:AH (3 players × 4 cols)\n" +
    "Chunk size: " + CHUNK_SIZE + "\n" +
    "Trigger interval: every " + TRIGGER_MINS + " minute"
  );
}

function _deleteOvernightTriggers3BM_() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === TRIGGER_FN_3BM)
    .forEach(t => ScriptApp.deleteTrigger(t));
}

function logRun3BM_(engineVersion, startTime, endTime, rowsProcessed, errorMsg) {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  let   sheet = ss.getSheetByName("RUN_LOGS");

  if (!sheet) {
    sheet = ss.insertSheet("RUN_LOGS");
    const headers = ["timestamp", "sheet", "engine_version", "rows_processed", "duration_seconds", "status", "error_message"];
    sheet.appendRow(headers);
    sheet.setFrozenRows(1);
  }

  const durationSeconds = Math.round((endTime - startTime) / 1000);
  const status          = errorMsg ? "ERROR" : "OK";

  sheet.appendRow([
    startTime,
    "3BMatchup",
    engineVersion,
    rowsProcessed,
    durationSeconds,
    status,
    errorMsg || ""
  ]);
}
