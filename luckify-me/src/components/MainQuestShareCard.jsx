import { useEffect, useRef, useState } from 'react';
import { downloadMainQuestShareCard, exportMainQuestShareCard } from '../utils/exportShareCard.js';
import { trackEvent } from '../utils/trackEvent.js';
import './MainQuestShareCard.css';

// Static 59.2 proof-of-concept content
const STATIC_CONTENT = {
  badge: 'MAIN QUEST UNLOCKED',
  title: 'Transformative Connection',
  sections: [
    {
      id: 'gift',
      icon: 'compass',
      heading: 'Your gift',
      body: 'You create connection naturally.',
    },
    {
      id: 'pattern',
      icon: 'spiral',
      heading: 'Your pattern',
      body: 'When it starts to matter, you keep it comfortable.',
    },
    {
      id: 'quest',
      icon: 'portal',
      heading: 'Your quest',
      body: 'Let the moment become real.',
    },
  ],
};

// Precomputed star positions — avoids hydration drift and re-randomisation on render
const STARS = [
  { x: 8.2, y: 3.1, r: 0.8, o: 0.7 }, { x: 15.4, y: 7.8, r: 1.2, o: 0.5 },
  { x: 23.1, y: 2.4, r: 0.6, o: 0.8 }, { x: 31.7, y: 11.2, r: 1.0, o: 0.4 },
  { x: 44.3, y: 4.5, r: 0.7, o: 0.9 }, { x: 52.8, y: 8.9, r: 1.4, o: 0.3 },
  { x: 61.0, y: 1.8, r: 0.6, o: 0.7 }, { x: 72.5, y: 6.3, r: 1.1, o: 0.6 },
  { x: 83.7, y: 3.9, r: 0.8, o: 0.5 }, { x: 92.1, y: 9.4, r: 1.3, o: 0.4 },
  { x: 5.6, y: 14.7, r: 0.6, o: 0.6 }, { x: 18.9, y: 18.3, r: 1.0, o: 0.7 },
  { x: 27.4, y: 22.6, r: 0.7, o: 0.5 }, { x: 38.2, y: 16.1, r: 1.2, o: 0.4 },
  { x: 47.6, y: 26.8, r: 0.9, o: 0.8 }, { x: 56.3, y: 20.4, r: 0.6, o: 0.6 },
  { x: 68.9, y: 14.2, r: 1.3, o: 0.3 }, { x: 78.1, y: 23.7, r: 0.7, o: 0.7 },
  { x: 88.4, y: 17.5, r: 1.0, o: 0.5 }, { x: 95.7, y: 21.9, r: 0.8, o: 0.6 },
  { x: 3.4, y: 31.2, r: 1.1, o: 0.4 }, { x: 12.8, y: 38.6, r: 0.6, o: 0.7 },
  { x: 22.3, y: 34.1, r: 1.4, o: 0.3 }, { x: 33.5, y: 42.7, r: 0.7, o: 0.6 },
  { x: 41.9, y: 35.8, r: 0.9, o: 0.5 }, { x: 64.2, y: 31.4, r: 1.0, o: 0.4 },
  { x: 75.6, y: 39.2, r: 0.6, o: 0.8 }, { x: 86.3, y: 33.6, r: 1.2, o: 0.5 },
  { x: 94.8, y: 41.5, r: 0.8, o: 0.6 }, { x: 7.1, y: 52.4, r: 1.0, o: 0.3 },
  { x: 19.6, y: 58.9, r: 0.7, o: 0.7 }, { x: 29.3, y: 63.1, r: 1.3, o: 0.4 },
  { x: 39.8, y: 55.7, r: 0.6, o: 0.6 }, { x: 50.4, y: 61.4, r: 0.9, o: 0.5 },
  { x: 62.7, y: 57.2, r: 1.1, o: 0.4 }, { x: 73.2, y: 64.8, r: 0.7, o: 0.7 },
  { x: 82.5, y: 52.3, r: 1.4, o: 0.3 }, { x: 91.3, y: 59.6, r: 0.8, o: 0.6 },
  { x: 97.6, y: 54.1, r: 1.0, o: 0.5 }, { x: 4.9, y: 72.8, r: 0.6, o: 0.7 },
  { x: 14.3, y: 79.4, r: 1.2, o: 0.4 }, { x: 25.7, y: 74.1, r: 0.8, o: 0.6 },
  { x: 36.1, y: 81.6, r: 1.0, o: 0.5 }, { x: 48.5, y: 76.3, r: 0.7, o: 0.7 },
  { x: 59.8, y: 82.9, r: 1.3, o: 0.3 }, { x: 70.4, y: 74.7, r: 0.6, o: 0.8 },
  { x: 80.9, y: 80.2, r: 1.1, o: 0.4 }, { x: 90.2, y: 75.8, r: 0.9, o: 0.5 },
  { x: 96.4, y: 83.4, r: 0.7, o: 0.6 }, { x: 2.8, y: 90.6, r: 1.2, o: 0.4 },
  { x: 11.5, y: 94.2, r: 0.6, o: 0.7 }, { x: 21.9, y: 88.7, r: 1.0, o: 0.5 },
  { x: 32.4, y: 95.8, r: 0.8, o: 0.6 }, { x: 43.7, y: 91.3, r: 1.4, o: 0.3 },
  { x: 55.1, y: 96.7, r: 0.7, o: 0.7 }, { x: 66.8, y: 90.1, r: 1.1, o: 0.4 },
  { x: 77.3, y: 94.5, r: 0.6, o: 0.8 }, { x: 87.6, y: 88.9, r: 1.3, o: 0.5 },
  { x: 98.1, y: 92.4, r: 0.9, o: 0.4 },
];

