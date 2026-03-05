#!/usr/bin/env python3
"""
Copywriter AI -- @john01 Skill
Generiert Produkt-Texte in DE+EN via Ollama (lokal).
Usage: python3 tools/copywriter-ai/copywriter.py <product_id> [--platform gumroad|stripe|landing|email] [--lang de|en|both]
"""
import os, sys, json, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://10.40.10.99:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
OUTPUT_DIR = BASE_DIR / "products/copy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = {
    "playbook01": {
        "name": "Local AI Stack Playbook",
        "tagline": "Dein kompletter Guide fuer den eigenen AI-Stack zuhause",
        "price": "EUR 49",
        "platform": "stripe",
        "features": [
            "180+ Seiten professioneller Guide",
            "Docker Swarm Setup Schritt-fuer-Schritt",
            "15+ Services konfiguriert und erklaert",
            "n8n, Ollama, Open WebUI, Grafana und mehr",
            "Lifetime Updates inklusive",
        ],
        "category": "Homelab / AI Infrastructure",
        "audience": "Technikbegeisterte, Homelab-Enthusiasten, DevOps-Einsteiger",
    },
    "n8n-bundle": {
        "name": "n8n Starter Bundle",
        "tagline": "13 sofort einsatzbereite n8n Workflows fuer KI-Automation",
        "price": "EUR 29",
        "platform": "gumroad",
        "features": [
            "13 produktionsreife n8n Workflows",
            "AI-Alerting, Slack, E-Mail, Webhooks",
            "Import mit einem Klick",
            "Kommentierte Nodes fuer einfaches Anpassen",
            "Bonus: Setup-Guide PDF",
        ],
        "category": "n8n / Workflow Automation",
        "audience": "n8n-Nutzer, Automatisierer, KI-Interessierte",
    },
    "grafana-pack": {
        "name": "Grafana Dashboard Pack",
        "tagline": "Professionelle Monitoring-Dashboards fuer deinen Stack",
        "price": "EUR 39",
        "platform": "gumroad",
        "features": [
            "6 fertige Grafana Dashboards",
            "Docker Swarm, Node Exporter, n8n, AI-Services",
            "1-Klick Import via JSON",
            "Prometheus & Loki kompatibel",
            "Bonus: Alert-Regeln fuer kritische Events",
        ],
        "category": "Monitoring / Grafana",
        "audience": "Homelab-Admins, DevOps, Monitoring-Enthusiasten",
    },
    "dsgvo-template": {
        "name": "DSGVO Art.30 Bundle",
        "tagline": "DSGVO-konform in 30 Minuten -- fertige Vorlagen fuer KMUs",
        "price": "EUR 79",
        "platform": "gumroad",
        "features": [
            "Vollstaendiges Verarbeitungsverzeichnis (Art.30)",
            "Word + PDF Vorlagen",
            "Muster-Datenschutzerklaerung",
            "Auftragsverarbeitungsvertrag (AVV)",
            "Erklaert in einfacher Sprache, kein Jurist noetig",
        ],
        "category": "DSGVO / Legal / Compliance",
        "audience": "KMUs, Freelancer, Online-Shop-Betreiber",
    },
    "ai-agent-blueprint": {
        "name": "AI Agent Team Blueprint",
        "tagline": "Baue dein eigenes KI-Agenten-Team mit Claude und n8n",
        "price": "EUR 19",
        "platform": "gumroad",
        "features": [
            "Vollstaendige Agent-Architektur erklaert",
            "42 Diagramme und Flowcharts",
            "Multi-Agent Kommunikation Schritt-fuer-Schritt",
            "Mattermost + n8n Integration",
            "Reales Produktions-Beispiel inklusive",
        ],
        "category": "AI Agents / Architecture",
        "audience": "KI-Entwickler, Tech-Enthusiasten, Automations-Profis",
    },
    "homelab-mcp-bundle": {
        "name": "Homelab MCP Bundle",
        "tagline": "Model Context Protocol fuer dein Homelab -- kostenlos",
        "price": "GRATIS",
        "platform": "gumroad",
        "features": [
            "8 fertige MCP-Server (n8n, Grafana, Portainer und mehr)",
            "51 Tools insgesamt",
            "5-Minuten Setup",
            "Claude Desktop + Open WebUI kompatibel",
            "Aktiv gepflegte Community",
        ],
        "category": "MCP / AI Tools",
        "audience": "Claude-Nutzer, Homelab-Enthusiasten, AI-Tinkerer",
    },
    "komplett-bundle": {
        "name": "AI Engineering Komplett Bundle",
        "tagline": "Alles was du brauchst fuer deinen AI-Stack -- zum Sparpreis",
        "price": "EUR 149",
        "platform": "gumroad",
        "features": [
            "Alle 5 Einzelprodukte inklusive",
            "EUR 215 Wert -- spare EUR 66",
            "Playbook + n8n + Grafana + DSGVO + Blueprint",
            "Lifetime Updates fuer alle Produkte",
            "Bonus: Exklusiver Discord-Zugang",
        ],
        "category": "Bundle / Alle Produkte",
        "audience": "Alle -- ideal fuer Einsteiger und Profis gleichermassen",
    },
}

