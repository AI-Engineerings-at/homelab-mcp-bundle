#!/usr/bin/env python3
"""
Cover Generator v4 — Gemini-powered professional covers
Uses Gemini API to generate a unique SVG hero per product, renders via Playwright.
800x800px output.

Usage:
    python3 gen_covers_gemini.py              # all products
    python3 gen_covers_gemini.py localai-playbook n8n-starter-bundle
"""
import sys, os, json, re, urllib.request
from pathlib import Path

OUTPUT_DIR = Path("/home/joe/cli_bridge/products/cover-templates")

def load_env():
    env = {}
    p = Path("/home/joe/cli_bridge/.env")
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env

ENV = load_env()
GEMINI_KEY = ENV.get("GEMINI_API_KEY", "")

PRODUCTS = [
    {
        "id": "localai-playbook",
        "filename": "localai-playbook-cover.png",
        "accent": "#10B981", "bg": "#020F0A",
        "category": "COMPLETE GUIDE",
        "title": "Local AI Stack\nPlaybook",
        "subtitle": "Run Ollama, n8n & Docker on your own hardware — fully private.",
        "features": ["Ollama GPU", "n8n Automation", "Docker Swarm"],
        "price": "EUR 49",
        "hero_hint": "terminal window (macOS style, 3 colored dots top-left) showing: '$ ollama run llama3.2' and response text, dark #0F172A background, green #10B981 text accents",
    },
    {
        "id": "n8n-starter-bundle",
        "filename": "n8n-starter-bundle-cover.png",
        "accent": "#FB923C", "bg": "#0A0500",
        "category": "WORKFLOW AUTOMATION",
        "title": "n8n Starter\nBundle",
        "subtitle": "30+ ready workflows for AI automation & business ops. Plug & play.",
        "features": ["30+ Workflows", "AI Nodes", "500+ Integrations"],
        "price": "EUR 29",
        "hero_hint": "n8n workflow diagram: 4 rounded-rect nodes (Webhook → AI Process → Email Send → Done) connected by curved arrows, orange #FB923C accent borders, dark bg",
    },
    {
        "id": "grafana-dashboard-pack",
        "filename": "grafana-dashboard-pack-cover.png",
        "accent": "#60A5FA", "bg": "#010810",
        "category": "INFRASTRUCTURE MONITORING",
        "title": "Grafana\nDashboard Pack",
        "subtitle": "Beautiful production-ready dashboards for Docker & self-hosted stacks.",
        "features": ["12 Dashboards", "50+ Panels", "5min Import"],
        "price": "EUR 39",
        "hero_hint": "Grafana-style dashboard panel: 3 metric cards (CPU 42%, RAM 67%, Uptime 99.9%) at top, then a small area chart in blue #60A5FA, dark panel bg #1E293B",
    },
    {
        "id": "dsgvo-art30-bundle",
        "filename": "dsgvo-art30-bundle-cover.png",
        "accent": "#C084FC", "bg": "#060010",
        "category": "LEGAL COMPLIANCE",
        "title": "DSGVO Art.30\nBundle",
        "subtitle": "Vollstaendige VVT-Vorlagen — DSGVO-konform, sofort einsatzbereit.",
        "features": ["15+ Templates", "Art.30 konform", "DE / AT Recht"],
        "price": "EUR 79",
        "hero_hint": "document mockup: A4-ish paper shape with 'Art. 30 VVT' header, 4 checklist rows with checkmarks, and a round compliance seal/stamp in bottom-right, purple accent",
    },
    {
        "id": "homelab-mcp-bundle",
        "filename": "homelab-mcp-bundle-cover.png",
        "accent": "#22D3EE", "bg": "#010C10",
        "category": "MCP SERVER COLLECTION",
        "title": "Homelab\nMCP Bundle",
        "subtitle": "8 production-ready MCP servers for Grafana, n8n, Portainer & more.",
        "features": ["8 MCP Servers", "51 Tools", "Free & Open Source"],
        "price": "FREE",
        "hero_hint": "3x3 grid of small rounded tiles, each showing a service name (Grafana, n8n, Portainer, Proxmox, Uptime, Mattermost, AdGuard, Ollama) with a simple icon shape, cyan #22D3EE borders",
    },
    {
        "id": "ai-agent-blueprint",
        "filename": "ai-agent-blueprint-cover.png",
        "accent": "#4ADE80", "bg": "#01080A",
        "category": "MULTI-AGENT ARCHITECTURE",
        "title": "AI Agent Team\nBlueprint",
        "subtitle": "Design & deploy your own AI agent team from scratch.",
        "features": ["10+ Agents", "7 Blueprints", "n8n + Claude"],
        "price": "EUR 19",
        "hero_hint": "org-chart hierarchy: one Manager node at top center, connected by lines down to 3 Specialist nodes, green #4ADE80 node borders, connection lines, dark bg, clean tech style",
    },
    {
        "id": "mcp-cheat-sheet",
        "filename": "mcp-cheat-sheet-cover.png",
        "accent": "#22D3EE", "bg": "#010C10",
        "category": "QUICK REFERENCE",
        "title": "MCP\nCheat Sheet",
        "subtitle": "Model Context Protocol — tools, resources & prompts at a glance.",
        "features": ["All Concepts", "Code Examples", "Free Download"],
        "price": "FREE",
        "hero_hint": "reference card mockup: two-column layout showing JSON code blocks with syntax highlighting (cyan strings, gray keys), monospace font, dark panel bg",
    },
]


