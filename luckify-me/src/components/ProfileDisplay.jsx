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

import { useState, useMemo } from 'react';
import { DimensionCard } from './DimensionCard.jsx';
import { LuckyWindow } from './LuckyWindow.jsx';
import { RhythmCalendar } from './RhythmCalendar.jsx';
import { GateContentCard } from './GateContentCard.jsx';
import { TITHI_DATA, TITHI_AXIOMS, TITHI_SVGS } from '../constants/tithi.js';
import { ELEMENT_CONFIG, ELEMENT_AXIOMS } from '../constants/element.js';
import { LP_CONFIG } from '../constants/lifePath.js';
import { getBlend } from '../constants/blends.js';
import { GENE_KEYS } from '../constants/geneKeys.js';
import { PURPOSE_GATES } from '../constants/purposeGates.js';
import { PLANETARY_FIX } from '../constants/planetaryFix.js';
import { calcGeneKeys, calcAllActivations } from '../utils/geneKeys.js';

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

// Best available description for a gate.
// If line is provided and has specific content, uses that; otherwise falls back to overall.
// Priority: line-specific adult → overall kids → overall adult
function gateDesc(gate, line) {
  const pg = PURPOSE_GATES[String(gate)];
  if (!pg) return null;
  const lineContent = line ? pg.lines?.[String(line)]?.adult?.header : null;
  return lineContent
      || pg.overall?.kids?.header
      || pg.overall?.adult?.header
      || null;
}

export function ProfileDisplay({ profile, onNewProfile, onLocationChange }) {
  const { type, cfg, element, lifePathNum, birthTime } = profile;

  // Always recompute geneKeys from stored birth data so old profiles pick up
  // formula fixes (GSTART, solar arc) without needing a manual recalculation.
  const geneKeys = useMemo(() => {
    const { y, mo, dy, birthTime: bt, birthGMT } = profile;
    if (!y || !mo || !dy) return profile.geneKeys;
    try {
      return calcGeneKeys({ year: y, month: mo, day: dy, birthTime: bt || '12:00', tzOffset: birthGMT ?? 0 });
    } catch { return profile.geneKeys; }
  }, [profile]);

  // Activations — also always recomputed on the fly.
  const activations = useMemo(() => {
    const { y, mo, dy, birthTime: bt, birthGMT } = profile;
    if (!y || !mo || !dy) return null;
    try {
      return calcAllActivations({ year: y, month: mo, day: dy, birthTime: bt || '12:00', tzOffset: birthGMT ?? 0 });
    } catch { return null; }
  }, [profile]);
  const hasBirthTime = Boolean(birthTime) && birthTime !== '00:00';

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
      axiom:  GENE_KEYS[geneKeys.lifeWork.gate]?.gift
           || gateDesc(geneKeys.lifeWork.gate, hasBirthTime ? geneKeys.lifeWork.line : null)
           || 'Descriptions coming soon',
      tabs: [
        {
          key: 'prime',
          label: 'Prime Keys',
          principles: [
            {
              title: `Life's Work — Gate ${geneKeys.lifeWork.gate} · Line ${geneKeys.lifeWork.line}`,
              body: GENE_KEYS[geneKeys.lifeWork.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.lifeWork.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.lifeWork.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.lifeWork.gate].siddhi}`
                : gateDesc(geneKeys.lifeWork.gate, hasBirthTime ? geneKeys.lifeWork.line : null) || `Gate ${geneKeys.lifeWork.gate} — content coming soon`,
            },
            {
              title: `Evolution — Gate ${geneKeys.evolution.gate} · Line ${geneKeys.evolution.line}`,
              body: GENE_KEYS[geneKeys.evolution.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.evolution.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.evolution.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.evolution.gate].siddhi}`
                : gateDesc(geneKeys.evolution.gate, hasBirthTime ? geneKeys.evolution.line : null) || `Gate ${geneKeys.evolution.gate} — content coming soon`,
            },
            {
              title: `Radiance — Gate ${geneKeys.radiance.gate} · Line ${geneKeys.radiance.line}`,
              body: GENE_KEYS[geneKeys.radiance.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.radiance.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.radiance.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.radiance.gate].siddhi}`
                : gateDesc(geneKeys.radiance.gate, hasBirthTime ? geneKeys.radiance.line : null) || `Gate ${geneKeys.radiance.gate} — content coming soon`,
            },
            {
              title: `Purpose — Gate ${geneKeys.purpose.gate} · Line ${geneKeys.purpose.line}`,
              body: GENE_KEYS[geneKeys.purpose.gate]
                ? `Shadow: ${GENE_KEYS[geneKeys.purpose.gate].shadow}  ·  Gift: ${GENE_KEYS[geneKeys.purpose.gate].gift}  ·  Siddhi: ${GENE_KEYS[geneKeys.purpose.gate].siddhi}`
                : gateDesc(geneKeys.purpose.gate, hasBirthTime ? geneKeys.purpose.line : null) || `Gate ${geneKeys.purpose.gate} — content coming soon`,
            },
          ],
        },
      ],
    }] : []),

    // ── Planetary Fix (Dimension V) ──
    // For each of the 24 activations, look up the gate.line in the 384-line fix table.
    // If the activating planet matches the exalting planet → EXALTED
    // If the activating planet matches the detrimenting planet → DETRIMENT
    // Otherwise → neither (not shown)
    ...(activations ? (() => {
      const chartLabel = chart => chart === 'conscious' ? 'C' : 'D';

      const flagged = activations
        .map(a => {
          const fix = PLANETARY_FIX[`${a.gate}.${a.line}`];
          if (!fix) return null;
          if (fix.exalt === a.planet)     return { ...a, polarity: 'exalt' };
          if (fix.detriment === a.planet) return { ...a, polarity: 'detriment' };
          return null;
        })
        .filter(Boolean);

      if (!flagged.length) return [];

      const exalted   = flagged.filter(a => a.polarity === 'exalt');
      const detriment = flagged.filter(a => a.polarity === 'detriment');

      const toItem = a => ({
        title: `${a.symbol} ${a.planet}  ${chartLabel(a.chart)} · Gate ${a.gate}.${a.line}`,
        body:  PLANETARY_FIX[`${a.gate}.${a.line}`]
               ? `${a.planet} is the ${a.polarity === 'exalt' ? 'exalting' : 'detrimenting'} planet for Gate ${a.gate}.${a.line} — a supported, integrated expression of this line's energy.`
               : '',
      });

      const swTabs = [];
      if (exalted.length)   swTabs.push({ key: 'exalt', label: `Exalted (${exalted.length})`,       principles: exalted.map(toItem)   });
      if (detriment.length) swTabs.push({ key: 'det',   label: `Detriment (${detriment.length})`,   principles: detriment.map(toItem) });

      return [{
        key:    'sw',
        system: 'DIMENSION V · PLANETARY FIX',
        icon:   <span style={{ fontSize: 22, lineHeight: 1 }}>⚖</span>,
        name:   `${exalted.length} exalted · ${detriment.length} detriment`,
        axiom:  'Each line has a planet that turns smoothly (exalted) and one that creates friction (detriment). When your activation matches either, the line carries that built-in polarity.',
        tabs:   swTabs,
      }];
    })() : []),
  ];

  return (
    <div className="profile-page">

      {/* ── Layer 1: Zone Hero (today's frequency) ── */}
      <LuckyWindow profile={profile} onLocationChange={onLocationChange} />

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
