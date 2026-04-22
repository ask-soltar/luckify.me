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
import { AnimatePresence, motion } from 'framer-motion';
import { DimensionCard } from './DimensionCard.jsx';
import { CoreConfigCard } from './CoreConfigCard.jsx';
import { LuckyWindow } from './LuckyWindow.jsx';
import { GateContentCard } from './GateContentCard.jsx';
import PassiveSkillInlineCarousel from './PassiveSkillInlineCarousel.jsx';
import { TITHI_CCE, ELEMENT_CCE, LP_CCE, getDynamic, getHumanModeContent, generateWatchFor, generateBestUse } from '../constants/coreConfig.js';
import { GENE_KEYS } from '../constants/geneKeys.js';
import { PURPOSE_GATES } from '../constants/purposeGates.js';
import { PLANETARY_FIX } from '../constants/planetaryFix.js';
import { calcGeneKeys, calcAllActivations } from '../utils/geneKeys.js';
import { deriveHumanDesign } from '../utils/humanDesign.js';
import { getDecisionEnginePayload } from '../utils/decisionEngine.js';
import { getAuthorityLoadout } from '../constants/authorityLoadouts.js';

// Element color palette — grounded, permanent, different energy from zone colors
const ELEMENT_COLORS = {
  Wood:  { text: '#6ab87a', accent: 'rgba(30, 110, 50, 0.18)' },
  Fire:  { text: '#e06040', accent: 'rgba(130, 30, 10, 0.18)' },
  Earth: { text: '#c89840', accent: 'rgba(110, 78, 10, 0.18)' },
  Metal: { text: '#90b0cc', accent: 'rgba(40, 70, 110, 0.16)' },
  Water: { text: '#4880c8', accent: 'rgba(20, 55, 130, 0.18)' },
};

// ── Foundation Section — always visible, element-accented ──

function FoundationSection({
  element,
  lifePathNum,
  cceT,
  cceEl,
  cceLp,
  dynamic,
  humanModeContent,
  watchFor,
  bestUse,
  decisionEngine,
  passiveSkillLoadout,
  passiveSkillOpen,
  onTogglePassiveSkill,
  mode,
  showCore = true,
  showDecisionEngine = true,
  defaultCoreOpen = false,
}) {
  const elColor = ELEMENT_COLORS[element] || { text: 'var(--pip-primary)', accent: 'rgba(200,152,42,0.1)' };

  return (
    <div className="foundation-section" style={{ '--el-text': elColor.text, '--el-accent': elColor.accent }}>
      {/* Core Configuration card (Dims I + II + III) */}
      <div className="foundation-dimensions">
        {showCore && (
          <CoreConfigCard
            icon={<span style={{ fontSize: 22, lineHeight: 1 }}>◈</span>}
            tithi={cceT}
            element={cceEl}
            trajectoryElement={element}
            dynamic={dynamic}
            humanModeContent={humanModeContent}
            lifePathNum={cceLp}
            lifePathValue={lifePathNum}
            watchFor={watchFor}
            bestUse={bestUse}
            mode={mode}
            defaultOpen={defaultCoreOpen}
          />
        )}
        {showDecisionEngine && decisionEngine && passiveSkillLoadout && (
          <div className={`foundation-decision-engine-wrap foundation-decision-engine-wrap--${mode}`}>
            <button
              type="button"
              className={`foundation-decision-engine foundation-decision-engine--${mode}`}
              onClick={onTogglePassiveSkill}
            >
            <div className="foundation-decision-engine-label">
              {mode === 'operator' ? 'PASSIVE SKILLS' : 'Passive Skills'}
            </div>
            <div className="foundation-decision-engine-skill">
              {mode === 'operator' ? 'DECISION ENGINE' : 'Decision Engine'}
            </div>
            <div className="foundation-decision-engine-main">
              {decisionEngine.engineName}
            </div>
            <div className="foundation-decision-engine-meta">
              {decisionEngine.authorityType} <span className="foundation-decision-engine-sep">·</span> Always active
            </div>
            </button>
            <PassiveSkillInlineCarousel
              loadout={passiveSkillLoadout}
              open={passiveSkillOpen}
              onToggle={onTogglePassiveSkill}
            />
          </div>
        )}
      </div>
    </div>
  );
}

