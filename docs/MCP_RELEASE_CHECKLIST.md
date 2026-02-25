# MCP Bundle — Release Checklist v1

> **Status**: Pre-Launch | **Ziel**: 6-Server Bundle als erstes Produkt
> **Strategie**: 6 Server = v1 fertig. AdGuard, Grafana, Neo4j = v2 Upsell.

---

## Produkt-Scope v1 (FINAL)

| # | MCP Server | Status |
|---|-----------|--------|
| 1 | Mattermost MCP | ✅ fertig |
| 2 | n8n MCP | ✅ fertig |
| 3 | Ollama MCP | ✅ fertig |
| 4 | Proxmox MCP | ✅ fertig |
| 5 | Uptime Kuma MCP | ✅ fertig |
| 6 | Portainer MCP | ✅ fertig |

**v2 Upsell (later):** AdGuard, Grafana, Neo4j

---

## Checklist

### GitHub / Deliverable
- [ ] Entscheidung: **GitHub public** oder **privat + Gumroad ZIP als Deliverable**?
  - Option A: Public Repo → Community Contribution, kostenloser Traffic, aber frei kopierbar
  - Option B: Privat + Gumroad ZIP → vollständige Kontrolle, Käufer kriegen Zugang per Link
  - Option C: Public README + privates Zip mit Doku/Extras (Hybrid)
- [ ] Repo struktur prüfen: README, LICENSE, INSTALL Guide vorhanden?
- [ ] Sensible Daten / Credentials aus allen Dateien entfernt?

### Website / Landing Page
- [ ] `/skills` Seite: **6 Beta Cards** (Portainer-Card fehlt noch!)
  - Portainer MCP Card hinzufügen (analog zu den anderen 5)
- [ ] Hero Section: "6 MCP Server" statt "5"
- [ ] Preise / CTA auf der Skills-Seite aktualisieren

### Gumroad
- [ ] Gumroad Listing erstellen / hochladen
  - Texte: `products/GUMROAD_MCP_LISTING.md` (ready)
  - Preis festlegen (Early Bird?)
  - ZIP / Deliverable hochladen
  - Thumbnail / Cover hochladen
- [ ] Delivery-URL oder Download-Datei konfiguriert?
- [ ] Test-Purchase durchführen (eigener Account)

### Payment
- [ ] **Stripe Payment Link** für MCP Bundle erstellen → **@joe (Action required)**
  - Alternativ: Gumroad als einziger Checkout
  - Entscheidung: Gumroad only vs. Gumroad + Stripe?

### Social Media
- [ ] **Twitter/X Thread** posten (`marketing/twitter-thread.md` ready)
- [ ] **HN (Hacker News)** Post (`marketing/hn-draft.md` ready)
- [ ] LinkedIn Post (falls vorhanden)
- [ ] Reddit r/selfhosted / r/homelab Post

### MCP Directories
- [ ] **MCP.so** Listing einreichen
- [ ] **Glama.ai** Listing einreichen
- [ ] **PulseMCP** Listing einreichen
- [ ] Screenshots / Demo GIFs für Listings vorbereiten?

### Product Hunt
- [ ] **Product Hunt Listing** vorbereiten
  - Tagline, Description, Gallery (Screenshots)
  - Launch-Tag festlegen (Dienstag–Donnerstag = beste Tage)
  - Hunter finden (oder self-hunt)

### Newsletter
- [ ] **Newsletter Announcement** verfassen
  - Betreff, Body, CTA
  - Liste: bestehende Subscribers + neue Leads aus Lead-Magnet
  - Versand-Datum festlegen

---

## Launch-Reihenfolge (empfohlen)

```
1. GitHub + Gumroad fertigstellen (Deliverable muss stehen)
2. /skills Seite fixen (Portainer Card + "6 Server")
3. Gumroad Test-Purchase
4. Stripe Link (@joe)
5. Social Posts: Twitter → Reddit → HN
6. MCP Directories: MCP.so + Glama + PulseMCP
7. Newsletter raus
8. Product Hunt (separate Kampagne, eigener Tag)
```

---

## Offene Entscheidungen (@joe / @jim)

| # | Frage | Wer entscheidet |
|---|-------|----------------|
| 1 | GitHub public oder privat? | @joe |
| 2 | Stripe Link erstellen? | @joe (Action) |
| 3 | Preis / Early Bird Discount? | @joe |
| 4 | Product Hunt Launch-Datum? | @joe / @jim |

---

*Erstellt: 2026-02-25 | v1 — 6 Server, Fokus auf Launch*
