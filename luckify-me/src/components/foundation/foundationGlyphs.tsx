import type { ReactNode, SVGProps } from 'react';

import {
  getFoundationGlyphKey,
} from '../../lib/foundation/foundationGlyphRegistry';
import type {
  FoundationGlyphKey,
  FoundationGlyphMode as GlyphMode,
  GlyphProps,
} from '../../lib/foundation/foundationGlyphTypes';

type BaseProps = GlyphProps & {
  children: ReactNode
  viewBox?: string
}

function glyphModeStyle(mode: GlyphMode, animated?: boolean): SVGProps<SVGSVGElement>['style'] {
  if (mode === 'operator') {
    return {
      color: '#9EFF7A',
      filter: animated ? 'drop-shadow(0 0 6px rgba(158, 255, 122, 0.24))' : undefined,
    };
  }

  return {
    color: '#D8E9DA',
    filter: animated ? 'drop-shadow(0 0 8px rgba(168, 232, 188, 0.18))' : undefined,
  };
}

function GlyphBase({
  mode = 'human',
  size = 24,
  title,
  className,
  animated,
  children,
  viewBox = '0 0 24 24',
}: BaseProps) {
  const labelled = Boolean(title)

  return (
    <svg
      viewBox={viewBox}
      width={size}
      height={size}
      role={labelled ? 'img' : 'presentation'}
      aria-hidden={labelled ? undefined : true}
      aria-label={labelled ? title : undefined}
      className={className}
      style={glyphModeStyle(mode, animated)}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {children}
    </svg>
  )
}

function glyphStroke(mode: GlyphMode, strokeWidth?: number) {
  return {
    stroke: 'currentColor',
    strokeWidth: strokeWidth ?? (mode === 'operator' ? 1.35 : 1.5),
    strokeLinecap: mode === 'operator' ? 'square' : 'round',
    strokeLinejoin: mode === 'operator' ? 'miter' : 'round',
    vectorEffect: 'non-scaling-stroke' as const,
  }
}

export function GlyphThePioneer({ mode = 'human', size = 24, title = 'The Pioneer', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 17L12 7L17 17" /></g>
      <g id="axis" {...s}><path d="M12 17V20" /></g>
      <g id="core" {...s}><path d="M10 13.5L12 11.5L14 13.5" /></g>
      <g id="support" {...s}><path d="M9 17H15" /></g>
      <g id="energy" {...s}><path d="M12 5V4" /></g>
    </GlyphBase>
  )
}

export function GlyphTheCatalyst({ mode = 'human', size = 24, title = 'The Catalyst', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7.5 17L12 6.8L16.5 17" /></g>
      <g id="axis" {...s}><path d="M12 16.8V19.2" /></g>
      <g id="core" {...s}><path d="M9.8 13.2L12 10.2L14.2 13.2" /></g>
      <g id="support" {...s}><path d="M8.6 16.9H15.4" /></g>
      <g id="energy" {...s}><path d="M12 4.2V3" /><path d="M9.1 7.2L8.2 6.1" /><path d="M14.9 7.2L15.8 6.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheFoundationStarter({ mode = 'human', size = 24, title = 'The Foundation Starter', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><rect x="6" y="7" width="12" height="9" rx="1.5" /></g>
      <g id="axis" {...s}><path d="M12 7V16" /></g>
      <g id="core" {...s}><path d="M9 12H15" /></g>
      <g id="support" {...s}><path d="M7.5 18.5H16.5" /><path d="M9 20H15" /></g>
      <g id="energy" {...s}><path d="M11 5.2H13" /></g>
    </GlyphBase>
  )
}

export function GlyphTheStrategist({ mode = 'human', size = 24, title = 'The Strategist', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 4.5L18 10L12 19.5L6 10L12 4.5Z" /></g>
      <g id="axis" {...s}><path d="M9 13L15 7" /></g>
      <g id="core" {...s}><path d="M10 10H14" /><path d="M12 8V12" /></g>
      <g id="support" {...s}><path d="M9.8 16H14.2" /></g>
      <g id="energy" {...s}><path d="M16.2 8.2H18" /></g>
    </GlyphBase>
  )
}

