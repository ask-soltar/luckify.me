/**
 * Zone scoring data — extracted from Project Soltar luckify-app.html
 * Used to render category score bars in the day detail sheet.
 */

export const CAT_EMOJI = {
  Action:     '⚡',
  Strategy:   '🧠',
  Discipline: '🔒',
  Social:     '🤝',
  Creativity: '✨',
  Risk:       '🎯',
};

// Raw category weights per zone
const BASE_WEIGHTS = {
  Orange: { Action:10, Strategy:8,  Discipline:8, Social:6, Creativity:6,  Risk:10 },
  Blue:   { Action:5,  Strategy:10, Discipline:4, Social:6, Creativity:8,  Risk:6  },
  Red:    { Action:9,  Strategy:5,  Discipline:3, Social:5, Creativity:4,  Risk:9  },
  Green:  { Action:6,  Strategy:6,  Discipline:9, Social:6, Creativity:5,  Risk:4  },
  Yellow: { Action:5,  Strategy:6,  Discipline:6, Social:9, Creativity:6,  Risk:5  },
  Purple: { Action:3,  Strategy:7,  Discipline:6, Social:4, Creativity:10, Risk:3  },
  Pink:   { Action:8,  Strategy:6,  Discipline:3, Social:7, Creativity:10, Risk:8  },
  Brown:  { Action:2,  Strategy:4,  Discipline:4, Social:3, Creativity:4,  Risk:2  },
};

// Multiplier that scales the overall energy level per zone
const MULT = {
  Orange:2.57, Blue:2.04, Red:2.25, Green:1.70,
  Yellow:0.75, Purple:0.50, Pink:1.50, Brown:1.00,
};

// One-line action guidance per category per zone
export const GUIDANCE = {
  Orange: { Action:'Move on it now',        Strategy:'Plan while moving',  Discipline:'Stay in structure',   Social:'Leverage your network',  Creativity:'Channel into output',   Risk:'Take the calculated bet' },
  Blue:   { Action:'Only what matters',     Strategy:'Deep work pays off', Discipline:'Follow the process',  Social:'Build key alliances',    Creativity:'Explore freely',         Risk:'Calculated exposure'     },
  Red:    { Action:'Controlled aggression', Strategy:'Adapt in real time', Discipline:'Hold your ground',   Social:'Keep your own counsel',  Creativity:'Improvise',              Risk:'Know your exit first'    },
  Green:  { Action:'Steady progress',       Strategy:'Long game thinking', Discipline:'This is your edge',  Social:'Strengthen foundations', Creativity:'Practice, not perform',  Risk:'Minimal today'           },
  Yellow: { Action:'Show up fully',         Strategy:'Build your plan',    Discipline:'Keep the routine',   Social:'Connection is the edge', Creativity:'Express naturally',      Risk:'Read the room'           },
  Purple: { Action:'Minimal action',        Strategy:'Reflect first',      Discipline:'Anchor to routine',  Social:'Limit exposure',         Creativity:'Inner work pays off',    Risk:'Not today'               },
  Pink:   { Action:'Seize the moment',      Strategy:'Bold moves work',    Discipline:'Channel the energy', Social:'Radiate, connect',       Creativity:'Full expression now',    Risk:'Size up when clear'      },
  Brown:  { Action:'One task only',         Strategy:'Simplify',           Discipline:'Maintain baseline',  Social:'Low bandwidth today',    Creativity:'Rest the mind',          Risk:'Preserve capital'        },
};

// Short tagline shown under zone name in day detail
export const CELL_LINE = {
  Orange: 'Make your move',
  Blue:   'Think it through',
  Red:    'Careful aggression',
  Green:  'Build the habit',
  Yellow: 'Show up present',
  Purple: 'Go inward',
  Pink:   'Full expression',
  Brown:  'Rest and reset',
};

/**
 * Returns category scores for a zone, sorted highest first.
 * Each entry: { cat, normalized } where normalized is 0–10.
 */
export function getZoneScores(zone) {
  const w = BASE_WEIGHTS[zone];
  const m = MULT[zone];
  if (!w || !m) return [];

  const raw = Object.entries(w)
    .map(([cat, wt]) => ({ cat, raw: wt * m }))
    .sort((a, b) => b.raw - a.raw);

  const zMax = raw[0].raw;
  return raw.map(r => ({
    cat: r.cat,
    normalized: Math.round((r.raw / zMax) * 100) / 10,
  }));
}
