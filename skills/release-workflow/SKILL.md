# Skill: release-workflow (v1.0)

> **@john01-Idee**: Ein einziger Befehl der alles macht -- QA, Covers, Copy, Git.
> Kein "hab ich die Cover schon regeneriert?", kein "wo ist die Datei?"-Chaos mehr.

## Zweck
Vollstaendiger Release-Ablauf in einem Kommando:
QA-Check -> Cover generieren -> Copy generieren -> (optional) Social Media.
Stoppt bei QA-Fehler -- kein Release ohne gruenem QA.

## Usage

```bash
# Ein Produkt voll releasen (inkl. Copy-Generierung)
./tools/release-workflow/release.sh n8n-bundle

# Alle 7 Produkte (dauert laenger)
./tools/release-workflow/release.sh all

# Ohne Copy-Generierung (schnell, nur QA + Covers)
./tools/release-workflow/release.sh n8n-bundle --skip-copy

# Mit Social Media Planung (Postiz muss konfiguriert sein)
./tools/release-workflow/release.sh n8n-bundle --skip-social
```

## Pipeline-Steps

| Step | Was passiert | Bei Fehler |
|------|-------------|------------|
| 1. QA Check | `qa_check.py` -- alle Dateien und Cover | **Stopp!** Kein Release |
| 2. Covers | `gen_thumbnails_v12.py` -- 800x800 PNG | Warnung, weiter |
| 3. Copy | `copywriter.py` -- DE+EN Listing-Text | Warnung, weiter (opt-out: `--skip-copy`) |
| 4. Social | Postiz Planung anzeigen | Standard OFF (opt-in: `--skip-social` invertiert) |

## Parameter

| Parameter | Beschreibung |
|-----------|-------------|
| `[product_id\|all]` | Produkt-ID oder `all` fuer alle 7 |
| `--skip-copy` | Copy-Generierung ueberspringen |
| `--skip-social` | Social-Media-Schritt aktivieren (Flag-Name invertiert!) |

## Naechste Schritte nach dem Workflow

```bash
# Review der generierten Dateien
ls products/covers/
ls products/copy/

# Commits
git add products/covers/ products/copy/
git commit -m "chore: release n8n-bundle 2026-03-05"
git push

# Gumroad Upload (via @jim02 -- Browser-Task!)
# Stripe Update (via Stripe Dashboard oder @jim02)
```

## Integrierte Skills

Dieser Skill orchestriert:
- `/qa-product-check` -- Vollstaendiger Produkt-QA
- `/cover-generator` (v12) -- Produkt-Thumbnails
- `/copywriter-ai` -- DE+EN Gumroad-Copy
- `/postiz` -- Social Media (optional)

## Dateipfade

| Datei | Pfad |
|-------|------|
| **Script** | `tools/release-workflow/release.sh` |
| **QA** | `tools/qa-product-check/qa_check.py` |
| **Covers** | `tools/cover-generator/gen_thumbnails_v12.py` |
| **Copy** | `tools/copywriter-ai/copywriter.py` |

## Regeln (ABSOLUT!)

- **NIEMALS** Step 1 (QA) ueberspringen -- kein Release ohne gruenem QA
- **NIEMALS** `--force` Flag hinzufuegen um QA zu umgehen
- **IMMER** generierten Content reviewen BEVOR er auf Gumroad/Stripe geht
- **NUR** `@jim02` macht den Browser-Upload -- @lisa01 und andere nicht!

## Abhaengigkeiten

```bash
bash >= 5.0
python3 >= 3.11
playwright  # fuer Cover-Generator
# Alle Sub-Scripts muessen verfuegbar sein (s.o.)
```

## Version History

| Version | Datum | Aenderung |
|---------|-------|-----------|
| v1.0 | 2026-03-05 | Initial -- @john01 Idee (One-Command-Release), @lisa01 House Style |
