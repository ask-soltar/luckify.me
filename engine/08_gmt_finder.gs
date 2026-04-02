/****************************************************
 * 08_gmt_finder.gs
 * LUCKIFY ME — GMT Offset Finder (Google Maps Timezone API)
 *
 * Auto-fills GMT offsets using birthplace location data.
 * Uses Google Geocoding + Timezone APIs.
 * Results cached for 7 days.
 ****************************************************/

const GOOGLE_MAPS_API_KEY = 'AIzaSyBZPFDKssI2v0Q52uqUQfwK8vn2CIrxn_Y';

const CACHE_MINUTES = 7 * 24 * 60; // 7 days
const ROW_PACING_MS = 100;
const SOFT_TIME_BUDGET_MS = 280000; // ~4.7 min safety stop
const USE_DST = false; // false = standard time (rawOffset only)

// Countries with >3 time zones — skip auto-fill for these (manual review needed)
const SKIP_MULTI_ZONE_COUNTRIES = {
  'United States': true,
  'Russia': true,
  'Canada': true,
  'Brazil': true,
  'Mexico': true,
  'Australia': true,
  'Indonesia': true,
  'France': true,
  'China': true,
  'Greenland': true,
  'Kiribati': true,
  'Philippines': true,
  'Micronesia': true,
  'Marshall Islands': true,
  'Palau': true,
  'Kazakhstan': true,
  'Mongolia': true,
  'Democratic Republic of the Congo': true,
  'Samoa': true,
  'Tonga': true
};

const COUNTRY_SYNONYMS = {
  'usa': 'United States','u.s.a.': 'United States','united states of america':'United States','u.s.':'United States','us':'United States',
  'uk':'United Kingdom','u.k.':'United Kingdom','england':'United Kingdom','scotland':'United Kingdom','wales':'United Kingdom','northern ireland':'United Kingdom',
  'russia':'Russian Federation','chechnya':'Russian Federation',
  'south korea':'Korea (Republic of)','north korea':"Korea (Democratic People's Republic of)",
  'czech republic':'Czechia','holland':'Netherlands','burma':'Myanmar',"cote d'ivoire":"Côte d'Ivoire","côte d'ivoire":"Côte d'Ivoire",'cape verde':'Cabo Verde'
};

const REPRESENTATIVE_COUNTRY_CENTER = {
  'United States': { lat: 39.0997, lng: -94.5786, label: 'Kansas City, United States (Central)' },
  'Canada':        { lat: 43.6532, lng: -79.3832, label: 'Toronto, Canada (Eastern)' },
  'Brazil':        { lat: -23.5505, lng: -46.6333, label: 'São Paulo, Brazil (BRT)' },
  'Mexico':        { lat: 19.4326, lng: -99.1332, label: 'Mexico City, Mexico (Central)' },
  'Australia':     { lat: -33.8688, lng: 151.2093, label: 'Sydney, Australia (AEST)' },
  'Russia':        { lat: 55.7558, lng: 37.6173,  label: 'Moscow, Russia (MSK)' },
  'Indonesia':     { lat: -6.2088, lng: 106.8456, label: 'Jakarta, Indonesia (WIB)' },
  'United Kingdom':{ lat: 51.5074, lng: -0.1278,  label: 'London, United Kingdom' },
  'Spain':         { lat: 40.4168, lng: -3.7038,  label: 'Madrid, Spain' },
  'Portugal':      { lat: 38.7223, lng: -9.1393,  label: 'Lisbon, Portugal' },
  'Argentina':     { lat: -34.6037, lng: -58.3816,label: 'Buenos Aires, Argentina' },
  'Chile':         { lat: -33.4489, lng: -70.6693,label: 'Santiago, Chile' },
  'Poland':        { lat: 52.2297, lng: 21.0122,  label: 'Warsaw, Poland' },
  'Jamaica':       { lat: 18.0179, lng: -76.8099, label: 'Kingston, Jamaica' },
  'Iceland':       { lat: 64.1466, lng: -21.9426, label: 'Reykjavík, Iceland' },
  'Ireland':       { lat: 53.3498, lng: -6.2603,  label: 'Dublin, Ireland' },
  'Netherlands':   { lat: 52.3676, lng: 4.9041,   label: 'Amsterdam, Netherlands' },
  'Czechia':       { lat: 50.0755, lng: 14.4378,  label: 'Prague, Czechia' },
  'Ukraine':       { lat: 50.4501, lng: 30.5234,  label: 'Kyiv, Ukraine' },
  'Turkey':        { lat: 41.0082, lng: 28.9784,  label: 'Istanbul, Turkey' },
  'Japan':         { lat: 35.6762, lng: 139.6503, label: 'Tokyo, Japan' },
  'New Zealand':   { lat: -36.8485, lng: 174.7633,label: 'Auckland, New Zealand' }
};


