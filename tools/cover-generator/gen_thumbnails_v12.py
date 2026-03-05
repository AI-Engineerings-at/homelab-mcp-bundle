#!/usr/bin/env python3
"""
Thumbnail Generator v12 -- Product Image Showcase Design

800x800 thumbnails used as product-image-cards inside Gumroad covers.
Layout:
  [top 42%]   Product screenshot (real or styled mockup)
  [~38% ctr]  Eagle watermark -- Schriftzug visible in transition zone (~60%)
  [42%-100%]  Product title, features, stats, price

Eagle at top:38% (center) -- Schriftzug (logo text) lands at ~60% -- visible
between product image area (0-42%) and the lower content section (65%+).

v12 changes vs prev:
  - Eagle moved from 52% -> 38% (center point)
  - Product image slot added (real screenshot or styled mockup)
  - Separator line between image and content

Usage:
  python3 gen_thumbnails_v12.py                  # all products
  python3 gen_thumbnails_v12.py n8n-starter-bundle localai-playbook
  python3 gen_thumbnails_v12.py --list
  python3 gen_thumbnails_v12.py --dry-run
  python3 gen_thumbnails_v12.py --out /tmp/thumbs-test
"""
import os, sys, base64, argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE         = Path("/home/joe/cli_bridge")
OUTPUT_DIR   = BASE / "products/covers"
EAGLE_PATH   = Path("/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png")

# Product screenshots (real screenshots for visual products, None = styled mockup)
SCREENSHOTS = {
    "localai-playbook":       None,
    "n8n-starter-bundle":     BASE / "n8n-workflows-dark.png",
    "grafana-dashboard-pack": BASE / "grafana-infra-overview.png",
    "dsgvo-art30-bundle":     None,
    "homelab-mcp-bundle":     None,
    "ai-agent-blueprint":     None,
    "komplett-bundle":        None,
}

PRODUCTS = [
    {"id": "localai-playbook",
     "accent": "#10B981", "accent_dark": "#059669",
     "gradient": "linear-gradient(175deg,#020817 0%,#041a10 55%,#020d14 100%)",
     "badge": "Bestseller 2025", "eyebrow": "The Complete Guide",
     "title": "Local <em>AI&nbsp;Stack</em> Playbook",
     "features": ["Docker Swarm", "Ollama GPU", "n8n Automation", "100% Private"],
     "stats": [("180+", "Pages"), ("42", "Diagrams"), ("15+", "Services")],
     "price": "EUR 49", "icon": "🧠"},

    {"id": "n8n-starter-bundle",
     "accent": "#FB923C", "accent_dark": "#EA580C",
     "gradient": "linear-gradient(175deg,#0c0800 0%,#1a1000 55%,#0c0800 100%)",
     "badge": "Most Popular", "eyebrow": "Workflow Automation",
     "title": "<em>n8n</em> Starter Bundle",
     "features": ["30+ Workflows", "AI Nodes", "Email &amp; CRM", "500+ Integrations"],
     "stats": [("30+", "Workflows"), ("500+", "Integrations"), ("10min", "Setup")],
     "price": "EUR 29", "icon": "⚡"},

    {"id": "grafana-dashboard-pack",
     "accent": "#60A5FA", "accent_dark": "#2563EB",
     "gradient": "linear-gradient(175deg,#020817 0%,#0a1220 55%,#020817 100%)",
     "badge": "Pro Quality", "eyebrow": "Infrastructure Monitoring",
     "title": "Grafana <em>Dashboard</em> Pack",
     "features": ["12 Dashboards", "Docker Metrics", "Real-time Alerts", "Import Ready"],
     "stats": [("12", "Dashboards"), ("50+", "Panels"), ("5min", "Import")],
     "price": "EUR 39", "icon": "📊"},

    {"id": "dsgvo-art30-bundle",
     "accent": "#C084FC", "accent_dark": "#9333EA",
     "gradient": "linear-gradient(175deg,#080010 0%,#120020 55%,#080010 100%)",
     "badge": "Legal Compliance", "eyebrow": "DSGVO Art. 30 VVT",
     "title": "DSGVO&nbsp;Art.30 <em>Bundle</em>",
     "features": ["VVT Templates", "Art.30 konform", "DE/AT Recht", "Sofort nutzbar"],
     "stats": [("15+", "Templates"), ("100%", "DSGVO"), ("DE/AT", "Recht")],
     "price": "EUR 79", "icon": "⚖️"},

    {"id": "homelab-mcp-bundle",
     "accent": "#22D3EE", "accent_dark": "#0891B2",
     "gradient": "linear-gradient(175deg,#020b0d 0%,#031520 55%,#020b0d 100%)",
     "badge": "Free · Open Source", "eyebrow": "MCP Server Collection",
     "title": "Homelab <em>MCP</em> Bundle",
     "features": ["8 MCP Servers", "51 Tools", "Homelab Ready", "Claude Compatible"],
     "stats": [("8", "MCP Servers"), ("51", "Tools"), ("0€", "Free")],
     "price": "FREE", "icon": "🔌"},

    {"id": "ai-agent-blueprint",
     "accent": "#4ADE80", "accent_dark": "#16A34A",
     "gradient": "linear-gradient(175deg,#010d02 0%,#021508 55%,#010d02 100%)",
     "badge": "New Release", "eyebrow": "Multi-Agent Architecture",
     "title": "AI Agent Team <em>Blueprint</em>",
     "features": ["Multi-Agent", "Architecture", "n8n + Claude", "Templates"],
     "stats": [("10+", "Agents"), ("7", "Blueprints"), ("1-Click", "Deploy")],
     "price": "EUR 19", "icon": "🤖"},
    {"id": "komplett-bundle",
     "accent": "#F59E0B", "accent_dark": "#D97706",
     "gradient": "linear-gradient(175deg,#0d0800 0%,#1a1000 55%,#0d0800 100%)",
     "badge": "Best Value · Spar 50%+", "eyebrow": "AI Engineering Komplett-Paket",
     "title": "AI Engineering <em>Komplett</em> Bundle",
     "features": ["Playbook + n8n", "Grafana + DSGVO", "MCP + Blueprint", "Alles drin"],
     "stats": [("6", "Produkte"), ("EUR 190+", "Einzelwert"), ("50%+", "Ersparnis")],
     "price": "EUR 149", "icon": "🎯"},
]