function IconCompass() {
  return (
    <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="22" cy="22" r="18" stroke="currentColor" strokeWidth="1" strokeOpacity="0.3" />
      <circle cx="22" cy="22" r="11" stroke="currentColor" strokeWidth="1" strokeOpacity="0.5" />
      <line x1="22" y1="4"  x2="22" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="22" y1="34" x2="22" y2="40" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="4"  y1="22" x2="10" y2="22" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="34" y1="22" x2="40" y2="22" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M22 12 L24.5 19.5 L32 22 L24.5 24.5 L22 32 L19.5 24.5 L12 22 L19.5 19.5 Z"
        fill="currentColor" fillOpacity="0.7" stroke="currentColor" strokeWidth="0.5" />
    </svg>
  );
}

function IconSpiral() {
  return (
    <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        d="M22 22
           C22 18.5 19 16 15.5 17.5
           C12 19 11.5 24 14.5 26.5
           C18.5 30 25.5 28 27.5 23
           C30.5 16 25.5 8 17 7
           C8.5 6 3 13 3 22
           C3 31 9 40 22 40"
        stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeOpacity="0.85" />
      <circle cx="22" cy="22" r="2" fill="currentColor" fillOpacity="0.6" />
    </svg>
  );
}

function IconPortal() {
  return (
    <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M11 40 L11 18 C11 11 16 7 22 7 C28 7 33 11 33 18 L33 40"
        stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="5" y1="40" x2="39" y2="40" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <ellipse cx="22" cy="18" rx="7" ry="5" stroke="currentColor" strokeWidth="1" strokeOpacity="0.4" />
      <circle cx="22" cy="18" r="2" fill="currentColor" fillOpacity="0.6" />
    </svg>
  );
}