def gemini_svg(product: dict) -> str:
    prompt = f"""Create a MINIMAL, clean SVG illustration for a dark digital product cover.

Hero type: {product['hero_hint']}
Accent color: {product['accent']}
Container: viewBox="0 0 340 210", transparent background

Rules:
- Maximum 45 SVG elements total — keep it simple
- Dark fills: #0F172A, #1E293B, #0D1117
- Use {product['accent']} for accents, borders, highlights only
- rounded corners rx=8 for boxes
- Subtle text labels in monospace font if needed (small, 10-12px)
- Look like a professional UI mockup, not a logo
- NO stroke-width > 2

Return ONLY the <svg> element, nothing else."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 2500}
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    for pat in [r'(<svg[\s\S]*?</svg>)', r'```(?:svg|xml)?\n([\s\S]*?)```']:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            s = m.group(1)
            if '<svg' in s:
                return s
    return fallback_svg(product)


def fallback_svg(p: dict) -> str:
    a = p["accent"]
    return f'''<svg viewBox="0 0 340 210" xmlns="http://www.w3.org/2000/svg">
  <rect width="340" height="210" rx="12" fill="#0F172A" stroke="{a}" stroke-width="1" opacity="0.6"/>
  <rect x="16" y="16" width="60" height="8" rx="4" fill="{a}" opacity="0.8"/>
  <rect x="16" y="36" width="100" height="6" rx="3" fill="#334155"/>
  <rect x="16" y="52" width="80" height="6" rx="3" fill="#334155"/>
  <rect x="16" y="68" width="120" height="6" rx="3" fill="#334155"/>
  <rect x="16" y="84" width="70" height="6" rx="3" fill="#334155"/>
  <circle cx="280" cy="105" r="45" fill="{a}" opacity="0.07"/>
</svg>'''


def build_html(p: dict, svg: str) -> str:
    a = p["accent"]
    bg = p["bg"]
    lines = p["title"].split("\n")
    title_html = "<br>".join(lines)
    pills = "".join(f'<span class="pill">{f}</span>' for f in p["features"])
    price_cls = "pfree" if p["price"] == "FREE" else "ppaid"

    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700;800&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:800px;overflow:hidden}}
.cover{{
  width:800px;height:800px;background:{bg};
  position:relative;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  padding:44px 60px;font-family:'Inter',sans-serif;overflow:hidden
}}
.grid{{position:absolute;inset:0;
  background-image:linear-gradient({a}09 1px,transparent 1px),linear-gradient(90deg,{a}09 1px,transparent 1px);
  background-size:56px 56px;z-index:0}}
.glow{{position:absolute;width:480px;height:480px;
  background:radial-gradient(circle,{a}1A 0%,transparent 68%);
  top:50%;left:50%;transform:translate(-50%,-50%);z-index:0}}
.c1{{position:absolute;top:0;left:0;width:180px;height:180px;
  border-right:1px solid {a}1E;border-bottom:1px solid {a}1E;
  border-bottom-right-radius:180px;z-index:1}}
.c2{{position:absolute;bottom:0;right:0;width:160px;height:160px;
  border-left:1px solid {a}1E;border-top:1px solid {a}1E;
  border-top-left-radius:160px;z-index:1}}
.bar{{position:absolute;left:0;top:18%;bottom:18%;
  width:3px;background:linear-gradient(to bottom,transparent,{a}CC,transparent);z-index:1}}
.content{{position:relative;z-index:10;display:flex;flex-direction:column;
  align-items:center;text-align:center;width:100%;gap:0}}
.cat{{font-size:9.5px;font-weight:600;letter-spacing:2.5px;color:{a};
  background:{a}14;border:1px solid {a}44;padding:5px 14px;
  border-radius:20px;margin-bottom:22px}}
.title{{font-family:'Space Grotesk',sans-serif;font-size:60px;font-weight:800;
  line-height:1.1;color:#F1F5F9;letter-spacing:-1.5px;margin-bottom:0px}}
.title em{{color:{a};font-style:normal}}
.hero{{width:100%;margin:20px 0;display:flex;justify-content:center;align-items:center}}
.hero svg{{width:340px;height:auto;
  filter:drop-shadow(0 8px 32px {a}35)}}
.sub{{font-size:14px;font-weight:400;color:#94A3B8;line-height:1.5;
  max-width:480px;margin-bottom:20px}}
.pills{{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;margin-bottom:22px}}
.pill{{font-size:11.5px;font-weight:500;color:#CBD5E1;
  background:#1E293B;border:1px solid #334155;padding:5px 14px;border-radius:20px}}
.ppaid{{font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;
  padding:8px 26px;border-radius:30px;color:{bg};background:{a}}}
.pfree{{font-family:'Space Grotesk',sans-serif;font-size:17px;font-weight:700;
  padding:8px 26px;border-radius:30px;color:{a};
  background:{a}1E;border:1.5px solid {a}}}
</style></head>
<body>
<div class="cover">
  <div class="grid"></div>
  <div class="glow"></div>
  <div class="c1"></div>
  <div class="c2"></div>
  <div class="bar"></div>
  <div class="content">
    <span class="cat">{p['category']}</span>
    <h1 class="title">{title_html}</h1>
    <div class="hero">{svg}</div>
    <p class="sub">{p['subtitle']}</p>
    <div class="pills">{pills}</div>
    <span class="{price_cls}">{p['price']}</span>
  </div>
</div>
</body></html>'''


def render(html_path: Path, out: Path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        page = br.new_page(viewport={"width": 800, "height": 800})
        page.goto(f"file://{html_path}", wait_until="networkidle")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(out), clip={"x":0,"y":0,"width":800,"height":800})
        br.close()


def generate(p: dict):
    pid = p["id"]
    print(f"\n[{pid}]")
    print(f"  Gemini SVG ({p['hero_hint'][:50]}...)...")
    try:
        svg = gemini_svg(p)
        print(f"  SVG: {len(svg)} chars")
    except Exception as e:
        print(f"  Gemini error ({e}) — fallback")
        svg = fallback_svg(p)

    html = build_html(p, svg)
    html_file = OUTPUT_DIR / f"{pid}-cover.html"
    html_file.write_text(html, encoding="utf-8")

    out = OUTPUT_DIR / p["filename"]
    print(f"  Rendering -> {p['filename']}...")
    render(html_file, out)
    print(f"  {out.stat().st_size // 1024} KB")


def main():
    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY not in .env")
        sys.exit(1)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ids = set(sys.argv[1:])
    targets = [p for p in PRODUCTS if not ids or p["id"] in ids]
    if not targets:
        print(f"No match. IDs: {[p['id'] for p in PRODUCTS]}")
        sys.exit(1)
    print(f"Generating {len(targets)} cover(s)...")
    for p in targets:
        try:
            generate(p)
        except Exception as e:
            import traceback
            print(f"  FAIL {p['id']}: {e}")
            traceback.print_exc()
    print("\nDone!")

if __name__ == "__main__":
    main()
