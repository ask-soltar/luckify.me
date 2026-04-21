import { useState, useCallback, useEffect } from 'react';
import { resolveProfileName } from '../utils/profileCalculator.js';

/**
 * Custom hook for localStorage-persisted profile list
 * Handles saving, loading, deleting profiles
 */
export function useProfileStorage() {
  const STORAGE_KEY = 'luckify_profiles';
  const CURRENT_KEY = 'luckify_current';

  const [profiles, setProfiles] = useState([]);
  const [currentProfileId, setCurrentProfileId] = useState(null);

  // Load profiles from localStorage on mount, migrating old format
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      const current = localStorage.getItem(CURRENT_KEY);
      const raw = saved ? JSON.parse(saved) : [];

      // Migrate pre-location profiles: add missing fields with safe defaults
      const migrated = raw.map(p => {
        if (!p.result) {
          return {
            ...p,
            name: (p.name || '').trim()
          };
        }
        const r = p.result;
        return {
          ...p,
          name: resolveProfileName(p.name, r),
          result: {
            birthGMT:    r.birthGMT    ?? null,
            birthTzId:   r.birthTzId   ?? null,
            currentGMT:  r.currentGMT  ?? null,
            currentTzId: r.currentTzId ?? null,
            birthTime:   r.birthTime   ?? '12:00',
            ...r
          }
        };
      });

      setProfiles(migrated);
      setCurrentProfileId(current);
    } catch (err) {
      console.error('Failed to load profiles from localStorage:', err);
      setProfiles([]);
    }
  }, []);

  // Persist profiles whenever they change
  const saveProfiles = useCallback((updatedProfiles) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedProfiles));
      setProfiles(updatedProfiles);
    } catch (err) {
      console.error('Failed to save profiles to localStorage:', err);
    }
  }, []);

  const addProfile = useCallback((profile) => {
    const newProfiles = [...profiles, profile];
    saveProfiles(newProfiles);
    setCurrentProfileId(profile.id);
    localStorage.setItem(CURRENT_KEY, profile.id);
    return profile.id;
  }, [profiles, saveProfiles]);

  const updateProfile = useCallback((id, updates) => {
    const updated = profiles.map(p => (p.id === id ? { ...p, ...updates } : p));
    saveProfiles(updated);
  }, [profiles, saveProfiles]);

  const deleteProfile = useCallback((id) => {
    const filtered = profiles.filter(p => p.id !== id);
    saveProfiles(filtered);
    if (currentProfileId === id) {
      const nextId = filtered.length > 0 ? filtered[0].id : null;
      setCurrentProfileId(nextId);
      localStorage.setItem(CURRENT_KEY, nextId || '');
    }
  }, [profiles, currentProfileId, saveProfiles]);

  const switchProfile = useCallback((id) => {
    setCurrentProfileId(id);
    localStorage.setItem(CURRENT_KEY, id);
  }, []);

  const getCurrentProfile = useCallback(() => {
    return profiles.find(p => p.id === currentProfileId) || null;
  }, [profiles, currentProfileId]);

  return {
    profiles,
    currentProfileId,
    addProfile,
    updateProfile,
    deleteProfile,
    switchProfile,
    getCurrentProfile,
    saveProfiles
  };
}
