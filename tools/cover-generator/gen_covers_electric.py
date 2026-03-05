#!/usr/bin/env python3
"""
Cover Generator — Electric Design

Electric Design Features (vs v4):
  - Font: Montserrat 800/900 (BrandKit) statt Space Grotesk
  - Eagle: 46% Hero + SVG Glow-Filter + Orbital Rings
  - Title: Text-Shadow Glow in Accent-Farbe
  - Separator: Gradient-Linie + glühende Punkte
  - Badge: Gradient-Badge + Box-Shadow Glow
  - Background: 3 Orbs + Circuit Grid + Orbital Rings
  - Price: Gradient + Box-Shadow Glow
  - Stats: Glowing Zahlen mit Text-Shadow

Usage:
  python3 gen_covers_electric.py                        # all products, cover format
  python3 gen_covers_electric.py localai-playbook        # single product
  python3 gen_covers_electric.py --format fb-post        # single format
  python3 gen_covers_electric.py --format cover,ig-post  # multiple formats
  python3 gen_covers_electric.py --format all            # all formats
  python3 gen_covers_electric.py --list                  # list products & formats
"""
import os, sys, base64, argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path("/home/joe/cli_bridge/products/cover-templates")
EAGLE_PATH = Path("/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png")
BRAND_BLUE = "#4262FF"


