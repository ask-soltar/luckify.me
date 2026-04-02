/****************************************************
 * 07c_fetcher_espn_players.gs
 * LUCKIFY ME — ESPN Golf Player Fetcher (PGA Athletes API)
 *
 * RULE: This is the ONLY file that makes ESPN API calls.
 *       Returns raw player data objects. No Sheets access.
 *       Caching layer prevents duplicate lookups.
 *
 * API: ESPN PGA Athletes endpoint (requires numeric player ID)
 * Data: Player names, birthdates, birthplace
 ****************************************************/

var ESPN_MEMO = {
  athletes: {}  // Cache athlete objects by ID
};

/**
 * ESPN_FETCH_ATHLETE_BY_ID_(playerId)
 * Fetches full athlete profile from ESPN PGA API using numeric player ID.
 * Extracts dateOfBirth and birthPlace.
 *
 * API: https://sports.core.api.espn.com/v2/sports/golf/leagues/pga/athletes/{playerId}
 */
function ESPN_FETCH_ATHLETE_BY_ID_(playerId) {
  if (!playerId) {
    return { error: "No player ID", found: false };
  }

  var playerId_str = String(playerId);
  var cacheKey = "espn_athlete_" + playerId_str;

  // In-memory memo check
  if (ESPN_MEMO.athletes[cacheKey]) {
    return ESPN_MEMO.athletes[cacheKey];
  }

  // Apps Script cache check (persists 6 hours)
  var cache = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    ESPN_MEMO.athletes[cacheKey] = parsed;
    return parsed;
  }

  var profileUrl = "https://sports.core.api.espn.com/v2/sports/golf/leagues/pga/athletes/" + playerId_str;

  try {
    var response = UrlFetchApp.fetch(profileUrl, {
      muteHttpExceptions: true,
      headers: { "User-Agent": "Luckify-Me/1.0" }
    });

    var code = response.getResponseCode();

    if (code === 429) {
      return { retry: true, error: "Rate limited", found: false };
    }

    if (code === 404) {
      // Player not found — cache this so we don't retry forever
      var notFoundOutput = {
        playerId: playerId_str,
        error: "Player not found",
        found: false
      };
      cache.put(cacheKey, JSON.stringify(notFoundOutput), 21600); // 6 hours
      return notFoundOutput;
    }

    if (code !== 200) {
      return { error: "API error: " + code, found: false };
    }

    var json = JSON.parse(response.getContentText());

    // Extract date of birth and format it
    var dob = json.dateOfBirth ? json.dateOfBirth.substring(0, 10) : "";

    // Extract birthplace
    var birthplace = "";
    if (json.birthPlace) {
      var city = json.birthPlace.city || "";
      var state = json.birthPlace.state || "";
      var country = json.birthPlace.country || "";
      birthplace = [city, state, country].filter(Boolean).join(", ");
    }

    var output = {
      playerId: playerId_str,
      displayName: json.displayName || "",
      dateOfBirth: dob,
      birthplace: birthplace,
      found: true
    };

    cache.put(cacheKey, JSON.stringify(output), 21600); // 6 hours
    ESPN_MEMO.athletes[cacheKey] = output;

    return output;
  } catch (e) {
    return { error: "Fetch exception: " + e.toString(), found: false };
  }
}
