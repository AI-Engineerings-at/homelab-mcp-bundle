# Affiliate / Referral Programm Konzept
## AI-Engineering.at — Gumroad Built-in

**Stand**: 2026-02-25
**Verantwortlich**: @lisa01

---

## Gumroad Affiliate System (Built-in, kostenlos)

### Wie es funktioniert
Gumroad hat ein natives Affiliate-System — kein Extra-Tool nötig:

1. **Affiliate anlegen**: Gumroad Dashboard → Affiliates → Add Affiliate
2. **Eindeutiger Link**: `https://aiengineering.gumroad.com/l/PRODUKT?a=AFFILIATE_CODE`
3. **Tracking**: Automatisch via Cookie (30 Tage)
4. **Auszahlung**: Gumroad zahlt direkt an Affiliate (PayPal/Stripe)

### Konditionen (Empfehlung)

| Produkt | Preis | Provision | Affiliate verdient |
|---------|-------|-----------|-------------------|
| n8n Starter Bundle | €29 | 30% | ~€8,70 |
| Grafana Dashboard Pack | €19 | 30% | ~€5,70 |
| AI Agent Team Blueprint | €49 | 30% | ~€14,70 |
| Bundle Deal (alle 3) | €79 | 25% | ~€19,75 |

**30% ist Industrie-Standard für digitale Produkte** (Vergleich: Gumroad selbst empfiehlt 20-40%)

---

## Zielgruppe für Affiliates

### Tier 1 — Tech-Content-Creator
- YouTube-Kanäle: Self-Hosting, Homelab, Docker
- Blogs: dev.to, medium.com Technik-Autoren
- Newsletter: Technik-fokussiert (5k+ Abonnenten)

### Tier 2 — Community Leaders
- Discord/Slack Server-Admins (Homelab, n8n, AI)
- Reddit-Moderatoren (r/selfhosted, r/homelab)
- GitHub-Stars mit relevantem Audience

### Tier 3 — B2B / Freelancer
- DevOps/SRE Freelancer (empfehlen an Kunden)
- IT-Consultants
- Studenten/Bootcamp-Alumni

---

## Launch-Strategie

### Phase 1: Seed Affiliates (Woche 1-2)
- 5-10 handverlesene Affiliates persönlich ansprechen
- Kostenloser Produktzugang als Incentive
- Onboarding: kurze Loom-Video-Erklärung

### Phase 2: Open Program (Woche 3+)
- Landing Page: "Werde Affiliate" auf ai-engineering.at
- Automatische Genehmigung (kein manuelles Review nötig)
- Affiliate-Kit: Banner, Texte, Screenshots

### Affiliate-Kit Inhalt
```
/affiliate-kit/
  ├── banners/          # 728x90, 300x250, 160x600
  ├── social-images/    # 1200x630 für LinkedIn/Twitter
  ├── email-template/   # Fertige Email-Vorlage
  ├── review-text.md    # Vorgeschlagener Beschreibungstext
  └── FAQ.md            # Häufige Fragen
```

---

## Gumroad Setup (Schritt für Schritt)

```
1. gumroad.com → Dashboard → Settings → Affiliates
2. "Enable Affiliates" aktivieren
3. Standard-Commission setzen: 30%
4. Affiliate-Anmeldelink generieren
5. Link auf Landing Page einbinden
```

**Wichtig**: Gumroad zahlt Affiliates automatisch am Monatsende.
Keine manuelle Arbeit nach dem Setup!

---

## KPIs für Affiliate-Programm

| Metrik | Ziel (Monat 1) | Ziel (Monat 3) |
|--------|---------------|---------------|
| Aktive Affiliates | 5 | 20 |
| Affiliate-Verkäufe | 3 | 15 |
| Affiliate-Revenue-Anteil | 10% | 25% |
| Top Affiliate Earnings | €50 | €200 |

---

## Rechtliches (DSGVO)

- Gumroad verarbeitet Affiliate-Daten (eigene AGB)
- Wir müssen Affiliates in Datenschutzerklärung erwähnen
- Cookie-Hinweis für Tracking-Link (30 Tage) nötig
- Affiliate-Einnahmen: Affiliates melden selbst beim Finanzamt

---

## Nächste Schritte

- [ ] @joe: Gumroad Affiliates aktivieren (5 Min.)
- [ ] @lisa01: Affiliate-Kit erstellen (Banner, Texte)
- [ ] @jim01: Landing Page "Affiliate werden" Sektion
- [ ] Team: 5 Seed-Affiliates identifizieren und ansprechen
