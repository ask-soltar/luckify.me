/****************************************************
 * 11_engine_categories.gs
 * LUCKIFY ME — Category & Color Engine
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure functions only.
 ****************************************************/

/* =========================
   PUBLIC API
========================= */

function LUCKY_CATEGORY_ALT_FROM_DELTA(d) {
  if (d == null || d === "") return "";
  const n = Number(d);
  if (!isFinite(n)) return "";
  return _categoryFromDeltaAlt_(n);
}

function LUCKY_CATEGORY_COLOR(cat) {
  if (cat == null || cat === "") return "";
  const MAP = {
    "Noise":             "Pink",
    "Prime":             "Orange",
    "Sub-Prime":         "Blue",
    "Edge":              "Yellow",
    "No Tax":            "Yellow",
    "Neutral":           "Yellow",
    "Null Edge":         "Yellow",
    "Survivor":          "Green",
    "Unstable Identity": "Purple",
    "Identity":          "Purple",
    "Stable Identity":   "Purple",
    "Growth":            "Green",
    "Variance":          "Blue",
    "Stable Swing":      "Blue",
    "Unstable Swing":    "Red",
    "Luck":              "Brown"
  };
  return MAP[String(cat).trim()] || "";
}

function LUCKY_DELTA_COLOR(d) {
  return LUCKY_CATEGORY_COLOR(LUCKY_CATEGORY_ALT_FROM_DELTA(d));
}

/* =========================
   PRIVATE
========================= */

function _categoryFromDeltaAlt_(d) {
  if (d >= 14)  return "Noise";
  if (d >= 7)   return "Prime";
  if (d >= 4)   return "Sub-Prime";
  if (d >= 2)   return "Edge";
  if (d === 0)  return "Neutral";
  if (d >= -1)  return "No Tax";
  if (d >= -2)  return "Null Edge";
  if (d >= -4)  return "Survivor";
  if (d >= -5)  return "Unstable Identity";
  if (d >= -8)  return "Identity";
  if (d >= -9)  return "Stable Identity";
  if (d >= -11) return "Growth";
  if (d >= -13) return "Variance";
  if (d >= -15) return "Stable Swing";
  if (d >= -29) return "Unstable Swing";
  if (d >= -40) return "Luck";
  return "Break Point";
}