export function GlyphTheTimingKeeper({ mode = 'human', size = 24, title = 'The Timing Keeper', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="11" r="6.25" /></g>
      <g id="axis" {...s}><path d="M12 11L15.4 8.6" /></g>
      <g id="core" {...s}><circle cx="12" cy="11" r="1.35" /></g>
      <g id="support" {...s}><path d="M6 11H7.4" /><path d="M12 4.9V6.3" /><path d="M17.6 11H19" /><path d="M12 15.7V17.1" /></g>
      <g id="energy" {...s}><path d="M8.8 18.1C10.1 18.9 11.2 19.3 12 19.3C12.8 19.3 13.9 18.9 15.2 18.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheCultivator({ mode = 'human', size = 24, title = 'The Cultivator', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 15.25C7 11.9 9.1 9.5 12 9.5C14.9 9.5 17 11.9 17 15.25" /></g>
      <g id="axis" {...s}><path d="M12 6.8V9" /></g>
      <g id="core" {...s}><circle cx="12" cy="6.2" r="1.4" /></g>
      <g id="support" {...s}><path d="M8.6 17.2C9.7 16.1 10.8 15.55 12 15.55C13.2 15.55 14.3 16.1 15.4 17.2" /><path d="M9.25 19.25H14.75" /></g>
      <g id="energy" {...s}><path d="M6.4 12.75L7.3 12.4" /><path d="M17.6 12.75L16.7 12.4" /></g>
    </GlyphBase>
  )
}

export function GlyphTheStabilizer({ mode = 'human', size = 24, title = 'The Stabilizer', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><rect x="5.5" y="5" width="13" height="14" rx="2" /></g>
      <g id="axis" {...s}><path d="M12 7.5V16.5" /></g>
      <g id="core" {...s}><path d="M8.5 12H15.5" /></g>
      <g id="support" {...s}><path d="M8 19H16" /><path d="M7.5 8H5.5" /><path d="M18.5 8H16.5" /></g>
      <g id="energy" {...s}><path d="M8.75 9.25L10 10.5" /><path d="M15.25 9.25L14 10.5" /></g>
    </GlyphBase>
  )
}

export function GlyphTheSteward({ mode = 'human', size = 24, title = 'The Steward', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 15.5C7 12.2 9.05 9.75 12 9.75C14.95 9.75 17 12.2 17 15.5" /></g>
      <g id="axis" {...s}><path d="M12 8.25V10" /></g>
      <g id="core" {...s}><circle cx="12" cy="8" r="1.5" /></g>
      <g id="support" {...s}><path d="M8.25 17.5H15.75" /><path d="M9.5 19.5H14.5" /></g>
      <g id="energy" {...s}><path d="M6.2 13.4L7.2 13.1" /><path d="M17.8 13.4L16.8 13.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheArchitect({ mode = 'human', size = 24, title = 'The Architect', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><rect x="5" y="4.5" width="14" height="15" rx="1.75" /></g>
      <g id="axis" {...s}><path d="M12 6.75V17.25" /></g>
      <g id="core" {...s}><path d="M8.25 9.5H15.75" /><path d="M8.25 14.5H15.75" /></g>
      <g id="support" {...s}><path d="M9 19.5H15" /><path d="M9 7L7.75 8.25" /><path d="M15 7L16.25 8.25" /></g>
      <g id="energy" {...s}><path d="M6.25 12H7.5" /><path d="M16.5 12H17.75" /></g>
    </GlyphBase>
  )
}

export function GlyphTheWiseGuardian({ mode = 'human', size = 24, title = 'The Wise Guardian', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 14.5C7 10.8 9.15 8.5 12 8.5C14.85 8.5 17 10.8 17 14.5V15.2C17 17.2 15.1 18.7 12 19.6C8.9 18.7 7 17.2 7 15.2V14.5Z" /></g>
      <g id="axis" {...s}><path d="M12 6V8.2" /></g>
      <g id="core" {...s}><circle cx="12" cy="5.2" r="1.35" /></g>
      <g id="support" {...s}><path d="M9.25 12.25C10.15 11.4 11.05 11 12 11C12.95 11 13.85 11.4 14.75 12.25" /></g>
      <g id="energy" {...s}><path d="M8 8.8C8.8 8.2 9.6 7.9 10.4 7.9" /><path d="M16 8.8C15.2 8.2 14.4 7.9 13.6 7.9" /></g>
    </GlyphBase>
  )
}