function PassiveSkillsSection({
  decisionEngine,
  passiveSkillLoadout,
  passiveSkillOpen,
  onTogglePassiveSkill,
}) {
  if (!decisionEngine || !passiveSkillLoadout) return null;

  return (
    <section className="profile-tab-panel profile-tab-panel--engine">
      <div className="profile-tab-panel-kicker">Decision Engine</div>
      <div className="profile-tab-panel-copy">
        Passive skills that shape how your choices move, settle, and become clear.
      </div>
      <div className="foundation-decision-engine-wrap foundation-decision-engine-wrap--human">
        <button
          type="button"
          className="foundation-decision-engine foundation-decision-engine--human"
          onClick={onTogglePassiveSkill}
        >
          <div className="foundation-decision-engine-label">Passive Skills</div>
          <div className="foundation-decision-engine-skill">Decision Engine</div>
          <div className="foundation-decision-engine-main">{decisionEngine.engineName}</div>
          <div className="foundation-decision-engine-meta">
            {decisionEngine.authorityType} <span className="foundation-decision-engine-sep">·</span> Always active
          </div>
        </button>
        <PassiveSkillInlineCarousel
          loadout={passiveSkillLoadout}
          open={passiveSkillOpen}
          onToggle={onTogglePassiveSkill}
        />
      </div>
    </section>
  );
}

function ActiveRhythmSection({
  profile,
  profileId,
  shouldAnimateRhythmReveal,
  humanDesign,
  onLocationChange,
}) {
  return (
    <section className="profile-tab-panel profile-tab-panel--active-rhythm">
      <div className="profile-tab-panel-kicker">Active Rhythm</div>
      <div className="profile-tab-panel-copy">
        Today&apos;s field, guidance, and monthly rhythm map.
      </div>
      <div className="profile-tab-rhythm-shell">
        <LuckyWindow
          profile={profile}
          profileId={profileId}
          shouldAnimateReveal={shouldAnimateRhythmReveal}
          humanDesign={humanDesign}
          onLocationChange={onLocationChange}
          mode="human"
          presentation="default"
          showModeToggle={false}
        />
      </div>
    </section>
  );
}

