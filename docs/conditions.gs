/****************************************************
 * LUCKIFY ME — GOLF CONDITIONS (FAST MENU VERSION)
 ****************************************************/

var CONDITIONS_CONFIG = {
  sheetName: "Event_Data",
  latCol: 11,        // K
  lonCol: 12,        // L
  gmtCol: 6,         // F
  startRow: 2,
  triggerMinutes: 1, // faster than 5
  batchSize: 200,    // rows per execution
  maxRunMillis: 330000, // ~5.5 min safety window

  datePairs: [
    { dateCol: 2, outputCol: 33 }, // B -> AG
    { dateCol: 3, outputCol: 34 }, // C -> AH
    { dateCol: 4, outputCol: 35 }, // D -> AI
    { dateCol: 5, outputCol: 36 }  // E -> AJ
  ]
};

var CONDITIONS_PROP_ROW = "COND_currentRow";
var CONDITIONS_TRIGGER_FN = "CONDITIONS_AUTO_FILL_BATCH";
var CONDITIONS_MEMO = {
  archive: {},
  forecast: {}
};

/* =========================
   MENU WRAPPERS
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

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONDITIONS_CONFIG.sheetName);
  var lastRow = sheet.getLastRow();
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
  var row = sheet.getActiveRange().getRow();

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
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(CONDITIONS_CONFIG.sheetName);
  var props = PropertiesService.getScriptProperties();

  var lastRow = sheet.getLastRow();
  var startRow = Number(props.getProperty(CONDITIONS_PROP_ROW) || CONDITIONS_CONFIG.startRow);

  if (startRow > lastRow) {
    CONDITIONS_DELETE_TRIGGER_();
    return true;
  }

  var endRow = Math.min(startRow + CONDITIONS_CONFIG.batchSize - 1, lastRow);
  var numRows = endRow - startRow + 1;

  var lastNeededCol = Math.max(
    CONDITIONS_CONFIG.lonCol,
    CONDITIONS_CONFIG.gmtCol,
    CONDITIONS_CONFIG.datePairs[CONDITIONS_CONFIG.datePairs.length - 1].outputCol
  );

  var values = sheet.getRange(startRow, 1, numRows, lastNeededCol).getValues();

  // Clone current full row values for output
  var output = values.map(function(r) { return r.slice(); });

  // Build forecast groups by lat/lon/gmt
  var forecastGroups = {};
  for (var i = 0; i < numRows; i++) {
    var row = values[i];
    var lat = row[CONDITIONS_CONFIG.latCol - 1];
    var lon = row[CONDITIONS_CONFIG.lonCol - 1];
    var gmt = row[CONDITIONS_CONFIG.gmtCol - 1] || 0;

    if (lat === "" || lat == null || lon === "" || lon == null) continue;

    var key = lat + "|" + lon + "|" + gmt;
    if (!forecastGroups[key]) {
      forecastGroups[key] = {
        lat: lat,
        lon: lon,
        gmt: gmt,
        data: null
      };
    }
  }

  // Fetch forecast once per location+gmt
  Object.keys(forecastGroups).forEach(function(key) {
    forecastGroups[key].data = CONDITIONS_FETCH_FORECAST_BATCH_(
      forecastGroups[key].lat,
      forecastGroups[key].lon,
      forecastGroups[key].gmt
    );
  });

  // Process each row in memory
  for (var i = 0; i < numRows; i++) {
    var row = values[i];
    var lat = row[CONDITIONS_CONFIG.latCol - 1];
    var lon = row[CONDITIONS_CONFIG.lonCol - 1];
    var gmt = row[CONDITIONS_CONFIG.gmtCol - 1] || 0;

    if (lat === "" || lat == null || lon === "" || lon == null) continue;

    var groupKey = lat + "|" + lon + "|" + gmt;
    var forecastMap = forecastGroups[groupKey] ? forecastGroups[groupKey].data : null;

    for (var p = 0; p < CONDITIONS_CONFIG.datePairs.length; p++) {
      var pair = CONDITIONS_CONFIG.datePairs[p];
      var date = row[pair.dateCol - 1];
      var existing = row[pair.outputCol - 1];

      // keep filled values
      if (existing !== "" && existing != null) continue;
      if (!date) continue;

      var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmt);
      var localD = new Date(new Date(date).getTime() + (gmt * 60 * 60 * 1000));
      var isPast = localD < localToday;

      var result;
      if (isPast) {
        var archive = CONDITIONS_FETCH_ARCHIVE_(date, lat, lon, gmt);
        if (archive.retry) {
          result = "Rate Limited - retry";
        } else if (archive.error) {
          result = archive.error;
        } else {
          result = CONDITIONS_CALCULATE_(archive);
        }
      } else {
        if (!forecastMap) {
          result = "No Forecast";
        } else if (forecastMap.retry) {
          result = "Rate Limited - retry";
        } else if (forecastMap.error) {
          result = forecastMap.error;
        } else {
          var dateStr = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmt);
          var dayData = forecastMap[dateStr];
          result = dayData ? CONDITIONS_CALCULATE_(dayData) : "Date Not In Forecast";
        }
      }

      output[i][pair.outputCol - 1] = result;
    }
  }

  // Write back only AG:AJ
  var firstOutputCol = CONDITIONS_CONFIG.datePairs[0].outputCol;
  var outWidth = CONDITIONS_CONFIG.datePairs.length;
  var outVals = output.map(function(r) {
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
  var results = [];

  for (var p = 0; p < CONDITIONS_CONFIG.datePairs.length; p++) {
    var pair = CONDITIONS_CONFIG.datePairs[p];
    var date = row[pair.dateCol - 1];
    if (!date) {
      results.push([""]);
      continue;
    }

    var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmt);
    var localD = new Date(new Date(date).getTime() + (gmt * 60 * 60 * 1000));
    var isPast = localD < localToday;
    var result;

    if (isPast) {
      var archive = CONDITIONS_FETCH_ARCHIVE_(date, lat, lon, gmt);
      if (archive.retry) result = "Rate Limited - retry";
      else if (archive.error) result = archive.error;
      else result = CONDITIONS_CALCULATE_(archive);
    } else {
      if (forecastMap.retry) result = "Rate Limited - retry";
      else if (forecastMap.error) result = forecastMap.error;
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
   HELPERS
========================= */

