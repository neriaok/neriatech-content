import sys, pathlib
from playwright.sync_api import sync_playwright

base = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

CSS = """
@font-face{font-family:H;src:url(heebo-hebrew-wght-normal.woff2) format('woff2');font-weight:100 900;unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}
@font-face{font-family:H;src:url(heebo-latin-wght-normal.woff2) format('woff2');font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
html{overflow:hidden;width:1080px;height:1350px}
.stage{position:absolute;top:0;left:0;width:1080px;height:1350px;overflow:hidden}
body{width:1080px;height:1350px;font-family:H,sans-serif;direction:rtl;color:#EAF2FF;
 background:#070D1C;overflow:hidden;position:relative}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;
 background:radial-gradient(circle,rgba(46,134,255,.35),rgba(46,134,255,0) 65%);top:-260px;left:-300px}
.glow2{position:absolute;width:700px;height:700px;border-radius:50%;
 background:radial-gradient(circle,rgba(46,134,255,.18),rgba(46,134,255,0) 65%);bottom:-260px;right:-220px}
.wrap{position:absolute;inset:0;padding:110px 96px 100px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:18px;font-size:30px;font-weight:600;color:#9DB6DB;letter-spacing:.5px}
.brand img{width:64px;height:64px;border-radius:50%}
.page{position:absolute;top:118px;left:96px;font-size:28px;color:#5F7BA6;font-weight:500;direction:ltr}
.num{font-size:260px;font-weight:900;line-height:.9;color:transparent;-webkit-text-stroke:3px #3D8BFF;direction:ltr;text-align:right;margin-top:auto}
h1{font-size:96px;font-weight:800;line-height:1.08;margin-top:40px}
h2{font-size:88px;font-weight:800;line-height:1.1;margin-top:50px}
.accent{color:#4D9BFF}
p{font-size:46px;line-height:1.45;font-weight:400;color:#C5D5EE;margin-top:44px;max-width:860px}
.bar{width:120px;height:10px;border-radius:5px;background:#3D8BFF;margin-top:56px}
.foot{margin-top:auto;padding-top:60px;display:flex;justify-content:space-between;align-items:center;font-size:32px;color:#7F98C0}
.swipe{font-weight:700;color:#4D9BFF}
.cta{margin-top:64px;display:inline-block;background:#3D8BFF;color:#fff;font-weight:800;font-size:46px;padding:30px 48px;border-radius:24px;align-self:flex-start}
"""

slides = [
 dict(kind="cover", h='האתר שלך<br><span class="accent">מבריח לקוחות?</span>',
      p='5 סימנים שכדאי לבדוק עוד היום. אם זיהיתם אפילו אחד מהם, אתם משאירים כסף על השולחן.'),
 dict(kind="item", n="01", h='נטען לאט בנייד', p='רוב הגולשים מגיעים מהטלפון, ומעט מאוד מהם מוכנים לחכות. כל שנייה של המתנה שולחת לקוח אל המתחרה.'),
 dict(kind="item", n="02", h='אין כפתור וואטסאפ בולט', p='לקוח עם שאלה לא יחפש טופס יצירת קשר. כפתור אחד, בולט, בכל עמוד, ופתאום מגיעות פניות.'),
 dict(kind="item", n="03", h='לא ברור מה אתם עושים', p='בתוך 5 שניות הכותרת צריכה לענות: מה אתם מציעים, למי, ולמה דווקא אתם.'),
 dict(kind="item", n="04", h='אין ביקורות או עבודות', p='אנשים סומכים על אנשים. המלצות אמיתיות ותמונות של עבודות קודמות בונות אמון כבר בגלילה הראשונה.'),
 dict(kind="item", n="05", h='טופס שאף אחד לא ממלא', p='עשרה שדות חובה זה מחסום. שם, טלפון ולחיצה אחת. כל השאר יכול לחכות לשיחה.'),
 dict(kind="cta", h='זיהיתם <span class="accent">סימן אחד</span><br>או יותר?',
      p='שלחו לי קישור לאתר בהודעה, ואחזור אליכם עם בדיקה חינמית ורשימת תיקונים.'),
]

import json
if len(sys.argv) > 3:
    slides = json.load(open(sys.argv[3], encoding="utf-8"))
total = len(slides)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1350})
    for i, s in enumerate(slides, 1):
        brand = '<div class="brand"><img src="logo.png"><span>NeriaTech</span></div>'
        pageno = f'<div class="page">{i}/{total}</div>'
        if s["kind"] == "cover":
            body = f'{brand}<h1 style="margin-top:auto">{s["h"]}</h1><div class="bar"></div><p>{s["p"]}</p>' \
                   f'<div class="foot"><span dir="ltr">@neria.tech</span><span class="swipe">החליקו ←</span></div>'
        elif s["kind"] == "item":
            body = f'{brand}<div class="num">{s["n"]}</div><h2>{s["h"]}</h2><p>{s["p"]}</p>' \
                   f'<div class="foot"><span dir="ltr">@neria.tech</span><span class="swipe">←</span></div>'
        else:
            body = f'{brand}<h1 style="margin-top:auto">{s["h"]}</h1><p>{s["p"]}</p>' \
                   f'<div class="cta">{s.get("btn", "שלחו הודעה עכשיו")}</div>' \
                   f'<div class="foot"><span dir="ltr">@neria.tech</span><span>אתרים · אפליקציות · AI לעסקים</span></div>'
        html = f'<!doctype html><html lang="he"><head><meta charset="utf-8"><style>{CSS}</style></head>' \
               f'<body><div class="stage"><div class="glow"></div><div class="glow2"></div><div class="wrap">{body}</div>{pageno}</div></body></html>'
        f = base / f"slide{i}.html"
        f.write_text(html, encoding="utf-8")
        pg.goto(f.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"{i:02d}.jpg"), type="jpeg", quality=92)
    b.close()
print("done")
