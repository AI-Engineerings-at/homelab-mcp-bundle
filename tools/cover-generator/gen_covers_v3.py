#!/usr/bin/env python3
import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("/home/joe/cli_bridge/products/cover-templates")

PRODUCTS = [
    {
        "id": "localai-playbook",
        "accent": "#10B981", "accent_dark": "#059669",
        "gradient": "linear-gradient(135deg, #020817 0%, #0a1628 40%, #041a10 100%)",
        "badge": "Bestseller 2025", "eyebrow": "The Complete Guide",
        "title": "Local <em>AI Stack</em><br>Playbook",
        "subtitle": "Run your own AI infrastructure with Ollama, n8n &amp; Docker — fully private, zero cloud costs.",
        "features": ["🐳 Docker Swarm","🤖 Ollama GPU","⚡ n8n Automation","🔒 100% Private"],
        "stats": [("180+","Pages"),("42","Diagrams"),("15+","Services")],
        "price": "EUR 49", "icon": "🧠",
    },
    {
        "id": "n8n-starter-bundle",
        "accent": "#FB923C", "accent_dark": "#EA580C",
        "gradient": "linear-gradient(135deg, #0c0800 0%, #1a0f00 40%, #0c0800 100%)",
        "badge": "Most Popular", "eyebrow": "Workflow Automation",
        "title": "<em>n8n</em> Starter<br>Bundle",
        "subtitle": "30+ ready-to-use workflows for AI automation, lead gen &amp; business ops. Plug-and-play.",
        "features": ["⚡ 30+ Workflows","🤖 AI Nodes","📧 Email &amp; CRM","🔗 500+ Integrations"],
        "stats": [("30+","Workflows"),("500+","Integrations"),("10min","Setup")],
        "price": "EUR 29", "icon": "⚡",
    },
    {
        "id": "grafana-dashboard-pack",
        "accent": "#60A5FA", "accent_dark": "#2563EB",
        "gradient": "linear-gradient(135deg, #020817 0%, #0a1220 40%, #020817 100%)",
        "badge": "Pro Quality", "eyebrow": "Infrastructure Monitoring",
        "title": "Grafana<br><em>Dashboard</em> Pack",
        "subtitle": "Beautiful, production-ready dashboards for Docker, Node Exporter &amp; self-hosted stacks.",
        "features": ["📊 12 Dashboards","🐳 Docker Metrics","⚡ Real-time Alerts","📦 Import Ready"],
        "stats": [("12","Dashboards"),("50+","Panels"),("5min","Import")],
        "price": "EUR 39", "icon": "📊",
    },
    {
        "id": "dsgvo-art30-bundle",
        "accent": "#C084FC", "accent_dark": "#9333EA",
        "gradient": "linear-gradient(135deg, #080010 0%, #120020 40%, #080010 100%)",
        "badge": "Legal Compliance", "eyebrow": "DSGVO Art. 30 VVT",
        "title": "DSGVO Art.30<br><em>Bundle</em>",
        "subtitle": "Vollständige Vorlagen für das Verzeichnis von Verarbeitungstätigkeiten — DSGVO-konform.",
        "features": ["📋 VVT Templates","🔐 Datenschutz","⚖️ Art. 30 konform","📝 Sofort nutzbar"],
        "stats": [("15+","Templates"),("100%","DSGVO"),("DE/AT","Recht")],
        "price": "EUR 79", "icon": "⚖️",
    },
    {
        "id": "homelab-mcp-bundle",
        "accent": "#22D3EE", "accent_dark": "#0891B2",
        "gradient": "linear-gradient(135deg, #020b0d 0%, #031520 40%, #020b0d 100%)",
        "badge": "Free · Open Source", "eyebrow": "MCP Server Collection",
        "title": "Homelab<br><em>MCP</em> Bundle",
        "subtitle": "8 production-ready MCP servers for your homelab: Grafana, n8n, Portainer, Proxmox &amp; more.",
        "features": ["🔌 8 MCP Servers","51 Tools","🏠 Homelab Ready","🤖 Claude Compatible"],
        "stats": [("8","MCP Servers"),("51","Tools"),("0€","Free")],
        "price": "FREE", "icon": "🔌",
    },
    {
        "id": "ai-agent-blueprint",
        "accent": "#4ADE80", "accent_dark": "#16A34A",
        "gradient": "linear-gradient(135deg, #010d02 0%, #021508 40%, #010d02 100%)",
        "badge": "New Release", "eyebrow": "Multi-Agent Architecture",
        "title": "AI Agent Team<br><em>Blueprint</em>",
        "subtitle": "Design and deploy your own AI agent team — Manager, Specialists &amp; Automation in one system.",
        "features": ["🤖 Multi-Agent","🏗️ Architecture","⚡ n8n + Claude","📐 Templates"],
        "stats": [("10+","Agents"),("7","Blueprints"),("1-Click","Deploy")],
        "price": "EUR 19", "icon": "🤖",
    },
    {
        "id": "mcp-cheat-sheet",
        "accent": "#22D3EE", "accent_dark": "#0891B2",
        "gradient": "linear-gradient(135deg, #020b0d 0%, #031520 40%, #020b0d 100%)",
        "badge": "Lead Magnet · Free", "eyebrow": "Quick Reference Card",
        "title": "MCP<br><em>Cheat Sheet</em>",
        "subtitle": "Everything you need to know about Model Context Protocol — tools, resources &amp; prompts at a glance.",
        "features": ["📋 All MCP Concepts","🔧 Tool Examples","🚀 Quick Setup","🤖 Claude Ready"],
        "stats": [("1 Page","Reference"),("MCP","Protocol"),("Free","Download")],
        "price": "FREE", "icon": "📋",
    },
]

