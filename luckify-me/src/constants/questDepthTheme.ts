const QUEST_THEME_GLOBALS = {
  shellBorder: 'rgba(124, 130, 176, 0.11)',
  shellInset: 'rgba(255, 255, 255, 0.028)',
  shellShadow: 'rgba(0, 0, 0, 0.46)',
  backgroundTopGlow: 'rgba(96, 84, 184, 0.18)',
  backgroundTopGlowSoft: 'rgba(86, 96, 178, 0.12)',
  backgroundMidGlow: 'rgba(66, 90, 132, 0.06)',
  backgroundGroundGlow: 'rgba(116, 84, 58, 0.045)',
  backgroundTopHazeOpacity: '0.82',
  backgroundMidHazeOpacity: '0.5',
  backgroundGroundOpacity: '0.56',
  backgroundBase:
    'linear-gradient(180deg, rgba(4, 7, 15, 0.982) 0%, rgba(5, 8, 16, 0.989) 26%, rgba(7, 10, 14, 0.994) 58%, rgba(9, 10, 11, 0.997) 100%)',
  starColor: 'rgba(246, 248, 255, 0.5)',
  starOpacity: '0.24',
  starFieldPrimaryScale: '380px 240px',
  starFieldSecondaryScale: '460px 280px',
  atmosphereLine: 'rgba(150, 160, 220, 0.04)',
  geometryLine: 'rgba(156, 166, 226, 0.05)',
  geometryOpacity: '0.28',
  grainOpacity: '0.02',
  heroAuraOpacity: '0.22',
  heroMotifOpacity: '0.82',
  heroBorderStrength: 'rgba(160, 150, 248, 0.4)',
  heroMotionDuration: '18s',
  heroPulseDuration: '8.5s',
  motionLiftDistance: '1px',
  earthSilhouette: 'rgba(8, 10, 11, 0.98)',
};

export const QUEST_DEPTH_TOKENS = {
  0: {
    borderColor: 'rgba(144, 132, 236, 0.28)',
    glowColor: 'rgba(118, 100, 208, 0.18)',
    textAccentColor: 'rgba(228, 224, 248, 0.92)',
    panelTint:
      'linear-gradient(180deg, rgba(18, 21, 34, 0.88) 0%, rgba(11, 13, 20, 0.72) 100%)',
    iconTint: 'rgba(194, 186, 238, 0.82)',
  },
  1: {
    borderColor: 'rgba(120, 130, 214, 0.2)',
    glowColor: 'rgba(94, 104, 192, 0.11)',
    textAccentColor: 'rgba(204, 212, 242, 0.86)',
    panelTint:
      'linear-gradient(180deg, rgba(15, 18, 28, 0.86) 0%, rgba(10, 12, 18, 0.7) 100%)',
    iconTint: 'rgba(170, 182, 228, 0.76)',
  },
  2: {
    borderColor: 'rgba(102, 122, 184, 0.16)',
    glowColor: 'rgba(80, 98, 162, 0.07)',
    textAccentColor: 'rgba(192, 204, 230, 0.8)',
    panelTint:
      'linear-gradient(180deg, rgba(13, 17, 26, 0.86) 0%, rgba(9, 11, 16, 0.74) 100%)',
    iconTint: 'rgba(158, 178, 216, 0.72)',
  },
  3: {
    borderColor: 'rgba(102, 126, 150, 0.14)',
    glowColor: 'rgba(82, 108, 136, 0.06)',
    textAccentColor: 'rgba(188, 200, 212, 0.76)',
    panelTint:
      'linear-gradient(180deg, rgba(13, 16, 21, 0.86) 0%, rgba(9, 11, 14, 0.74) 100%)',
    iconTint: 'rgba(154, 170, 186, 0.68)',
  },
  4: {
    borderColor: 'rgba(146, 126, 104, 0.15)',
    glowColor: 'rgba(126, 100, 72, 0.05)',
    textAccentColor: 'rgba(214, 194, 172, 0.76)',
    panelTint:
      'linear-gradient(180deg, rgba(18, 15, 14, 0.86) 0%, rgba(11, 10, 10, 0.76) 100%)',
    iconTint: 'rgba(198, 176, 150, 0.68)',
  },
  5: {
    borderColor: 'rgba(176, 136, 108, 0.22)',
    glowColor: 'rgba(156, 102, 74, 0.1)',
    textAccentColor: 'rgba(236, 206, 184, 0.84)',
    panelTint:
      'linear-gradient(180deg, rgba(22, 16, 14, 0.9) 0%, rgba(12, 10, 10, 0.8) 100%)',
    iconTint: 'rgba(208, 168, 144, 0.72)',
  },
} as const;