function HeroSymbol() {
  return (
    <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        {/* Wide soft glow — two-pass blur composited under source */}
        <filter id="mqsc-star-glow" x="-60%" y="-60%" width="220%" height="220%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="wide" />
          <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="tight" />
          <feMerge>
            <feMergeNode in="wide" />
            <feMergeNode in="tight" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        {/* Tight halo for center dot */}
        <filter id="mqsc-dot-glow" x="-150%" y="-150%" width="400%" height="400%">
          <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* ── Layer 1: three thin concentric rings ── */}
      <circle cx="100" cy="100" r="83" stroke="rgba(139,92,246,0.08)" strokeWidth="0.75" />
      <circle cx="100" cy="100" r="61" stroke="rgba(59,130,246,0.10)" strokeWidth="0.75" />
      <circle cx="100" cy="100" r="42" stroke="rgba(212,175,55,0.13)" strokeWidth="0.75" />

      {/* ── Layer 2: two subtle orbit arcs + minimal cardinal ticks ── */}
      <ellipse cx="100" cy="100" rx="76" ry="18"
        stroke="rgba(139,92,246,0.22)" strokeWidth="1" fill="none"
        transform="rotate(-22 100 100)" />
      <ellipse cx="100" cy="100" rx="76" ry="18"
        stroke="rgba(59,130,246,0.16)" strokeWidth="1" fill="none"
        transform="rotate(22 100 100)" />

      {/* Cardinal ticks — hair-thin, quarter-opacity */}
      <line x1="100" y1="16" x2="100" y2="26" stroke="rgba(212,175,55,0.22)" strokeWidth="0.75" strokeLinecap="round" />
      <line x1="100" y1="174" x2="100" y2="184" stroke="rgba(212,175,55,0.22)" strokeWidth="0.75" strokeLinecap="round" />
      <line x1="16"  y1="100" x2="26"  y2="100" stroke="rgba(212,175,55,0.22)" strokeWidth="0.75" strokeLinecap="round" />
      <line x1="174" y1="100" x2="184" y2="100" stroke="rgba(212,175,55,0.22)" strokeWidth="0.75" strokeLinecap="round" />

      {/* ── Layer 3: geometrically precise 8-point star + center dot ── */}
      {/* Outer r=38, inner r=16 — calculated at 22.5° offsets from 90° start */}
      <path
        d="M100,62 L106.1,85.2 L126.9,73.1 L114.8,93.9
           L138,100 L114.8,106.1 L126.9,126.9 L106.1,114.8
           L100,138 L93.9,114.8 L73.1,126.9 L85.2,106.1
           L62,100 L85.2,93.9 L73.1,73.1 L93.9,85.2 Z"
        fill="rgba(212,175,55,0.84)"
        stroke="rgba(255,225,110,0.18)"
        strokeWidth="0.5"
        filter="url(#mqsc-star-glow)"
      />
      <circle cx="100" cy="100" r="5" fill="rgba(255,232,130,0.96)" filter="url(#mqsc-dot-glow)" />
    </svg>
  );
}

const ICON_MAP = { compass: IconCompass, spiral: IconSpiral, portal: IconPortal };

