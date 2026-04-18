/**
 * geneKeys.js — Gene Keys calculation
 *
 * Computes the 4 Prime Keys from birth data:
 *   Life's Work  = Conscious Sun gate
 *   Evolution    = Conscious Earth gate (Sun + 180°)
 *   Radiance     = Conscious Moon gate
 *   Purpose      = Unconscious Sun gate (Sun − 88° arc = ~88 days before birth)
 *
 * Each key returns { gate: 1–64, line: 1–6 }
 */

import { dateToSerial } from './tithi.js';
import {
  GATE_WHEEL,
  GATE_START_LONGITUDE,
  DEGREES_PER_GATE,
  DEGREES_PER_LINE,
} from '../constants/geneKeys.js';

// ── Astronomy helpers ──────────────────────────────────

// Days elapsed since J2000.0 (noon, Jan 1 2000 UTC)
function daysFromJ2000(year, month, day, hour24, tzOffset) {
  const tUTC = (hour24 - tzOffset) / 24;
  return dateToSerial(year, month, day) + tUTC - (dateToSerial(2000, 1, 1) + 0.5);
}

// Sun's ecliptic longitude in degrees (accurate to ~0.01°)
function sunLongitude(d) {
  const r = Math.PI / 180;
  const L = ((280.4665 + 0.98564736 * d) % 360 + 360) % 360; // mean longitude
  const g = ((357.5291092 + 0.98560028 * d) % 360 + 360) % 360; // mean anomaly
  const lon = L
    + 1.9146 * Math.sin(g * r)
    + 0.0200 * Math.sin(2 * g * r)
    - 0.0048 * Math.cos(g * r);
  return ((lon % 360) + 360) % 360;
}

// Moon's ecliptic longitude in degrees (accurate to ~1°)
function moonLongitude(d) {
  const r = Math.PI / 180;
  const Lm = ((218.3165 + 13.17639648 * d) % 360 + 360) % 360; // mean longitude
  const Mp = ((134.9633964 + 13.06499295 * d) % 360 + 360) % 360; // Moon mean anomaly
  const Ms = ((357.5291092 + 0.98560028  * d) % 360 + 360) % 360; // Sun mean anomaly
  const Dm = ((297.8501921 + 12.19074912 * d) % 360 + 360) % 360; // mean elongation
  const lon = Lm
    + 6.289 * Math.sin(Mp * r)
    - 2.100 * Math.sin(Ms * r)
    - 1.274 * Math.sin((2 * Dm - Mp) * r)
    - 0.658 * Math.sin(2 * Dm * r)
    - 0.214 * Math.sin(2 * Mp * r)
    - 0.110 * Math.sin(Dm * r);
  return ((lon % 360) + 360) % 360;
}

// ── Gate mapping ───────────────────────────────────────

// Convert an ecliptic longitude to { gate (1–64), line (1–6) }
function longitudeToGate(longitude) {
  const adjusted = ((longitude - GATE_START_LONGITUDE) % 360 + 360) % 360;
  const slot     = Math.min(Math.floor(adjusted / DEGREES_PER_GATE), 63);
  const line     = Math.min(Math.floor((adjusted % DEGREES_PER_GATE) / DEGREES_PER_LINE) + 1, 6);
  return { gate: GATE_WHEEL[slot], line };
}

// ── Public API ─────────────────────────────────────────

/**
 * calcGeneKeys — compute the 4 Prime Keys for a birth profile.
 *
 * @param {object} params
 * @param {number} params.year
 * @param {number} params.month
 * @param {number} params.day
 * @param {string} params.birthTime  — 'HH:MM' (24h)
 * @param {number} params.tzOffset   — numeric UTC offset (e.g. -5 for EST)
 *
 * @returns {{
 *   lifeWork:  { gate: number, line: number },  // Conscious Sun
 *   evolution: { gate: number, line: number },  // Conscious Earth (Sun + 180°)
 *   radiance:  { gate: number, line: number },  // Conscious Moon
 *   purpose:   { gate: number, line: number },  // Unconscious Sun (Sun − 88°)
 * }}
 */
export function calcGeneKeys({ year, month, day, birthTime = '12:00', tzOffset = 0 }) {
  const [hStr, mStr] = (birthTime || '12:00').split(':');
  const hour24 = parseInt(hStr, 10) + parseInt(mStr, 10) / 60;

  const d = daysFromJ2000(year, month, day, hour24, tzOffset);

  const sunLon       = sunLongitude(d);
  const moonLon      = moonLongitude(d);
  const earthLon     = (sunLon + 180) % 360;          // Earth = opposite Sun
  const purposeLon   = ((sunLon - 88) % 360 + 360) % 360; // 88° arc before birth

  return {
    lifeWork:  longitudeToGate(sunLon),
    evolution: longitudeToGate(earthLon),
    radiance:  longitudeToGate(moonLon),
    purpose:   longitudeToGate(purposeLon),
  };
}
