/****************************************************
 * 21_utils_elements_math.gs
 * LUCKIFY ME — Element & Math Utilities
 *
 * RULE: NO Sheets access. NO SpreadsheetApp. Ever.
 *       Pure math and element helper functions only.
 ****************************************************/

/* =========================
   VECTOR HELPERS
========================= */

function _toVec01_(pctObj) {
  return EL_ORDER.map(el => (pctObj && pctObj[el] != null ? Number(pctObj[el]) : 0) / 100);
}

function _vecToPct_(vec01) {
  const out = {};
  for (let i = 0; i < 5; i++) out[EL_ORDER[i]] = Math.round((vec01[i] || 0) * 100);
  return out;
}

function _dotRel_(from, to, M) {
  const left = new Array(5).fill(0);
  for (let i = 0; i < 5; i++) {
    let s = 0;
    for (let j = 0; j < 5; j++) s += from[j] * M[j][i];
    left[i] = s;
  }
  let out = 0;
  for (let i = 0; i < 5; i++) out += left[i] * to[i];
  return out;
}

/* =========================
   SCORE SHAPING
========================= */

function _shape_(x) {
  return Math.tanh(LUCKY_CFG.SHAPE_TANH_K * x);
}

function _entropy_(v) {
  const eps = 1e-9;
  let H = 0;
  for (let i = 0; i < 5; i++) {
    const p = Math.max(eps, v[i]);
    H -= p * Math.log(p);
  }
  return H;
}

function _peakiness_(v) {
  const Hmax = Math.log(5);
  return (Hmax - _entropy_(v)) / Hmax;
}

/* =========================
   ELEMENT RELATIONSHIP HELPERS
========================= */

function _controllerOf_(el) {
  return { Wood:"Metal", Fire:"Water", Earth:"Wood", Metal:"Fire", Water:"Earth" }[el] || null;
}

function _dominantEl_(pctObj) {
  let best = "Wood", bestV = -1;
  for (const el of EL_ORDER) {
    const v = Number(pctObj[el] || 0);
    if (v > bestV) { bestV = v; best = el; }
  }
  return best;
}
