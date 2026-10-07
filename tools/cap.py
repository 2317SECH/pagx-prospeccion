import sys,asyncio
from playwright.async_api import async_playwright
import os
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\","/")
CSS="html{scroll-behavior:auto!important}header.nav{position:static!important}.wa-fab,.demo-badge{display:none!important}"
async def shot(p,name,w,h,out):
    b=await p.chromium.launch(channel="chrome")
    pg=await b.new_page(viewport={"width":w,"height":h},device_scale_factor=1)
    await pg.goto(f"file:///{REPO}/bocetos/{name}.html",wait_until="networkidle",timeout=60000)
    await pg.add_style_tag(content=CSS)
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(1200)
    await pg.screenshot(path=out,full_page=True)
    await b.close()
async def main():
    name=sys.argv[1]
    async with async_playwright() as p:
        await shot(p,name,1280,800,f"{REPO}/bocetos/preview/{name}-desktop.png")
        await shot(p,name,390,844,f"{REPO}/bocetos/preview/{name}-mobile.png")
asyncio.run(main())
