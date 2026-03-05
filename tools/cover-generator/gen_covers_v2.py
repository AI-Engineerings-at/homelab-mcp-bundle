#!/usr/bin/env python3
"""
Cover Generator v2 — ai-engineering.at
Generates professional 800x800 product covers with product-specific SVG visuals.
Usage: python3 gen_covers_v2.py [--product n8n|grafana|mcp|dsgvo|blueprint|playbook|cheatsheet] [--all] [--preview]
"""
import os, sys, re, base64, subprocess, argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent / "products" / "cover-templates"
ASSET_SRC = BASE_DIR / "cover-n8n-starter-bundle-sq2.html"

def get_eagle_b64() -> str:
    """Extract eagle logo base64 from existing template."""
    with open(ASSET_SRC) as f:
        content = f.read()
    matches = re.findall(r'src="(data:image/[^"]+)"', content)
    return matches[0] if matches else ""

def n8n_workflow_svg() -> str:
    """n8n-style workflow visualization as SVG."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="rgba(251,146,60,0.6)"/>
    </marker>
  </defs>
  <!-- Connection lines -->
  <line x1="112" y1="50" x2="168" y2="50" stroke="rgba(251,146,60,0.5)" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="272" y1="50" x2="328" y2="50" stroke="rgba(251,146,60,0.5)" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="240" y1="72" x2="240" y2="118" stroke="rgba(251,146,60,0.4)" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arr)"/>
  <line x1="112" y1="150" x2="168" y2="150" stroke="rgba(251,146,60,0.5)" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="272" y1="150" x2="328" y2="150" stroke="rgba(251,146,60,0.5)" stroke-width="2" marker-end="url(#arr)"/>
  <!-- Row 1: Trigger → AI → Output -->
  <rect x="10" y="24" width="102" height="52" rx="10" fill="rgba(251,146,60,0.15)" stroke="#FB923C" stroke-width="1.5" filter="url(#glow)"/>
  <text x="61" y="44" text-anchor="middle" fill="#FB923C" font-size="9" font-family="monospace" font-weight="700">TRIGGER</text>
  <text x="61" y="59" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Stripe Webhook</text>
  <text x="61" y="73" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">New Payment</text>
  <rect x="168" y="24" width="104" height="52" rx="10" fill="rgba(168,85,247,0.15)" stroke="#A855F7" stroke-width="1.5"/>
  <text x="220" y="44" text-anchor="middle" fill="#A855F7" font-size="9" font-family="monospace" font-weight="700">AI NODE</text>
  <text x="220" y="59" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Analyze Intent</text>
  <text x="220" y="73" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">GPT-4 / Ollama</text>
  <rect x="328" y="24" width="102" height="52" rx="10" fill="rgba(34,197,94,0.15)" stroke="#22C55E" stroke-width="1.5"/>
  <text x="379" y="44" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace" font-weight="700">ACTION</text>
  <text x="379" y="59" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Send Report</text>
  <text x="379" y="73" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">Mattermost</text>
  <!-- Row 2: Cron → Transform → Multi-Output -->
  <rect x="10" y="124" width="102" height="52" rx="10" fill="rgba(251,146,60,0.12)" stroke="rgba(251,146,60,0.6)" stroke-width="1.5"/>
  <text x="61" y="144" text-anchor="middle" fill="#FB923C" font-size="9" font-family="monospace" font-weight="700">SCHEDULE</text>
  <text x="61" y="159" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Daily Report</text>
  <text x="61" y="173" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">Cron: 08:00</text>
  <rect x="168" y="124" width="104" height="52" rx="10" fill="rgba(96,165,250,0.15)" stroke="#60A5FA" stroke-width="1.5"/>
  <text x="220" y="144" text-anchor="middle" fill="#60A5FA" font-size="9" font-family="monospace" font-weight="700">HTTP REQUEST</text>
  <text x="220" y="159" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Fetch Metrics</text>
  <text x="220" y="173" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">Prometheus API</text>
  <rect x="328" y="124" width="102" height="52" rx="10" fill="rgba(34,197,94,0.15)" stroke="#22C55E" stroke-width="1.5"/>
  <text x="379" y="144" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace" font-weight="700">NOTIFY</text>
  <text x="379" y="159" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">Alert Team</text>
  <text x="379" y="173" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">MM + Email</text>
  <!-- Status indicator -->
  <circle cx="440" cy="30" r="6" fill="#22C55E" filter="url(#glow)"/>
  <text x="430" y="48" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">LIVE</text>
</svg>'''

def grafana_dashboard_svg() -> str:
    """Grafana-style dashboard panel visualization."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <!-- Dashboard panels -->
  <!-- Panel 1: Line Chart -->
  <rect x="10" y="10" width="220" height="95" rx="8" fill="rgba(15,23,42,0.8)" stroke="rgba(96,165,250,0.3)" stroke-width="1"/>
  <text x="20" y="28" fill="#60A5FA" font-size="9" font-family="monospace" font-weight="700">CPU USAGE</text>
  <text x="190" y="28" text-anchor="end" fill="#22C55E" font-size="11" font-family="monospace" font-weight="700">23%</text>
  <polyline points="20,80 50,70 80,75 110,55 140,60 170,45 200,50 220,42" 
    fill="none" stroke="#60A5FA" stroke-width="2.5" stroke-linejoin="round"/>
  <polyline points="20,80 50,70 80,75 110,55 140,60 170,45 200,50 220,42 220,95 20,95" 
    fill="rgba(96,165,250,0.08)" stroke="none"/>
  <!-- Panel 2: Stat -->
  <rect x="240" y="10" width="110" height="95" rx="8" fill="rgba(15,23,42,0.8)" stroke="rgba(96,165,250,0.3)" stroke-width="1"/>
  <text x="295" y="35" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">MEMORY</text>
  <text x="295" y="65" text-anchor="middle" fill="#F8FAFC" font-size="22" font-family="sans-serif" font-weight="900">7.2</text>
  <text x="295" y="82" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">GB / 16 GB</text>
  <rect x="250" y="90" width="90" height="8" rx="4" fill="rgba(255,255,255,0.1)"/>
  <rect x="250" y="90" width="50" height="8" rx="4" fill="#60A5FA"/>
  <!-- Panel 3: Bar chart -->
  <rect x="360" y="10" width="110" height="95" rx="8" fill="rgba(15,23,42,0.8)" stroke="rgba(96,165,250,0.3)" stroke-width="1"/>
  <text x="415" y="28" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">REQUESTS/s</text>
  <rect x="375" y="75" width="14" height="20" rx="2" fill="rgba(96,165,250,0.5)"/>
  <rect x="393" y="55" width="14" height="40" rx="2" fill="rgba(96,165,250,0.6)"/>
  <rect x="411" y="42" width="14" height="53" rx="2" fill="#60A5FA"/>
  <rect x="429" y="60" width="14" height="35" rx="2" fill="rgba(96,165,250,0.5)"/>
  <text x="415" y="100" text-anchor="middle" fill="#22C55E" font-size="11" font-family="monospace" font-weight="700">↑ 142/s</text>
  <!-- Panel 4: Heatmap row -->
  <rect x="10" y="115" width="460" height="95" rx="8" fill="rgba(15,23,42,0.8)" stroke="rgba(96,165,250,0.3)" stroke-width="1"/>
  <text x="20" y="132" fill="#60A5FA" font-size="9" font-family="monospace" font-weight="700">DOCKER SERVICES — SWARM HEALTH</text>
  <text x="460" y="132" text-anchor="end" fill="#22C55E" font-size="9" font-family="monospace">17/17 UP</text>
  <!-- Service status bars -->
  <rect x="20" y="140" width="80" height="24" rx="4" fill="rgba(34,197,94,0.15)" stroke="rgba(34,197,94,0.4)" stroke-width="1"/>
  <text x="60" y="156" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">voice-gw ●</text>
  <rect x="108" y="140" width="80" height="24" rx="4" fill="rgba(34,197,94,0.15)" stroke="rgba(34,197,94,0.4)" stroke-width="1"/>
  <text x="148" y="156" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">n8n ●</text>
  <rect x="196" y="140" width="80" height="24" rx="4" fill="rgba(34,197,94,0.15)" stroke="rgba(34,197,94,0.4)" stroke-width="1"/>
  <text x="236" y="156" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">grafana ●</text>
  <rect x="284" y="140" width="80" height="24" rx="4" fill="rgba(34,197,94,0.15)" stroke="rgba(34,197,94,0.4)" stroke-width="1"/>
  <text x="324" y="156" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">prometheus ●</text>
  <rect x="372" y="140" width="80" height="24" rx="4" fill="rgba(34,197,94,0.15)" stroke="rgba(34,197,94,0.4)" stroke-width="1"/>
  <text x="412" y="156" text-anchor="middle" fill="#22C55E" font-size="9" font-family="monospace">mattermost ●</text>
  <!-- Uptime bar -->
  <text x="20" y="185" fill="#475569" font-size="8" font-family="monospace">UPTIME 30d</text>
  <rect x="90" y="177" width="360" height="8" rx="4" fill="rgba(255,255,255,0.05)"/>
  <rect x="90" y="177" width="355" height="8" rx="4" fill="rgba(34,197,94,0.6)"/>
  <text x="455" y="185" text-anchor="end" fill="#22C55E" font-size="8" font-family="monospace">99.8%</text>
