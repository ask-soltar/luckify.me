/**
 * Lucky Window Calculator — BaZi scoring engine
 * Ported from Project Soltar / Lucky window calculator / luckycalc.html
 *
 * Core concept: Computes person-environment elemental alignment.
 * Birth chart (natal pillars) vs daily chart (day + year pillars) → delta → color zone.
 */

// ── Constants ──

const LUCKY_CFG = {
  AM_HOUR: 10, PM_HOUR: 19, MINUTE: 0,
  DEFAULT_BOUNDARY: "MIDNIGHT",
  DEFAULT_PRESET: "CLASSIC",
  NATAL_W: { year: 1, month: 2, day: 3, hour: 1 },
  NATAL_YEAR_MULT: 1.5,
  ENV_W_DAY: 0.7, ENV_W_YEAR: 0.3,
  ENV_COUNTER_BOOST: 0.08,
  SHAPE_TANH_K: 1.2,
  PEAK_ENV_GAIN: 0.25,
  STABLE_MAX: 0.30, SWINGY_MIN: 0.45,
  ENV_MATRIX: [
    [1,    0.35, 0,   -0.9, 0.85],
    [0.85, 1,    0.35, 0.85,-0.9],
    [0,    0.85, 1,    0.35, 0.85],
    [-0.9, 0,    0.85, 1,    0.35],
    [0.35,-0.9,  0,    0.85, 1]
  ]
};

const EL_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"];
const LUCKY_BASELINE = 72;

const STEMS = [
  { key: "Jia",  yin: false, element: "Wood"  },
  { key: "Yi",   yin: true,  element: "Wood"  },
  { key: "Bing", yin: false, element: "Fire"  },
  { key: "Ding", yin: true,  element: "Fire"  },
  { key: "Wu",   yin: false, element: "Earth" },
  { key: "Ji",   yin: true,  element: "Earth" },
  { key: "Geng", yin: false, element: "Metal" },
  { key: "Xin",  yin: true,  element: "Metal" },
  { key: "Ren",  yin: false, element: "Water" },
  { key: "Gui",  yin: true,  element: "Water" }
];
const STEM_KEYS = STEMS.map(s => s.key);

const BRANCHES = [
  { key: "Zi",   animal: "Rat"     }, { key: "Chou", animal: "Ox"      },
  { key: "Yin",  animal: "Tiger"   }, { key: "Mao",  animal: "Rabbit"  },
  { key: "Chen", animal: "Dragon"  }, { key: "Si",   animal: "Snake"   },
  { key: "Wu",   animal: "Horse"   }, { key: "Wei",  animal: "Goat"    },
  { key: "Shen", animal: "Monkey"  }, { key: "You",  animal: "Rooster" },
  { key: "Xu",   animal: "Dog"     }, { key: "Hai",  animal: "Pig"     }
];
const BRANCH_KEYS = BRANCHES.map(b => b.key);

const BRANCH_HIDDEN_STEMS = {
  Rat: ["Gui"], Ox: ["Ji","Xin","Gui"], Tiger: ["Jia","Bing","Wu"], Rabbit: ["Yi"],
  Dragon: ["Wu","Yi","Gui"], Snake: ["Bing","Geng","Wu"], Horse: ["Ding","Ji"],
  Goat: ["Ji","Yi","Ding"], Monkey: ["Geng","Ren","Wu"], Rooster: ["Xin"],
  Dog: ["Wu","Xin","Ding"], Pig: ["Ren","Jia"]
};

const HIDDEN_WEIGHTS = { 1: [1.00], 2: [0.70, 0.30], 3: [0.70, 0.20, 0.10] };

const SEASONAL_PRESETS = {
  CLASSIC: { "旺": 1.00, "相": 0.85, "休": 0.70, "囚": 0.50, "死": 0.30 },
  TWELVE:  { "旺": 1.00, "相": 0.90, "休": 0.75, "囚": 0.55, "死": 0.30 }
};

const GEN_CYCLE = ["Wood", "Fire", "Earth", "Metal", "Water"];
const KE_CYCLE  = ["Wood", "Earth", "Water", "Fire", "Metal"];
const TIGER_MONTH_STEM_BASE = { 0: 3, 1: 5, 2: 7, 3: 9, 4: 1 };

// ── Date helpers ──

