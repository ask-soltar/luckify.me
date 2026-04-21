/**
 * LocationInput — City autocomplete with GeoNames API + DST-aware GMT offset
 * Ported from Project Soltar / Lucky window calculator / luckycalc.html
 */

import { useState, useRef, useEffect, useCallback } from 'react';
import { searchCities } from '../utils/locationSearch.js';

function debounce(fn, ms) {
  let t;
  return (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}

/**
 * Props:
 *   label       — form label text (e.g. "> BIRTH LOCATION")
 *   placeholder — input placeholder
 *   onSelect    — called with { label, offset, tzId, latitude, longitude } when city is selected
 *   hint        — optional hint text below input
 */
const MANUAL_OFFSETS = [
  -12,-11,-10,-9.5,-9,-8,-7,-6,-5,-4,-3.5,-3,-2,-1,0,
  1,2,3,3.5,4,4.5,5,5.5,5.75,6,6.5,7,8,8.75,9,9.5,10,10.5,11,12,12.75,13,14
];

export function LocationInput({ label, placeholder, onSelect, hint }) {
  const [inputVal, setInputVal]     = useState('');
  const [badge, setBadge]           = useState('');
  const [results, setResults]       = useState([]);
  const [activeIdx, setActiveIdx]   = useState(0);
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState('');
  const [showManual, setShowManual] = useState(false);
  const [manualGMT, setManualGMT]   = useState(0);
  const [open, setOpen]             = useState(false);

  const inputRef  = useRef(null);
  const dropRef   = useRef(null);
  const searchRef = useRef(null);

  // Build debounced search function once
  useEffect(() => {
    searchRef.current = debounce(async (query) => {
      try {
        const res = await searchCities(query);
        // Only update if the input still matches
        if (inputRef.current && inputRef.current.value.trim() === query) {
          setResults(res);
          setActiveIdx(0);
          setOpen(res.length > 0);
          setLoading(false);
          if (res.length === 0) { setError('No results'); setShowManual(true); }
          else setError('');
        }
      } catch (err) {
        setLoading(false);
        setError('Search unavailable');
        setShowManual(true);
        setResults([]);
        setOpen(false);
      }
    }, 320);
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    function handleOutside(e) {
      if (
        dropRef.current && !dropRef.current.contains(e.target) &&
        inputRef.current && !inputRef.current.contains(e.target)
      ) {
        setOpen(false);
      }
    }
    document.addEventListener('mousedown', handleOutside);
    return () => document.removeEventListener('mousedown', handleOutside);
  }, []);

  function handleInput(e) {
    const q = e.target.value;
    setInputVal(q);
    setBadge('');
    setShowManual(false);
    onSelect(null); // clear selection

    if (q.trim().length < 2) {
      setResults([]);
      setOpen(false);
      setError('');
      setLoading(false);
      return;
    }

    setLoading(true);
    setError('');
    searchRef.current(q.trim());
  }

  function handleManualChange(e) {
    const offset = Number(e.target.value);
    setManualGMT(offset);
    const sign = offset >= 0 ? '+' : '';
    setBadge(`UTC${sign}${offset}  ·  manual`);
    onSelect({ label: inputVal || 'Manual offset', offset, tzId: null });
  }

  function selectCity(city) {
    const sign  = city.offset >= 0 ? '+' : '';
    const label = city.admin
      ? `${city.city}, ${city.admin}, ${city.country}`
      : `${city.city}, ${city.country}`;
    setInputVal(label);
    setBadge(`UTC${sign}${city.offset}  ·  ${city.tz}`);
    setResults([]);
    setOpen(false);
    onSelect({
      label,
      offset: city.offset,
      tzId: city.tz,
      latitude: city.latitude,
      longitude: city.longitude,
    });
  }

  function handleKeyDown(e) {
    if (!open || results.length === 0) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIdx(i => Math.min(i + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIdx(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[activeIdx]) selectCity(results[activeIdx]);
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  }

  return (
    <div className="form-section">
      {label && <label className="form-label">{label}</label>}

      <div className="loc-wrap">
        <input
          ref={inputRef}
          type="text"
          className="pip-input full-width"
          placeholder={placeholder || 'City, Country'}
          value={inputVal}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          onFocus={() => { if (results.length > 0) setOpen(true); }}
          autoComplete="off"
        />

        {badge && (
          <div className="loc-badge">{badge}</div>
        )}

        {(open || loading || error) && (
          <div ref={dropRef} className="loc-dropdown">
            {loading && (
              <div className="loc-option loc-dim">searching…</div>
            )}
            {!loading && error && (
              <div className="loc-option loc-dim">{error}</div>
            )}
            {!loading && results.map((c, i) => {
              const sign  = c.offset >= 0 ? '+' : '';
              const admin = c.admin
                ? <span className="loc-admin"> · {c.admin}</span>
                : null;
              return (
                <div
                  key={`${c.city}-${c.tz}`}
                  className={`loc-option${i === activeIdx ? ' active' : ''}`}
                  onMouseDown={() => selectCity(c)}
                  onMouseEnter={() => setActiveIdx(i)}
                >
                  <span className="loc-city">{c.city}</span>
                  {admin}
                  <span className="loc-country"> {c.country}</span>
                  <span className="loc-tz">UTC{sign}{c.offset}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Manual UTC fallback — shows when API fails or no results */}
      {showManual && !badge && (
        <div className="loc-manual">
          <span className="loc-manual-label">Set offset manually:</span>
          <select
            className="pip-select loc-manual-select"
            value={manualGMT}
            onChange={handleManualChange}
          >
            {MANUAL_OFFSETS.map(o => {
              const sign = o >= 0 ? '+' : '';
              return <option key={o} value={o}>UTC{sign}{o}</option>;
            })}
          </select>
        </div>
      )}

      {hint && !showManual && <p className="form-hint">{hint}</p>}
    </div>
  );
}
