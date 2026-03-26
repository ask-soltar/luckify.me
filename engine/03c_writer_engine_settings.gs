/****************************************************
 * 03c_writer_engine_settings.gs
 * LUCKIFY ME — Engine Settings Sheet
 *
 * RULE: Only manages the ENGINE_SETTINGS sheet.
 *       All other modules read version via getEngineVersion_().
 ****************************************************/

const ENGINE_SETTINGS_HEADERS = [
  "engine_version", "active", "notes", "last_updated"
];

function initEngineSettings_() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  let   sheet = ss.getSheetByName("ENGINE_SETTINGS");

  if (!sheet) {
    sheet = ss.insertSheet("ENGINE_SETTINGS");
    sheet.appendRow(ENGINE_SETTINGS_HEADERS);
    sheet.setFrozenRows(1);
    sheet.appendRow([ENGINE_VERSION, "true", "", new Date()]);
  }
}

function getEngineVersion_() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("ENGINE_SETTINGS");

  if (!sheet) return ENGINE_VERSION;
  return sheet.getRange("A2").getValue() || ENGINE_VERSION;
}