/**
 * AUTO_FILL_GMT_FROM_BIRTHPLACE()
 * Reads BIRTHDAY_VERIFY where action="UPDATE"
 * Uses ESPN birthplace to look up GMT offset
 * Skips countries with >3 time zones (requires manual review)
 * Writes GMT to PLAYERS sheet
 */
function AUTO_FILL_GMT_FROM_BIRTHPLACE() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var playersSheet = ss.getSheetByName(PLAYERS.SHEET);
  var verifySheet = ss.getSheetByName(BIRTHDAY_VERIFY.SHEET);

  if (!playersSheet || !verifySheet) {
    console.error("Required sheets not found");
    return;
  }


  // Read BIRTHDAY_VERIFY to find UPDATE rows
  var lastRow = verifySheet.getLastRow();
  if (lastRow < BIRTHDAY_VERIFY.START_ROW) {
    console.log("No verification data");
    return;
  }

  var verifyRange = verifySheet.getRange(BIRTHDAY_VERIFY.START_ROW, 1, lastRow - BIRTHDAY_VERIFY.START_ROW + 1, BIRTHDAY_VERIFY.COL_NOTES);
  var verifyValues = verifyRange.getValues();

  var updatesToProcess = [];
  var skippedMultiZone = [];

  for (var i = 0; i < verifyValues.length; i++) {
    var row = verifyValues[i];
    var playerName = row[BIRTHDAY_VERIFY.COL_NAME - 1];
    var espnBirthplace = row[BIRTHDAY_VERIFY.COL_ESPN_BIRTHPLACE - 1];
    var action = row[BIRTHDAY_VERIFY.COL_ACTION - 1];

    // Only process UPDATE actions with a birthplace
    if (action === "UPDATE" && espnBirthplace) {
      var birthplaceStr = String(espnBirthplace).trim();
      var country = _extractCountryFromBirthplace_(birthplaceStr);

      // Check if country has >3 time zones
      if (SKIP_MULTI_ZONE_COUNTRIES[country]) {
        skippedMultiZone.push(String(playerName).trim() + " (" + country + ")");
      } else {
        updatesToProcess.push({
          playerName: String(playerName).trim(),
          birthplace: birthplaceStr
        });
      }
    }
  }

  if (updatesToProcess.length === 0) {
    console.log("No UPDATE actions with birthplace found");
    SpreadsheetApp.getUi().alert("No UPDATE actions with birthplace to process.");
    return;
  }

  // Read all PLAYERS data
  var playersLastRow = playersSheet.getLastRow();
  var playersRange = playersSheet.getRange(PLAYERS.START_ROW, 1, playersLastRow - PLAYERS.START_ROW + 1, PLAYERS.COL_GMT);
  var playersValues = playersRange.getValues();

  var gmtUpdates = {};
  var t0 = Date.now();
  var processed = 0;

  // Build map of unique birthplaces to avoid duplicate API calls
  var uniquePlaces = {};
  for (var i = 0; i < updatesToProcess.length; i++) {
    var bp = updatesToProcess[i].birthplace;
    if (!uniquePlaces[bp]) uniquePlaces[bp] = [];
    uniquePlaces[bp].push(updatesToProcess[i].playerName);
  }

  var places = Object.keys(uniquePlaces);

  // Look up GMT for each unique birthplace
  for (var p = 0; p < places.length; p++) {
    if (Date.now() - t0 > SOFT_TIME_BUDGET_MS) break;

    var place = places[p];
    var offset = _getGmtOffsetForPlace_(place, Math.floor(Date.now() / 1000));

    // Map offset to all players with this birthplace
    var players = uniquePlaces[place];
    for (var j = 0; j < players.length; j++) {
      gmtUpdates[players[j]] = offset;
      processed++;
    }

    Utilities.sleep(ROW_PACING_MS);
  }

  // Update PLAYERS sheet with GMT values
  var updateCount = 0;
  for (var i = 0; i < playersValues.length; i++) {
    var pName = String(playersValues[i][PLAYERS.COL_NAME - 1]).trim();
    if (gmtUpdates.hasOwnProperty(pName)) {
      playersValues[i][PLAYERS.COL_GMT - 1] = gmtUpdates[pName] || "";
      updateCount++;
    }
  }

  if (updateCount > 0) {
    playersRange.setValues(playersValues);
    console.log("✓ Updated " + updateCount + " GMT offsets in PLAYERS sheet");
  } else {
    console.log("No GMT updates made");
  }

  // Report skipped multi-zone countries
  if (skippedMultiZone.length > 0) {
    var skipMsg = "Skipped " + skippedMultiZone.length + " players (multi-zone countries):\n" + skippedMultiZone.slice(0, 10).join("\n");
    if (skippedMultiZone.length > 10) skipMsg += "\n... and " + (skippedMultiZone.length - 10) + " more";
    console.log(skipMsg);
    SpreadsheetApp.getUi().alert("✓ Updated " + updateCount + " GMT offsets\n\n" + skipMsg + "\n\n(These need manual review)");
  } else if (updateCount > 0) {
    SpreadsheetApp.getUi().alert("✓ Updated " + updateCount + " GMT offsets");
  }
}

