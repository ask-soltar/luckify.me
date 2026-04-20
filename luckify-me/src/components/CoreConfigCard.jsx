/**
 * CoreConfigCard — Foundation Engine V2
 *
 * Two top-level modes toggled from the card header:
 *   Standard  — "Core Loadout"       — human / intuitive / discovery
 *   Operator  — "Core Configuration" — diagnostic / systemic / debug
 *
 * Standard body:
 *   You're naturally wired to… [stem + lp tail]
 *   ✦ You may have noticed… [recognition]
 *   Because of this… [outcome bridge + LP outcome]
 *   ▼ Loadout Mechanics (expandable)
 *   ⚠ Watch For  🛠 Best Use
 *
 * Operator body:
 *   Dynamic Pattern   [operator_dynamic_pattern]
 *   Directional Vector [directional_vector]
 *   ✦ You may have noticed… [recognition]
 *   Because of this… [outcome bridge + LP outcome]
 *   ▼ Configuration Logic (expandable)
 *   ⚠ Watch For  🛠 Best Use
 */

import { useState } from 'react';

function parseBestUse(text) {
  if (!text) return [];
  const three = text.match(/^(.+?),\s+(.+?),\s+and\s+(.+?)\.?\s*$/i);
  if (three) return [cap(three[1]) + '.', cap(three[2]) + '.', cap(three[3]) + '.'];
  const two = text.match(/^(.+?),\s+and\s+(.+?)\.?\s*$/i);
  if (two) return [cap(two[1]) + '.', cap(two[2]) + '.'];
  return [text];
}

function cap(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
}

const NUMBERED = ['①', '②', '③'];
const RAW_PREFIX = 'You may have noticed ';

