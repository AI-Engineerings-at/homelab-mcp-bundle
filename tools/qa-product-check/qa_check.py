#!/usr/bin/env python3
"""
QA Product Check -- @john01 Skill
Prueft vor jedem Release: Dateien, Cover, Preise, Service-Health.
Usage: python3 tools/qa-product-check/qa_check.py [product_id|all]
"""
import os, sys, json, urllib.request
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[2]
FILES_DIR = BASE_DIR / "tools/download-issuer/files"
COVERS_DIR = BASE_DIR / "products/covers"
DOWNLOAD_ISSUER_URL = os.environ.get("DOWNLOAD_ISSUER_URL", "http://127.0.0.1:3002")

PRODUCTS = {
    "playbook01":         {"name": "Local AI Stack Playbook",        "price_eur": 49,  "file": "Der-Lokale-AI-Stack-Playbook.pdf",        "platform": "stripe",  "cover": "thumbnail-localai-playbook.png"},
    "n8n-bundle":         {"name": "n8n Starter Bundle",             "price_eur": 29,  "file": "n8n-bundle.zip",                          "platform": "gumroad", "cover": "thumbnail-n8n-starter-bundle.png"},
    "grafana-pack":       {"name": "Grafana Dashboard Pack",         "price_eur": 39,  "file": "grafana-dashboard-pack.zip",              "platform": "gumroad", "cover": "thumbnail-grafana-dashboard-pack.png"},
    "dsgvo-template":     {"name": "DSGVO Art.30 Bundle",            "price_eur": 79,  "file": "dsgvo-art30-bundle.zip",                  "platform": "gumroad", "cover": "thumbnail-dsgvo-art30-bundle.png"},
    "ai-agent-blueprint": {"name": "AI Agent Team Blueprint",        "price_eur": 19,  "file": "ai-agent-team-blueprint.zip",             "platform": "gumroad", "cover": "thumbnail-ai-agent-blueprint.png"},
    "homelab-mcp-bundle": {"name": "Homelab MCP Bundle",             "price_eur": 0,   "file": "Homelab-MCP-Bundle-Cheat-Sheet.pdf",      "platform": "gumroad", "cover": "thumbnail-homelab-mcp-bundle.png"},
    "komplett-bundle":    {"name": "AI Engineering Komplett Bundle", "price_eur": 149, "file": "ai-engineering-komplett-bundle.zip",       "platform": "gumroad", "cover": "thumbnail-komplett-bundle.png"},
}

GREEN="[92m"; RED="[91m"; YELLOW="[93m"; CYAN="[96m"; BOLD="[1m"; RESET="[0m"

def check(label, ok, detail=""):
    icon = f"{GREEN}[OK]{RESET}" if ok else f"{RED}[FAIL]{RESET}"
    suffix = f"  {YELLOW}{detail}{RESET}" if detail else ""
    print(f"  {icon}  {label}{suffix}")
    return ok

def check_product(pid):
    p = PRODUCTS[pid]
    fpath = FILES_DIR / p["file"]
    file_ok = fpath.exists()
    r1 = check(f"Datei:  {p['file']}", file_ok, f"{fpath.stat().st_size//1024} KB" if file_ok else f"FEHLT in {FILES_DIR}")
    cover_path = COVERS_DIR / p["cover"]
    r2 = check(f"Cover:  {p['cover']}", cover_path.exists(), "" if cover_path.exists() else "FEHLT -- gen_thumbnails_v12.py ausfuehren")
    price = p["price_eur"]
    r3 = check(f"Preis:  {'FREE' if price==0 else f'EUR {price}'} [{p['platform'].upper()}]", price >= 0)
    return r1 and r2 and r3

def check_service_health():
    print(f"\n{CYAN}Download-Issuer Health{RESET}  {DOWNLOAD_ISSUER_URL}")
    try:
        with urllib.request.urlopen(f"{DOWNLOAD_ISSUER_URL}/health", timeout=3) as r:
            data = json.loads(r.read())
            return check(f"Service UP -- {data.get('products_available',0)}/{data.get('products_configured',0)} Produkte", data.get("status")=="ok")
    except Exception as exc:
        check("Download-Issuer erreichbar", False, str(exc))
        print(f"  {YELLOW}-> Starten: python3 tools/download-issuer/app.py{RESET}")
        return False

def run_qa(ids):
    print(f"\n{BOLD}{'='*60}{RESET}\n{BOLD}  QA Product Check -- @john01  |  AI Engineering{RESET}\n  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{BOLD}{'='*60}{RESET}")
    check_service_health()
    failed = 0
    for pid in ids:
        if pid not in PRODUCTS:
            print(f"\n{RED}Unbekanntes Produkt: {pid}{RESET}"); failed += 1; continue
        print(f"\n{CYAN}  {PRODUCTS[pid]['name']}  ({pid}){RESET}")
        if not check_product(pid): failed += 1
    print(f"\n{BOLD}{'='*60}{RESET}")
    if failed == 0: print(f"  {GREEN}{BOLD}Alle Checks bestanden -- Release-ready!{RESET}")
    else: print(f"  {RED}{BOLD}{failed} Produkt(e) NICHT release-ready{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
    return failed

def main():
    args = sys.argv[1:]
    ids = list(PRODUCTS.keys()) if not args or args[0]=="all" else args
    sys.exit(min(run_qa(ids), 1))

if __name__ == "__main__": main()
