(() => {
  'use strict';
  const {defaults, normalizeSettings} = NoShorts;
  const keys=Object.keys(defaults), inputs=Object.fromEntries(keys.map(k=>[k,document.getElementById(k)]));
  const status=document.getElementById('status'), error=document.getElementById('error'), reset=document.getElementById('reset');
  let state=defaults, loaded=false, busy=false;
  document.getElementById('version').textContent='v'+chrome.runtime.getManifest().version;
  function render() {
    for(const k of keys){inputs[k].checked=state[k];inputs[k].disabled=!loaded||busy||(k!=='enabled'&&!state.enabled);}
    status.textContent=!loaded?'Unavailable':state.enabled?'Protection active':'Protection paused';
    status.parentElement.classList.toggle('paused',!loaded||!state.enabled); reset.disabled=!loaded||busy;
  }
  async function save(patch) {
    busy=true;error.hidden=true;render();
    try {await chrome.storage.local.set(patch);state=normalizeSettings(await chrome.storage.local.get(defaults));}
    catch {error.hidden=false;}
    finally {busy=false;render();}
  }
  for(const k of keys) inputs[k].addEventListener('change',()=>save({[k]:inputs[k].checked}));
  reset.addEventListener('click',()=>save(defaults));
  chrome.storage.onChanged.addListener((changes,area)=>{if(area!=='local')return;const next={...state};for(const k of keys)if(k in changes)next[k]=changes[k].newValue;state=normalizeSettings(next);render();});
  chrome.storage.local.get(defaults).then(data=>{state=normalizeSettings(data);loaded=true;render();}).catch(()=>{error.hidden=false;render();});
})();