def load_b64(path):
    p = Path(path) if not isinstance(path, Path) else path
    if p and p.exists() and p.stat().st_size > 0:
        ext  = p.suffix.lower().lstrip(".")
        mime = "image/png" if ext == "png" else "image/jpeg"
        with open(p, "rb") as f:
            return "data:" + mime + ";base64," + base64.b64encode(f.read()).decode()
    return ""


def build_mockup(p):
    """CSS-only styled mockup for products without a real screenshot."""
    a = p["accent"]
    feature_pills = "".join(
        f'<div style="background:rgba(255,255,255,.05);border:1px solid {a}33;'
        f'border-radius:6px;padding:7px 13px;color:rgba(248,250,252,.72);'
        f'font-size:12px;font-weight:500;display:inline-block;margin:3px">{f}</div>'
        for f in p["features"]
    )
    return (
        f'<div style="width:100%;height:100%;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;gap:14px;padding:28px 24px;'
        f'background:radial-gradient(ellipse at 50% 40%,{a}18 0%,transparent 65%)">'
        f'<div style="font-size:74px;line-height:1;filter:drop-shadow(0 0 24px {a}80)">{p["icon"]}</div>'
        f'<div style="color:{a};font-size:11px;font-weight:700;letter-spacing:.18em;'
        f'text-transform:uppercase">{p["eyebrow"]}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:5px;justify-content:center;max-width:340px">'
        f'{feature_pills}</div></div>'
    )


