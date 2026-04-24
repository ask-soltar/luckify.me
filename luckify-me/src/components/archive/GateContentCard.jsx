/**
 * GateContentCard — archived Purpose Frame gate content
 *
 * Archived after removing Purpose Frame from the live Cmd layer.
 * Preserved here so the implementation can be referenced or restored later
 * without keeping it active in the current app navigation.
 */

import { useState } from 'react';
import { PURPOSE_GATES } from '../../constants/purposeGates.js';

const KIDS_STORAGE_KEY = 'luckify_kids_mode';

function useKidsMode() {
  const [kidsMode, setKidsMode] = useState(() => {
    try { return localStorage.getItem(KIDS_STORAGE_KEY) === 'true'; }
    catch { return false; }
  });

  function toggle() {
    setKidsMode(prev => {
      const next = !prev;
      try { localStorage.setItem(KIDS_STORAGE_KEY, String(next)); } catch {}
      return next;
    });
  }

  return [kidsMode, toggle];
}

const ADULT_FIELDS_BASE = [
  { key: 'expanded', label: null, variant: 'prose' },
  { key: 'at_the_table', label: 'AT THE TABLE', variant: 'prose' },
];

const ADULT_FIELDS_LINE = [
  ...ADULT_FIELDS_BASE,
  { key: 'edge', label: 'EDGE', variant: 'edge' },
  { key: 'blind_spot', label: 'BLIND SPOT', variant: 'risk' },
];

const KIDS_FIELDS = [
  { key: 'expanded', label: null, variant: 'prose' },
  { key: 'in_the_game', label: 'IN THE GAME', variant: 'prose' },
  { key: 'superpower', label: 'SUPERPOWER', variant: 'edge' },
  { key: 'kryptonite', label: 'KRYPTONITE', variant: 'risk' },
];

export function GateContentCard({ profile, geneKeys: geneKeysProp }) {
  const [open, setOpen] = useState(false);
  const [kidsMode, toggleKids] = useKidsMode();

  const { birthTime } = profile;
  const geneKeys = geneKeysProp || profile.geneKeys;
  if (!geneKeys?.purpose) return null;

  const { gate, line } = geneKeys.purpose;
  const gateData = PURPOSE_GATES[String(gate)];
  if (!gateData) return null;

  const hasBirthTime = Boolean(birthTime) && birthTime !== '00:00';
  const section = hasBirthTime ? gateData.lines[String(line)] : gateData.overall;
  if (!section) return null;

  const kidsSection = section.kids?.header ? section.kids : gateData.overall?.kids;
  const kidsAvailable = Boolean(kidsSection?.header);
  const effectiveKids = kidsMode && kidsAvailable;
  const content = effectiveKids ? kidsSection : section.adult;
  if (!content?.header) return null;

  const gateId = hasBirthTime ? `${gate}.${line}` : String(gate);
  const title1 = hasBirthTime ? (section.title1 || gateData.title1) : gateData.title1;
  const title2 = hasBirthTime ? section.title2 : gateData.title2;

  const fields = effectiveKids ? KIDS_FIELDS : (hasBirthTime ? ADULT_FIELDS_LINE : ADULT_FIELDS_BASE);

  return (
    <div className={`gate-card${open ? ' open' : ''}${effectiveKids ? ' kids' : ''}`}>
      <div className="gate-card-topbar">
        <div className="gate-card-click" onClick={() => setOpen(o => !o)}>
          <div className="gate-num-badge">{gateId}</div>
          <div className="gate-card-meta">
            <div className="gate-card-system">PURPOSE FRAME</div>
            <div className="gate-card-name">
              {title1}
              {title2 && <span className="gate-card-name-sub"> / {title2}</span>}
            </div>
          </div>
          <div className={`gate-chevron${open ? ' open' : ''}`}>▼</div>
        </div>

        <button
          className={`gate-kids-btn${effectiveKids ? ' active' : ''}${!kidsAvailable ? ' unavailable' : ''}`}
          onClick={() => kidsAvailable && toggleKids()}
          title={!kidsAvailable ? 'Kids content not yet available' : effectiveKids ? 'Switch to adult view' : 'Switch to kids view'}
          aria-pressed={effectiveKids}
          disabled={!kidsAvailable}
        >
          <span className="gate-kids-star">{effectiveKids ? '★' : '☆'}</span>
          <span className="gate-kids-label">KIDS</span>
        </button>
      </div>

      <div className="gate-hook" onClick={() => setOpen(o => !o)}>
        <p className="gate-hook-text">{content.header}</p>
        {!open && (
          <span className="gate-expand-hint">
            {open ? '' : 'EXPAND ▸'}
          </span>
        )}
      </div>

      {open && (
        <div className="gate-body">
          {fields.map(f => {
            const text = content[f.key];
            if (!text) return null;
            return (
              <div key={f.key} className={`gate-field gate-field--${f.variant}${f.label ? ' gate-field--labeled' : ''}`}>
                {f.label && <div className="gate-field-label">{f.label}</div>}
                <p className="gate-field-text">{text}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
