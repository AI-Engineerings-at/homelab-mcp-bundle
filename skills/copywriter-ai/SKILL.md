# Skill: copywriter-ai (v1.0)

> **@john01-Idee**: Produkt-Texte in DE+EN generieren ohne jedes Mal von Null anfangen.
> Ollama laeuft lokal -- kein externes API, kein Datenschutz-Problem.

## Zweck
KI-generierte Produkt-Texte (Gumroad-Listings, Landing Page Copy, E-Mail) in Deutsch und Englisch.
Nutzt lokales Ollama auf .99 -- schnell, datenschutzkonform, kostenlos.

## Usage

```bash
# Vollstaendige Copy DE+EN (Standard)
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py n8n-bundle

# Nur Deutsch
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py n8n-bundle --lang de

# Nur Englisch
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py dsgvo-template --lang en

# Fuer Gumroad-Listing (Standard)
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py playbook01 --platform gumroad

# Alle Produkte anzeigen
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py
```

## Parameter

| Parameter | Optionen | Default |
|-----------|----------|---------|
| `product_id` | s. Produktliste | Pflicht |
| `--platform` | `gumroad`, `stripe`, `landing`, `email` | `gumroad` |
| `--lang` | `de`, `en`, `both` | `both` |

## Produkte (7 Produkte)

| product_id | Name | Preis |
|------------|------|-------|
| `playbook01` | Local AI Stack Playbook | EUR 49 |
| `n8n-bundle` | n8n Starter Bundle | EUR 29 |
| `grafana-pack` | Grafana Dashboard Pack | EUR 39 |
| `dsgvo-template` | DSGVO Art.30 Bundle | EUR 79 |
| `ai-agent-blueprint` | AI Agent Team Blueprint | EUR 19 |
| `homelab-mcp-bundle` | Homelab MCP Bundle | FREE |
| `komplett-bundle` | AI Engineering Komplett Bundle | EUR 149 |

## Output

**Standard**: `products/copy/<product_id>-<timestamp>.md`

Format pro Datei:
```
# Produktname -- Copy [PLATFORM]
> Generiert: 2026-03-05T14:23:00

## DE
[Deutsches Gumroad-Listing]

## EN
[English Gumroad Listing]
```

## Technischer Stack

- **Ollama**: `llama3.2:3b` auf .99 (RTX 2060) — Default
- **Fallback**: `.80` CPU Ollama wenn .99 nicht erreichbar
- **Prompt-Typ**: Strukturiertes Gumroad-Listing-Format
- **Timeout**: 120s pro Anfrage

## Umgebungsvariablen

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `OLLAMA_URL` | `http://10.40.10.99:11434` | Ollama Endpunkt |
| `OLLAMA_MODEL` | `llama3.2:3b` | Modell |

## Dateipfade

| Datei | Pfad |
|-------|------|
| **Script** | `tools/copywriter-ai/copywriter.py` |
| **Output** | `products/copy/<id>-<ts>.md` |

## Neues Produkt hinzufuegen

`PRODUCTS`-Dict in `copywriter.py` erweitern:
```python
"mein-produkt": {
    "name": "Mein Produkt",
    "tagline": "Kurze praegnante Beschreibung",
    "price": "EUR 29",
    "platform": "gumroad",
    "features": ["Feature 1", "Feature 2", "Feature 3"],
    "category": "Kategorie / Subkategorie",
    "audience": "Zielgruppe beschreiben",
},
```

## Regeln (ABSOLUT!)

- **NIEMALS** generierten Text ohne Gegenlesen verwenden -- immer reviewen
- **IMMER** DE+EN generieren fuer Gumroad (internationale Kaeufer!)
- **KEIN** Hardcoding von Produktdaten -- PRODUCTS-Dict ist die einzige Quelle
- Output-Dateien committen: `git add products/copy/` nach Review

## Abhaengigkeiten

```bash
python3 >= 3.11  # stdlib only
# Ollama muss laufen: curl http://10.40.10.99:11434/api/tags
```

## Version History

| Version | Datum | Aenderung |
|---------|-------|-----------|
| v1.0 | 2026-03-05 | Initial -- @john01 Idee (lokale KI), @lisa01 House Style |
