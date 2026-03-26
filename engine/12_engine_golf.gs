/****************************************************
 * 12_engine_golf.gs
 * LUCKIFY ME — Golf Luck Scoring Engine
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure functions only.
 *
 * OUTPUT: [[execScore, upsideScore, peak]]
 ****************************************************/

/* =========================
   PUBLIC API
========================= */

function GOLF_LUCK_SCORES_NO_BIRTH_TIME(birthDate, birthGMT, envDate, envTime, envTZ, boundary, preset) {
  const b = String(boundary || "ZI").toUpperCase();
  const p = String(preset   || "CLASSIC").toUpperCase();

  const birthLocalDT = _WD_buildLocalDT_(birthDate, "12:00");
  const envLocalDT   = _WD_buildLocalDT_(envDate, _WD_normTime_(envTime, "12:00"));
  const envGMT       = _envGMTFromTZIDorOffset_(envTZ, envLocalDT);

  const dmEl         = _WD_dayStemElement_(birthLocalDT, Number(birthGMT), b);
  const envStemEl    = _WD_dayStemElement_(envLocalDT, Number(envGMT), b);
  const envHiddenEls = _WD_hiddenElementsFromDayBranch_(envLocalDT, Number(envGMT), b);
  const env          = _GOLF_envBlend_(envLocalDT, Number(envGMT), b, p);
  const out          = _GOLF_scoreDual_(dmEl, envStemEl, envHiddenEls, env.peak);

  return [[out.execScore, out.upsideScore, +env.peak.toFixed(3)]];
}

/* =========================
   DAY STEM HELPERS
========================= */

function _WD_dayStemElement_(localDT, tzHours, boundary) {
  const s = BAZI_DAY_STEM_OBJ(localDT, tzHours, boundary);
  if (!s || !s.element) throw new Error("Could not compute day stem element.");
  return s.element;
}

function _WD_hiddenElementsFromDayBranch_(localDT, tzHours, boundary) {
  const b = BAZI_DAY_BRANCH_OBJ(localDT, tzHours, boundary);
  if (!b || !b.animal) return [];
  return (BRANCH_HIDDEN_STEMS[b.animal] || []).map(k => _stemKeyToElement_(k)).filter(Boolean);
}

function _WD_wealthEl_(dmEl)   { return ({Wood:"Earth",  Fire:"Metal", Earth:"Water", Metal:"Wood",  Water:"Fire" })[dmEl] || null; }
function _WD_resourceEl_(dmEl) { return ({Wood:"Water",  Fire:"Wood",  Earth:"Fire",  Metal:"Earth", Water:"Metal"})[dmEl] || null; }
function _WD_outputEl_(dmEl)   { return ({Wood:"Fire",   Fire:"Earth", Earth:"Metal", Metal:"Water", Water:"Wood" })[dmEl] || null; }
function _WD_powerEl_(dmEl)    { return _controllerOf_(dmEl); }

/* =========================
   ENVIRONMENT BLEND
========================= */

function _GOLF_envBlend_(envLocalDT, envGMT, boundary, preset) {
  const dayPct  = BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(envLocalDT, envGMT, boundary, preset);
  const yearPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(
    envLocalDT, envGMT, boundary, preset,
    { year: 1, month: 0, day: 0, hour: 0 }
  );

  const vd = dayPct  ? _toVec01_(dayPct)  : [0,0,0,0,0];
  const vy = yearPct ? _toVec01_(yearPct) : [0,0,0,0,0];

  const v = new Array(5).fill(0);
  for (let i = 0; i < 5; i++) {
    v[i] = GOLF_CFG.ENV_W_DAY * vd[i] + GOLF_CFG.ENV_W_YEAR * vy[i];
  }

  const sum = v.reduce((a, b) => a + Math.max(0, b), 0) || 1;
  for (let i = 0; i < 5; i++) v[i] = Math.max(0, v[i]) / sum;

  return { vec: v, peak: _peakiness_(v) };
}

/* =========================
   DUAL SCORE CALCULATOR
========================= */