function CONDITIONS_DELETE_TRIGGER_() {
  ScriptApp.getProjectTriggers()
    .filter(function(t) { return t.getHandlerFunction() === CONDITIONS_TRIGGER_FN; })
    .forEach(function(t) { ScriptApp.deleteTrigger(t); });
}

function CONDITIONS_GET_LOCAL_DATE_STR_(date, gmtOffset) {
  var d = new Date(date);
  var localMs = d.getTime() + (gmtOffset * 60 * 60 * 1000);
  return Utilities.formatDate(new Date(localMs), "UTC", "yyyy-MM-dd");
}

function CONDITIONS_GET_LOCAL_TODAY_(gmtOffset) {
  var now = new Date();
  var localMs = now.getTime() + (gmtOffset * 60 * 60 * 1000);
  var local = new Date(localMs);
  local.setUTCHours(0, 0, 0, 0);
  return local;
}

/* =========================
   FETCHERS
========================= */

function CONDITIONS_FETCH_ARCHIVE_(date, latitude, longitude, gmtOffset) {
  var d = new Date(date);
  if (isNaN(d.getTime())) return { error: "Invalid Date" };
  if (latitude < -90 || latitude > 90) return { error: "Invalid Latitude" };
  if (longitude < -180 || longitude > 180) return { error: "Invalid Longitude" };

  var dateStr = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmtOffset);
  var cacheKey = "cond_arc_" + dateStr + "_" + latitude + "_" + longitude;

  if (CONDITIONS_MEMO.archive[cacheKey]) return CONDITIONS_MEMO.archive[cacheKey];

  var cache = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    CONDITIONS_MEMO.archive[cacheKey] = parsed;
    return parsed;
  }

  var url = "https://archive-api.open-meteo.com/v1/archive"
    + "?latitude=" + latitude
    + "&longitude=" + longitude
    + "&start_date=" + dateStr
    + "&end_date=" + dateStr
    + "&daily=windspeed_10m_max,windgusts_10m_max,precipitation_sum,temperature_2m_max,temperature_2m_min"
    + "&timezone=UTC"
    + "&windspeed_unit=mph"
    + "&temperature_unit=fahrenheit";

  try {
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = response.getResponseCode();

    if (code === 429) return { retry: true };
    if (code !== 200) return { error: "API Error " + code };

    var json = JSON.parse(response.getContentText());
    if (!json.daily) return { error: "No Data" };

    var result = {
      wind: json.daily.windspeed_10m_max[0] || 0,
      gusts: json.daily.windgusts_10m_max[0] || 0,
      precip: json.daily.precipitation_sum[0] || 0,
      tempMax: json.daily.temperature_2m_max[0] || 70,
      tempMin: json.daily.temperature_2m_min[0] || 70
    };

    CONDITIONS_MEMO.archive[cacheKey] = result;
    cache.put(cacheKey, JSON.stringify(result), 21600);
    return result;
  } catch (e) {
    return { error: e.message };
  }
}