/* ========================= Core lookups ========================= */

function _getGmtOffsetForPlace_(placeRaw, whenEpochSeconds) {
  var place = _normalizePlace_(placeRaw);
  var cacheKey = 'tz:' + place + ':' + whenEpochSeconds + ':' + (USE_DST ? 'dst1' : 'dst0');
  var cached = _getCache_(cacheKey);
  if (cached !== null) return cached;

  var r = _getGmtOffsetWithDiag_(place, whenEpochSeconds);
  var val = (r && !r.error) ? r.offset : "";
  _putCache_(cacheKey, val);
  return val;
}

function _getGmtOffsetWithDiag_(placeRaw, whenEpochSeconds) {
  try {
    var place = _normalizePlace_(placeRaw);
    var parts = place.split(",");
    var partsClean = [];
    for (var pi = 0; pi < parts.length; pi++) {
      var s = String(parts[pi]).trim();
      if (s) partsClean.push(s);
    }

    // Country-only input
    if (partsClean.length === 1) {
      var country = _normalizeCountryName_(partsClean[0]);

      // Try representative center override
      var rep = _getRepresentativeLatLngForCountry_(country);
      if (rep) {
        var tz = _fetchTimezoneOffsetHours_(rep.lat, rep.lng, whenEpochSeconds);
        if (tz.error) return { offset: null, queryUsed: rep.label, error: tz.error };
        return { offset: tz.offset, queryUsed: rep.label, error: null };
      }

      // Fallback: RestCountries capital
      var cap = _fetchCountryCapitalAndLatLng_(country);
      if (!cap) return { offset: null, queryUsed: country, error: 'Country lookup failed' };
      var tz2 = _fetchTimezoneOffsetHours_(cap.lat, cap.lng, whenEpochSeconds);
      if (tz2.error) return { offset: null, queryUsed: cap.capital || country, error: tz2.error };
      return { offset: tz2.offset, queryUsed: cap.capital || country, error: null };
    }

    // City present — use Google Geocoding
    var geo = _geocodeGoogleWithStatus_(place);
    if (geo.error) return { offset: null, queryUsed: place, error: 'Geocoding: ' + geo.status };
    if (!geo.lat || !geo.lng) return { offset: null, queryUsed: place, error: 'No lat/lng' };

    var tz = _fetchTimezoneOffsetHours_(geo.lat, geo.lng, whenEpochSeconds);
    if (tz.error) return { offset: null, queryUsed: place, error: tz.error };
    return { offset: tz.offset, queryUsed: place, error: null };

  } catch (e) {
    return { offset: null, queryUsed: placeRaw, error: String(e) };
  }
}

function _getRepresentativeLatLngForCountry_(countryName) {
  var key = _normalizeCountryName_(countryName);
  return REPRESENTATIVE_COUNTRY_CENTER[key] || null;
}

/* ========================= External APIs ========================= */

function _geocodeGoogleWithStatus_(address) {
  try {
    var url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' +
      encodeURIComponent(address) + '&key=' + encodeURIComponent(GOOGLE_MAPS_API_KEY);
    var res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = res.getResponseCode();
    if (code !== 200) return { status: 'HTTP_' + code, error: 'HTTP error' };

    var data = JSON.parse(res.getContentText());
    var status = (data && data.status) ? data.status : 'NO_STATUS';
    var errMsg = (data && (data.error_message || data.errorMessage)) ? (data.error_message || data.errorMessage) : '';

    if (status !== 'OK' || !data || !data.results || !data.results.length) {
      return { status: status, error: errMsg || 'No results' };
    }
    var loc = data.results[0] && data.results[0].geometry && data.results[0].geometry.location ? data.results[0].geometry.location : null;
    if (!loc) return { status: 'OK', error: 'No geometry.location' };
    return { status: 'OK', error: null, lat: loc.lat, lng: loc.lng };
  } catch (e) {
    return { status: 'EXCEPTION', error: String(e) };
  }
}

