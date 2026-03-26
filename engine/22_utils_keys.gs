/****************************************************
 * 22_utils_keys.gs
 * LUCKIFY ME — Key & ID Utilities
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure helper functions for key generation.
 ****************************************************/

function _safeKey_(v) {
  if (v instanceof Date) return v.toISOString();
  if (typeof v === "number") return String(v);
  return String(v || "");
}

// TODO P2: add generatePlayerId(), generateEventId(), generateCalcId()
