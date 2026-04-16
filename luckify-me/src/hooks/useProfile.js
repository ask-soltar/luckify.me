import { useState, useMemo } from 'react';
import { calculateProfile } from '../utils/profileCalculator.js';

/**
 * Custom hook for profile calculation and caching
 * Memoizes profile calculation to avoid recalculating on every render
 */
export function useProfile(formData) {
  const [isCalculating, setIsCalculating] = useState(false);

  const profile = useMemo(() => {
    if (!formData || !formData.month || !formData.day || !formData.year) {
      return null;
    }

    try {
      setIsCalculating(true);
      const result = calculateProfile({
        year: parseInt(formData.year),
        month: parseInt(formData.month),
        day: parseInt(formData.day),
        hour12: formData.hour12,
        minute: formData.minute,
        ampm: formData.ampm,
        tzOffset: formData.tzOffset
      });
      setIsCalculating(false);
      return result;
    } catch (err) {
      console.error('Profile calculation error:', err);
      setIsCalculating(false);
      return null;
    }
  }, [formData]);

  return { profile, isCalculating };
}