export function GlyphTheChallenger({ mode = 'human', size = 24, title = 'The Challenger', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 17L12 7L17 17" /></g>
      <g id="axis" {...s}><path d="M10.2 17L13.8 7" /></g>
      <g id="core" {...s}><path d="M9.2 13.8L14.8 13.8" /></g>
      <g id="support" {...s}><path d="M8.8 17H15.2" /></g>
      <g id="energy" {...s}><path d="M12 5.5V4.2" /></g>
    </GlyphBase>
  )
}

export function GlyphTheForge({ mode = 'human', size = 24, title = 'The Forge', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 5L17.5 10.5L12 19L6.5 10.5L12 5Z" /></g>
      <g id="axis" {...s}><path d="M12 9V15.8" /></g>
      <g id="core" {...s}><path d="M9.4 11.5C10.05 10.3 10.95 9.7 12 9.7C13.05 9.7 13.95 10.3 14.6 11.5" /></g>
      <g id="support" {...s}><path d="M8.8 16.4H15.2" /></g>
      <g id="energy" {...s}><path d="M15 7.4L16.1 6.3" /><path d="M9 7.4L7.9 6.3" /></g>
    </GlyphBase>
  )
}

export function GlyphTheStronghold({ mode = 'human', size = 24, title = 'The Stronghold', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><rect x="5" y="5" width="14" height="13" rx="1.75" /></g>
      <g id="axis" {...s}><path d="M9 8.25V14.75" /><path d="M15 8.25V14.75" /></g>
      <g id="core" {...s}><path d="M9 11.5H15" /></g>
      <g id="support" {...s}><path d="M7.5 18H16.5" /><path d="M9 20H15" /></g>
      <g id="energy" {...s}><path d="M6.75 8.5H8" /><path d="M16 8.5H17.25" /></g>
    </GlyphBase>
  )
}

export function GlyphTheMaster({ mode = 'human', size = 24, title = 'The Master', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 4.5L18 10L12 19.5L6 10L12 4.5Z" /></g>
      <g id="axis" {...s}><path d="M12 7.5V16.5" /><path d="M8.5 10H15.5" /></g>
      <g id="core" {...s}><circle cx="12" cy="10" r="1.4" /></g>
      <g id="support" {...s}><path d="M10.1 15.6H13.9" /></g>
      <g id="energy" {...s}><path d="M15.8 7.1L16.9 6" /></g>
    </GlyphBase>
  )
}

export function GlyphTheResilientSage({ mode = 'human', size = 24, title = 'The Resilient Sage', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="10.5" r="6.25" /></g>
      <g id="axis" {...s}><path d="M12 4.25V5.7" /></g>
      <g id="core" {...s}><circle cx="12" cy="10.5" r="1.4" /></g>
      <g id="support" {...s}><path d="M9.1 14.65C10.05 16.4 11.4 17.4 13.1 17.55C14.25 17.65 15.3 17.3 16.15 16.55" /><path d="M8.6 19.2C10 20 11.15 20.4 12 20.4C12.85 20.4 14 20 15.4 19.2" /></g>
      <g id="energy" {...s}><path d="M8.2 5.2L9.1 6.1" /><path d="M15.8 5.2L14.9 6.1" /></g>
    </GlyphBase>
  )
}

export function GlyphThePruner({ mode = 'human', size = 24, title = 'The Pruner', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M7 17L17 7" /></g>
      <g id="axis" {...s}><path d="M8.75 8.75L15.25 15.25" /></g>
      <g id="core" {...s}><path d="M10.5 17H7V13.5" /></g>
      <g id="support" {...s}><path d="M13.5 7H17V10.5" /></g>
      <g id="energy" {...s}><path d="M5.5 18.5L7 17" /></g>
    </GlyphBase>
  )
}

export function GlyphTheStructuralReformer({ mode = 'human', size = 24, title = 'The Structural Reformer', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><rect x="5" y="4" width="14" height="16" rx="2" /></g>
      <g id="axis" {...s}><path d="M12 7V17" /></g>
      <g id="core" {...s}><path d="M8.5 14.5H12" /><path d="M12 10.5H15.5" /></g>
      <g id="support" {...s}><path d="M8 20H16" /></g>
      <g id="energy" {...s}><path d="M6.5 8.5L8 7" /></g>
    </GlyphBase>
  )
}