</svg>'''

def mcp_network_svg() -> str:
    """MCP server network visualization."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <defs>
    <filter id="ng"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Central AI node -->
  <circle cx="240" cy="110" r="38" fill="rgba(34,211,238,0.12)" stroke="#22D3EE" stroke-width="2" filter="url(#ng)"/>
  <circle cx="240" cy="110" r="28" fill="rgba(34,211,238,0.2)" stroke="rgba(34,211,238,0.8)" stroke-width="1.5"/>
  <text x="240" y="105" text-anchor="middle" fill="#22D3EE" font-size="9" font-family="monospace" font-weight="700">AI AGENT</text>
  <text x="240" y="120" text-anchor="middle" fill="#F8FAFC" font-size="8" font-family="monospace">Claude / LLM</text>
  <!-- Connection lines -->
  <line x1="205" y1="95" x2="132" y2="62" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="210" y1="110" x2="110" y2="110" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="205" y1="125" x2="132" y2="158" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="275" y1="95" x2="348" y2="62" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="270" y1="110" x2="370" y2="110" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="275" y1="125" x2="348" y2="158" stroke="rgba(34,211,238,0.4)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="240" y1="72" x2="240" y2="28" stroke="rgba(34,211,238,0.3)" stroke-width="1.5" stroke-dasharray="5,3"/>
  <!-- MCP Server nodes -->
  <rect x="78" y="36" width="108" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="132" y="55" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">n8n-mcp</text>
  <text x="132" y="68" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">7 tools</text>
  <rect x="20" y="84" width="90" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="65" y="103" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">ollama-mcp</text>
  <text x="65" y="116" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">4 tools</text>
  <rect x="78" y="136" width="108" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="132" y="155" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">portainer-mcp</text>
  <text x="132" y="168" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">6 tools</text>
  <rect x="294" y="36" width="108" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="348" y="55" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">proxmox-mcp</text>
  <text x="348" y="68" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">8 tools</text>
  <rect x="370" y="84" width="100" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="420" y="103" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">grafana-mcp</text>
  <text x="420" y="116" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">6 tools</text>
  <rect x="294" y="136" width="108" height="48" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="348" y="155" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">uptime-kuma-mcp</text>
  <text x="348" y="168" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">5 tools</text>
  <!-- Top: mattermost-mcp -->
  <rect x="178" y="5" width="124" height="38" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
  <text x="240" y="21" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">mattermost-mcp</text>
  <text x="240" y="35" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">7 tools · 51 total</text>
</svg>'''

