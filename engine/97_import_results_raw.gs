/****************************************************
 * 97_import_results_raw.gs
 * LUCKIFY ME — Import Results from Golf_Analytics to RESULTS_RAW
 *
 * Reads Golf_Analytics rows, looks up player_id and event_id,
 * and populates RESULTS_RAW with the scores.
 *
 * Usage:
 *   Run IMPORT_RESULTS_FROM_GOLF_ANALYTICS() in the console
 *   It will process all rows in Golf_Analytics and create entries in RESULTS_RAW
 ****************************************************/

/**
 * IMPORT_RESULTS_FROM_GOLF_ANALYTICS()
 * Main import function.
 * - Reads Golf_Analytics (rows 2+)
 * - Looks up player_id from Player name (column C)
 * - Looks up event_id from Event_Name (column B)
 * - Writes to RESULTS_RAW with result_id, player_id, event_id, scores, total, status
 */
function IMPORT_RESULTS_FROM_GOLF_ANALYTICS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const gaSheet = ss.getSheetByName(GA.SHEET);
  const rrSheet = ss.getSheetByName(RESULTS_RAW.SHEET);

  if (!gaSheet) {
    console.error("Golf_Analytics sheet not found");
    return;
  }

  if (!rrSheet) {
    console.error("RESULTS_RAW sheet not found");
    return;
  }

  // Load all players and events for lookup
  const players = getAllPlayers();
  const events = getAllEvents();

  // Build lookup maps by name
  const playersByName = {};
  for (const p of players) {
    playersByName[p.name] = p.player_id;
  }

  const eventsByName = {};
  for (const e of events) {
    eventsByName[e.event_title] = e.event_id;
  }

  // Read Golf_Analytics
  const lastRow = gaSheet.getLastRow();
  if (lastRow < GA.START_ROW) {
    console.log("No data in Golf_Analytics");
    return;
  }

  const gaRange = gaSheet.getRange(GA.START_ROW, 1, lastRow - GA.START_ROW + 1, 200);
  const gaValues = gaRange.getValues();

  // Column indices (0-based, since we're reading from column 1)
  const COL_EVENT_NAME = 1;      // B = index 1
  const COL_PLAYER = 2;          // C = index 2
  const COL_R1 = 3;              // D = index 3
  const COL_R2 = 4;              // E = index 4
  const COL_R3 = 5;              // F = index 5
  const COL_R4 = 6;              // G = index 6
  const COL_TOTAL = 7;           // H = index 7
  const COL_STATUS = 8;          // I = index 8

  // Prepare rows to insert into RESULTS_RAW
  const resultsToInsert = [];
  let resultCounter = 1;
  let matchCount = 0;
  let skipCount = 0;

  for (let i = 0; i < gaValues.length; i++) {
    const row = gaValues[i];
    const eventName = row[COL_EVENT_NAME];
    const playerName = row[COL_PLAYER];
    const r1 = row[COL_R1];
    const r2 = row[COL_R2];
    const r3 = row[COL_R3];
    const r4 = row[COL_R4];
    const total = row[COL_TOTAL];
    const status = row[COL_STATUS];

    // Skip empty rows
    if (!eventName || !playerName) {
      skipCount++;
      continue;
    }

    // Look up IDs
    const playerId = playersByName[playerName];
    const eventId = eventsByName[eventName];

    if (!playerId || !eventId) {
      console.warn("No ID match for " + playerName + " / " + eventName);
      skipCount++;
      continue;
    }

    // Build result_id
    const resultId = generateId_(ID_PREFIXES.result, resultCounter);
    resultCounter++;

    // Build row for RESULTS_RAW
    const resultRow = [
      resultId,           // A: result_id
      playerId,           // B: player_id
      eventId,            // C: event_id
      r1 || "",           // D: r1_score
      r2 || "",           // E: r2_score
      r3 || "",           // F: r3_score
      r4 || "",           // G: r4_score
      total || "",        // H: total
      status || "",       // I: status
      "",                 // J: notes
      new Date()          // K: created_at
    ];

    resultsToInsert.push(resultRow);
    matchCount++;
  }

  // Write to RESULTS_RAW
  if (resultsToInsert.length > 0) {
    const insertRange = rrSheet.getRange(RESULTS_RAW.START_ROW, 1, resultsToInsert.length, 11);
    insertRange.setValues(resultsToInsert);
    console.log("✓ Imported " + matchCount + " results. Skipped " + skipCount + " rows.");
  } else {
    console.log("No results to import.");
  }
}
