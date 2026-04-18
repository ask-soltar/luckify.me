/**
 * geneKeys.js — Gene Keys constants
 *
 * GATE_WHEEL: 64 gates in ecliptic order, starting at Gate 25
 *   (28°15' Pisces = 358.25°). Each gate spans 5.625° (360/64).
 *   Source: Human Design Mandala — verified against published degree tables.
 *
 * GENE_KEYS: descriptions keyed by gate number.
 *   Populate with your own content — structure: { name, shadow, gift, siddhi }
 *   Lines can be added as: lines: { 1: '...', 2: '...', 3: '...', 4: '...', 5: '...', 6: '...' }
 */

// Starting ecliptic longitude of Gate 25 (28°15' Pisces)
export const GATE_START_LONGITUDE = 358.25;

// Degrees per gate and line
export const DEGREES_PER_GATE = 5.625;   // 360 / 64
export const DEGREES_PER_LINE = 0.9375;  // 5.625 / 6

/**
 * 64 gate numbers in zodiac order, starting from 28°15' Pisces.
 * Each index corresponds to a 5.625° slot.
 *
 * Aries:       25  17  21  51  42   3
 * Taurus:      27  24   2  23   8  20
 * Gemini:      16  35  45  12  15  52
 * Cancer:      39  53  62  56  31  33
 * Leo:          7   4  29  59  40  64
 * Virgo:       47   6  46  18  48  57
 * Libra:       32  50  28  44   1  43
 * Scorpio:     14  34   9   5  26  11
 * Sagittarius: 10  58  38  54  61  60
 * Capricorn:   41  19  13  49  30  55
 * Aquarius:    37  63  22  36  (last 4 — then cycle returns to Gate 25)
 */
export const GATE_WHEEL = [
  25, 17, 21, 51, 42,  3,  // Aries
  27, 24,  2, 23,  8, 20,  // Taurus
  16, 35, 45, 12, 15, 52,  // Gemini
  39, 53, 62, 56, 31, 33,  // Cancer
   7,  4, 29, 59, 40, 64,  // Leo
  47,  6, 46, 18, 48, 57,  // Virgo
  32, 50, 28, 44,  1, 43,  // Libra → Scorpio
  14, 34,  9,  5, 26, 11,  // Scorpio → Sagittarius
  10, 58, 38, 54, 61, 60,  // Sagittarius → Capricorn
  41, 19, 13, 49, 30, 55,  // Capricorn → Aquarius
  37, 63, 22, 36,           // Aquarius → Pisces (back to Gate 25)
];

/**
 * Gene Key descriptions — fill these in with your own content.
 *
 * Template for each gate:
 * {
 *   name:   'Key Name',
 *   shadow: 'Shadow quality',
 *   gift:   'Gift quality',
 *   siddhi: 'Siddhi quality',
 *   lines: {          // optional — add when you have line-level content
 *     1: '...',
 *     2: '...',
 *     3: '...',
 *     4: '...',
 *     5: '...',
 *     6: '...',
 *   }
 * }
 */
export const GENE_KEYS = {
  // Paste your 64 gate entries here, keyed by gate number (integer)
  // 1:  { name: '', shadow: '', gift: '', siddhi: '' },
  // 2:  { name: '', shadow: '', gift: '', siddhi: '' },
  // ...
};
