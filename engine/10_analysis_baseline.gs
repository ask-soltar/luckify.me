/****************************************************
 * 10_analysis_baseline.gs
 * LUCKIFY ME — Analysis Layer: Baseline Formulas
 *
 * Builds ANALYSIS sheet with measurement model.
 * Columns: player, event, round, score, condition, color, exec, upside
 * Plus calculated: course_avg, diff_course_avg, player_hist_par
 *
 * Step 1: Initialize sheet structure
 * Step 2: Populate from Golf_Analytics
 * Step 3: Add formulas for calculations
 ****************************************************/

/**
 * INIT_COURSES_SHEET()
 * Creates COURSES sheet and extracts unique courses from EVENTS.
 * You then fill in PAR for each course.
 */
function INIT_COURSES_SHEET() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var eventsSheet = ss.getSheetByName(EVENTS.SHEET);
  var coursesSheet = ss.getSheetByName(COURSES.SHEET);

  if (!eventsSheet) {
    console.error("EVENTS sheet not found");
    return;
  }

  // Create COURSES sheet if needed
  if (!coursesSheet) {
    coursesSheet = ss.insertSheet(COURSES.SHEET);
  } else {
    // Clear existing data (keep headers)
    var lastRow = coursesSheet.getLastRow();
    if (lastRow > 1) {
      coursesSheet.deleteRows(2, lastRow - 1);
    }
  }

  // Set headers
  var headers = ["course_id", "course_name", "location", "notes"];
  coursesSheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Extract unique courses from EVENTS
  var eventsLastRow = eventsSheet.getLastRow();
  var eventsRange = eventsSheet.getRange(EVENTS.START_ROW, 1, eventsLastRow - EVENTS.START_ROW + 1, EVENTS.COL_LOCATION);
  var eventsValues = eventsRange.getValues();

  var uniqueCourses = {};

  for (var i = 0; i < eventsValues.length; i++) {
    var eventRow = eventsValues[i];
    var venue = String(eventRow[EVENTS.COL_VENUE - 1]).trim();
    var location = String(eventRow[EVENTS.COL_LOCATION - 1]).trim();

    if (venue && !uniqueCourses[venue]) {
      uniqueCourses[venue] = location;
    }
  }

  // Write unique courses (no par — par is event+year specific now)
  var courseRows = [];
  var courseId = 1;

  for (var venue in uniqueCourses) {
    var location = uniqueCourses[venue];
    courseRows.push([
      "COURSE_" + String(courseId).padStart(3, "0"),  // A: course_id
      venue,                                            // B: course_name
      location,                                         // C: location
      ""                                                // D: notes
    ]);
    courseId++;
  }

  if (courseRows.length > 0) {
    var writeRange = coursesSheet.getRange(COURSES.START_ROW, 1, courseRows.length, courseRows[0].length);
    writeRange.setValues(courseRows);
    console.log("✓ Created COURSES sheet with " + courseRows.length + " unique courses");
    console.log("→ Next: run INIT_EVENTS_COURSES_SHEET() to set up par by event+year");
  }
}

/**
 * INIT_EVENTS_COURSES_SHEET()
 * Creates EVENTS_COURSES junction table.
 * Maps each event to its courses and par by year.
 * You fill in the par values and course sequences.
 */
