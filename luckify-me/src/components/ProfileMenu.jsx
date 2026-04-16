/**
 * ProfileMenu — Side drawer for saved profiles
 */

import { TITHI_SVGS } from '../constants/tithi.js';
import { ELEMENT_CONFIG } from '../constants/element.js';

function ProfileAvatar({ result }) {
  if (!result) return <div className="menu-avatar-placeholder">?</div>;

  const svg = TITHI_SVGS[result.type] || '';
  return (
    <svg viewBox="0 0 56 56" fill="none" style={{ width: 28, height: 28 }}
      dangerouslySetInnerHTML={{ __html: svg }} />
  );
}

function ProfileItem({ profile, isCurrent, onSwitch, onDelete }) {
  const elemCfg = profile.result ? ELEMENT_CONFIG[profile.result.element] : null;
  const subtitle = profile.result
    ? `${profile.result.element || '—'} · ${profile.result.type || '—'}`
    : 'No reading yet';

  return (
    <div
      className={`menu-profile-item${isCurrent ? ' current' : ''}`}
      onClick={() => onSwitch(profile.id)}
    >
      <div className="menu-profile-avatar">
        <ProfileAvatar result={profile.result} />
      </div>
      <div className="menu-profile-info">
        <div className="menu-profile-name-row">
          <span className="menu-profile-name">{profile.name}</span>
          {isCurrent && <span className="current-dot" />}
        </div>
        <span className="menu-profile-type">{subtitle}</span>
      </div>
      <button
        className="menu-delete-btn"
        onClick={e => { e.stopPropagation(); onDelete(profile.id); }}
        title="Delete profile"
      >
        ×
      </button>
    </div>
  );
}

export function ProfileMenu({ open, profiles, currentProfileId, onSwitch, onDelete, onNew, onClose }) {
  return (
    <div className={`menu-overlay${open ? ' open' : ''}`}>
      <div className="menu-backdrop" onClick={onClose} />
      <div className="menu-drawer">
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

        <div className="menu-add-btn" onClick={() => { onNew(); onClose(); }}>
          <span className="menu-add-icon">+</span>
          <span className="menu-add-label">[ NEW PROFILE ]</span>
        </div>

        <button className="pip-button menu-close-btn" onClick={onClose}>
          [ CLOSE ]
        </button>
      </div>
    </div>
  );
}
