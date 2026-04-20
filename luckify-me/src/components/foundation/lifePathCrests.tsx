import type { ReactNode, SVGProps } from 'react';

import { getLifePathCrestKey } from '../../lib/foundation/lifePathCrestRegistry';
import type {
  LifePathCrestKey,
  LifePathCrestProps,
  LifePathMode,
} from '../../lib/foundation/lifePathCrestTypes';

type CrestBaseProps = LifePathCrestProps & {
  children: ReactNode;
  viewBox?: string;
};

function crestModeStyle(mode: LifePathMode, animated?: boolean): SVGProps<SVGSVGElement>['style'] {
  if (mode === 'operator') {
    return {
      color: '#9EFF7A',
      filter: animated ? 'drop-shadow(0 0 10px rgba(158, 255, 122, 0.2))' : undefined,
    };
  }

  return {
    color: '#E8F0E7',
    filter: animated ? 'drop-shadow(0 0 12px rgba(198, 232, 205, 0.14))' : undefined,
  };
}

function crestStroke(mode: LifePathMode, strokeWidth?: number) {
  return {
    stroke: 'currentColor',
    strokeWidth: strokeWidth ?? (mode === 'operator' ? 1.3 : 1.45),
    strokeLinecap: mode === 'operator' ? 'square' : 'round',
    strokeLinejoin: mode === 'operator' ? 'miter' : 'round',
    vectorEffect: 'non-scaling-stroke' as const,
  };
}

function CrestBase({
  mode = 'human',
  size = 96,
  title,
  className,
  animated,
  children,
  viewBox = '0 0 48 56',
}: CrestBaseProps) {
  const labelled = Boolean(title);

  return (
    <svg
      viewBox={viewBox}
      width={size}
      height={size}
      role={labelled ? 'img' : 'presentation'}
      aria-hidden={labelled ? undefined : true}
      aria-label={labelled ? title : undefined}
      className={className}
      style={crestModeStyle(mode, animated)}
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {children}
    </svg>
  );
}

function CrestShell({ mode = 'human', size = 96, title = 'Life Path Crest', className, animated, children }: CrestBaseProps) {
  const s = crestStroke(mode);
  return (
    <CrestBase mode={mode} size={size} title={title} className={className} animated={animated}>
      <g opacity={mode === 'operator' ? 0.18 : 0.16} {...s}>
        <path d="M24 4L41 11V28C41 39 34.5 47.5 24 52C13.5 47.5 7 39 7 28V11L24 4Z" />
      </g>
      <g opacity={mode === 'operator' ? 0.42 : 0.28} {...s}>
        <path d="M24 8L36.5 13V27.2C36.5 35.6 31.8 42.3 24 46.1C16.2 42.3 11.5 35.6 11.5 27.2V13L24 8Z" />
      </g>
      {children}
    </CrestBase>
  );
}