function INIT_EVENTS_COURSES_SHEET() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var eventsSheet = ss.getSheetByName(EVENTS.SHEET);
  var coursesSheet = ss.getSheetByName(COURSES.SHEET);
  var ecSheet = ss.getSheetByName(EVENTS_COURSES.SHEET);

  if (!eventsSheet || !coursesSheet) {
    console.error("Required sheets not found");
    return;
  }

  // Create EVENTS_COURSES sheet if needed
  if (!ecSheet) {
    ecSheet = ss.insertSheet(EVENTS_COURSES.SHEET);
  } else {
    var lastRow = ecSheet.getLastRow();
    if (lastRow > 1) {
      ecSheet.deleteRows(2, lastRow - 1);
    }
  }

  // Set headers
  var headers = ["event_id", "course_id", "year", "par", "course_sequence", "notes"];
  ecSheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Read EVENTS
  var eventsLastRow = eventsSheet.getLastRow();
  var eventsRange = eventsSheet.getRange(EVENTS.START_ROW, 1, eventsLastRow - EVENTS.START_ROW + 1, EVENTS.COL_LOCATION);
  var eventsValues = eventsRange.getValues();

  // Read COURSES
  var coursesLastRow = coursesSheet.getLastRow();
  var coursesRange = coursesSheet.getRange(COURSES.START_ROW, 1, coursesLastRow - COURSES.START_ROW + 1, COURSES.COL_LOCATION);
  var coursesValues = coursesRange.getValues();

  // Build map: course_name → course_id
  var courseNameToId = {};
  for (var i = 0; i < coursesValues.length; i++) {
    var courseRow = coursesValues[i];
    var courseId = courseRow[COURSES.COL_COURSE_ID - 1];
    var courseName = String(courseRow[COURSES.COL_COURSE_NAME - 1]).trim();
    courseNameToId[courseName] = courseId;
  }

  // Create stub rows (one per event, assuming single course for now)
  // User can edit to add multiple courses per event
  var ecRows = [];
  var year = new Date().getFullYear();

  for (var i = 0; i < eventsValues.length; i++) {
    var eventRow = eventsValues[i];
    var eventId = eventRow[EVENTS.COL_EVENT_ID - 1] || "";
    var eventTitle = eventRow[EVENTS.COL_EVENT_TITLE - 1] || "";
    var venue = String(eventRow[EVENTS.COL_VENUE - 1]).trim();

    if (!eventId) continue;

    var courseId = courseNameToId[venue] || "";

    ecRows.push([
      eventId,                // A: event_id
      courseId,               // B: course_id
      year,                   // C: year (current year)
      "",                     // D: par (YOU FILL IN)
      1,                      // E: course_sequence (1st course)
      ""                      // F: notes
    ]);
  }

  if (ecRows.length > 0) {
    var writeRange = ecSheet.getRange(EVENTS_COURSES.START_ROW, 1, ecRows.length, ecRows[0].length);
    writeRange.setValues(ecRows);
    console.log("✓ Created EVENTS_COURSES with " + ecRows.length + " stub rows");
    console.log("→ Fill in PAR for each event+course+year combination");
    console.log("→ For multi-course events, add extra rows with course_sequence = 2, 3, etc.");
  }
}

/**
 * INIT_ANALYSIS_SHEET()
 * Creates ANALYSIS sheet with headers.
 * Does not populate data yet.
 */
function INIT_ANALYSIS_SHEET() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);

  if (!analysisSheet) {
    analysisSheet = ss.insertSheet(ANALYSIS.SHEET);
  }

  var headers = [
    "player_id",
    "player_name",
    "event_id",
    "event_name",
    "round_num",
    "score",
    "par",
    "course_avg",
    "diff_course_avg",
    "condition",
    "color",
    "exec",
    "upside",
    "player_hist_par",
    "diff_player_hist_par"
  ];

  analysisSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  console.log("✓ ANALYSIS sheet initialized with headers");

  return analysisSheet;
}

/**
 * POPULATE_ANALYSIS_FROM_GOLF_ANALYTICS()
 * Reads Golf_Analytics and populates ANALYSIS sheet base columns.
 * Extracts one row per round played.
 *
 * Base columns (values): player_id, player_name, event_id, event_name, round_num, score, par, condition
 * Formula columns: course_avg, diff_course_avg, color, exec, upside, player_hist_par, diff_player_hist_par
 */
