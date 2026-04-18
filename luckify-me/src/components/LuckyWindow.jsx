/**
 * LuckyWindow — Immersive Zone Hero
 * The primary daily read. Full-bleed zone color, large name, identity, mantra.
 * Future slot: Ask-Claude / fortune entry point.
 */

import { useMemo, useState } from 'react';
import { calcTodayWindow } from '../utils/luckyWindow.js';
import { COLOR_RHYTHM } from '../constants/colorRhythm.js';
import { getZoneScores, GUIDANCE, CELL_LINE, CAT_EMOJI } from '../constants/zoneScoring.js';
import { LocationInput } from './LocationInput.jsx';

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

const TODAY_LABEL = new Date().toLocaleDateString('en-US', {
  weekday: 'long', month: 'long', day: 'numeric'
});

export function LuckyWindow({ profile, onLocationChange }) {
  const [catsOpen, setCatsOpen] = useState(false);
  const [editingLoc, setEditingLoc] = useState(false);
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

  // Radial glow from top-center — zone color fades into dark base
  const heroBg = `radial-gradient(ellipse 70% 60% at 50% 0%, ${css.glow}44 0%, ${css.bg} 65%)`;

  return (
    <div className="zone-hero" style={{ background: heroBg, color: css.text }}>
      {/* Date + Location */}
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

      {/* Zone + Identity */}
      <div className="zone-hero-main">
        <div className="zone-hero-name">{result.zone}</div>
        <div className="zone-hero-identity">
          {rhythm?.identity || result.band}
        </div>
      </div>

      {/* Mantra */}
      <div className="zone-hero-mantra">"{result.mantra}"</div>

      {/* Category score bars — collapsible */}
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

      {/* Future: Ask-Claude / fortune slot */}
      <div className="zone-hero-ask">
        <span className="zone-hero-ask-icon">✦</span>
        <span className="zone-hero-ask-text">ASK ABOUT YOUR DAY</span>
        <span className="zone-hero-ask-soon">COMING SOON</span>
      </div>
    </div>
  );
}
