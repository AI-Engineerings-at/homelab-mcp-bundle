# Launch Checklist — ai-engineering.at

> Erstellt: 2026-02-26 | @lisa01
> Status: BEREIT ZUM ABHAKEN | Aktualisiert: 2026-02-26

## AKTUELLER STATUS

| Check | Status | Wer |
|-------|--------|-----|
| Copy Review 20/20 Seiten | ✅ DONE (Commit d8aa9a6) | @john01 |
| RSS Feed live | ✅ DONE | @john01 |
| HTTP Status Alle Seiten | ⏳ Ausstehend | @john01 |
| Lighthouse Scores | ⏳ Ausstehend | @john01 |
| OG Image Preview | ⏳ Ausstehend | @john01 |
| Broken Links Check | ⏳ Ausstehend | @john01 |

---

## PRE-LAUNCH (Vor dem Go-Live)

### QA & Testing
- [ ] Alle Seiten HTTP 200 — Kein 404, kein 500 (@john01)
- [ ] Lighthouse Score: Performance ≥80, Accessibility ≥90 (@john01)
- [ ] OG Image Preview (ai-engineering.at/eagle-logo.png) — Twitter Card + LinkedIn richtig (@john01)
- [ ] Broken Links prüfen (alle internen + externen Links) (@john01)
- [ ] Mobile Responsive Check (iOS Safari, Android Chrome) (@john01)
- [ ] Newsletter-Signup funktioniert (DOI-Mail ankommt, Eintrag in Rapidmail Liste 1655) (@john01)
- [ ] Stripe Checkout komplett — Payment, Danke-Seite, Delivery (@john01)
- [ ] Alle Produktseiten: Preise korrekt, Features korrekt (@jim)

### Content & Copy
- [x] Copy Review 20/20 Seiten — DONE (Commit d8aa9a6)
- [x] RSS Feed live
- [ ] /impressum — Deutsche Pflichtangaben vollständig
- [ ] /datenschutz — DSGVO-konform, alle Datenverarbeitungen dokumentiert
- [ ] /agb — Aktuelle Preise + Produkte referenziert
- [ ] Blog-Artikel mind. 1 veröffentlicht (ai-engineering.at/blog/...)

### Infrastruktur
- [x] Vercel Deployment live
- [x] Rapidmail ENV Vars gesetzt (User, Password, List-ID 1655)
- [ ] Custom Domain (ai-engineering.at) → SSL-Zertifikat gültig
- [ ] n8n DOI-Confirm Workflow aktiv (n8n_rapidmail_doi_confirm.json)
- [ ] n8n Stripe Delivery Workflow aktiv
- [ ] Gumroad-Links in Produktseiten korrekt
- [ ] GitHub Repo public (homelab-mcp-bundle) — README vollständig

### Social Media vorbereiten
- [ ] Twitter/X Account eingeloggt, Thread-Drafts gespeichert
- [ ] LinkedIn Account eingeloggt, Post-Draft bereit
- [ ] HN-Draft final (hn-draft.md — korrekte URLs)
- [ ] Dev.to Account verifiziert, Artikel als Draft gespeichert
- [ ] Reddit-Account Karma ausreichend (r/selfhosted, r/homelab)
- [ ] Product Hunt: Draft erstellt, "upcoming" aktiviert (PRODUCT_HUNT_DRAFT.md)

---

## LAUNCH DAY

### Posting-Reihenfolge (empfohlen)

| Zeit | Platform | Aktion |
|------|----------|--------|
| 00:01 PST | Product Hunt | Launch live stellen (Di/Mi empfohlen), Maker Comment posten |
| 08:00 UTC | Hacker News | Show HN Post live stellen |
| 08:15 UTC | Twitter/X | Thread Option A posten |
| 08:30 UTC | LinkedIn | Launch Post posten |
| 09:00 UTC | Dev.to | Artikel veröffentlichen |
| 10:00 UTC | Reddit r/selfhosted | Post mit Link zu HN |
| 10:15 UTC | Reddit r/homelab | Post (andere Perspektive, kein Repost) |
| 12:00 UTC | Reddit r/LocalLLaMA | Falls HN gut läuft |

