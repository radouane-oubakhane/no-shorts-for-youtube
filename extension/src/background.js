importScripts('shared.js');
const {defaults, normalizeSettings} = NoShorts;
async function refreshBadge() {
  const {enabled} = normalizeSettings(await chrome.storage.local.get(defaults));
  await chrome.action.setBadgeText({text: enabled ? '' : 'OFF'});
  await chrome.action.setBadgeBackgroundColor({color:'#64748b'});
  await chrome.action.setTitle({title: enabled ? 'No Shorts — active' : 'No Shorts — paused'});
}
const update = () => refreshBadge().catch(console.error);
chrome.runtime.onInstalled.addListener(update);
chrome.runtime.onStartup.addListener(update);
chrome.storage.onChanged.addListener((changes, area) => { if (area === 'local' && 'enabled' in changes) update(); });
