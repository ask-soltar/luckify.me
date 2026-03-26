/****************************************************
 * 98_auto_add_missing_players.gs
 * LUCKIFY ME — Auto-add Missing Players from Golf_Analytics
 *
 * Scans Golf_Analytics for player names not in PLAYERS sheet.
 * Automatically adds them with generated player_id.
 *
 * Usage:
 *   Run AUTO_ADD_MISSING_PLAYERS() in the console
 ****************************************************/

/**
 * AUTO_ADD_MISSING_PLAYERS()
 * - Reads all player names from Golf_Analytics (column C)
 * - Checks against PLAYERS sheet
 * - Adds missing players with auto-generated player_id
 */
function AUTO_ADD_MISSING_PLAYERS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const gaSheet = ss.getSheetByName(GA.SHEET);
  const playersSheet = ss.getSheetByName(PLAYERS.SHEET);

  if (!gaSheet) {
    console.error("Golf_Analytics sheet not found");
    return;
  }

  if (!playersSheet) {
    console.error("PLAYERS sheet not found");
    return;
  }

  // Get all existing player names
  const existingPlayers = getAllPlayers();
  const existingNames = {};
  let maxPlayerId = 0;

  for (const p of existingPlayers) {
    existingNames[p.name] = true;
    // Extract number from PLY_XXXX
    const numPart = parseInt(String(p.player_id).substring(4), 10);
    maxPlayerId = Math.max(maxPlayerId, numPart);
  }

  // Scan Golf_Analytics for unique player names
  const lastRow = gaSheet.getLastRow();
  if (lastRow < GA.START_ROW) {
    console.log("No data in Golf_Analytics");
    return;
  }

  const gaRange = gaSheet.getRange(GA.START_ROW, 3, lastRow - GA.START_ROW + 1, 1); // Column C (Player)
  const gaValues = gaRange.getValues();

  const uniqueNames = {};
  for (let i = 0; i < gaValues.length; i++) {
    const playerName = gaValues[i][0];
    if (playerName && playerName.trim()) {
      uniqueNames[playerName] = true;
    }
  }

  // Find missing players
  const playersToAdd = [];
  for (const name in uniqueNames) {
    if (!existingNames[name]) {
      playersToAdd.push(name);
    }
  }

  if (playersToAdd.length === 0) {
    console.log("No missing players to add.");
    return;
  }

  // Add missing players to PLAYERS sheet
  const playersLastRow = playersSheet.getLastRow();
  let insertRow = playersLastRow + 1;
  let counter = maxPlayerId + 1;

  const rowsToAdd = [];
  for (const playerName of playersToAdd) {
    const playerId = generateId_(ID_PREFIXES.player, counter);
    counter++;

    // Row: [player_id, name, birthday, birthplace, gmt, human_check, element, horoscope, horo_bucket, first_red, pers_card, soul_card, bc_pattern, numer_bucket, tithi_num, tithi_type]
    const newRow = [
      playerId,     // A: player_id
      playerName,   // B: name
      "",           // C: birthday (blank — to be filled manually)
      "",           // D: birthplace
      "",           // E: gmt
      "",           // F: human_check
      "",           // G: element
      "",           // H: horoscope
      "",           // I: horo_bucket
      "",           // J: first_red
      "",           // K: pers_card
      "",           // L: soul_card
      "",           // M: bc_pattern
      "",           // N: numer_bucket
      "",           // O: tithi_num
      ""            // P: tithi_type
    ];
    rowsToAdd.push(newRow);
  }

  // Insert rows
  if (rowsToAdd.length > 0) {
    const insertRange = playersSheet.getRange(insertRow, 1, rowsToAdd.length, 16);
    insertRange.setValues(rowsToAdd);
    console.log("✓ Added " + rowsToAdd.length + " missing players to PLAYERS sheet.");
    console.log("  Remember to fill in birthday and gmt for these players manually.");
  }

  // Clear cache so next import sees the new players
  clearPlayerCache_();
}
