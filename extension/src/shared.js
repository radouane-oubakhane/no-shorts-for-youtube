/* Shared settings and route classification. No remote code or requests. */
(() => {
  'use strict';
  const defaults = Object.freeze({ enabled: true, hideNavigation: true, blockDirect: true });
  const hosts = new Set(['www.youtube.com', 'youtube.com', 'm.youtube.com']);
  function normalizeSettings(raw = {}) {
    return Object.fromEntries(Object.entries(defaults).map(([key, value]) => [key, typeof raw[key] === 'boolean' ? raw[key] : value]));
  }
  function classify(input, base = 'https://www.youtube.com/') {
    let url;
    try { url = new URL(input, base); } catch { return null; }
    if (!hosts.has(url.hostname) || !['https:', 'http:'].includes(url.protocol)) return null;
    const path = url.pathname.replace(/\/+$/, '');
    if (/^\/(?:shorts|feed\/shorts)(?:\/|$)/i.test(path)) return { kind: 'shorts', target: new URL('/', url.origin).href };
    const match = path.match(/^(\/@[^/]+|\/(?:channel|c|user)\/[^/]+)\/shorts(?:\/|$)/i);
    return match ? { kind: 'channel', target: new URL(match[1] + '/videos', url.origin).href } : null;
  }
  globalThis.NoShorts = Object.freeze({ defaults, normalizeSettings, classify });
})();
