/****************************************************
 * 01_menu.gs
 * LUCKIFY ME — Menu & Primary Entry Points
 *
 * RULE: This file touches Sheets (UI only).
 *       No engine logic. No data processing.
 *       All heavy lifting delegated to other modules.
 ****************************************************/

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Golf Analytics")
    .addItem("▶ Fill Blank (Colors + Scores)", "FILL_ALL")
    .addSeparator()
    .addItem("🎨 Fill Blank Colors Only", "FILL_GOLF_COLORS")
    .addItem("📊 Fill Blank Scores Only", "FILL_GOLF_SCORES")
    .addSeparator()
    .addItem("🔁 Force Recompute Everything", "FORCE_RECOMPUTE_ALL")
    .addSeparator()
    .addItem("🏆 Mark Best Round (Upside)", "FILL_BEST_ROUND")
    .addSeparator()
    .addItem("🧪 Test Single Row", "TEST_SINGLE_ROW")
    .addItem("🔍 Debug Active Row", "DEBUG_ACTIVE_ROW")
    .addSeparator()
    .addItem("🌙 Start Overnight Run", "START_OVERNIGHT")
    .addItem("🌙 Start Overnight from Row X", "START_OVERNIGHT_FROM_ROW")
    .addItem("🌙 Start Overnight Force Run", "START_OVERNIGHT_FORCE")
    .addItem("🎨 Start Overnight Colors Only", "START_OVERNIGHT_COLORS_ONLY")
    .addItem("📊 Start Overnight Scores Only", "START_OVERNIGHT_SCORES_ONLY")
    .addItem("⏹ Stop Overnight Run", "STOP_OVERNIGHT")
    .addItem("📍 Overnight Status", "OVERNIGHT_STATUS")
    .addItem("🔄 Reset Overnight Progress", "RESET_OVERNIGHT")
    .addToUi();
}

/* =========================
   PRIMARY ENTRY POINTS
   These call the writer (03_writer_golf_analytics.gs)
========================= */

function FILL_ALL() {
  _fillSheet_(false, true, true);
}

function FILL_GOLF_COLORS() {
  _fillSheet_(false, true, false);
}

function FILL_GOLF_SCORES() {
  _fillSheet_(false, false, true);
}

function FORCE_RECOMPUTE_ALL() {
  _fillSheet_(true, true, true);
}

/* =========================
   OVERNIGHT RUNNERS
========================= */

function START_OVERNIGHT_FROM_ROW() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.prompt(
    "Start Overnight Run from Row:",
    "Enter starting row number (e.g., 24658):",
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() === ui.Button.OK) {
    const startRow = Number(response.getResponseText());
    if (!isNaN(startRow) && startRow >= GA.START_ROW) {
      const props = PropertiesService.getScriptProperties();
      props.setProperty(PROP_PROGRESS, String(startRow));
      _startOvernightRun_(false, true, true);
    } else {
      ui.alert("Invalid row number. Must be >= " + GA.START_ROW);
    }
  }
}
