/****************************************************
 * 04_best_round.gs
 * LUCKIFY ME — Best Round Marker
 *
 * RULE: Touches Golf_Analytics sheet.
 *       No engine logic. Reads upside scores, writes best round label.
 ****************************************************/

function FILL_BEST_ROUND() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(GA.SHEET);
  const lastRow = sheet.getLastRow();
  const numRows = lastRow - GA.START_ROW + 1;
  if (numRows < 1) return;

  const scores = sheet.getRange(GA.START_ROW, GA.COL_SCORE_START, numRows, 12).getValues();

  const results = scores.map(function(row) {
    const upsides = [row[1], row[4], row[7], row[10]];
    const labels  = ["R1", "R2", "R3", "R4"];
    let best      = -Infinity;
    let bestLabel = "";

    upsides.forEach(function(u, i) {
      if (u !== "" && u != null && !isNaN(Number(u)) && Number(u) > best) {
        best      = Number(u);
        bestLabel = labels[i];
      }
    });

    return [bestLabel];
  });

  sheet.getRange(GA.START_ROW, GA.COL_BEST_ROUND, numRows, 1).setValues(results);
}
