/**
 * RhythmCalendar — Monthly color rhythm calendar
 * Matches the old Project Soltar 30-day forecast + luckify-app.html detail sheet.
 * Day detail popup shows: zone tagline, category score bars (Action/Strategy/etc.),
 * guidance text per category, plus stats grid and mantra.
 */

import { useState, useMemo } from 'react';
import { calcLuckyWindow } from '../utils/luckyWindow.js';
import { getZoneScores, GUIDANCE, CELL_LINE, CAT_EMOJI } from '../constants/zoneScoring.js';

const DOW = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

const MONTH_NAMES = [
  'January','February','March','April','May','June',
  'July','August','September','October','November','December'
];

function buildMonthData(year, month, birthDate, birthTime, birthGMT, eventGMT) {
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const firstDow    = new Date(year, month, 1).getDay();
  const today       = new Date();
  const todayKey    = `${today.getFullYear()}-${today.getMonth()}-${today.getDate()}`;

  const cells = [];
  for (let i = 0; i < firstDow; i++) cells.push(null);

  for (let d = 1; d <= daysInMonth; d++) {
    const date    = new Date(year, month, d);
    const dateKey = `${year}-${month}-${d}`;
    let zone = 'Yellow', delta = 0, band = '', mantra = '',
        total = 0, edge50 = 0, stability = '', dom_person = '', dom_env = '';

    try {
      const r = calcLuckyWindow({
        birthDate,
        birthTime:  birthTime || '12:00',
        birthGMT:   birthGMT  ?? 0,
        eventDate:  date,
        eventGMT:   eventGMT  ?? birthGMT ?? 0
      });
      zone       = r.zone;
      delta      = r.delta;
      band       = r.band;
      mantra     = r.mantra;
      total      = r.total;
      edge50     = r.edge50;
      stability  = r.stability;
      dom_person = r.dom_person;
      dom_env    = r.dom_env;
    } catch (e) { /* keep defaults */ }

    cells.push({ day: d, date, dateKey, isToday: dateKey === todayKey,
                 zone, delta, band, mantra, total, edge50, stability, dom_person, dom_env });
  }

  return cells;
}

function CategoryBar({ cat, normalized, textColor, guidance }) {
  const pct = normalized * 10; // normalized is 0–10, bar width is 0–100%
  return (
    <div className="cat-score-row">
      <span className="cat-score-emoji">{CAT_EMOJI[cat] || '·'}</span>
      <span className="cat-score-name" style={{ color: textColor }}>{cat}</span>
      <div className="cat-score-bar-wrap">
        <div
          className="cat-score-bar"
          style={{ width: `${pct}%`, background: textColor }}
        />
      </div>
      <span className="cat-score-val" style={{ color: textColor }}>{normalized.toFixed(1)}</span>
      <span className="cat-score-guide" style={{ color: textColor }}>{guidance}</span>
    </div>
  );
}