export function CoreConfigCard({ icon, tithi, element, dynamic, lifePathNum, watchFor, bestUse }) {
  const [open,        setOpen]        = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [mode,        setMode]        = useState('standard'); // 'standard' | 'operator'

  const themeName = dynamic?.configuration_theme_name;
  const metaLine  = [tithi?.functional_name, element?.functional_name].filter(Boolean).join(' · ');

  // Recognition — shared across modes
  const recognRaw  = dynamic?.recognition_line || '';
  const recognBody = recognRaw.startsWith(RAW_PREFIX)
    ? cap(recognRaw.slice(RAW_PREFIX.length))
    : recognRaw;

  // Standard mode reveal: stem + lp tail
  const stem   = dynamic?.simple_reveal_stem;
  const lpTail = lifePathNum?.lp_tail;
  const stdReveal = stem && lpTail
    ? `${cap(stem)} ${lpTail}`
    : stem || lpTail || null;

  // Operator mode fields
  const opDynPattern  = dynamic?.operator_dynamic_pattern;
  const opDirVector   = lifePathNum?.directional_vector;

  // Expandable fields — differ by mode
  const analyticalFields = mode === 'standard'
    ? [
        { key: 'natural',  label: 'What comes naturally\u2026',  body: dynamic?.simple_natural_expression },
        { key: 'teaches',  label: 'What life teaches you\u2026', body: dynamic?.simple_developmental_force },
        { key: 'shows',    label: 'How it shows up\u2026',       body: dynamic?.simple_pattern_statement },
      ].filter(f => f.body)
    : [
        { key: 'natural',  label: 'Natural Expression',          body: dynamic?.operator_natural_expression },
        { key: 'pressure', label: 'Developmental Pressure',      body: dynamic?.operator_developmental_pressure },
        { key: 'emergent', label: 'Emergent Pattern',            body: dynamic?.operator_emergent_pattern },
      ].filter(f => f.body);

  const bestUseBeats = parseBestUse(bestUse);
  const expandLabel  = mode === 'standard' ? 'Loadout Mechanics' : 'Configuration Logic';

  return (
    <div className={`dim-card core-config-card${open ? ' open' : ''} core-config-card--${mode}`}>

      {/* ── Header ── */}
      <div className="dim-card-header" onClick={() => setOpen(o => !o)}>
        <div className="dim-card-icon">{icon}</div>
        <div className="dim-card-titles">
          <div className="core-config-system-label">
            {mode === 'standard' ? 'CORE LOADOUT' : 'CORE CONFIGURATION'}
          </div>
          <div className="core-config-theme-name">{themeName || 'Core Configuration'}</div>
          {metaLine && <div className="core-config-meta-line">{metaLine}</div>}
        </div>
        <div className="core-config-header-right">
          <div
            className="core-config-header-toggle"
            onClick={e => { e.stopPropagation(); setMode(m => m === 'standard' ? 'operator' : 'standard'); }}
          >
            <span className={mode === 'standard' ? 'active' : ''}>STD</span>
            <span className={mode === 'operator' ? 'active' : ''}>OPR</span>
          </div>
          <div className={`dim-card-chevron${open ? ' rotated' : ''}`}>▼</div>
        </div>
      </div>

      {/* ── Body ── */}
      {open && (
        <div className="dim-card-body core-config-body">

          {/* ── Standard mode top block ── */}
          {mode === 'standard' && stdReveal && (
            <div className="core-config-std-reveal-block">
              <div className="core-config-std-reveal-label">You&rsquo;re naturally wired to&hellip;</div>
              <p className="core-config-std-reveal">{stdReveal}</p>
            </div>
          )}

          {/* ── Operator mode top blocks ── */}
          {mode === 'operator' && (opDynPattern || opDirVector) && (
            <div className="core-config-op-blocks">
              {opDynPattern && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">Dynamic Pattern</div>
                  <p className="core-config-op-value">{opDynPattern}</p>
                </div>
              )}
              {opDirVector && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">Directional Vector</div>
                  <p className="core-config-op-value">{opDirVector}</p>
                </div>
              )}
            </div>
          )}

          {/* ── Recognition — shared ── */}
          {recognBody && (
            <div className="core-config-recognition-wrap">
              <span className="core-config-recognition-mark">✦</span>
              <div>
                <div className="core-config-recognition-label">You may have noticed&hellip;</div>
                <p className="core-config-recognition">{recognBody}</p>
              </div>
            </div>
          )}

          {/* ── Outcome bridge — shared ── */}
          {lifePathNum?.outcome && (
            <div className="core-config-field core-config-field--build">
              <div className="core-config-outcome-bridge">
                Because of this, you may be drawn to cultivate&hellip;
              </div>
              <div className="core-config-outcome">{lifePathNum.outcome}</div>
            </div>
          )}

          {/* ── Expandable mechanics / logic ── */}
          {analyticalFields.length > 0 && (
            <div className="core-config-analysis-section">
              <button
                className={`core-config-analysis-toggle${detailsOpen ? ' open' : ''}`}
                onClick={() => setDetailsOpen(o => !o)}
              >
                <span>{expandLabel}</span>
                <span className={`core-config-analysis-chevron${detailsOpen ? ' rotated' : ''}`}>▼</span>
              </button>

              {detailsOpen && analyticalFields.map((f, i) => (
                <div key={f.key} className={`core-config-field core-config-field--${f.key}`}>
                  <div className="core-config-label">
                    <span className="core-config-field-num">{NUMBERED[i]}</span>
                    {f.label}
                  </div>
                  <div className="core-config-value">{f.body}</div>
                </div>
              ))}
            </div>
          )}

          {/* ── Tactical zone — Watch For + Best Use ── */}
          {(watchFor || bestUseBeats.length > 0) && (
            <div className="core-config-tactical">
              {watchFor && (
                <div className="core-config-tactical-item core-config-tactical--watchfor">
                  <div className="core-config-tactical-label">
                    <span className="core-config-tactical-icon">⚠</span>
                    Watch For
                  </div>
                  <div className="core-config-tactical-body">{watchFor}</div>
                </div>
              )}
              {bestUseBeats.length > 0 && (
                <div className="core-config-tactical-item core-config-tactical--bestuse">
                  <div className="core-config-tactical-label">
                    <span className="core-config-tactical-icon">🛠</span>
                    Best Use
                  </div>
                  <div className="core-config-tactical-beats">
                    {bestUseBeats.map((beat, i) => (
                      <div key={i} className="core-config-beat">{beat}</div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

        </div>
      )}
    </div>
  );
}