function getDepthToken(depth = 0) {
  return QUEST_DEPTH_TOKENS[depth as keyof typeof QUEST_DEPTH_TOKENS] ?? QUEST_DEPTH_TOKENS[0];
}

export function getQuestThemeVars() {
  return {
    '--quest-shell-border': QUEST_THEME_GLOBALS.shellBorder,
    '--quest-shell-inset': QUEST_THEME_GLOBALS.shellInset,
    '--quest-shell-shadow': QUEST_THEME_GLOBALS.shellShadow,
    '--quest-bg-top-glow': QUEST_THEME_GLOBALS.backgroundTopGlow,
    '--quest-bg-top-glow-soft': QUEST_THEME_GLOBALS.backgroundTopGlowSoft,
    '--quest-bg-mid-glow': QUEST_THEME_GLOBALS.backgroundMidGlow,
    '--quest-bg-ground-glow': QUEST_THEME_GLOBALS.backgroundGroundGlow,
    '--quest-bg-top-haze-opacity': QUEST_THEME_GLOBALS.backgroundTopHazeOpacity,
    '--quest-bg-mid-haze-opacity': QUEST_THEME_GLOBALS.backgroundMidHazeOpacity,
    '--quest-bg-ground-opacity': QUEST_THEME_GLOBALS.backgroundGroundOpacity,
    '--quest-bg-base': QUEST_THEME_GLOBALS.backgroundBase,
    '--quest-bg-stars': QUEST_THEME_GLOBALS.starColor,
    '--quest-bg-stars-opacity': QUEST_THEME_GLOBALS.starOpacity,
    '--quest-bg-stars-scale-primary': QUEST_THEME_GLOBALS.starFieldPrimaryScale,
    '--quest-bg-stars-scale-secondary': QUEST_THEME_GLOBALS.starFieldSecondaryScale,
    '--quest-bg-line': QUEST_THEME_GLOBALS.atmosphereLine,
    '--quest-bg-geometry-line': QUEST_THEME_GLOBALS.geometryLine,
    '--quest-bg-geometry-opacity': QUEST_THEME_GLOBALS.geometryOpacity,
    '--quest-bg-grain-opacity': QUEST_THEME_GLOBALS.grainOpacity,
    '--quest-hero-aura-opacity': QUEST_THEME_GLOBALS.heroAuraOpacity,
    '--quest-hero-motif-opacity': QUEST_THEME_GLOBALS.heroMotifOpacity,
    '--quest-hero-border-strong': QUEST_THEME_GLOBALS.heroBorderStrength,
    '--quest-hero-motion-duration': QUEST_THEME_GLOBALS.heroMotionDuration,
    '--quest-hero-pulse-duration': QUEST_THEME_GLOBALS.heroPulseDuration,
    '--quest-motion-lift-distance': QUEST_THEME_GLOBALS.motionLiftDistance,
    '--quest-bg-earth': QUEST_THEME_GLOBALS.earthSilhouette,
  };
}

export function getQuestDepthVars(depth = 0) {
  const token = getDepthToken(depth);

  return {
    '--quest-depth-border': token.borderColor,
    '--quest-depth-glow': token.glowColor,
    '--quest-depth-accent': token.textAccentColor,
    '--quest-depth-panel': token.panelTint,
    '--quest-depth-icon': token.iconTint,
  };
}
