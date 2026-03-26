/****************************************************
 * 08_writer_conditions.gs
 * LUCKIFY ME — Conditions Sheet Writer & Batch Runner
 *
 * RULE: Reads from and writes to Event_Data sheet only.
 *       Calls 07_fetcher_conditions.gs for weather data.
 *       Calls 14_engine_conditions.gs for scoring.
 *       No direct API calls. No engine logic.
 ****************************************************/

var CONDITIONS_CONFIG = {
  sheetName:      "Event_Data",
  latCol:         11,       // K
  lonCol:         12,       // L
  gmtCol:         6,        // F
  startRow:       2,
  triggerMinutes: 1,
  batchSize:      200,
  maxRunMillis:   330000,   // ~5.5 min

  datePairs: [
    { dateCol: 2, outputCol: 33 }, // B -> AG
    { dateCol: 3, outputCol: 34 }, // C -> AH
    { dateCol: 4, outputCol: 35 }, // D -> AI
    { dateCol: 5, outputCol: 36 }  // E -> AJ
  ]
};

var CONDITIONS_PROP_ROW    = "COND_currentRow";
var CONDITIONS_TRIGGER_FN  = "CONDITIONS_AUTO_FILL_BATCH";

/* =========================
   PUBLIC MENU HANDLERS
========================= */

function CONDITIONS_FILL_NEXT_BATCH() {
  CONDITIONS_PROCESS_BATCH_(false);
}

function CONDITIONS_FILL_ALL_NOW() {
  CONDITIONS_FILL_ALL_REMAINING_();
}

function CONDITIONS_START_AUTO_FILL() {
  CONDITIONS_DELETE_TRIGGER_();
  PropertiesService.getScriptProperties().setProperty(
    CONDITIONS_PROP_ROW,
    String(CONDITIONS_CONFIG.startRow)
  );

  ScriptApp.newTrigger(CONDITIONS_TRIGGER_FN)
    .timeBased()
    .everyMinutes(CONDITIONS_CONFIG.triggerMinutes)
    .create();

  SpreadsheetApp.getUi().alert(
    "Conditions auto-fill started.\n" +
    "Runs every " + CONDITIONS_CONFIG.triggerMinutes + " minute.\n" +
    "Batch size: " + CONDITIONS_CONFIG.batchSize + " rows."
  );
}

function CONDITIONS_STOP_AUTO_FILL() {
  CONDITIONS_DELETE_TRIGGER_();
  SpreadsheetApp.getUi().alert("Conditions auto-fill stopped.");
}

function CONDITIONS_TRIGGER_STATUS() {
  var triggers = ScriptApp.getProjectTriggers().filter(function(t) {
    return t.getHandlerFunction() === CONDITIONS_TRIGGER_FN;
  });

  var sheet      = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONDITIONS_CONFIG.sheetName);
  var lastRow    = sheet.getLastRow();
  var currentRow = Number(
    PropertiesService.getScriptProperties().getProperty(CONDITIONS_PROP_ROW) ||
    CONDITIONS_CONFIG.startRow
  );

  var pct = lastRow > CONDITIONS_CONFIG.startRow
    ? Math.min(100, Math.round(((currentRow - CONDITIONS_CONFIG.startRow) / (lastRow - CONDITIONS_CONFIG.startRow)) * 100))
    : 0;

  SpreadsheetApp.getUi().alert(
    (currentRow > lastRow ? "✅ Complete" : "🔄 In progress — " + pct + "%") + "\n" +
    "Current row: " + currentRow + " of " + lastRow + "\n" +
    "Trigger active: " + (triggers.length > 0 ? "Yes" : "No") + "\n" +
    "Interval: every " + CONDITIONS_CONFIG.triggerMinutes + " minute\n" +
    "Batch size: " + CONDITIONS_CONFIG.batchSize + " rows"
  );
}

function CONDITIONS_RESET_PROGRESS() {
  PropertiesService.getScriptProperties().setProperty(
    CONDITIONS_PROP_ROW,
    String(CONDITIONS_CONFIG.startRow)
  );
  SpreadsheetApp.getUi().alert("Conditions progress reset.");
}

