/****************************************************
 * 09_writer_birthday_verify.gs
 * LUCKIFY ME — Birthday & Birthplace Verification (ESPN + Wikidata)
 *
 * Single sheet: VERIFICATION
 * - Fetches from ESPN + Wikidata
 * - Double-verifies birthdays & birthplaces
 * - Auto-approves DOUBLE_MATCH rows
 * - Allows manual approval of other rows
 ****************************************************/

/**
 * FETCH_VERIFICATION_DATA()
 * Main entry point.
 * - Reads PLAYERS + Golf_Analytics
 * - Fetches ESPN + Wikidata for each unique player
 * - Populates VERIFICATION sheet with all data
 * - Auto-approves DOUBLE_MATCH rows
 */
function FETCH_VERIFICATION_DATA() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var playersSheet = ss.getSheetByName(PLAYERS.SHEET);
  var gaSheet = ss.getSheetByName(GA.SHEET);
  var verifySheet = _getOrCreateVerificationSheet_(ss);

  if (!playersSheet || !gaSheet) {
    console.error("Required sheets not found");
    return;
  }

  // Clear verify sheet (keep headers)
  var verifyLastRow = verifySheet.getLastRow();
  if (verifyLastRow > 1) {
    verifySheet.deleteRows(2, verifyLastRow - 1);
    console.log("Cleared old VERIFICATION data");
  }

  // Read all PLAYERS data
  var playersLastRow = playersSheet.getLastRow();
  var playersRange = playersSheet.getRange(PLAYERS.START_ROW, 1, playersLastRow - PLAYERS.START_ROW + 1, PLAYERS.COL_BIRTHPLACE);
  var playersValues = playersRange.getValues();

  // Build map: player_name → {birthday, birthplace}
  var playerDataMap = {};
  for (var i = 0; i < playersValues.length; i++) {
    var plyRow = playersValues[i];
    var plyName = String(plyRow[PLAYERS.COL_NAME - 1]).trim();
    var plyBday = plyRow[PLAYERS.COL_BIRTHDAY - 1];
    var plyBirthplace = plyRow[PLAYERS.COL_BIRTHPLACE - 1];
    if (plyName) {
      playerDataMap[plyName] = {
        birthday: plyBday || "",
        birthplace: plyBirthplace || ""
      };
    }
  }

  // Extract unique ESPN player IDs from Golf_Analytics
  var gaLastRow = gaSheet.getLastRow();
  var gaDedupeCol = 10; // Column J
  var gaNameCol = 3;    // Column C
  var gaRange = gaSheet.getRange(GA.START_ROW, 1, gaLastRow - GA.START_ROW + 1, gaDedupeCol);
  var gaValues = gaRange.getValues();

  var playerIdSet = {};
  for (var i = 0; i < gaValues.length; i++) {
    var gaRow = gaValues[i];
    var dedupeKey = gaRow[gaDedupeCol - 1];
    var playerName = gaRow[gaNameCol - 1];

    if (!dedupeKey || !playerName) continue;

    var dedupeParts = String(dedupeKey).split("_");
    var espnPlayerId = dedupeParts[dedupeParts.length - 1];

    if (!isNaN(espnPlayerId)) {
      if (!playerIdSet[espnPlayerId]) {
        playerIdSet[espnPlayerId] = String(playerName).trim();
      }
    }
  }

  var espnPlayerIds = Object.keys(playerIdSet);
  console.log("Found " + espnPlayerIds.length + " unique ESPN player IDs");

  var verifyRows = [];
  var processedCount = 0;
  var batchStartTime = new Date().getTime();
  var maxRunTime = 240000; // 4 minutes
  var batchSize = 50;

  // Main loop: fetch ESPN + Wikidata for each player
  for (var i = 0; i < espnPlayerIds.length; i++) {
    var espnPlayerId = espnPlayerIds[i];
    var playerName = playerIdSet[espnPlayerId];

    // Time budget check
    if (new Date().getTime() - batchStartTime > maxRunTime) {
      _writeBatch_(verifySheet, verifyRows);
      console.log("Time limit. Processed " + processedCount + " players. Run again to continue.");
      return;
    }

    // Fetch ESPN
    var espnResult = ESPN_FETCH_ATHLETE_BY_ID_(espnPlayerId);
    var espnBday = (espnResult.found) ? (espnResult.dateOfBirth || "") : "";
    var espnBirthplace = (espnResult.found) ? _cleanBirthplace_(espnResult.birthplace || "") : "";

    // Fetch Wikidata
    var wikidataResult = WIKIDATA_FETCH_BIRTHDAY_(playerName);
    var wikidataBday = (wikidataResult.found) ? (wikidataResult.dateOfBirth || "") : "";
    var wikidataBirthplace = (wikidataResult.found) ? (wikidataResult.birthplace || "") : "";

    // Get current data from PLAYERS
    var currentData = playerDataMap[playerName] || { birthday: "", birthplace: "" };

    // Auto-approval logic
    var actionBday = "";
    var actionBirthplace = "";

    if (espnBday && wikidataBday && espnBday === wikidataBday) {
      actionBday = "UPDATE"; // Auto-approve if ESPN == Wikidata
    }

    if (espnBirthplace && wikidataBirthplace && String(espnBirthplace).trim() === String(wikidataBirthplace).trim()) {
      actionBirthplace = "UPDATE"; // Auto-approve if ESPN == Wikidata
    }

    // Build verification row
    var verifyRow = [
      espnPlayerId,                    // A: player_id
      playerName,                      // B: name
      currentData.birthday || "",      // C: current_birthday
      espnBday,                        // D: espn_birthday
      wikidataBday,                    // E: wikidata_birthday
      "",                              // F: bday_status (formula)
      currentData.birthplace || "",    // G: current_birthplace
      espnBirthplace,                  // H: espn_birthplace
      wikidataBirthplace,              // I: wikidata_birthplace
      "",                              // J: birthplace_status (formula)
      espnPlayerId,                    // K: espn_id
      actionBday,                      // L: action_bday
      actionBirthplace,                // M: action_birthplace
      ""                               // N: notes
    ];

    verifyRows.push(verifyRow);
    processedCount++;

    // Batch write every 50 rows
    if (verifyRows.length >= batchSize) {
      _writeBatch_(verifySheet, verifyRows);
      verifyRows = [];
      console.log("✓ Batch: " + processedCount + " processed");
    }

    Utilities.sleep(300); // Rate limit for ESPN
  }

  // Write remaining rows
  if (verifyRows.length > 0) {
    _writeBatch_(verifySheet, verifyRows);
  }

  console.log("✓ Verification complete. Total: " + processedCount + " players");
}

