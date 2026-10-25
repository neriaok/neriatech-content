import sys, pathlib
from playwright.sync_api import sync_playwright
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); dur=float(sys.argv[3]); fps=int(sys.argv[4])
out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    pg.goto(src.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    n=int(dur*fps)
    for i in range(n):
        pg.evaluate(f"setT({i/fps})")
        pg.screenshot(path=str(out/f"f{i:04d}.jpg"),type='jpeg',quality=90)
    b.close()
print(n)
