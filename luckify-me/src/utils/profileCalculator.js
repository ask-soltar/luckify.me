/**
 * Profile Calculator
 * Orchestrates all three dimensions (Tithi, Element, Life Path) into a complete profile
 */

import { calcTithi } from './tithi.js';
import { getChineseZodiac } from './element.js';
import { calcLifePath } from './lifePath.js';
import { calcGeneKeys, calcAllActivations } from './geneKeys.js';
import { deriveHumanDesign } from './humanDesign.js';
import { TYPE_CONFIG } from '../constants/tithi.js';
import { LP_CONFIG } from '../constants/lifePath.js';

/**
 * Calculate a complete Luckify Me profile from birth date and time
 * @param {Object} inputs - Birth information
 * @param {number} inputs.year - Birth year
 * @param {number} inputs.month - Birth month (1-12)
 * @param {number} inputs.day - Birth day (1-31)
 * @param {number} inputs.hour12 - Hour (1-12)
 * @param {number} inputs.minute - Minute (0-59)
 * @param {string} inputs.ampm - 'AM' or 'PM'
 * @param {number} inputs.tzOffset - Timezone offset in hours
 * @returns {Object} Complete profile result
 * @returns {string} result.type - Tithi type (nanda, bhadra, jaya, rikta, purna)
 * @returns {Object} result.cfg - Tithi type configuration
 * @returns {string} result.paksha - Ascending or Descending
 * @returns {number} result.tIdx - Tithi index (0-29)
 * @returns {number} result.elong - Sun-moon elongation (0-360°)
 * @returns {string} result.element - Wu Xing element (Wood, Fire, Earth, Metal, Water)
 * @returns {Object} result.zodiac - Chinese zodiac entry { year, month, day, animal, element }
 * @returns {number} result.lifePathNum - Life path number (1-9, 11, 22, 33)
 * @returns {Object} result.lpCfg - Life path configuration
 * @returns {number} result.y - Birth year
 * @returns {number} result.mo - Birth month
 * @returns {number} result.dy - Birth day
 */
export function calculateProfile(inputs) {
  const { year, month, day, hour12, minute, ampm, tzOffset, birthLat = null, birthLng = null } = inputs;

  // Calculate all dimensions
  const tithi = calcTithi(year, month, day, hour12, minute, ampm, tzOffset);
  const zodiac = getChineseZodiac(year, month, day);
  const elementName = zodiac ? zodiac.element : null;
  const lifePathNum = calcLifePath(month, day, year);
  const lpCfg = LP_CONFIG[lifePathNum] || null;

  // Convert hour12 + ampm to HH:MM for Gene Keys
  const h24 = ampm === 'PM' && hour12 < 12 ? hour12 + 12
            : ampm === 'AM' && hour12 === 12 ? 0
            : hour12;
  const birthTime24 = `${String(h24).padStart(2,'0')}:${String(minute).padStart(2,'0')}`;
  const geneKeys = calcGeneKeys({ year, month, day, birthTime: birthTime24, tzOffset: tzOffset ?? 0 });
  const activations = calcAllActivations({
    year,
    month,
    day,
    birthTime: birthTime24,
    tzOffset: tzOffset ?? 0,
    latitude: birthLat,
    longitude: birthLng,
  });
  const humanDesign = deriveHumanDesign(activations);

  return {
    type: tithi.type,
    cfg: TYPE_CONFIG[tithi.type],
    paksha: tithi.paksha,
    tIdx: tithi.tIdx,
    elong: tithi.elong,
    element: elementName,
    zodiac,
    lifePathNum,
    lpCfg,
    geneKeys,
    activations,
    humanDesign,
    y: year,
    mo: month,
    dy: day,
    birthLat,
    birthLng,
  };
}

/**
 * Generate a profile name from element and tithi type
 * @param {string} element - Wu Xing element (e.g., 'Fire')
 * @param {string} tithiType - Tithi type (e.g., 'nanda')
 * @returns {string} Generated name (e.g., 'Fire Nanda')
 */
export function generateProfileName(element, tithiType) {
  return (element || 'Unknown') + ' ' + (tithiType ? tithiType.charAt(0).toUpperCase() + tithiType.slice(1) : '');
}

/**
 * Generate a unique ID for a profile
 * Format: 'prof_' + timestamp + random string
 * @returns {string} Unique profile ID
 */
export function generateId() {
  return 'prof_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * Validate profile input data
 * @param {Object} inputs
 * @returns {Object} { valid: boolean, error: string|null }
 */
export function validateProfileInputs(inputs) {
  const { month, day, year } = inputs;

  if (!month || !day || !year) {
    return { valid: false, error: 'Please select your full birth date.' };
  }

  if (month < 1 || month > 12) {
    return { valid: false, error: 'Invalid month.' };
  }

  if (day < 1 || day > 31) {
    return { valid: false, error: 'Invalid day.' };
  }

  if (year < 1900 || year > new Date().getFullYear()) {
    return { valid: false, error: 'Invalid year.' };
  }

  return { valid: true, error: null };
}
