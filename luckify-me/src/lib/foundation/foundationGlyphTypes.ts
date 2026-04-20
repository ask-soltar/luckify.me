export const FOUNDATION_GLYPH_KEYS = [
  'the-pioneer',
  'the-catalyst',
  'the-foundation-starter',
  'the-strategist',
  'the-timing-keeper',
  'the-cultivator',
  'the-stabilizer',
  'the-steward',
  'the-architect',
  'the-wise-guardian',
  'the-challenger',
  'the-forge',
  'the-stronghold',
  'the-master',
  'the-resilient-sage',
  'the-pruner',
  'the-structural-reformer',
  'the-grounded-seer',
  'the-refiner',
  'the-deep-seer',
  'the-harvester',
  'the-illuminator',
  'the-integrator',
  'the-finisher',
  'the-wisdom-keeper',
] as const;

export type FoundationGlyphKey = (typeof FOUNDATION_GLYPH_KEYS)[number];
export type FoundationGlyphMode = 'human' | 'operator';
export type FoundationDynamicGroup = 'nanda' | 'bhadra' | 'jaya' | 'rikta' | 'purna';

export type GlyphProps = {
  mode?: FoundationGlyphMode;
  size?: number | string;
  title?: string;
  className?: string;
  animated?: boolean;
  strokeWidth?: number;
};

export type FoundationGlyphRegistryEntry = {
  key: FoundationGlyphKey;
  slug: FoundationGlyphKey;
  dynamicName: string;
  group: FoundationDynamicGroup;
  assetName: string;
  componentName: string;
};
