/**
 * geneKeys.js — Gene Keys calculation
 *
 * Prime Keys (4): Life's Work, Evolution, Radiance, Purpose — from Sun/Earth positions.
 * All Activations (24): 12 planets × 2 charts (conscious at birth + design ~88 days prior).
 *   Planets: Sun, Earth, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, N.Node
 *
 * Accuracy: ~0.5–2° for most planets using 3D Keplerian + inclination.
 *   Sun: ~0.01° (equation of center), Moon: ~1° (Chapront reduced).
 *   Mercury–Mars: ~0.5°, Jupiter–Neptune: ~1–2°.
 *   Gate = 5.625° wide — sufficient for almost all activations.
 *   Activations within ~0.05° of a line boundary may differ from Swiss Ephemeris.
 * Formulas: 3D Keplerian (inclination + ascending node) + geocentric projection.
 */

import { dateToSerial } from './tithi.js';
import {
  GATE_WHEEL,
  GATE_START_LONGITUDE,
  DEGREES_PER_GATE,
  DEGREES_PER_LINE,
} from '../constants/geneKeys.js';

// ── Constants ──────────────────────────────────────────

const D2R = Math.PI / 180;

function norm(x) { return ((x % 360) + 360) % 360; }

// ── Time helpers ───────────────────────────────────────

// Days elapsed since J2000.0 (noon, Jan 1 2000 UTC)
function daysFromJ2000(year, month, day, hour24, tzOffset) {
  const tUTC = (hour24 - tzOffset) / 24;
  return dateToSerial(year, month, day) + tUTC - (dateToSerial(2000, 1, 1) + 0.5);
}

// ── Solar longitude (accurate to ~0.01°) ──────────────

function sunLongitude(d) {
  const L = norm(280.4665 + 0.98564736 * d);
  const g = norm(357.5291092 + 0.98560028 * d);
  const lon = L
    + 1.9146 * Math.sin(g * D2R)
    + 0.0200 * Math.sin(2 * g * D2R)
    - 0.0048 * Math.cos(g * D2R);
  return norm(lon);
}

// ── Moon longitude (accurate to ~1°) ──────────────────

function moonLongitude(d) {
  const L  = norm(218.3165 + 13.17639648 * d);
  const M  = norm(134.9634 + 13.06499295 * d);
  const D  = norm(297.8502 + 12.19074912 * d);
  const F  = norm(93.2721  + 13.22935024 * d);
  const Ms = norm(357.5291 +  0.98560028 * d); // Sun's mean anomaly

  return norm(L
    + 6.289  * Math.sin(M  * D2R)
    - 1.274  * Math.sin((2*D - M)     * D2R)
    + 0.658  * Math.sin((2*D)         * D2R)
    - 0.186  * Math.sin(Ms            * D2R)
    + 0.214  * Math.sin((2*M)         * D2R)
    - 0.059  * Math.sin((2*D - 2*M)   * D2R)
    - 0.057  * Math.sin((2*D - M - Ms)* D2R)
    + 0.053  * Math.sin((2*D + M)     * D2R)
    + 0.046  * Math.sin((2*D - Ms)    * D2R)
    + 0.041  * Math.sin((M - Ms)      * D2R)
    - 0.035  * Math.sin(D             * D2R)
    - 0.031  * Math.sin((M + Ms)      * D2R)
    - 0.015  * Math.sin((2*F - 2*D)   * D2R)
    + 0.011  * Math.sin((M - 4*D)     * D2R));
}

// ── North Node longitude (mean node, retrograde) ──────

function northNodeLongitude(d) {
  return norm(125.0445 - 0.05295377 * d);
}

// ── Planetary geocentric longitude (3D Keplerian) ──────

/*
 * Orbital elements at J2000.0 with linear rate per Julian century.
 * Format: [L0, L1, w0, w1, e0, e1, a, i, O0, O1]
 *   L  = mean longitude (deg)            L1 = rate (deg/century)
 *   w  = longitude of perihelion (deg)   w1 = rate (deg/century)
 *   e  = eccentricity                    e1 = rate (1/century)
 *   a  = semi-major axis (AU)
 *   i  = inclination to ecliptic (deg)   — fixed, negligible rate for our accuracy
 *   O0 = longitude of ascending node     O1 = rate (deg/century)
 * Source: Meeus "Astronomical Algorithms" Tables 31.a & 31.b.
 */
