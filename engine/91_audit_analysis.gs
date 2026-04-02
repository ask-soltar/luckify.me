/****************************************************
 * 91_audit_analysis.gs
 * LUCKIFY ME — ANALYSIS Sheet Audit
 *
 * Checks for duplicate rows and data integrity
 ****************************************************/

/**
 * AUDIT_ANALYSIS_SHEET()
 * Comprehensive audit of ANALYSIS sheet:
 * - Check for duplicate rows by key (player_id, event_id, round_num)
 * - Verify column counts
 * - Check for missing required data
 * - Report statistics
 */
function AUDIT_ANALYSIS_SHEET() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(ANALYSIS.SHEET);

  if (!sheet) {
    console.error("ANALYSIS sheet not found");
    SpreadsheetApp.getUi().alert("❌ ANALYSIS sheet not found");
    return;
  }

  console.log("=== ANALYSIS SHEET AUDIT ===");

  try {
    var lastRow = sheet.getLastRow();
    var lastCol = sheet.getLastColumn();

    console.log("Sheet dimensions: " + (lastRow - 1) + " data rows × " + lastCol + " columns");

    if (lastRow <= 1) {
      console.log("⚠ No data in ANALYSIS sheet");
      SpreadsheetApp.getUi().alert("⚠ ANALYSIS sheet is empty (header only)");
      return;
    }

    // Read all data (A:C columns for key: player_id, event_id, round_num)
    var range = sheet.getRange(2, 1, lastRow - 1, 3);  // A2:C + lastRow
    var values = range.getValues();

    console.log("Reading " + values.length + " rows for duplicate audit...");

    // Check for duplicates by key (A=player_id, B=event_id, C=round_num)
    var keyMap = {};
    var duplicates = 0;
    var duplicateKeys = [];

    for (var i = 0; i < values.length; i++) {
      var playerId = values[i][0];
      var eventId = values[i][1];
      var roundNum = values[i][2];
      var key = String(playerId) + "|" + String(eventId) + "|" + String(roundNum);

      if (keyMap[key]) {
        duplicates++;
        if (!duplicateKeys.includes(key)) {
          duplicateKeys.push(key);
        }
      } else {
        keyMap[key] = true;
      }
    }

    console.log("\n=== DUPLICATE AUDIT ===");
    console.log("Total rows: " + values.length);
    console.log("Unique keys: " + Object.keys(keyMap).length);
    console.log("Duplicate rows found: " + duplicates);

    if (duplicates > 0) {
      console.log("⚠ Duplicate key combinations (first 10):");
      for (var i = 0; i < Math.min(10, duplicateKeys.length); i++) {
        console.log("  " + duplicateKeys[i]);
      }
    }

    // Check for missing required data
    console.log("\n=== DATA INTEGRITY ===");
    var missingPlayerId = 0;
    var missingEventId = 0;
    var missingRoundNum = 0;

    for (var i = 0; i < values.length; i++) {
      if (!values[i][0] || values[i][0] === "") missingPlayerId++;
      if (!values[i][1] || values[i][1] === "") missingEventId++;
      if (!values[i][2] || values[i][2] === "") missingRoundNum++;
    }

    console.log("Missing player_id: " + missingPlayerId);
    console.log("Missing event_id: " + missingEventId);
    console.log("Missing round_num: " + missingRoundNum);

    // Final verdict
    console.log("\n=== AUDIT VERDICT ===");
    if (duplicates === 0 && missingPlayerId === 0 && missingEventId === 0 && missingRoundNum === 0) {
      console.log("✓ ANALYSIS sheet is CLEAN - No duplicates, no missing required data");
      SpreadsheetApp.getUi().alert("✓ ANALYSIS AUDIT PASSED\n\n" +
        values.length + " unique rows\n" +
        "0 duplicates\n" +
        "0 missing required data\n\n" +
        "Ready for formulas!");
    } else {
      var issues = [];
      if (duplicates > 0) issues.push(duplicates + " duplicates");
      if (missingPlayerId > 0) issues.push(missingPlayerId + " missing player_id");
      if (missingEventId > 0) issues.push(missingEventId + " missing event_id");
      if (missingRoundNum > 0) issues.push(missingRoundNum + " missing round_num");

      console.log("⚠ ISSUES FOUND: " + issues.join(", "));
      SpreadsheetApp.getUi().alert("⚠ AUDIT FOUND ISSUES:\n\n" + issues.join("\n"));
    }

  } catch (err) {
    console.error("✗ Audit error: " + err.toString());
    SpreadsheetApp.getUi().alert("❌ Audit error: " + err.toString());
  }
}
