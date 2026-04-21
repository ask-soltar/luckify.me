/**
 * CoreConfigCard — Foundation Engine V2
 *
 * Two top-level modes controlled from the shared profile toggle:
 *   Human     — "Core Loadout"       — intuitive / discovery
 *   Operator  — "Core Configuration" — diagnostic / systemic / debug
 *
 * Standard body:
 *   You're naturally wired to… [reveal statement]
 *   You may recognize this as… [recognition]
 *   This may be helping you build toward… [human LP outcome]
 *   ▼ Loadout Mechanics (expandable)
 *   ⚠ Watch For  🛠 Best Use
 *
 * Operator body:
 *   Dynamic Pattern   [operator_dynamic_pattern]
 *   Recognition Signal [recognition_signal_operator]
 *   Directional Vector [directional_vector]
 *   Directional Outcome [operator life path outcome]
 *   ▼ Configuration Logic (expandable)
 *   Failure Mode
 *   Optimization Path
 */

import { useState } from 'react';
import { FoundationGlyph } from './foundation/foundationGlyphs';
import { LifePathCrest } from './foundation/lifePathCrests';

function parseBestUse(text) {
  if (!text) return [];
  if (Array.isArray(text)) return text.filter(Boolean);
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
const PROTOCOL_NUMBERS = ['01', '02', '03'];

function FoundationGlyphBadge({ glyph, mode, title, fallback }) {
  return (
    <div className={`core-config-glyph-badge core-config-glyph-badge--${mode}`}>
      {glyph ? (
        <FoundationGlyph
          glyph={glyph}
          mode={mode}
          size={mode === 'operator' ? 38 : 32}
          title={title}
          className="core-config-glyph"
          animated={mode === 'operator'}
          strokeWidth={mode === 'operator' ? 1.35 : 1.6}
        />
      ) : fallback}
    </div>
  );
}

export function CoreConfigCard({ icon, tithi, element, dynamic, humanModeContent = null, lifePathNum, lifePathValue, watchFor, bestUse, mode = 'human' }) {
  const [open,        setOpen]        = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [exploreOpen, setExploreOpen] = useState(false);
  const isOperator = mode === 'operator';

  const themeName = dynamic?.configuration_theme_name;
  const metaLine  = [tithi?.functional_name, element?.functional_name].filter(Boolean).join(' · ');

  // Recognition — mode-specific
  const recognBody   = humanModeContent?.recognition || dynamic?.recognition_line_simple || null;
  const recognSignal = dynamic?.recognition_signal_operator || null;

  // Standard mode reveal: stem + lp tail
  const stdReveal = humanModeContent?.reveal
    || dynamic?.human_reveal_statement
    || (dynamic?.simple_reveal_stem ? cap(dynamic.simple_reveal_stem) : null)
    || lifePathNum?.lp_tail
    || null;

  // Operator mode fields
  const opDynPattern  = dynamic?.operator_dynamic_pattern;
  const opDirVector   = lifePathNum?.directional_vector;
  const opOutcome     = lifePathNum?.operator_outcome_name || lifePathNum?.outcome;
  const humanOutcome  = humanModeContent?.orientation || lifePathNum?.human_outcome_name || lifePathNum?.outcome;

  // Expandable fields — differ by mode
  const analyticalFields = isOperator
    ? [
        { key: 'natural',  label: 'Natural Expression',          body: dynamic?.operator_natural_expression },
        { key: 'pressure', label: 'Developmental Pressure',      body: dynamic?.operator_developmental_pressure },
        { key: 'emergent', label: 'Emergent Pattern',            body: dynamic?.operator_emergent_pattern },
      ].filter(f => f.body)
    : [
        { key: 'natural',  label: 'What comes naturally\u2026',  body: humanModeContent?.howYouNaturallyOperate || dynamic?.simple_natural_expression },
        { key: 'teaches',  label: 'What life teaches you\u2026', body: humanModeContent?.whatLifeTeachesYou || dynamic?.simple_developmental_force },
      ].filter(f => f.body);

  const bestUseBeats = parseBestUse(bestUse);
  const expandLabel  = isOperator ? 'Configuration Logic' : 'Loadout Mechanics';
  const operatorFailureMode = dynamic?.failure_mode_operator || null;
  const operatorOptimizationSteps = [
    dynamic?.optimization_step_1_operator,
    dynamic?.optimization_step_2_operator,
    dynamic?.optimization_step_3_operator,
  ].filter(Boolean);
  const systemLabel = isOperator ? 'CORE CONFIGURATION' : 'Core Loadout';
  const themeTitle = isOperator
    ? `CONFIGURATION: ${(themeName || 'Core Configuration').replace(/^The\s+/i, '').toUpperCase()}`
    : (themeName || 'Core Configuration');
  const expandBracketLabel = isOperator ? '[ CONFIGURATION LOGIC ]' : 'Loadout Mechanics';

  return (
    <div className={`dim-card core-config-card${open ? ' open' : ''} core-config-card--${mode}`}>

      {/* ── Header ── */}
      <div className={`dim-card-header core-config-header core-config-header--${mode}`} onClick={() => setOpen(o => !o)}>
        <div className="dim-card-icon core-config-glyph-wrap">
          <FoundationGlyphBadge glyph={themeName} mode={mode} title={themeName} fallback={icon} />
        </div>
        <div className="dim-card-titles">
          <div className="core-config-system-label">
            {systemLabel}
          </div>
          <div className="core-config-theme-name">{themeTitle}</div>
          {metaLine && <div className="core-config-meta-line">{metaLine}</div>}
        </div>
        <div className="core-config-header-right">
          <div className={`dim-card-chevron${open ? ' rotated' : ''}`}>▼</div>
        </div>
      </div>

      {/* ── Body ── */}
      {open && (
        <div className="dim-card-body core-config-body">

          {/* ── Standard mode top block ── */}
          {!isOperator && stdReveal && (
            <div className="core-config-std-reveal-block">
              <div className="core-config-std-reveal-label">You&rsquo;re naturally wired to&hellip;</div>
              <p className="core-config-std-reveal">{stdReveal}</p>
            </div>
          )}

          {/* ── Recognition — mode-specific ── */}
          {!isOperator && recognBody && (
            <div className="core-config-recognition-wrap">
              <div className="core-config-recognition-head">
                <span className="core-config-recognition-mark">✦</span>
                <div className="core-config-recognition-label">You may recognize this as&hellip;</div>
              </div>
              <p className="core-config-recognition">{recognBody}</p>
            </div>
          )}
          {/* ── Operator mode diagnostic blocks ── */}
          {isOperator && (opDynPattern || recognSignal || opDirVector) && (
            <div className="core-config-op-blocks">
              {opDynPattern && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">DYNAMIC PATTERN</div>
                  <p className="core-config-op-value">{opDynPattern}</p>
                </div>
              )}
              {recognSignal && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">RECOGNITION SIGNAL</div>
                  <p className="core-config-op-value">{recognSignal}</p>
                </div>
              )}
              {opDirVector && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">DIRECTIONAL VECTOR</div>
                  <p className="core-config-op-value">{opDirVector}</p>
                </div>
              )}
              {opOutcome && (
                <div className="core-config-op-block">
                  <div className="core-config-op-label">DIRECTIONAL OUTCOME</div>
                  <p className="core-config-op-value core-config-op-value--outcome">{opOutcome}</p>
                </div>
              )}
            </div>
          )}

          {/* ── Outcome bridge — standard only ── */}
          {!isOperator && humanOutcome && (
            <div className="core-config-field core-config-field--build">
              <div className="core-config-outcome-shell">
                <div className="core-config-outcome-crest">
                  <LifePathCrest
                    lifePath={lifePathValue}
                    mode="human"
                    size={92}
                    className="core-config-life-path-crest"
                    title={humanOutcome ? `${humanOutcome} crest` : 'Life Path crest'}
                  />
                </div>
                <div className="core-config-outcome-copy">
                  <div className="core-config-outcome-bridge">
                    This may be helping you build toward&hellip;
                  </div>
                  <div className="core-config-outcome">{humanOutcome}</div>
                </div>
              </div>
            </div>
          )}

          {/* ── Expandable mechanics / logic ── */}
          {isOperator && analyticalFields.length > 0 && (
            <div className="core-config-analysis-section">
              <button
                className={`core-config-analysis-toggle${detailsOpen ? ' open' : ''}`}
                onClick={() => setDetailsOpen(o => !o)}
              >
                <span>{isOperator ? expandBracketLabel : expandLabel}</span>
                <span className={`core-config-analysis-chevron${detailsOpen ? ' rotated' : ''}`}>▼</span>
              </button>

              {detailsOpen && analyticalFields.map((f, i) => (
                <div key={f.key} className={`core-config-field core-config-field--${f.key}`}>
                  <div className={`core-config-label${isOperator ? ' core-config-label--operator' : ''}`}>
                    {!isOperator && <span className="core-config-field-num">{NUMBERED[i]}</span>}
                    {isOperator ? f.label.toUpperCase() : f.label}
                  </div>
                  <div className="core-config-value">{f.body}</div>
                </div>
              ))}
            </div>
          )}

          {!isOperator && (analyticalFields.length > 0 || watchFor || bestUseBeats.length > 0) && (
            <div className="core-config-guidance">
              <div className="core-config-guidance-intro">
                Here&rsquo;s how to work with this in real life
              </div>
              <button
                className={`core-config-guidance-toggle${exploreOpen ? ' open' : ''}`}
                onClick={() => setExploreOpen(o => !o)}
              >
                <span>Explore Your Loadout</span>
                <span className={`core-config-guidance-chevron${exploreOpen ? ' rotated' : ''}`}>▼</span>
              </button>

              {exploreOpen && (
                <div className="core-config-guidance-body">
                  {analyticalFields.length > 0 && (
                    <div className="core-config-guidance-panel core-config-guidance-panel--operate">
                      <div className="core-config-guidance-label">How You Naturally Operate</div>
                      <div className="core-config-guidance-copy">
                        {analyticalFields.map((f, i) => (
                          <div key={f.key} className="core-config-guidance-row">
                            <div className="core-config-guidance-row-label">
                              <span className="core-config-field-num">{NUMBERED[i]}</span>
                              {f.label}
                            </div>
                            <div className="core-config-value">{f.body}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {watchFor && (
                    <div className="core-config-guidance-panel core-config-guidance-panel--drift">
                      <div className="core-config-guidance-label">Watch For Drift</div>
                      <div className="core-config-tactical-body">{watchFor}</div>
                    </div>
                  )}

                  {bestUseBeats.length > 0 && (
                    <div className="core-config-guidance-panel core-config-guidance-panel--best-use">
                      <div className="core-config-guidance-label">Best Use</div>
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

          {isOperator && (operatorFailureMode || operatorOptimizationSteps.length > 0) && (
            <div className="core-config-tactical core-config-tactical--operator">
              {operatorFailureMode && (
                <div className="core-config-tactical-item core-config-tactical--failure">
                  <div className="core-config-tactical-label">FAILURE MODE</div>
                  <div className="core-config-tactical-body">{operatorFailureMode}</div>
                </div>
              )}
              {operatorOptimizationSteps.length > 0 && (
                <div className="core-config-tactical-item core-config-tactical--optimization">
                  <div className="core-config-tactical-label">OPTIMIZATION PATH</div>
                  <div className="core-config-protocol-list">
                    {operatorOptimizationSteps.map((step, i) => (
                      <div key={i} className="core-config-protocol-step">
                        <span className="core-config-protocol-num">[{PROTOCOL_NUMBERS[i] || String(i + 1).padStart(2, '0')}]</span>
                        <span className="core-config-protocol-text">{step}</span>
                      </div>
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