function coerceDate(v) {
  if (v instanceof Date) return new Date(v.getTime());
  const d = new Date(v);
  if (!isNaN(d)) return d;
  throw new Error("Invalid date: " + v);
}

function jdFromDate(date) {
  return date.getTime() / 86400000 + 2440587.5;
}

function norm360(x) { x = x % 360; return x < 0 ? x + 360 : x; }

function localToUTC(localDate, tzHours) {
  return new Date(+coerceDate(localDate) - Number(tzHours) * 3600000);
}

function solarLongitudeUTC(utcDate) {
  const JD = jdFromDate(utcDate);
  const T  = (JD - 2451545.0) / 36525.0;
  const L0 = norm360(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
  const M  = norm360(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
  const Mr = M * Math.PI / 180;
  const C  = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(Mr)
           + (0.019993 - 0.000101 * T) * Math.sin(2 * Mr)
           + 0.000289 * Math.sin(3 * Mr);
  const trueLong = L0 + C;
  const omega = 125.04 - 1934.136 * T;
  return norm360(trueLong - 0.00569 - 0.00478 * Math.sin(omega * Math.PI / 180));
}

function solarLon(localDate, tzHours) {
  return solarLongitudeUTC(localToUTC(localDate, Number(tzHours)));
}

// ── Pillar helpers ──

function pillarFromIdx(stemIdx, branchIdx) {
  const stemKey    = STEM_KEYS[stemIdx - 1];
  const branchKey  = BRANCH_KEYS[branchIdx - 1];
  const stem       = STEMS.find(s => s.key === stemKey) || {};
  const branch     = BRANCHES.find(b => b.key === branchKey) || {};
  return { stemIdx, branchIdx, stemKey, stemElement: stem.element, branchKey, branchAnimal: branch.animal };
}

function adjustedYearForLichun(d, tz) {
  const y   = d.getFullYear();
  const lon = solarLon(d, tz);
  const m   = d.getMonth();
  const after = (m > 1) || (m === 1 && d.getDate() >= 4) || (lon >= 315 || lon < 45);
  return after ? y : y - 1;
}

function stemFromYear(y)   { return 1 + ((y - 4) % 10 + 10) % 10; }
function branchFromYear(y) { return 1 + ((y - 4) % 12 + 12) % 12; }

function monthBranchFromLon(lon) {
  const l = ((+lon % 360) + 360) % 360;
  const k = Math.floor(((l - 315 + 360) % 360) / 30);
  return (k % 12) + 1;
}

function monthStemFromYearStem(ys, mb) {
  const group = Math.floor((ys - 1) / 2);
  const base  = TIGER_MONTH_STEM_BASE[group];
  return 1 + ((base - 1 + (mb - 1)) % 10);
}

function hourBranchFromTime(d) {
  const h    = d.getHours() + d.getMinutes() / 60;
  const slot = Math.floor(((h + 1) % 24) / 2);
  return slot + 1;
}

function hourStemFromDayStem(ds, hb) {
  const bases = [1, 3, 5, 7, 9];
  const g     = Math.floor((ds - 1) / 2);
  return 1 + ((bases[g] - 1 + (hb - 1)) % 10);
}

function sexagenaryDay(localDT, tzHours, boundary) {
  let y = localDT.getFullYear(), m = localDT.getMonth(), d = localDT.getDate();
  if (String(boundary || "MIDNIGHT").toUpperCase() === "ZI") {
    const hrs = localDT.getHours() + localDT.getMinutes() / 60;
    if (hrs >= 23) {
      const next = new Date(localDT.getTime() + 86400000);
      y = next.getFullYear(); m = next.getMonth(); d = next.getDate();
    }
  }
  const localMid = new Date(y, m, d, 0, 0, 0);
  const utcMid   = localToUTC(localMid, tzHours);
  const JDN      = Math.floor(jdFromDate(utcMid) + 0.5);
  return { stemNum: 1 + ((JDN + 9) % 10 + 10) % 10, branchNum: 1 + ((JDN + 1) % 12 + 12) % 12 };
}

function dayStemObj(localDT, tzHours, boundary) {
  const n = sexagenaryDay(localDT, tzHours, boundary);
  const s = STEMS[n.stemNum - 1];
  return { key: s.key, element: s.element, yin: s.yin };
}

function dayBranchObj(localDT, tzHours, boundary) {
  const n = sexagenaryDay(localDT, tzHours, boundary);
  const b = BRANCHES[n.branchNum - 1];
  return { key: b.key, animal: b.animal };
}

function stemKeyToElement(key) {
  return STEMS.find(s => s.key === key)?.element || "";
}

function seasonElementFromLon(lon) {
  const l = ((+lon % 360) + 360) % 360;
  if (l >= 315 || l < 45)   return "Wood";
  if (l >= 45  && l < 135)  return "Fire";
  if (l >= 135 && l < 225)  return "Metal";
  return "Water";
}

function statusForElement(el, seasonEl) {
  if (el === seasonEl) return "旺";
  const si = GEN_CYCLE.indexOf(seasonEl);
  if (el === GEN_CYCLE[(si + 1) % 5]) return "相";
  if (el === GEN_CYCLE[(si + 4) % 5]) return "休";
  const ki = KE_CYCLE.indexOf(seasonEl);
  if (el === KE_CYCLE[(ki + 1) % 5]) return "囚";
  return "死";
}

function seasonalMult(el, sunLon, preset) {
  const table = SEASONAL_PRESETS[(preset || "CLASSIC").toUpperCase()] || SEASONAL_PRESETS.CLASSIC;
  return table[statusForElement(el, seasonElementFromLon(sunLon))] || 1.0;
}

function accumulatePillar(totals, pillar, weight, sunLon, preset) {
  totals[pillar.stemElement] += weight * seasonalMult(pillar.stemElement, sunLon, preset);
  const hidden = BRANCH_HIDDEN_STEMS[pillar.branchAnimal] || [];
  const splits = HIDDEN_WEIGHTS[hidden.length] || [];
  for (let i = 0; i < hidden.length; i++) {
    const el = stemKeyToElement(hidden[i]);
    totals[el] += (splits[i] || 0) * weight * seasonalMult(el, sunLon, preset);
  }
}

function fullPillars(localDT, tzHours, boundary) {
  const tz     = Number(tzHours);
  const lon    = solarLon(localDT, tz);
  const adjY   = adjustedYearForLichun(localDT, tz);
  const yStem  = stemFromYear(adjY);
  const yBranch = branchFromYear(adjY);
  const year   = pillarFromIdx(yStem, yBranch);
  const mBranch = monthBranchFromLon(lon);
  const mStem   = monthStemFromYearStem(yStem, mBranch);
  const month  = pillarFromIdx(mStem, mBranch);
  const dStemO  = dayStemObj(localDT, tz, boundary);
  const dBranchO = dayBranchObj(localDT, tz, boundary);
  const dStem  = STEM_KEYS.indexOf(dStemO.key) + 1;
  const dBranch = BRANCH_KEYS.indexOf(dBranchO.key) + 1;
  const day    = pillarFromIdx(dStem, dBranch);
  const hBranch = hourBranchFromTime(localDT);
  const hStem   = hourStemFromDayStem(dStem, hBranch);
  const hour   = pillarFromIdx(hStem, hBranch);
  return { year, month, day, hour, sunLon: lon };
}

function fullChartElementPct(localDT, tzHours, boundary, preset, wts) {
  const P  = fullPillars(localDT, tzHours, boundary);
  if (!P) return null;
  const W  = Object.assign({ year: 1, month: 2, day: 3, hour: 1 }, wts || {});
  const totals = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };
  accumulatePillar(totals, P.year,  W.year,  P.sunLon, preset);
  accumulatePillar(totals, P.month, W.month, P.sunLon, preset);
  accumulatePillar(totals, P.day,   W.day,   P.sunLon, preset);
  accumulatePillar(totals, P.hour,  W.hour,  P.sunLon, preset);
  const sum = Object.values(totals).reduce((a, b) => a + b, 0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el] / sum) * 100);
  return out;
}

