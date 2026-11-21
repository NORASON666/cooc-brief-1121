# 簡報逐頁 1920×1080 截圖（隱藏操作列、等動畫跑完）→ 合成橫向 PDF
import sys, asyncio, http.server, threading, functools, os
from playwright.async_api import async_playwright
from PIL import Image
root, out, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
tmp='/private/tmp/claude-502/deckpdf'; os.makedirs(tmp, exist_ok=True)
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), functools.partial(Q, directory=root)); threading.Thread(target=srv.serve_forever, daemon=True).start()
HIDE = "#bar,#secchip,#prog,#timerBadge,#timerPanel,#panel,#zoom,#edgeGlow,.supbtn{display:none!important}"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=angle","--enable-webgl","--ignore-gpu-blocklist"])
        files=[]
        for i in range(1, n + 1):
            pg = await b.new_page(viewport={"width": 1920, "height": 1080})
            await pg.goto(f"http://127.0.0.1:8766/index.html#p{i}")
            await pg.add_style_tag(content=HIDE)
            await pg.wait_for_timeout(4500)
            f=f"{tmp}/s{i:02d}.png"; await pg.screenshot(path=f); files.append(f); await pg.close()
        await b.close()
    ims=[Image.open(f).convert('RGB') for f in files]
    ims[0].save(out, save_all=True, append_images=ims[1:], resolution=144)
    print('pages', len(ims))
asyncio.run(main())
