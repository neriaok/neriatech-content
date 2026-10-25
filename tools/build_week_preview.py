import sys, json, base64, html, re, pathlib
repo = pathlib.Path(sys.argv[1]); logo_p = sys.argv[2]; out = sys.argv[3]; dates = sys.argv[4:]
B = "https://raw.githubusercontent.com/neriaok/neriatech-content/main/"
def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()
def local(url): return repo / url.replace(B, "")
logo = b64(logo_p, "image/png")
DAYS = {6: "מוצ״ש", 0: "א׳", 1: "ב׳", 2: "ג׳", 3: "ד׳", 4: "ה׳", 5: "ו׳"}
import datetime
TYPE = {"carousel": "קרוסלה", "reel": "ריל", "photo": "תמונה"}

posts = []
for d in dates:
    p = json.load(open(repo / "posts" / f"{d}.json", encoding="utf-8"))
    dt = datetime.date.fromisoformat(d)
    wd = (dt.weekday() + 1) % 7
    label = f"{DAYS[wd]} {dt.day}/{dt.month} · {TYPE[p['type']]}"
    cap = html.escape(p["caption"])
    cap = re.sub(r'(#\S+)', r'<span class="tag">\1</span>', cap).replace("\n", "<br>")
    if p["type"] == "carousel":
        media = [b64(local(f["image_url"]), "image/jpeg") for f in p["files"]]
    elif p["type"] == "photo":
        media = [b64(local(p["image_url"]), "image/jpeg")]
    else:
        media = [b64(local(p["video_url"]), "video/mp4")]
    posts.append(dict(label=label, type=p["type"], media=media, cap=cap, approved=p.get("approved", False)))

