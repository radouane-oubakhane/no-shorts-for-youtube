# Chrome Web Store listing draft

**Title:** No Shorts for YouTube

**Summary:** Hide YouTube Shorts from feeds, search, channels and navigation. Stay focused on the videos you choose.

**Category suggestion:** Productivity

**Description**
No Shorts gives you control over your YouTube experience by hiding recognized Shorts cards, shelves and navigation elements. Enjoy regular videos without the Shorts feed getting in the way.

- Hide Shorts on supported homepage, search, subscriptions, history, recommendations and channel layouts.
- Remove the Shorts navigation and channel tab.
- Optionally redirect direct Shorts URLs away from the Shorts player.
- Pause and resume from the toolbar; changes take effect on open YouTube tabs with the current content script.
- Automatically match your browser's dark or light theme.
- No account, analytics, ads, or external servers. Your settings stay on your device.

The extension identifies Shorts by page structure and URLs, not the length or title of a video. YouTube can change its layout, so coverage may vary. No Shorts is an independent tool and is not affiliated with Google or YouTube.

**Single purpose:** Hide recognized YouTube Shorts and optionally prevent navigation to Shorts-specific pages, while preserving ordinary videos.

**Storage justification:** Save the user's three boolean extension preferences on their local device.

**Site access justification:** Content scripts need to access supported YouTube website pages to identify Shorts-related markup, apply display rules, and optionally redirect Shorts-specific URLs. No other websites are accessed.

**Remote code:** No. All scripts are packaged locally.

**Data disclosures:** No personal data is collected or transmitted by the extension. It processes page URLs and markup locally for its single purpose and stores only preferences. Review the dashboard's exact data categories and attestations before submitting.
