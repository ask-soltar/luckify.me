/**
 * geneKeys.js — Gene Keys calculation
 *
 * Computes the 4 Prime Keys from birth data:
 *   Life's Work  = Conscious Sun gate     (Sun at birth)
 *   Evolution    = Conscious Earth gate   (Sun + 180° at birth)
 *   Radiance     = Unconscious Sun gate   (Design Sun: Sun ~88 days before birth)
 *   Purpose      = Unconscious Earth gate (Design Earth: Design Sun + 180°)
 *
 * Gene Keys uses only Sun positions — no Moon.
 * The Design chart is calculated ~88 days before birth (88 solar arc degrees).
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
 *   radiance:  { gate: number, line: number },  // Unconscious Sun (Design — ~88 days before birth)
 *   purpose:   { gate: number, line: number },  // Unconscious Earth (Design Sun + 180°)
 * }}
 */
export function calcGeneKeys({ year, month, day, birthTime = '12:00', tzOffset = 0 }) {
  const [hStr, mStr] = (birthTime || '12:00').split(':');
  const hour24 = parseInt(hStr, 10) + parseInt(mStr, 10) / 60;

  const d = daysFromJ2000(year, month, day, hour24, tzOffset);

  // Conscious chart — at birth
  const sunLon       = sunLongitude(d);
  const earthLon     = (sunLon + 180) % 360;

  // Unconscious (Design) chart — Sun ~88 days before birth
  const designSunLon   = sunLongitude(d - 88);
  const designEarthLon = (designSunLon + 180) % 360;

  return {
    lifeWork:  longitudeToGate(sunLon),         // Conscious Sun
    evolution: longitudeToGate(earthLon),        // Conscious Earth
    radiance:  longitudeToGate(designSunLon),    // Unconscious Sun (Design)
    purpose:   longitudeToGate(designEarthLon),  // Unconscious Earth (Design)
  };
}
