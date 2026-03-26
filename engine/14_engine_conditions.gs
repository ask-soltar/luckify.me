/****************************************************
 * 14_engine_conditions.gs
 * LUCKIFY ME — Conditions Scoring Engine
 *
 * RULE: NO Sheets access. NO API calls. NO SpreadsheetApp. Ever.
 *       Pure function only. Takes a weather data object,
 *       returns a label + numeric score.
 *       API calls live in 07_fetcher_conditions.gs only.
 ****************************************************/

function CONDITIONS_CALCULATE_(data) {
  const avgTemp = (data.tempMax + data.tempMin) / 2;
  let score = 0;

  // Wind speed scoring
  if      (data.wind >= 25) score += 4;
  else if (data.wind >= 18) score += 3;
  else if (data.wind >= 12) score += 2;
  else if (data.wind >= 7)  score += 1;

  // Gusts scoring
  if      (data.gusts >= 35) score += 2;
  else if (data.gusts >= 25) score += 1;

  // Temperature scoring
  if      (avgTemp < 40) score += 2;
  else if (avgTemp < 55) score += 1;
  else if (avgTemp > 90) score += 1;

  // Precipitation scoring
  if      (data.precip >= 10) score += 2;
  else if (data.precip >= 3)  score += 1;

  // Label
  if      (score >= 6) return "Tough";
  else if (score >= 3) return "Moderate";
  else                 return "Calm";
}
