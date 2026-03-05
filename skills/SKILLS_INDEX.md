# AI Engineering -- Skills Index

> Repository: cli_bridge | Letztes Update: 2026-03-05
> Alle Skills fuer Content, Brand, Marketing, QA und Release-Management

## Skills Uebersicht

| Skill | Version | Zweck | Autor-Idee |
|-------|---------|-------|------------|
| [cover-generator](#cover-generator) | v12 | Produkt-Cover 800x800 PNG | @lisa01 |
| [gemini-brand-gen](#gemini-brand-gen) | v1 | Universal Brand Asset Generator | @lisa01 |
| [brand-media-gen](#brand-media-gen) | v1 | Marketing-Medien (9 Formate) | @lisa01 |
| [postiz](#postiz) | v1 | Social Media Posting (28+ Plattformen) | @lisa01 |
| [qa-product-check](#qa-product-check) | v1 | Release-QA: Dateien, Cover, Preise | @john01 |
| [copywriter-ai](#copywriter-ai) | v1 | KI-Produkt-Texte DE+EN via Ollama | @john01 |
| [release-workflow](#release-workflow) | v1 | One-Command Release-Pipeline | @john01 |

---

## cover-generator

**Produkt-Cover 800x800 PNG via Playwright + Google Fonts**

- Layout v12: Screenshot-Slot oben + Content-Bereich + Brand-Strip unten
- 7 Produkte vorkonfiguriert, Eagle Watermark @38% opacity
- Renderer: Playwright Chromium Headless

```bash
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py        # alle
python3 ~/cli_bridge/tools/cover-generator/gen_thumbnails_v12.py n8n-starter-bundle  # einzeln
./skills/cover-generator/cover-generator.sh --all                        # Shell wrapper
```

Doku: `skills/cover-generator/SKILL.md`

---

## gemini-brand-gen

**Universal Brand Asset Generator -- 8 Formate, Gemini API + Playwright**

- Formate: cover, ig-post, fb-post, twitter-post, yt-thumb, ig-story, fb-banner, li-banner
- Gemini API generiert SVG-Illustrationen
- Custom Brand Kit via JSON
- Fallback ohne API (--no-gemini)

```bash
python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --title "Mein Produkt" --format cover --type cover \
  --features "Feature 1" "Feature 2" --price "EUR 49"

python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py \
  --prompt "Instagram post fuer n8n Kurs" --format ig-post

python3 ~/cli_bridge/tools/gemini-brand-gen/brand_gen.py --list-formats
```

Doku: `skills/gemini-brand-gen/SKILL.md`

---

## brand-media-gen

**Multi-Format Marketing Media Generator (9 Formate, alle Produkte)**

- Formate: gumroad-thumbnail, fb-banner, og-image, instagram, twitter, blog-header, linkedin, story
- Basiert auf Playbook01 BrandKit (Primary: #4263FF, Secondary: #9A25EA)

```bash
~/.claude/skills/brand-media-gen.sh                 # alles
~/.claude/skills/brand-media-gen.sh fb-banner       # nur FB Banner
~/.claude/skills/brand-media-gen.sh instagram-post n8n-starter-bundle  # spezifisch
```

Doku: `skills/brand-media-gen/SKILL.md`

---

## postiz

**Social Media Automation CLI -- 28+ Plattformen**

- Plattformen: Twitter/X, LinkedIn, Instagram, TikTok, YouTube, Reddit, Facebook, und mehr
- Features: Scheduling, Threads, Media Upload, Analytics

```bash
postiz integrations:list
postiz posts:create -c "Content" -s "2026-03-10T10:00:00Z" -i "<integration-id>"
postiz upload image.jpg
```

Doku: `skills/postiz/SKILL.md`

---

## qa-product-check

**@john01-Idee: Automatischer Release-QA fuer alle Produkte**

- Prueft: Download-Datei vorhanden, Cover generiert, Preis korrekt, Service erreichbar
- Exit 0 = release-ready | Exit 1 = Fehler gefunden
- Stoppt Release-Workflow bei Fehler (hartcodiert als Gate)

```bash
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py          # alle 7 Produkte
python3 ~/cli_bridge/tools/qa-product-check/qa_check.py n8n-bundle  # einzeln
```

Doku: `skills/qa-product-check/SKILL.md`

---

## copywriter-ai

**@john01-Idee: Lokale KI schreibt Produkt-Texte in DE+EN**

- Gumroad-Listings, Landing Page Copy, E-Mail-Texte
- Ollama lokal auf .99 (RTX 2060) -- kein externes API
- Strukturiertes Output-Format, direkt commitbar

```bash
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py n8n-bundle          # DE+EN
python3 ~/cli_bridge/tools/copywriter-ai/copywriter.py playbook01 --lang de  # nur DE
```

Doku: `skills/copywriter-ai/SKILL.md`

---

## release-workflow

**@john01-Idee: Ein Befehl -- vollstaendiger Release-Ablauf**

- QA -> Cover -> Copy -> (optional) Social Media
- Stoppt bei QA-Fehler, setzt durch bei Warnungen
- Integriert alle 3 john01-Skills + cover-generator v12

```bash
./tools/release-workflow/release.sh n8n-bundle          # Standard Release
./tools/release-workflow/release.sh all --skip-copy     # Alle, ohne Copy
./tools/release-workflow/release.sh n8n-bundle --skip-social  # Mit Social Planung
```

Doku: `skills/release-workflow/SKILL.md`

---

## Format-Matrix (Visual Assets)

| Format | Groesse | cover-gen v12 | gemini-brand | brand-media |
|--------|---------|:---:|:---:|:---:|
| Gumroad Cover | 800x800 | OK | OK | OK |
| YouTube Thumb | 1280x720 | -- | OK | OK |
| Facebook/OG | 1200x628 | -- | OK | OK |
| Instagram Post | 1080x1080 | -- | OK | OK |
| Twitter/X | 1200x675 | -- | OK | OK |
| Blog Header | 1600x900 | -- | -- | OK |
| LinkedIn Post | 1200x627 | -- | OK | OK |
| IG Story | 1080x1920 | -- | OK | OK |
| LinkedIn Banner | 1584x396 | -- | OK | -- |
| Facebook Banner | 820x312 | -- | OK | OK |

---

## BrandKit (AI Engineering)

> Referenz: `Playbook01/media/assets/BrandKit.png`

| Token | Wert |
|-------|------|
| Primary | `#4263FF` (Blue) |
| Secondary | `#9A25EA` (Purple) |
| Background | Dark Navy (sehr dunkel, fast schwarz) |
| Font Primary | Montserrat |
| Logo | Eagle (weiss auf dunkel) |

---

## Lisa01 House Style -- Skill-Regeln

> Alle neuen Skills MUESSEN diesem Format folgen!

### SKILL.md Pflichtstruktur

```
# Skill: <name> (v<major>.<minor>)
> Ideen-Herkunft + 1-Satz Kerngedanke

## Zweck          -- 2-3 Saetze, kein Bullshit
## Usage          -- Bash-Codeblocks mit Kommentaren
## [Optionen|Formate|Produkte] -- Tabelle(n)
## Output         -- Was kommt raus, wo landet es
## Dateipfade     -- Tabelle mit allen relevanten Pfaden
## Neues X hinzufuegen -- Erweiterungsanleitung
## Regeln (ABSOLUT!) -- Was NIEMALS passieren darf
## Abhaengigkeiten -- pip/brew/etc
## Version History -- Tabelle
```

### Konventionen

- **Sprache**: Doku auf Deutsch, Code/Commits auf Englisch
- **Ton**: Direkt, technisch, kein Marketing-Speak
- **Tabellen**: Fuer ALLE Optionen/Formate/Produkte (nie Freitext-Listen)
- **Regeln**: IMMER in "Regeln (ABSOLUT!)" Sektion, mit Grossbuchstaben "NIEMALS"/"IMMER"
- **Ideen-Credit**: "@john01-Idee" / "@lisa01 House Style" in der Intro-Blockquote
- **Version History**: Chronologisch, neueste oben
