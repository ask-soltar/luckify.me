/**
 * CoreConfigCard — V1 Discovery Experience
 *
 * Open state:
 *   Reveal statement (stands alone)
 *   Recognition (soft subnote)
 *   Outcome (no label — large centered text)
 *   ── How This Works ▼ (expandable, numbered) ──
 *   ① What Comes Naturally…
 *   ② What Life Develops…
 *   ③ When These Work Together…
 *   ── ──
 *   ⚠ Watch For   🛠 Best Use (tool cards)
 */

import { useState } from 'react';

// Split "A, B, and C." → ["A.", "B.", "C."]
// Falls back to ["A.", "B."] for 2-part, or [full text] for single.
function parseBestUse(text) {
  if (!text) return [];

  // "A, B, and C[.]" — 3 beats
  const three = text.match(/^(.+?),\s+(.+?),\s+and\s+(.+?)\.?\s*$/i);
  if (three) {
    return [
      cap(three[1]) + '.',
      cap(three[2]) + '.',
      cap(three[3]) + '.',
    ];
  }

  // "A, and B[.]" — 2 beats
  const two = text.match(/^(.+?),\s+and\s+(.+?)\.?\s*$/i);
  if (two) {
    return [cap(two[1]) + '.', cap(two[2]) + '.'];
  }

  return [text];
}

function cap(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
}

const NUMBERED = ['①', '②', '③'];

export function CoreConfigCard({ icon, tithi, element, dynamic, lifePathNum, watchFor, bestUse }) {
  const [open,        setOpen]        = useState(false);
  const [detailsOpen, setDetailsOpen] = useState(false);

  const themeName  = dynamic?.configuration_theme_name;
  const revealText = dynamic?.reveal_statement;
  // Strip universal "You may have noticed " prefix — the label carries it
  const RAW_PREFIX = 'You may have noticed ';
  const recognRaw  = dynamic?.recognition_line || '';
  const recognBody = recognRaw.startsWith(RAW_PREFIX)
    ? cap(recognRaw.slice(RAW_PREFIX.length))
    : recognRaw;
  const metaLine   = [tithi?.functional_name, element?.functional_name].filter(Boolean).join(' · ');
  const bestUseBeats = parseBestUse(bestUse);

  const analyticalFields = [
    { key: 'naturally', label: 'What Comes Naturally to You\u2026',       body: tithi?.naturally_statement },
    { key: 'shapes',    label: 'What Life Seems to Develop in You\u2026',  body: element?.shapes_you_through },
    { key: 'pattern',   label: 'When These Work Together\u2026',           body: dynamic?.pattern_statement },
  ].filter(f => f.body);

  return (
    <div className={`dim-card core-config-card${open ? ' open' : ''}`}>

      {/* ── Header ── */}
      <div className="dim-card-header" onClick={() => setOpen(o => !o)}>
        <div className="dim-card-icon">{icon}</div>
        <div className="dim-card-titles">
          <div className="core-config-theme-name">{themeName || 'Core Configuration'}</div>
          {metaLine && <div className="core-config-meta-line">{metaLine}</div>}
        </div>
        <div className={`dim-card-chevron${open ? ' rotated' : ''}`}>▼</div>
      </div>

      {/* ── Body ── */}
      {open && (
        <div className="dim-card-body core-config-body">

          {/* Discovery block — reveal + recognition */}
          {(revealText || recognText) && (
            <div className="core-config-discovery">
              {revealText && <p className="core-config-reveal">{revealText}</p>}
              {recognBody && (
                <div className="core-config-recognition-wrap">
                  <span className="core-config-recognition-mark">✦</span>
                  <div>
                    <div className="core-config-recognition-label">You may have noticed&hellip;</div>
                    <p className="core-config-recognition">{recognBody}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Outcome — bridge line + anchor text */}
          {lifePathNum?.outcome && (
            <div className="core-config-field core-config-field--build">
              <div className="core-config-outcome-bridge">
                Because of this, you may be drawn to cultivate&hellip;
              </div>
              <div className="core-config-outcome">{lifePathNum.outcome}</div>
            </div>
          )}

          {/* How This Works — expandable, numbered */}
          {analyticalFields.length > 0 && (
            <div className="core-config-analysis-section">
              <button
                className={`core-config-analysis-toggle${detailsOpen ? ' open' : ''}`}
                onClick={() => setDetailsOpen(o => !o)}
              >
                <span>How This Works</span>
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

          {/* Tactical zone — Watch For + Best Use */}
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
