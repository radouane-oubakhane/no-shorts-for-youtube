(() => {
  'use strict';
  const {defaults, normalizeSettings, classify} = NoShorts;
  const marker = 'data-ns-navigation';
  const controls = 'yt-tab-shape,tp-yt-paper-tab,yt-chip-cloud-chip-renderer,ytm-chip-cloud-chip-renderer,yt-chip-cloud-chip-view-model,ytm-chip-cloud-chip-view-model,ytd-guide-entry-renderer,ytd-mini-guide-entry-renderer,ytm-pivot-bar-item-renderer,yt-tab-view-model';
  const labels = new Set(['shorts','youtube shorts','فيديوهات قصيرة','الفيديوهات القصيرة','مقاطع قصيرة','مقاطع الفيديو القصيرة','vidéos courtes','cortos','vídeos curtos','kurzvideos','ショート','쇼츠','短片','短视频','短影片']);
  const norm = value => (value || '').trim().replace(/\s+/g,' ').toLowerCase();
  let settings = defaults, ready = false, timer = 0, lastURL = '', poll = 0;
  const observer = new MutationObserver(schedule);
  function checkRoute() {
    if (!ready || !settings.enabled || !settings.blockDirect) return;
    if (lastURL === location.href) return;
    lastURL = location.href;
    const route = classify(location.href);
    if (route) location.replace(route.target);
  }
  function scan() {
    timer = 0;
    if (!settings.enabled || !settings.hideNavigation) return;
    for (const el of document.querySelectorAll(controls)) {
      const link = el.matches('a[href]') ? el : el.querySelector('a[href]');
      const route = link && classify(link.getAttribute('href'), location.href);
      const values = [el.getAttribute('tab-title'),el.getAttribute('aria-label'),el.getAttribute('title'),el.textContent];
      el.toggleAttribute(marker, Boolean(route) || values.some(v => labels.has(norm(v))));
    }
    checkRoute();
  }
  function schedule() { if (!timer && settings.enabled && settings.hideNavigation) timer = setTimeout(scan, 80); }
  function apply(next) {
    settings = normalizeSettings(next); ready = true;
    const root = document.documentElement;
    if (!root) { document.addEventListener('DOMContentLoaded', () => apply(settings), {once:true}); return; }
    root.toggleAttribute('data-ns-active', settings.enabled);
    root.toggleAttribute('data-ns-hide-nav', settings.enabled && settings.hideNavigation);
    observer.disconnect(); clearTimeout(timer); timer = 0;
    if (settings.enabled && settings.hideNavigation) {
      observer.observe(root,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['href','aria-label','title','tab-title']});
      scan();
    }
    clearInterval(poll); poll = 0; lastURL = '';
    if (settings.enabled && settings.blockDirect) { checkRoute(); poll = setInterval(checkRoute, 600); }
  }
  for (const event of ['yt-navigate-finish','yt-page-data-updated','yt-navigate-start']) document.addEventListener(event, () => {checkRoute(); schedule();}, true);
  window.addEventListener('popstate', checkRoute);
  window.addEventListener('pageshow', checkRoute);
  document.addEventListener('click', event => {
    if (!ready || !settings.enabled || !settings.blockDirect || event.button !== 0 || event.ctrlKey || event.altKey || event.metaKey || event.shiftKey) return;
    const link = event.composedPath().find(node => node instanceof HTMLAnchorElement);
    if (!link) return;
    const route = classify(link.href, location.href);
    if (route) { event.preventDefault(); event.stopImmediatePropagation(); if (location.href !== route.target) location.assign(route.target); }
  }, true);
  let revision = 0;
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;
    const updated = {...settings}; let changed = false;
    for (const key of Object.keys(defaults)) if (key in changes) {updated[key] = changes[key].newValue; changed = true;}
    if (changed) {revision++; apply(updated);}
  });
  const initialRevision = revision;
  chrome.storage.local.get(defaults).then(data => {if (revision === initialRevision) apply(data);}).catch(() => {if (revision === initialRevision) apply(defaults);});
})();