def dsgvo_docs_svg() -> str:
    """DSGVO document stack visualization."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <!-- Document stack -->
  <rect x="80" y="20" width="200" height="260" rx="8" fill="rgba(192,132,252,0.06)" stroke="rgba(192,132,252,0.2)" stroke-width="1" transform="rotate(-8 180 140)"/>
  <rect x="80" y="20" width="200" height="260" rx="8" fill="rgba(192,132,252,0.08)" stroke="rgba(192,132,252,0.25)" stroke-width="1" transform="rotate(-4 180 140)"/>
  <!-- Main document -->
  <rect x="50" y="10" width="210" height="200" rx="10" fill="rgba(15,23,42,0.95)" stroke="rgba(192,132,252,0.5)" stroke-width="2"/>
  <rect x="50" y="10" width="210" height="40" rx="10" fill="rgba(192,132,252,0.15)"/>
  <rect x="50" y="38" width="210" height="12" fill="rgba(192,132,252,0.15)"/>
  <text x="155" y="32" text-anchor="middle" fill="#C084FC" font-size="10" font-family="monospace" font-weight="700">DSGVO ART. 30</text>
  <!-- Document lines -->
  <rect x="68" y="62" width="174" height="7" rx="3" fill="rgba(255,255,255,0.08)"/>
  <rect x="68" y="75" width="140" height="7" rx="3" fill="rgba(255,255,255,0.06)"/>
  <rect x="68" y="88" width="160" height="7" rx="3" fill="rgba(255,255,255,0.06)"/>
  <rect x="68" y="108" width="174" height="7" rx="3" fill="rgba(255,255,255,0.08)"/>
  <rect x="68" y="121" width="120" height="7" rx="3" fill="rgba(255,255,255,0.06)"/>
  <rect x="68" y="134" width="150" height="7" rx="3" fill="rgba(255,255,255,0.06)"/>
  <!-- Checkboxes -->
  <rect x="68" y="155" width="14" height="14" rx="3" fill="rgba(34,197,94,0.2)" stroke="#22C55E" stroke-width="1.5"/>
  <path d="M71 162 L74 165 L80 158" stroke="#22C55E" stroke-width="2" fill="none" stroke-linecap="round"/>
  <rect x="68" y="175" width="14" height="14" rx="3" fill="rgba(34,197,94,0.2)" stroke="#22C55E" stroke-width="1.5"/>
  <path d="M71 182 L74 185 L80 178" stroke="#22C55E" stroke-width="2" fill="none" stroke-linecap="round"/>
  <text x="88" y="164" fill="#94A3B8" font-size="9" font-family="sans-serif">Verarbeitungsverzeichnis erstellt</text>
  <text x="88" y="184" fill="#94A3B8" font-size="9" font-family="sans-serif">TOMs dokumentiert</text>
  <!-- Right side: info boxes -->
  <rect x="290" y="10" width="185" height="56" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(192,132,252,0.4)" stroke-width="1.5"/>
  <text x="382" y="30" text-anchor="middle" fill="#C084FC" font-size="9" font-family="monospace" font-weight="700">GDPR ART. 30</text>
  <text x="382" y="46" text-anchor="middle" fill="#F8FAFC" font-size="11" font-family="sans-serif" font-weight="700">Compliant in</text>
  <text x="382" y="58" text-anchor="middle" fill="#22C55E" font-size="11" font-family="monospace" font-weight="700">30 Minutes</text>
  <rect x="290" y="76" width="185" height="46" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(192,132,252,0.3)" stroke-width="1"/>
  <text x="382" y="93" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">INCLUDES</text>
  <text x="382" y="107" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif">Word + Google Docs Template</text>
  <text x="382" y="117" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="sans-serif">+ PDF + Befüllungsanleitung</text>
  <rect x="290" y="132" width="85" height="42" rx="8" fill="rgba(192,132,252,0.1)" stroke="rgba(192,132,252,0.4)" stroke-width="1.5"/>
  <text x="332" y="150" text-anchor="middle" fill="#C084FC" font-size="17" font-family="sans-serif" font-weight="900">5+</text>
  <text x="332" y="166" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Templates</text>
  <rect x="385" y="132" width="90" height="42" rx="8" fill="rgba(34,197,94,0.1)" stroke="rgba(34,197,94,0.4)" stroke-width="1.5"/>
  <text x="430" y="150" text-anchor="middle" fill="#22C55E" font-size="17" font-family="sans-serif" font-weight="900">€0</text>
  <text x="430" y="166" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Anwalt nötig</text>
  <rect x="290" y="184" width="185" height="36" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(192,132,252,0.2)" stroke-width="1"/>
  <text x="382" y="200" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">DSGVO · GDPR · Data Protection</text>
  <text x="382" y="213" text-anchor="middle" fill="#C084FC" font-size="8" font-family="monospace">Austria · Germany · EU</text>
</svg>'''

def ai_blueprint_svg() -> str:
    """AI Agent team architecture diagram."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <defs>
    <filter id="ag"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Manager agent top -->
  <rect x="165" y="5" width="150" height="52" rx="10" fill="rgba(74,222,128,0.15)" stroke="#4ADE80" stroke-width="2" filter="url(#ag)"/>
  <text x="240" y="24" text-anchor="middle" fill="#4ADE80" font-size="9" font-family="monospace" font-weight="700">MANAGER AGENT</text>
  <text x="240" y="38" text-anchor="middle" fill="#F8FAFC" font-size="10" font-family="sans-serif" font-weight="600">@jim — Orchestrator</text>
  <text x="240" y="50" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Routes · Delegates · Tracks</text>
  <!-- Connecting lines -->
  <line x1="180" y1="57" x2="85" y2="100" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <line x1="220" y1="57" x2="180" y2="100" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <line x1="240" y1="57" x2="240" y2="100" stroke="rgba(74,222,128,0.5)" stroke-width="2"/>
  <line x1="260" y1="57" x2="300" y2="100" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <line x1="300" y1="57" x2="395" y2="100" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <!-- Specialist agents row -->
  <rect x="10" y="100" width="110" height="52" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <text x="65" y="118" text-anchor="middle" fill="#4ADE80" font-size="8" font-family="monospace" font-weight="700">@lisa01</text>
  <text x="65" y="130" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif">Programmer</text>
  <text x="65" y="143" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Python · n8n</text>
  <rect x="130" y="100" width="100" height="52" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <text x="180" y="118" text-anchor="middle" fill="#4ADE80" font-size="8" font-family="monospace" font-weight="700">@echo_log</text>
  <text x="180" y="130" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif">Voice AI</text>
  <text x="180" y="143" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Tools · Memory</text>
  <rect x="190" y="100" width="100" height="52" rx="8" fill="rgba(96,165,250,0.15)" stroke="#60A5FA" stroke-width="2" filter="url(#ag)"/>
  <text x="240" y="118" text-anchor="middle" fill="#60A5FA" font-size="8" font-family="monospace" font-weight="700">LLM BACKEND</text>
  <text x="240" y="130" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif">Ollama GPU</text>
  <text x="240" y="143" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">RTX 3090 · Local</text>
  <rect x="300" y="100" width="100" height="52" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <text x="350" y="118" text-anchor="middle" fill="#4ADE80" font-size="8" font-family="monospace" font-weight="700">@john01</text>
  <text x="350" y="130" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif">QA · Shop</text>
  <text x="350" y="143" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Testing · UI</text>
  <rect x="410" y="100" width="65" height="52" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(74,222,128,0.4)" stroke-width="1.5"/>
  <text x="442" y="118" text-anchor="middle" fill="#4ADE80" font-size="8" font-family="monospace" font-weight="700">+More</text>
  <text x="442" y="130" text-anchor="middle" fill="#F8FAFC" font-size="8" font-family="sans-serif">Copilot</text>
  <text x="442" y="143" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Gemini</text>
  <!-- Tools row bottom -->
  <line x1="240" y1="152" x2="240" y2="175" stroke="rgba(74,222,128,0.3)" stroke-width="1.5" stroke-dasharray="4,3"/>
  <rect x="20" y="175" width="440" height="40" rx="8" fill="rgba(15,23,42,0.8)" stroke="rgba(74,222,128,0.25)" stroke-width="1"/>
  <text x="240" y="190" text-anchor="middle" fill="#4ADE80" font-size="8" font-family="monospace" font-weight="700">SHARED TOOLS &amp; MEMORY</text>
  <text x="240" y="205" text-anchor="middle" fill="#64748B" font-size="8" font-family="monospace">ERPNext · Mattermost · n8n · Grafana · Neo4j · ChromaDB</text>
