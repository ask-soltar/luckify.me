const isDev = typeof import.meta !== 'undefined' && import.meta.env?.DEV;

/**
 * Fire an analytics event.
 * In development: logs to console.
 * In production: no-op until a real analytics backend is wired here.
 * Never throws — tracking must never break the UI.
 */
export function trackEvent(eventName, payload = {}) {
  try {
    if (isDev) {
      console.log('[analytics]', eventName, payload);
    }
    // TODO: replace with real analytics call, e.g.:
    // window.analytics?.track(eventName, payload);
  } catch (_) {
    // Silently swallow — analytics must never affect the user flow
  }
}
