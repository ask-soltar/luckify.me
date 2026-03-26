/****************************************************
 * 03b_writer_run_logs.gs
 * LUCKIFY ME — Run Logging
 *
 * RULE: One public function — logRun_().
 *       Creates RUN_LOGS sheet with headers if absent,
 *       then appends one row per engine run.
 ****************************************************/

const RUN_LOGS_HEADERS = [
  "timestamp", "engine_version", "rows_processed",
  "duration_seconds", "status", "error_message"
];

function logRun_(engineVersion, startTime, endTime, rowsProcessed, errorMsg) {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  let   sheet = ss.getSheetByName("RUN_LOGS");

  if (!sheet) {
    sheet = ss.insertSheet("RUN_LOGS");
    sheet.appendRow(RUN_LOGS_HEADERS);
    sheet.setFrozenRows(1);
  }

  const durationSeconds = Math.round((endTime - startTime) / 1000);
  const status          = errorMsg ? "ERROR" : "OK";

  sheet.appendRow([
    startTime,
    engineVersion,
    rowsProcessed,
    durationSeconds,
    status,
    errorMsg || ""
  ]);
}
