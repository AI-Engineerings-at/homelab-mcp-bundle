# AI Engineering — Skills Index

> Repository: cli_bridge | Letztes Update: 2026-03-05
> Alle Skills fuer Content-Erstellung, Brand, Marketing und Social Media

## Skills Übersicht

| Skill | Version | Zweck | Script |
|-------|---------|-------|--------|
| [cover-generator](#cover-generator) | v5 | Produkt-Cover 800x800 PNG | `tools/cover-generator/gen_covers_v5.py` |
| [gemini-brand-gen](#gemini-brand-gen) | v1 | Universal Brand Asset Generator | `tools/gemini-brand-gen/brand_gen.py` |
| [brand-media-gen](#brand-media-gen) | v1 | Marketing-Medien (9 Formate) | `~/.claude/skills/brand-media-gen.sh` |
| [postiz](#postiz) | v1 | Social Media Posting (28+ Plattformen) | `postiz` CLI |

---

## cover-generator

**Produkt-Cover 800x800 PNG via Playwright + Google Fonts**

- Layout: Text links + Produkt-Thumbnail rechts (floating 3D Card)
- 7 Produkte vorkonfiguriert
- Renderer: Playwright Chromium Headless

```bash
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py        # alle
python3 ~/cli_bridge/tools/cover-generator/gen_covers_v5.py n8n-starter-bundle  # einzeln
./skills/cover-generator/cover-generator.sh --all                   # Shell wrapper
```

Doku: `skills/cover-generator/SKILL.md`

---

## gemini-brand-gen

**Universal Brand Asset Generator — 8 Formate, Gemini API + Playwright**

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

**Social Media Automation CLI — 28+ Plattformen**

- Plattformen: Twitter/X, LinkedIn, Instagram, TikTok, YouTube, Reddit, Facebook, und mehr
- Features: Scheduling, Threads, Media Upload, Analytics

```bash
postiz integrations:list
postiz posts:create -c "Content" -s "2026-03-10T10:00:00Z" -i "<integration-id>"
postiz upload image.jpg
```

Doku: `skills/postiz/SKILL.md`

---

## Format-Matrix (alle Skills)

| Format | Größe | cover-gen v5 | gemini-brand | brand-media |
|--------|-------|:---:|:---:|:---:|
| Gumroad Cover | 800x800 | ✅ | ✅ | ✅ |
| YouTube Thumb | 1280x720 | — | ✅ | ✅ |
| Facebook/OG | 1200x628 | — | ✅ | ✅ |
| Instagram Post | 1080x1080 | — | ✅ | ✅ |
| Twitter/X | 1200x675 | — | ✅ | ✅ |
| Blog Header | 1600x900 | — | — | ✅ |
| LinkedIn Post | 1200x627 | — | ✅ | ✅ |
| IG Story | 1080x1920 | — | ✅ | ✅ |
| LinkedIn Banner | 1584x396 | — | ✅ | — |
| Facebook Banner | 820x312 | — | ✅ | ✅ |

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
