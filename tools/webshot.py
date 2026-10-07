import sys,asyncio
from playwright.async_api import async_playwright
async def m(url,out,w,h):
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome");pg=await b.new_page(viewport={"width":w,"height":h})
        try: await pg.goto(url,wait_until="networkidle",timeout=45000)
        except Exception as e: print("warn",e)
        await pg.wait_for_timeout(2500);await pg.screenshot(path=out);await b.close()
asyncio.run(m(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 1280,int(sys.argv[4]) if len(sys.argv)>4 else 800))
