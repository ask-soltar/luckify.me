import type { LifePathCrestKey, LifePathCrestRegistryEntry } from './lifePathCrestTypes';
import { LIFE_PATH_CREST_KEYS } from './lifePathCrestTypes';

export const lifePathCrestRegistry: Record<LifePathCrestKey, LifePathCrestRegistryEntry> = {
  '1': {
    key: '1',
    number: 1,
    slug: 'life-path-1',
    operatorOutcomeName: 'Independent Initiation',
    humanOutcomeName: 'Growing Through Independent Initiation',
    componentName: 'LifePathCrestOne',
    archetype: 'initiator',
  },
  '2': {
    key: '2',
    number: 2,
    slug: 'life-path-2',
    operatorOutcomeName: 'Meaningful Connection',
    humanOutcomeName: 'Deepening Meaningful Connection',
    componentName: 'LifePathCrestTwo',
    archetype: 'bridge',
  },
  '3': {
    key: '3',
    number: 3,
    slug: 'life-path-3',
    operatorOutcomeName: 'Creative Transformation',
    humanOutcomeName: 'Living Creative Transformation',
    componentName: 'LifePathCrestThree',
    archetype: 'alchemist',
  },
  '4': {
    key: '4',
    number: 4,
    slug: 'life-path-4',
    operatorOutcomeName: 'Enduring Structures',
    humanOutcomeName: 'Building What Endures',
    componentName: 'LifePathCrestFour',
    archetype: 'builder',
  },
  '5': {
    key: '5',
    number: 5,
    slug: 'life-path-5',
    operatorOutcomeName: 'Adaptive Mastery',
    humanOutcomeName: 'Growing Into Adaptive Mastery',
    componentName: 'LifePathCrestFive',
    archetype: 'wanderer',
  },
  '6': {
    key: '6',
    number: 6,
    slug: 'life-path-6',
    operatorOutcomeName: 'Protective Responsibility',
    humanOutcomeName: 'Carrying What Matters Responsibly',
    componentName: 'LifePathCrestSix',
    archetype: 'guardian',
  },
  '7': {
    key: '7',
    number: 7,
    slug: 'life-path-7',
    operatorOutcomeName: 'Deep Understanding',
    humanOutcomeName: 'Growing Into Deep Understanding',
    componentName: 'LifePathCrestSeven',
    archetype: 'seer',
  },
  '8': {
    key: '8',
    number: 8,
    slug: 'life-path-8',
    operatorOutcomeName: 'Systemic Influence',
    humanOutcomeName: 'Creating Meaningful Systemic Influence',
    componentName: 'LifePathCrestEight',
    archetype: 'sovereign',
  },
  '9': {
    key: '9',
    number: 9,
    slug: 'life-path-9',
    operatorOutcomeName: 'Cyclical Integration',
    humanOutcomeName: 'Living Through Cyclical Integration',
    componentName: 'LifePathCrestNine',
    archetype: 'cycle',
  },
  '11': {
    key: '11',
    number: 11,
    slug: 'life-path-11',
    operatorOutcomeName: 'Visionary Insight',
    humanOutcomeName: 'Growing Into Visionary Insight',
    componentName: 'LifePathCrestEleven',
    archetype: 'oracle',
  },
  '22': {
    key: '22',
    number: 22,
    slug: 'life-path-22',
    operatorOutcomeName: 'Structural Innovation',
    humanOutcomeName: 'Creating Structural Innovation',
    componentName: 'LifePathCrestTwentyTwo',
    archetype: 'architect',
  },
  '33': {
    key: '33',
    number: 33,
    slug: 'life-path-33',
    operatorOutcomeName: 'Awakened Service',
    humanOutcomeName: 'Living Awakened Service',
    componentName: 'LifePathCrestThirtyThree',
    archetype: 'healer',
  },
};

const crestKeySet = new Set<string>(LIFE_PATH_CREST_KEYS);

export function isLifePathCrestKey(value: unknown): value is LifePathCrestKey {
  return typeof value === 'string' && crestKeySet.has(value);
}

export function getLifePathCrestKey(input?: string | number | null): LifePathCrestKey | null {
  if (input === null || input === undefined) return null;
  const normalized = String(input).trim();
  return isLifePathCrestKey(normalized) ? normalized : null;
}

export function resolveLifePathCrestKey(
  input?: string | number | null,
  fallback: LifePathCrestKey = '4',
): LifePathCrestKey {
  return getLifePathCrestKey(input) || fallback;
}
