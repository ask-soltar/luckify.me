/****************************************************
 * 13_engine_bazi_core.gs
 * LUCKIFY ME — BaZi Core Engine
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure functions only. This is the foundational IP.
 *
 * Contains: solar longitude, sexagenary day numbers,
 *           all BaZi pillar calculations, seasonal multipliers,
 *           element accumulation.
 ****************************************************/

/* =========================
   SOLAR LONGITUDE
========================= */

function jdFromDate(date) {
  let d = date;
  if (!(d instanceof Date)) d = new Date(d);
  if (isNaN(d)) throw new Error("jdFromDate: invalid Date");
  return d.getTime() / 86400000 + 2440587.5;
}

function norm360(x) { x = x % 360; return x < 0 ? x + 360 : x; }

function solarLongitudeUTC(utcDate) {
  if (!(utcDate instanceof Date) || isNaN(utcDate)) throw new Error("solarLongitudeUTC: invalid Date");
  const JD = jdFromDate(utcDate);
  const T  = (JD - 2451545.0) / 36525.0;
  const L0 = norm360(280.46646 + 36000.76983*T + 0.0003032*T*T);
  const M  = norm360(357.52911 + 35999.05029*T - 0.0001537*T*T);
  const Mr = M * Math.PI/180;
  const C  = (1.914602 - 0.004817*T - 0.000014*T*T) * Math.sin(Mr)
           + (0.019993 - 0.000101*T) * Math.sin(2*Mr)
           + 0.000289 * Math.sin(3*Mr);
  const trueLong = L0 + C;
  const omega    = 125.04 - 1934.136*T;
  const lambda   = trueLong - 0.00569 - 0.00478 * Math.sin(omega * Math.PI/180);
  return norm360(lambda);
}

function SOLAR_LON(dateSerialOrDate, tzHours) {
  const local = _coerceDate_(dateSerialOrDate);
  const tz    = Number(tzHours);
  if (!isFinite(tz)) return "";
  return solarLongitudeUTC(localToUTC(local, tz));
}

/* =========================
   BAZI PILLAR BUILDERS
========================= */

function _pillarFromStemBranchIdx_(stemIdx, branchIdx) {
  const stemKey   = STEM_KEYS[stemIdx-1];
  const branchKey = BRANCH_KEYS[branchIdx-1];
  const stem      = STEMS.find(s => s.key === stemKey) || {};
  return { stemIdx, branchIdx, stemKey, stemElement: stem.element, branchKey, branchAnimal: BRANCH_ANIMALS[branchKey] };
}

function _stemIndexFromYear_(y)   { return 1 + ((y-4)%10 + 10)%10; }
function _branchIndexFromYear_(y) { return 1 + ((y-4)%12 + 12)%12; }

function _adjustedYearForLichun_(d, tz) {
  const y      = d.getFullYear();
  const sunLon = SOLAR_LON(d, tz);
  const m      = d.getMonth();
  const after  = (m>1) || (m===1 && d.getDate()>=4) || (sunLon>=315 || sunLon<45);
  return after ? y : y-1;
}

function _monthBranchIndexFromSunLon_(sunLon) {
  const lon = ((+sunLon % 360) + 360) % 360;
  const k   = Math.floor(((lon - 315 + 360) % 360) / 30);
  return (k % 12) + 1;
}

function _monthStemIndexFromYearStemAndMonthBranch_(ys, mb) {
  const group = Math.floor((ys-1)/2);
  const base  = TIGER_MONTH_STEM_BASE_BY_YEAR_GROUP[group];
  return 1 + ((base - 1 + (mb - 1)) % 10);
}

function _hourBranchIndexFromLocalTime_(d) {
  const h = d.getHours() + d.getMinutes()/60;
  return Math.floor(((h + 1) % 24) / 2) + 1;
}

function _hourStemIndexFromDayStemAndHourBranch_(ds, hb) {
  const baseByDayGroup = [1,3,5,7,9];
  const g = Math.floor((ds-1)/2);
  return 1 + ((baseByDayGroup[g] - 1 + (hb - 1)) % 10);
}

function _stemKeyToElement_(key) {
  const s = STEMS.find(x => x.key === key);
  return s ? s.element : "";
}

/* =========================
   PUBLIC PILLAR FUNCTIONS
========================= */

function BAZI_FULL_PILLARS(dateSerialOrDate, tzHours, boundary) {
  const local    = _coerceDate_(dateSerialOrDate);
  const tz       = Number(tzHours);
  const sunLon   = SOLAR_LON(local, tz);
  const adjYear  = _adjustedYearForLichun_(local, tz);
  const yStem    = _stemIndexFromYear_(adjYear);
  const yBranch  = _branchIndexFromYear_(adjYear);
  const year     = _pillarFromStemBranchIdx_(yStem, yBranch);
  const mBranch  = _monthBranchIndexFromSunLon_(sunLon);
  const mStem    = _monthStemIndexFromYearStemAndMonthBranch_(yStem, mBranch);
  const month    = _pillarFromStemBranchIdx_(mStem, mBranch);
  const dStemObj = BAZI_DAY_STEM_OBJ(local, tz, boundary);
  const dBranchObj = BAZI_DAY_BRANCH_OBJ(local, tz, boundary);
  const dStem    = STEM_KEYS.indexOf(dStemObj.key) + 1;
  const dBranch  = BRANCH_KEYS.indexOf(dBranchObj.key) + 1;
  const day      = _pillarFromStemBranchIdx_(dStem, dBranch);
  const hBranch  = _hourBranchIndexFromLocalTime_(local);
  const hStem    = _hourStemIndexFromDayStemAndHourBranch_(dStem, hBranch);
  const hour     = _pillarFromStemBranchIdx_(hStem, hBranch);
  return { year, month, day, hour, sunLon };
}