function _fetchTimezoneOffsetHours_(lat, lng, epochSeconds) {
  try {
    var url = 'https://maps.googleapis.com/maps/api/timezone/json?' +
      'location=' + encodeURIComponent(lat + ',' + lng) +
      '&timestamp=' + encodeURIComponent(epochSeconds) +
      '&key=' + encodeURIComponent(GOOGLE_MAPS_API_KEY);
    var res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = res.getResponseCode();
    if (code !== 200) return { offset: null, error: 'HTTP ' + code };
    var data = JSON.parse(res.getContentText());
    var status = (data && data.status) ? data.status : 'NO_STATUS';
    if (status !== 'OK') return { offset: null, error: 'TZ API: ' + status };
    if (typeof data.rawOffset !== 'number') return { offset: null, error: 'Missing rawOffset' };

    var raw = data.rawOffset || 0;
    var dst = data.dstOffset || 0;
    var total = USE_DST ? (raw + dst) : raw;
    return { offset: total / 3600, error: null };
  } catch (e) {
    return { offset: null, error: 'Exception: ' + e };
  }
}

function _fetchCountryCapitalAndLatLng_(countryName) {
  try {
    var url = 'https://restcountries.com/v3.1/name/' + encodeURIComponent(countryName) +
      '?fields=capital,capitalInfo,latlng,name,cca2';
    var res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) return null;
    var arr = JSON.parse(res.getContentText());
    if (!arr || !arr.length) return null;
    var c = arr[0];
    var capital = null, lat = null, lng = null;
    if (c && c.capital && c.capital.length) capital = c.capital[0];
    if (c && c.capitalInfo && c.capitalInfo.latlng && c.capitalInfo.latlng.length === 2) {
      lat = c.capitalInfo.latlng[0]; lng = c.capitalInfo.latlng[1];
    } else if (c && c.latlng && c.latlng.length === 2) {
      lat = c.latlng[0]; lng = c.latlng[1];
    }
    if (lat == null || lng == null) return null;
    return { capital: capital, lat: lat, lng: lng };
  } catch (e) {
    return null;
  }
}

/* ========================= Multi-Zone Country Check ========================= */

function _extractCountryFromBirthplace_(birthplaceStr) {
  // Birthplace format: "City, State/Region, Country"
  // Extract the last part (country)
  var parts = birthplaceStr.split(",");
  if (parts.length > 0) {
    var country = String(parts[parts.length - 1]).trim();
    return _normalizeCountryName_(country);
  }
  return "";
}

/* ========================= Formatting ========================= */

function _normalizePlace_(s) {
  s = String(s).trim().replace(/\s+/g, ' ');
  var bits = s.split(",");
  var clean = [];
  for (var i = 0; i < bits.length; i++) {
    var x = String(bits[i]).trim();
    if (x) clean.push(x);
  }
  if (clean.length === 1) return _normalizeCountryName_(clean[0]);
  clean[clean.length - 1] = _normalizeCountryName_(clean[clean.length - 1]);
  return clean.join(", ");
}

function _normalizeCountryName_(name) {
  var key = String(name).trim().toLowerCase();
  if (COUNTRY_SYNONYMS[key]) return COUNTRY_SYNONYMS[key];
  return _titleCase_(name);
}

function _titleCase_(str) {
  return String(str).replace(/\w\S*/g, function(w){ return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase(); });
}

/* ========================= Cache ========================= */

function _getCache_(key) {
  var p = PropertiesService.getScriptProperties();
  var raw = p.getProperty(key);
  if (!raw) return null;
  try {
    var obj = JSON.parse(raw);
    if (Date.now() > obj.expires) { p.deleteProperty(key); return null; }
    return obj.value;
  } catch (e) { return null; }
}

function _putCache_(key, value) {
  var p = PropertiesService.getScriptProperties();
  var expires = Date.now() + CACHE_MINUTES * 60 * 1000;
  p.setProperty(key, JSON.stringify({ value: value, expires: expires }));
}
