/**
 * Wu Xing (Five Elements) calculations
 * Derives element from Chinese zodiac birth date
 */

import { CHINESE_ZODIAC } from '../constants/element.js';

/**
 * Get Chinese zodiac entry for a birth date
 * Handles lunar new year cutoff: birthdays on/after CNY date use that year's animal,
 * otherwise use previous year's animal
 *
 * @param {number} year - Birth year
 * @param {number} month - Birth month (1-12)
 * @param {number} day - Birth day (1-31)
 * @returns {Object|null} Zodiac entry { year, month, day, animal, element } or null if not found
 */
export function getChineseZodiac(year, month, day) {
  let match = null;

  for (let i = 0; i < CHINESE_ZODIAC.length; i++) {
    const row = CHINESE_ZODIAC[i];

    if (row.year === year) {
      // Found the year entry. Check if birthday is on/after lunar new year date.
      const cnyDate = new Date(row.year, row.month - 1, row.day);
      const birthDate = new Date(year, month - 1, day);

      if (birthDate >= cnyDate) {
        // Born on or after CNY → use this year's animal
        match = row;
      } else {
        // Born before CNY → use previous year's animal
        match = CHINESE_ZODIAC[i - 1] || null;
      }
      break;
    }
  }

  return match;
}