export function GlyphTheGroundedSeer({ mode = 'human', size = 24, title = 'The Grounded Seer', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="10.5" r="5.75" /></g>
      <g id="axis" {...s}><path d="M12 6.8V14.2" /><path d="M8.3 10.5H15.7" /></g>
      <g id="core" {...s}><circle cx="12" cy="10.5" r="1.3" /></g>
      <g id="support" {...s}><path d="M8 17H16" /><path d="M9.5 19H14.5" /></g>
      <g id="energy" {...s}><path d="M6.7 6.8L7.8 7.6" /><path d="M17.3 6.8L16.2 7.6" /></g>
    </GlyphBase>
  )
}

export function GlyphTheRefiner({ mode = 'human', size = 24, title = 'The Refiner', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 4L18 10L12 20L6 10L12 4Z" /></g>
      <g id="axis" {...s}><path d="M12 7V17" /></g>
      <g id="core" {...s}><path d="M9.5 12H14.5" /></g>
      <g id="support" {...s}><path d="M10 18.2L12 16.8L14 18.2" /></g>
      <g id="energy" {...s}><path d="M15.2 8.2L16.4 7" /></g>
    </GlyphBase>
  )
}

export function GlyphTheDeepSeer({ mode = 'human', size = 24, title = 'The Deep Seer', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="11" r="6.5" /></g>
      <g id="axis" {...s}><path d="M5 11H7" /><path d="M17 11H19" /></g>
      <g id="core" {...s}><circle cx="12" cy="11" r="1.5" /></g>
      <g id="support" {...s}><path d="M9.25 15.25C10.15 17.1 11.55 18.15 13.35 18.4C14.55 18.55 15.65 18.3 16.55 17.7" /></g>
      <g id="energy" {...s}><path d="M12 4V5.5" /><path d="M8.2 5.2L9.1 6.1" /><path d="M15.8 5.2L14.9 6.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheHarvester({ mode = 'human', size = 24, title = 'The Harvester', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M6.5 13.5C8.1 10.2 10.05 8.6 12 8.6C13.95 8.6 15.9 10.2 17.5 13.5" /></g>
      <g id="axis" {...s}><path d="M12 8.6V17.4" /></g>
      <g id="core" {...s}><circle cx="12" cy="13.3" r="1.35" /></g>
      <g id="support" {...s}><path d="M8.25 16.8C9.5 18 10.75 18.6 12 18.6C13.25 18.6 14.5 18 15.75 16.8" /></g>
      <g id="energy" {...s}><path d="M8.1 10.3L7.2 9.2" /><path d="M15.9 10.3L16.8 9.2" /></g>
    </GlyphBase>
  )
}

export function GlyphTheIlluminator({ mode = 'human', size = 24, title = 'The Illuminator', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="11.5" r="5.5" /></g>
      <g id="axis" {...s}><path d="M12 4.2V6" /><path d="M12 17V18.8" /><path d="M4.7 11.5H6.5" /><path d="M17.5 11.5H19.3" /></g>
      <g id="core" {...s}><circle cx="12" cy="11.5" r="1.35" /></g>
      <g id="support" {...s}><path d="M8.1 7.6L9.3 8.8" /><path d="M15.9 7.6L14.7 8.8" /><path d="M8.1 15.4L9.3 14.2" /><path d="M15.9 15.4L14.7 14.2" /></g>
      <g id="energy" {...s}><path d="M12 2.8V3.6" /></g>
    </GlyphBase>
  )
}

export function GlyphTheIntegrator({ mode = 'human', size = 24, title = 'The Integrator', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M8 9.5C8.9 8.2 10.25 7.5 12 7.5C13.75 7.5 15.1 8.2 16 9.5" /><path d="M8 14.5C8.9 15.8 10.25 16.5 12 16.5C13.75 16.5 15.1 15.8 16 14.5" /></g>
      <g id="axis" {...s}><path d="M12 7.5V18" /></g>
      <g id="core" {...s}><circle cx="12" cy="12" r="1.35" /></g>
      <g id="support" {...s}><path d="M8.5 18.5H15.5" /><path d="M9.75 20H14.25" /></g>
      <g id="energy" {...s}><path d="M6.9 12H8" /><path d="M16 12H17.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheFinisher({ mode = 'human', size = 24, title = 'The Finisher', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 4.5L17.5 10L12 19.5L6.5 10L12 4.5Z" /></g>
      <g id="axis" {...s}><path d="M12 7.3V16.7" /></g>
      <g id="core" {...s}><circle cx="12" cy="12" r="1.25" /></g>
      <g id="support" {...s}><path d="M9.2 16.2C10.05 16.9 10.95 17.25 12 17.25C13.05 17.25 13.95 16.9 14.8 16.2" /><path d="M9.6 8.3H14.4" /></g>
      <g id="energy" {...s}><path d="M15.9 7L16.8 6.1" /></g>
    </GlyphBase>
  )
}

