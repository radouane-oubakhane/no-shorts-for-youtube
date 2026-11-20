"""Package runtime only; no Git metadata, tests or developer materials."""
import json, zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]; ext=root/'extension'; manifest=json.loads((ext/'manifest.json').read_text())
assert manifest['manifest_version']==3
files=[*manifest['icons'].values(),manifest['action']['default_popup'],manifest['background']['service_worker']]
for c in manifest['content_scripts']: files += c['js']+c['css']
assert all((ext/p).is_file() for p in files)
out=root/'dist'; out.mkdir(exist_ok=True); target=out/f'no-shorts-v{manifest["version"]}-webstore.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ext.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(ext))
with zipfile.ZipFile(target) as z:
    assert 'manifest.json' in z.namelist() and z.testzip() is None
print(target)