function DayDetail({ day, profile, onClose, embedded = false }) {
  if (!day) return null;

  const zoneLower  = day.zone?.toLowerCase();
  const textColor  = `var(--${zoneLower}-text, #eee)`;
  const tc         = () => ({ color: textColor });
  const deltaSign  = day.delta >= 0 ? '+' : '';
  const edgeSign   = day.edge50 >= 0 ? '+' : '';
  const scores     = getZoneScores(day.zone);
  const guidance   = GUIDANCE[day.zone] || {};
  const tagline    = CELL_LINE[day.zone] || '';

  const detailContent = (
    <>
      {!embedded && <div className="cal-detail-handle" />}

      {/* Date */}
      <div className="cal-detail-date">
        {day.date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
      </div>

      {/* Zone name + tagline */}
      <div className="cal-detail-zone" style={tc()}>{day.zone}</div>
      {tagline && (
        <div className="cal-detail-tagline" style={tc()}>{tagline}</div>
      )}

      {/* Category score bars */}
      {scores.length > 0 && (
        <div className="cat-score-rows">
          {scores.map(({ cat, normalized }) => (
            <CategoryBar
              key={cat}
              cat={cat}
              normalized={normalized}
              textColor={textColor}
              guidance={guidance[cat] || ''}
            />
          ))}
        </div>
      )}

      {/* Stats grid */}
      <div className="cal-detail-stats">
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">SCORE</div>
          <div className="cal-detail-stat-val" style={tc()}>{day.total}</div>
        </div>
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">DELTA</div>
          <div className="cal-detail-stat-val" style={tc()}>{deltaSign}{day.delta}</div>
        </div>
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">EDGE</div>
          <div className="cal-detail-stat-val" style={tc()}>{edgeSign}{day.edge50}</div>
        </div>
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">STABILITY</div>
          <div className="cal-detail-stat-val cal-detail-stat-sm" style={tc()}>{day.stability}</div>
        </div>
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">PERSON EL</div>
          <div className="cal-detail-stat-val cal-detail-stat-sm" style={tc()}>{day.dom_person}</div>
        </div>
        <div className="cal-detail-stat">
          <div className="cal-detail-stat-label">ENV EL</div>
          <div className="cal-detail-stat-val cal-detail-stat-sm" style={tc()}>{day.dom_env}</div>
        </div>
      </div>

      {/* Mantra */}
      <div className="cal-detail-mantra" style={tc()}>
        "{day.mantra}"
      </div>

      <button className="pip-button cal-detail-close" onClick={onClose}>Close</button>
    </>
  );

  if (embedded) {
    return (
      <div
        className="cal-detail-inline"
        style={{ background: `var(--${zoneLower}-bg, #111)` }}
      >
        {detailContent}
      </div>
    );
  }

  return (
    <div className="cal-detail-overlay open" onClick={onClose}>
      <div
        className="cal-detail-sheet"
        style={{ background: `var(--${zoneLower}-bg, #111)` }}
        onClick={e => e.stopPropagation()}
      >
        {detailContent}
      </div>
    </div>
  );
}

export function RhythmCalendar({ profile, embedded = false }) {
  const now = new Date();
  const [open, setOpen]           = useState(false);
  const [viewYear, setViewYear]   = useState(now.getFullYear());
  const [viewMonth, setViewMonth] = useState(now.getMonth());
  const [selected, setSelected]   = useState(null);

  const birthDate = useMemo(() => {
    if (!profile?.y || !profile?.mo || !profile?.dy) return null;
    const pad = n => String(n).padStart(2, '0');
    return `${profile.y}-${pad(profile.mo)}-${pad(profile.dy)}`;
  }, [profile?.y, profile?.mo, profile?.dy]);

  const cells = useMemo(() => {
    if (!birthDate) return [];
    return buildMonthData(
      viewYear, viewMonth,
      birthDate,
      profile.birthTime,
      profile.birthGMT,
      profile.currentGMT
    );
  }, [birthDate, viewYear, viewMonth, profile?.birthTime, profile?.birthGMT, profile?.currentGMT]);

  function prevMonth() {
    if (viewMonth === 0) { setViewYear(y => y - 1); setViewMonth(11); }
    else setViewMonth(m => m - 1);
  }

  function nextMonth() {
    if (viewMonth === 11) { setViewYear(y => y + 1); setViewMonth(0); }
    else setViewMonth(m => m + 1);
  }

  if (!birthDate) return null;

  const isExpanded = embedded || open;

  return (
    <div className={`rhythm-cal${open ? ' open' : ''}${embedded ? ' rhythm-cal--embedded open' : ''}`}>
      {!embedded && (
        <div className="rhythm-cal-header" onClick={() => setOpen(o => !o)}>
          <div className="rhythm-cal-titles">
            <div className="rhythm-cal-eyebrow">COLOR RHYTHM CALENDAR</div>
            <div className="rhythm-cal-month">{MONTH_NAMES[viewMonth]} {viewYear}</div>
          </div>
          <div className="rhythm-cal-chevron">{open ? '▲' : '▼'}</div>
        </div>
      )}

      {isExpanded && (
        <div className="rhythm-cal-nav">
          <button className="rhythm-cal-nav-btn" onClick={prevMonth}>‹</button>
          <span className="rhythm-cal-nav-label">{MONTH_NAMES[viewMonth]} {viewYear}</span>
          <button className="rhythm-cal-nav-btn" onClick={nextMonth}>›</button>
        </div>
      )}

      <div className="cal-dow-row">
        {DOW.map(d => <div key={d} className="cal-dow">{d}</div>)}
      </div>

      <div className={`cal-grid${isExpanded ? ' expanded' : ''}`}>
        {cells.map((cell, i) => {
          if (!cell) return <div key={`empty-${i}`} className="cal-day empty" />;
          const zoneLower = cell.zone?.toLowerCase();
          const sign = cell.delta >= 0 ? '+' : '';
          return (
            <div
              key={cell.dateKey}
              className={`cal-day zc-${zoneLower}${cell.isToday ? ' today' : ''}${selected?.dateKey === cell.dateKey ? ' selected' : ''}`}
              onClick={() => setSelected(cell)}
            >
              <span className="day-num">{cell.day}</span>
              {isExpanded && <span className="day-zone">{cell.zone}</span>}
              {isExpanded && <span className="day-delta">{sign}{cell.delta}</span>}
            </div>
          );
        })}
      </div>

      {selected && <DayDetail day={selected} profile={profile} embedded={embedded} onClose={() => setSelected(null)} />}
    </div>
  );
}