export function GlyphTheWisdomKeeper({ mode = 'human', size = 24, title = 'The Wisdom Keeper', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth)
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><circle cx="12" cy="10.75" r="6" /></g>
      <g id="axis" {...s}><path d="M12 4.75V6.1" /></g>
      <g id="core" {...s}><circle cx="12" cy="10.75" r="1.35" /></g>
      <g id="support" {...s}><path d="M8.95 14.8C10.05 16.5 11.45 17.25 13.05 17.2C14.2 17.15 15.2 16.7 16.05 15.85" /><path d="M9 18.8H15" /></g>
      <g id="energy" {...s}><path d="M16.2 6.4C15.5 5.85 14.8 5.45 14.1 5.25" /><path d="M8.2 19.9L9.3 18.8" /></g>
    </GlyphBase>
  )
}

export function GlyphFallback({ mode = 'human', size = 24, title = 'Foundation Glyph', className, strokeWidth }: GlyphProps) {
  const s = glyphStroke(mode, strokeWidth);
  return (
    <GlyphBase mode={mode} size={size} title={title} className={className}>
      <g id="frame" {...s}><path d="M12 4.5L18.5 11L12 19.5L5.5 11L12 4.5Z" /></g>
      <g id="axis" {...s}><path d="M12 7V15" /></g>
      <g id="core" {...s}><circle cx="12" cy="11" r="1.35" /></g>
      <g id="support" {...s}><path d="M9 17H15" /></g>
    </GlyphBase>
  );
}

export const glyphRegistry = {
  'the-pioneer': GlyphThePioneer,
  'the-catalyst': GlyphTheCatalyst,
  'the-foundation-starter': GlyphTheFoundationStarter,
  'the-strategist': GlyphTheStrategist,
  'the-timing-keeper': GlyphTheTimingKeeper,
  'the-cultivator': GlyphTheCultivator,
  'the-stabilizer': GlyphTheStabilizer,
  'the-steward': GlyphTheSteward,
  'the-architect': GlyphTheArchitect,
  'the-wise-guardian': GlyphTheWiseGuardian,
  'the-challenger': GlyphTheChallenger,
  'the-forge': GlyphTheForge,
  'the-stronghold': GlyphTheStronghold,
  'the-master': GlyphTheMaster,
  'the-resilient-sage': GlyphTheResilientSage,
  'the-pruner': GlyphThePruner,
  'the-structural-reformer': GlyphTheStructuralReformer,
  'the-grounded-seer': GlyphTheGroundedSeer,
  'the-refiner': GlyphTheRefiner,
  'the-deep-seer': GlyphTheDeepSeer,
  'the-harvester': GlyphTheHarvester,
  'the-illuminator': GlyphTheIlluminator,
  'the-integrator': GlyphTheIntegrator,
  'the-finisher': GlyphTheFinisher,
  'the-wisdom-keeper': GlyphTheWisdomKeeper,
} as const;

export function FoundationGlyph({
  glyph,
  mode = 'human',
  size = 24,
  title,
  className,
  animated,
  strokeWidth,
}: GlyphProps & { glyph?: FoundationGlyphKey | string | null }) {
  const resolvedGlyph = getFoundationGlyphKey(glyph);
  const Component = resolvedGlyph ? glyphRegistry[resolvedGlyph] : GlyphFallback;
  const safeTitle = title
    || (resolvedGlyph ? glyph.replace(/-/g, ' ') : 'Foundation glyph');

  return (
    <span
      className={className}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        lineHeight: 0,
        filter: animated
          ? (mode === 'operator'
              ? 'drop-shadow(0 0 8px rgba(158, 255, 122, 0.22))'
              : 'drop-shadow(0 0 10px rgba(168, 232, 188, 0.16))')
          : undefined,
      }}
    >
      <Component
        mode={mode}
        size={size}
        title={safeTitle}
        strokeWidth={strokeWidth}
        animated={animated}
      />
    </span>
  );
}
