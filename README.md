# No Shorts for YouTube — v2.0.0

Independent Manifest V3 Chrome extension that hides recognizable Shorts in YouTube feeds, search, subscriptions, history, recommendations and channels. Enabled by default. No remote services or telemetry.

## Install / develop

Open `chrome://extensions`, enable Developer mode, select **Load unpacked** and choose the `extension/` directory (not the repository root). Disable the old v1 installation and reload open YouTube tabs. Pin the new extension to the toolbar to open the menu.

The popup supports a master switch, optional navigation filtering, optional direct-link redirection, and reset. Settings are saved in `chrome.storage.local`. All three switches default to on. Changes propagate to running content scripts using `chrome.storage.onChanged`; installing/updating requires reloading already-open YouTube pages. Direct Shorts routes redirect to the homepage; channel Shorts routes redirect to that channel's Videos page. Comments/descriptions with Shorts links remain readable, but their links are redirected when direct-link blocking is on.

## Source layout

- `extension/` — complete runtime, no third-party dependencies or build step
- `tests/` — unit tests, offline Chromium fixture tests, optional unpacked extension integration test
- `scripts/package.py` — validates and builds store ZIP with manifest at root
- `store/` — listing copy, privacy policy, promotional graphics and actual popup renders (mocked Chrome storage)
- `CHANGELOG.md` — releases; Git tags `v1.0.0`, `v2.0.0`

## Test / package

```bash
node --test tests/routes.test.js
python -m venv .venv
source .venv/bin/activate
pip install playwright
python tests/browser_test.py
# Optional: run on a machine allowing unpacked extensions and intercepted YouTube navigation
python tests/extension_integration.py
python scripts/package.py
```
Set `CHROMIUM=/path/to/chromium` if needed. The optional test uses an intercepted fixture, not live YouTube.

## Verification / release gate

Route and settings unit tests passed; actual Chromium DOM/CSS and popup tests passed using representative offline layouts and mocked Chrome storage. The full installed-extension integration could not be run: the build environment blocks unpacked extension loading and YouTube navigation. Before Store submission, load it on your desktop Chrome and complete the live smoke-test checklist in `store/PUBLISHING.md`. The site can change markup; unmarked Shorts served as ordinary watch links may remain visible. The extension is not intended for the native YouTube phone app.

## Version control

The source archive includes the initialized local Git repository and two release tags. No public remote has been created. The initial import preserves the original v1.0.0; the second commit contains the revised extension. Configure your own Git author before making further commits. See `git log --oneline --decorate`.
