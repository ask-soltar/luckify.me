/****************************************************
 * 96_wire_golf_analytics.gs
 * LUCKIFY ME — Wire Golf_Analytics K:Q to PLAYERS/EVENTS
 *
 * Replaces manually entered values in Golf_Analytics columns K:Q
 * with lookup formulas that pull from PLAYERS and EVENTS sheets.
 *
 * K (birthday) and L (birth_gmt): VLOOKUP from PLAYERS by player name
 * M-P (round dates) and Q (venue_gmt): INDEX/MATCH from EVENTS by event title
 *
 * Usage:
 *   Run WIRE_GOLF_ANALYTICS_FORMULAS() in the console
 *   It will set formulas for all rows in Golf_Analytics
 ****************************************************/

/**
 * WIRE_GOLF_ANALYTICS_FORMULAS()
 * Main function. Writes lookup formulas to Golf_Analytics K:Q.
 */
function WIRE_GOLF_ANALYTICS_FORMULAS() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const gaSheet = ss.getSheetByName(GA.SHEET);

  if (!gaSheet) {
    console.error("Golf_Analytics sheet not found");
    return;
  }

  const lastRow = gaSheet.getLastRow();
  if (lastRow < GA.START_ROW) {
    console.log("No data in Golf_Analytics");
    return;
  }

  const numRows = lastRow - GA.START_ROW + 1;

  // Build formula arrays for each column (K through Q)
  const formulas = [];

  for (let i = 0; i < numRows; i++) {
    const rowNum = GA.START_ROW + i;

    // Column B (event name) and Column C (player name) references
    const bRef = "B" + rowNum;
    const cRef = "C" + rowNum;

    // K: Birthday (VLOOKUP from PLAYERS)
    const kFormula = '=IFERROR(VLOOKUP(' + cRef + ',PLAYERS!B:E,2,0),"")';

    // L: Birth GMT (VLOOKUP from PLAYERS)
    const lFormula = '=IFERROR(VLOOKUP(' + cRef + ',PLAYERS!B:E,4,0),"")';

    // M: R1 Date (INDEX/MATCH from EVENTS)
    const mFormula = '=IFERROR(INDEX(EVENTS!C:C,MATCH(' + bRef + ',EVENTS!H:H,0)),"")';

    // N: R2 Date
    const nFormula = '=IFERROR(INDEX(EVENTS!D:D,MATCH(' + bRef + ',EVENTS!H:H,0)),"")';

    // O: R3 Date
    const oFormula = '=IFERROR(INDEX(EVENTS!E:E,MATCH(' + bRef + ',EVENTS!H:H,0)),"")';

    // P: R4 Date
    const pFormula = '=IFERROR(INDEX(EVENTS!F:F,MATCH(' + bRef + ',EVENTS!H:H,0)),"")';

    // Q: Venue GMT
    const qFormula = '=IFERROR(INDEX(EVENTS!G:G,MATCH(' + bRef + ',EVENTS!H:H,0)),"")';

    formulas.push([kFormula, lFormula, mFormula, nFormula, oFormula, pFormula, qFormula]);
  }

  // Write all formulas at once (K:Q for all rows)
  const formulaRange = gaSheet.getRange(GA.START_ROW, 11, numRows, 7); // Columns K-Q
  formulaRange.setFormulas(formulas);

  console.log("✓ Wired " + numRows + " rows in Golf_Analytics columns K:Q");
  console.log("  Formulas now reference PLAYERS and EVENTS sheets.");
}