function CONDITIONS_REFRESH_ACTIVE_ROW() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONDITIONS_CONFIG.sheetName);
  var row   = sheet.getActiveRange().getRow();

  if (row < CONDITIONS_CONFIG.startRow) {
    SpreadsheetApp.getUi().alert("Select a data row first.");
    return;
  }

  CONDITIONS_REFRESH_ROW_(sheet, row);
  SpreadsheetApp.getUi().alert("Refreshed row " + row + ".");
}

/* =========================
   TRIGGER WORKER
========================= */

function CONDITIONS_AUTO_FILL_BATCH() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return;

  try {
    CONDITIONS_PROCESS_BATCH_(true);
  } finally {
    lock.releaseLock();
  }
}

function CONDITIONS_FILL_ALL_REMAINING_() {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    var started = Date.now();
    while (Date.now() - started < CONDITIONS_CONFIG.maxRunMillis) {
      var done = CONDITIONS_PROCESS_BATCH_(false);
      if (done) break;
    }
  } finally {
    lock.releaseLock();
  }
}

/* =========================
   CORE BATCH PROCESSOR
========================= */

function CONDITIONS_PROCESS_BATCH_(fromTrigger) {
  var ss    = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(CONDITIONS_CONFIG.sheetName);
  var props = PropertiesService.getScriptProperties();

  var lastRow  = sheet.getLastRow();
  var startRow = Number(props.getProperty(CONDITIONS_PROP_ROW) || CONDITIONS_CONFIG.startRow);

  if (startRow > lastRow) {
    CONDITIONS_DELETE_TRIGGER_();
    return true;
  }

  var endRow  = Math.min(startRow + CONDITIONS_CONFIG.batchSize - 1, lastRow);
  var numRows = endRow - startRow + 1;

  var lastNeededCol = Math.max(
    CONDITIONS_CONFIG.lonCol,
    CONDITIONS_CONFIG.gmtCol,
    CONDITIONS_CONFIG.datePairs[CONDITIONS_CONFIG.datePairs.length - 1].outputCol
  );

  var values = sheet.getRange(startRow, 1, numRows, lastNeededCol).getValues();
  var output = values.map(function(r) { return r.slice(); });

  // Group rows by location to fetch forecast once per unique lat/lon/gmt
  var forecastGroups = {};
  for (var i = 0; i < numRows; i++) {
    var row = values[i];
    var lat = row[CONDITIONS_CONFIG.latCol - 1];
    var lon = row[CONDITIONS_CONFIG.lonCol - 1];
    var gmt = row[CONDITIONS_CONFIG.gmtCol - 1] || 0;

    if (lat === "" || lat == null || lon === "" || lon == null) continue;

    var key = lat + "|" + lon + "|" + gmt;
    if (!forecastGroups[key]) {
      forecastGroups[key] = { lat: lat, lon: lon, gmt: gmt, data: null };
    }
  }

  // Fetch forecast once per unique location
  Object.keys(forecastGroups).forEach(function(key) {
    forecastGroups[key].data = CONDITIONS_FETCH_FORECAST_BATCH_(
      forecastGroups[key].lat,
      forecastGroups[key].lon,
      forecastGroups[key].gmt
    );
  });

  // Process each row
  for (var i = 0; i < numRows; i++) {
    var row = values[i];
    var lat = row[CONDITIONS_CONFIG.latCol - 1];
    var lon = row[CONDITIONS_CONFIG.lonCol - 1];
    var gmt = row[CONDITIONS_CONFIG.gmtCol - 1] || 0;

    if (lat === "" || lat == null || lon === "" || lon == null) continue;

    var groupKey    = lat + "|" + lon + "|" + gmt;
    var forecastMap = forecastGroups[groupKey] ? forecastGroups[groupKey].data : null;

    for (var p = 0; p < CONDITIONS_CONFIG.datePairs.length; p++) {
      var pair     = CONDITIONS_CONFIG.datePairs[p];
      var date     = row[pair.dateCol - 1];
      var existing = row[pair.outputCol - 1];

      if (existing !== "" && existing != null) continue; // keep filled values
      if (!date) continue;

      var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmt);
      var localD     = new Date(new Date(date).getTime() + (gmt * 60 * 60 * 1000));
      var isPast     = localD < localToday;
      var result;

      if (isPast) {
        var archive = CONDITIONS_FETCH_ARCHIVE_(date, lat, lon, gmt);
        if (archive.retry)      result = "Rate Limited - retry";
        else if (archive.error) result = archive.error;
        else                    result = CONDITIONS_CALCULATE_(archive);
      } else {
        if (!forecastMap)            result = "No Forecast";
        else if (forecastMap.retry)  result = "Rate Limited - retry";
        else if (forecastMap.error)  result = forecastMap.error;
        else {
          var dateStr = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmt);
          var dayData = forecastMap[dateStr];
          result = dayData ? CONDITIONS_CALCULATE_(dayData) : "Date Not In Forecast";
        }
      }

      output[i][pair.outputCol - 1] = result;
    }
  }

  // Write only the output columns (AG:AJ)
  var firstOutputCol = CONDITIONS_CONFIG.datePairs[0].outputCol;
  var outWidth       = CONDITIONS_CONFIG.datePairs.length;
  var outVals        = output.map(function(r) {
    return r.slice(firstOutputCol - 1, firstOutputCol - 1 + outWidth);
  });

  sheet.getRange(startRow, firstOutputCol, numRows, outWidth).setValues(outVals);
  props.setProperty(CONDITIONS_PROP_ROW, String(endRow + 1));

  if (endRow >= lastRow) {
    CONDITIONS_DELETE_TRIGGER_();
    return true;
  }

  return false;
}

