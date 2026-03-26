/****************************************************
 * 03_writer_golf_analytics.gs
 * LUCKIFY ME — Golf Analytics Sheet Writer
 *
 * RULE: Reads from and writes to Golf_Analytics sheet.
 *       Calls engine functions — never contains engine logic itself.
 *       All column references use GA config constants from 00_config.gs
 ****************************************************/

/* =========================
   PUBLIC ENTRY — called by 01_menu.gs
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

/* =========================
   CHUNK PROCESSOR
   Called by both _fillSheet_ (immediate) and OVERNIGHT_CHUNK (trigger)
========================= */

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
   SINGLE ROW WRITER
   Called by TEST_SINGLE_ROW in 90_debug_tests.gs
========================= */

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

/* =========================
   OUTPUT ROW BUILDER
   Pure data transformation — builds one output row from one input row.
   Calls engine functions from 10_engine_lucky_day.gs and 12_engine_golf.gs
========================= */

function _buildOutputRow_(sourceRow, existingRow, forceAll, doColors, doScores, rowNumber) {
  const birthday = sourceRow[0];
  const bdayGMT  = sourceRow[1];
  const venueGMT = sourceRow[6];
  const rounds   = [sourceRow[2], sourceRow[3], sourceRow[4], sourceRow[5]];

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

    const colorCol    = idx;
    const scoreOffset = 4 + idx * 3;

    const needColor  = doColors && _needsColor_(existingRow, colorCol, forceAll);
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
      if (computed.exec   !== "") outRow[scoreOffset]     = computed.exec;
      if (computed.upside !== "") outRow[scoreOffset + 1] = computed.upside;
      if (computed.peak   !== "") outRow[scoreOffset + 2] = computed.peak;
    }
  }

  return outRow;
}

/* =========================
   COMPUTE ENGINE OUTPUTS FOR ONE ROUND
   Calls Lucky Day + Golf engine. Caches result in _MEMO.
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

  let color  = "";
  let exec   = "";
  let upside = "";
  let peak   = "";
  let error  = "";

  try {
    const delta = LUCKY_DAY_DELTA(
      birthday, bdayGMT, eventDate, venueGMT,
      9, 0, null, GA.BOUNDARY, GA.PRESET
    );
    const cat = LUCKY_CATEGORY_ALT_FROM_DELTA(delta);
    color = LUCKY_CATEGORY_COLOR(cat);
  } catch (e) {
    error += "[COLOR] " + (e && e.message ? e.message : e) + " ";
  }

  try {
    const result = GOLF_LUCK_SCORES_NO_BIRTH_TIME(
      birthday, bdayGMT, eventDate,
      GA.TEEOFF_TIME, venueGMT, GA.BOUNDARY, GA.PRESET
    );
    exec   = result[0][0];
    upside = result[0][1];
    peak   = result[0][2];
  } catch (e) {
    error += "[SCORES] " + (e && e.message ? e.message : e);
  }

  const out = { color, exec, upside, peak, error: error.trim() };
  _MEMO.roundOutputs[key] = out;
  return out;
}

/* =========================
   GUARD HELPERS
========================= */

function _hasRequiredInputs_(birthday, bdayGMT, venueGMT) {
  return !!birthday &&
    bdayGMT !== "" && bdayGMT != null &&
    venueGMT !== "" && venueGMT != null;
}

function _needsColor_(existingRow, colorCol, forceAll) {
  return forceAll || !existingRow ||
    existingRow[colorCol] === "" || existingRow[colorCol] == null;
}

function _needsScores_(existingRow, scoreOffset, forceAll) {
  return forceAll || !existingRow ||
    existingRow[scoreOffset]     === "" || existingRow[scoreOffset]     == null ||
    existingRow[scoreOffset + 1] === "" || existingRow[scoreOffset + 1] == null ||
    existingRow[scoreOffset + 2] === "" || existingRow[scoreOffset + 2] == null;
}