function dayElementPct(localDT, tzHours, boundary, preset) {
  const s = dayStemObj(localDT, tzHours, boundary);
  const b = dayBranchObj(localDT, tzHours, boundary);
  if (!s || !b) return null;
  const lon    = solarLon(localDT, tzHours);
  const totals = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };
  totals[s.element] += 1 * seasonalMult(s.element, lon, preset);
  const hidden  = BRANCH_HIDDEN_STEMS[b.animal] || [];
  const weights = HIDDEN_WEIGHTS[hidden.length] || [];
  for (let i = 0; i < hidden.length; i++) {
    const el = stemKeyToElement(hidden[i]);
    totals[el] += (weights[i] || 0) * seasonalMult(el, lon, preset);
  }
  const sum = Object.values(totals).reduce((a, b) => a + b, 0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el] / sum) * 100);
  return out;
}

// ── Math helpers ──

function toVec01(pct) {
  return EL_ORDER.map(el => (pct && pct[el] != null ? Number(pct[el]) : 0) / 100);
}

function dotRel(from, to, M) {
  const left = new Array(5).fill(0);
  for (let i = 0; i < 5; i++) { let s = 0; for (let j = 0; j < 5; j++) s += from[j] * M[j][i]; left[i] = s; }
  let out = 0; for (let i = 0; i < 5; i++) out += left[i] * to[i]; return out;
}

