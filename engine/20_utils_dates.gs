/****************************************************
 * 20_utils_dates.gs
 * LUCKIFY ME — Date & Timezone Utilities
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure helper functions only.
 ****************************************************/

function _coerceDate_(value) {
  if (value instanceof Date) return new Date(value.getTime());
  if (typeof value === "number") return new Date(Math.round((value - 25569) * 86400000));
  const d = new Date(value);
  if (!isNaN(d)) return d;
  throw new Error("Invalid date: " + value);
}

function _buildLocalDateTime_(dayDate, hour, minute) {
  const d = _coerceDate_(dayDate);
  return new Date(d.getFullYear(), d.getMonth(), d.getDate(), hour, minute, 0);
}

function localToUTC(dateLocal, tzHours) {
  const tz = Number(tzHours);
  if (!isFinite(tz)) throw new Error("localToUTC: tzHours must be numeric");
  return new Date((+_coerceDate_(dateLocal)) - tz * 3600000);
}

function _envGMTFromTZIDorOffset_(envTZ, whenLocal) {
  if (envTZ == null || envTZ === "") throw new Error("Missing envTZ.");
  if (typeof envTZ === "number") return Number(envTZ);
  const s = String(envTZ).trim();
  if (/^[+-]?\d+(\.\d+)?$/.test(s)) return Number(s);
  return _gmtOffsetFromTZID_(s, whenLocal);
}

function _gmtOffsetFromTZID_(tzid, whenLocal) {
  const d    = _coerceDate_(whenLocal);
  const z    = Utilities.formatDate(d, String(tzid), "Z");
  const sign = z.startsWith("-") ? -1 : 1;
  const hh   = parseInt(z.substring(1,3), 10);
  const mm   = parseInt(z.substring(3,5), 10);
  return sign * (hh + mm/60);
}

function _WD_normTime_(t, defaultTime) {
  if (t == null || t === "") return defaultTime;
  const s = String(t).trim();
  if (s === "") return defaultTime;
  const parts = s.split(":");
  if (parts.length === 2) return `${String(parseInt(parts[0],10)).padStart(2,"0")}:${String(parseInt(parts[1],10)).padStart(2,"0")}`;
  return defaultTime;
}

function _WD_buildLocalDT_(dayDate, hhmm) {
  const [hh, mm] = hhmm.split(":").map(Number);
  return _buildLocalDateTime_(dayDate, Number(hh), Number(mm));
}

// CONDITIONS date helpers (moved from conditions script)
function CONDITIONS_GET_LOCAL_DATE_STR_(date, gmtOffset) {
  const d      = new Date(date);
  const localMs = d.getTime() + (gmtOffset * 60 * 60 * 1000);
  return Utilities.formatDate(new Date(localMs), "UTC", "yyyy-MM-dd");
}

function CONDITIONS_GET_LOCAL_TODAY_(gmtOffset) {
  const now     = new Date();
  const localMs = now.getTime() + (gmtOffset * 60 * 60 * 1000);
  const local   = new Date(localMs);
  local.setUTCHours(0, 0, 0, 0);
  return local;
}
