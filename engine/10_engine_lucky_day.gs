/****************************************************
 * 10_engine_lucky_day.gs
 * LUCKIFY ME — Lucky Day Engine
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure functions only. Given the same inputs,
 *       always returns the same outputs.
 ****************************************************/

/* =========================
   PUBLIC API
========================= */

function LUCKY_DAY_DELTA(birthDT, birthGMT, dayDate, envTZ, hour, minute, baseline, boundary, preset) {
  const base = (baseline === undefined || baseline === null || baseline === "")
    ? LUCKY_BASELINE
    : Number(baseline);
  return _luckyDayDeltaFromWindow_(
    birthDT, birthGMT, dayDate, envTZ,
    Number(hour || LUCKY_CFG.AM_HOUR),
    Number(minute || 0),
    boundary, preset, base
  );
}

/* =========================
   CORE SCORING
========================= */

function _luckyDayDeltaFromWindow_(birthDT, birthGMT, dayDate, envTZ, hour, minute, boundary, preset, baselineOverride) {
  const envLocalDT = _buildLocalDateTime_(dayDate, Number(hour), Number(minute));
  const envGMT     = _envGMTFromTZIDorOffset_(envTZ, envLocalDT);
  const r = _cachedPersonEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, {
    boundary: boundary || LUCKY_CFG.DEFAULT_BOUNDARY,
    preset:   preset   || LUCKY_CFG.DEFAULT_PRESET
  });
  if (!r) return "";
  const baseline = (baselineOverride === undefined || baselineOverride === null)
    ? LUCKY_BASELINE
    : Number(baselineOverride);
  if (!isFinite(baseline)) throw new Error("Baseline must be numeric.");
  return r.total - baseline;
}

function _cachedPersonEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts) {
  const key = JSON.stringify(["LDv1", _safeKey_(birthDT), birthGMT, _safeKey_(envLocalDT), envGMT, opts]);
  if (_MEMO.personEnv[key]) return _MEMO.personEnv[key];
  const r = _personEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts);
  _MEMO.personEnv[key] = r;
  return r;
}

function _personEnvScore_(birthDT, birthGMT, envLocalDT, envGMT, opts) {
  opts = opts || {};
  const boundary = String(opts.boundary || LUCKY_CFG.DEFAULT_BOUNDARY).toUpperCase();
  const preset   = String(opts.preset   || LUCKY_CFG.DEFAULT_PRESET).toUpperCase();
  const W = Object.assign({}, LUCKY_CFG.NATAL_W);
  W.year *= LUCKY_CFG.NATAL_YEAR_MULT;

  const personPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(birthDT, Number(birthGMT), boundary, preset, W);
  if (!personPct) return null;
  const envDayPct = BAZI_DAY_ELEMENT_PERCENT_WEIGHTED_SEASONAL_OBJ(envLocalDT, Number(envGMT), boundary, preset);
  if (!envDayPct) return null;
  const envYearPct = BAZI_FULL_CHART_ELEMENT_PERCENT_OBJ(envLocalDT, Number(envGMT), boundary, preset, {year:1,month:0,day:0,hour:0});
  if (!envYearPct) return null;

  const ed = _toVec01_(envDayPct);
  const ey = _toVec01_(envYearPct);
  const P  = BAZI_FULL_PILLARS(envLocalDT, Number(envGMT), boundary);
  const yearStemEl = (P && P.year && P.year.stemElement) ? P.year.stemElement : "Earth";
  const counterEl  = _controllerOf_(yearStemEl);

  let eblend = new Array(5);
  for (let i = 0; i < 5; i++) eblend[i] = LUCKY_CFG.ENV_W_DAY * ed[i] + LUCKY_CFG.ENV_W_YEAR * ey[i];
  if (counterEl) {
    const idx = EL_ORDER.indexOf(counterEl);
    if (idx >= 0) eblend[idx] += LUCKY_CFG.ENV_COUNTER_BOOST;
  }
  const sumE = eblend.reduce((a, b) => a + Math.max(0, b), 0) || 1;
  for (let i = 0; i < 5; i++) eblend[i] = Math.max(0, eblend[i]) / sumE;

  const a       = _toVec01_(personPct);
  const e       = eblend;
  const env_peak = _peakiness_(e);
  const raw     = _shape_(_dotRel_(e, a, LUCKY_CFG.ENV_MATRIX) * (1 + LUCKY_CFG.PEAK_ENV_GAIN * env_peak));
  const total   = Math.round((raw * 0.5 + 0.5) * 100);
  const edge50  = total - 50;
  const stability = (env_peak <= LUCKY_CFG.STABLE_MAX) ? "Stable"
                  : (env_peak >= LUCKY_CFG.SWINGY_MIN) ? "Swingy" : "Normal";
  const label   = _labelFromTotal_(total);

  return {
    total, edge50, label, stability, env_peak, yearStemEl,
    person:     personPct,
    env_vec:    e,
    dom_person: _dominantEl_(personPct),
    dom_env:    _dominantEl_(_vecToPct_(e))
  };
}

function _labelFromTotal_(total) {
  if (total >= 80) return "Greenlight++";
  if (total >= 65) return "Greenlight+";
  if (total >= 50) return "Neutral";
  if (total >= 35) return "Friction";
  return "Red";
}