function shape(x) { return Math.tanh(LUCKY_CFG.SHAPE_TANH_K * x); }

function entropy(v) {
  const eps = 1e-9; let H = 0;
  for (let i = 0; i < 5; i++) { const p = Math.max(eps, v[i]); H -= p * Math.log(p); }
  return H;
}

function peakiness(v) { return (Math.log(5) - entropy(v)) / Math.log(5); }

function controllerOf(el) {
  return { Wood: "Metal", Fire: "Water", Earth: "Wood", Metal: "Fire", Water: "Earth" }[el] || null;
}

function dominantEl(pct) {
  let best = "Wood", bestV = -1;
  for (const el of EL_ORDER) { const v = Number(pct[el] || 0); if (v > bestV) { bestV = v; best = el; } }
  return best;
}

// ── Core scorer ──

function personEnvScore(birthLocalDT, birthGMT, envLocalDT, envGMT, opts) {
  opts = opts || {};
  const boundary = String(opts.boundary || LUCKY_CFG.DEFAULT_BOUNDARY).toUpperCase();
  const preset   = String(opts.preset   || LUCKY_CFG.DEFAULT_PRESET).toUpperCase();

  const W = Object.assign({}, LUCKY_CFG.NATAL_W);
  W.year *= LUCKY_CFG.NATAL_YEAR_MULT;

  const personPct  = fullChartElementPct(birthLocalDT, Number(birthGMT), boundary, preset, W);
  const envDayPct  = dayElementPct(envLocalDT, Number(envGMT), boundary, preset);
  const envYearPct = fullChartElementPct(envLocalDT, Number(envGMT), boundary, preset, { year: 1, month: 0, day: 0, hour: 0 });

  if (!personPct || !envDayPct || !envYearPct) return null;

  const ed = toVec01(envDayPct);
  const ey = toVec01(envYearPct);

  const P          = fullPillars(envLocalDT, Number(envGMT), boundary);
  const yearStemEl = P?.year?.stemElement || "Earth";
  const counterEl  = controllerOf(yearStemEl);

  const eblend = new Array(5);
  for (let i = 0; i < 5; i++) eblend[i] = LUCKY_CFG.ENV_W_DAY * ed[i] + LUCKY_CFG.ENV_W_YEAR * ey[i];

  if (counterEl) {
    const idx = EL_ORDER.indexOf(counterEl);
    if (idx >= 0) eblend[idx] += LUCKY_CFG.ENV_COUNTER_BOOST;
  }

  const sumE = eblend.reduce((a, b) => a + Math.max(0, b), 0) || 1;
  for (let i = 0; i < 5; i++) eblend[i] = Math.max(0, eblend[i]) / sumE;

  const a       = toVec01(personPct);
  const e       = eblend;
  const env_peak = peakiness(e);
  const raw      = shape(dotRel(e, a, LUCKY_CFG.ENV_MATRIX) * (1 + LUCKY_CFG.PEAK_ENV_GAIN * env_peak));

  const total     = Math.round((raw * 0.5 + 0.5) * 100);
  const stability = env_peak <= LUCKY_CFG.STABLE_MAX ? "Stable" : env_peak >= LUCKY_CFG.SWINGY_MIN ? "Swingy" : "Normal";

  return {
    total,
    stability,
    env_peak,
    dom_person: dominantEl(personPct),
    dom_env:    dominantEl({ Wood: Math.round(e[0] * 100), Fire: Math.round(e[1] * 100),
                             Earth: Math.round(e[2] * 100), Metal: Math.round(e[3] * 100),
                             Water: Math.round(e[4] * 100) })
  };
}