/**
 * APPLY_VERIFIED_UPDATES()
 * Reads VERIFICATION and applies updates marked as "UPDATE"
 * Updates PLAYERS sheet for both birthdays & birthplaces
 */
function APPLY_VERIFIED_UPDATES() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var playersSheet = ss.getSheetByName(PLAYERS.SHEET);
  var verifySheet = ss.getSheetByName(BIRTHDAY_VERIFY.SHEET);

  if (!playersSheet || !verifySheet) {
    console.error("Required sheets not found");
    return;
  }

  // Read VERIFICATION
  var lastRow = verifySheet.getLastRow();
  if (lastRow < BIRTHDAY_VERIFY.START_ROW) {
    console.log("No verification data");
    return;
  }

  var verifyRange = verifySheet.getRange(BIRTHDAY_VERIFY.START_ROW, 1, lastRow - BIRTHDAY_VERIFY.START_ROW + 1, BIRTHDAY_VERIFY.COL_NOTES);
  var verifyValues = verifyRange.getValues();

  var bdayUpdates = [];
  var birthplaceUpdates = [];

  for (var i = 0; i < verifyValues.length; i++) {
    var row = verifyValues[i];
    var playerName = row[BIRTHDAY_VERIFY.COL_NAME - 1];
    var espnBday = row[BIRTHDAY_VERIFY.COL_ESPN_BDAY - 1];
    var espnBirthplace = row[BIRTHDAY_VERIFY.COL_ESPN_BIRTHPLACE - 1];
    var actionBday = row[BIRTHDAY_VERIFY.COL_ACTION_BDAY - 1];
    var actionBirthplace = row[BIRTHDAY_VERIFY.COL_ACTION_BIRTHPLACE - 1];

    if (actionBday === "UPDATE" && espnBday) {
      bdayUpdates.push({
        playerName: String(playerName).trim(),
        newBday: String(espnBday).trim()
      });
    }

    if (actionBirthplace === "UPDATE" && espnBirthplace) {
      birthplaceUpdates.push({
        playerName: String(playerName).trim(),
        newBirthplace: String(espnBirthplace).trim()
      });
    }
  }

  // Apply updates to PLAYERS sheet
  var playersLastRow = playersSheet.getLastRow();
  var playersRange = playersSheet.getRange(PLAYERS.START_ROW, 1, playersLastRow - PLAYERS.START_ROW + 1, PLAYERS.COL_BIRTHPLACE);
  var playersValues = playersRange.getValues();

  var bdayCount = 0;
  var birthplaceCount = 0;

  // Apply birthday updates
  for (var i = 0; i < bdayUpdates.length; i++) {
    var update = bdayUpdates[i];
    for (var j = 0; j < playersValues.length; j++) {
      var pName = String(playersValues[j][PLAYERS.COL_NAME - 1]).trim();
      if (pName === update.playerName) {
        playersValues[j][PLAYERS.COL_BIRTHDAY - 1] = update.newBday;
        bdayCount++;
        break;
      }
    }
  }

  // Apply birthplace updates
  for (var i = 0; i < birthplaceUpdates.length; i++) {
    var update = birthplaceUpdates[i];
    for (var j = 0; j < playersValues.length; j++) {
      var pName = String(playersValues[j][PLAYERS.COL_NAME - 1]).trim();
      if (pName === update.playerName) {
        playersValues[j][PLAYERS.COL_BIRTHPLACE - 1] = update.newBirthplace;
        birthplaceCount++;
        break;
      }
    }
  }

  // Write back to PLAYERS
  if (bdayCount > 0 || birthplaceCount > 0) {
    playersRange.setValues(playersValues);
    console.log("✓ Updated " + bdayCount + " birthdays, " + birthplaceCount + " birthplaces");
  }
}