TMPL = '''<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { width:800px; height:800px; overflow:hidden; font-family:'Inter','Segoe UI',sans-serif; }
.wrap { width:800px; height:800px; background: GRADIENT; position:relative; overflow:hidden; }
.orb1 { position:absolute; width:600px; height:600px; background:radial-gradient(circle,ACCENT22 0%,transparent 65%); top:-150px; left:-150px; z-index:2; }
.orb2 { position:absolute; width:450px; height:450px; background:radial-gradient(circle,ACCENT11 0%,transparent 65%); bottom:-100px; right:-100px; z-index:2; }
.grid { position:absolute; inset:0; background-image:linear-gradient(ACCENT0a 1px,transparent 1px),linear-gradient(90deg,ACCENT0a 1px,transparent 1px); background-size:55px 55px; z-index:3; }
.corner { position:absolute; top:0; right:0; width:220px; height:220px; border-left:1px solid ACCENT30; border-bottom:1px solid ACCENT30; border-bottom-left-radius:220px; z-index:5; }
.lline { position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(to bottom,transparent,ACCENT,transparent); z-index:5; }
.content { position:absolute; inset:0; z-index:10; display:flex; flex-direction:column; padding:44px 52px 44px 56px; }
.toprow { display:flex; align-items:center; justify-content:space-between; margin-bottom:36px; }
.badge { display:inline-flex; align-items:center; gap:7px; background:ACCENT20; border:1px solid ACCENT50; border-radius:100px; padding:6px 16px; color:ACCENT; font-size:11.5px; font-weight:600; letter-spacing:.07em; text-transform:uppercase; }
.bdot { width:5px; height:5px; background:ACCENT; border-radius:50%; }
.ibox { width:44px; height:44px; background:ACCENT18; border:1px solid ACCENT35; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:20px; }
.ey { color:ACCENT; font-size:12.5px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; margin-bottom:14px; }
.title { font-family:'Space Grotesk',sans-serif; font-size:66px; font-weight:700; line-height:1.04; color:#F8FAFC; letter-spacing:-.02em; margin-bottom:22px; }
.title em { color:ACCENT; font-style:normal; }
.sub { font-size:16.5px; color:rgba(248,250,252,.55); line-height:1.65; max-width:470px; margin-bottom:36px; }
.feats { display:flex; gap:9px; flex-wrap:wrap; }
.feat { background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.11); border-radius:6px; padding:7px 14px; color:rgba(248,250,252,.8); font-size:13px; font-weight:500; }
.sp { flex:1; }
.div { height:1px; background:linear-gradient(to right,ACCENT40,transparent); margin-bottom:24px; }
.bot { display:flex; align-items:center; justify-content:space-between; }
.stats { display:flex; gap:36px; }
.snum { font-size:24px; font-weight:700; color:ACCENT; line-height:1; }
.slbl { font-size:10.5px; color:rgba(255,255,255,.35); margin-top:4px; text-transform:uppercase; letter-spacing:.06em; }
.price { background:linear-gradient(135deg,ACCENT,ACCENT_DARK); border-radius:12px; padding:13px 30px; font-size:28px; font-weight:800; color:#fff; }
.brand { font-size:11px; color:rgba(255,255,255,.2); letter-spacing:.1em; text-transform:uppercase; margin-top:3px; }
</style></head><body>
<div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="grid"></div>
<div class="corner"></div><div class="lline"></div>
<div class="content">
  <div class="toprow"><div class="badge"><span class="bdot"></span>BADGE</div><div class="ibox">ICON</div></div>
  <div class="ey">EYEBROW</div>
  <div class="title">TITLE</div>
  <div class="sub">SUBTITLE</div>
  <div class="feats">FEATURES</div>
  <div class="sp"></div>
  <div class="div"></div>
  <div class="bot">
    <div class="stats">STATS</div>
    <div style="text-align:right"><div class="price">PRICE</div><div class="brand">ai-engineering.at</div></div>
  </div>
</div></div></body></html>'''

