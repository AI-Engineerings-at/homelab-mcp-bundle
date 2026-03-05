# Skill: qa-product-check (v1.0)

> **@john01-Idee**: QA vor jedem Release systematisch pruefen — keine gebrochenen Links,
> keine fehlenden Files, keine falschen Preise mehr.

## Zweck
Prueft alle Produkte vor einem Release vollautomatisch:
Download-Dateien vorhanden, Cover generiert, Preise korrekt, Download-Issuer erreichbar.

## Usage

```bash
# Alle 7 Produkte pruefen (Standard)
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py

# Einzelne Produkte
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py n8n-bundle
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py playbook01 grafana-pack

# Explizit alle
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py all
```

**Exit Codes**: `0` = alles OK | `1` = mindestens 1 Produkt nicht release-ready

## Checks pro Produkt

| Check | Was wird geprueft | Fehlerbehebung |
|-------|------------------|----------------|
| Datei | `files/<name>` existiert + Groesse | Datei in `tools/download-issuer/files/` ablegen |
| Cover | `products/covers/thumbnail-{id}.png` | `gen_thumbnails_v12.py` ausfuehren |
| Preis | Preis >= 0, Platform definiert | `qa_check.py` PRODUCTS-Dict anpassen |
| Health | Download-Issuer `/health` erreichbar | Service starten: `python3 tools/download-issuer/app.py` |

## Produkte (7 Produkte)

| product_id | Name | Preis | Platform |
|------------|------|-------|----------|
| `playbook01` | Local AI Stack Playbook | EUR 49 | Stripe |
| `n8n-bundle` | n8n Starter Bundle | EUR 29 | Gumroad |
| `grafana-pack` | Grafana Dashboard Pack | EUR 39 | Gumroad |
| `dsgvo-template` | DSGVO Art.30 Bundle | EUR 79 | Gumroad |
| `ai-agent-blueprint` | AI Agent Team Blueprint | EUR 19 | Gumroad |
| `homelab-mcp-bundle` | Homelab MCP Bundle | FREE | Gumroad |
| `komplett-bundle` | AI Engineering Komplett Bundle | EUR 149 | Gumroad |

## Typischer Release-Ablauf

```bash
# 1. QA pruefen
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py all

# 2. Bei Fehlern: Cover regenerieren
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py

# 3. QA nochmal -> gruen -> Release!
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py all
```

Oder alles in einem via `/release-workflow`.

## Dateipfade

| Datei | Pfad |
|-------|------|
| **Script** | `tools/qa-product-check/qa_check.py` |
| **Download-Files** | `tools/download-issuer/files/` |
| **Covers** | `products/covers/thumbnail-{id}.png` |

## Neues Produkt hinzufuegen

`PRODUCTS`-Dict in `qa_check.py` erweitern:
```python
"mein-produkt": {
    "name": "Mein Produkt Name",
    "price_eur": 29,
    "file": "mein-produkt.zip",
    "platform": "gumroad",
    "cover": "thumbnail-mein-produkt.png",
},
```

## Regeln (ABSOLUT!)

- **NIEMALS** ein Release ohne gruenen QA-Check
- **IMMER** nach Cover-Regenerierung nochmal QA laufen lassen
- **IMMER** `PRODUCTS`-Dict und `app.py PRODUCT_MAP` synchron halten
- **KEIN** manuelles "ich glaube die Datei ist da" — Script ausfuehren!

## Abhaengigkeiten

```bash
python3 >= 3.11  # stdlib only, kein pip install noetig
```

Download-Issuer muss laufen fuer Health-Check (optional, Produkt-Checks laufen immer).

## Version History

| Version | Datum | Aenderung |
|---------|-------|-----------|
| v1.0 | 2026-03-05 | Initial -- @john01 Idee, @lisa01 House Style |
