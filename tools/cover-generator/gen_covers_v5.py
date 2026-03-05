#!/usr/bin/env python3
"""
Cover Generator v5 -- Product Image Showcase Design

800x800 covers with product thumbnail as floating card on the right.

Usage:
  python3 gen_covers_v5.py                  # all 7 products
  python3 gen_covers_v5.py localai-playbook  # single product
  python3 gen_covers_v5.py --list            # list products + thumb status
  python3 gen_covers_v5.py --dry-run         # HTML only, no screenshot
"""
import os, sys, base64, argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("/home/joe/cli_bridge/products/cover-templates")
THUMB_DIR  = Path("/home/joe/cli_bridge/products/cover-templates")
EAGLE_PATH = Path("/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png")

PRODUCTS = [
    {"id":"localai-playbook","accent":"#10B981","accent_dark":"#059669",
     "gradient":"linear-gradient(145deg,#020817 0%,#0a1628 45%,#041a10 100%)",
     "badge":"Bestseller 2025","eyebrow":"The Complete Guide",
     "title":"Local <em>AI&nbsp;Stack</em><br>Playbook",
     "subtitle":"Run your own AI infrastructure — fully private, zero cloud costs.",
     "features":["Docker Swarm","Ollama GPU","n8n Automation","100% Private"],
     "stats":[("180+","Pages"),("42","Diagrams"),("15+","Services")],
     "price":"EUR 49","icon":"🧠","thumb":"thumbnail-localai-playbook.png"},
    {"id":"n8n-starter-bundle","accent":"#FB923C","accent_dark":"#EA580C",
     "gradient":"linear-gradient(145deg,#0c0800 0%,#1a1000 45%,#0c0800 100%)",
     "badge":"Most Popular","eyebrow":"Workflow Automation",
     "title":"<em>n8n</em> Starter<br>Bundle",
     "subtitle":"30+ ready-to-use workflows for AI automation, lead gen &amp; business ops.",
     "features":["30+ Workflows","AI Nodes","Email &amp; CRM","500+ Integrations"],
     "stats":[("30+","Workflows"),("500+","Integrations"),("10min","Setup")],
     "price":"EUR 29","icon":"⚡","thumb":"thumbnail-n8n-starter-bundle.png"},
    {"id":"grafana-dashboard-pack","accent":"#60A5FA","accent_dark":"#2563EB",
     "gradient":"linear-gradient(145deg,#020817 0%,#0a1220 45%,#020817 100%)",
     "badge":"Pro Quality","eyebrow":"Infrastructure Monitoring",
     "title":"Grafana<br><em>Dashboard</em>&nbsp;Pack",
     "subtitle":"Production-ready dashboards for Docker, Node Exporter &amp; self-hosted stacks.",
     "features":["12 Dashboards","Docker Metrics","Real-time Alerts","Import Ready"],
     "stats":[("12","Dashboards"),("50+","Panels"),("5min","Import")],
     "price":"EUR 39","icon":"📊","thumb":"thumbnail-grafana-dashboard-pack.png"},
    {"id":"dsgvo-art30-bundle","accent":"#C084FC","accent_dark":"#9333EA",
     "gradient":"linear-gradient(145deg,#080010 0%,#120020 45%,#080010 100%)",
     "badge":"Legal Compliance","eyebrow":"DSGVO Art. 30 VVT",
     "title":"DSGVO&nbsp;Art.30<br><em>Bundle</em>",
     "subtitle":"Vollstaendige Vorlagen fuer das Verzeichnis von Verarbeitungstaetigkeiten.",
     "features":["VVT Templates","Art.30 konform","DE/AT Recht","Sofort nutzbar"],
     "stats":[("15+","Templates"),("100%","DSGVO"),("DE/AT","Recht")],
     "price":"EUR 79","icon":"⚖️","thumb":"thumbnail-dsgvo-art30-bundle.png"},
    {"id":"homelab-mcp-bundle","accent":"#22D3EE","accent_dark":"#0891B2",
     "gradient":"linear-gradient(145deg,#020b0d 0%,#031520 45%,#020b0d 100%)",
     "badge":"Free · Open Source","eyebrow":"MCP Server Collection",
     "title":"Homelab<br><em>MCP</em>&nbsp;Bundle",
     "subtitle":"8 production-ready MCP servers: Grafana, n8n, Portainer, Proxmox &amp; more.",
     "features":["8 MCP Servers","51 Tools","Homelab Ready","Claude Compatible"],
     "stats":[("8","MCP Servers"),("51","Tools"),("0€","Free")],
     "price":"FREE","icon":"🔌","thumb":"thumbnail-homelab-mcp-bundle.png"},
    {"id":"ai-agent-blueprint","accent":"#4ADE80","accent_dark":"#16A34A",
     "gradient":"linear-gradient(145deg,#010d02 0%,#021508 45%,#010d02 100%)",
     "badge":"New Release","eyebrow":"Multi-Agent Architecture",
     "title":"AI Agent Team<br><em>Blueprint</em>",
     "subtitle":"Design and deploy your own AI agent team — Manager, Specialists &amp; Automation.",
     "features":["Multi-Agent","Architecture","n8n + Claude","Templates"],
     "stats":[("10+","Agents"),("7","Blueprints"),("1-Click","Deploy")],
     "price":"EUR 19","icon":"🤖","thumb":"thumbnail-ai-agent-blueprint.png"},
    {"id":"mcp-cheat-sheet","accent":"#22D3EE","accent_dark":"#0891B2",
     "gradient":"linear-gradient(145deg,#020b0d 0%,#031520 45%,#020b0d 100%)",
     "badge":"Lead Magnet · Free","eyebrow":"Quick Reference Card",
     "title":"MCP<br><em>Cheat&nbsp;Sheet</em>",
     "subtitle":"Everything about Model Context Protocol -- tools, resources &amp; prompts.",
     "features":["All MCP Concepts","Tool Examples","Quick Setup","Claude Ready"],
     "stats":[("1 Page","Reference"),("MCP","Protocol"),("Free","Download")],
     "price":"FREE","icon":"📋","thumb":"cover-mcp-cheat-sheet.png"},
]


