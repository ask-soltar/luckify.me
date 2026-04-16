/**
 * LuckyWindow — Immersive Zone Hero
 * The primary daily read. Full-bleed zone color, large name, identity, mantra.
 * Future slot: Ask-Claude / fortune entry point.
 */

import { useMemo } from 'react';
import { calcTodayWindow } from '../utils/luckyWindow.js';
import { COLOR_RHYTHM } from '../constants/colorRhythm.js';

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

export function LuckyWindow({ profile }) {
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
      {/* Date */}
      <div className="zone-hero-date">{TODAY_LABEL}</div>

      {/* Zone + Identity */}
      <div className="zone-hero-main">
        <div className="zone-hero-name">{result.zone}</div>
        <div className="zone-hero-identity">
          {rhythm?.identity || result.band}
        </div>
      </div>

      {/* Mantra */}
      <div className="zone-hero-mantra">"{result.mantra}"</div>

      {/* Future: Ask-Claude / fortune slot */}
      <div className="zone-hero-ask">
        <span className="zone-hero-ask-icon">✦</span>
        <span className="zone-hero-ask-text">ASK ABOUT YOUR DAY</span>
        <span className="zone-hero-ask-soon">COMING SOON</span>
      </div>
    </div>
  );
}