function POPULATE_ANALYSIS_FROM_GOLF_ANALYTICS() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var gaSheet = ss.getSheetByName(GA.SHEET);
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);

  if (!gaSheet || !analysisSheet) {
    console.error("Required sheets not found");
    return;
  }

  // Read Golf_Analytics
  var gaLastRow = gaSheet.getLastRow();
  var gaRange = gaSheet.getRange(GA.START_ROW, 1, gaLastRow - GA.START_ROW + 1, GA.COL_COND_R4);
  var gaValues = gaRange.getValues();

  var analysisRows = [];

  // Extract one row per round (R1, R2, R3, R4)
  for (var i = 0; i < gaValues.length; i++) {
    var gaRow = gaValues[i];

    var playerId = gaRow[GA.COL_PLAYER_ID - 1] || "";  // May be blank
    var playerName = gaRow[GA.COL_PLAYER - 1];
    var eventId = gaRow[GA.COL_EVENT_ID - 1] || "";    // May be blank
    var eventName = gaRow[GA.COL_VENUE - 1];
    var year = gaRow[GA.COL_YEAR - 1];

    // Scores and conditions
    var scores = [
      gaRow[GA.COL_R1 - 1],
      gaRow[GA.COL_R2 - 1],
      gaRow[GA.COL_R3 - 1],
      gaRow[GA.COL_R4 - 1]
    ];

    var conditions = [
      gaRow[GA.COL_COND_R1 - 1],
      gaRow[GA.COL_COND_R2 - 1],
      gaRow[GA.COL_COND_R3 - 1],
      gaRow[GA.COL_COND_R4 - 1]
    ];

    // Extract color/exec/upside (will be populated via VLOOKUP later)
    var colors = [
      gaRow[GA.COL_COLOR_START - 1],
      gaRow[GA.COL_COLOR_START],
      gaRow[GA.COL_COLOR_START + 1],
      gaRow[GA.COL_COLOR_START + 2]
    ];

    // Create one row per round
    for (var round = 0; round < 4; round++) {
      var score = scores[round];
      if (!score || score === "") continue; // Skip empty rounds

      var analysisRow = [
        playerId,                    // A: player_id
        playerName,                  // B: player_name
        eventId,                     // C: event_id
        eventName,                   // D: event_name
        round + 1,                   // E: round_num (1-4)
        score,                       // F: score
        "",                          // G: par (will VLOOKUP from EVENTS)
        "",                          // H: course_avg (will calculate)
        "",                          // I: diff_course_avg (formula: F - H)
        conditions[round] || "",     // J: condition
        colors[round] || "",         // K: color (from engine)
        "",                          // L: exec (from engine)
        "",                          // M: upside (from engine)
        "",                          // N: player_hist_par (formula)
        ""                           // O: diff_player_hist_par (formula: F - N)
      ];

      analysisRows.push(analysisRow);
    }
  }

  // Write all rows
  if (analysisRows.length > 0) {
    var insertRow = ANALYSIS.START_ROW;
    var writeRange = analysisSheet.getRange(insertRow, 1, analysisRows.length, analysisRows[0].length);
    writeRange.setValues(analysisRows);

    console.log("✓ Populated ANALYSIS with " + analysisRows.length + " rounds");
  }
}

/**
 * INIT_ANALYSIS_V3_SHEET()
 * Renames existing ANALYSIS sheet to ANALYSIS_v2.
 * Creates new ANALYSIS sheet with v3 headers (24 columns).
 */
function INIT_ANALYSIS_V3_SHEET() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var existingSheet = ss.getSheetByName(ANALYSIS.SHEET);

  // Rename existing ANALYSIS to ANALYSIS_v2
  if (existingSheet) {
    existingSheet.setName("ANALYSIS_v2");
    console.log("✓ Renamed existing ANALYSIS sheet to ANALYSIS_v2");
  }

  // Create new ANALYSIS sheet
  var newSheet = ss.insertSheet(ANALYSIS.SHEET);

  // Define v3 headers (36 columns A-AJ)
  var headers = [
    "player_id",           // A
    "player_name",         // B
    "event_id",            // C
    "event_name",          // D
    "year",                // E
    "round_num",           // F
    "score",               // G
    "par",                 // H
    "course_avg",          // I
    "vs_avg",              // J
    "condition",           // K
    "round_type",          // L
    "color",               // M
    "exec",                // N
    "upside",              // O
    "peak",                // P
    "moon",                // Q
    "wu_xing",             // R
    "zodiac",              // S
    "life_path",           // T
    "tithi",               // U
    "gap",                 // V
    "tour",                // W
    "is_best_round",       // X
    "horoscope",           // Y (populated data)
    "moonwest",            // Z (populated data)
    "player_hist_par",     // AA (formula)
    "player_his_cnt",      // AB (formula)
    "off_par",             // AC (formula)
    "exec_bucket",         // AD (formula)
    "upside_bucket",       // AE (formula)
    "gap_bucket",          // AF (formula)
    "adj_his_par",         // AG (formula)
    "tournament_type",     // AH (formula)
    "Birthday",            // AI (formula: XLOOKUP from PLAYERS)
    "Personal Year"        // AJ (formula: numerology calculation)
  ];

  newSheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  console.log("✓ Created ANALYSIS v3 sheet with 36 columns (A-AJ)");
}

