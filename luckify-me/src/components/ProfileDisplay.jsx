/**
 * ProfileDisplay — profile view
 *
 * Layer 1: Zone Hero (always visible — the daily read)
 * Layer 2: Foundation — who you are (always visible, element-accented)
 * Layer 3: Color Rhythm Calendar (expand to see the month)
 *
 * Dimensions are config-driven — add future dimensions to the array,
 * nothing else in this file needs to change.
 */

import { useState } from 'react';
import { DimensionCard } from './DimensionCard.jsx';
import { LuckyWindow } from './LuckyWindow.jsx';
import { RhythmCalendar } from './RhythmCalendar.jsx';
import { GateContentCard } from './GateContentCard.jsx';
import { TITHI_DATA, TITHI_AXIOMS, TITHI_SVGS } from '../constants/tithi.js';
import { ELEMENT_CONFIG, ELEMENT_AXIOMS } from '../constants/element.js';
import { LP_CONFIG } from '../constants/lifePath.js';
import { getBlend } from '../constants/blends.js';
import { GENE_KEYS } from '../constants/geneKeys.js';

// Element color palette — grounded, permanent, different energy from zone colors
const ELEMENT_COLORS = {
  Wood:  { text: '#6ab87a', accent: 'rgba(30, 110, 50, 0.18)' },
  Fire:  { text: '#e06040', accent: 'rgba(130, 30, 10, 0.18)' },
  Earth: { text: '#c89840', accent: 'rgba(110, 78, 10, 0.18)' },
  Metal: { text: '#90b0cc', accent: 'rgba(40, 70, 110, 0.16)' },
  Water: { text: '#4880c8', accent: 'rgba(20, 55, 130, 0.18)' },
};

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

// ── Collapsible Layer (calendar only) ──────────────────

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

// ── Foundation Section — always visible, element-accented ──

function FoundationSection({ blend, element, type, elemCfg, lifePathNum, dimensions }) {
  const elColor = ELEMENT_COLORS[element] || { text: 'var(--pip-primary)', accent: 'rgba(200,152,42,0.1)' };
  const tithiLabel = type.charAt(0).toUpperCase() + type.slice(1);

  return (
    <div className="foundation-section" style={{ '--el-text': elColor.text, '--el-accent': elColor.accent }}>
      {/* Identity bar */}
      <div className="foundation-identity">
        <span className="foundation-glyph">{elemCfg?.glyph}</span>
        <span className="foundation-identity-text">
          {element} · {tithiLabel} · Life Path {lifePathNum}
        </span>
      </div>

      {/* Blend — always visible */}
      {blend && (
        <div className="foundation-blend">
          <div className="foundation-blend-label">{element} × {tithiLabel}</div>
          <p className="foundation-blend-body">{blend.statement}</p>
        </div>
      )}

      {/* Dimension cards — individually expandable */}
      <div className="foundation-dimensions">
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
      </div>
    </div>
  );
}

// ── Main Component ──────────────────────────────────────

function GeneKeyIcon({ gate }) {
  return (
    <div className="gk-gate-circle">{gate}</div>
  );
}

export function ProfileDisplay({ profile, onNewProfile }) {
  const { type, cfg, element, lifePathNum, geneKeys } = profile;

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
    // ── Gene Keys (Dimension IV) ──
    ...(geneKeys ? [{
      key:    'geneKeys',
      system: 'DIMENSION IV · GENE KEYS',
      icon:   <GeneKeyIcon gate={geneKeys.lifeWork.gate} />,
      name:   `Gate ${geneKeys.lifeWork.gate}.${geneKeys.lifeWork.line} · Life's Work`,
      axiom:  GENE_KEYS[geneKeys.lifeWork.gate]?.gift || 'Descriptions coming soon',
      tabs: [
        {
          key: 'prime',
          label: 'Prime Keys',
          principles: [
            {
              title: `Life's Work — Gate ${geneKeys.lifeWork.gate} · Line ${geneKeys.lifeWork.line}`,
              body: GENE_KEYS[geneKeys.lifeWork.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.lifeWork.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.lifeWork.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.lifeWork.gate].siddhi}`
                : 'Gate descriptions coming — add your content to src/constants/geneKeys.js',
            },
            {
              title: `Evolution — Gate ${geneKeys.evolution.gate} · Line ${geneKeys.evolution.line}`,
              body: GENE_KEYS[geneKeys.evolution.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.evolution.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.evolution.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.evolution.gate].siddhi}`
                : `Gate ${geneKeys.evolution.gate} — add your content to src/constants/geneKeys.js`,
            },
            {
              title: `Radiance — Gate ${geneKeys.radiance.gate} · Line ${geneKeys.radiance.line}`,
              body: GENE_KEYS[geneKeys.radiance.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.radiance.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.radiance.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.radiance.gate].siddhi}`
                : `Gate ${geneKeys.radiance.gate} — add your content to src/constants/geneKeys.js`,
            },
            {
              title: `Purpose — Gate ${geneKeys.purpose.gate} · Line ${geneKeys.purpose.line}`,
              body: GENE_KEYS[geneKeys.purpose.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.purpose.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.purpose.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.purpose.gate].siddhi}`
                : `Gate ${geneKeys.purpose.gate} — add your content to src/constants/geneKeys.js`,
            },
          ],
        },
      ],
    }] : []),
  ];

  return (
    <div className="profile-page">

      {/* ── Layer 1: Zone Hero (today's frequency) ── */}
      <LuckyWindow profile={profile} />

      {/* ── Layer 2: Foundation (who you are — always visible) ── */}
      <FoundationSection
        blend={blend}
        element={element}
        type={type}
        elemCfg={elemCfg}
        lifePathNum={lifePathNum}
        dimensions={dimensions}
      />

      {/* ── Layer 3: Color Rhythm Calendar ── */}
      <ProfileLayer label="THIS MONTH'S RHYTHM">
        <RhythmCalendar profile={profile} />
      </ProfileLayer>

      {/* ── Layer 4: Purpose Frame ── */}
      {geneKeys?.purpose && (
        <GateContentCard profile={profile} />
      )}

      {/* New profile */}
      <button className="pip-button calc-btn" onClick={onNewProfile} style={{ marginTop: 16 }}>
        [ NEW PROFILE ]
      </button>

    </div>
  );
}
