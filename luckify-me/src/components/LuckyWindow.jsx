/**
 * LuckyWindow — Immersive Zone Hero
 * The primary daily read. Full-bleed zone color, large name, identity, mantra.
 * Future slot: Ask-Claude / fortune entry point.
 */

import { useMemo, useRef, useState } from 'react';
import { calcTodayWindow } from '../utils/luckyWindow.js';
import { COLOR_RHYTHM } from '../constants/colorRhythm.js';
import { getZoneScores, GUIDANCE, CELL_LINE, CAT_EMOJI } from '../constants/zoneScoring.js';
import { getDecisionSupportForRhythm } from '../constants/rhythmDecisionSupport.js';
import { LocationInput } from './LocationInput.jsx';
import { RhythmCalendar } from './RhythmCalendar.jsx';

// Format a timezone ID or GMT offset into a readable city/offset label
function locationLabel(tzId, gmt) {
  if (tzId) {
    const parts = tzId.split('/');
    return parts[parts.length - 1].replace(/_/g, ' ');
  }
  if (gmt !== null && gmt !== undefined) {
    const sign = gmt >= 0 ? '+' : '';
    return `UTC${sign}${gmt}`;
  }
  return 'Set location';
}

function CategoryBar({ cat, normalized, textColor, guidance }) {
  const pct = normalized * 10;
  return (
    <div className="cat-score-row">
      <span className="cat-score-emoji">{CAT_EMOJI[cat] || '·'}</span>
      <span className="cat-score-name" style={{ color: textColor }}>{cat}</span>
      <div className="cat-score-bar-wrap">
        <div className="cat-score-bar" style={{ width: `${pct}%`, background: textColor }} />
      </div>
      <span className="cat-score-val" style={{ color: textColor }}>{normalized.toFixed(1)}</span>
      <span className="cat-score-guide" style={{ color: textColor }}>{guidance}</span>
    </div>
  );
}

// Raw hex values used to build the radial glow — must match index.css zone vars
const ZONE_CSS = {
  Pink:   { bg: '#3d0a34', text: 'var(--pink-text)',   glow: '#c03090' },
  Orange: { bg: '#2e1200', text: 'var(--orange-text)', glow: '#d06020' },
  Blue:   { bg: '#060f20', text: 'var(--blue-text)',   glow: '#2060c0' },
  Yellow: { bg: '#1c1600', text: 'var(--yellow-text)', glow: '#b0a000' },
  Green:  { bg: '#061208', text: 'var(--green-text)',  glow: '#10a030' },
  Purple: { bg: '#100720', text: 'var(--purple-text)', glow: '#7030c0' },
  Red:    { bg: '#1e0605', text: 'var(--red-text)',    glow: '#c02018' },
  Brown:  { bg: '#100906', text: 'var(--brown-text)',  glow: '#806040' },
};

// Optional atmospheric art backgrounds. Only zones listed here receive the
// image treatment; all others keep the existing pure-gradient card.
const ZONE_ART = {
  Blue: '/color-rhythm-backgrounds/Blue.png',
};

const TODAY_LABEL = new Date().toLocaleDateString('en-US', {
  weekday: 'long', month: 'long', day: 'numeric'
});