// ── Zone mapping ──

export function colorZoneFromDelta(d) {
  if (d >= 14)  return "Pink";
  if (d >= 7)   return "Orange";
  if (d >= 4)   return "Blue";
  if (d >= -2)  return "Yellow";
  if (d >= -4)  return "Green";
  if (d >= -9)  return "Purple";
  if (d >= -11) return "Green";
  if (d >= -15) return "Blue";
  if (d >= -29) return "Red";
  return "Brown";
}

export function bandFromDelta(d) {
  if (d >= 14)  return "Peak";
  if (d >= 7)   return "Strong";
  if (d >= 4)   return "Favorable";
  if (d >= -2)  return "Baseline";
  if (d >= -4)  return "Mild friction";
  if (d >= -9)  return "Challenged";
  if (d >= -11) return "Recovery";
  if (d >= -15) return "Recovery";
  if (d >= -29) return "Adverse";
  return "Floor";
}

export const ZONE_MANTRAS = {
  Pink:   "Full expression",
  Orange: "Make your move",
  Blue:   "Think it through",
  Yellow: "Show up present",
  Green:  "Build the habit",
  Purple: "Go inward",
  Red:    "Careful aggression",
  Brown:  "Rest and reset"
};

// ── Public API ──

/**
 * Calculate the lucky window zone for a birth profile on a given date.
 *
 * @param {Object} params
 * @param {Date|string} params.birthDate     — birth date
 * @param {string}      params.birthTime     — "HH:MM" (24h) or "12:00" if unknown
 * @param {number}      params.birthGMT      — birth timezone UTC offset
 * @param {Date|string} params.eventDate     — target date to score
 * @param {number}      params.eventGMT      — event timezone UTC offset
 * @param {string}      [params.windowType]  — "AM" | "PM" (default "AM")
 * @returns {{ zone, band, delta, total, stability, mantra }}
 */
export function calcLuckyWindow({ birthDate, birthTime, birthGMT, eventDate, eventGMT, windowType = "AM" }) {
  const bt       = birthTime || "12:00";
  const [bh, bm] = bt.split(":").map(Number);

  // Parse birthDate as a LOCAL date — new Date("YYYY-MM-DD") is UTC midnight in JS,
  // which shifts the day backward in UTC- timezones and breaks all pillar calculations.
  let by, bmo, bdy;
  if (typeof birthDate === "string" && /^\d{4}-\d{2}-\d{2}$/.test(birthDate)) {
    [by, bmo, bdy] = birthDate.split("-").map(Number);
    bmo -= 1; // JS months are 0-indexed
  } else {
    const bd = coerceDate(birthDate);
    by = bd.getFullYear(); bmo = bd.getMonth(); bdy = bd.getDate();
  }
  const birthLocalDT = new Date(by, bmo, bdy, bh, bm, 0);

  const hour = windowType === "PM" ? LUCKY_CFG.PM_HOUR : LUCKY_CFG.AM_HOUR;
  const ed   = coerceDate(eventDate);
  const envLocalDT = new Date(ed.getFullYear(), ed.getMonth(), ed.getDate(), hour, 0, 0);

  const r = personEnvScore(birthLocalDT, Number(birthGMT), envLocalDT, Number(eventGMT), {
    boundary: "MIDNIGHT",
    preset: "CLASSIC"
  });

  if (!r) throw new Error("Calculation failed — check inputs.");

  const delta = r.total - LUCKY_BASELINE;
  const zone  = colorZoneFromDelta(delta);
  const band  = bandFromDelta(delta);

  return {
    zone,
    band,
    delta,
    total:      r.total,
    edge50:     r.total - 50,
    stability:  r.stability,
    mantra:     ZONE_MANTRAS[zone],
    dom_person: r.dom_person,
    dom_env:    r.dom_env
  };
}

/**
 * Calculate lucky window for the current day.
 */
export function calcTodayWindow({ birthDate, birthTime, birthGMT, currentGMT }) {
  const gmt = currentGMT ?? birthGMT ?? 0;
  return calcLuckyWindow({
    birthDate,
    birthTime,
    birthGMT,
    eventDate: new Date(),
    eventGMT: gmt
  });
}
