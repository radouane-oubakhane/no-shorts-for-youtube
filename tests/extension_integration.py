"""Real Chromium extension integration tests using a local, intercepted YouTube fixture.
Requires Python Playwright and system Chromium; never visits live YouTube.
"""
import os, tempfile, re
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
FIXTURE='''<!doctype html><html><head><title>Local YouTube fixture</title><style>body{font:16px sans-serif}ytd-rich-item-renderer,ytd-rich-section-renderer,ytd-guide-entry-renderer,yt-tab-shape,yt-lockup-view-model,ytd-video-renderer,ytd-reel-shelf-renderer,ytm-shorts-lockup-view-model{display:block;padding:8px}a{display:inline-block}</style></head><body>
<ytd-guide-entry-renderer id="nav"><a href="/shorts">Shorts</a></ytd-guide-entry-renderer>
<yt-tab-shape id="tab">Shorts</yt-tab-shape><yt-tab-shape id="fr">Vidéos courtes</yt-tab-shape><yt-tab-shape id="videos">Videos</yt-tab-shape>
<ytd-rich-item-renderer id="regular"><a href="/watch?v=regular">A 12-second video called Shorts</a></ytd-rich-item-renderer>
<ytd-rich-item-renderer id="short"><a href="/shorts/ABC">Short clip</a></ytd-rich-item-renderer>
<ytd-rich-section-renderer id="shelf"><div id="content"><ytd-reel-shelf-renderer>Shorts shelf</ytd-reel-shelf-renderer></div></ytd-rich-section-renderer>
<yt-lockup-view-model id="modern"><a href="https://www.youtube.com/shorts/xyz">Modern Short</a></yt-lockup-view-model>
<ytd-video-renderer id="badge"><div overlay-style="SHORTS">Short by badge</div><a href="/watch?v=short">Short</a></ytd-video-renderer>
<ytd-video-renderer id="normal"><a href="/watch?v=normal">Regular result</a></ytd-video-renderer>
<ytd-rich-section-renderer id="mixed"><div><ytd-video-renderer id="mixednormal"><a href="/watch?v=mixed">Mixed regular</a></ytd-video-renderer><ytm-shorts-lockup-view-model id="mixedshort">Mobile Shorts</ytm-shorts-lockup-view-model></div></ytd-rich-section-renderer>
<a id="comment" href="/shorts/a">Comment link</a><a id="ordinary" href="/watch?v=normal">Ordinary link</a>
</body></html>'''

def run():
    with sync_playwright() as p, tempfile.TemporaryDirectory() as profile:
        ext=str(ROOT/'extension'); context=p.chromium.launch_persistent_context(profile,executable_path=os.getenv('CHROMIUM','/usr/bin/chromium'), headless=True,ignore_default_args=['--disable-extensions'],args=['--no-sandbox',f'--disable-extensions-except={ext}',f'--load-extension={ext}'], viewport={'width':1280,'height':800})
        try:
            context.route('https://www.youtube.com/**',lambda r:r.fulfill(status=200,content_type='text/html',body=FIXTURE))
            worker=context.service_workers[0] if context.service_workers else context.wait_for_event('serviceworker',timeout=10000)
            eid=worker.url.split('/')[2]
            page=context.new_page(); page.goto('https://www.youtube.com/'); expect(page.locator('html')).to_have_attribute('data-ns-active','')
            for el in ['nav','tab','fr','short','shelf','modern','badge','mixedshort']: expect(page.locator('#'+el)).to_be_hidden()
            for el in ['regular','normal','videos','mixednormal','comment','ordinary']: expect(page.locator('#'+el)).to_be_visible()
            page.evaluate("document.body.insertAdjacentHTML('beforeend','<ytd-video-renderer id=dynamic><a href=/shorts/new>Short</a></ytd-video-renderer>')")
            expect(page.locator('#dynamic')).to_be_hidden()
            page.evaluate("document.querySelector('#dynamic a').href='/watch?v=changed'")
            expect(page.locator('#dynamic')).to_be_visible()
            print('PASS: cards, explicit shelves, mixed content, regular videos, localized navigation, mutation and reused card')
            popup=context.new_page(); popup.goto(f'chrome-extension://{eid}/ui/popup.html'); expect(popup.locator('#status')).to_have_text('Protection active'); expect(popup.locator('#enabled')).to_be_checked()
            popup.locator('#hideNavigation').uncheck(); expect(page.locator('#nav')).to_be_visible(); expect(page.locator('#short')).to_be_hidden()
            popup.locator('#blockDirect').uncheck(); page.goto('https://www.youtube.com/shorts/keep'); expect(page).to_have_url('https://www.youtube.com/shorts/keep')
            popup.locator('#enabled').uncheck(); expect(page.locator('#short')).to_be_visible(); expect(popup.locator('#status')).to_have_text('Protection paused'); expect(popup.locator('#hideNavigation')).to_be_disabled()
            popup.reload(); expect(popup.locator('#enabled')).not_to_be_checked(); expect(popup.locator('#status')).to_have_text('Protection paused')
            popup.locator('#reset').click(); expect(popup.locator('#status')).to_have_text('Protection active'); expect(page).to_have_url('https://www.youtube.com/'); expect(page.locator('#short')).to_be_hidden(); expect(page.locator('#nav')).to_be_hidden()
            page.goto('https://www.youtube.com/@test/shorts'); expect(page).to_have_url('https://www.youtube.com/@test/videos')
            page.evaluate("history.pushState({},'', '/shorts/spa');document.dispatchEvent(new Event('yt-navigate-finish'))")
            expect(page).to_have_url('https://www.youtube.com/')
            page.locator('#comment').click(); expect(page).to_have_url('https://www.youtube.com/')
            page.locator('#ordinary').click(); expect(page).to_have_url('https://www.youtube.com/watch?v=normal')
            print('PASS: popup settings, live updates, persistence, reset, initial & SPA redirects, normal links')
            popup.set_viewport_size({'width':348,'height':650}); popup.emulate_media(color_scheme='light'); popup.locator('main').screenshot(path=str(ROOT/'store/popup-light.png'))
            popup.emulate_media(color_scheme='dark'); popup.locator('main').screenshot(path=str(ROOT/'store/popup-dark.png'))
            print('PASS: real popup screenshots (light and dark)')
        finally: context.close()
if __name__=='__main__': run()
