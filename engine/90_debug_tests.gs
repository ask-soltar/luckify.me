/****************************************************
 * 90_debug_tests.gs
 * LUCKIFY ME — Debug & Test Functions
 *
 * RULE: May touch Sheets for testing purposes only.
 *       Never called in production runs.
 *       All test functions are menu-triggered manually.
 ****************************************************/

function TEST_SINGLE_ROW() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const row   = sheet.getActiveRange().getRow();

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
  const row   = sheet.getActiveRange().getRow();

  if (row < GA.START_ROW) {
    SpreadsheetApp.getUi().alert("Select a data row first (row 2 or below).");
    return;
  }

  const vals     = sheet.getRange(row, GA.READ_START_COL, 1, GA.READ_NUM_COLS).getValues()[0];
  const birthday = vals[0];
  const bdayGMT  = vals[1];
  const venueGMT = vals[6];
  const rounds   = [vals[2], vals[3], vals[4], vals[5]];

  const lines = [];
  lines.push("Row " + row);
  lines.push("birthday = " + birthday);
  lines.push("bdayGMT  = " + bdayGMT);
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
      " | date="   + eventDate +
      " | color="  + computed.color +
      " | exec="   + computed.exec +
      " | upside=" + computed.upside +
      " | peak="   + computed.peak +
      " | error="  + (computed.error || "—")
    );
  }

  Logger.log(lines.join("\n"));
  SpreadsheetApp.getUi().alert("Debug written to Apps Script logs for row " + row + ".");
}
