# Skill: brand-media-gen

## Zweck
Generiert alle Marketing-Medien für AI Engineering Produkte.
Unterstützt 9+ Formate für Gumroad, Social Media, Blog, und mehr.

## Usage

```bash
# Alle Formate, alle Produkte
~/.claude/skills/brand-media-gen.sh

# Nur bestimmtes Format
~/.claude/skills/brand-media-gen.sh gumroad-thumbnail
~/.claude/skills/brand-media-gen.sh fb-banner all

# Einzelnes Produkt
~/.claude/skills/brand-media-gen.sh instagram-post n8n-starter-bundle

# Liste
~/.claude/skills/brand-media-gen.sh list
```

## Formate

| Format | Größe | Verwendung |
|--------|-------|------------|
| gumroad-thumbnail | 800x800 | Gumroad Produkt-Thumbnail |
| gumroad-cover | 1280x720 | Gumroad Seiten-Header |
| fb-banner | 1200x628 | Facebook / Meta Banner |
| og-image | 1200x630 | Open Graph (Website, Blog) |
| instagram-post | 1080x1080 | Instagram Feed |
| twitter-card | 1200x675 | Twitter/X Post |
| blog-header | 1600x900 | Blog Artikel Header |
| linkedin-post | 1200x627 | LinkedIn Post |
| story | 1080x1920 | Instagram/TikTok Story |

## Produkte

| ID | Name |
|----|------|
| n8n-starter-bundle | n8n Starter Bundle |
| ai-agent-blueprint | AI Agent Team Blueprint |
| grafana-dashboard-pack | Grafana Dashboard Pack |
| dsgvo-compliance-bundle | DSGVO Art.30 Bundle |
| lokaler-ai-stack-playbook | Local AI Stack Playbook |

## Design-System (BrandKit)

- Background: Dark Navy #0B0C0F + Gradient
- Primary Color: #4263FF (Blue)
- Secondary Color: #9A25EA (Purple)
- Eagle-Logo: Watermark, 40% opacity
- Font: Montserrat 900 weight fuer Titel
- BrandKit Referenz: Playbook01/media/assets/BrandKit.png

## Output

Standard: Playbook01/branding/output/<product>-<format>.png