def load_b64(path):
    if path.exists() and path.stat().st_size > 0:
        ext  = path.suffix.lower().lstrip(".")
        mime = "image/png" if ext == "png" else "image/jpeg"
        with open(path,"rb") as f:
            return f"data:{mime};base64,"+base64.b64encode(f.read()).decode()
    return ""

def css_vars(p):
    a,d = p["accent"],p["accent_dark"]
    return (f"--accent:{a};--accent-dark:{d};"
            f"--a08:{a}08;--a0a:{a}0a;--a10:{a}10;--a15:{a}15;--a18:{a}18;"
            f"--a20:{a}20;--a30:{a}30;--a35:{a}35;--a40:{a}40;--a50:{a}50;")

def resolve_thumb(p):
    for path in [THUMB_DIR/p.get("thumb",""),
                 THUMB_DIR/f"thumbnail-{p['id']}.png",
                 THUMB_DIR/f"{p['id']}-cover.png",
                 THUMB_DIR/f"cover-{p['id']}.png"]:
        b = load_b64(path)
        if b: return b
    return ""

def build_cover(p):
    eagle = load_b64(EAGLE_PATH)
    thumb = resolve_thumb(p)
    feats = "".join(f'<div class="feat">{f}</div>' for f in p["features"])
    stats = "".join(f'<div class="stat"><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"])
    eagle_html = (f'<div style="position:absolute;width:360px;height:360px;top:50%;right:-20px;'
                  f'transform:translateY(-50%);opacity:0.07;z-index:4;">'
                  f'<img src="{eagle}" style="width:100%;height:100%;object-fit:contain" alt=""></div>') if eagle else ""
    if thumb:
        thumb_html=(f'<div class="thumb-wrap"><div class="thumb-glow"></div>'
                    f'<div class="thumb-card"><img src="{thumb}" class="thumb-img" alt="{p["id"]}"></div></div>')
    else:
        thumb_html=(f'<div class="thumb-wrap"><div class="thumb-glow"></div>'
                    f'<div class="thumb-card thumb-fallback">'
                    f'<div style="font-size:100px;line-height:1">{p["icon"]}</div>'
                    f'<div style="font-size:14px;color:var(--accent);margin-top:18px;font-weight:700;'
                    f'letter-spacing:.1em;text-transform:uppercase">{p["eyebrow"]}</div></div></div>')
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}:root{{{css_vars(p)}}}
body{{width:800px;height:800px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:800px;height:800px;background:{p['gradient']};position:relative;overflow:hidden;display:flex}}
.orb1{{position:absolute;width:540px;height:540px;background:radial-gradient(circle,var(--a18) 0%,transparent 65%);top:-150px;left:-90px;z-index:2}}
.orb2{{position:absolute;width:400px;height:400px;background:radial-gradient(circle,var(--a10) 0%,transparent 65%);bottom:-110px;right:60px;z-index:2}}
.gbg{{position:absolute;inset:0;background-image:linear-gradient(var(--a0a) 1px,transparent 1px),linear-gradient(90deg,var(--a0a) 1px,transparent 1px);background-size:46px 46px;z-index:3}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:6}}
.corner{{position:absolute;top:0;left:0;width:150px;height:150px;border-right:1px solid var(--a30);border-bottom:1px solid var(--a30);border-bottom-right-radius:150px;z-index:5}}
.vdiv{{position:absolute;left:432px;top:8%;bottom:8%;width:1px;background:linear-gradient(to bottom,transparent,var(--a35),transparent);z-index:6}}
.left{{position:relative;z-index:10;width:432px;min-width:432px;display:flex;flex-direction:column;padding:40px 22px 38px 44px}}
.brand-row{{display:flex;align-items:center;justify-content:space-between;margin-bottom:28px}}
.brand-name{{font-size:10px;font-weight:700;color:#475569;letter-spacing:2px;text-transform:uppercase}}
.badge{{display:inline-flex;align-items:center;gap:6px;background:var(--a18);border:1px solid var(--a50);border-radius:100px;padding:5px 13px;color:var(--accent);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}}
.bdot{{width:4px;height:4px;background:var(--accent);border-radius:50%}}
.ey{{color:var(--accent);font-size:10.5px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;margin-bottom:11px}}
.title{{font-family:'Space Grotesk',sans-serif;font-size:54px;font-weight:800;line-height:1.04;letter-spacing:-.02em;color:#F8FAFC;margin-bottom:14px}}
.title em{{color:var(--accent);font-style:normal}}
.sub{{font-size:13px;color:rgba(248,250,252,.46);line-height:1.58;margin-bottom:20px;max-width:340px}}
.feats{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:auto}}
.feat{{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.10);border-radius:6px;padding:6px 11px;color:rgba(248,250,252,.78);font-size:11px;font-weight:500}}
.div{{height:1px;background:linear-gradient(to right,var(--a40),transparent);margin:18px 0}}
.bot{{display:flex;align-items:center;justify-content:space-between}}
.stats{{display:flex;gap:22px}}
.snum{{font-size:20px;font-weight:700;color:var(--accent);line-height:1}}
.slbl{{font-size:9px;color:rgba(255,255,255,.28);margin-top:3px;text-transform:uppercase;letter-spacing:.07em}}
.price{{background:linear-gradient(135deg,var(--accent),var(--accent-dark));border-radius:10px;padding:11px 20px;font-size:23px;font-weight:800;color:#fff}}
.brand-url{{font-size:8.5px;color:rgba(255,255,255,.18);letter-spacing:.14em;text-transform:uppercase;margin-top:4px;text-align:right}}
.right{{position:relative;z-index:10;flex:1;display:flex;align-items:center;justify-content:center;padding:20px 32px 20px 12px}}
.thumb-wrap{{position:relative;display:flex;align-items:center;justify-content:center}}
.thumb-card{{width:290px;height:290px;border-radius:14px;border:1px solid var(--a40);overflow:hidden;box-shadow:0 0 0 1px var(--a20),0 8px 40px rgba(0,0,0,.65),0 0 70px var(--a18);transform:perspective(900px) rotateY(-5deg) rotateX(2deg);background:#080808;display:flex;align-items:center;justify-content:center}}
.thumb-img{{width:100%;height:100%;object-fit:cover;display:block}}
.thumb-fallback{{flex-direction:column;background:var(--a08)}}
.thumb-glow{{position:absolute;width:260px;height:260px;background:radial-gradient(ellipse,var(--a30) 0%,transparent 70%);z-index:-1;filter:blur(28px)}}
</style></head><body><div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="gbg"></div>
{eagle_html}
<div class="lline"></div><div class="corner"></div><div class="vdiv"></div>
<div class="left">
  <div class="brand-row"><div class="brand-name">AI Engineering</div><div class="badge"><span class="bdot"></span>{p['badge']}</div></div>
  <div class="ey">{p['eyebrow']}</div>
  <div class="title">{p['title']}</div>
  <div class="sub">{p['subtitle']}</div>
  <div class="feats">{feats}</div>
  <div class="div"></div>
  <div class="bot"><div class="stats">{stats}</div><div><div class="price">{p['price']}</div><div class="brand-url">ai-engineering.at</div></div></div>
</div>
<div class="right">{thumb_html}</div>
</div></body></html>"""


def render(p, out_dir, dry_run=False):
    html = build_cover(p)
    hp = f"/tmp/cv5-{p['id']}.html"
    op = out_dir / f"{p['id']}-cover.png"
    with open(hp,"w",encoding="utf-8") as fh: fh.write(html)
    if dry_run:
        print(f"  DRY  {p['id']}  -> {hp}")
        return op
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--no-sandbox","--disable-setuid-sandbox","--disable-web-security","--disable-features=VizDisplayCompositor"])
        pg = br.new_page(viewport={"width":800,"height":800})
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(3000)
        pg.screenshot(path=str(op),clip={"x":0,"y":0,"width":800,"height":800})
        br.close()
    print(f"  ok  {p['id']:<32}  {os.path.getsize(op)//1024:>4}KB  ->  {op.name}")
    return op


def main():
    parser = argparse.ArgumentParser(description="Cover Generator v5 -- Product Image Showcase 800x800")
    parser.add_argument("products",nargs="*",help="Product IDs (default: all)")
    parser.add_argument("--out",default=str(OUTPUT_DIR))
    parser.add_argument("--list",action="store_true")
    parser.add_argument("--dry-run",action="store_true")
    args = parser.parse_args()
    if args.list:
        print(f"\n{'ID':<34} {'Price':<10} Accent    Thumb")
        print("-"*72)
        for p in PRODUCTS:
            tp = THUMB_DIR/p.get("thumb",f"thumbnail-{p['id']}.png")
            ok = "OK" if tp.exists() else "!!"
            print(f"  [{ok}] {p['id']:<32} {p['price']:<10} {p['accent']}  {p.get('thumb','')}")
        return
    ids = args.products or None
    products = [p for p in PRODUCTS if ids is None or p["id"] in ids]
    if not products:
        print(f"No products matched: {ids}"); sys.exit(1)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True,exist_ok=True)
    print(f"\nCover Generator v5  --  {len(products)} Produkt(e)  [800x800 + product image]\n")
    ok_count = 0
    for p in products:
        try: render(p,out_dir,dry_run=args.dry_run); ok_count+=1
        except Exception as e: print(f"  ERROR  {p['id']}: {e}")
    print(f"\n{ok_count}/{len(products)} Cover fertig  ->  {out_dir}")

if __name__ == "__main__":
    main()