function LifePathCrestOne(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 1 Crest'}>
      <g {...s}>
        <path d="M24 16V37" />
        <path d="M18 22L24 16L30 22" />
        <path d="M16 42H32" />
        <path d="M24 10V13" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestTwo(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 2 Crest'}>
      <g {...s}>
        <path d="M16 29C18.2 23.8 20.9 21.2 24 21.2C27.1 21.2 29.8 23.8 32 29" />
        <path d="M15.5 35C18.2 38.4 21 40.1 24 40.1C27 40.1 29.8 38.4 32.5 35" />
        <path d="M24 15V18" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestThree(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 3 Crest'}>
      <g {...s}>
        <path d="M24 16C19.5 20.3 18.2 24.4 20 28.3C21.3 31.1 24.2 32.5 28.7 32.5" />
        <path d="M17 36C20 39.2 22.9 40.8 25.8 40.8C29.2 40.8 32.1 38.8 34.5 34.7" />
        <path d="M17.5 23.5L20.5 22.2" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestFour(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 4 Crest'}>
      <g {...s}>
        <path d="M16 20H32V37H16V20Z" />
        <path d="M24 20V37" />
        <path d="M16 28.5H32" />
        <path d="M18.5 42H29.5" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestFive(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 5 Crest'}>
      <g {...s}>
        <path d="M24 15C18.6 18.6 16.2 22.5 16.8 26.8C17.5 31.5 21.2 34 28 34.4" />
        <path d="M20 38.8C22.5 40.4 24.8 41.2 27 41.2C29.2 41.2 31.2 40.2 33 38.2" />
        <path d="M30 19.2L33.5 18" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestSix(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 6 Crest'}>
      <g {...s}>
        <path d="M16.5 30.2C16.5 23.7 19.3 20.2 24 18.4C28.7 20.2 31.5 23.7 31.5 30.2V31.6C31.5 35.9 29 39.2 24 41.8C19 39.2 16.5 35.9 16.5 31.6V30.2Z" />
        <path d="M24 14.5V18" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestSeven(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 7 Crest'}>
      <g {...s}>
        <circle cx="24" cy="27" r="8" />
        <circle cx="24" cy="27" r="2" />
        <path d="M24 16V20" />
        <path d="M24 34V38" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestEight(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 8 Crest'}>
      <g {...s}>
        <path d="M16 23.5H32" />
        <path d="M16 30.5H32" />
        <path d="M18 18H30V36H18V18Z" />
        <path d="M24 13V18" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestNine(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 9 Crest'}>
      <g {...s}>
        <path d="M24 16C18.8 19.6 16.8 23.5 18 27.8C18.9 31 21.2 33.1 24.9 34.2C28.7 35.3 30.6 37.2 30.6 39.8" />
        <path d="M18.5 39.2C20.2 40.8 22 41.6 24 41.6C26.2 41.6 28.2 40.6 30 38.7" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestEleven(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 11 Crest'}>
      <g {...s}>
        <path d="M24 13L28 22H36L29.5 27.5L32.2 36.2L24 31.7L15.8 36.2L18.5 27.5L12 22H20L24 13Z" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestTwentyTwo(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 22 Crest'}>
      <g {...s}>
        <path d="M15 20H33V37H15V20Z" />
        <path d="M19 24H29" />
        <path d="M19 29H29" />
        <path d="M24 14V20" />
        <path d="M17.5 41H30.5" />
      </g>
    </CrestShell>
  );
}

function LifePathCrestThirtyThree(props: LifePathCrestProps) {
  const s = crestStroke(props.mode, props.strokeWidth);
  return (
    <CrestShell {...props} title={props.title || 'Life Path 33 Crest'}>
      <g {...s}>
        <path d="M24 18C20.1 18 17.4 20.3 17.4 23.8C17.4 27.2 20 29.6 24 33.2C28 29.6 30.6 27.2 30.6 23.8C30.6 20.3 27.9 18 24 18Z" />
        <path d="M24 33.2V40.4" />
        <path d="M19.5 40.4H28.5" />
      </g>
    </CrestShell>
  );
}

export const lifePathCrestComponents = {
  '1': LifePathCrestOne,
  '2': LifePathCrestTwo,
  '3': LifePathCrestThree,
  '4': LifePathCrestFour,
  '5': LifePathCrestFive,
  '6': LifePathCrestSix,
  '7': LifePathCrestSeven,
  '8': LifePathCrestEight,
  '9': LifePathCrestNine,
  '11': LifePathCrestEleven,
  '22': LifePathCrestTwentyTwo,
  '33': LifePathCrestThirtyThree,
} as const;

export function LifePathCrestFallback({ mode = 'human', size = 96, title = 'Life Path Crest', className, animated, strokeWidth }: LifePathCrestProps) {
  const s = crestStroke(mode, strokeWidth);
  return (
    <CrestShell mode={mode} size={size} title={title} className={className} animated={animated}>
      <g {...s}>
        <path d="M24 17V36" />
        <circle cx="24" cy="25" r="5.2" />
        <path d="M18.5 41.2H29.5" />
      </g>
    </CrestShell>
  );
}

export function LifePathCrest({
  lifePath,
  mode = 'human',
  size = 96,
  title,
  className,
  animated,
  strokeWidth,
}: LifePathCrestProps & { lifePath?: LifePathCrestKey | string | number | null }) {
  const resolvedLifePath = getLifePathCrestKey(lifePath);
  const Component = resolvedLifePath ? lifePathCrestComponents[resolvedLifePath] : LifePathCrestFallback;
  const safeTitle = title || (resolvedLifePath ? `Life Path ${resolvedLifePath} Crest` : 'Life Path Crest');

  return (
    <span
      className={className}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        lineHeight: 0,
      }}
    >
      <Component
        mode={mode}
        size={size}
        title={safeTitle}
        animated={animated}
        strokeWidth={strokeWidth}
      />
    </span>
  );
}
