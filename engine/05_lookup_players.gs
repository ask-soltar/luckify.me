/****************************************************
 * 05_lookup_players.gs
 * LUCKIFY ME — Player Data Access Layer
 *
 * RULE: Reads from the PLAYERS (Birthday) sheet only.
 *       Returns player objects. No engine logic.
 *
 * All players are cached on first read (within a single script run)
 * to avoid repeated sheet access.
 ****************************************************/

let _PLAYERS_CACHE = null;

/**
 * _loadAllPlayers_()
 * Internal helper. Reads PLAYERS sheet once and caches in memory.
 * Returns array of player objects.
 */
function _loadAllPlayers_() {
  if (_PLAYERS_CACHE !== null) {
    return _PLAYERS_CACHE;
  }

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(PLAYERS.SHEET);

  if (!sheet) {
    console.error("PLAYERS sheet '" + PLAYERS.SHEET + "' not found");
    return [];
  }

  const lastRow = sheet.getLastRow();
  if (lastRow < PLAYERS.START_ROW) {
    _PLAYERS_CACHE = [];
    return _PLAYERS_CACHE;
  }

  const numRows = lastRow - PLAYERS.START_ROW + 1;
  const range = sheet.getRange(PLAYERS.START_ROW, 1, numRows, 16); // A through P
  const values = range.getValues();

  const players = [];
  for (let i = 0; i < values.length; i++) {
    const row = values[i];
    const player = {
      player_id:     row[PLAYERS.COL_PLAYER_ID - 1],
      name:          row[PLAYERS.COL_NAME - 1],
      birthday:      row[PLAYERS.COL_BIRTHDAY - 1],
      birthplace:    row[PLAYERS.COL_BIRTHPLACE - 1],
      gmt:           row[PLAYERS.COL_GMT - 1],
      human_check:   row[PLAYERS.COL_HUMAN_CHECK - 1],
      element:       row[PLAYERS.COL_ELEMENT - 1],
      horoscope:     row[PLAYERS.COL_HOROSCOPE - 1],
      horo_bucket:   row[PLAYERS.COL_HORO_BUCKET - 1],
      first_red:     row[PLAYERS.COL_FIRST_RED - 1],
      pers_card:     row[PLAYERS.COL_PERS_CARD - 1],
      soul_card:     row[PLAYERS.COL_SOUL_CARD - 1],
      bc_pattern:    row[PLAYERS.COL_BC_PATTERN - 1],
      numer_bucket:  row[PLAYERS.COL_NUMER_BUCKET - 1],
      tithi_num:     row[PLAYERS.COL_TITHI_NUM - 1],
      tithi_type:    row[PLAYERS.COL_TITHI_TYPE - 1]
    };
    players.push(player);
  }

  _PLAYERS_CACHE = players;
  return players;
}

/**
 * getPlayerById(player_id)
 * Returns the player object with the given player_id (PLY_XXXX).
 * Returns null if not found.
 */
function getPlayerById(player_id) {
  const players = _loadAllPlayers_();
  for (const p of players) {
    if (p.player_id === player_id) {
      return p;
    }
  }
  return null;
}

/**
 * getPlayerByName(name)
 * Returns the first player with the given name (case-sensitive).
 * Returns null if not found.
 */
function getPlayerByName(name) {
  const players = _loadAllPlayers_();
  for (const p of players) {
    if (p.name === name) {
      return p;
    }
  }
  return null;
}

/**
 * getAllPlayers()
 * Returns array of all player objects.
 */
function getAllPlayers() {
  return _loadAllPlayers_();
}

/**
 * clearPlayerCache_()
 * Clears the in-memory cache. Useful if you modify the PLAYERS sheet
 * during a script run and need fresh data.
 */
function clearPlayerCache_() {
  _PLAYERS_CACHE = null;
}
