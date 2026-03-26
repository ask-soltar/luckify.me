/****************************************************
 * 07_fetcher_conditions.gs
 * LUCKIFY ME — Conditions Weather Fetcher
 *
 * RULE: This is the ONLY file that makes API calls for weather.
 *       Returns raw data objects. No scoring. No Sheets writes.
 *       Swap to a paid weather API by changing THIS FILE ONLY.
 *
 * Current API: Open-Meteo (free, no key required)
 * Planned upgrade: paid provider (Tomorrow.io or similar)
 ****************************************************/

var CONDITIONS_MEMO = {
  archive:  {},
  forecast: {}
};

/* =========================
   ARCHIVE FETCHER
   For past dates — uses Open-Meteo historical archive endpoint.
========================= */

function CONDITIONS_FETCH_ARCHIVE_(date, latitude, longitude, gmtOffset) {
  if (isNaN(new Date(date).getTime()))       return { error: "Invalid Date" };
  if (latitude  < -90  || latitude  > 90)   return { error: "Invalid Latitude" };
  if (longitude < -180 || longitude > 180)  return { error: "Invalid Longitude" };

  var dateStr  = CONDITIONS_GET_LOCAL_DATE_STR_(date, gmtOffset);
  var cacheKey = "cond_arc_" + dateStr + "_" + latitude + "_" + longitude;

  // In-memory memo check
  if (CONDITIONS_MEMO.archive[cacheKey]) return CONDITIONS_MEMO.archive[cacheKey];

  // Apps Script cache check (persists 6 hours)
  var cache  = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    CONDITIONS_MEMO.archive[cacheKey] = parsed;
    return parsed;
  }

  var url = "https://archive-api.open-meteo.com/v1/archive"
    + "?latitude="   + latitude
    + "&longitude="  + longitude
    + "&start_date=" + dateStr
    + "&end_date="   + dateStr
    + "&daily=windspeed_10m_max,windgusts_10m_max,precipitation_sum,temperature_2m_max,temperature_2m_min"
    + "&timezone=UTC"
    + "&windspeed_unit=mph"
    + "&temperature_unit=fahrenheit";

  try {
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code     = response.getResponseCode();

    if (code === 429) return { retry: true };
    if (code !== 200) return { error: "API Error " + code };

    var json = JSON.parse(response.getContentText());
    if (!json.daily) return { error: "No Data" };

    var result = {
      wind:    json.daily.windspeed_10m_max[0]   || 0,
      gusts:   json.daily.windgusts_10m_max[0]   || 0,
      precip:  json.daily.precipitation_sum[0]   || 0,
      tempMax: json.daily.temperature_2m_max[0]  || 70,
      tempMin: json.daily.temperature_2m_min[0]  || 70
    };

    CONDITIONS_MEMO.archive[cacheKey] = result;
    cache.put(cacheKey, JSON.stringify(result), 21600);
    return result;
  } catch (e) {
    return { error: e.message };
  }
}

/* =========================
   FORECAST FETCHER
   For future/current dates — fetches 15-day window once per location.
   Returns a map keyed by date string: { "2025-04-10": { wind, gusts, ... } }
========================= */

function CONDITIONS_FETCH_FORECAST_BATCH_(latitude, longitude, gmtOffset) {
  if (latitude  < -90  || latitude  > 90)  return { error: "Invalid Latitude" };
  if (longitude < -180 || longitude > 180) return { error: "Invalid Longitude" };

  var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmtOffset);
  var endDate    = new Date(localToday);
  endDate.setUTCDate(localToday.getUTCDate() + 15);

  var startStr = Utilities.formatDate(localToday, "UTC", "yyyy-MM-dd");
  var endStr   = Utilities.formatDate(endDate,    "UTC", "yyyy-MM-dd");
  var cacheKey = "cond_fc_" + startStr + "_" + latitude + "_" + longitude;

  if (CONDITIONS_MEMO.forecast[cacheKey]) return CONDITIONS_MEMO.forecast[cacheKey];

  var cache  = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    CONDITIONS_MEMO.forecast[cacheKey] = parsed;
    return parsed;
  }

  var url = "https://api.open-meteo.com/v1/forecast"
    + "?latitude="   + latitude
    + "&longitude="  + longitude
    + "&start_date=" + startStr
    + "&end_date="   + endStr
    + "&daily=windspeed_10m_max,windgusts_10m_max,precipitation_sum,temperature_2m_max,temperature_2m_min"
    + "&timezone=UTC"
    + "&windspeed_unit=mph"
    + "&temperature_unit=fahrenheit";

  try {
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code     = response.getResponseCode();

    if (code === 429) return { retry: true };
    if (code !== 200) return { error: "API Error " + code };

    var json = JSON.parse(response.getContentText());
    if (!json.daily || !json.daily.time) return { error: "No Data" };

    var result = {};
    for (var i = 0; i < json.daily.time.length; i++) {
      result[json.daily.time[i]] = {
        wind:    json.daily.windspeed_10m_max[i]  || 0,
        gusts:   json.daily.windgusts_10m_max[i]  || 0,
        precip:  json.daily.precipitation_sum[i]  || 0,
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
   SHEET FORMULA ENTRY POINT
   Called directly from a cell formula: =CONDITIONS(date, lat, lon, gmt)
========================= */

function CONDITIONS(date, latitude, longitude, gmtOffset) {
  gmtOffset      = gmtOffset || 0;
  var localToday = CONDITIONS_GET_LOCAL_TODAY_(gmtOffset);
  var localD     = new Date(new Date(date).getTime() + (gmtOffset * 60 * 60 * 1000));
  var isPast     = localD < localToday;

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