const ORB = {
  //           L0           L1         w0        w1       e0       e1       a       i      O0       O1
  Mercury: [252.25084, 149472.67411,  77.45779,  0.16047, 0.20563,  0.00002, 0.387098,  7.0050,  48.3313,  1.18515],
  Venus:   [181.97973,  58517.81539, 131.56370,  0.00268, 0.00677, -0.00005, 0.723330,  3.3947,  76.6799, -0.27769],
  Earth:   [100.46435,  35999.37245, 102.93735,  0.31997, 0.01671, -0.00004, 1.000000,  0.0000,   0.0000,  0.00000],
  Mars:    [355.43327,  19140.30268, 336.06023,  0.44441, 0.09341,  0.00009, 1.523688,  1.8497,  49.5574, -0.29257],
  Jupiter: [ 34.35148,   3034.74613,  14.72847,  0.21253, 0.04839, -0.00013, 5.202561,  1.3041, 100.4542,  0.33298],
  Saturn:  [ 50.07747,   1222.49362,  93.05678, -0.41898, 0.05551, -0.00051, 9.554747,  2.4853, 113.6634, -0.25656],
  Uranus:  [314.05501,    428.48203, 170.95426,  0.40806, 0.04630, -0.00004,19.218140,  0.7732,  74.0095,  0.05786],
  Neptune: [304.34867,    218.45945,  44.96476, -0.32241, 0.00898,  0.00006,30.109570,  1.7700, 131.7806, -0.01449],
  Pluto:   [238.92881,    145.20780, 224.06892, -0.04063, 0.24882,  0.00006,39.481680, 17.1420, 110.3039, -0.27040],
};

// Solve Kepler's equation: E = M + e·sin(E), returns E in radians
function keplerE(M_rad, e) {
  let E = M_rad;
  for (let i = 0; i < 12; i++) E = M_rad + e * Math.sin(E);
  return E;
}

// Heliocentric ecliptic x, y, z (AU) — full 3D including orbital inclination.
// Uses standard Keplerian rotation: perihelion → inclination → ascending node.
function helioXYZ(L0, L1, w0, w1, e0, e1, a, i_deg, O0, O1, T) {
  const L     = norm(L0 + L1 * T);
  const w     = norm(w0 + w1 * T);   // longitude of perihelion
  const O     = norm(O0 + O1 * T);   // longitude of ascending node
  const e     = e0 + e1 * T;
  const M     = norm(L - w) * D2R;
  const E     = keplerE(M, e);
  const nu    = 2 * Math.atan2(
    Math.sqrt(1 + e) * Math.sin(E / 2),
    Math.sqrt(1 - e) * Math.cos(E / 2)
  );
  const r     = a * (1 - e * Math.cos(E));
  const i     = i_deg * D2R;
  const Orad  = O * D2R;
  // Argument of latitude from ascending node (in orbital plane)
  const theta = (nu / D2R + w - O) * D2R;
  return {
    x: r * (Math.cos(Orad) * Math.cos(theta) - Math.sin(Orad) * Math.sin(theta) * Math.cos(i)),
    y: r * (Math.sin(Orad) * Math.cos(theta) + Math.cos(Orad) * Math.sin(theta) * Math.cos(i)),
    z: r * Math.sin(theta) * Math.sin(i),
  };
}

// Geocentric ecliptic longitude (projects onto the ecliptic plane — ignores latitude).
function geocentricLon(planet, d) {
  const T = d / 36525; // Julian centuries from J2000
  const p = helioXYZ(...ORB[planet], T);
  const e = helioXYZ(...ORB.Earth,   T);
  return norm(Math.atan2(p.y - e.y, p.x - e.x) / D2R);
}

// ── Design date (88° solar arc) ───────────────────────
//
// Human Design uses 88° of solar arc before birth, NOT 88 calendar days.
// The sun moves ~0.9856°/day on average but varies through the year.
// We solve iteratively: find d such that sunLongitude(d) == birthSunLon - 88°.