function _GOLF_scoreDual_(dmEl, envStemEl, envHiddenEls, env_peak) {
  const resourceEl = _WD_resourceEl_(dmEl);
  const outputEl   = _WD_outputEl_(dmEl);
  const powerEl    = _WD_powerEl_(dmEl);
  const wealthEl   = _WD_wealthEl_(dmEl);

  let exec = GOLF_CFG.EXEC.base;
  let up   = GOLF_CFG.UPSIDE.base;

  const peak       = Math.max(0, Math.min(1, Number(env_peak || 0)));
  const hiddenMult = _GOLF_hiddenMult_(peak);

  // ── EXEC scoring ──
  if (envStemEl === resourceEl)              exec += GOLF_CFG.EXEC.resourceStem;
  if (envHiddenEls.includes(resourceEl))     exec += GOLF_CFG.EXEC.resourceHidden * hiddenMult;
  if (envStemEl === powerEl)                 exec += GOLF_CFG.EXEC.powerStem;
  if (envHiddenEls.includes(powerEl))        exec += GOLF_CFG.EXEC.powerHidden * hiddenMult;
  if (envStemEl === outputEl)                exec += GOLF_CFG.EXEC.outputStem;
  if (envStemEl === wealthEl)                exec += GOLF_CFG.EXEC.wealthStem;
  if (envStemEl === dmEl)                    exec += GOLF_CFG.EXEC.peerStem;

  const powerPresent    = (envStemEl === powerEl)    || envHiddenEls.includes(powerEl);
  const resourcePresent = (envStemEl === resourceEl) || envHiddenEls.includes(resourceEl);

  if (powerPresent && !resourcePresent) exec += GOLF_CFG.POWER_SUPPORT.noResourcePenaltyExec;
  if (powerPresent &&  resourcePresent) exec += GOLF_CFG.POWER_SUPPORT.supportedBonusExec;

  exec -= GOLF_CFG.EXEC.peakPenaltyK * peak;

  // ── UPSIDE scoring ──
  if (envStemEl === outputEl)                up += GOLF_CFG.UPSIDE.outputStem;
  if (envHiddenEls.includes(outputEl))       up += GOLF_CFG.UPSIDE.outputHidden * hiddenMult;
  if (envStemEl === wealthEl)                up += GOLF_CFG.UPSIDE.wealthStem;
  if (envHiddenEls.includes(wealthEl))       up += GOLF_CFG.UPSIDE.wealthHidden * hiddenMult;
  if (envStemEl === resourceEl)              up += GOLF_CFG.UPSIDE.resourceStem;
  if (envStemEl === powerEl)                 up += GOLF_CFG.UPSIDE.powerStem;
  if (envStemEl === dmEl)                    up += GOLF_CFG.UPSIDE.peerStem;

  if (powerPresent && !resourcePresent)      up += GOLF_CFG.POWER_SUPPORT.noResourcePenaltyUpside;

  up += GOLF_CFG.UPSIDE.peakPlateauBonusK * _GOLF_plateauBonus_(peak);

  if (peak > GOLF_CFG.UPSIDE.extremeStart) {
    const t = (peak - GOLF_CFG.UPSIDE.extremeStart) / (1 - GOLF_CFG.UPSIDE.extremeStart);
    up -= GOLF_CFG.UPSIDE.peakExtremePenaltyK * Math.max(0, Math.min(1, t));
  }

  exec = Math.max(0, Math.min(100, Math.round(exec)));
  up   = Math.max(0, Math.min(100, Math.round(up)));

  return {
    execScore:   exec,
    upsideScore: up,
    execRaw:     +exec.toFixed(2),
    upsideRaw:   +up.toFixed(2),
    execLabel:   _GOLF_execLabel_(exec),
    upsideLabel: _GOLF_upsideLabel_(up)
  };
}

/* =========================
   HELPER FUNCTIONS
========================= */

function _GOLF_hiddenMult_(peak) {
  const p = Math.max(0, Math.min(1, Number(peak || 0)));
  const a = GOLF_CFG.HIDDEN_DAMP_START;
  const b = GOLF_CFG.HIDDEN_DAMP_END;
  if (p <= a) return 1;
  if (p >= b) return 0.35;
  const t = (p - a) / (b - a);
  return 1 - (0.65 * t);
}

function _GOLF_plateauBonus_(peak) {
  const p = Math.max(0, Math.min(1, Number(peak || 0)));
  if (p <= 0.20) return p / 0.20 * 0.35;
  if (p <= 0.45) return 0.35 + ((p - 0.20) / 0.25) * 0.65;
  if (p <= 0.65) return 1.0;
  if (p <= 0.82) return 1.0 - ((p - 0.65) / 0.17) * 0.55;
  return 0.45;
}

function _GOLF_execLabel_(score) {
  if (score >= 80) return "Locked In";
  if (score >= 65) return "Clean";
  if (score >= 50) return "Playable";
  if (score >= 35) return "Messy";
  return "Avoid Force";
}

function _GOLF_upsideLabel_(score) {
  if (score >= 80) return "Heater Potential";
  if (score >= 65) return "Birdie Runs";
  if (score >= 50) return "Neutral";
  if (score >= 35) return "Grind Mode";
  return "Blow-Up Risk";
}
