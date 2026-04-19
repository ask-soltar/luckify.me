/**
 * geneKeys.js — Gene Keys calculation
 *
 * Prime Keys (4): Life's Work, Evolution, Radiance, Purpose — from Sun/Earth positions.
 * All Activations (24): 12 planets × 2 charts (conscious at birth + design ~88 days prior).
 *   Planets: Sun, Earth, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, N.Node
 *
 * Accuracy:
 *   Sun: ~0.01° (equation of center).
 *   Moon: ~1° (Chapront reduced series).
 *   Mercury–Pluto: <0.1° via VSOP87 full theory (astronomia library).
 *   N.Node: mean node formula, ~0.05°.
 *   Gate = 5.625° wide, line = 0.9375° — VSOP87 is sufficient for all activations.
 */

import { dateToSerial } from './tithi.js';
import {
  GATE_WHEEL,
  GATE_START_LONGITUDE,
  DEGREES_PER_GATE,
  DEGREES_PER_LINE,
} from '../constants/geneKeys.js';

// VSOP87 planetary data (B-series: heliocentric ecliptic, dynamical ecliptic of date)
import vsop87Bmercury from 'astronomia/data/vsop87Bmercury';
import vsop87Bvenus   from 'astronomia/data/vsop87Bvenus';
import vsop87Bearth   from 'astronomia/data/vsop87Bearth';
import vsop87Bmars    from 'astronomia/data/vsop87Bmars';
import vsop87Bjupiter from 'astronomia/data/vsop87Bjupiter';
import vsop87Bsaturn  from 'astronomia/data/vsop87Bsaturn';
import vsop87Buranus  from 'astronomia/data/vsop87Buranus';
import vsop87Bneptune from 'astronomia/data/vsop87Bneptune';
import { Planet }     from 'astronomia/planetposition';

// Pre-instantiate planet objects (avoid re-creating on every call)
const VSOP = {
  Mercury: new Planet(vsop87Bmercury),
  Venus:   new Planet(vsop87Bvenus),
  Earth:   new Planet(vsop87Bearth),
  Mars:    new Planet(vsop87Bmars),
  Jupiter: new Planet(vsop87Bjupiter),
  Saturn:  new Planet(vsop87Bsaturn),
  Uranus:  new Planet(vsop87Buranus),
  Neptune: new Planet(vsop87Bneptune),
};

// ── Constants ──────────────────────────────────────────

const D2R = Math.PI / 180;

function norm(x) { return ((x % 360) + 360) % 360; }

// ── Time helpers ───────────────────────────────────────

// Days elapsed since J2000.0 (noon, Jan 1 2000 UTC)
function daysFromJ2000(year, month, day, hour24, tzOffset) {
  const tUTC = (hour24 - tzOffset) / 24;
  return dateToSerial(year, month, day) + tUTC - (dateToSerial(2000, 1, 1) + 0.5);
}

// Julian Day Ephemeris from days-since-J2000
function toJDE(d) { return 2451545.0 + d; }

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
  const Ms = norm(357.5291 +  0.98560028 * d);

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

// ── VSOP87 geocentric ecliptic longitude ───────────────
//
// Uses the B-series (heliocentric ecliptic of date).
// Geocentric longitude is computed by subtracting Earth's heliocentric
// position from the planet's, then taking atan2.

function vsopGeocentricLon(planetName, d) {
  const JDE = toJDE(d);
  const pp  = VSOP[planetName].position(JDE); // { lon (rad), lat (rad), range (AU) }
  const ep  = VSOP.Earth.position(JDE);

  // Rectangular heliocentric ecliptic coords
  const px = pp.range * Math.cos(pp.lat) * Math.cos(pp.lon);
  const py = pp.range * Math.cos(pp.lat) * Math.sin(pp.lon);
  const ex = ep.range * Math.cos(ep.lat) * Math.cos(ep.lon);
  const ey = ep.range * Math.cos(ep.lat) * Math.sin(ep.lon);

  return norm(Math.atan2(py - ey, px - ex) / D2R);
}

// ── Design date (88° solar arc) ───────────────────────
//
// Human Design uses 88° of solar arc before birth, NOT 88 calendar days.

function designDate(d_birth) {
  const targetLon = norm(sunLongitude(d_birth) - 88);
  let d = d_birth - 88;
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
  { name: 'Mercury', symbol: '☿', getLon: d => vsopGeocentricLon('Mercury', d) },
  { name: 'Venus',   symbol: '♀', getLon: d => vsopGeocentricLon('Venus',   d) },
  { name: 'Mars',    symbol: '♂', getLon: d => vsopGeocentricLon('Mars',    d) },
  { name: 'Jupiter', symbol: '♃', getLon: d => vsopGeocentricLon('Jupiter', d) },
  { name: 'Saturn',  symbol: '♄', getLon: d => vsopGeocentricLon('Saturn',  d) },
  { name: 'Uranus',  symbol: '♅', getLon: d => vsopGeocentricLon('Uranus',  d) },
  { name: 'Neptune', symbol: '♆', getLon: d => vsopGeocentricLon('Neptune', d) },
  { name: 'Pluto',   symbol: '♇', getLon: d => vsopGeocentricLon('Pluto',   d) },
  { name: 'N.Node',  symbol: '☊', getLon: d => northNodeLongitude(d) },
];

// Note: Pluto falls back to the existing Keplerian calculation since
// astronomia does not include a VSOP87 Pluto dataset.
// Pluto's gate changes slowly (~1 gate per decade) so Keplerian is adequate.
const ORB_PLUTO = [238.92881, 145.20780, 224.06892, -0.04063, 0.24882, 0.00006, 39.481680, 17.1420, 110.3039, -0.27040];
function keplerE(M_rad, e) { let E = M_rad; for (let i = 0; i < 12; i++) E = M_rad + e * Math.sin(E); return E; }
function plutoGeoLon(d) {
  const T = d / 36525;
  const [L0,L1,w0,w1,e0,e1,a,i_deg,O0,O1] = ORB_PLUTO;
  const L=norm(L0+L1*T), w=norm(w0+w1*T), O=norm(O0+O1*T), e=e0+e1*T;
  const M=norm(L-w)*D2R, E=keplerE(M,e);
  const nu=2*Math.atan2(Math.sqrt(1+e)*Math.sin(E/2),Math.sqrt(1-e)*Math.cos(E/2));
  const r=a*(1-e*Math.cos(E)), i=i_deg*D2R, Or=O*D2R;
  const theta=(nu/D2R+w-O)*D2R;
  const px=r*(Math.cos(Or)*Math.cos(theta)-Math.sin(Or)*Math.sin(theta)*Math.cos(i));
  const py=r*(Math.sin(Or)*Math.cos(theta)+Math.cos(Or)*Math.sin(theta)*Math.cos(i));
  // Earth via VSOP87
  const JDE=toJDE(d), ep=VSOP.Earth.position(JDE);
  const ex=ep.range*Math.cos(ep.lat)*Math.cos(ep.lon);
  const ey=ep.range*Math.cos(ep.lat)*Math.sin(ep.lon);
  return norm(Math.atan2(py-ey,px-ex)/D2R);
}
// Override Pluto entry
PLANETS[10] = { name: 'Pluto', symbol: '♇', getLon: d => plutoGeoLon(d) };

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