function designDate(d_birth) {
  const targetLon = norm(sunLongitude(d_birth) - 88);
  let d = d_birth - 88; // initial estimate
  for (let i = 0; i < 12; i++) {
    const err = norm(sunLongitude(d) - targetLon + 180) - 180;
    d -= err / 0.9856;
  }
  return d;
}

// ── Gate mapping ───────────────────────────────────────

function longitudeToGate(longitude) {
  const adjusted = norm(longitude - GATE_START_LONGITUDE);
  const slot     = Math.min(Math.floor(adjusted / DEGREES_PER_GATE), 63);
  const line     = Math.min(Math.floor((adjusted % DEGREES_PER_GATE) / DEGREES_PER_LINE) + 1, 6);
  return { gate: GATE_WHEEL[slot], line };
}

// ── Planet catalogue ───────────────────────────────────

// { name, symbol, getLon(d) → degrees }
const PLANETS = [
  { name: 'Sun',     symbol: '☉', getLon: d => sunLongitude(d) },
  { name: 'Earth',   symbol: '⊕', getLon: d => norm(sunLongitude(d) + 180) },
  { name: 'Moon',    symbol: '☽', getLon: d => moonLongitude(d) },
  { name: 'Mercury', symbol: '☿', getLon: d => geocentricLon('Mercury', d) },
  { name: 'Venus',   symbol: '♀', getLon: d => geocentricLon('Venus',   d) },
  { name: 'Mars',    symbol: '♂', getLon: d => geocentricLon('Mars',    d) },
  { name: 'Jupiter', symbol: '♃', getLon: d => geocentricLon('Jupiter', d) },
  { name: 'Saturn',  symbol: '♄', getLon: d => geocentricLon('Saturn',  d) },
  { name: 'Uranus',  symbol: '♅', getLon: d => geocentricLon('Uranus',  d) },
  { name: 'Neptune', symbol: '♆', getLon: d => geocentricLon('Neptune', d) },
  { name: 'Pluto',   symbol: '♇', getLon: d => geocentricLon('Pluto',   d) },
  { name: 'N.Node',  symbol: '☊', getLon: d => northNodeLongitude(d) },
];

// ── Public API ─────────────────────────────────────────

/**
 * calcGeneKeys — compute the 4 Prime Keys for a birth profile.
 *
 * @returns {{ lifeWork, evolution, radiance, purpose }} — each { gate, line }
 */
export function calcGeneKeys({ year, month, day, birthTime = '12:00', tzOffset = 0 }) {
  const [hStr, mStr] = (birthTime || '12:00').split(':');
  const hour24 = parseInt(hStr, 10) + parseInt(mStr, 10) / 60;

  const d = daysFromJ2000(year, month, day, hour24, tzOffset);

  const sunLon         = sunLongitude(d);
  const earthLon       = norm(sunLon + 180);
  const d_design       = designDate(d);
  const designSunLon   = sunLongitude(d_design);
  const designEarthLon = norm(designSunLon + 180);

  return {
    lifeWork:  longitudeToGate(sunLon),
    evolution: longitudeToGate(earthLon),
    radiance:  longitudeToGate(designSunLon),
    purpose:   longitudeToGate(designEarthLon),
  };
}

/**
 * calcAllActivations — compute all 24 planetary activations (12 planets × 2 charts).
 *
 * @returns {Array<{ planet, symbol, chart, gate, line }>}
 *   chart: 'conscious' (at birth) | 'design' (~88 days before birth)
 */
export function calcAllActivations({ year, month, day, birthTime = '12:00', tzOffset = 0 }) {
  const [hStr, mStr] = (birthTime || '12:00').split(':');
  const hour24 = parseInt(hStr, 10) + parseInt(mStr, 10) / 60;

  const d = daysFromJ2000(year, month, day, hour24, tzOffset);

  const d_design = designDate(d);
  const charts = [
    { chart: 'conscious', dChart: d },
    { chart: 'design',    dChart: d_design },
  ];

  const activations = [];

  for (const { chart, dChart } of charts) {
    for (const planet of PLANETS) {
      const lon = planet.getLon(dChart);
      const { gate, line } = longitudeToGate(lon);
      activations.push({ planet: planet.name, symbol: planet.symbol, chart, gate, line });
    }
  }

  return activations;
}