function CmdCoreLoadoutSection({
  element,
  lifePathNum,
  cceT,
  cceEl,
  cceLp,
  dynamic,
  humanModeContent,
  watchFor,
  bestUse,
}) {
  return (
    <section className="profile-tab-panel profile-tab-panel--cmd-anchor">
      <div className="profile-tab-panel-kicker profile-tab-panel-kicker--cmd">Cmd Core Loadout</div>
      <div className="profile-tab-panel-copy profile-tab-panel-copy--cmd">
        Structural readout for the current build before entering experimental modules.
      </div>
      <div className="profile-tab-cmd-anchor">
        <CoreConfigCard
          icon={<span style={{ fontSize: 22, lineHeight: 1 }}>◈</span>}
          tithi={cceT}
          element={cceEl}
          trajectoryElement={element}
          dynamic={dynamic}
          humanModeContent={humanModeContent}
          lifePathNum={cceLp}
          lifePathValue={lifePathNum}
          watchFor={watchFor}
          bestUse={bestUse}
          mode="operator"
          defaultOpen
        />
      </div>
    </section>
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

export function ProfileDisplay({
  profile,
  profileId = null,
  shouldAnimateRhythmReveal = false,
  onResetRhythmReveal,
  onLocationChange
}) {
  const { type, element, lifePathNum, birthTime } = profile;
  const [activeTab, setActiveTab] = useState('loadout');
  const [passiveSkillOpen, setPassiveSkillOpen] = useState(false);

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
    const { y, mo, dy, birthTime: bt, birthGMT, birthLat, birthLng } = profile;
    if (!y || !mo || !dy) return null;
    try {
      return calcAllActivations({
        year: y,
        month: mo,
        day: dy,
        birthTime: bt || '12:00',
        tzOffset: birthGMT ?? 0,
        latitude: birthLat,
        longitude: birthLng,
      });
    } catch { return null; }
  }, [profile]);
  const humanDesign = useMemo(() => {
    if (!activations?.length) return profile.humanDesign || null;
    try {
      return deriveHumanDesign(activations);
    } catch {
      return profile.humanDesign || null;
    }
  }, [activations, profile.humanDesign]);
  const decisionEngine = useMemo(() => {
    if (!humanDesign?.authority) return null;
    return getDecisionEnginePayload(humanDesign.authority);
  }, [humanDesign]);
  const passiveSkillLoadout = useMemo(() => {
    if (!humanDesign?.authority) return null;
    return getAuthorityLoadout(humanDesign.authority);
  }, [humanDesign]);
  const activationAuditItems = useMemo(() => {
    if (!activations?.length) return [];

    return activations.map(a => ({
      title: `${a.chart === 'conscious' ? 'Conscious' : 'Design'} · ${a.planet}`,
      body: `Gate ${a.gate}.${a.line}`,
    }));
  }, [activations]);
  const hasBirthTime = Boolean(birthTime) && birthTime !== '00:00';

  // ── Core Configuration Engine lookups ──────────────
  const cceT       = TITHI_CCE[type];
  const cceEl      = ELEMENT_CCE[element];
  const cceLp      = LP_CCE[lifePathNum];
  const dynamic    = getDynamic(type, element);
  const humanModeContent = getHumanModeContent(type, element, lifePathNum);
  // Per-entry content takes priority; generated formulas are fallback only
  const watchFor   = humanModeContent?.watchForDrift || humanModeContent?.baseWatchForDrift || dynamic?.watch_for || generateWatchFor(type, element, lifePathNum);
  const bestUse    = humanModeContent?.bestUse || dynamic?.best_use || generateBestUse(type, element, lifePathNum);
  const coreCardProps = {
    element,
    lifePathNum,
    cceT,
    cceEl,
    cceLp,
    dynamic,
    humanModeContent,
    watchFor,
    bestUse,
  };

  // ── Dimension config array — IV and V only ─────────
  // Dims I/II/III are handled by CoreConfigCard above.
  const dimensions = [
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
    // For each of the 26 activations, look up the gate.line in the 384-line fix table.
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

      const toItem = a => {
        const pg      = PURPOSE_GATES[String(a.gate)];
        const section = pg?.lines?.[String(a.line)]?.adult ?? pg?.overall?.adult ?? null;
        const field   = a.polarity === 'exalt' ? 'edge' : 'blind_spot';
        const body    = section?.[field] ?? null;
        return {
          title: `${a.symbol} ${a.planet}  ${chartLabel(a.chart)} · Gate ${a.gate}.${a.line}`,
          body:  body || '',
        };
      };

      const swTabs = [];
      if (exalted.length)   swTabs.push({ key: 'exalt', label: `Exalted (${exalted.length})`,       principles: exalted.map(toItem)   });
      if (detriment.length) swTabs.push({ key: 'det',   label: `Detriment (${detriment.length})`,   principles: detriment.map(toItem) });

      return [{
        key:    'sw',
        system: 'DIMENSION V · PLANETARY FIX',
        icon:   <span style={{ fontSize: 22, lineHeight: 1 }}>⚖</span>,
        name:   `${exalted.length} exalted · ${detriment.length} detriment`,
        axiom:  'Each line has a planet that turns smoothly (exalted) and one that creates friction (detriment). When one of your chart activations matches either, the line carries that built-in polarity.',
        tabs:   swTabs,
      }];
    })() : []),

    ...(humanDesign ? [{
      key: 'authority',
      system: 'DIMENSION V · HUMAN DESIGN',
      icon: <span style={{ fontSize: 22, lineHeight: 1 }}>◎</span>,
      name: decisionEngine?.engineName || humanDesign.authority,
      axiom: decisionEngine?.essenceLine || 'Authority is derived from fully defined channels first, then defined centers, then standard Human Design type and authority hierarchy. If Solar Plexus is defined, authority is Emotional before any lower authority is considered.',
      tabs: [
        ...(decisionEngine ? [{
          key: 'decision-engine',
          label: 'Decision Engine',
          principles: [
            {
              title: `${decisionEngine.engineName} · ${decisionEngine.authorityType}`,
              body: `${decisionEngine.microTag} · ${decisionEngine.coreInstruction}`,
            },
            {
              title: decisionEngine.recognitionTitle,
              body: decisionEngine.recognitionText,
            },
            {
              title: decisionEngine.supportTitle,
              body: decisionEngine.supportText,
            },
            {
              title: decisionEngine.expansionTitle,
              body: decisionEngine.expansionText,
            },
            {
              title: 'Icon Direction',
              body: decisionEngine.iconDirection.join(' · '),
            },
            {
              title: 'Keywords',
              body: decisionEngine.keywords.join(' · '),
            },
          ],
        }] : []),
        {
          key: 'overview',
          label: 'Overview',
          principles: [
            {
              title: 'Authority Type',
              body: `${humanDesign.authority} · ${humanDesign.type}`,
            },
            {
              title: 'Defined Centers',
              body: humanDesign.definedCenterLabels?.length
                ? humanDesign.definedCenterLabels.join(' · ')
                : 'None defined',
            },
            {
              title: 'Defined Channels',
              body: humanDesign.definedChannels?.length
                ? humanDesign.definedChannels
                    .map(channel => `${channel.key} (${channel.centers.join(' ↔ ')})`)
                    .join(' · ')
                : 'No fully defined channels',
            },
            {
              title: 'Active Gates',
              body: humanDesign.activeGates?.length
                ? humanDesign.activeGates.join(' · ')
                : 'No active gates',
            },
          ],
        },
        {
          key: 'activations',
          label: `Activations (${activationAuditItems.length})`,
          principles: activationAuditItems,
        },
      ],
    }] : []),
  ];

  return (
    <div className={`profile-page profile-page--${activeTab}`}>
      <div className="profile-tab-shell">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            className={`profile-tab-view profile-tab-view--${activeTab}`}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}
          >
            {activeTab === 'loadout' && (
              <FoundationSection
                {...coreCardProps}
                decisionEngine={decisionEngine}
                passiveSkillLoadout={passiveSkillLoadout}
                passiveSkillOpen={passiveSkillOpen}
                onTogglePassiveSkill={() => setPassiveSkillOpen(open => !open)}
                mode="human"
                showDecisionEngine={false}
                defaultCoreOpen
              />
            )}

            {activeTab === 'engine' && (
              <>
                <ActiveRhythmSection
                  profile={profile}
                  profileId={profileId}
                  shouldAnimateRhythmReveal={shouldAnimateRhythmReveal}
                  humanDesign={humanDesign}
                  onLocationChange={onLocationChange}
                />
                <PassiveSkillsSection
                  decisionEngine={decisionEngine}
                  passiveSkillLoadout={passiveSkillLoadout}
                  passiveSkillOpen={passiveSkillOpen}
                  onTogglePassiveSkill={() => setPassiveSkillOpen(open => !open)}
                />
              </>
            )}

            {activeTab === 'cmd' && (
              <>
                <CmdCoreLoadoutSection {...coreCardProps} />
                <div className="profile-exploration-panel profile-exploration-panel--cmd">
                  <div className="profile-exploration-label">Experimental Layer</div>
                  <div className="profile-exploration-copy">
                    Exploratory tools for play, pattern testing, and live interpretation.
                  </div>

                  <div className="profile-exploration-controls">
                    <button
                      type="button"
                      className="profile-exploration-reset"
                      onClick={() => onResetRhythmReveal?.()}
                      disabled={!profileId}
                    >
                      Reset Rhythm Reveal
                    </button>
                  </div>

                  <div className="profile-exploration-stack">
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
                    {geneKeys?.purpose && (
                      <GateContentCard profile={profile} geneKeys={geneKeys} />
                    )}
                  </div>
                </div>
              </>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      <nav className="profile-bottom-nav" aria-label="Primary profile navigation">
        <button
          type="button"
          className={`profile-bottom-nav-item${activeTab === 'loadout' ? ' active' : ''}`}
          onClick={() => setActiveTab('loadout')}
        >
          <span className="profile-bottom-nav-label">Loadout</span>
        </button>
        <button
          type="button"
          className={`profile-bottom-nav-item${activeTab === 'engine' ? ' active' : ''}`}
          onClick={() => setActiveTab('engine')}
        >
          <span className="profile-bottom-nav-label">Engine</span>
        </button>
        <button
          type="button"
          className={`profile-bottom-nav-item${activeTab === 'cmd' ? ' active' : ''}`}
          onClick={() => setActiveTab('cmd')}
        >
          <span className="profile-bottom-nav-label">Cmd</span>
        </button>
      </nav>
    </div>
  );
}