function CONDITIONS_FETCH_FORECAST_BATCH_(latitude, longitude, gmtOffset) {
  if (latitude < -90 || latitude > 90) return { error: "Invalid Latitude" };
  if (longitude < -180 || longitude > 180) return { error: "Invalid Longitude" };

  var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmtOffset);
  var endDate = new Date(localToday);
  endDate.setUTCDate(localToday.getUTCDate() + 15);

  var startStr = Utilities.formatDate(localToday, "UTC", "yyyy-MM-dd");
  var endStr = Utilities.formatDate(endDate, "UTC", "yyyy-MM-dd");
  var cacheKey = "cond_fc_" + startStr + "_" + latitude + "_" + longitude;

  if (CONDITIONS_MEMO.forecast[cacheKey]) return CONDITIONS_MEMO.forecast[cacheKey];

  var cache = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    CONDITIONS_MEMO.forecast[cacheKey] = parsed;
    return parsed;
  }

  var url = "https://api.open-meteo.com/v1/forecast"
    + "?latitude=" + latitude
    + "&longitude=" + longitude
    + "&start_date=" + startStr
    + "&end_date=" + endStr
    + "&daily=windspeed_10m_max,windgusts_10m_max,precipitation_sum,temperature_2m_max,temperature_2m_min"
    + "&timezone=UTC"
    + "&windspeed_unit=mph"
    + "&temperature_unit=fahrenheit";

  try {
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = response.getResponseCode();

    if (code === 429) return { retry: true };
    if (code !== 200) return { error: "API Error " + code };

    var json = JSON.parse(response.getContentText());
    if (!json.daily || !json.daily.time) return { error: "No Data" };

    var result = {};
    for (var i = 0; i < json.daily.time.length; i++) {
      result[json.daily.time[i]] = {
        wind: json.daily.windspeed_10m_max[i] || 0,
        gusts: json.daily.windgusts_10m_max[i] || 0,
        precip: json.daily.precipitation_sum[i] || 0,
        tempMax: json.daily.temperature_2m_max[i] || 70,
        tempMin: json.daily.temperature_2m_min[i] || 70
      };
    }

    CONDITIONS_MEMO.forecast[cacheKey] = result;
    cache.put(cacheKey, JSON.stringify(result), 21600);
    return result;
  } catch (e) {
    return { error: e.message };
  }
}

/* =========================
   SCORE
========================= */

function CONDITIONS_CALCULATE_(data) {
  var avgTemp = (data.tempMax + data.tempMin) / 2;
  var score = 0;

  if      (data.wind >= 25) score += 4;
  else if (data.wind >= 18) score += 3;
  else if (data.wind >= 12) score += 2;
  else if (data.wind >= 7)  score += 1;

  if      (data.gusts >= 35) score += 2;
  else if (data.gusts >= 25) score += 1;

  if      (avgTemp < 40) score += 2;
  else if (avgTemp < 55) score += 1;
  else if (avgTemp > 90) score += 1;

  if      (data.precip >= 10) score += 2;
  else if (data.precip >= 3)  score += 1;

  if      (score >= 6) return "Tough";
  else if (score >= 3) return "Moderate";
  else                 return "Calm";
}

/* =========================
   SHEET FORMULA
========================= */

function CONDITIONS(date, latitude, longitude, gmtOffset) {
  gmtOffset = gmtOffset || 0;
  var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmtOffset);
  var localD = new Date(new Date(date).getTime() + (gmtOffset * 60 * 60 * 1000));
  var isPast = localD < localToday;

  if (isPast) {
    var archive = CONDITIONS_FETCH_ARCHIVE_(date, latitude, longitude, gmtOffset);
    if (archive.retry) return "Rate Limited - retry";
    if (archive.error) return archive.error;
    return CONDITIONS_CALCULATE_(archive);
  } else {
    var forecastMap = CONDITIONS_FETCH_FORECAST_BATCH_(latitude, longitude, gmtOffset);
    if (forecastMap.retry) return "Rate Limited - retry";
    if (forecastMap.error) return forecastMap.error;
    var dateStr = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmtOffset);
    var dayData = forecastMap[dateStr];
    if (!dayData) return "Date Not In Forecast";
    return CONDITIONS_CALCULATE_(dayData);
  }
}