GUMROAD_PROMPT_DE = """Du bist ein erfahrener Texter fuer digitale Produkte im deutschsprachigen Tech-Raum.
Schreibe ein Gumroad-Listing fuer das folgende Produkt. Ton: klar, direkt, technisch aber zugaenglich.
KEIN Marketing-Bullshit. Echte Mehrwerte kommunizieren.

Produkt: {name}
Tagline: {tagline}
Preis: {price}
Zielgruppe: {audience}
Features: {features}

Format:
## [Titel]
[Kurze Hook-Sentence, 1 Zeile]

### Was bekommst du?
[Bullet-Liste der Features, konkret]

### Fuer wen ist das?
[2-3 Saetze Zielgruppe]

### Details
[Preis, Format, Besonderheiten]

Schreibe in klarem Deutsch. Max 300 Woerter."""

GUMROAD_PROMPT_EN = """You are an experienced copywriter for digital tech products.
Write a Gumroad listing for the following product. Tone: clear, direct, technical but accessible.
NO marketing fluff. Communicate real value.

Product: {name}
Tagline: {tagline}
Price: {price}
Audience: {audience}
Features: {features}

Format:
## [Title]
[Short hook sentence, 1 line]

### What do you get?
[Bullet list of features, specific]

### Who is this for?
[2-3 sentences about target audience]

### Details
[Price, format, highlights]

Write in clear English. Max 300 words."""


def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read()).get("response", "").strip()
    except Exception as exc:
        return f"[OLLAMA FEHLER: {exc}]"


def generate_copy(pid: str, platform: str = "gumroad", lang: str = "both") -> dict:
    if pid not in PRODUCTS:
        print(f"Unbekanntes Produkt: {pid}")
        sys.exit(1)
    p = PRODUCTS[pid]
    features_str = "\n".join(f"- {f}" for f in p["features"])
    result = {"product_id": pid, "name": p["name"], "platform": platform, "generated_at": datetime.now().isoformat(), "copy": {}}

    if lang in ("de", "both"):
        print(f"  Generiere DE-Copy via Ollama ({OLLAMA_MODEL})...")
        prompt_de = GUMROAD_PROMPT_DE.format(name=p["name"], tagline=p["tagline"], price=p["price"], audience=p["audience"], features=features_str)
        result["copy"]["de"] = call_ollama(prompt_de)

    if lang in ("en", "both"):
        print(f"  Generiere EN-Copy via Ollama ({OLLAMA_MODEL})...")
        prompt_en = GUMROAD_PROMPT_EN.format(name=p["name"], tagline=p["tagline"], price=p["price"], audience=p["audience"], features=features_str)
        result["copy"]["en"] = call_ollama(prompt_en)

    return result


def save_and_print(result: dict) -> Path:
    pid = result["product_id"]
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = OUTPUT_DIR / f"{pid}-{ts}.md"
    lines = [f"# {result['name']} -- Copy [{result['platform'].upper()}]", f"> Generiert: {result['generated_at']}", ""]
    for lang, text in result["copy"].items():
        lines += [f"## {lang.upper()}", "", text, ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n{'='*60}\n{chr(10).join(lines)}\n{'='*60}")
    print(f"\nGespeichert: {out_path}")
    return out_path


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 copywriter.py <product_id> [--platform gumroad|stripe|landing] [--lang de|en|both]")
        print(f"Produkte: {', '.join(PRODUCTS)}")
        sys.exit(1)
    pid = args[0]
    platform = "gumroad"
    lang = "both"
    for i, a in enumerate(args):
        if a == "--platform" and i+1 < len(args): platform = args[i+1]
        if a == "--lang" and i+1 < len(args): lang = args[i+1]
    print(f"\nCopywriter AI -- {pid} [{platform.upper()}]")
    result = generate_copy(pid, platform, lang)
    save_and_print(result)

if __name__ == "__main__":
    main()