/**
 * START_ANALYSIS_V3_AUTO()
 * Creates a time-based trigger to run POPULATE_ANALYSIS_V3_CHUNKED every 1 minute.
 * Continues until completion message appears.
 */
function START_ANALYSIS_V3_AUTO() {
  // Remove any existing triggers first
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === "POPULATE_ANALYSIS_V3_CHUNKED")
    .forEach(t => ScriptApp.deleteTrigger(t));

  // Create new 1-minute trigger
  ScriptApp.newTrigger("POPULATE_ANALYSIS_V3_CHUNKED")
    .timeBased()
    .everyMinutes(1)
    .create();

  SpreadsheetApp.getUi().alert("▶▶ ANALYSIS v3 auto-populate started. Runs every 1 minute until complete.\nCheck logs for progress. Stop with ⏹ menu item.");
}

/**
 * STOP_ANALYSIS_V3_AUTO()
 * Deletes the auto-trigger for POPULATE_ANALYSIS_V3_CHUNKED.
 */
function STOP_ANALYSIS_V3_AUTO() {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === "POPULATE_ANALYSIS_V3_CHUNKED")
    .forEach(t => ScriptApp.deleteTrigger(t));

  SpreadsheetApp.getUi().alert("⏹ ANALYSIS v3 auto-populate stopped.");
}

/**
 * ADD_ANALYSIS_V3_FORMULAS()
 * Adds formula columns to ANALYSIS v3 after population is complete.
 * Formulas: AA, AB, AC, AD, AE, AF, AG
 * (Columns Y, Z are populated data: horoscope, moonwest)
 */
function ADD_ANALYSIS_V3_FORMULAS() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(ANALYSIS.SHEET);
  if (!sheet) {
    console.error("ANALYSIS sheet not found");
    return;
  }

  var lastRow = sheet.getLastRow();
  if (lastRow < ANALYSIS_V3.START_ROW) {
    console.error("No data in ANALYSIS sheet");
    return;
  }

  // Define formulas for each column (row 2 is the template, will auto-adjust when copied down)
  var formulas = {
    AA: '=IFERROR(AVERAGEIFS($AC:$AC,$B:$B,B2,$K:$K,K2,$AC:$AC,"<>"),"")',
    AB: '=IFERROR(COUNTIFS($B:$B,B2,$K:$K,K2,$AC:$AC,"<>"),"")',
    AC: '=IFERROR(IF(OR(AH2="T",AH2="P",AH2="M"),"",G2-H2),"")',
    AD: '=IFERROR(IF(N2<25,"0-25",IF(N2<50,"25-50",IF(N2<75,"50-75","75-100"))),"")',
    AE: '=IFERROR(IF(O2<25,"0-25",IF(O2<50,"25-50",IF(O2<75,"50-75","75-100"))),"")',
    AF: '=IFERROR(IF(V2>=20,"20-30",IF(V2>=10,"10-20",IF(V2>=0,"0-10",IF(V2>=-10,"-10-0",IF(V2>=-20,"-20--10","<-20"))))),"")',
    AG: '=IFERROR(IF(AB2<2,"",(AA2*AB2+VLOOKUP(K2,TOUR_STATS!$A$2:$B$4,2,0)*10)/(AB2+10)),"")',
    AH: '=IFERROR(INDEX(EVENTS!BG:BG,MATCH(C2,EVENTS!A:A,0)),"")',
    AI: '=IFERROR(XLOOKUP(A2,PLAYERS!A:A,PLAYERS!C:C,""),"")',
    AJ: '=IF(OR(AI2="",E2=""),"",LET(b,AI2,y,E2,mRed,MOD(MONTH(b)-1,9)+1,dRed,MOD(DAY(b)-1,9)+1,yRed,MOD(SUMPRODUCT(MID(y&"",SEQUENCE(LEN(y&"")),1)*1)-1,9)+1,total,mRed+dRed+yRed,IF(MOD(total,9)=0,9,MOD(total,9))))'
  };

  // Column index mapping (AA=27, AB=28, AC=29, AD=30, AE=31, AF=32, AG=33, AH=34, AI=35, AJ=36)
  var colMap = {AA: 27, AB: 28, AC: 29, AD: 30, AE: 31, AF: 32, AG: 33, AH: 34, AI: 35, AJ: 36};

  // Add formulas for each column
  for (var col in formulas) {
    var colNum = colMap[col];
    var formula = formulas[col];
    sheet.getRange(ANALYSIS_V3.START_ROW, colNum).setFormula(formula);
  }

  // Copy formulas down to all data rows
  for (var col in formulas) {
    var colNum = colMap[col];
    var sourceRange = sheet.getRange(ANALYSIS_V3.START_ROW, colNum);
    var targetRange = sheet.getRange(ANALYSIS_V3.START_ROW, colNum, lastRow - ANALYSIS_V3.START_ROW + 1, 1);
    sourceRange.copyTo(targetRange);
  }

  console.log("✓ Added formulas to columns AA, AB, AC, AD, AE, AF, AG, AH, AI, AJ");
  SpreadsheetApp.getUi().alert("✓ Formulas added to ANALYSIS v3 (columns AA-AJ). All rows updated.");
}