def render(p, out_dir):
    feats = " ".join(f'<div class="feat">{f}</div>' for f in p["features"])
    stats = " ".join(f'<div><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"])
    
    a = p["accent"]
    # Build alpha versions for inline use
    html = TMPL
    html = html.replace("GRADIENT", p["gradient"])
    html = html.replace("ACCENT_DARK", p["accent_dark"])
    html = html.replace("ACCENT22", a + "22")
    html = html.replace("ACCENT11", a + "11")
    html = html.replace("ACCENT0a", a + "0a")
    html = html.replace("ACCENT30", a + "30")
    html = html.replace("ACCENT50", a + "50")
    html = html.replace("ACCENT20", a + "20")
    html = html.replace("ACCENT18", a + "18")
    html = html.replace("ACCENT35", a + "35")
    html = html.replace("ACCENT40", a + "40")
    html = html.replace("ACCENT", a)
    html = html.replace("BADGE", p["badge"])
    html = html.replace("ICON", p["icon"])
    html = html.replace("EYEBROW", p["eyebrow"])
    html = html.replace("SUBTITLE", p["subtitle"])
    html = html.replace("TITLE", p["title"])
    html = html.replace("FEATURES", feats)
    html = html.replace("STATS", stats)
    html = html.replace("PRICE", p["price"])
    
    hp = f"/tmp/cv3-{p['id']}.html"
    op = out_dir / f"{p['id']}-cover.png"
    with open(hp, "w") as f:
        f.write(html)
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--no-sandbox","--disable-setuid-sandbox","--disable-web-security"])
        pg = br.new_page(viewport={"width":800,"height":800})
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(2500)
        pg.screenshot(path=str(op), clip={"x":0,"y":0,"width":800,"height":800})
        br.close()
    print(f"  ✓ {p['id']}: {os.path.getsize(op)//1024}KB")
    return op

ids = sys.argv[1:] if len(sys.argv)>1 else None
products = [p for p in PRODUCTS if ids is None or p["id"] in ids]
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"Generiere {len(products)} Cover...")
for p in products:
    render(p, OUTPUT_DIR)
print("Fertig!")
