import { useState } from 'react';
import { validateProfileInputs } from '../utils/profileCalculator.js';

/**
 * Custom hook for profile form state management
 * Handles input validation and form submission
 */
export function useProfileForm(onSubmit) {
  const [formData, setFormData] = useState({
    displayName: '',
    month: '',
    day: '',
    year: '',
    hour12: 12,
    minute: 0,
    ampm: 'PM',
    birthGMT: null,    // numeric offset from birth location
    birthTzId: null,   // IANA tz string for DST-aware calcs
    birthLat: null,    // decimal latitude for observer-based moon audit
    birthLng: null,    // decimal longitude for observer-based moon audit
    currentGMT: null,  // numeric offset from current/event location
    currentTzId: null  // IANA tz string for current location
  });

  const [error, setError] = useState(null);

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: field === 'hour12' || field === 'minute' ? Number(value) : value
    }));
    setError(null);
  };

  // Called by LocationInput onSelect for birth/current location
  const handleLocation = (field, selection) => {
    if (field === 'birth') {
      setFormData(prev => ({
        ...prev,
        birthGMT: selection ? selection.offset : null,
        birthTzId: selection ? selection.tzId : null,
        birthLat: selection ? selection.latitude ?? null : null,
        birthLng: selection ? selection.longitude ?? null : null,
      }));
    } else if (field === 'current') {
      setFormData(prev => ({
        ...prev,
        currentGMT: selection ? selection.offset : null,
        currentTzId: selection ? selection.tzId : null
      }));
    }
    setError(null);
  };

  const handleSubmit = (e) => {
    e?.preventDefault();

    // Validate birth date fields
    const { valid, error: validationError } = validateProfileInputs(formData);
    if (!valid) {
      setError(validationError);
      return;
    }

    // birthGMT defaults to 0 (UTC) if no location selected — not a blocker
    if (onSubmit) {
      onSubmit({
        ...formData,
        displayName: (formData.displayName || '').trim(),
        birthGMT: formData.birthGMT ?? 0,
        currentGMT: formData.currentGMT ?? formData.birthGMT ?? 0
      });
    }
  };

  const reset = () => {
    setFormData({
      displayName: '',
      month: '',
      day: '',
      year: '',
      hour12: 12,
      minute: 0,
      ampm: 'PM',
      birthGMT: null,
      birthTzId: null,
      birthLat: null,
      birthLng: null,
      currentGMT: null,
      currentTzId: null
    });
    setError(null);
  };

  return {
    formData,
    handleChange,
    handleLocation,
    handleSubmit,
    reset,
    error,
    clearError: () => setError(null)
  };
}