</svg>'''

def playbook_stack_svg() -> str:
    """Local AI stack layers visualization."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <!-- Stack layers from bottom to top -->
  <!-- Layer 1: Hardware -->
  <rect x="60" y="185" width="360" height="32" rx="6" fill="rgba(16,185,129,0.08)" stroke="rgba(16,185,129,0.3)" stroke-width="1.5"/>
  <text x="240" y="203" text-anchor="middle" fill="#6EE7B7" font-size="9" font-family="monospace" font-weight="700">HARDWARE</text>
  <text x="240" y="214" text-anchor="middle" fill="#475569" font-size="8" font-family="monospace">RTX 3090 · Proxmox VE · Docker Swarm</text>
  <!-- Layer 2: Infra -->
  <rect x="50" y="148" width="380" height="32" rx="6" fill="rgba(16,185,129,0.1)" stroke="rgba(16,185,129,0.35)" stroke-width="1.5"/>
  <text x="240" y="163" text-anchor="middle" fill="#10B981" font-size="9" font-family="monospace" font-weight="700">INFRASTRUCTURE</text>
  <text x="240" y="176" text-anchor="middle" fill="#475569" font-size="8" font-family="monospace">n8n · Grafana · Prometheus · Mattermost</text>
  <!-- Layer 3: AI Stack -->
  <rect x="40" y="110" width="400" height="33" rx="6" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.45)" stroke-width="2"/>
  <text x="240" y="125" text-anchor="middle" fill="#10B981" font-size="9" font-family="monospace" font-weight="700">AI STACK</text>
  <text x="240" y="138" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Ollama · Open WebUI · Voice Gateway · RAG</text>
  <!-- Layer 4: Agents -->
  <rect x="30" y="70" width="420" height="34" rx="6" fill="rgba(16,185,129,0.15)" stroke="rgba(16,185,129,0.55)" stroke-width="2"/>
  <text x="240" y="85" text-anchor="middle" fill="#10B981" font-size="9" font-family="monospace" font-weight="700">AGENT LAYER</text>
  <text x="240" y="100" text-anchor="middle" fill="#94A3B8" font-size="8" font-family="monospace">Claude Code · Copilot · Gemini · MCP Servers</text>
  <!-- Layer 5: Business -->
  <rect x="20" y="28" width="440" height="36" rx="6" fill="rgba(16,185,129,0.18)" stroke="#10B981" stroke-width="2.5"/>
  <text x="240" y="44" text-anchor="middle" fill="#10B981" font-size="9" font-family="monospace" font-weight="700">BUSINESS AUTOMATION</text>
  <text x="240" y="57" text-anchor="middle" fill="#F8FAFC" font-size="9" font-family="sans-serif" font-weight="600">ERPNext · Shop · Analytics · Reporting</text>
  <!-- Side labels -->
  <text x="8" y="210" fill="rgba(16,185,129,0.3)" font-size="8" font-family="monospace" transform="rotate(-90 8 170)">FOUNDATION</text>
  <text x="8" y="50" fill="rgba(16,185,129,0.6)" font-size="8" font-family="monospace" transform="rotate(-90 8 85)">PRODUCT</text>
</svg>'''