export function LuckyWindow({ profile, humanDesign = null, onLocationChange, mode = 'human', onModeChange }) {
  const [catsOpen, setCatsOpen] = useState(false);
  const [editingLoc, setEditingLoc] = useState(false);
  const [activePanel, setActivePanel] = useState(0);
  const gestureRef = useRef({
    startX: 0,
    startY: 0,
    startTime: 0,
    axis: null,
  });
  const result = useMemo(() => {
    try {
      const { y, mo, dy } = profile;
      if (!y || !mo || !dy) return null;
      const pad = n => String(n).padStart(2, '0');
      return calcTodayWindow({
        birthDate:  `${y}-${pad(mo)}-${pad(dy)}`,
        birthTime:  profile.birthTime  || '12:00',
        birthGMT:   profile.birthGMT   ?? 0,
        currentGMT: profile.currentGMT ?? profile.birthGMT ?? 0
      });
    } catch { return null; }
  }, [profile]);

  if (!result) return null;

  const css    = ZONE_CSS[result.zone] || ZONE_CSS.Yellow;
  const rhythm = COLOR_RHYTHM[result.zone?.toLowerCase()];
  const authority = humanDesign?.authority || profile?.humanDesign?.authority || null;
  const decisionSupport = getDecisionSupportForRhythm(authority, result.zone);
  const panelCount = 2;
  const zoneArtUrl = ZONE_ART[result.zone] || null;
  const zoneHasAtmosphere = Boolean(zoneArtUrl || result.zone === 'Green');

  // Radial glow from top-center — zone color fades into dark base
  const heroBg = `radial-gradient(ellipse 70% 60% at 50% 0%, ${css.glow}44 0%, ${css.bg} 65%)`;

  function goToPanel(nextIndex) {
    setActivePanel((nextIndex + panelCount) % panelCount);
  }

  function handleTouchStart(event) {
    const touch = event.touches?.[0];
    if (!touch) return;

    gestureRef.current = {
      startX: touch.clientX,
      startY: touch.clientY,
      startTime: performance.now(),
      axis: null,
    };
  }

  function handleTouchMove(event) {
    const touch = event.touches?.[0];
    if (!touch) return;

    const dx = touch.clientX - gestureRef.current.startX;
    const dy = touch.clientY - gestureRef.current.startY;
    const absX = Math.abs(dx);
    const absY = Math.abs(dy);

    // Dead zone: tiny movements should never commit the gesture direction.
    if (gestureRef.current.axis == null && absX < 12 && absY < 12) return;

    if (gestureRef.current.axis == null) {
      // Directional lock: only treat this as horizontal when intent is clearly
      // horizontal, otherwise let the gesture remain a normal vertical scroll.
      if (absX > absY * 1.35 && absX > 18) {
        gestureRef.current.axis = 'x';
      } else if (absY > absX * 1.15 && absY > 14) {
        gestureRef.current.axis = 'y';
      }
    }

    if (gestureRef.current.axis === 'x') {
      event.preventDefault();
    }
  }

  function handleTouchEnd(event) {
    const touch = event.changedTouches?.[0];
    if (!touch) return;

    const deltaX = touch.clientX - gestureRef.current.startX;
    const deltaY = touch.clientY - gestureRef.current.startY;
    const elapsed = Math.max(performance.now() - gestureRef.current.startTime, 1);
    const absX = Math.abs(deltaX);
    const absY = Math.abs(deltaY);
    const velocityX = absX / elapsed; // px per ms

    // If the gesture never resolved to a horizontal swipe, do nothing.
    if (gestureRef.current.axis !== 'x') {
      gestureRef.current.axis = null;
      return;
    }

    // A deliberate panel change now requires either:
    // 1. a strong horizontal drag, or
    // 2. a smaller but clearly intentional flick.
    const crossedDistance = absX >= 72 && absX > absY * 1.3;
    const crossedFlick = absX >= 48 && velocityX >= 0.42 && absX > absY * 1.5;

    gestureRef.current.axis = null;

    if (!crossedDistance && !crossedFlick) return;

    if (deltaX < 0) goToPanel(activePanel + 1);
    else goToPanel(activePanel - 1);
  }

  return (
    <div
      className={`zone-hero zone-hero--${result.zone?.toLowerCase() || 'yellow'}${zoneHasAtmosphere ? ' zone-hero--artful' : ''}`}
      style={{
        background: heroBg,
        color: css.text,
        ...(zoneArtUrl ? { '--zone-art-image': `url("${zoneArtUrl}")` } : {}),
      }}
    >
      {zoneHasAtmosphere && (
        <div className="zone-hero-art" aria-hidden="true">
          <div className="zone-hero-art-base" />
          <div className="zone-hero-art-glow" />
          <div className="zone-hero-art-image" />
          <div className="zone-hero-art-veil" />
        </div>
      )}

      <div className="zone-hero-topbar">
        <div className="zone-hero-topbar-copy">
          <div className="zone-hero-date">{TODAY_LABEL}</div>
          <div
            className="zone-hero-location"
            onClick={() => setEditingLoc(o => !o)}
            title="Change current location"
          >
            <span className="zone-hero-loc-dot">◎</span>
            <span className="zone-hero-loc-label">
              {locationLabel(profile.currentTzId, profile.currentGMT)}
            </span>
            <span className="zone-hero-loc-edit">✎</span>
          </div>
        </div>

        <button
          type="button"
          className="profile-mode-toggle"
          onClick={() => onModeChange?.(mode === 'human' ? 'operator' : 'human')}
          aria-label={`Switch to ${mode === 'human' ? 'command' : 'character'} mode`}
        >
          <span className={mode === 'human' ? 'active' : ''}>CHARACTER VIEW</span>
          <span className={mode === 'operator' ? 'active' : ''}>COMMAND MODE</span>
        </button>
      </div>

      {editingLoc && (
        <div className="zone-hero-loc-editor">
          <LocationInput
            placeholder="Search city to update location…"
            onSelect={sel => {
              if (sel && onLocationChange) {
                onLocationChange({ offset: sel.offset, tzId: sel.tzId, label: sel.label });
                setEditingLoc(false);
              }
            }}
          />
        </div>
      )}

      <div className="zone-hero-panel-tabs" role="tablist" aria-label="Rhythm views">
        <button
          type="button"
          role="tab"
          aria-selected={activePanel === 0}
          className={`zone-hero-panel-tab${activePanel === 0 ? ' active' : ''}`}
          onClick={() => goToPanel(0)}
        >
          Color Rhythm
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={activePanel === 1}
          className={`zone-hero-panel-tab${activePanel === 1 ? ' active' : ''}`}
          onClick={() => goToPanel(1)}
        >
          Monthly Calendar
        </button>
      </div>

      <div
        className="zone-hero-panel-shell"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        <div
          className="zone-hero-panel-track"
          style={{ transform: `translateX(-${activePanel * 50}%)` }}
        >
          <section className="zone-hero-panel zone-hero-panel--today" aria-label="Color Rhythm">
            <div className="zone-hero-main">
              <div className="zone-hero-mode-label">ACTIVE RHYTHM</div>
              <div className="zone-hero-name">{result.zone}</div>
            </div>

            <div className="zone-hero-authority">
              <div className="zone-hero-authority-label">YOUR DECISION ENGINE</div>
              <div className="zone-hero-authority-engine">
                {decisionSupport.authorityEngineName || decisionSupport.authorityLabel}
              </div>
              <div className="zone-hero-authority-human">
                {(authority || decisionSupport.authorityLabel)} · Always active
              </div>
            </div>

            <div className="zone-hero-decision-support">
              <div className="zone-hero-decision-support-label">TODAY&apos;S DECISION GUIDANCE</div>
              <div className="zone-hero-decision-support-cue">
                {decisionSupport.slogan || result.mantra}
              </div>
              <p className="zone-hero-decision-support-text">{decisionSupport.supportText}</p>
              <div className="zone-hero-decision-support-grid">
                <div className="zone-hero-decision-support-item zone-hero-decision-support-item--best">
                  <div className="zone-hero-decision-support-item-label">Best Use</div>
                  <p className="zone-hero-decision-support-item-copy">{decisionSupport.bestUseText}</p>
                </div>
                <div className="zone-hero-decision-support-item zone-hero-decision-support-item--watch">
                  <div className="zone-hero-decision-support-item-label">Watch Out</div>
                  <p className="zone-hero-decision-support-item-copy">{decisionSupport.watchOutText}</p>
                </div>
              </div>
            </div>

            <div className="zone-hero-cats">
              <button className="zone-hero-cats-toggle" onClick={() => setCatsOpen(o => !o)}>
                <span>TODAY'S FREQUENCIES</span>
                <span className={`zone-hero-cats-chevron${catsOpen ? ' open' : ''}`}>▼</span>
              </button>
              {catsOpen && (
                <div className="zone-hero-cats-body">
                  {getZoneScores(result.zone).map(({ cat, normalized }) => (
                    <CategoryBar
                      key={cat}
                      cat={cat}
                      normalized={normalized}
                      textColor={css.text}
                      guidance={GUIDANCE[result.zone]?.[cat] || ''}
                    />
                  ))}
                  {CELL_LINE[result.zone] && (
                    <p className="zone-hero-cats-tagline">{CELL_LINE[result.zone]}</p>
                  )}
                </div>
              )}
            </div>

            <div className="zone-hero-ask">
              <span className="zone-hero-ask-icon">✦</span>
              <span className="zone-hero-ask-text">ASK ABOUT YOUR DAY</span>
              <span className="zone-hero-ask-soon">COMING SOON</span>
            </div>
          </section>

          <section className="zone-hero-panel zone-hero-panel--calendar" aria-label="Monthly Rhythm Calendar">
            <div className="zone-hero-calendar-intro">
              <div className="zone-hero-calendar-eyebrow">MONTHLY RHYTHM CALENDAR</div>
              <div className="zone-hero-calendar-title">Track how your color rhythm moves through the month.</div>
            </div>
            <RhythmCalendar profile={profile} embedded />
          </section>
        </div>
      </div>
    </div>
  );
}
