#!/usr/bin/env python3
"""Generate the header image and link-preview card for every blog post.

For each content/posts/<slug>/index.md this writes, next to it:
  hero.jpg   2400x900  artwork shown at the top of the post
  cover.jpg  2400x1260 the same artwork with the post title, used as the
                       LinkedIn / Open Graph preview image (rendered at 2x
                       so it stays sharp after LinkedIn recompresses it)

Each post gets a motif and accent colour (cover_motif / cover_accent in its
front matter, or picked from the slug) drawn with a pattern seeded from the
slug, so re-running the script reproduces it exactly. Motifs: graph, rings,
split, flow, loop, fabric, waves, clos. Accents: violet, teal, blue, orange,
green, amber, pink, or any hex colour. Existing images
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
.shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(13,18,25,.97) 0%,rgba(13,18,25,.9) 52%,rgba(13,18,25,.35) 70%,rgba(13,18,25,0) 84%)}
.text{position:absolute;left:72px;right:72px;top:64px;bottom:64px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:16px;font-size:28px;font-weight:600;color:#d6dce4}
.mark{width:54px;height:54px;border-radius:13px;background:#eef0f3;color:#0d1219;display:grid;place-items:center;font:600 34px/1 "Source Serif 4",serif}
.eyebrow{margin-top:auto;font-size:24px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:__ACCENT__}
h1{margin-top:14px;max-width:740px;font-weight:700;letter-spacing:-.025em;line-height:1.08}
.meta{margin-top:24px;font-size:28px;color:#b7bfc9}
</style></head><body>
<svg id="art" width="__W__" height="__H__" viewBox="0 0 __W__ __H__"></svg>
__OVERLAY__
<script>
const W=__W__, H=__H__, SEED=__SEED__, TEXTSIDE=__TEXTSIDE__, MOTIF="__MOTIF__", A="__ACCENT__";
let s=SEED>>>0; const rnd=()=>{s=(s+0x6D2B79F5)>>>0;let t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296};
const svg=document.getElementById('art'), NS='http://www.w3.org/2000/svg';
const el=(n,a,parent)=>{const e=document.createElementNS(NS,n);for(const k in a)e.setAttribute(k,a[k]);(parent||svg).appendChild(e);return e};
const B='#7fa6dc';                       // secondary line colour
const CX = TEXTSIDE ? W*0.8 : W*0.5;     // on covers the motif lives in the right third, clear of the title
const S = TEXTSIDE ? W*0.42 : Math.min(W, H*2.4);   // motif scale
const XL = TEXTSIDE ? W*0.6 : 0;         // left edge for edge-to-edge motifs on covers
el('defs',{}).innerHTML=`<radialGradient id="bg" cx="${CX/W*100}%" cy="45%" r="80%"><stop offset="0" stop-color="#18253a"/><stop offset=".6" stop-color="#0f1824"/><stop offset="1" stop-color="#0a0e14"/></radialGradient>
<radialGradient id="tint" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="${A}" stop-opacity=".22"/><stop offset="1" stop-color="${A}" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="${A}" stop-opacity=".7"/><stop offset="1" stop-color="${A}" stop-opacity="0"/></radialGradient>
<marker id="arw" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="${A}"/></marker>`;
el('rect',{width:W,height:H,fill:'url(#bg)'});
el('ellipse',{cx:CX,cy:H*0.48,rx:S*0.42,ry:H*0.75,fill:'url(#tint)'});
const dot=(x,y,r,o)=>el('circle',{cx:x,cy:y,r,fill:'#d7e4f6','fill-opacity':o});
const hot=(x,y,r)=>{el('circle',{cx:x,cy:y,r:r*6,fill:'url(#glow)'});el('circle',{cx:x,cy:y,r,fill:A})};
const line=(x1,y1,x2,y2,c,o,w,extra)=>el('line',Object.assign({x1,y1,x2,y2,stroke:c,'stroke-opacity':o,'stroke-width':w||1},extra||{}));
const path=(d,c,o,w,extra)=>el('path',Object.assign({d,fill:'none',stroke:c,'stroke-opacity':o,'stroke-width':w||1,'stroke-linecap':'round'},extra||{}));

const M = {
graph(){ const N=Math.round(W*H/7000), pts=[];
  for(let i=0;i<N;i++){let x=rnd(); if(TEXTSIDE) x=Math.pow(x,.55); pts.push({x:x*W,y:rnd()*H,r:1.5+rnd()*2.5,h:rnd()<.07})}
  for(const p of pts){for(const [q,d] of pts.map(q=>[q,(q.x-p.x)**2+(q.y-p.y)**2]).filter(a=>a[1]>0).sort((a,b)=>a[1]-b[1]).slice(0,3)){
    if(d>(W/5)**2)continue; line(p.x,p.y,q.x,q.y,p.h&&q.h?A:B,p.h&&q.h?.7:.14+.16*(p.x/W))}}
  for(const p of pts) p.h?hot(p.x,p.y,p.r+1.5):dot(p.x,p.y,p.r,.25+.5*(p.x/W)) },

rings(){ // nested harness layers around a core
  const cy=H*0.5, n=7;
  for(let i=n;i>=1;i--){ const w=S*0.09*i*1.25, h=H*0.105*i, r=Math.min(w,h)*0.22;
    el('rect',{x:CX-w,y:cy-h,width:2*w,height:2*h,rx:r,fill:'none',stroke:i===1?A:B,'stroke-opacity':i===1?.9:.10+.32*(1-i/n),'stroke-width':i===1?2:1.2});
    const k=3+Math.floor(rnd()*4);
    for(let j=0;j<k;j++){ const side=Math.floor(rnd()*4), t=rnd(); let x,y;
      if(side===0){x=CX-w+t*2*w;y=cy-h} else if(side===1){x=CX+w;y=cy-h+t*2*h} else if(side===2){x=CX-w+t*2*w;y=cy+h} else {x=CX-w;y=cy-h+t*2*h}
      if(i>1 && rnd()<.35){ const ix=CX+(x-CX)*(i-1)/i, iy=cy+(y-cy)*(i-1)/i; line(x,y,ix,iy,A,.45,1.2,{'stroke-dasharray':'3 4'}) }
      i<=2||(!TEXTSIDE&&rnd()<.2) ? hot(x,y,2.6) : el('rect',{x:x-3,y:y-3,width:6,height:6,rx:1.5,fill:'#d7e4f6','fill-opacity':.55}) } }
  el('circle',{cx:CX,cy,r:S*0.06,fill:'url(#glow)'});
  for(let j=0;j<3;j++) el('rect',{x:CX-S*0.05,y:cy-H*0.04+j*H*0.035,width:S*(0.1-j*0.025),height:H*0.012,rx:H*0.006,fill:'#eef0f3','fill-opacity':.85}) },

split(){ // neural (organic) meets symbolic (grid)
  const mid=TEXTSIDE?W*0.74:W*0.5, sp=TEXTSIDE?W*0.04:S*0.055;
  const left=[]; for(let i=0;i<Math.round(W*H/9000);i++){ const x=XL+rnd()*(mid-XL), y=rnd()*H; left.push({x,y,r:1.5+rnd()*3}) }
  for(const p of left){ for(const [q,d] of left.map(q=>[q,(q.x-p.x)**2+(q.y-p.y)**2]).filter(a=>a[1]>0).sort((a,b)=>a[1]-b[1]).slice(0,2)){
    const mx=(p.x+q.x)/2+(rnd()-.5)*40, my=(p.y+q.y)/2+(rnd()-.5)*40; path(`M${p.x},${p.y} Q${mx},${my} ${q.x},${q.y}`,B,.22) } dot(p.x,p.y,p.r,.5) }
  const cols=[]; for(let x=mid+sp*0.6;x<W+sp;x+=sp) cols.push(x);
  for(let y=sp*0.5;y<H+sp;y+=sp) for(const x of cols){ line(x,y,x+sp,y,A,.22); line(x,y,x,y+sp,A,.22); el('rect',{x:x-3,y:y-3,width:6,height:6,fill:A,'fill-opacity':.75}) }
  line(mid,0,mid,H,A,.6,1.5,{'stroke-dasharray':'6 6'});
  for(let k=0;k<5;k++){ const p=left[Math.floor(rnd()*left.length)], y=Math.round((p.y-sp*0.5)/sp)*sp+sp*0.5; path(`M${p.x},${p.y} C${(p.x+mid)/2},${p.y} ${(p.x+mid)/2},${y} ${cols[0]},${y}`,A,.6,1.4); hot(cols[0],y,3) } },

flow(){ // calls streaming between endpoints
  const x0=TEXTSIDE?XL:W*0.08, x1=W*0.94, n=18;
  const ends=(k,x)=>Array.from({length:k},(_,i)=>({x,y:H*(0.12+0.76*(i+0.5)/k)}));
  const L=ends(6,x0), R=ends(9,x1);
  for(let i=0;i<n;i++){ const a=L[Math.floor(rnd()*L.length)], b=R[Math.floor(rnd()*R.length)], c=i<4;
    const p=path(`M${a.x},${a.y} C${a.x+(b.x-a.x)*0.5},${a.y} ${a.x+(b.x-a.x)*0.5},${b.y} ${b.x},${b.y}`,c?A:B,c?.8:.22,c?2:1.2);
    const len=p.getTotalLength(); for(let t=0.15;t<1;t+=0.18+rnd()*0.2){ const q=p.getPointAtLength(len*t); c?hot(q.x,q.y,2.2):dot(q.x,q.y,1.8,.6) } }
  for(const e of L) el('rect',{x:e.x-9,y:e.y-9,width:18,height:18,rx:5,fill:'#0f1824',stroke:A,'stroke-width':1.5});
  for(const e of R) el('rect',{x:e.x-7,y:e.y-7,width:14,height:14,rx:4,fill:'#0f1824',stroke:B,'stroke-opacity':.7,'stroke-width':1.2}) },

loop(){ // reinforcing feedback loop
  const cy=H*0.5, rx=S*0.3, ry=H*0.34;
  for(let k=3;k>=1;k--) el('ellipse',{cx:CX,cy,rx:rx*(1+k*0.16),ry:ry*(1+k*0.16),fill:'none',stroke:B,'stroke-opacity':.08+.04*(3-k),'stroke-dasharray':k===2?'3 7':''});
  const nodes=5, pts=[];
  for(let i=0;i<nodes;i++){ const a=-Math.PI/2+i*2*Math.PI/nodes; pts.push([CX+rx*Math.cos(a),cy+ry*Math.sin(a)]) }
  for(let i=0;i<nodes;i++){ const a1=-Math.PI/2+i*2*Math.PI/nodes+0.2, a2=a1+2*Math.PI/nodes-0.4;
    path(`M${CX+rx*Math.cos(a1)},${cy+ry*Math.sin(a1)} A${rx},${ry} 0 0 1 ${CX+rx*Math.cos(a2)},${cy+ry*Math.sin(a2)}`,A,.9,2.6,{'marker-end':'url(#arw)'}) }
  for(const [x,y] of pts){ el('rect',{x:x-S*0.04,y:y-H*0.035,width:S*0.08,height:H*0.07,rx:8,fill:'#111b28',stroke:B,'stroke-opacity':.6,'stroke-width':1.2});
    el('rect',{x:x-S*0.026,y:y-H*0.006,width:S*0.052,height:H*0.012,rx:3,fill:'#d7e4f6','fill-opacity':.6}) }
  el('circle',{cx:CX,cy,r:S*0.05,fill:'none',stroke:A,'stroke-opacity':.7,'stroke-width':1.5,'stroke-dasharray':'4 5'});
  hot(CX,cy,4) },

fabric(){ // switch fabric with highlighted paths
  const sp=TEXTSIDE?W*0.04:S*0.05, x0=TEXTSIDE?XL:sp*0.5, nodes=[];
  for(let y=sp*0.6;y<H;y+=sp) for(let x=x0;x<W+sp;x+=sp){ nodes.push([x,y]); line(x,y,x+sp,y,B,.12); line(x,y,x,y+sp,B,.12); el('rect',{x:x-2.5,y:y-2.5,width:5,height:5,fill:'#d7e4f6','fill-opacity':.3}) }
  for(let k=0;k<5;k++){ let x=x0, y=sp*0.6+Math.floor(rnd()*(H/sp))*sp, d=`M${x},${y}`;
    while(x<W){ if(rnd()<.6) x+=sp; else y=Math.max(sp*0.6,Math.min(H-sp*0.4,y+(rnd()<.5?-sp:sp))); d+=` L${x},${y}` }
    path(d,A,.75,2.2,{'stroke-linejoin':'round'}); hot(x0,Number(d.split(' ')[0].split(',')[1]),3) } },

waves(){ // control-plane telemetry
  const n=16, x0=XL;
  for(let i=0;i<n;i++){ const base=H*(0.08+0.84*i/(n-1)), amp=H*0.01+rnd()*H*0.025, f=0.004+rnd()*0.01, ph=rnd()*6; let d='';
    for(let x=x0;x<=W;x+=6){ const y=base+amp*Math.sin(x*f+ph)+amp*0.4*Math.sin(x*f*3.1+ph*2); d+=(d?' L':'M')+x+','+y.toFixed(1) }
    path(d,B,.10+.16*(i%3===0),1.2) }
  const base=H*0.52; let d='', spikes=[];
  for(let x=x0;x<=W;x+=4){ let y=base+H*0.012*Math.sin(x*0.02);
    const k=((x-x0)%(W*0.18)); if(k<12) y-=H*0.28*Math.sin(k/12*Math.PI); else if(k<20) y+=H*0.1*Math.sin((k-12)/8*Math.PI);
    if(k<4) spikes.push(x); d+=(d?' L':'M')+x+','+y.toFixed(1) }
  path(d,A,.9,2.4,{'stroke-linejoin':'round'});
  for(const x of spikes) hot(x+6,base-H*0.28,3) },

clos(){ // tiered Clos / fat-tree
  const tiers=TEXTSIDE?[3,6,10,14]:[4,8,16,24], x0=TEXTSIDE?XL:W*0.06, x1=W*0.95, ys=[0.16,0.4,0.64,0.86].map(t=>t*H), T=[];
  tiers.forEach((n,i)=>{ T.push(Array.from({length:n},(_,j)=>[x0+(x1-x0)*(j+0.5)/n,ys[i]])) });
  for(let i=0;i<3;i++) for(const [ax,ay] of T[i]) for(const [bx,by] of T[i+1]) if(Math.abs(bx-ax)<(x1-x0)*(i===0?0.6:0.22)) line(ax,ay,bx,by,B,.10);
  let cur=T[0][Math.floor(rnd()*4)];
  for(let i=1;i<4;i++){ const cand=T[i].filter(([x])=>Math.abs(x-cur[0])<(x1-x0)*0.2); const nx=cand[Math.floor(rnd()*cand.length)]; line(cur[0],cur[1],nx[0],nx[1],A,.85,2.2); cur=nx }
  T.forEach((row,i)=>row.forEach(([x,y])=>{ const w=[26,20,14,9][i]; el('rect',{x:x-w/2,y:y-w*0.4,width:w,height:w*0.8,rx:3,fill:'#122033',stroke:i===0?A:B,'stroke-opacity':i===0?.9:.55,'stroke-width':1.2}) })) },
};
(M[MOTIF]||M.graph)();
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
    return get("title"), get("date"), cats, {"cover_motif": get("cover_motif"), "cover_accent": get("cover_accent")}


MOTIFS = ["graph", "rings", "split", "flow", "loop", "fabric", "waves", "clos"]
ACCENTS = {"violet": "#a78bfa", "teal": "#2dd4bf", "blue": "#60a5fa", "orange": "#fb8a4c",
           "green": "#4ade80", "amber": "#fbbf24", "pink": "#f472b6"}


def style_for(slug, fm):
    """Front matter can set cover_motif and cover_accent; otherwise pick from the slug."""
    h = int(hashlib.sha256(slug.encode()).hexdigest()[8:16], 16)
    motif = fm.get("cover_motif") or MOTIFS[h % len(MOTIFS)]
    accent = fm.get("cover_accent") or list(ACCENTS)[(h // 7) % len(ACCENTS)]
    return motif, ACCENTS.get(accent, accent)


def title_size(title):
    n = len(title)
    return 84 if n <= 30 else 72 if n <= 55 else 60 if n <= 80 else 52


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
            title, date, cats, fm = front_matter(md.read_text(encoding="utf-8"))
            motif, accent = style_for(slug, fm)
            seed = int(hashlib.sha256(slug.encode()).hexdigest()[:8], 16)
            when = datetime.date.fromisoformat(date[:10]).strftime("%B %-d, %Y") if date else ""
            jobs = [("hero.jpg", 1200, 450, 2, "", 0),
                    ("cover.jpg", 1200, 630, 2, OVERLAY.replace("__EYEBROW__", html.escape(" · ".join(cats) or "Writing"))
                        .replace("__TITLE__", html.escape(title)).replace("__SIZE__", str(title_size(title)))
                        .replace("__DATE__", html.escape(when)), 1)]
            for name, w, h, scale, overlay, textside in jobs:
                out = md.parent / name
                if out.exists() and not args.force:
                    print(f"keep   {out.relative_to(ROOT)}"); continue
                page = (PAGE.replace("__W__", str(w)).replace("__H__", str(h)).replace("__SEED__", str(seed))
                        .replace("__TEXTSIDE__", str(textside)).replace("__OVERLAY__", overlay)
                        .replace("__MOTIF__", motif).replace("__ACCENT__", accent))
                p = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
                p.set_content(page, wait_until="networkidle")
                p.evaluate("document.fonts.ready")
                p.screenshot(path=str(out), type="jpeg", quality=95)
                p.close()
                print(f"wrote  {out.relative_to(ROOT)}")
        browser.close()


if __name__ == "__main__":
    sys.exit(main())