/* =========================
   SINGLE ROW REFRESH
========================= */

function CONDITIONS_REFRESH_ROW_(sheet, rowNum) {
  var lastNeededCol = Math.max(
    CONDITIONS_CONFIG.lonCol,
    CONDITIONS_CONFIG.gmtCol,
    CONDITIONS_CONFIG.datePairs[CONDITIONS_CONFIG.datePairs.length - 1].outputCol
  );

  var row = sheet.getRange(rowNum, 1, 1, lastNeededCol).getValues()[0];
  var lat = row[CONDITIONS_CONFIG.latCol - 1];
  var lon = row[CONDITIONS_CONFIG.lonCol - 1];
  var gmt = row[CONDITIONS_CONFIG.gmtCol - 1] || 0;

  if (lat === "" || lat == null || lon === "" || lon == null) return;

  var forecastMap = CONDITIONS_FETCH_FORECAST_BATCH_(lat, lon, gmt);
  var results     = [];

  for (var p = 0; p < CONDITIONS_CONFIG.datePairs.length; p++) {
    var pair = CONDITIONS_CONFIG.datePairs[p];
    var date = row[pair.dateCol - 1];
    if (!date) { results.push([""]); continue; }

    var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmt);
    var localD     = new Date(new Date(date).getTime() + (gmt * 60 * 60 * 1000));
    var isPast     = localD < localToday;
    var result;

    if (isPast) {
      var archive = CONDITIONS_FETCH_ARCHIVE_(date, lat, lon, gmt);
      if (archive.retry)      result = "Rate Limited - retry";
      else if (archive.error) result = archive.error;
      else                    result = CONDITIONS_CALCULATE_(archive);
    } else {
      if (forecastMap.retry)       result = "Rate Limited - retry";
      else if (forecastMap.error)  result = forecastMap.error;
      else {
        var dateStr = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmt);
        var dayData = forecastMap[dateStr];
        result = dayData ? CONDITIONS_CALCULATE_(dayData) : "Date Not In Forecast";
      }
    }

    results.push([result]);
  }

  sheet.getRange(rowNum, CONDITIONS_CONFIG.datePairs[0].outputCol, 1, results.length)
    .setValues([results.map(function(x) { return x[0]; })]);
}

/* =========================
   TRIGGER HELPER
========================= */

function CONDITIONS_DELETE_TRIGGER_() {
  ScriptApp.getProjectTriggers()
    .filter(function(t) { return t.getHandlerFunction() === CONDITIONS_TRIGGER_FN; })
    .forEach(function(t) { ScriptApp.deleteTrigger(t); });
}
