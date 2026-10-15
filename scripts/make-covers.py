#!/usr/bin/env python3
"""Generate the header image and link-preview card for every blog post.

For each content/posts/<slug>/index.md this writes, next to it:
  hero.jpg   2400x900  artwork shown at the top of the post
  cover.jpg  1200x630  the same artwork with the post title, used as the
                       LinkedIn / Open Graph preview image

The artwork is a network graph seeded from the slug, so each post gets its
own pattern and re-running the script reproduces it exactly. Existing images
are kept unless --force is given.

Needs Python 3 and Playwright with Chromium:
  pip install playwright && playwright install chromium
  python3 scripts/make-covers.py [--force] [slug ...]
"""
import argparse, hashlib, html, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"

PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,600&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
body{width:__W__px;height:__H__px;overflow:hidden;font-family:Inter,sans-serif;color:#eef0f3;background:#0d1219}
svg{position:absolute;inset:0}
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,18,25,.96) 0%,rgba(13,18,25,.86) 46%,rgba(13,18,25,.2) 78%,rgba(13,18,25,0) 100%)}
.text{position:absolute;left:72px;right:72px;top:64px;bottom:64px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:14px;font-size:22px;font-weight:600;color:#c9d0d9}
.mark{width:44px;height:44px;border-radius:11px;background:#eef0f3;color:#0d1219;display:grid;place-items:center;font:600 28px/1 "Source Serif 4",serif}
.eyebrow{margin-top:auto;font-size:20px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#fb8a4c}
h1{margin-top:14px;max-width:760px;font-weight:700;letter-spacing:-.025em;line-height:1.08}
.meta{margin-top:22px;font-size:22px;color:#a3abb6}
</style></head><body>
<svg id="art" width="__W__" height="__H__" viewBox="0 0 __W__ __H__"></svg>
__OVERLAY__
<script>
const W=__W__, H=__H__, SEED=__SEED__, TEXTSIDE=__TEXTSIDE__;
let s=SEED>>>0; const rnd=()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296};
const svg=document.getElementById('art'), NS='http://www.w3.org/2000/svg';
const el=(n,a)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);svg.appendChild(e);return e};
const defs=el('defs',{});
defs.innerHTML=`<radialGradient id="bg" cx="${70+rnd()*20}%" cy="${20+rnd()*40}%" r="85%"><stop offset="0" stop-color="#1b2a3f"/><stop offset=".55" stop-color="#111a26"/><stop offset="1" stop-color="#0b0f15"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fb8a4c" stop-opacity=".55"/><stop offset="1" stop-color="#fb8a4c" stop-opacity="0"/></radialGradient>`;
el('rect',{width:W,height:H,fill:'url(#bg)'});
// faint grid
for(let x=0;x<W;x+=W/24) el('line',{x1:x,y1:0,x2:x,y2:H,stroke:'#5f9ff5','stroke-opacity':.05});
for(let y=0;y<H;y+=W/24) el('line',{x1:0,y1:y,x2:W,y2:y,stroke:'#5f9ff5','stroke-opacity':.05});
// nodes, denser away from the text side
const N=Math.round(W*H/7000), pts=[];
for(let i=0;i<N;i++){let x=rnd(); if(TEXTSIDE) x=Math.pow(x,.55); pts.push({x:x*W,y:rnd()*H,r:1.5+rnd()*2.5,hot:rnd()<.07})}
// links to nearest neighbours
for(const p of pts){const near=pts.map(q=>[q,(q.x-p.x)**2+(q.y-p.y)**2]).filter(a=>a[1]>0).sort((a,b)=>a[1]-b[1]).slice(0,3);
  for(const [q,d] of near){if(d>(W/5)**2)continue; const hot=p.hot&&q.hot;
    el('line',{x1:p.x,y1:p.y,x2:q.x,y2:q.y,stroke:hot?'#fb8a4c':'#5f9ff5','stroke-opacity':hot?.7:(.12+.18*(p.x/W)),'stroke-width':hot?1.6:1})}}
// a few highlighted paths through hot nodes
const hot=pts.filter(p=>p.hot).sort((a,b)=>a.x-b.x);
for(let i=1;i<hot.length;i++){if(rnd()<.5)el('line',{x1:hot[i-1].x,y1:hot[i-1].y,x2:hot[i].x,y2:hot[i].y,stroke:'#fb8a4c','stroke-opacity':.35,'stroke-width':1.2,'stroke-dasharray':'4 6'})}
for(const p of pts){ if(p.hot){el('circle',{cx:p.x,cy:p.y,r:p.r*7,fill:'url(#glow)'});el('circle',{cx:p.x,cy:p.y,r:p.r+1.5,fill:'#fb8a4c'})}
  else el('circle',{cx:p.x,cy:p.y,r:p.r,fill:'#cfe0f7','fill-opacity':.25+.55*(p.x/W)})}
</script></body></html>"""

OVERLAY = """<div class="shade"></div><div class="text">
<div class="brand"><div class="mark">λ</div>A Field CTO Perspective</div>
<div class="eyebrow">__EYEBROW__</div>
<h1 style="font-size:__SIZE__px">__TITLE__</h1>
<div class="meta">Gary Berger · __DATE__</div></div>"""


def front_matter(text):
    fm = text.split("\n---\n", 1)[0]
    def get(key):
        m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.M)
        return m.group(1).replace('\\"', '"') if m else ""
    cats = re.findall(r'"([^"]+)"', get("categories") or "")
    return get("title"), get("date"), cats


def title_size(title):
    n = len(title)
    return 72 if n <= 30 else 60 if n <= 55 else 50 if n <= 80 else 44


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="overwrite existing images")
    ap.add_argument("slugs", nargs="*", help="only these posts")
    args = ap.parse_args()
    from playwright.sync_api import sync_playwright
    import datetime
    with sync_playwright() as pw:
        # CHROMIUM=/path/to/chrome uses an existing browser instead of Playwright's own.
        browser = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        for md in sorted(POSTS.glob("*/index.md")):
            slug = md.parent.name
            if args.slugs and slug not in args.slugs:
                continue
            title, date, cats = front_matter(md.read_text(encoding="utf-8"))
            seed = int(hashlib.sha256(slug.encode()).hexdigest()[:8], 16)
            when = datetime.date.fromisoformat(date[:10]).strftime("%B %-d, %Y") if date else ""
            jobs = [("hero.jpg", 1200, 450, 2, "", 0),
                    ("cover.jpg", 1200, 630, 1, OVERLAY.replace("__EYEBROW__", html.escape(" · ".join(cats) or "Writing"))
                        .replace("__TITLE__", html.escape(title)).replace("__SIZE__", str(title_size(title)))
                        .replace("__DATE__", html.escape(when)), 1)]
            for name, w, h, scale, overlay, textside in jobs:
                out = md.parent / name
                if out.exists() and not args.force:
                    print(f"keep   {out.relative_to(ROOT)}"); continue
                page = (PAGE.replace("__W__", str(w)).replace("__H__", str(h)).replace("__SEED__", str(seed))
                        .replace("__TEXTSIDE__", str(textside)).replace("__OVERLAY__", overlay))
                p = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
                p.set_content(page, wait_until="networkidle")
                p.evaluate("document.fonts.ready")
                p.screenshot(path=str(out), type="jpeg", quality=88)
                p.close()
                print(f"wrote  {out.relative_to(ROOT)}")
        browser.close()


if __name__ == "__main__":
    sys.exit(main())