/* ========================= Helpers ========================= */

function _writeBatch_(sheet, rows) {
  if (rows.length === 0) return;

  var insertRow = sheet.getLastRow() + 1;
  var dataRows = [];
  var bdayFormulaRows = [];
  var birthplaceFormulaRows = [];

  for (var k = 0; k < rows.length; k++) {
    var row = rows[k];
    // Write all except formulas (F and J)
    dataRows.push([row[0], row[1], row[2], row[3], row[4], row[6], row[7], row[8], row[10], row[11], row[12], row[13]]);

    // Birthday status formula (column F)
    bdayFormulaRows.push(['=IF(AND(D' + (insertRow + k) + '="",E' + (insertRow + k) + '=""),"NOT_FOUND",IF(C' + (insertRow + k) + '="","NEW",IF(AND(D' + (insertRow + k) + '<>"",E' + (insertRow + k) + '<>"",D' + (insertRow + k) + '=E' + (insertRow + k) + ',"DOUBLE_MATCH",IF(TEXT(C' + (insertRow + k) + ',"YYYY-MM-DD")=TEXT(D' + (insertRow + k) + ',"YYYY-MM-DD"),"MATCH","CONFLICT"))))']);

    // Birthplace status formula (column J)
    birthplaceFormulaRows.push(['=IF(AND(H' + (insertRow + k) + '="",I' + (insertRow + k) + '=""),"NOT_FOUND",IF(G' + (insertRow + k) + '="","NEW",IF(AND(H' + (insertRow + k) + '<>"",I' + (insertRow + k) + '<>"",H' + (insertRow + k) + '=I' + (insertRow + k) + ',"DOUBLE_MATCH",IF(G' + (insertRow + k) + '=H' + (insertRow + k) + ',"MATCH","CONFLICT"))))']);
  }

  // Write data
  var dataRange = sheet.getRange(insertRow, 1, rows.length, 12);
  dataRange.setValues(dataRows);

  // Write formulas
  var bdayFormulaRange = sheet.getRange(insertRow, 6, rows.length, 1);
  bdayFormulaRange.setFormulas(bdayFormulaRows);

  var birthplaceFormulaRange = sheet.getRange(insertRow, 10, rows.length, 1);
  birthplaceFormulaRange.setFormulas(birthplaceFormulaRows);
}

function _getOrCreateVerificationSheet_(ss) {
  var sheet = ss.getSheetByName(BIRTHDAY_VERIFY.SHEET);

  if (!sheet) {
    sheet = ss.insertSheet(BIRTHDAY_VERIFY.SHEET);
  }

  // Set headers
  var headers = [
    "player_id",
    "name",
    "current_birthday",
    "espn_birthday",
    "wikidata_birthday",
    "bday_status",
    "current_birthplace",
    "espn_birthplace",
    "wikidata_birthplace",
    "birthplace_status",
    "espn_id",
    "action_bday",
    "action_birthplace",
    "notes"
  ];

  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  console.log("VERIFICATION sheet ready");

  return sheet;
}

function _cleanBirthplace_(birthplaceStr) {
  if (!birthplaceStr) return "";

  var parts = birthplaceStr.split(",");
  var cleaned = [];

  for (var i = 0; i < parts.length; i++) {
    var part = String(parts[i]).trim();
    part = part.replace(/\s+/g, " ");
    if (part) {
      cleaned.push(part);
    }
  }

  return cleaned.join(", ");
}

function _normalizeDateFormat_(dateStr) {
  if (!dateStr) return "";

  dateStr = String(dateStr).trim();

  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    return dateStr;
  }

  if (/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(dateStr)) {
    var parts = dateStr.split("/");
    var part1 = String(parts[0]).padStart(2, "0");
    var part2 = String(parts[1]).padStart(2, "0");
    var year = parts[2];
    var day = part1;
    var month = part2;
    return year + "-" + month + "-" + day;
  }

  return dateStr;
}