/**
 * POPULATE_ANALYSIS_V3_CHUNKED()
 * Chunked version: processes Golf_Analytics in batches to avoid 6-min timeout.
 * Call this repeatedly from menu or as a time-based trigger.
 * FIX: Clears ANALYSIS sheet on first run to prevent duplicate appends.
 */
function POPULATE_ANALYSIS_V3_CHUNKED() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var gaSheet = ss.getSheetByName(GA.SHEET);
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);
  var gaLastRow = gaSheet.getLastRow();

  if (!analysisSheet) {
    console.error("ANALYSIS sheet not found");
    return;
  }

  var props = PropertiesService.getScriptProperties();
  var lastProcessedRow = Number(props.getProperty("ANALYSIS_V3_PROGRESS") || GA.START_ROW);

  // CLEAR ANALYSIS on first run (when starting from GA.START_ROW)
  if (lastProcessedRow === GA.START_ROW) {
    var analysisLastRow = analysisSheet.getLastRow();
    if (analysisLastRow > ANALYSIS_V3.START_ROW) {
      analysisSheet.deleteRows(ANALYSIS_V3.START_ROW, analysisLastRow - ANALYSIS_V3.START_ROW + 1);
      console.log("✓ Cleared ANALYSIS sheet before population");
    }
  }

  if (lastProcessedRow > gaLastRow) {
    console.log("✓ ANALYSIS v3 population complete!");
    props.deleteProperty("ANALYSIS_V3_PROGRESS");
    SpreadsheetApp.getUi().alert("✓ ANALYSIS v3 population complete! Now run: Menu → 📊 ANALYSIS v3 → \"➕ Add Formulas\"");
    return;
  }

  var chunkSize = 10000;  // Process 10000 GA rows per execution
  var endRow = Math.min(lastProcessedRow + chunkSize - 1, gaLastRow);

  _populateAnalysisV3Batch_(lastProcessedRow, endRow);

  props.setProperty("ANALYSIS_V3_PROGRESS", String(endRow + 1));
  console.log("✓ Processed GA rows " + lastProcessedRow + "–" + endRow);
  if (endRow < gaLastRow) {
    console.log("  Next: run again (or set up trigger). Progress: " + endRow + " / " + gaLastRow);
  }
}

/**
 * POPULATE_ANALYSIS_V3()
 * Reads Golf_Analytics and populates ANALYSIS v3 sheet (32 columns).
 * WARNING: May timeout on large datasets (24k+ rows). Use POPULATE_ANALYSIS_V3_CHUNKED() instead.
 * One row per round played, with all available columns.
 * FIX: Clears ANALYSIS sheet before population to prevent duplicates.
 */
function POPULATE_ANALYSIS_V3() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var gaSheet = ss.getSheetByName(GA.SHEET);
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);

  if (!analysisSheet) {
    console.error("ANALYSIS sheet not found");
    return;
  }

  // Clear ANALYSIS before population
  var analysisLastRow = analysisSheet.getLastRow();
  if (analysisLastRow > ANALYSIS_V3.START_ROW) {
    analysisSheet.deleteRows(ANALYSIS_V3.START_ROW, analysisLastRow - ANALYSIS_V3.START_ROW + 1);
    console.log("✓ Cleared ANALYSIS sheet before population");
  }

  var gaLastRow = gaSheet.getLastRow();
  _populateAnalysisV3Batch_(GA.START_ROW, gaLastRow);
  console.log("✓ Full ANALYSIS v3 population complete. Now run: Menu → 📊 ANALYSIS v3 → \"➕ Add Formulas\"");
}

