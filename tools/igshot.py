import asyncio,sys
from playwright.async_api import async_playwright
OUT="C:/Users/Sergio/Desktop/PAGX Studio/pagx-prospeccion/bocetos/evidencia/"
pairs=[a.split("=") for a in sys.argv[1:]]
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel="chrome")
        for user,slug in pairs:
            pg=await b.new_page(viewport={"width":500,"height":900})
            try: await pg.goto(f"https://www.instagram.com/{user}/",wait_until="networkidle",timeout=40000)
            except Exception: pass
            await pg.wait_for_timeout(2500)
            await pg.evaluate("document.querySelectorAll('div[role=dialog]').forEach(d=>{let x=d;while(x.parentElement&&x.parentElement!==document.body)x=x.parentElement;x.remove()});document.body.style.overflow='auto'")
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=OUT+slug+"-ig.jpg");await pg.close();print("ok",slug)
        await b.close()
asyncio.run(m())
