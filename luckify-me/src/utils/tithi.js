/**
 * Tithi (Lunar cycle position) calculations
 * Uses astronomical methods to determine sun-moon elongation
 */

import { TYPES } from '../constants/tithi.js';

/**
 * Convert calendar date to Excel serial number
 * Used for astronomical calculations referenced to 1899-12-30
 * @param {number} y - Year
 * @param {number} m - Month (1-12)
 * @param {number} d - Day (1-31)
 * @returns {number} Serial number
 */
export function dateToSerial(y, m, d) {
  const base = new Date(1899, 11, 30);
  return (new Date(y, m - 1, d) - base) / 86400000;
}

/**
 * Calculate Tithi (lunar cycle position) from birth date and time
 * Uses solar longitude and sun-moon elongation to determine tithi type
 *
 * @param {number} year - Birth year
 * @param {number} month - Birth month (1-12)
 * @param {number} day - Birth day (1-31)
 * @param {number} hour12 - Hour in 12-hour format (1-12)
 * @param {number} minute - Minute (0-59)
 * @param {string} ampm - 'AM' or 'PM'
 * @param {number} tzOffset - Timezone offset in hours (e.g., -5 for EST)
 * @returns {Object} Result: { type, typeIdx, tIdx, elong, paksha }
 */
export function calcTithi(year, month, day, hour12, minute, ampm, tzOffset) {
  // Convert time to 24-hour format and UTC fraction
  let hr = hour12 % 12;
  if (ampm === 'PM') hr += 12;
  const timeFrac = (hr * 3600 + minute * 60) / 86400;
  const tUTC = timeFrac + 0.5 - tzOffset / 24;

  // Julian day calculation (days since J2000.0 epoch)
  const d =
    dateToSerial(year, month, day) +
    tUTC -
    (dateToSerial(2000, 1, 1) + 0.5);

  // Astronomical calculations for sun-moon elongation
  // These constants and coefficients are from standard astronomical ephemeris
  const r = Math.PI / 180; // radians conversion

  // Mean longitudes
  const Dm = ((297.8501921 + 12.19074912 * d) % 360 + 360) % 360;
  const Ms = ((357.5291092 + 0.98560028 * d) % 360 + 360) % 360;
  const Mp = ((134.9633964 + 13.06499295 * d) % 360 + 360) % 360;

  // Lunar ecliptic longitude with perturbation terms
  const psi =
    180 -
    Dm -
    6.289 * Math.sin(Mp * r) +
    2.1 * Math.sin(Ms * r) -
    1.274 * Math.sin((2 * Dm - Mp) * r) -
    0.658 * Math.sin(2 * Dm * r) -
    0.214 * Math.sin(2 * Mp * r) -
    0.11 * Math.sin(Dm * r);

  // Sun-moon elongation (0-360°)
  const elong = ((psi % 360) + 360) % 360;

  // Tithi index: elongation divided by 12° per tithi (0-29)
  const tIdx = Math.floor(elong / 12);

  // Type index: maps 30 tithis to 5 types (0-4)
  const typeIdx = tIdx % 5;
  const type = TYPES[typeIdx];

  // Paksha: Ascending (waxing) or Descending (waning)
  const paksha = tIdx < 15 ? 'Ascending' : 'Descending';

  return { type, typeIdx, tIdx, elong, paksha };
}