def cheatsheet_terminal_svg() -> str:
    """MCP Cheat Sheet terminal/code visualization."""
    return '''<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="width:480px;height:220px">
  <!-- Terminal window -->
  <rect x="10" y="5" width="285" height="210" rx="10" fill="rgba(15,23,42,0.95)" stroke="rgba(34,211,238,0.3)" stroke-width="1.5"/>
  <rect x="10" y="5" width="285" height="32" rx="10" fill="rgba(30,41,59,0.9)"/>
  <rect x="10" y="25" width="285" height="12" fill="rgba(30,41,59,0.9)"/>
  <circle cx="30" cy="21" r="5" fill="#FF5F57"/>
  <circle cx="46" cy="21" r="5" fill="#FFBD2E"/>
  <circle cx="62" cy="21" r="5" fill="#28C840"/>
  <text x="152" y="25" text-anchor="middle" fill="#64748B" font-size="9" font-family="monospace">MCP Quick Reference</text>
  <!-- Terminal content -->
  <text x="22" y="55" fill="#22D3EE" font-size="9" font-family="monospace">$ claude mcp add n8n-mcp</text>
  <text x="22" y="70" fill="#22C55E" font-size="9" font-family="monospace">✓ Added n8n-mcp (7 tools)</text>
  <text x="22" y="88" fill="#22D3EE" font-size="9" font-family="monospace">$ claude mcp add proxmox-mcp</text>
  <text x="22" y="103" fill="#22C55E" font-size="9" font-family="monospace">✓ Added proxmox-mcp (8 tools)</text>
  <text x="22" y="118" fill="#475569" font-size="9" font-family="monospace">───────────────────────────</text>
  <text x="22" y="135" fill="#A855F7" font-size="9" font-family="monospace">// Available commands:</text>
  <text x="22" y="150" fill="#94A3B8" font-size="9" font-family="monospace">list_workflows    → n8n</text>
  <text x="22" y="164" fill="#94A3B8" font-size="9" font-family="monospace">get_vm_status     → proxmox</text>
  <text x="22" y="178" fill="#94A3B8" font-size="9" font-family="monospace">send_message      → mattermost</text>
  <text x="22" y="192" fill="#94A3B8" font-size="9" font-family="monospace">get_dashboards    → grafana</text>
  <text x="22" y="207" fill="#22D3EE" font-size="9" font-family="monospace">█</text>
  <!-- Right side: tool count panels -->
  <rect x="308" y="5" width="165" height="50" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.4)" stroke-width="1.5"/>
  <text x="390" y="24" text-anchor="middle" fill="#22D3EE" font-size="22" font-family="sans-serif" font-weight="900">51</text>
  <text x="390" y="42" text-anchor="middle" fill="#94A3B8" font-size="9" font-family="monospace">Total MCP Tools</text>
  <rect x="308" y="63" width="77" height="42" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.3)" stroke-width="1"/>
  <text x="346" y="81" text-anchor="middle" fill="#F8FAFC" font-size="16" font-family="sans-serif" font-weight="700">8</text>
  <text x="346" y="97" text-anchor="middle" fill="#64748B" font-size="8" font-family="monospace">Servers</text>
  <rect x="395" y="63" width="78" height="42" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.3)" stroke-width="1"/>
  <text x="434" y="81" text-anchor="middle" fill="#22C55E" font-size="13" font-family="monospace" font-weight="700">FREE</text>
  <text x="434" y="97" text-anchor="middle" fill="#64748B" font-size="8" font-family="monospace">Open Source</text>
  <!-- Compatible with -->
  <rect x="308" y="115" width="165" height="100" rx="8" fill="rgba(15,23,42,0.9)" stroke="rgba(34,211,238,0.25)" stroke-width="1"/>
  <text x="390" y="133" text-anchor="middle" fill="#22D3EE" font-size="8" font-family="monospace" font-weight="700">COMPATIBLE WITH</text>
  <text x="322" y="152" fill="#F8FAFC" font-size="9" font-family="sans-serif">✓ Claude Code (CLI)</text>
  <text x="322" y="167" fill="#F8FAFC" font-size="9" font-family="sans-serif">✓ Claude Desktop</text>
  <text x="322" y="182" fill="#F8FAFC" font-size="9" font-family="sans-serif">✓ Open WebUI</text>
  <text x="322" y="197" fill="#F8FAFC" font-size="9" font-family="sans-serif">✓ Custom AI Agents</text>
  <text x="322" y="212" fill="#64748B" font-size="8" font-family="sans-serif">+ Any MCP-compatible host</text>
</svg>'''