### Content zum Posten

**Twitter/X — Thread Option A** (marketing/twitter-thread.md)
```
Was wäre, wenn dein KI-Team 24/7 für dich arbeitet...
→ https://ai-engineering.at
```

**LinkedIn** (automation/n8n_linkedin_post.json als Vorlage)
- Professionellerer Ton, Fokus auf Business-Value
- Link: https://ai-engineering.at

**HN** (marketing/hn-draft.md)
```
Show HN: I built a 4-agent Claude Code team on self-hosted infra (GDPR, €0/month)
```

**Dev.to** (marketing/devto-article.md)
- Tags: ai, automation, selfhosted, claudecode
- Cover: eagle-logo.png

**Reddit r/selfhosted**
```
Title: I've been running a 4-agent AI team on my homelab for 3 months — here's what I learned
→ Link zu HN Post ODER direkt zu ai-engineering.at
```

### Monitoring am Launch Day
- [ ] Analytics-Dashboard (Vercel/Plausible) offen halten
- [ ] HN Comments beobachten — innerhalb 30min antworten!
- [ ] Twitter Notifications an — auf Kommentare reagieren
- [ ] n8n Newsletter-Signup Workflow läuft — neue Subscriber prüfen
- [ ] Stripe: Erste Verkäufe prüfen

---

## POST-LAUNCH (Erste 7 Tage)

### Woche 1 — Monitoring

| Tag | Aufgabe |
|-----|---------|
| Tag 1 | HN/Reddit Comments beantworten, Twitter Engagement messen |
| Tag 2 | Email Sequence aktiv? (Email-01-Welcome wird gesendet) |
| Tag 3 | Analytics auswerten: Traffic-Quellen, Conversion |
| Tag 5 | Email-02 versendet? (MCP Use Cases) |
| Tag 7 | Email-03 versendet? (Playbook Offer) — Erste Verkäufe analysieren |

### Analytics-Ziele (Woche 1)

| Metrik | Ziel |
|--------|------|
| Unique Visitors | ≥500 |
| Newsletter Signups | ≥50 |
| Stripe Sales | ≥5 |
| HN Upvotes | ≥50 |
| Dev.to Reactions | ≥20 |

### Ongoing
- [ ] Blog: 1 Artikel/Woche (Content-Kalender aufbauen)
- [ ] Twitter: 3x/Woche Tweets (Standalone Tweets aus twitter-thread.md)
- [ ] Newsletter: Wöchentlicher Roundup an alle Subscriber
- [ ] Reddit: Community-Mitglied sein, nicht nur promoten
- [ ] GitHub: Issues beantworten, homelab-mcp-bundle weiterentwickeln

### Email Sequence (automation/email_7day_sequence.md)
- [x] Email 01: Welcome (Tag 0 — sofort nach Signup)
- [x] Email 02: MCP Use Cases (Tag 2)
- [x] Email 03: Playbook Offer mit Discount (Tag 5)
- [ ] Email 04–07: Noch zu entwickeln (@lisa01)

---

## QUICK-REFERENCE LINKS

| Resource | URL |
|----------|-----|
| Website | https://ai-engineering.at |
| GitHub | https://github.com/AI-Engineerings-at/homelab-mcp-bundle |
| n8n | http://10.40.10.80:5678 |
| Vercel Dashboard | https://vercel.com/dashboard |
| Rapidmail | https://www.rapidmail.de |
| Stripe Dashboard | https://dashboard.stripe.com |
| Gumroad | https://app.gumroad.com |

---

*Checklist Owner: @jim | Erstellt von @lisa01 | Stand: 2026-02-26*
