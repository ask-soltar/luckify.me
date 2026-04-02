/****************************************************
 * 07d_fetcher_wikidata.gs
 * LUCKIFY ME — Wikidata Birthday Fetcher
 *
 * Uses Wikidata API to look up player birthdates.
 * Returns birth date in YYYY-MM-DD format.
 * Caching layer prevents duplicate lookups.
 ****************************************************/

var WIKIDATA_MEMO = {
  birthdays: {}  // Cache by player name
};

/**
 * WIKIDATA_FETCH_BIRTHDAY_(playerName)
 * Searches Wikidata for a player and extracts birth date (P569) + birthplace (P19).
 * Returns: { dateOfBirth, birthplace, found, displayName }
 */
function WIKIDATA_FETCH_BIRTHDAY_(playerName) {
  if (!playerName) {
    return { error: "No player name", found: false };
  }

  var nameKey = String(playerName).trim();
  var cacheKey = "wikidata_full_" + nameKey;

  // In-memory memo check
  if (WIKIDATA_MEMO.birthdays[cacheKey]) {
    return WIKIDATA_MEMO.birthdays[cacheKey];
  }

  // Apps Script cache check (persists 6 hours)
  var cache = CacheService.getScriptCache();
  var cached = cache.get(cacheKey);
  if (cached) {
    var parsed = JSON.parse(cached);
    WIKIDATA_MEMO.birthdays[cacheKey] = parsed;
    return parsed;
  }

  // Search for entity
  var searchUrl = "https://www.wikidata.org/w/api.php?" +
    "action=wbsearchentities&search=" + encodeURIComponent(nameKey) +
    "&type=item&language=en&format=json";

  try {
    var searchResponse = UrlFetchApp.fetch(searchUrl, {
      muteHttpExceptions: true,
      headers: { "User-Agent": "Luckify-Me/1.0" }
    });

    if (searchResponse.getResponseCode() !== 200) {
      return { error: "Search failed", found: false };
    }

    var searchData = JSON.parse(searchResponse.getContentText());
    if (!searchData.search || !searchData.search.length) {
      var notFoundOutput = {
        playerName: nameKey,
        error: "Not found on Wikidata",
        found: false
      };
      cache.put(cacheKey, JSON.stringify(notFoundOutput), 21600); // 6 hours
      return notFoundOutput;
    }

    // Get first result's entity ID
    var entityId = searchData.search[0].id;
    var displayName = searchData.search[0].label || nameKey;

    // Fetch entity details
    var entityUrl = "https://www.wikidata.org/wiki/Special:EntityData/" + entityId + ".json";
    var entityResponse = UrlFetchApp.fetch(entityUrl, {
      muteHttpExceptions: true,
      headers: { "User-Agent": "Luckify-Me/1.0" }
    });

    if (entityResponse.getResponseCode() !== 200) {
      return { error: "Entity fetch failed", found: false };
    }

    var entityData = JSON.parse(entityResponse.getContentText());
    var entity = entityData.entities[entityId];

    if (!entity || !entity.claims || !entity.claims.P569) {
      var noBdayOutput = {
        playerName: nameKey,
        displayName: displayName,
        error: "No birth date on Wikidata",
        found: false
      };
      cache.put(cacheKey, JSON.stringify(noBdayOutput), 21600);
      return noBdayOutput;
    }

    // Extract birth date
    var bdayFormatted = "";
    if (entity.claims.P569 && entity.claims.P569.length > 0) {
      var bdayClaim = entity.claims.P569[0];
      var bdayValue = bdayClaim.mainsnak.datavalue.value.time;
      bdayFormatted = bdayValue.substring(1, 11); // Extract YYYY-MM-DD from +YYYY-MM-DDTHH:MM:SSZ
    }

    // Extract birthplace (P19) — get the actual place name, not entity ID
    var birthplaceStr = "";
    if (entity.claims.P19 && entity.claims.P19.length > 0) {
      var birthplaceClaim = entity.claims.P19[0];
      var birthplaceEntityId = birthplaceClaim.mainsnak.datavalue.value.id;

      // Fetch the birthplace entity to get its label
      try {
        var bpEntityUrl = "https://www.wikidata.org/wiki/Special:EntityData/" + birthplaceEntityId + ".json";
        var bpResponse = UrlFetchApp.fetch(bpEntityUrl, {
          muteHttpExceptions: true,
          headers: { "User-Agent": "Luckify-Me/1.0" }
        });

        if (bpResponse.getResponseCode() === 200) {
          var bpEntityData = JSON.parse(bpResponse.getContentText());
          var bpEntity = bpEntityData.entities[birthplaceEntityId];
          if (bpEntity && bpEntity.labels && bpEntity.labels.en) {
            birthplaceStr = bpEntity.labels.en.value;
          }
        }
      } catch (e) {
        // Fallback to entity ID if fetch fails
        birthplaceStr = birthplaceEntityId;
      }
    }

    var output = {
      playerName: nameKey,
      displayName: displayName,
      dateOfBirth: bdayFormatted,
      birthplace: birthplaceStr,
      found: (bdayFormatted || birthplaceStr ? true : false)
    };

    cache.put(cacheKey, JSON.stringify(output), 21600); // 6 hours
    WIKIDATA_MEMO.birthdays[cacheKey] = output;

    return output;
  } catch (e) {
    return { error: "Fetch exception: " + e.toString(), found: false };
  }
}
