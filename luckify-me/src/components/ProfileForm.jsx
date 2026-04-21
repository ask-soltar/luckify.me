/**
 * ProfileForm — Birth date/time/location input form
 * Includes Option B animated intro: sequential copy lines fade in,
 * then form inputs stagger in below.
 */

import { useProfileForm } from '../hooks/index.js';
import { LocationInput } from './LocationInput.jsx';

function FormIntro() {
  return (
    <div className="form-intro">
      <p className="form-intro-line form-intro-line-1">Your output isn't constant.</p>
      <p className="form-intro-line form-intro-line-2">Neither is your day.</p>
      <h1 className="form-intro-title form-intro-line-3">Find your rhythm.</h1>
    </div>
  );
}

const MONTHS = [
  'January','February','March','April','May','June',
  'July','August','September','October','November','December'
];

const currentYear = new Date().getFullYear();
const YEARS = Array.from({ length: currentYear - 1919 }, (_, i) => currentYear - i);
const DAYS  = Array.from({ length: 31 }, (_, i) => i + 1);
const HOURS = Array.from({ length: 12 }, (_, i) => i + 1);
const MINS  = Array.from({ length: 60 }, (_, i) => i);

export function ProfileForm({ onSubmit }) {
  const { formData, handleChange, handleLocation, handleSubmit, error } = useProfileForm(onSubmit);

  return (
    <div className="form-page">
      <div className="form-atmosphere" aria-hidden="true">
        <div className="form-atmosphere-glow form-atmosphere-glow-1" />
        <div className="form-atmosphere-glow form-atmosphere-glow-2" />
        <div className="form-atmosphere-grid" />
      </div>

      <div className="form-kicker">
        <span className="form-kicker-dot" />
        <span className="form-kicker-text">Signal Setup</span>
      </div>

      <FormIntro />

      <div className="form-body">
      <form onSubmit={handleSubmit} className="calc-form form-shell">

        <div className="form-section">
          <label className="form-label" htmlFor="display-name">&gt; NAME</label>
          <input
            id="display-name"
            className="pip-input"
            type="text"
            value={formData.displayName}
            onChange={e => handleChange('displayName', e.target.value)}
            placeholder="What should we call you?"
            autoComplete="name"
            maxLength={60}
          />
          <p className="form-hint">Use your own name or any profile name you want to see in the app.</p>
        </div>

        {/* Birth Date */}
        <div className="form-section">
          <label className="form-label">&gt; BIRTH DATE</label>
          <div className="date-row">
            <select
              className="pip-select"
              value={formData.month}
              onChange={e => handleChange('month', e.target.value)}
            >
              <option value="">Month</option>
              {MONTHS.map((m, i) => (
                <option key={i} value={i + 1}>{m}</option>
              ))}
            </select>

            <select
              className="pip-select"
              value={formData.day}
              onChange={e => handleChange('day', e.target.value)}
            >
              <option value="">Day</option>
              {DAYS.map(d => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>

            <select
              className="pip-select"
              value={formData.year}
              onChange={e => handleChange('year', e.target.value)}
            >
              <option value="">Year</option>
              {YEARS.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Birth Time */}
        <div className="form-section">
          <label className="form-label">&gt; BIRTH TIME</label>
          <div className="time-row">
            <select
              className="pip-select"
              value={formData.hour12}
              onChange={e => handleChange('hour12', e.target.value)}
            >
              {HOURS.map(h => (
                <option key={h} value={h}>{h}</option>
              ))}
            </select>

            <select
              className="pip-select"
              value={formData.minute}
              onChange={e => handleChange('minute', e.target.value)}
            >
              {MINS.map(m => (
                <option key={m} value={m}>{m < 10 ? `0${m}` : m}</option>
              ))}
            </select>

            <select
              className="pip-select"
              value={formData.ampm}
              onChange={e => handleChange('ampm', e.target.value)}
            >
              <option value="AM">AM</option>
              <option value="PM">PM</option>
            </select>
          </div>
          <p className="form-hint">No birth time? Leave at 12:00 PM</p>
        </div>

        {/* Birth Location */}
        <LocationInput
          label="> BIRTH LOCATION"
          placeholder="Search city, country…"
          onSelect={sel => handleLocation('birth', sel)}
          hint="City where you were born — sets birth timezone automatically"
        />

        {/* Current Location */}
        <LocationInput
          label="> CURRENT LOCATION"
          placeholder="Search city, country…"
          onSelect={sel => handleLocation('current', sel)}
          hint="Where you are now — used for local timing calculations"
        />

        {error && <p className="error-msg">{error}</p>}

        <button className="pip-button calc-btn" type="submit">
          [ REVEAL SIGNAL ]
        </button>
      </form>
      </div>
    </div>
  );
}
