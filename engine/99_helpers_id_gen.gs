/****************************************************
 * 99_helpers_id_gen.gs
 * LUCKIFY ME — ID Generation Helpers
 *
 * Run these functions ONCE to populate player_id and event_id columns.
 * After running, they are no longer needed — delete or archive.
 *
 * Usage:
 *   1. Add column headers "player_id" (A1) and "event_id" (A1) to respective sheets
 *   2. Run GENERATE_PLAYER_IDS() in the console
 *   3. Run GENERATE_EVENT_IDS() in the console
 *   Done. IDs are now in place.
 ****************************************************/

/**
 * GENERATE_PLAYER_IDS()
 * Fills column A (player_id) in the Birthdays sheet with PLY_XXXX IDs.
 * Skips rows that already have IDs.
 * Run once, then can be deleted.
 */
function GENERATE_PLAYER_IDS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(PLAYERS.SHEET);

  if (!sheet) {
    console.error("Sheet '" + PLAYERS.SHEET + "' not found");
    return;
  }

  const lastRow = sheet.getLastRow();
  const range = sheet.getRange(PLAYERS.START_ROW, PLAYERS.COL_PLAYER_ID, lastRow - PLAYERS.START_ROW + 1, 1);
  const values = range.getValues();

  let counter = 1;
  let anyChanges = false;

  for (let i = 0; i < values.length; i++) {
    const currentId = values[i][0];

    // Skip if already has an ID
    if (currentId && String(currentId).startsWith("PLY_")) {
      // Extract the number from existing ID
      const numPart = parseInt(String(currentId).substring(4), 10);
      counter = Math.max(counter, numPart + 1);
      continue;
    }

    // Generate new ID
    values[i][0] = generateId_(ID_PREFIXES.player, counter);
    counter++;
    anyChanges = true;
  }

  if (anyChanges) {
    range.setValues(values);
    console.log("Player IDs generated. Counter: " + counter);
  } else {
    console.log("All players already have IDs.");
  }
}

/**
 * GENERATE_EVENT_IDS()
 * Fills column A (event_id) in the Event_Data sheet with EVT_XXXX IDs.
 * Skips rows that already have IDs.
 * Run once, then can be deleted.
 */
function GENERATE_EVENT_IDS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(EVENTS.SHEET);

  if (!sheet) {
    console.error("Sheet '" + EVENTS.SHEET + "' not found");
    return;
  }

  const lastRow = sheet.getLastRow();
  const range = sheet.getRange(EVENTS.START_ROW, EVENTS.COL_EVENT_ID, lastRow - EVENTS.START_ROW + 1, 1);
  const values = range.getValues();

  let counter = 1;
  let anyChanges = false;

  for (let i = 0; i < values.length; i++) {
    const currentId = values[i][0];

    // Skip if already has an ID
    if (currentId && String(currentId).startsWith("EVT_")) {
      // Extract the number from existing ID
      const numPart = parseInt(String(currentId).substring(4), 10);
      counter = Math.max(counter, numPart + 1);
      continue;
    }

    // Generate new ID
    values[i][0] = generateId_(ID_PREFIXES.event, counter);
    counter++;
    anyChanges = true;
  }

  if (anyChanges) {
    range.setValues(values);
    console.log("Event IDs generated. Counter: " + counter);
  } else {
    console.log("All events already have IDs.");
  }
}
