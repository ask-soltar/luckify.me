/**
 * ProfileDisplay — 3-layer profile view
 *
 * Layer 1: Zone Hero (always visible — the daily read)
 * Layer 2: Color Rhythm Calendar (expand to see the month)
 * Layer 3: Your Profile — dimension cards (expand to see the "why")
 *
 * Dimensions are config-driven — add future dimensions to the array,
 * nothing else in this file needs to change.
 */

import { useState } from 'react';
import { DimensionCard } from './DimensionCard.jsx';
import { LuckyWindow } from './LuckyWindow.jsx';
import { RhythmCalendar } from './RhythmCalendar.jsx';
import { TITHI_DATA, TITHI_AXIOMS, TITHI_SVGS } from '../constants/tithi.js';
import { ELEMENT_CONFIG, ELEMENT_AXIOMS } from '../constants/element.js';
import { LP_CONFIG } from '../constants/lifePath.js';
import { getBlend } from '../constants/blends.js';

// ── Icons ──────────────────────────────────────────────

function TithiIcon({ type }) {
  const svg = TITHI_SVGS[type] || '';
  return (
    <svg viewBox="0 0 56 56" fill="none" style={{ width: 36, height: 36 }}
      dangerouslySetInnerHTML={{ __html: svg }} />
  );
}

function ElementIcon({ element }) {
  const cfg = ELEMENT_CONFIG[element];
  return <span style={{ fontSize: 28 }}>{cfg?.glyph || '?'}</span>;
}

function LifePathIcon({ number }) {
  return <div className="lp-number-circle">{number}</div>;
}

// ── Collapsible Layer ───────────────────────────────────

function ProfileLayer({ label, defaultOpen = false, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="profile-layer">
      <button className="profile-layer-toggle" onClick={() => setOpen(o => !o)}>
        <span className="profile-layer-label">{label}</span>
        <span className={`profile-layer-chevron${open ? ' open' : ''}`}>▼</span>
      </button>
      {open && <div className="profile-layer-body">{children}</div>}
    </div>
  );
}

// ── Main Component ──────────────────────────────────────

export function ProfileDisplay({ profile, onNewProfile }) {
  const { type, cfg, element, lifePathNum } = profile;

  const tithiData  = TITHI_DATA[type];
  const tithiAxiom = TITHI_AXIOMS[type];
  const elemCfg    = ELEMENT_CONFIG[element];
  const elemAxiom  = ELEMENT_AXIOMS[element];
  const lpCfg      = LP_CONFIG[lifePathNum];
  const blend      = getBlend(element, type);

  // ── Dimension config array ──────────────────────────
  // Add future dimensions here — no other changes needed.
  const dimensions = [
    {
      key:    'tithi',
      system: 'DIMENSION I · TITHI',
      icon:   <TithiIcon type={type} />,
      name:   cfg?.label || type,
      axiom:  tithiAxiom,
      tabs:   tithiData ? [
        { key: 'operating', label: 'Operating', principles: tithiData.operating },
        { key: 'intuitive', label: 'Intuitive',  principles: tithiData.intuitive },
      ] : [],
    },
    {
      key:    'element',
      system: 'DIMENSION II · WU XING',
      icon:   <ElementIcon element={element} />,
      name:   `${element} · ${elemCfg?.keyword || ''}`,
      axiom:  elemAxiom,
      tabs:   elemCfg ? [
        { key: 'desc', label: 'Signal', principles: [{ title: elemCfg.keyword, body: elemCfg.desc }] }
      ] : [],
    },
    {
      key:    'lifePath',
      system: 'DIMENSION III · LIFE PATH',
      icon:   <LifePathIcon number={lifePathNum} />,
      name:   lpCfg?.name || `Life Path ${lifePathNum}`,
      axiom:  lpCfg?.axiom,
      tabs:   lpCfg ? [
        { key: 'mission', label: 'Mission', principles: [{ title: lpCfg.name, body: lpCfg.axiom }] }
      ] : [],
    },
    // future: { key: 'destinyCard', system: 'DIMENSION IV · ...', ... }
  ];

  return (
    <div className="profile-page">

      {/* ── Layer 1: Zone Hero (always visible) ── */}
      <LuckyWindow profile={profile} />

      {/* ── Layer 2: Color Rhythm Calendar ── */}
      <ProfileLayer label="THIS MONTH'S RHYTHM">
        <RhythmCalendar profile={profile} />
      </ProfileLayer>

      {/* ── Layer 3: Your Profile ── */}
      <ProfileLayer label="YOUR PROFILE">
        {/* Signal blend — the combo statement */}
        {blend && (
          <div className="profile-blend">
            <div className="profile-blend-label">
              {element} × {type.charAt(0).toUpperCase() + type.slice(1)}
            </div>
            <p className="profile-blend-statement">{blend.statement}</p>
          </div>
        )}

        {/* Dimension cards — config driven */}
        {dimensions.map(dim => (
          <DimensionCard
            key={dim.key}
            icon={dim.icon}
            system={dim.system}
            name={dim.name}
            axiom={dim.axiom}
            tabs={dim.tabs}
          />
        ))}
      </ProfileLayer>

      {/* New profile */}
      <button className="pip-button calc-btn" onClick={onNewProfile} style={{ marginTop: 16 }}>
        [ NEW PROFILE ]
      </button>

    </div>
  );
}