def build_thumbnail(p):
    eagle    = load_b64(EAGLE_PATH)
    shot_key = SCREENSHOTS.get(p["id"])
    shot_b64 = load_b64(shot_key) if shot_key else ""
    a, d     = p["accent"], p["accent_dark"]

    # Determine background color for gradient overlay (extract first stop from gradient)
    bg_dark = p["gradient"].split(",")[1].strip().split(" ")[0]

    # Product image section (top 42% = 336px of 800px)
    if shot_b64:
        # Real screenshot with gradient blend-out overlay
        product_section = (
            f'<div style="position:relative;width:100%;height:336px;overflow:hidden;flex-shrink:0;z-index:5">'
            f'<img src="{shot_b64}" style="width:100%;height:100%;object-fit:cover;'
            f'object-position:top left;display:block;filter:brightness(.86) saturate(1.18)">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(to bottom,'
            f'transparent 0%,transparent 45%,{bg_dark}ee 100%)"></div>'
            f'<div style="position:absolute;top:15px;left:15px;background:{a}22;border:1px solid {a}60;'
            f'border-radius:100px;padding:5px 14px;color:{a};font-size:10px;font-weight:700;'
            f'letter-spacing:.12em;text-transform:uppercase">{p["badge"]}</div>'
            f'</div>'
        )
    else:
        product_section = (
            f'<div style="position:relative;width:100%;height:336px;overflow:hidden;flex-shrink:0;'
            f'background:{p["gradient"]};z-index:5">'
            f'{build_mockup(p)}'
            f'<div style="position:absolute;top:15px;left:15px;background:{a}22;border:1px solid {a}60;'
            f'border-radius:100px;padding:5px 14px;color:{a};font-size:10px;font-weight:700;'
            f'letter-spacing:.12em;text-transform:uppercase">{p["badge"]}</div>'
            f'</div>'
        )

    # Feature pills
    feats = "".join(
        f'<div style="background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.10);'
        f'border-radius:6px;padding:5px 10px;color:rgba(248,250,252,.75);font-size:11px;'
        f'font-weight:500">{f}</div>'
        for f in p["features"]
    )
    # Stats
    stats = "".join(
        f'<div style="text-align:left">'
        f'<div style="font-size:20px;font-weight:700;color:{a};line-height:1">{n}</div>'
        f'<div style="font-size:9px;color:rgba(255,255,255,.28);text-transform:uppercase;'
        f'letter-spacing:.07em;margin-top:2px">{l}</div></div>'
        for n, l in p["stats"]
    )

    # Eagle watermark: center at top:38% -> Schriftzug visible between product and content
    eagle_html = (
        f'<div style="position:absolute;width:580px;height:580px;'
        f'top:38%;left:50%;transform:translate(-50%,-50%);opacity:0.22;z-index:4;'
        f'pointer-events:none">'
        f'<img src="{eagle}" style="width:100%;height:100%;object-fit:contain" alt=""></div>'
    ) if eagle else ""

    # Brand logo for footer
    brand_logo_html = (
        f'<img src="{eagle}" style="width:20px;height:20px;object-fit:contain;'
        f'opacity:.45;filter:brightness(0) invert(1)" alt="">'
    ) if eagle else ""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:800px;height:800px;overflow:hidden;font-family:'Inter',sans-serif;color:#F8FAFC}}
.wrap{{width:800px;height:800px;background:{p['gradient']};position:relative;overflow:hidden;
  display:flex;flex-direction:column}}
.wrap::before{{content:'';position:absolute;inset:0;
  background-image:linear-gradient({a}07 1px,transparent 1px),
  linear-gradient(90deg,{a}07 1px,transparent 1px);
  background-size:46px 46px;z-index:3}}
.orb1{{position:absolute;width:500px;height:500px;
  background:radial-gradient(circle,{a}14 0%,transparent 65%);
  top:-110px;right:-70px;z-index:2}}
.orb2{{position:absolute;width:360px;height:360px;
  background:radial-gradient(circle,{a}0a 0%,transparent 65%);
  bottom:-80px;left:30px;z-index:2}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(to bottom,transparent,{a},{a},transparent);z-index:6}}
.sep{{height:1px;background:linear-gradient(to right,{a}50,{a}20,transparent);
  position:relative;z-index:6;flex-shrink:0}}
.content{{position:relative;z-index:10;flex:1;display:flex;flex-direction:column;
  padding:16px 28px 12px 30px;min-height:0}}
.eyebrow{{color:{a};font-size:10px;font-weight:700;letter-spacing:.18em;
  text-transform:uppercase;margin-bottom:7px}}