/**
 * BUILD_TOUR_STATS()
 * Calculates tour average performance by condition from ANALYSIS v3.
 * Updates TOUR_STATS sheet with Calm/Moderate/Tough averages.
 * Uses off_par (AC) as the metric.
 */
function BUILD_TOUR_STATS() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);
  var tourStatsSheet = ss.getSheetByName("TOUR_STATS");

  if (!analysisSheet) {
    console.error("ANALYSIS sheet not found");
    return;
  }

  // Create TOUR_STATS sheet if needed
  if (!tourStatsSheet) {
    tourStatsSheet = ss.insertSheet("TOUR_STATS");
  }

  var lastRow = analysisSheet.getLastRow();
  if (lastRow < ANALYSIS_V3.START_ROW) {
    console.error("No data in ANALYSIS sheet");
    return;
  }

  // Write headers and formulas (not static values)
  var headers = ["Condition", "Tour_Avg_OffPar", "Formula"];
  tourStatsSheet.clearContents();
  tourStatsSheet.getRange(1, 1, 1, 3).setValues([headers]);

  // Write condition names and formulas
  var tourStatsData = [
    ["Calm", '=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Calm",ANALYSIS!$AC:$AC,"<>"),"")', '=AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Calm",ANALYSIS!$AC:$AC,"<>")'],
    ["Moderate", '=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Moderate",ANALYSIS!$AC:$AC,"<>"),"")', '=AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Moderate",ANALYSIS!$AC:$AC,"<>")'],
    ["Tough", '=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Tough",ANALYSIS!$AC:$AC,"<>"),"")', '=AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Tough",ANALYSIS!$AC:$AC,"<>")']
  ];

  // Write condition names
  var conditionRange = tourStatsSheet.getRange(2, 1, 3, 1);
  conditionRange.setValues([["Calm"], ["Moderate"], ["Tough"]]);

  // Write formulas for column B (Tour_Avg_OffPar)
  var formulaRange = tourStatsSheet.getRange(2, 2, 3, 1);
  formulaRange.setFormulas([
    ['=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Calm",ANALYSIS!$AC:$AC,"<>"),"")'],
    ['=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Moderate",ANALYSIS!$AC:$AC,"<>"),"")'],
    ['=IFERROR(AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Tough",ANALYSIS!$AC:$AC,"<>"),"")']
  ]);

  // Write formulas for column C (audit trail)
  var auditRange = tourStatsSheet.getRange(2, 3, 3, 1);
  auditRange.setValues([
    ['AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Calm",ANALYSIS!$AC:$AC,"<>")'],
    ['AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Moderate",ANALYSIS!$AC:$AC,"<>")'],
    ['AVERAGEIFS(ANALYSIS!$AC:$AC,ANALYSIS!$K:$K,"Tough",ANALYSIS!$AC:$AC,"<>")']
  ]);

  console.log("✓ Built TOUR_STATS with formulas from ANALYSIS v3");
  console.log("  Each condition uses AVERAGEIFS on off_par (AC) where condition (K) matches");
  SpreadsheetApp.getUi().alert(
    "✓ TOUR_STATS updated with formulas\n" +
    "Column A: Conditions\n" +
    "Column B: Calculated averages (formulas)\n" +
    "Column C: Formula audit trail"
  );
}

/**
 * _populateAnalysisV3Batch_(startRow, endRow)
 * Internal: populates ANALYSIS v3 for a specific row range in Golf_Analytics.
 */
