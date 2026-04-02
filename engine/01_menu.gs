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

  const mainMenu = ui.createMenu("Golf Analytics");

  // ── CORE FILL OPERATIONS ──
  mainMenu.addItem("▶ Fill Blank (Colors + Scores)", "FILL_ALL")
    .addItem("🎨 Fill Blank Colors Only", "FILL_GOLF_COLORS")
    .addItem("📊 Fill Blank Scores Only", "FILL_GOLF_SCORES")
    .addItem("🔁 Force Recompute Everything", "FORCE_RECOMPUTE_ALL")
    .addItem("🏆 Mark Best Round (Upside)", "FILL_BEST_ROUND")
    .addSeparator();

  // ── OVERNIGHT RUNNER ──
  const overnightMenu = ui.createMenu("🌙 Overnight Runner");
  overnightMenu.addItem("Start Overnight Run", "START_OVERNIGHT")
    .addItem("Start from Row X", "START_OVERNIGHT_FROM_ROW")
    .addItem("Force Run (Recompute All)", "START_OVERNIGHT_FORCE")
    .addItem("Colors Only", "START_OVERNIGHT_COLORS_ONLY")
    .addItem("Scores Only", "START_OVERNIGHT_SCORES_ONLY")
    .addSeparator()
    .addItem("Stop Overnight Run", "STOP_OVERNIGHT")
    .addItem("📍 Status", "OVERNIGHT_STATUS")
    .addItem("🔄 Reset Progress", "RESET_OVERNIGHT");
  mainMenu.addSubMenu(overnightMenu)
    .addSeparator();

  // ── 3BMATCHUP OVERNIGHT RUNNER ──
  const overnight3BMMenu = ui.createMenu("🌙 3BMatchup Overnight");
  overnight3BMMenu.addItem("Start Overnight Run", "START_OVERNIGHT_3BM")
    .addItem("Force Run (Recompute All)", "START_OVERNIGHT_3BM_FORCE")
    .addItem("Colors Only", "START_OVERNIGHT_3BM_COLORS_ONLY")
    .addItem("Scores Only", "START_OVERNIGHT_3BM_SCORES_ONLY")
    .addSeparator()
    .addItem("Stop Overnight Run", "STOP_OVERNIGHT_3BM")
    .addItem("📍 Status", "OVERNIGHT_STATUS_3BM")
    .addItem("🔄 Reset Progress", "RESET_OVERNIGHT_3BM");
  mainMenu.addSubMenu(overnight3BMMenu)
    .addSeparator();

  // ── ANALYSIS v3 ──
  const analysisMenu = ui.createMenu("📊 ANALYSIS v3");
  analysisMenu.addItem("🔨 Init ANALYSIS v3 Sheet", "INIT_ANALYSIS_V3_SHEET")
    .addItem("▶ Populate (One-Time)", "POPULATE_ANALYSIS_V3")
    .addItem("▶ Populate (Single Batch)", "POPULATE_ANALYSIS_V3_CHUNKED")
    .addSeparator()
    .addItem("▶▶ Start Auto-Populate", "START_ANALYSIS_V3_AUTO")
    .addItem("⏹ Stop Auto-Populate", "STOP_ANALYSIS_V3_AUTO")
    .addSeparator()
    .addItem("➕ Add Formulas", "ADD_ANALYSIS_V3_FORMULAS")
    .addItem("📊 Build TOUR_STATS", "BUILD_TOUR_STATS")
    .addSeparator()
    .addItem("🔍 Audit Sheet (Check Duplicates)", "AUDIT_ANALYSIS_SHEET");
  mainMenu.addSubMenu(analysisMenu)
    .addSeparator();

  // ── WEATHER CONDITIONS ──
  const conditionsMenu = ui.createMenu("🌤 Conditions");
  conditionsMenu.addItem("Fetch Next Batch", "CONDITIONS_FILL_NEXT_BATCH")
    .addItem("Fetch All Now", "CONDITIONS_FILL_ALL_NOW")
    .addSeparator()
    .addItem("▶▶ Start Auto-Fetch", "CONDITIONS_START_AUTO_FILL")
    .addItem("⏹ Stop Auto-Fetch", "CONDITIONS_STOP_AUTO_FILL")
    .addSeparator()
    .addItem("📍 Status", "CONDITIONS_TRIGGER_STATUS")
    .addItem("🔄 Reset Progress", "CONDITIONS_RESET_PROGRESS");
  mainMenu.addSubMenu(conditionsMenu)
    .addSeparator();

  // ── DEBUG ──
  const debugMenu = ui.createMenu("🧪 Debug");
  debugMenu.addItem("Test Single Row", "TEST_SINGLE_ROW")
    .addItem("Debug Active Row", "DEBUG_ACTIVE_ROW");
  mainMenu.addSubMenu(debugMenu);

  mainMenu.addToUi();
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
      _startOvernightRun_(false, true, true, false);  // resetProgress=false: keep custom row
    } else {
      ui.alert("Invalid row number. Must be >= " + GA.START_ROW);
    }
  }
}
