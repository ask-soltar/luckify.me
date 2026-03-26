/****************************************************
 * 06_lookup_events.gs
 * LUCKIFY ME — Event Data Access Layer
 *
 * RULE: Reads from the EVENTS (event_data) sheet only.
 *       Returns event objects. No engine logic.
 *
 * All events are cached on first read (within a single script run)
 * to avoid repeated sheet access.
 ****************************************************/

let _EVENTS_CACHE = null;

/**
 * _loadAllEvents_()
 * Internal helper. Reads EVENTS sheet once and caches in memory.
 * Returns array of event objects.
 */
function _loadAllEvents_() {
  if (_EVENTS_CACHE !== null) {
    return _EVENTS_CACHE;
  }

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(EVENTS.SHEET);

  if (!sheet) {
    console.error("EVENTS sheet '" + EVENTS.SHEET + "' not found");
    return [];
  }

  const lastRow = sheet.getLastRow();
  if (lastRow < EVENTS.START_ROW) {
    _EVENTS_CACHE = [];
    return _EVENTS_CACHE;
  }

  const numRows = lastRow - EVENTS.START_ROW + 1;
  const range = sheet.getRange(EVENTS.START_ROW, 1, numRows, 46); // A through AT
  const values = range.getValues();

  const events = [];
  for (let i = 0; i < values.length; i++) {
    const row = values[i];
    const event = {
      event_id:      row[EVENTS.COL_EVENT_ID - 1],
      tour:          row[EVENTS.COL_TOUR - 1],
      r1_date:       row[EVENTS.COL_R1_DATE - 1],
      r2_date:       row[EVENTS.COL_R2_DATE - 1],
      r3_date:       row[EVENTS.COL_R3_DATE - 1],
      r4_date:       row[EVENTS.COL_R4_DATE - 1],
      gmt:           row[EVENTS.COL_GMT - 1],
      event_title:   row[EVENTS.COL_EVENT_TITLE - 1],
      venue:         row[EVENTS.COL_VENUE - 1],
      location:      row[EVENTS.COL_LOCATION - 1],
      start_time:    row[EVENTS.COL_START_TIME - 1],
      latitude:      row[EVENTS.COL_LATITUDE - 1],
      longitude:     row[EVENTS.COL_LONGITUDE - 1],
      moon_r1_10c:   row[EVENTS.COL_MOON_R1_10C - 1],
      moon_r2_10c:   row[EVENTS.COL_MOON_R2_10C - 1],
      moon_r3_10c:   row[EVENTS.COL_MOON_R3_10C - 1],
      moon_r4_10c:   row[EVENTS.COL_MOON_R4_10C - 1],
      moon_r1_8c:    row[EVENTS.COL_MOON_R1_8C - 1],
      moon_r2_8c:    row[EVENTS.COL_MOON_R2_8C - 1],
      moon_r3_8c:    row[EVENTS.COL_MOON_R3_8C - 1],
      moon_r4_8c:    row[EVENTS.COL_MOON_R4_8C - 1],
      tithi_r1:      row[EVENTS.COL_TITHI_R1 - 1],
      tithi_r2:      row[EVENTS.COL_TITHI_R2 - 1],
      tithi_r3:      row[EVENTS.COL_TITHI_R3 - 1],
      tithi_r4:      row[EVENTS.COL_TITHI_R4 - 1],
      type_r1:       row[EVENTS.COL_TYPE_R1 - 1],
      type_r2:       row[EVENTS.COL_TYPE_R2 - 1],
      type_r3:       row[EVENTS.COL_TYPE_R3 - 1],
      type_r4:       row[EVENTS.COL_TYPE_R4 - 1],
      ascdec_r1:     row[EVENTS.COL_ASCDEC_R1 - 1],
      ascdec_r2:     row[EVENTS.COL_ASCDEC_R2 - 1],
      ascdec_r3:     row[EVENTS.COL_ASCDEC_R3 - 1],
      ascdec_r4:     row[EVENTS.COL_ASCDEC_R4 - 1],
      ws_d1:         row[EVENTS.COL_WS_D1 - 1],
      ws_d2:         row[EVENTS.COL_WS_D2 - 1],
      ws_d3:         row[EVENTS.COL_WS_D3 - 1],
      ws_d4:         row[EVENTS.COL_WS_D4 - 1],
      rnd1_bucket:   row[EVENTS.COL_RND1_BUCKET - 1],
      rnd2_bucket:   row[EVENTS.COL_RND2_BUCKET - 1],
      rnd3_bucket:   row[EVENTS.COL_RND3_BUCKET - 1],
      rnd4_bucket:   row[EVENTS.COL_RND4_BUCKET - 1],
      r1_avg:        row[EVENTS.COL_R1_AVG - 1],
      r2_avg:        row[EVENTS.COL_R2_AVG - 1],
      r3_avg:        row[EVENTS.COL_R3_AVG - 1],
      r4_avg:        row[EVENTS.COL_R4_AVG - 1],
      year:          row[EVENTS.COL_YEAR - 1],

      // Conditions (if present in the new column positions)
      cond_r1:       row[EVENTS.COL_COND_R1 - 1],
      cond_r2:       row[EVENTS.COL_COND_R2 - 1],
      cond_r3:       row[EVENTS.COL_COND_R3 - 1],
      cond_r4:       row[EVENTS.COL_COND_R4 - 1]
    };
    events.push(event);
  }

  _EVENTS_CACHE = events;
  return events;
}

/**
 * getEventById(event_id)
 * Returns the event object with the given event_id (EVT_XXXX).
 * Returns null if not found.
 */
function getEventById(event_id) {
  const events = _loadAllEvents_();
  for (const e of events) {
    if (e.event_id === event_id) {
      return e;
    }
  }
  return null;
}

/**
 * getEventByName(name)
 * Returns the first event with the given event_title (case-sensitive).
 * Returns null if not found.
 */
function getEventByName(name) {
  const events = _loadAllEvents_();
  for (const e of events) {
    if (e.event_title === name) {
      return e;
    }
  }
  return null;
}

/**
 * getAllEvents()
 * Returns array of all event objects.
 */
function getAllEvents() {
  return _loadAllEvents_();
}

/**
 * clearEventCache_()
 * Clears the in-memory cache. Useful if you modify the EVENTS sheet
 * during a script run and need fresh data.
 */
function clearEventCache_() {
  _EVENTS_CACHE = null;
}
