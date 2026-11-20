"""Chromium DOM and popup tests with simulated extension APIs on a local fixture.
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

MOCK="""(()=>{let state={};const listeners=[];window.chrome={runtime:{getManifest:()=>({version:'2.0.0'})},storage:{local:{get:async d=>({...d,...state}),set:async patch=>{const changes={};for(const [key,newValue] of Object.entries(patch)){changes[key]={oldValue:state[key],newValue};state[key]=newValue;}listeners.forEach(f=>f(changes,'local'));}},onChanged:{addListener:f=>listeners.push(f)}}};})();"""
def load_scripts(page, *paths):
    for path in paths: page.add_script_tag(content=(ROOT/'extension'/path).read_text())
def run():
    import base64
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=os.getenv('CHROMIUM','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
        try:
            page=browser.new_page(); page.set_content(FIXTURE.replace('<head>','<head><base href="https://www.youtube.com/">'))
            page.add_style_tag(content=(ROOT/'extension/src/hide-shorts.css').read_text()); page.add_script_tag(content=MOCK); load_scripts(page,'src/shared.js','src/content.js')
            expect(page.locator('html')).to_have_attribute('data-ns-active','')
            for el in ['nav','tab','fr','short','shelf','modern','badge','mixedshort']: expect(page.locator('#'+el)).to_be_hidden()
            for el in ['regular','normal','videos','mixednormal','comment','ordinary']: expect(page.locator('#'+el)).to_be_visible()
            page.evaluate("document.body.insertAdjacentHTML('beforeend','<ytd-video-renderer id=dynamic><a href=/shorts/new>Short</a></ytd-video-renderer>')")
            expect(page.locator('#dynamic')).to_be_hidden()
            page.evaluate("document.querySelector('#dynamic a').href='/watch?v=changed'"); expect(page.locator('#dynamic')).to_be_visible()
            page.evaluate('chrome.storage.local.set({hideNavigation:false})'); expect(page.locator('#nav')).to_be_visible(); expect(page.locator('#short')).to_be_hidden()
            page.evaluate('chrome.storage.local.set({enabled:false})'); expect(page.locator('#short')).to_be_visible()
            page.evaluate('chrome.storage.local.set({enabled:true,hideNavigation:true})'); expect(page.locator('#short')).to_be_hidden(); expect(page.locator('#nav')).to_be_hidden()
            print('PASS: Chromium DOM: regular videos, explicit shelves, mixed content, localized tabs, dynamic and reused cards, settings changes')
            popup=browser.new_page(viewport={'width':348,'height':650}); html=(ROOT/'extension/ui/popup.html').read_text(); icon=base64.b64encode((ROOT/'extension/icons/icon-128.png').read_bytes()).decode(); html=html.replace('../icons/icon-128.png','data:image/png;base64,'+icon); html=re.sub(r'<script[^>]*></script>|<link[^>]*>', '',html)
            popup.set_content(html); popup.add_style_tag(content=(ROOT/'extension/ui/popup.css').read_text()); popup.add_script_tag(content=MOCK); load_scripts(popup,'src/shared.js','ui/popup.js'); expect(popup.locator('#status')).to_have_text('Protection active')
            popup.locator('#hideNavigation').uncheck(); expect(popup.locator('#hideNavigation')).not_to_be_checked(); assert popup.evaluate('chrome.storage.local.get({})')['hideNavigation']==False
            popup.locator('#blockDirect').uncheck(); assert popup.evaluate('chrome.storage.local.get({})')['blockDirect']==False
            popup.locator('#enabled').uncheck(); expect(popup.locator('#status')).to_have_text('Protection paused'); expect(popup.locator('#hideNavigation')).to_be_disabled()
            popup.locator('#reset').click(); expect(popup.locator('#status')).to_have_text('Protection active'); expect(popup.locator('#blockDirect')).to_be_checked()
            popup.emulate_media(color_scheme='light'); popup.locator('main').screenshot(path=str(ROOT/'store/popup-light.png'))
            popup.emulate_media(color_scheme='dark'); popup.locator('main').screenshot(path=str(ROOT/'store/popup-dark.png'))
            print('PASS: Chromium popup: switches, storage writes, reset, paused state, light/dark screenshots')
        finally: browser.close()
if __name__=='__main__': run()