data = json.dumps(posts, ensure_ascii=False)
page = """<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>תצוגת השבוע – neria.tech</title>
<style>
:root{--bg:#fff;--fg:#000;--mut:#737373;--line:#dbdbdb;--dot:#a8a8a8;--blue:#0095f6;--page:#f2f2f2;--tag:#00376b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#000;--fg:#f5f5f5;--mut:#a8a8a8;--line:#262626;--dot:#555;--page:#121212;--tag:#e0f1ff}}
:root[data-theme="dark"]{--bg:#000;--fg:#f5f5f5;--mut:#a8a8a8;--line:#262626;--dot:#555;--page:#121212;--tag:#e0f1ff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--page);font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--fg);display:flex;flex-direction:column;align-items:center;padding:20px 0 48px;gap:14px}
h1{font-size:18px;font-weight:700}
.tabs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:0 16px}
.tabs button,.bar button{border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:999px;padding:7px 14px;cursor:pointer;font-size:13px}
.tabs button.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.st{font-size:12px;color:var(--mut)}
.phone{width:min(100vw,414px);background:var(--bg);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.top{display:flex;align-items:center;gap:10px;padding:10px 12px}
.av{width:34px;height:34px;border-radius:50%;padding:2px;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7)}
.av img{width:100%;height:100%;border-radius:50%;border:2px solid var(--bg);display:block}
.un{font-weight:600;font-size:14px}.sub{font-size:12px;color:var(--mut)}.more{margin-inline-start:auto;font-size:20px}
.view{position:relative;width:100%;overflow:hidden;background:#000;direction:ltr;touch-action:pan-y}
.view.c{aspect-ratio:4/5}.view.r{aspect-ratio:9/16}
.track{display:flex;height:100%;transition:transform .3s ease}
.s{flex:0 0 100%;height:100%}.s img,.view video{width:100%;height:100%;object-fit:cover;display:block;user-select:none;-webkit-user-drag:none}
.cnt{position:absolute;top:12px;right:12px;background:rgba(0,0,0,.6);color:#fff;font-size:12px;border-radius:12px;padding:3px 9px}
.nav{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border-radius:50%;border:0;background:rgba(255,255,255,.85);color:#000;font-size:16px;cursor:pointer}
.prev{left:10px}.next{right:10px}.nav[hidden]{display:none}
.mute{position:absolute;bottom:12px;right:12px;background:rgba(0,0,0,.6);color:#fff;border:0;border-radius:50%;width:30px;height:30px;font-size:13px}
.acts{display:flex;align-items:center;padding:8px 12px;gap:14px;position:relative}
.acts svg{width:24px;height:24px;stroke:var(--fg);fill:none;stroke-width:1.8}.save{margin-inline-start:auto}
.dots{position:absolute;left:50%;transform:translateX(-50%);display:flex;gap:4px;direction:ltr}
.dots i{width:6px;height:6px;border-radius:50%;background:var(--dot)}.dots i.on{background:var(--blue)}
.txt{padding:0 12px 14px;font-size:14px;line-height:1.45}.likes{font-weight:600;margin-bottom:4px}
.cap{overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}.cap.open{display:block}
.tag{color:var(--tag)}.mbtn{color:var(--mut);background:none;border:0;font-size:14px;cursor:pointer}
.time{color:var(--mut);font-size:11px;margin-top:6px}
.note{font-size:12px;color:var(--mut);max-width:414px;text-align:center;padding:0 16px}
</style></head><body>
<h1>תצוגת השבוע · neria.tech</h1>
<div class="tabs" id="tabs"></div>
<div class="st" id="st"></div>
<div class="phone">
 <div class="top"><div class="av"><img src="__LOGO__" alt=""></div><div><div class="un">neria.tech</div><div class="sub">NeriaTech</div></div><div class="more">···</div></div>
 <div id="media"></div>
 <div class="acts">
  <svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.5-9.2C1 8.2 3.4 4.5 7 4.5c2 0 3.6 1.1 5 3 1.4-1.9 3-3 5-3 3.6 0 6 3.7 4.5 7.3C19.5 16.4 12 21 12 21z"/></svg>
  <svg viewBox="0 0 24 24"><path d="M20.5 11.5a8.5 8.5 0 1 1-4-7.2L21 3l-1.2 4.4a8.4 8.4 0 0 1 .7 4.1z"/></svg>
  <svg viewBox="0 0 24 24"><path d="M22 3 11 13M22 3l-7 18-4-8-8-4z"/></svg>
  <div class="dots" id="dots"></div>
  <svg class="save" viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V3h14z"/></svg>
 </div>
 <div class="txt"><div class="likes">0 לייקים</div><div class="cap" id="cap"></div><button class="mbtn" id="mbtn">עוד</button><div class="time">לפני רגע</div></div>
</div>
<div class="bar"><button id="theme">מצב כהה / בהיר</button></div>
<p class="note">תצוגה מקדימה מקומית. בקרוסלות: גררו, השתמשו בחיצים או במקלדת. ברילס: הסרטון מתנגן בלולאה.</p>
<script>
const P=__DATA__;let cur=0,i=0,n=1;
const $=id=>document.getElementById(id);
function tabs(){$('tabs').innerHTML='';P.forEach((p,k)=>{const b=document.createElement('button');b.textContent=p.label;b.className=k===cur?'on':'';b.onclick=()=>show(k);$('tabs').appendChild(b);});}
function go(k){i=Math.max(0,Math.min(n-1,k));const tr=document.querySelector('.track');if(!tr)return;tr.style.transform=`translateX(${-i*100}%)`;
 [...$('dots').children].forEach((d,j)=>d.classList.toggle('on',j===i));$('cnt').textContent=(i+1)+'/'+n;$('prev').hidden=i===0;$('next').hidden=i===n-1;}
function show(k){cur=k;i=0;const p=P[k];tabs();$('st').textContent=p.approved?'מאושר לפרסום':'ממתין לאישור';
 const m=$('media');
 if(p.type==='reel'){n=1;m.innerHTML=`<div class="view r"><video src="${p.media[0]}" autoplay muted loop playsinline></video><button class="mute" id="mute">🔇</button></div>`;$('dots').innerHTML='';
  $('mute').onclick=e=>{const v=m.querySelector('video');v.muted=!v.muted;e.target.textContent=v.muted?'🔇':'🔊';};}
 else{n=p.media.length;m.innerHTML=`<div class="view c" id="view"><div class="track">${p.media.map((u,j)=>`<div class="s"><img src="${u}" alt="שקף ${j+1}"></div>`).join('')}</div><div class="cnt" id="cnt"></div><button class="nav prev" id="prev">‹</button><button class="nav next" id="next">›</button></div>`;
  $('dots').innerHTML=n>1?p.media.map(()=>'<i></i>').join(''):'';$('prev').onclick=()=>go(i-1);$('next').onclick=()=>go(i+1);
  let sx=null;$('view').onpointerdown=e=>{sx=e.clientX};$('view').onpointerup=e=>{if(sx===null)return;const d=e.clientX-sx;if(d<-40)go(i+1);else if(d>40)go(i-1);sx=null;};go(0);}
 $('cap').innerHTML='<b>neria.tech</b> '+p.cap;$('cap').classList.remove('open');$('mbtn').style.display='';}
$('mbtn').onclick=e=>{$('cap').classList.add('open');e.target.style.display='none';};
addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(i+1);if(e.key==='ArrowLeft')go(i-1);});
$('theme').onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';};
show(0);
</script></body></html>"""
page = page.replace("__DATA__", data).replace("__LOGO__", logo)
open(out, "w", encoding="utf-8").write(page)
print(len(page) // 1024, "KB")