function BAZI_DAY_STEM_OBJ(dateSerialOrDate, tzHours, boundary) {
  const nums = _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary);
  if (!nums) return "";
  const stem = STEMS[nums.stemNum-1];
  return { key: stem.key, element: stem.element, yin: stem.yin };
}

function BAZI_DAY_BRANCH_OBJ(dateSerialOrDate, tzHours, boundary) {
  const nums = _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary);
  if (!nums) return "";
  const br = BRANCHES[nums.branchNum-1];
  return { key: br.key, animal: br.animal };
}

function BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(dateSerialOrDate, tzHours, boundary, preset, pillarWeights) {
  const P = BAZI_FULL_PILLARS(dateSerialOrDate, tzHours, boundary);
  if (!P) return "";
  const sunLon = P.sunLon;
  const W = Object.assign({year:1,month:2,day:3,hour:1}, pillarWeights || {});
  const totals = {Wood:0,Fire:0,Earth:0,Metal:0,Water:0};
  _accumulatePillar_(totals, P.year,  W.year,  sunLon, preset);
  _accumulatePillar_(totals, P.month, W.month, sunLon, preset);
  _accumulatePillar_(totals, P.day,   W.day,   sunLon, preset);
  _accumulatePillar_(totals, P.hour,  W.hour,  sunLon, preset);
  const sum = Object.values(totals).reduce((a,b)=>a+b,0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el]/sum)*100);
  return out;
}

function BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(dateSerialOrDate, tzHours, boundary, preset) {
  const s = BAZI_DAY_STEM_OBJ(dateSerialOrDate, tzHours, boundary);
  const b = BAZI_DAY_BRANCH_OBJ(dateSerialOrDate, tzHours, boundary);
  if (!s || !b) return "";
  const sunLon = SOLAR_LON(dateSerialOrDate, tzHours);
  const totals = {Wood:0,Fire:0,Earth:0,Metal:0,Water:0};
  totals[s.element] += 1 * _seasonalMultiplier_(s.element, sunLon, preset);
  const hidden  = BRANCH_HIDDEN_STEMS[b.animal] || [];
  const weights = HIDDEN_WEIGHTS_BY_COUNT[hidden.length] || [];
  for (let i = 0; i < hidden.length; i++) {
    const el = _stemKeyToElement_(hidden[i]);
    totals[el] += (weights[i] || 0) * _seasonalMultiplier_(el, sunLon, preset);
  }
  const sum = Object.values(totals).reduce((a,b)=>a+b,0) || 1;
  const out = {};
  for (const el of EL_ORDER) out[el] = Math.round((totals[el]/sum)*100);
  return out;
}

/* =========================
   SEXAGENARY DAY NUMBERS
========================= */

function _sexagenaryDayNumbers_(dateSerialOrDate, tzHours, boundary) {
  if (dateSerialOrDate == null || tzHours == null) return null;
  const tz      = Number(tzHours);
  const localDT = _coerceDate_(dateSerialOrDate);
  let y = localDT.getFullYear(), m = localDT.getMonth(), d = localDT.getDate();

  if (String(boundary||"MIDNIGHT").toUpperCase() === "ZI") {
    const hrs = localDT.getHours() + localDT.getMinutes()/60;
    if (hrs >= 23) {
      const next = new Date(localDT.getTime() + 86400000);
      y = next.getFullYear();
      m = next.getMonth();
      d = next.getDate();
    }
  }

  const localMid = new Date(y, m, d, 0, 0, 0);
  const utcMid   = localToUTC(localMid, tz);
  const JD0      = jdFromDate(utcMid);
  const JDN      = Math.floor(JD0 + 0.5);

  return {
    stemNum:   1 + ((JDN + 9) % 10 + 10) % 10,
    branchNum: 1 + ((JDN + 1) % 12 + 12) % 12
  };
}

/* =========================
   SEASONAL MULTIPLIERS
========================= */

function _seasonElementFromLon_(lon) {
  lon = ((+lon%360)+360)%360;
  if (lon>=315 || lon<45)  return "Wood";
  if (lon>=45  && lon<135) return "Fire";
  if (lon>=135 && lon<225) return "Metal";
  return "Water";
}

function _statusForElementRelativeToSeason_(el, seasonEl) {
  if (el === seasonEl) return "旺";
  const sIdx = GEN_CYCLE.indexOf(seasonEl);
  if (el === GEN_CYCLE[(sIdx+1)%5]) return "相";
  if (el === GEN_CYCLE[(sIdx+4)%5]) return "休";
  const kIdx = KE_CYCLE.indexOf(seasonEl);
  if (el === KE_CYCLE[(kIdx+1)%5]) return "囚";
  return "死";
}

function _seasonalMultiplier_(el, sunLon, preset) {
  const seasonEl = _seasonElementFromLon_(sunLon);
  const status   = _statusForElementRelativeToSeason_(el, seasonEl);
  const table    = SEASONAL_PRESETS[(preset||"CLASSIC").toUpperCase()] || SEASONAL_PRESETS.CLASSIC;
  return table[status] || 1.0;
}

function _accumulatePillar_(totals, pillar, weight, sunLon, preset) {
  totals[pillar.stemElement] += weight * _seasonalMultiplier_(pillar.stemElement, sunLon, preset);
  const hidden = BRANCH_HIDDEN_STEMS[pillar.branchAnimal] || [];
  const splits = HIDDEN_WEIGHTS_BY_COUNT[hidden.length] || [];
  for (let i = 0; i < hidden.length; i++) {
    const el = _stemKeyToElement_(hidden[i]);
    totals[el] += (splits[i] || 0) * weight * _seasonalMultiplier_(el, sunLon, preset);
  }
}