function _populateAnalysisV3Batch_(startRow, endRow) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var gaSheet = ss.getSheetByName(GA.SHEET);
  var analysisSheet = ss.getSheetByName(ANALYSIS.SHEET);
  var ecSheet = ss.getSheetByName(EVENTS_COURSES.SHEET);

  if (!gaSheet || !analysisSheet) {
    console.error("Golf_Analytics or ANALYSIS sheet not found");
    return;
  }

  // Read Golf_Analytics chunk (all columns up to COL_EVENT_ID)
  var numRows = endRow - startRow + 1;
  var gaRange = gaSheet.getRange(startRow, 1, numRows, GA.COL_EVENT_ID);
  var gaValues = gaRange.getValues();

  // Pre-load EVENTS_COURSES for par lookups
  var ecParMap = {}; // key: "event_id_year", value: par
  if (ecSheet) {
    var ecLastRow = ecSheet.getLastRow();
    if (ecLastRow > EVENTS_COURSES.START_ROW) {
      var ecRange = ecSheet.getRange(EVENTS_COURSES.START_ROW, 1, ecLastRow - EVENTS_COURSES.START_ROW + 1, EVENTS_COURSES.COL_PAR);
      var ecValues = ecRange.getValues();
      for (var j = 0; j < ecValues.length; j++) {
        var ecRow = ecValues[j];
        var eventId = ecRow[EVENTS_COURSES.COL_EVENT_ID - 1];
        var year = ecRow[EVENTS_COURSES.COL_YEAR - 1];
        var par = ecRow[EVENTS_COURSES.COL_PAR - 1];
        if (eventId && year && par) {
          var key = String(eventId) + "_" + String(year);
          ecParMap[key] = par;
        }
      }
    }
  }

  var analysisRows = [];

  // Extract one row per round (R1, R2, R3, R4)
  for (var i = 0; i < gaValues.length; i++) {
    var gaRow = gaValues[i];

    var playerId = gaRow[GA.COL_PLAYER_ID - 1] || "";
    var playerName = gaRow[GA.COL_PLAYER - 1];
    var eventId = gaRow[GA.COL_EVENT_ID - 1] || "";
    var eventName = gaRow[GA.COL_VENUE - 1];
    var year = gaRow[GA.COL_YEAR - 1];

    // Scores and conditions
    var scores = [
      gaRow[GA.COL_R1 - 1],
      gaRow[GA.COL_R2 - 1],
      gaRow[GA.COL_R3 - 1],
      gaRow[GA.COL_R4 - 1]
    ];

    var courseAvgs = [
      gaRow[GA.COL_COURSE_AVG_R1 - 1],
      gaRow[GA.COL_COURSE_AVG_R2 - 1],
      gaRow[GA.COL_COURSE_AVG_R3 - 1],
      gaRow[GA.COL_COURSE_AVG_R4 - 1]
    ];

    var vsAvgs = [
      gaRow[GA.COL_VS_AVG_R1 - 1],
      gaRow[GA.COL_VS_AVG_R2 - 1],
      gaRow[GA.COL_VS_AVG_R3 - 1],
      gaRow[GA.COL_VS_AVG_R4 - 1]
    ];

    var conditions = [
      gaRow[GA.COL_COND_R1 - 1],
      gaRow[GA.COL_COND_R2 - 1],
      gaRow[GA.COL_COND_R3 - 1],
      gaRow[GA.COL_COND_R4 - 1]
    ];

    var roundTypes = [
      gaRow[GA.COL_TYPE_R1 - 1],
      gaRow[GA.COL_TYPE_R2 - 1],
      gaRow[GA.COL_TYPE_R3 - 1],
      gaRow[GA.COL_TYPE_R4 - 1]
    ];

    var moons = [
      gaRow[GA.COL_MOON_R1 - 1],
      gaRow[GA.COL_MOON_R2 - 1],
      gaRow[GA.COL_MOON_R3 - 1],
      gaRow[GA.COL_MOON_R4 - 1]
    ];

    var moonwests = [
      gaRow[GA.COL_MOONWEST_R1 - 1],
      gaRow[GA.COL_MOONWEST_R2 - 1],
      gaRow[GA.COL_MOONWEST_R3 - 1],
      gaRow[GA.COL_MOONWEST_R4 - 1]
    ];

    var colors = [
      gaRow[GA.COL_COLOR_START - 1],
      gaRow[GA.COL_COLOR_START],
      gaRow[GA.COL_COLOR_START + 1],
      gaRow[GA.COL_COLOR_START + 2]
    ];

    // Exec, upside, peak: 3 cols per round, cols 22–33 (offsets 21–32)
    // R1: 22, 23, 24 (indices 21, 22, 23)
    // R2: 25, 26, 27 (indices 24, 25, 26)
    // R3: 28, 29, 30 (indices 27, 28, 29)
    // R4: 31, 32, 33 (indices 30, 31, 32)
    var execs = [
      gaRow[GA.COL_SCORE_START - 1],           // R1 exec at col 22
      gaRow[GA.COL_SCORE_START + 3 - 1],       // R2 exec at col 25
      gaRow[GA.COL_SCORE_START + 6 - 1],       // R3 exec at col 28
      gaRow[GA.COL_SCORE_START + 9 - 1]        // R4 exec at col 31
    ];

    var upsides = [
      gaRow[GA.COL_SCORE_START + 1 - 1],       // R1 upside at col 23
      gaRow[GA.COL_SCORE_START + 4 - 1],       // R2 upside at col 26
      gaRow[GA.COL_SCORE_START + 7 - 1],       // R3 upside at col 29
      gaRow[GA.COL_SCORE_START + 10 - 1]       // R4 upside at col 32
    ];

    var peaks = [
      gaRow[GA.COL_SCORE_START + 2 - 1],       // R1 peak at col 24
      gaRow[GA.COL_SCORE_START + 5 - 1],       // R2 peak at col 27
      gaRow[GA.COL_SCORE_START + 8 - 1],       // R3 peak at col 30
      gaRow[GA.COL_SCORE_START + 11 - 1]       // R4 peak at col 33
    ];

    // Player-level divination columns (same for all rounds)
    var wuXing = gaRow[GA.COL_WU_XING - 1] || "";
    var zodiac = gaRow[GA.COL_ZODIAC - 1] || "";
    var horoscope = gaRow[GA.COL_HOROSCOPE - 1] || "";
    var lifePath = gaRow[GA.COL_LIFE_PATH - 1] || "";
    var tithi = gaRow[GA.COL_TITHI - 1] || "";
    var gap = gaRow[GA.COL_GAP_R1 - 1] || "";  // R1 only
    var tour = gaRow[GA.COL_TOUR - 1] || "";

    // Best round (if GA has this column)
    var bestRoundLabel = gaRow[GA.COL_BEST_ROUND - 1] || "";

    // Create one row per round
    for (var round = 0; round < 4; round++) {
      var score = scores[round];
      if (!score || score === "") continue; // Skip empty rounds

      // Determine if this is the best round
      var isBestRound = 0;
      if (bestRoundLabel) {
        var bestRoundNum = parseInt(String(bestRoundLabel).substring(1), 10); // Extract number from "R1", "R2", etc.
        if (bestRoundNum === round + 1) {
          isBestRound = 1;
        }
      }

      // Gap is only for R1
      var gapValue = round === 0 ? gap : "";

      // Lookup par from EVENTS_COURSES
      var parValue = "";
      if (eventId && year) {
        var ecKey = String(eventId) + "_" + String(year);
        if (ecParMap[ecKey]) {
          parValue = ecParMap[ecKey];
        }
      }

      // Calculate the sheet row number for this data row (for formula references)
      var sheetRow = ANALYSIS_V3.START_ROW + analysisRows.length;

      var analysisRow = [
        playerId,                    // A: player_id
        playerName,                  // B: player_name
        eventId,                     // C: event_id
        eventName,                   // D: event_name
        year,                        // E: year
        round + 1,                   // F: round_num (1-4)
        score,                       // G: score
        parValue,                    // H: par
        courseAvgs[round] || "",     // I: course_avg
        vsAvgs[round] || "",         // J: vs_avg
        conditions[round] || "",     // K: condition
        roundTypes[round] || "",     // L: round_type
        colors[round] || "",         // M: color
        execs[round] || "",          // N: exec
        upsides[round] || "",        // O: upside
        peaks[round] || "",          // P: peak
        moons[round] || "",          // Q: moon
        wuXing,                      // R: wu_xing
        zodiac,                      // S: zodiac
        lifePath,                    // T: life_path
        tithi,                       // U: tithi
        gapValue,                    // V: gap (R1 only)
        tour,                        // W: tour
        isBestRound,                 // X: is_best_round
        horoscope,                   // AA: horoscope
        moonwests[round] || ""       // AB: moonwest (per-round)
      ];

      analysisRows.push(analysisRow);
    }
  }

  // Write all rows (append after existing data)
  if (analysisRows.length > 0) {
    var analysisLastRow = analysisSheet.getLastRow();
    var insertRow = Math.max(ANALYSIS_V3.START_ROW, analysisLastRow + 1);
    var writeRange = analysisSheet.getRange(insertRow, 1, analysisRows.length, analysisRows[0].length);
    writeRange.setValues(analysisRows);
  }
}