.title{{font-family:'Space Grotesk',sans-serif;font-size:40px;font-weight:800;
  line-height:1.05;letter-spacing:-.02em;color:#F8FAFC;margin-bottom:10px}}
.title em{{color:{a};font-style:normal}}
.feats{{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:auto}}
.div{{height:1px;background:linear-gradient(to right,{a}45,transparent);margin:10px 0}}
.bot{{display:flex;align-items:center;justify-content:space-between}}
.stats{{display:flex;gap:16px}}
.price{{background:linear-gradient(135deg,{a},{d});border-radius:10px;
  padding:9px 18px;font-size:22px;font-weight:800;color:#fff}}
.brand{{display:flex;align-items:center;gap:7px;padding:7px 30px 9px;
  border-top:1px solid rgba(255,255,255,.06);position:relative;z-index:10;flex-shrink:0}}
.brand-name{{font-size:9px;font-weight:700;color:rgba(255,255,255,.28);
  letter-spacing:.12em;text-transform:uppercase}}
.brand-url{{font-size:8px;color:rgba(255,255,255,.16);letter-spacing:.12em;
  text-transform:uppercase;margin-left:auto}}
</style></head><body>
<div class="wrap">
  <div class="orb1"></div><div class="orb2"></div>
  {eagle_html}
  <div class="lline"></div>
  {product_section}
  <div class="sep"></div>
  <div class="content">
    <div class="eyebrow">{p['eyebrow']}</div>
    <div class="title">{p['title']}</div>
    <div class="feats">{feats}</div>
    <div class="div"></div>
    <div class="bot">
      <div class="stats">{stats}</div>
      <div class="price">{p['price']}</div>
    </div>
  </div>
  <div class="brand">
    {brand_logo_html}
    <div class="brand-name">AI Engineering</div>
    <div class="brand-url">ai-engineering.at</div>
  </div>
</div>
</body></html>"""


def render(p, out_dir, dry_run=False):
    html = build_thumbnail(p)
    hp   = f"/tmp/thumb_v12_{p['id']}.html"
    op   = out_dir / f"thumbnail-{p['id']}.png"
    with open(hp, "w", encoding="utf-8") as fh:
        fh.write(html)
    if dry_run:
        print(f"  DRY  {p['id']}  -> {hp}")
        return op
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=[
            "--no-sandbox", "--disable-setuid-sandbox",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
        ])
        pg = br.new_page(viewport={"width": 800, "height": 800})
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(3000)
        pg.screenshot(path=str(op), clip={"x": 0, "y": 0, "width": 800, "height": 800})
        br.close()
    kb   = os.path.getsize(op) // 1024
    shot = "screenshot" if (SCREENSHOTS.get(p["id"]) and Path(str(SCREENSHOTS[p["id"]])).exists()) else "mockup"
    print(f"  ok  {p['id']:<36}  {kb:>4}KB  [{shot}]  ->  {op.name}")
    return op


def main():
    parser = argparse.ArgumentParser(
        description="Thumbnail Generator v12 -- Eagle@38%, Produktbild oben, 800x800"
    )
    parser.add_argument("products", nargs="*", help="Product IDs (default: all)")
    parser.add_argument("--out", default=str(OUTPUT_DIR))
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.list:
        print(f"\n{'ID':<38} {'Price':<8} {'Screenshot':<44} Accent")
        print("-" * 95)
        for p in PRODUCTS:
            s    = SCREENSHOTS.get(p["id"])
            sstr = f"OK  {Path(str(s)).name}" if (s and Path(str(s)).exists()) else "-- mockup"
            print(f"  {p['id']:<36} {p['price']:<8} {sstr:<44} {p['accent']}")
        return

    ids      = args.products or None
    products = [p for p in PRODUCTS if ids is None or p["id"] in ids]
    if not products:
        print(f"No products matched: {ids}"); sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nThumbnail Generator v12  --  {len(products)} Produkt(e)  [Eagle@38%, 800x800]\n")
    ok = 0
    for p in products:
        try:
            render(p, out_dir, dry_run=args.dry_run)
            ok += 1
        except Exception as e:
            print(f"  ERROR  {p['id']}: {e}")
    print(f"\n{ok}/{len(products)} Thumbnails fertig  ->  {out_dir}")


if __name__ == "__main__":
    main()
