/**
 * ProfileMenu — Side drawer for saved profiles
 */

import { useEffect } from 'react';
import { TITHI_SVGS } from '../constants/tithi.js';

function ProfileAvatar({ result }) {
  if (!result) return <div className="menu-avatar-placeholder">?</div>;

  const svg = TITHI_SVGS[result.type] || '';
  return (
    <svg viewBox="0 0 56 56" fill="none" style={{ width: 28, height: 28 }}
      dangerouslySetInnerHTML={{ __html: svg }} />
  );
}

function ProfileItem({ profile, isCurrent, onSwitch, onDelete }) {
  const subtitle = profile.result
    ? `${profile.result.element || '—'} · ${profile.result.type || '—'}`
    : 'No reading yet';
  const profileName = profile.name || subtitle;

  return (
    <button
      type="button"
      className={`menu-profile-item${isCurrent ? ' current' : ''}`}
      onClick={() => onSwitch(profile.id)}
      aria-current={isCurrent ? 'true' : undefined}
    >
      <div className="menu-profile-avatar">
        <ProfileAvatar result={profile.result} />
      </div>
      <div className="menu-profile-info">
        <div className="menu-profile-name-row">
          <span className="menu-profile-name">{profileName}</span>
          {isCurrent && <span className="current-dot" />}
        </div>
        <span className="menu-profile-type">{subtitle}</span>
      </div>
      <button
        type="button"
        className="menu-delete-btn"
        onClick={e => { e.stopPropagation(); onDelete(profile.id); }}
        aria-label={`Delete profile ${profileName}`}
        title="Delete profile"
      >
        ×
      </button>
    </button>
  );
}

export function ProfileMenu({ open, profiles, currentProfileId, onSwitch, onDelete, onNew, onClose }) {
  useEffect(() => {
    if (!open || typeof window === 'undefined') return undefined;

    function handleKeyDown(event) {
      if (event.key === 'Escape') onClose();
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open, onClose]);

  return (
    <div className={`menu-overlay${open ? ' open' : ''}`}>
      <div className="menu-backdrop" onClick={onClose} />
      <div
        className="menu-drawer"
        role="dialog"
        aria-modal="true"
        aria-label="Saved profiles"
      >
        <div className="menu-header">
          <div className="menu-header-title">&gt; PROFILES</div>
          <div className="menu-header-sub">Saved signal readings</div>
        </div>

        <div className="menu-profile-list">
          {profiles.length === 0 ? (
            <div className="menu-empty">No saved profiles yet</div>
          ) : (
            profiles.map(p => (
              <ProfileItem
                key={p.id}
                profile={p}
                isCurrent={p.id === currentProfileId}
                onSwitch={id => { onSwitch(id); onClose(); }}
                onDelete={onDelete}
              />
            ))
          )}
        </div>

        {profiles.length <= 1 && (
          <div className="menu-helper-card">
            <div className="menu-helper-title">Build a comparison set</div>
            <div className="menu-helper-copy">
              Save more than one profile so permanent structure stays easy to compare against daily rhythm shifts.
            </div>
          </div>
        )}

        <button
          type="button"
          className="menu-add-btn"
          onClick={() => { onNew(); onClose(); }}
        >
          <span className="menu-add-icon">+</span>
          <span className="menu-add-label">[ NEW PROFILE ]</span>
        </button>

        <button type="button" className="pip-button menu-close-btn" onClick={onClose}>
          [ CLOSE ]
        </button>
      </div>
    </div>
  );
}
