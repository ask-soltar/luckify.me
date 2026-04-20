export const LIFE_PATH_CREST_KEYS = [
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '11',
  '22',
  '33',
] as const;

export type LifePathCrestKey = (typeof LIFE_PATH_CREST_KEYS)[number];
export type LifePathMode = 'human' | 'operator';

export type LifePathCrestProps = {
  mode?: LifePathMode;
  size?: number | string;
  title?: string;
  className?: string;
  animated?: boolean;
  strokeWidth?: number;
};

export type LifePathCrestRegistryEntry = {
  key: LifePathCrestKey;
  number: number;
  slug: `life-path-${LifePathCrestKey}`;
  operatorOutcomeName: string;
  humanOutcomeName: string;
  componentName: string;
  archetype: string;
};