PRODUCTS = {
    "n8n": {
        "slug": "cover-n8n-starter-bundle-sq2",
        "output": "n8n-starter-bundle-cover.png",
        "badge": "N8N · AUTOMATION BUNDLE",
        "title_line1": "n8n Starter",
        "title_line2": "Bundle",
        "accent_name": "n8n",
        "accent": "#FB923C",
        "accent_rgb": "251,146,60",
        "bg_gradient": "145deg, #0F172A 0%, #1a1205 55%, #0F172A 100%",
        "tagline": "3 AI Workflows — Ready to Import & Run",
        "outcome": "Automate your homelab in 30 minutes",
        "stats": [("3", "Workflows"), ("30+", "Nodes"), ("100%", "Self-Hosted"), ("0", "Vendor Lock-in")],
        "svg_fn": n8n_workflow_svg,
    },
    "grafana": {
        "slug": "cover-grafana-dashboard-pack-sq2",
        "output": "grafana-dashboard-pack-cover.png",
        "badge": "GRAFANA · MONITORING PACK",
        "title_line1": "Grafana",
        "title_line2": "Dashboard Pack",
        "accent_name": "grafana",
        "accent": "#60A5FA",
        "accent_rgb": "96,165,250",
        "bg_gradient": "145deg, #0F172A 0%, #051226 55%, #0F172A 100%",
        "tagline": "4 Production Dashboards — Import in 60 Seconds",
        "outcome": "Full stack visibility in under 5 minutes",
        "stats": [("4", "Dashboards"), ("200+", "Panels"), ("17", "Services"), ("99.8%", "Uptime Tracked")],
        "svg_fn": grafana_dashboard_svg,
    },
    "mcp": {
        "slug": "cover-homelab-mcp-bundle-sq2",
        "output": "homelab-mcp-bundle-cover.png",
        "badge": "MCP · HOMELAB BUNDLE",
        "title_line1": "Homelab MCP",
        "title_line2": "Bundle",
        "accent_name": "mcp",
        "accent": "#22D3EE",
        "accent_rgb": "34,211,238",
        "bg_gradient": "145deg, #0F172A 0%, #051a1f 55%, #0F172A 100%",
        "tagline": "8 MCP Servers · 51 Tools for Your AI Agent",
        "outcome": "Give Claude control of your entire homelab",
        "stats": [("8", "MCP Servers"), ("51", "Tools"), ("100%", "Free"), ("1-Click", "Install")],
        "svg_fn": mcp_network_svg,
    },
    "dsgvo": {
        "slug": "cover-dsgvo-art30-bundle-sq2",
        "output": "dsgvo-art30-bundle-cover.png",
        "badge": "DSGVO · GDPR COMPLIANCE",
        "title_line1": "DSGVO Art. 30",
        "title_line2": "Bundle",
        "accent_name": "dsgvo",
        "accent": "#C084FC",
        "accent_rgb": "192,132,252",
        "bg_gradient": "145deg, #0F172A 0%, #12051e 55%, #0F172A 100%",
        "tagline": "5 Templates — Compliant in 30 Minutes",
        "outcome": "No lawyer needed. No fines. Just done.",
        "stats": [("5+", "Templates"), ("Art. 30", "DSGVO"), ("Word + PDF", "Formate"), ("30 min", "to Done")],
        "svg_fn": dsgvo_docs_svg,
    },
    "blueprint": {
        "slug": "cover-ai-agent-blueprint-sq2",
        "output": "ai-agent-blueprint-cover.png",
        "badge": "AI AGENT · TEAM BLUEPRINT",
        "title_line1": "AI Agent Team",
        "title_line2": "Blueprint",
        "accent_name": "blueprint",
        "accent": "#4ADE80",
        "accent_rgb": "74,222,128",
        "bg_gradient": "145deg, #0F172A 0%, #051205 55%, #0F172A 100%",
        "tagline": "Build a 10-Agent Team on Your Local Hardware",
        "outcome": "From zero to autonomous AI team in 1 weekend",
        "stats": [("10", "Agents"), ("5", "Swarm Nodes"), ("100%", "Local AI"), ("0", "Monthly Fees")],
        "svg_fn": ai_blueprint_svg,
    },
    "playbook": {
        "slug": "cover-localai-playbook-sq2",
        "output": "localai-playbook-cover.png",
        "badge": "PLAYBOOK · LOCAL AI STACK",
        "title_line1": "Local AI Stack",
        "title_line2": "Playbook",
        "accent_name": "playbook",
        "accent": "#10B981",
        "accent_rgb": "16,185,129",
        "bg_gradient": "145deg, #0F172A 0%, #051a0f 55%, #0F172A 100%",
        "tagline": "Complete Guide — Self-Hosted AI in Production",
        "outcome": "Replace ChatGPT. Own your data. Ship faster.",
        "stats": [("5", "Stack Layers"), ("100%", "Self-Hosted"), ("17", "Services"), ("RTX", "GPU Ready")],
        "svg_fn": playbook_stack_svg,
    },
    "cheatsheet": {
        "slug": "cover-mcp-cheat-sheet-sq2",
        "output": "mcp-cheat-sheet-cover.png",
        "badge": "FREE · MCP QUICK REFERENCE",
        "title_line1": "MCP Server",
        "title_line2": "Cheat Sheet",
        "accent_name": "cheatsheet",
        "accent": "#22D3EE",
        "accent_rgb": "34,211,238",
        "bg_gradient": "145deg, #0F172A 0%, #051a1f 55%, #0F172A 100%",
        "tagline": "51 Tools · 8 Servers · One Reference Card",
        "outcome": "Copy. Paste. Control your homelab with AI.",
        "stats": [("51", "Tools"), ("8", "Servers"), ("FREE", "Download"), ("PDF", "Format")],
        "svg_fn": cheatsheet_terminal_svg,
    },
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{
    width: 800px; height: 800px; overflow: hidden;
    background: #0F172A;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    color: #F8FAFC;
  }}
  .container {{
    width: 800px; height: 800px;
    background: linear-gradient({bg_gradient});
    position: relative;
    display: flex; flex-direction: column;
    overflow: hidden;
  }}
  .container::before {{
    content: '';
    position: absolute; inset: 0;
    background-image:
      linear-gradient(rgba({accent_rgb},0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba({accent_rgb},0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 1;
  }}
  .glow-center {{
    position: absolute;
    width: 700px; height: 700px;
    background: radial-gradient(ellipse, rgba({accent_rgb},0.07) 0%, transparent 65%);
    top: 50%; left: 50%; transform: translate(-50%, -50%);
    z-index: 2;
  }}
  .eagle-bg {{
    position: absolute;
    width: 420px; height: 420px;
    bottom: -30px; right: -30px;
    opacity: 0.06;
    z-index: 3;
  }}
  .eagle-bg img {{ width: 100%; height: 100%; object-fit: contain; }}
  /* HEADER */
  .header {{
    position: relative; z-index: 20;
    display: flex; align-items: center; justify-content: space-between;
    padding: 24px 36px 0;
    flex-shrink: 0;
  }}
  .brand {{
    display: flex; align-items: center; gap: 10px;
  }}
  .brand img {{
    width: 36px; height: 36px; object-fit: contain;
    filter: drop-shadow(0 0 10px rgba({accent_rgb},0.4));
  }}
  .brand-name {{
    font-size: 12px; font-weight: 700; color: #475569;
    letter-spacing: 1.5px; text-transform: uppercase;
  }}
  .badge-cat {{
    background: rgba({accent_rgb},0.12);
    border: 1px solid rgba({accent_rgb},0.45);
    color: {accent};
    font-size: 10px; font-weight: 800;
    padding: 5px 16px; border-radius: 50px;
    letter-spacing: 2.5px; text-transform: uppercase;
    font-family: 'Courier New', monospace;
  }}
  /* MAIN CONTENT */
  .main {{
    position: relative; z-index: 10;
    padding: 20px 40px 0;
    flex-shrink: 0;
  }}
  h1 {{
    font-size: 62px; font-weight: 900;
    line-height: 1.0; letter-spacing: -2px;
    margin-bottom: 10px;
  }}
  h1 .accent {{ color: {accent}; }}
  .tagline {{
    font-size: 17px; font-weight: 400;
    color: #94A3B8; line-height: 1.4;
    margin-bottom: 6px;
  }}
  .outcome {{
    font-size: 14px; font-weight: 600;
    color: {accent}; opacity: 0.8;
    font-family: 'Courier New', monospace;
    letter-spacing: 0.5px;
  }}
  /* SVG VISUAL */
  .visual {{
    position: relative; z-index: 10;
    padding: 14px 32px 0;
    flex: 1;
    display: flex; align-items: flex-start;
  }}
  .visual-inner {{
    background: rgba(15,23,42,0.5);
    border: 1px solid rgba({accent_rgb},0.2);
    border-radius: 12px;
    padding: 8px;
    width: 100%;
    box-shadow: 0 0 40px rgba({accent_rgb},0.06);
  }}
  /* STATS */
  .stats {{
    position: relative; z-index: 20;
    display: flex; gap: 0;
    margin: 12px 0 0;
    flex-shrink: 0;
    border-top: 1px solid rgba(255,255,255,0.05);
  }}
  .stat {{
    flex: 1;
    padding: 12px 0;
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.05);
  }}
  .stat:last-child {{ border-right: none; }}
  .stat-num {{
    font-size: 22px; font-weight: 900;
    color: {accent};
    line-height: 1.1;
    display: block;
  }}
  .stat-label {{
    font-size: 10px; font-weight: 600;
    color: #475569;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Courier New', monospace;
  }}
  /* FOOTER */
  .footer {{
    position: relative; z-index: 20;
    display: flex; align-items: center; justify-content: center;
    gap: 10px;
    padding: 10px 0 14px;
    border-top: 1px solid rgba({accent_rgb},0.12);
    flex-shrink: 0;
  }}
  .footer-text {{
    font-size: 11px; font-weight: 700;
    color: {accent}; opacity: 0.7;
    letter-spacing: 2.5px; text-transform: uppercase;
    font-family: 'Courier New', monospace;
  }}
  .footer-sep {{ color: rgba(255,255,255,0.15); }}
  .footer-sub {{
    font-size: 10px; color: #334155;
    letter-spacing: 1px;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="glow-center"></div>
  <div class="eagle-bg"><img src="{eagle_b64}" alt=""></div>
  <!-- Header -->
  <div class="header">
    <div class="brand">
      <img src="{eagle_b64}" alt="ai-engineering.at">
      <span class="brand-name">ai-engineering.at</span>
    </div>
    <div class="badge-cat">{badge}</div>
  </div>
  <!-- Title -->
  <div class="main">
    <h1><span class="accent">{title_line1}</span><br>{title_line2}</h1>
    <p class="tagline">{tagline}</p>
    <p class="outcome">→ {outcome}</p>
  </div>
  <!-- Visual -->
  <div class="visual">
    <div class="visual-inner">{svg_content}</div>
  </div>
  <!-- Stats -->
  <div class="stats">
    {stats_html}
  </div>
  <!-- Footer -->
  <div class="footer">
    <span class="footer-text">ai-engineering.at</span>
    <span class="footer-sep">·</span>
    <span class="footer-sub">Local AI · Self-Hosted · Open Source</span>
  </div>
</div>
</body>
</html>'''

def make_stats_html(stats):
    parts = []
    for num, label in stats:
        parts.append(f'<div class="stat"><span class="stat-num">{num}</span><span class="stat-label">{label}</span></div>')
    return "\n    ".join(parts)

def generate_html(product_key: str, eagle_b64: str) -> str:
    p = PRODUCTS[product_key]
    svg = p["svg_fn"]()
    stats_html = make_stats_html(p["stats"])
    return HTML_TEMPLATE.format(
        bg_gradient=p["bg_gradient"],
        accent_rgb=p["accent_rgb"],
        accent=p["accent"],
        eagle_b64=eagle_b64,
        badge=p["badge"],
        title_line1=p["title_line1"],
        title_line2=p["title_line2"],
        tagline=p["tagline"],
        outcome=p["outcome"],
        svg_content=svg,
        stats_html=stats_html,
    )

def render_html_to_png(html_path: str, png_path: str) -> bool:
    """Render HTML to PNG using Chromium."""
    result = subprocess.run(
        ["chromium-browser", "--headless", "--no-sandbox", "--disable-gpu",
         "--disable-software-rasterizer", "--window-size=800,800",
         f"--screenshot={png_path}", f"file://{html_path}"],
        capture_output=True, text=True, timeout=30
    )
    return os.path.exists(png_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", choices=list(PRODUCTS.keys()), help="Single product")
    parser.add_argument("--all", action="store_true", help="Generate all covers")
    parser.add_argument("--html-only", action="store_true", help="Only write HTML, don't render")
    args = parser.parse_args()

    print("Loading eagle asset...")
    eagle_b64 = get_eagle_b64()
    if not eagle_b64:
        print("ERROR: Could not load eagle asset")
        sys.exit(1)
    print(f"  Asset: {len(eagle_b64)} chars")

    keys = list(PRODUCTS.keys()) if args.all else ([args.product] if args.product else [])
    if not keys:
        print("Use --all or --product <name>")
        print("Products:", list(PRODUCTS.keys()))
        sys.exit(1)

    for key in keys:
        p = PRODUCTS[key]
        html_path = BASE_DIR / f"cover-{p['slug'].replace('cover-','')}.v2.html"
        # Use same slot as sq2 but new version
        html_path = BASE_DIR / f"cover-v2-{key}.html"
        png_path = BASE_DIR / p["output"]
        
        print(f"\n[{key}] Generating HTML...")
        html = generate_html(key, eagle_b64)
        with open(html_path, "w") as f:
            f.write(html)
        print(f"  Written: {html_path}")

        if not args.html_only:
            print(f"  Rendering to PNG...")
            if render_html_to_png(str(html_path), str(png_path)):
                size = os.path.getsize(png_path) // 1024
                print(f"  OK: {png_path} ({size} KB)")
            else:
                print(f"  ERROR: PNG not created")

    print("\nDone.")

if __name__ == "__main__":
    main()
