/**
 * Location search utilities — city autocomplete via GeoNames proxy
 * Ported from Project Soltar / Lucky window calculator / luckycalc.html
 */

const GEONAMES_PROXY = "https://geonames-proxy.luckifyme.workers.dev";

/**
 * Get UTC offset for an IANA timezone, DST-aware for the given date.
 * Uses Intl.DateTimeFormat so no external library needed.
 */
export function getOffsetForTZ(tzid, forDate) {
  try {
    const d = forDate || new Date();
    const formatter = new Intl.DateTimeFormat("en-US", {
      timeZone: tzid,
      timeZoneName: "shortOffset"
    });
    const parts = formatter.formatToParts(d);
    const tzPart = parts.find(p => p.type === "timeZoneName");
    if (!tzPart) return 0;
    const raw = tzPart.value;
    if (raw === "GMT") return 0;
    const m = raw.match(/GMT([+-])(\d+)(?::(\d+))?/);
    if (!m) return 0;
    const sign = m[1] === "+" ? 1 : -1;
    const h = parseInt(m[2], 10);
    const min = m[3] ? parseInt(m[3], 10) / 60 : 0;
    return sign * (h + min);
  } catch (e) {
    return 0;
  }
}

/**
 * Get UTC offset for an IANA timezone on a specific date (handles DST).
 * Returns null if tzid is not set.
 */
export function getOffsetForDateStr(tzid, dateStr) {
  if (!tzid) return null;
  try {
    const d = new Date(dateStr + "T12:00:00");
    return getOffsetForTZ(tzid, d);
  } catch (e) {
    return null;
  }
}

/**
 * Search cities by name via GeoNames proxy.
 * Returns array of { city, country, admin, tz, offset }
 */
export async function searchCities(query) {
  const cleanQuery = query.split(",")[0].trim();
  const url = `${GEONAMES_PROXY}?q=${encodeURIComponent(cleanQuery)}&maxRows=8`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Search failed");
  const data = await res.json();
  if (data.status) throw new Error(data.status.message);

  const cities = data.geonames || [];

  // Fetch timezone for each city in parallel via lat/lng
  const results = await Promise.all(
    cities.map(async c => {
      try {
        const tzRes = await fetch(`${GEONAMES_PROXY}?lat=${c.lat}&lng=${c.lng}`);
        const tzData = await tzRes.json();
        const tzId = tzData.timezoneId;
        if (!tzId) return null;
        const offset = getOffsetForTZ(tzId, new Date());
        return {
          city: c.name,
          country: c.countryCode,
          admin: c.adminName1 || "",
          tz: tzId,
          offset
        };
      } catch (e) {
        return null;
      }
    })
  );

  return results.filter(Boolean);
}
