# No Shorts for YouTube

**A cleaner YouTube experience. Fewer distractions. More focus.**

No Shorts for YouTube is a lightweight, open-source Chrome extension that automatically hides YouTube Shorts while preserving regular videos.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Manifest](https://img.shields.io/badge/Manifest-V3-orange)

## Features

- Hide Shorts from the YouTube homepage.
- Remove Shorts from search results, subscriptions, history and recommendations.
- Hide Shorts on channel pages.
- Remove Shorts navigation buttons and tabs.
- Block direct Shorts links.
- Enable or disable filtering instantly.
- Automatic light and dark themes.
- Persistent local preferences.
- No tracking, advertisements or external services.

## Installation

1. Download or clone this repository.
2. Open `chrome://extensions` in Chrome.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `extension/` directory.
6. Refresh YouTube.

Pin the extension to your browser toolbar to access its settings.

## How it works

The extension uses CSS and JavaScript to detect recognizable YouTube Shorts elements and URL patterns.

It dynamically filters newly loaded content as you scroll or navigate, without relying on video duration, resolution or orientation.

## Project structure

- `extension/` — Extension source code and assets.
- `tests/` — Automated tests and browser integration tests.
- `scripts/` — Packaging and validation tools.
- `store/` — Chrome Web Store publishing materials.
- `CHANGELOG.md` — Version history.
- `LICENSE` — MIT License.

## Development

    git clone https://github.com/radouane-oubakhane/no-shorts-for-youtube.git
    cd no-shorts-for-youtube

The extension requires no runtime dependencies or compilation.

### Run tests

    node --test tests/routes.test.js

For browser tests:

    python -m venv .venv
    source .venv/bin/activate
    pip install playwright
    python -m playwright install chromium
    python tests/browser_test.py

### Build the release package

    python scripts/package.py

## Privacy

All processing takes place locally in your browser. Preferences are stored using Chrome's local storage API.

No personal information is collected or transmitted.

## Compatibility and limitations

Built for Chromium-based browsers using Manifest V3.

YouTube layout changes may affect filtering. Automated offline tests have passed, but live installed-extension verification is still required.

The extension does not support the native YouTube mobile application.

## Contributing

Bug reports, feature requests and pull requests are welcome.

## License

Distributed under the MIT License. See `LICENSE` for details.

---

An independent open-source project. Not affiliated with YouTube or Google.