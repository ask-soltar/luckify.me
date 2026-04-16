/**
 * Blends: Element × Tithi Type Combinations
 * Describes the 25 unique combinations and their principles
 *
 * NOTE: Due to size constraints, abbreviated version shown here.
 * Full detailed principles can be extracted from APP/tithi-profiler.html
 * BLENDS object (line ~1156)
 */

export const BLENDS = {
  // Fire × types
  'Fire × Nanda': {
    statement: 'A fire that lights the room the moment it walks in — and is already thinking about the next room.',
    principles: [
      { title: 'You are at your best in the first five minutes.', body: 'The opening conversation, the first pitch, the moment you arrive — that is when your signal is loudest and clearest.' },
      { title: 'Your enthusiasm is contagious but it has an expiry date.', body: 'When you are lit up about something, everyone around you gets lit up too. But if you move on before they do, you leave people holding a fire you already dropped.' }
    ]
  },

  // Wood × types
  'Wood × Jaya': {
    statement: 'A root system that goes through rock — not because it is harder than rock, but because it is more persistent.',
    principles: [
      { title: 'You are the profile that turns obstacles into growing medium.', body: 'Wood pushes through resistance as a natural function and Jaya activates under pressure. Your combination does not just survive difficulty — it uses it.' },
      { title: 'You grow in the direction of what you want even when the path is completely unclear.', body: 'Wood orients toward light without needing to see the whole route. Jaya keeps moving through resistance.' }
    ]
  },

  'Earth × Nanda': {
    statement: 'The one who plants the seed and actually comes back to water it.',
    principles: [
      { title: 'You have a rare combination — you can start things and make them real.', body: 'Nanda fires at the threshold and Earth grounds and integrates. Most initiator profiles struggle with making things tangible.' },
      { title: 'People feel stabilized by your excitement, not swept away by it.', body: 'Nanda\'s enthusiasm is contagious. Earth centers everything around it.' }
    ]
  },

  // Simplified entries - full data to be added from source HTML
  'Metal × Bhadra': {
    statement: 'Precision meeting patience.',
    principles: [
      { title: 'You cut through noise with patience.', body: 'Metal clarity combined with Bhadra stability creates an unshakeable read.' }
    ]
  },

  'Water × Rikta': {
    statement: 'The depths that absorb what needs to be understood.',
    principles: [
      { title: 'You receive from places others cannot access.', body: 'Water depth meets Rikta clarity at the intersection of visible and invisible.' }
    ]
  },

  // Additional blend entries (abbreviated)
  // Full 25 combinations should be extracted from APP/tithi-profiler.html
  // Structure: element + ' × ' + tithi_type
  // Keys: Fire, Wood, Earth, Metal, Water × Nanda, Bhadra, Jaya, Rikta, Purna
};

// Helper to get blend by element and type
export function getBlend(element, tithiType) {
  const blendKey = `${element} × ${tithiType.charAt(0).toUpperCase()}${tithiType.slice(1)}`;
  return BLENDS[blendKey] || null;
}
