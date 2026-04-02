/****************************************************
 * 04_writer_3bmatchup.gs
 * LUCKIFY ME — 3BMatchup Color & Score Writer
 *
 * RULE: Reads from and writes to 3BMatchup sheet.
 *       Calls engine functions (10_–14_) for computation.
 *       Processes one row at a time, three players per row.
 ****************************************************/

/* =========================
   CHUNK PROCESSOR
   Called by both 02b_runner_overnight_3bmatchup.gs (trigger) and direct menu calls.
   Processes rows startRow–endRow, computing colors + scores for each player.
========================= */

function _process3BMatchupChunk_(sheet, startRow, endRow, forceAll, doColors, doScores) {
  const numRows = endRow - startRow + 1;
  if (numRows <= 0) return;

  const data = sheet.getRange(startRow, 1, numRows, 33).getValues();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const rowNum = startRow + i;

    // Extract common inputs
    const eventDate = row[COLS_3BM.EVENT_DATE - 1];        // E
    const eventGMT = row[COLS_3BM.EVENT_GMT - 1];          // F
    const condition = row[COLS_3BM.CONDITION - 1];         // T
    const roundType = row[COLS_3BM.ROUND_TYPE - 1];        // U

    // Extract player data
    const playerA = {
      name: row[COLS_3BM.PLAYER_A - 1],                     // H
      birthday: row[COLS_3BM.BIRTHDAY_A - 1],              // N
      gmt: row[COLS_3BM.GMT_A - 1],                        // O
      label: "A"
    };

    const playerB = {
      name: row[COLS_3BM.PLAYER_B - 1],                     // I
      birthday: row[COLS_3BM.BIRTHDAY_B - 1],              // P
      gmt: row[COLS_3BM.GMT_B - 1],                        // Q
      label: "B"
    };

    const playerC = {
      name: row[COLS_3BM.PLAYER_C - 1],                     // J
      birthday: row[COLS_3BM.BIRTHDAY_C - 1],              // R
      gmt: row[COLS_3BM.GMT_C - 1],                        // S
      label: "C"
    };

    // Process each player
    _writePlayerScores3BM_(sheet, rowNum, playerA, eventDate, eventGMT, COLS_3BM.COLOR_A, forceAll, doColors, doScores);
    _writePlayerScores3BM_(sheet, rowNum, playerB, eventDate, eventGMT, COLS_3BM.COLOR_B, forceAll, doColors, doScores);
    _writePlayerScores3BM_(sheet, rowNum, playerC, eventDate, eventGMT, COLS_3BM.COLOR_C, forceAll, doColors, doScores);
  }
}

/* =========================
   SINGLE PLAYER WRITER
   Computes and writes color + exec/upside/peak for one player in one matchup row.
========================= */

function _writePlayerScores3BM_(sheet, rowNum, player, eventDate, eventGMT, startCol, forceAll, doColors, doScores) {
  // Skip if missing required inputs
  // Note: GMT can be 0, so check explicitly for null/undefined/empty string, not falsy
  if (!player.birthday || player.gmt === "" || player.gmt == null || !eventDate || eventGMT === "" || eventGMT == null) {
    return;
  }

  // Check if already computed (skip if forceAll=false and color exists)
  const colorCell = sheet.getRange(rowNum, startCol);
  if (!forceAll && colorCell.getValue()) {
    return;
  }

  try {
    // Compute color & scores using engine
    const color = doColors ? _computeColor3BM_(player.birthday, player.gmt, eventDate, eventGMT) : "";
    const scores = doScores ? _computeScores3BM_(player.birthday, player.gmt, eventDate, eventGMT) : { exec: "", upside: "", peak: "" };

    // Write results (4 columns: color, exec, upside, peak)
    if (doColors) {
      sheet.getRange(rowNum, startCol).setValue(color);
    }
    if (doScores) {
      sheet.getRange(rowNum, startCol + 1).setValue(scores.exec || "");
      sheet.getRange(rowNum, startCol + 2).setValue(scores.upside || "");
      sheet.getRange(rowNum, startCol + 3).setValue(scores.peak || "");
    }
  } catch (err) {
    Logger.log("Error processing 3BMatchup row " + rowNum + " player " + player.label + ": " + err.message);
  }
}

/* =========================
   ENGINE WRAPPERS — Call actual scoring engines
   Uses the same engine calls as Golf_Analytics writer.
========================= */

function _computeColor3BM_(birthday, gmt, eventDate, eventGMT) {
  // Compute lucky day delta and convert to color
  // Matches the Golf_Analytics computation exactly.

  try {
    const delta = LUCKY_DAY_DELTA(
      birthday, gmt, eventDate, eventGMT,
      9, 0, null, GA.BOUNDARY, GA.PRESET
    );
    const cat = LUCKY_CATEGORY_ALT_FROM_DELTA(delta);
    const color = LUCKY_CATEGORY_COLOR(cat);
    return color || "";
  } catch (err) {
    Logger.log("  Color computation error: " + err.message);
    return "";
  }
}

function _computeScores3BM_(birthday, gmt, eventDate, eventGMT) {
  // Compute exec, upside, peak using Golf engine
  // Matches the Golf_Analytics computation exactly.

  try {
    const result = GOLF_LUCK_SCORES_NO_BIRTH_TIME(
      birthday, gmt, eventDate,
      GA.TEEOFF_TIME, eventGMT, GA.BOUNDARY, GA.PRESET
    );
    return {
      exec: result[0][0] || "",
      upside: result[0][1] || "",
      peak: result[0][2] || ""
    };
  } catch (err) {
    Logger.log("  Scores computation error: " + err.message);
    return { exec: "", upside: "", peak: "" };
  }
}
