"""Render a 1080x1920 story. Usage: render_story.py <assets_dir> <out.jpg> <json>
json: {"kind":"question"|"teaser", "eyebrow":..., "h":..., "p":..., "img": optional filename in assets_dir, "tag": optional}"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright
d = pathlib.Path(sys.argv[1]).resolve(); out = sys.argv[2]; s = json.loads(sys.argv[3])
CSS = """
@font-face{font-family:H;src:url(heebo-hebrew-wght-normal.woff2) format('woff2');font-weight:100 900;unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}
@font-face{font-family:H;src:url(heebo-latin-wght-normal.woff2) format('woff2');font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#070D1C;font-family:H,sans-serif;color:#EAF2FF;direction:rtl}
.stage{position:absolute;inset:0;overflow:hidden}
.g1{position:absolute;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle,rgba(46,134,255,.32),rgba(46,134,255,0) 65%);top:-420px;left:-420px}
.g2{position:absolute;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(46,134,255,.16),rgba(46,134,255,0) 65%);bottom:-380px;right:-360px}
.wrap{position:absolute;inset:0;padding:300px 100px 340px;display:flex;flex-direction:column;align-items:flex-start}
.brand{display:flex;align-items:center;gap:20px;font-size:36px;font-weight:600;color:#9DB6DB}
.brand img{width:80px;height:80px;border-radius:50%}
.eyebrow{margin-top:auto;font-size:40px;font-weight:700;color:#4D9BFF;letter-spacing:1px}
h1{font-size:104px;font-weight:900;line-height:1.08;margin-top:24px}
.accent{color:#4D9BFF}
p{font-size:50px;line-height:1.45;color:#C5D5EE;margin-top:40px;max-width:880px}
.shot{width:620px;align-self:center;margin-top:60px;border-radius:36px;overflow:hidden;border:4px solid #22324A;box-shadow:0 30px 80px rgba(0,0,0,.5)}
.shot img{width:100%;display:block}
.pill{margin-top:56px;background:#3D8BFF;color:#fff;font-weight:800;font-size:50px;padding:30px 56px;border-radius:999px}
.handle{position:absolute;bottom:200px;left:0;right:0;text-align:center;font-size:40px;color:#7F98C0;direction:ltr}
"""
img = f'<div class="shot"><img src="{s["img"]}"></div>' if s.get("img") else ""
pill = f'<div class="pill">{s["tag"]}</div>' if s.get("tag") else ""
html = f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="stage"><div class="g1"></div><div class="g2"></div>
<div class="wrap"><div class="brand"><img src="logo.png"><span>NeriaTech</span></div>
<div class="eyebrow">{s.get("eyebrow","")}</div><h1>{s["h"]}</h1>{f'<p>{s["p"]}</p>' if s.get("p") else ""}{img}{pill}</div>
<div class="handle">@neria.tech</div></div></body></html>'''
f = d / "_story.html"; f.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1920})
    pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
    pg.screenshot(path=out, type="jpeg", quality=92); b.close()
