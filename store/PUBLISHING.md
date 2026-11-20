# Pre-submission checklist

1. Install the unpacked `extension/` folder in Chrome and disable the old version. Pin the toolbar icon and reload YouTube.
2. Manually verify home, search, subscriptions, history, channel Home/Videos/Shorts tabs, recommended videos, infinite scroll, regular short-duration videos, direct `/shorts/` and channel `/shorts` links, back/forward navigation, and that all switches take effect across two YouTube tabs. Test disabled state after browser restart and light/dark modes. Check `chrome://extensions` for errors and verify the OFF toolbar badge.
3. Run `node --test tests/routes.test.js` and `python tests/browser_test.py` (passed in build). Run `python tests/extension_integration.py` on an unrestricted development browser (not run in build environment).
4. Check naming/branding and trademark compliance; publisher name and support contact are yours to choose. Verify the listing and privacy disclosures against the actual behavior.
5. Publish `PRIVACY.md` with your real identity and support contact at a public HTTPS URL if required or requested by the dashboard. Draft promotional images are included. The screenshots show the actual popup rendered in Chromium with simulated storage; capture at least one real installed-extension screenshot at 1280×800 on your own Chrome before submitting, especially if the dashboard needs end-to-end screenshots.
6. Register at https://chrome.google.com/webstore/devconsole, complete account verification and any applicable registration fee. Enable 2-step verification. Create a new item, upload the runtime-only ZIP from `scripts/package.py`, enter listing and privacy fields, upload icon and images, and submit for review. Google controls approval.
7. For future releases: increment manifest version, update CHANGELOG, test, commit, tag and rebuild ZIP. Upload as an update to the same store item.

Official documentation:
- https://developer.chrome.com/docs/webstore/prepare
- https://developer.chrome.com/docs/webstore/cws-dashboard-listing
- https://developer.chrome.com/docs/webstore/cws-dashboard-privacy
- https://developer.chrome.com/docs/webstore/images
- https://developer.chrome.com/docs/webstore/program-policies/policies