export function MainQuestShareCard({ cardId = 'mq-share-card', content = STATIC_CONTENT, onComplete, skipLabel = 'Skip for now', trackingMeta = {} }) {
  const wrapperRef = useRef(null);
  const [scale, setScale] = useState(0.32);
  const [exporting, setExporting] = useState(false);
  const [confirmed, setConfirmed] = useState(false);

  useEffect(() => {
    if (!wrapperRef.current) return;
    const measure = () => {
      const width = wrapperRef.current?.getBoundingClientRect().width;
      if (width) setScale(width / 1080);
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(wrapperRef.current);
    return () => ro.disconnect();
  }, []);

  async function handleShare() {
    if (exporting) return;
    setExporting(true);
    try {
      await exportMainQuestShareCard(cardId);
      trackEvent('main_quest_share_card_shared', trackingMeta);
      setConfirmed(true);
      trackEvent('main_quest_share_card_confirmed', { ...trackingMeta, action: 'share' });
    } catch (err) {
      console.error('Share failed:', err);
    } finally {
      setExporting(false);
    }
  }

  async function handleSave() {
    if (exporting) return;
    setExporting(true);
    try {
      await downloadMainQuestShareCard(cardId);
      trackEvent('main_quest_share_card_saved', trackingMeta);
      setConfirmed(true);
      trackEvent('main_quest_share_card_confirmed', { ...trackingMeta, action: 'save' });
    } catch (err) {
      console.error('Save failed:', err);
    } finally {
      setExporting(false);
    }
  }

  const { badge, title, sections } = content;

  return (
    <div className="mqsc-outer">
      {/* Scaled preview wrapper */}
      <div
        className="mqsc-preview"
        ref={wrapperRef}
        style={{ height: `${1350 * scale}px` }}
      >
        {/* The actual export card — always 1080×1350 */}
        <div
          id={cardId}
          className="mqsc"
          style={{ transform: `scale(${scale})` }}
        >
          {/* Starfield */}
          <div className="mqsc__stars" aria-hidden="true">
            {STARS.map((s, i) => (
              <div
                key={i}
                className="mqsc__star"
                style={{
                  left: `${s.x}%`,
                  top: `${s.y}%`,
                  width: `${s.r * 2}px`,
                  height: `${s.r * 2}px`,
                  opacity: s.o,
                }}
              />
            ))}
          </div>

          {/* Ambient glow */}
          <div className="mqsc__glow" aria-hidden="true" />

          {/* Glass panel */}
          <div className="mqsc__glass">
            {/* Badge */}
            <div className="mqsc__badge">{badge}</div>

            {/* Hero symbol */}
            <div className="mqsc__hero">
              <div className="mqsc__hero-glow" aria-hidden="true" />
              <HeroSymbol />
            </div>

            {/* Title */}
            <div className="mqsc__title">{title}</div>
            <div className="mqsc__rule" aria-hidden="true" />

            {/* Three sections */}
            <div className="mqsc__sections">
              {sections.map(section => {
                const Icon = ICON_MAP[section.icon];
                return (
                  <div className="mqsc__section" key={section.id}>
                    <div className="mqsc__section-icon">
                      {Icon ? <Icon /> : null}
                    </div>
                    <div className="mqsc__section-text">
                      <div className="mqsc__section-heading">{section.heading}</div>
                      <div className="mqsc__section-body">{section.body}</div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Branding footer */}
            <div className="mqsc__footer">
              <div className="mqsc__footer-cta">Find your Main Quest</div>
              <div className="mqsc__footer-brand">Luckify.me</div>
            </div>
          </div>
        </div>
      </div>

      {confirmed ? (
        /* Confirmation state — shown after share or save succeeds */
        <div className="mqsc-confirmed">
          <div className="mqsc-confirmed__title">Quest marked.</div>
          <p className="mqsc-confirmed__body">
            You&apos;ll start noticing this pattern faster now.
          </p>
          {onComplete && (
            <button
              type="button"
              className="mqsc-btn mqsc-btn--continue"
              onClick={onComplete}
            >
              Continue to Quest →
            </button>
          )}
        </div>
      ) : (
        <>
          {/* Share prompt */}
          <div className="mqsc-prompt">
            <p className="mqsc-prompt__headline">
              A quest becomes real when it is named.
            </p>
            <p className="mqsc-prompt__sub">
              Share your Main Quest to mark the pattern you&apos;re ready to
              recognize — and maybe help someone else recognize theirs too.
            </p>
          </div>

          {/* Buttons */}
          <div className="mqsc-buttons">
            <button
              type="button"
              className="mqsc-btn mqsc-btn--share"
              onClick={handleShare}
              disabled={exporting}
            >
              {exporting ? 'Preparing…' : 'Share My Main Quest'}
            </button>
            <button
              type="button"
              className="mqsc-btn mqsc-btn--save"
              onClick={handleSave}
              disabled={exporting}
            >
              Save Privately
            </button>

            {onComplete && (
              <button
                type="button"
                className="mqsc-btn mqsc-btn--skip"
                onClick={() => {
                  trackEvent('main_quest_share_card_skipped', trackingMeta);
                  onComplete();
                }}
              >
                {skipLabel}
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
}