def load_eagle_b64():
    if EAGLE_PATH.exists():
        with open(EAGLE_PATH, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    print("  WARNING: Eagle logo not found")
    return ""

EAGLE_B64 = load_eagle_b64()

PRODUCTS = [
    {"id":"localai-playbook","accent":"#10B981","accent_dark":"#059669",
     "gradient":"linear-gradient(135deg,#020817 0%,#0a1628 40%,#041a10 100%)",
     "badge":"Bestseller 2025","eyebrow":"The Complete Guide",
     "title":"Local <em>AI Stack</em><br>Playbook",
     "subtitle":"Run your own AI infrastructure with Ollama, n8n &amp; Docker — fully private, zero cloud costs.",
     "features":["Docker Swarm","Ollama GPU","n8n Automation","100% Private"],
     "stats":[("180+","Pages"),("42","Diagrams"),("15+","Services")],
     "price":"EUR 49","icon":"🧠"},
    {"id":"n8n-starter-bundle","accent":"#FB923C","accent_dark":"#EA580C",
     "gradient":"linear-gradient(135deg,#0c0800 0%,#1a0f00 40%,#0c0800 100%)",
     "badge":"Most Popular","eyebrow":"Workflow Automation",
     "title":"<em>n8n</em> Starter<br>Bundle",
     "subtitle":"30+ ready-to-use workflows for AI automation, lead gen &amp; business ops. Plug-and-play.",
     "features":["30+ Workflows","AI Nodes","Email &amp; CRM","500+ Integrations"],
     "stats":[("30+","Workflows"),("500+","Integrations"),("10min","Setup")],
     "price":"EUR 29","icon":"⚡"},
    {"id":"grafana-dashboard-pack","accent":"#60A5FA","accent_dark":"#2563EB",
     "gradient":"linear-gradient(135deg,#020817 0%,#0a1220 40%,#020817 100%)",
     "badge":"Pro Quality","eyebrow":"Infrastructure Monitoring",
     "title":"Grafana<br><em>Dashboard</em> Pack",
     "subtitle":"Beautiful, production-ready dashboards for Docker, Node Exporter &amp; self-hosted stacks.",
     "features":["12 Dashboards","Docker Metrics","Real-time Alerts","Import Ready"],
     "stats":[("12","Dashboards"),("50+","Panels"),("5min","Import")],
     "price":"EUR 39","icon":"📊"},
    {"id":"dsgvo-art30-bundle","accent":"#C084FC","accent_dark":"#9333EA",
     "gradient":"linear-gradient(135deg,#080010 0%,#120020 40%,#080010 100%)",
     "badge":"Legal Compliance","eyebrow":"DSGVO Art. 30 VVT",
     "title":"DSGVO Art.30<br><em>Bundle</em>",
     "subtitle":"Vollst&auml;ndige Vorlagen f&uuml;r das Verzeichnis von Verarbeitungst&auml;tigkeiten — DSGVO-konform.",
     "features":["VVT Templates","Datenschutz","Art. 30 konform","Sofort nutzbar"],
     "stats":[("15+","Templates"),("100%","DSGVO"),("DE/AT","Recht")],
     "price":"EUR 79","icon":"⚖️"},
    {"id":"homelab-mcp-bundle","accent":"#22D3EE","accent_dark":"#0891B2",
     "gradient":"linear-gradient(135deg,#020b0d 0%,#031520 40%,#020b0d 100%)",
     "badge":"Free · Open Source","eyebrow":"MCP Server Collection",
     "title":"Homelab<br><em>MCP</em> Bundle",
     "subtitle":"8 production-ready MCP servers for your homelab: Grafana, n8n, Portainer, Proxmox &amp; more.",
     "features":["8 MCP Servers","51 Tools","Homelab Ready","Claude Compatible"],
     "stats":[("8","MCP Servers"),("51","Tools"),("0€","Free")],
     "price":"FREE","icon":"🔌"},
    {"id":"ai-agent-blueprint","accent":"#4ADE80","accent_dark":"#16A34A",
     "gradient":"linear-gradient(135deg,#010d02 0%,#021508 40%,#010d02 100%)",
     "badge":"New Release","eyebrow":"Multi-Agent Architecture",
     "title":"AI Agent Team<br><em>Blueprint</em>",
     "subtitle":"Design and deploy your own AI agent team — Manager, Specialists &amp; Automation in one system.",
     "features":["Multi-Agent","Architecture","n8n + Claude","Templates"],
     "stats":[("10+","Agents"),("7","Blueprints"),("1-Click","Deploy")],
     "price":"EUR 19","icon":"🤖"},
    {"id":"mcp-cheat-sheet","accent":"#22D3EE","accent_dark":"#0891B2",
     "gradient":"linear-gradient(135deg,#020b0d 0%,#031520 40%,#020b0d 100%)",
     "badge":"Lead Magnet · Free","eyebrow":"Quick Reference Card",
     "title":"MCP<br><em>Cheat Sheet</em>",
     "subtitle":"Everything you need to know about Model Context Protocol — tools, resources &amp; prompts at a glance.",
     "features":["All MCP Concepts","Tool Examples","Quick Setup","Claude Ready"],
     "stats":[("1 Page","Reference"),("MCP","Protocol"),("Free","Download")],
     "price":"FREE","icon":"📋"},
]

FORMATS = {
    "cover":        {"w":800,  "h":800,  "layout":"square"},
    "ig-post":      {"w":1080, "h":1080, "layout":"square"},
    "fb-post":      {"w":1200, "h":630,  "layout":"landscape"},
    "twitter-post": {"w":1200, "h":675,  "layout":"landscape"},
    "yt-thumb":     {"w":1280, "h":720,  "layout":"landscape"},
    "ig-story":     {"w":1080, "h":1920, "layout":"story"},
    "fb-banner":    {"w":820,  "h":312,  "layout":"banner"},
    "li-banner":    {"w":1584, "h":396,  "layout":"banner"},
}
ALL_FORMATS = list(FORMATS.keys())


def css_vars(p):
    a, d = p["accent"], p["accent_dark"]
    return (f"--accent:{a};--accent-dark:{d};--brand-blue:{BRAND_BLUE};"
            f"--a0a:{a}0a;--a11:{a}11;--a15:{a}15;--a18:{a}18;--a20:{a}20;"
            f"--a22:{a}22;--a30:{a}30;--a35:{a}35;--a40:{a}40;--a50:{a}50;")


def eagle_hero(size_px, accent, top_pct=50, right_val=None):
    """Eagle at 46% opacity with SVG glow filter + orbital rings."""
    if not EAGLE_B64:
        return ""
    if right_val is not None:
        pos = f"top:50%;right:{right_val};transform:translateY(-50%)"
    else:
        pos = f"top:{top_pct}%;left:50%;transform:translate(-50%,-50%)"
    fid = f"eg{size_px}"
    r1, r2 = int(size_px * 0.52), int(size_px * 0.68)
    return (
        f'<div style="position:absolute;{pos};width:{size_px}px;height:{size_px}px;z-index:4">'
        # SVG: glow filter + orbital rings + eagle image
        f'<svg width="{size_px}" height="{size_px}" style="position:absolute;inset:0;overflow:visible">'
        f'<defs>'
        f'<filter id="{fid}" x="-40%" y="-40%" width="180%" height="180%">'
        f'<feGaussianBlur in="SourceGraphic" stdDeviation="20" result="b"/>'
        f'<feColorMatrix in="b" type="matrix" '
        f'values="0 0 0 0 0.26 0 0 0 0 0.38 0 0 0 0 1 0 0 0 0.55 0" result="g"/>'
        f'<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter>'
        f'</defs>'
        # Orbital rings
        f'<ellipse cx="{size_px//2}" cy="{size_px//2}" rx="{r1}" ry="{int(r1*0.3)}" '
        f'fill="none" stroke="{accent}" stroke-width="1" stroke-opacity="0.35" stroke-dasharray="6 4"/>'
        f'<ellipse cx="{size_px//2}" cy="{size_px//2}" rx="{r2}" ry="{int(r2*0.26)}" '
        f'fill="none" stroke="{accent}" stroke-width="1" stroke-opacity="0.18" stroke-dasharray="3 8"/>'
        # Dots on orbital rings
        f'<circle cx="{size_px//2 + r1}" cy="{size_px//2}" r="3" fill="{accent}" opacity="0.75"/>'
        f'<circle cx="{size_px//2 - r2}" cy="{size_px//2}" r="2" fill="{accent}" opacity="0.45"/>'
        # Eagle image with glow
        f'<image href="{EAGLE_B64}" width="{size_px}" height="{size_px}" '
        f'filter="url(#{fid})" opacity="0.46"/>'
        f'</svg>'
        f'</div>'
    )


def glowing_separator(width_pct, accent, s=1.0):
    ds = max(4, int(6 * s))
    return (
        f'<div style="position:relative;width:{width_pct}%;height:{ds}px;margin-bottom:{int(20*s)}px">'
        f'<div style="position:absolute;top:50%;left:0;right:0;height:1px;transform:translateY(-50%);'
        f'background:linear-gradient(to right,{accent},{accent}77,transparent)"></div>'
        f'<div style="position:absolute;top:50%;left:0;transform:translateY(-50%);'
        f'width:{ds}px;height:{ds}px;border-radius:50%;background:{accent};'
        f'box-shadow:0 0 {ds*2}px {ds}px {accent}55"></div>'
        f'<div style="position:absolute;top:50%;left:{int(44*s)}px;transform:translateY(-50%);'
        f'width:{int(ds*0.6)}px;height:{int(ds*0.6)}px;border-radius:50%;background:{accent};opacity:0.45;'
        f'box-shadow:0 0 {ds}px {int(ds*0.5)}px {accent}33"></div>'
        f'</div>'
    )


# ---- SQUARE ----
def build_square(p, fmt):
    w, h = fmt["w"], fmt["h"]
    s = w / 800
    a = p["accent"]
    feats = "".join(f'<div class="feat">{f}</div>' for f in p["features"])
    stats = "".join(f'<div><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"])
    eagle = eagle_hero(int(480*s), a, top_pct=30)
    sep = glowing_separator(85, a, s)
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}:root{{{css_vars(p)}}}
body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:{w}px;height:{h}px;background:{p['gradient']};position:relative;overflow:hidden}}
.orb1{{position:absolute;width:{int(620*s)}px;height:{int(620*s)}px;background:radial-gradient(circle,var(--a22) 0%,transparent 65%);top:{int(-160*s)}px;left:{int(-160*s)}px;z-index:2}}
.orb2{{position:absolute;width:{int(480*s)}px;height:{int(480*s)}px;background:radial-gradient(circle,var(--a11) 0%,transparent 65%);bottom:{int(-120*s)}px;right:{int(-120*s)}px;z-index:2}}
.orb3{{position:absolute;width:{int(320*s)}px;height:{int(320*s)}px;background:radial-gradient(circle,{BRAND_BLUE}18 0%,transparent 65%);bottom:{int(100*s)}px;left:{int(30*s)}px;z-index:2}}
.gbg{{position:absolute;inset:0;background-image:linear-gradient(var(--a0a) 1px,transparent 1px),linear-gradient(90deg,var(--a0a) 1px,transparent 1px);background-size:{int(55*s)}px {int(55*s)}px;z-index:3}}
.corner{{position:absolute;top:0;right:0;width:{int(220*s)}px;height:{int(220*s)}px;border-left:1px solid var(--a30);border-bottom:1px solid var(--a30);border-bottom-left-radius:{int(220*s)}px;z-index:5}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:5;box-shadow:0 0 12px 2px var(--a50)}}
.content{{position:absolute;inset:0;z-index:10;display:flex;flex-direction:column;padding:{int(44*s)}px {int(52*s)}px {int(44*s)}px {int(56*s)}px}}
.toprow{{display:flex;align-items:center;justify-content:space-between;margin-bottom:{int(36*s)}px}}
.badge{{display:inline-flex;align-items:center;gap:7px;background:linear-gradient(135deg,var(--a30),{BRAND_BLUE}2a);border:1px solid var(--a50);border-radius:100px;padding:6px 16px;color:var(--accent);font-size:{round(11.5*s,1)}px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;box-shadow:0 0 14px 2px var(--a20),0 0 24px 4px {BRAND_BLUE}14}}
.bdot{{width:5px;height:5px;background:var(--accent);border-radius:50%;box-shadow:0 0 6px 2px var(--a50)}}
.ibox{{width:{int(44*s)}px;height:{int(44*s)}px;background:var(--a18);border:1px solid var(--a35);border-radius:{int(10*s)}px;display:flex;align-items:center;justify-content:center;font-size:{int(20*s)}px;box-shadow:0 0 12px 2px var(--a15)}}
.ey{{color:var(--accent);font-size:{round(12.5*s,1)}px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:{int(14*s)}px}}
.title{{font-family:'Montserrat',sans-serif;font-size:{int(64*s)}px;font-weight:900;line-height:1.04;color:#F8FAFC;letter-spacing:-.02em;margin-bottom:{int(22*s)}px;text-shadow:0 0 40px var(--a35),0 0 80px var(--a18)}}
.title em{{color:var(--accent);font-style:normal;text-shadow:0 0 30px var(--a50),0 0 60px var(--a30)}}
.sub{{font-size:{round(16*s,1)}px;color:rgba(248,250,252,.52);line-height:1.65;max-width:{int(470*s)}px;margin-bottom:{int(28*s)}px}}
.feats{{display:flex;gap:{int(9*s)}px;flex-wrap:wrap}}
.feat{{background:rgba(255,255,255,.055);border:1px solid rgba(255,255,255,.11);border-radius:6px;padding:{int(7*s)}px {int(14*s)}px;color:rgba(248,250,252,.8);font-size:{int(13*s)}px;font-weight:500}}
.sp{{flex:1}}
.bot{{display:flex;align-items:center;justify-content:space-between}}
.stats{{display:flex;gap:{int(36*s)}px}}
.snum{{font-size:{int(24*s)}px;font-weight:800;color:var(--accent);line-height:1;text-shadow:0 0 20px var(--a50),0 0 40px var(--a30)}}
.slbl{{font-size:{round(10.5*s,1)}px;color:rgba(255,255,255,.35);margin-top:4px;text-transform:uppercase;letter-spacing:.06em}}
.price{{background:linear-gradient(135deg,var(--accent),var(--accent-dark));border-radius:{int(12*s)}px;padding:{int(13*s)}px {int(30*s)}px;font-size:{int(28*s)}px;font-weight:800;color:#fff;box-shadow:0 0 24px 4px var(--a35),0 8px 32px var(--a20)}}
.brand{{font-size:{int(11*s)}px;color:rgba(255,255,255,.2);letter-spacing:.1em;text-transform:uppercase;margin-top:3px;text-align:right}}
</style></head><body><div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
<div class="gbg"></div>{eagle}
<div class="corner"></div><div class="lline"></div>
<div class="content">
  <div class="toprow"><div class="badge"><span class="bdot"></span>{p['badge']}</div><div class="ibox">{p['icon']}</div></div>
  <div class="ey">{p['eyebrow']}</div>
  <div class="title">{p['title']}</div>
  <div class="sub">{p['subtitle']}</div>
  <div class="feats">{feats}</div>
  <div class="sp"></div>
  {sep}
  <div class="bot">
    <div class="stats">{stats}</div>
    <div><div class="price">{p['price']}</div><div class="brand">ai-engineering.at</div></div>
  </div>
</div></div></body></html>"""


# ---- LANDSCAPE ----
def build_landscape(p, fmt):
    w, h = fmt["w"], fmt["h"]
    sw, sh = w/1200, h/630
    a = p["accent"]
    feats = "".join(f'<div class="feat">{f}</div>' for f in p["features"])
    stats = "".join(f'<div class="stat"><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"])
    eagle = eagle_hero(int(420*sw), a, right_val=f"{int(40*sw)}px")
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}:root{{{css_vars(p)}}}
body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:{w}px;height:{h}px;background:{p['gradient']};position:relative;overflow:hidden;display:flex}}
.orb1{{position:absolute;width:{int(500*sw)}px;height:{int(500*sw)}px;background:radial-gradient(circle,var(--a18) 0%,transparent 65%);top:{int(-150*sh)}px;left:{int(-80*sw)}px;z-index:1}}
.orb2{{position:absolute;width:{int(360*sw)}px;height:{int(360*sw)}px;background:radial-gradient(circle,var(--a11) 0%,transparent 65%);bottom:{int(-100*sh)}px;right:{int(-80*sw)}px;z-index:1}}
.orb3{{position:absolute;width:{int(280*sw)}px;height:{int(280*sw)}px;background:radial-gradient(circle,{BRAND_BLUE}15 0%,transparent 65%);top:50%;left:52%;transform:translateY(-50%);z-index:1}}
.gbg{{position:absolute;inset:0;background-image:linear-gradient(var(--a0a) 1px,transparent 1px),linear-gradient(90deg,var(--a0a) 1px,transparent 1px);background-size:{int(50*sw)}px {int(50*sh)}px;z-index:2}}
.vdiv{{position:absolute;top:8%;bottom:8%;left:60%;width:1px;background:linear-gradient(to bottom,transparent,var(--a50),transparent);z-index:4;box-shadow:0 0 8px 1px var(--a30)}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:5;box-shadow:0 0 12px 2px var(--a50)}}
.left{{position:relative;z-index:10;width:60%;padding:{int(44*sh)}px {int(36*sw)}px {int(44*sh)}px {int(52*sw)}px;display:flex;flex-direction:column;justify-content:center}}
.badge{{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,var(--a30),{BRAND_BLUE}28);border:1px solid var(--a50);border-radius:100px;padding:5px 14px;color:var(--accent);font-size:{round(10.5*sw,1)}px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:{int(16*sh)}px;width:fit-content;box-shadow:0 0 12px 2px var(--a20)}}
.bdot{{width:4px;height:4px;background:var(--accent);border-radius:50%;box-shadow:0 0 5px 2px var(--a50)}}
.ey{{color:var(--accent);font-size:{round(11*sw,1)}px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:{int(10*sh)}px}}
.title{{font-family:'Montserrat',sans-serif;font-size:{int(50*sw)}px;font-weight:900;line-height:1.08;color:#F8FAFC;letter-spacing:-.02em;margin-bottom:{int(14*sh)}px;text-shadow:0 0 40px var(--a30),0 0 80px var(--a15)}}
.title em{{color:var(--accent);font-style:normal;text-shadow:0 0 30px var(--a50)}}
.sub{{font-size:{round(13*sw,1)}px;color:rgba(248,250,252,.5);line-height:1.6;max-width:{int(460*sw)}px;margin-bottom:{int(16*sh)}px}}
.feats{{display:flex;gap:{int(7*sw)}px;flex-wrap:wrap}}
.feat{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:5px;padding:{int(5*sh)}px {int(12*sw)}px;color:rgba(248,250,252,.75);font-size:{int(11*sw)}px;font-weight:500}}
.right{{position:relative;z-index:10;width:40%;padding:{int(44*sh)}px {int(44*sw)}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{int(16*sh)}px}}
.stat{{background:rgba(255,255,255,.05);border:1px solid var(--a20);border-radius:{int(10*sw)}px;padding:{int(12*sh)}px {int(18*sw)}px;text-align:center;width:100%}}
.snum{{font-size:{int(26*sw)}px;font-weight:800;color:var(--accent);line-height:1;text-shadow:0 0 20px var(--a50),0 0 40px var(--a30)}}
.slbl{{font-size:{round(9*sw,1)}px;color:rgba(255,255,255,.3);margin-top:3px;text-transform:uppercase;letter-spacing:.06em}}
.price{{background:linear-gradient(135deg,var(--accent),var(--accent-dark));border-radius:{int(12*sw)}px;padding:{int(14*sh)}px {int(28*sw)}px;font-size:{int(30*sw)}px;font-weight:800;color:#fff;text-align:center;width:100%;box-shadow:0 0 24px 4px var(--a35),0 8px 28px var(--a20)}}
.brand{{font-size:{int(9*sw)}px;color:rgba(255,255,255,.2);letter-spacing:.1em;text-transform:uppercase}}
</style></head><body><div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
<div class="gbg"></div>{eagle}
<div class="vdiv"></div><div class="lline"></div>
<div class="left">
  <div class="badge"><span class="bdot"></span>{p['badge']}</div>
  <div class="ey">{p['eyebrow']}</div>
  <div class="title">{p['title']}</div>
  <div class="sub">{p['subtitle']}</div>
  <div class="feats">{feats}</div>
</div>
<div class="right">{stats}<div class="price">{p['price']}</div><div class="brand">ai-engineering.at</div></div>
</div></body></html>"""


# ---- STORY ----
def build_story(p, fmt):
    w, h = fmt["w"], fmt["h"]
    a = p["accent"]
    feats = "".join(f'<div class="feat">{f}</div>' for f in p["features"])
    stats = "".join(f'<div class="stat"><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"])
    eagle = eagle_hero(680, a, top_pct=50)
    sep = glowing_separator(80, a, 1.0)
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}:root{{{css_vars(p)}}}
body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:{w}px;height:{h}px;background:{p['gradient']};position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:90px 72px}}
.orb1{{position:absolute;width:920px;height:920px;background:radial-gradient(circle,var(--a22) 0%,transparent 65%);top:-320px;left:50%;transform:translateX(-50%);z-index:1}}
.orb2{{position:absolute;width:720px;height:720px;background:radial-gradient(circle,var(--a15) 0%,transparent 65%);bottom:-220px;left:50%;transform:translateX(-50%);z-index:1}}
.orb3{{position:absolute;width:500px;height:500px;background:radial-gradient(circle,{BRAND_BLUE}18 0%,transparent 65%);top:50%;left:50%;transform:translate(-50%,-50%);z-index:1}}
.gbg{{position:absolute;inset:0;background-image:linear-gradient(var(--a0a) 1px,transparent 1px),linear-gradient(90deg,var(--a0a) 1px,transparent 1px);background-size:60px 60px;z-index:2}}
.lline-l{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:5;box-shadow:0 0 12px 2px var(--a50)}}
.lline-r{{position:absolute;right:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:5;box-shadow:0 0 12px 2px var(--a50)}}
.top{{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;text-align:center}}
.brand-top{{font-size:14px;color:rgba(255,255,255,.25);letter-spacing:.22em;text-transform:uppercase;margin-bottom:32px}}
.badge{{display:inline-flex;align-items:center;gap:8px;background:linear-gradient(135deg,var(--a30),{BRAND_BLUE}28);border:1px solid var(--a50);border-radius:100px;padding:9px 24px;color:var(--accent);font-size:14px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;box-shadow:0 0 16px 3px var(--a20)}}
.bdot{{width:6px;height:6px;background:var(--accent);border-radius:50%;box-shadow:0 0 8px 3px var(--a50)}}
.mid{{position:relative;z-index:10;text-align:center}}
.ey{{color:var(--accent);font-size:15px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;margin-bottom:26px}}
.title{{font-family:'Montserrat',sans-serif;font-size:86px;font-weight:900;line-height:1.05;color:#F8FAFC;letter-spacing:-.02em;margin-bottom:28px;text-shadow:0 0 50px var(--a35),0 0 100px var(--a18)}}
.title em{{color:var(--accent);font-style:normal;text-shadow:0 0 40px var(--a50),0 0 80px var(--a30)}}
.sub{{font-size:20px;color:rgba(248,250,252,.48);line-height:1.6;max-width:840px;margin:0 auto 36px}}
.feats{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}}
.feat{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:11px 22px;color:rgba(248,250,252,.8);font-size:16px;font-weight:500}}
.bot{{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;gap:24px;width:100%}}
.stats{{display:flex;width:100%;background:rgba(255,255,255,.04);border:1px solid var(--a20);border-radius:16px;overflow:hidden}}
.stat{{flex:1;padding:24px 16px;text-align:center;border-right:1px solid var(--a15)}}
.stat:last-child{{border-right:none}}
.snum{{font-size:30px;font-weight:800;color:var(--accent);line-height:1;text-shadow:0 0 20px var(--a50),0 0 40px var(--a30)}}
.slbl{{font-size:11px;color:rgba(255,255,255,.28);margin-top:5px;text-transform:uppercase;letter-spacing:.07em}}
.price{{background:linear-gradient(135deg,var(--accent),var(--accent-dark));border-radius:16px;padding:20px 70px;font-size:42px;font-weight:800;color:#fff;box-shadow:0 0 30px 6px var(--a35),0 10px 40px var(--a20)}}
.brand-bot{{font-size:13px;color:rgba(255,255,255,.2);letter-spacing:.16em;text-transform:uppercase}}
</style></head><body><div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
<div class="gbg"></div>{eagle}
<div class="lline-l"></div><div class="lline-r"></div>
<div class="top"><div class="brand-top">ai-engineering.at</div><div class="badge"><span class="bdot"></span>{p['badge']}</div></div>
<div class="mid"><div class="ey">{p['eyebrow']}</div><div class="title">{p['title']}</div><div class="sub">{p['subtitle']}</div><div class="feats">{feats}</div></div>
<div class="bot">{sep}<div class="stats">{stats}</div><div class="price">{p['price']}</div><div class="brand-bot">ai-engineering.at</div></div>
</div></body></html>"""


# ---- BANNER ----
def build_banner(p, fmt):
    w, h = fmt["w"], fmt["h"]
    sw, sh = w/1584, h/396
    a = p["accent"]
    stats = "".join(f'<div class="stat"><div class="snum">{n}</div><div class="slbl">{l}</div></div>' for n,l in p["stats"][:2])
    eagle = eagle_hero(int(300*sw), a, right_val=f"{int(270*sw)}px")
    sub = p["subtitle"][:107] + "..." if len(p["subtitle"]) > 110 else p["subtitle"]
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}:root{{{css_vars(p)}}}
body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:{w}px;height:{h}px;background:{p['gradient']};position:relative;overflow:hidden;display:flex;align-items:stretch}}
.orb1{{position:absolute;width:{int(380*sw)}px;height:{int(380*sw)}px;background:radial-gradient(circle,var(--a18) 0%,transparent 65%);top:50%;left:{int(280*sw)}px;transform:translateY(-50%);z-index:1}}
.orb2{{position:absolute;width:{int(260*sw)}px;height:{int(260*sw)}px;background:radial-gradient(circle,{BRAND_BLUE}15 0%,transparent 65%);top:50%;right:{int(320*sw)}px;transform:translateY(-50%);z-index:1}}
.gbg{{position:absolute;inset:0;background-image:linear-gradient(var(--a0a) 1px,transparent 1px),linear-gradient(90deg,var(--a0a) 1px,transparent 1px);background-size:{int(44*sw)}px {int(44*sw)}px;z-index:2}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,var(--accent),transparent);z-index:5;box-shadow:0 0 10px 2px var(--a50)}}
.col-brand{{position:relative;z-index:10;width:{int(200*sw)}px;min-width:{int(160*sw)}px;padding:{int(32*sh)}px {int(22*sw)}px {int(32*sh)}px {int(34*sw)}px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid var(--a20)}}
.icon{{font-size:{int(34*sw)}px;margin-bottom:{int(8*sh)}px}}
.brand-name{{font-family:'Montserrat',sans-serif;font-size:{int(15*sw)}px;font-weight:800;color:var(--accent);text-shadow:0 0 12px var(--a40)}}
.brand-url{{font-size:{int(8.5*sw)}px;color:rgba(255,255,255,.28);letter-spacing:.12em;text-transform:uppercase;margin-top:3px}}
.col-content{{position:relative;z-index:10;flex:1;padding:{int(32*sh)}px {int(28*sw)}px;display:flex;flex-direction:column;justify-content:center}}
.badge{{display:inline-flex;align-items:center;gap:5px;background:linear-gradient(135deg,var(--a20),{BRAND_BLUE}20);border:1px solid var(--a50);border-radius:100px;padding:3px 10px;color:var(--accent);font-size:{round(8*sw,1)}px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:{int(7*sh)}px;width:fit-content;box-shadow:0 0 8px 1px var(--a20)}}
.bdot{{width:3px;height:3px;background:var(--accent);border-radius:50%}}
.title{{font-family:'Montserrat',sans-serif;font-size:{int(32*sw)}px;font-weight:900;line-height:1.1;color:#F8FAFC;letter-spacing:-.01em;margin-bottom:{int(5*sh)}px;text-shadow:0 0 20px var(--a25)}}
.title em{{color:var(--accent);font-style:normal;text-shadow:0 0 15px var(--a50)}}
.sub{{font-size:{int(11*sw)}px;color:rgba(248,250,252,.42);line-height:1.5}}
.col-right{{position:relative;z-index:10;width:{int(260*sw)}px;min-width:{int(210*sw)}px;padding:{int(32*sh)}px {int(30*sw)}px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:{int(10*sh)}px;border-left:1px solid var(--a20)}}
.stats{{display:flex;gap:{int(14*sw)}px}}
.stat{{text-align:center}}
.snum{{font-size:{int(17*sw)}px;font-weight:800;color:var(--accent);line-height:1;text-shadow:0 0 12px var(--a50)}}
.slbl{{font-size:{round(7*sw,1)}px;color:rgba(255,255,255,.28);margin-top:2px;text-transform:uppercase;letter-spacing:.06em}}
.price{{background:linear-gradient(135deg,var(--accent),var(--accent-dark));border-radius:{int(8*sw)}px;padding:{int(8*sh)}px {int(20*sw)}px;font-size:{int(20*sw)}px;font-weight:800;color:#fff;white-space:nowrap;box-shadow:0 0 16px 3px var(--a35)}}
</style></head><body><div class="wrap">
<div class="orb1"></div><div class="orb2"></div><div class="gbg"></div>
{eagle}<div class="lline"></div>
<div class="col-brand"><div class="icon">{p['icon']}</div><div class="brand-name">AI Engineering</div><div class="brand-url">ai-engineering.at</div></div>
<div class="col-content"><div class="badge"><span class="bdot"></span>{p['badge']}</div><div class="title">{p['title']}</div><div class="sub">{sub}</div></div>
<div class="col-right"><div class="stats">{stats}</div><div class="price">{p['price']}</div></div>
</div></body></html>"""


BUILDERS = {"square": build_square, "landscape": build_landscape, "story": build_story, "banner": build_banner}


def render(p, fmt_name, fmt, out_dir):
    html = BUILDERS[fmt["layout"]](p, fmt)
    w, h = fmt["w"], fmt["h"]
    hp = f"/tmp/cel-{p['id']}-{fmt_name}.html"
    op = out_dir / f"{p['id']}-{fmt_name}-electric.png"
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--no-sandbox","--disable-setuid-sandbox","--disable-web-security"])
        pg = br.new_page(viewport={"width":w,"height":h})
        pg.goto(f"file://{hp}")
        pg.wait_for_timeout(3000)
        pg.screenshot(path=str(op), clip={"x":0,"y":0,"width":w,"height":h})
        br.close()
    print(f"  ✓ {p['id']}  [{fmt_name} {w}x{h}]  {os.path.getsize(op)//1024}KB")
    return op


def main():
    parser = argparse.ArgumentParser(description="Cover Generator — Electric Design",
                                     epilog=f"Formats: {', '.join(ALL_FORMATS)}")
    parser.add_argument("products", nargs="*", help="Product IDs (default: all)")
    parser.add_argument("--format","-f", default="cover", help="Format(s) or 'all'")
    parser.add_argument("--out", default=str(OUTPUT_DIR))
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        print("\nProducts:")
        for p in PRODUCTS: print(f"  {p['id']:<32} {p['price']:<10} {p['accent']}")
        print("\nFormats:")
        for n,f in FORMATS.items(): print(f"  {n:<16} {f['w']}x{f['h']:<6}  [{f['layout']}]")
        return

    fmt_names = ALL_FORMATS if args.format.strip().lower()=="all" else [f.strip() for f in args.format.split(",")]
    bad = [f for f in fmt_names if f not in FORMATS]
    if bad:
        print(f"Unknown: {bad}\nAvailable: {ALL_FORMATS}"); sys.exit(1)

    ids = args.products or None
    products = [p for p in PRODUCTS if ids is None or p["id"] in ids]
    if not products:
        print(f"No products matched: {ids}"); sys.exit(1)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    total = len(products) * len(fmt_names)
    print(f"\nElectric Design — {len(products)} Produkt(e) x {len(fmt_names)} Format(e) = {total} Assets\n")

    for fmt_name in fmt_names:
        fmt = FORMATS[fmt_name]
        print(f"[{fmt_name}  {fmt['w']}x{fmt['h']}]")
        for p in products:
            try: render(p, fmt_name, fmt, out_dir)
            except Exception as e: print(f"  ERROR {p['id']}: {e}")
        print()
    print(f"Fertig! {total} Assets -> {out_dir}")


if __name__ == "__main__":
    main()
