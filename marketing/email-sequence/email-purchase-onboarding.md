# Customer Onboarding Email — Nach dem Kauf

**Subject**: Dein Download ist bereit + Erste Schritte 🎉
**From**: AI Engineering <hello@ai-engineering.at>
**Trigger**: Sofort nach Gumroad-Kauf (Webhook → n8n → Rapidmail)
**Segment**: Käufer (alle Produkte)

---

Hey {{ customer.first_name | default: "du" }},

vielen Dank für deinen Kauf! 🙌

Hier ist dein Download-Link:

---

**[→ {{ product.name }} herunterladen]({{ download_url }})**

*(Link ist 30 Tage gültig — speichere dir die Datei am besten gleich lokal)*

---

## Erste Schritte in 10 Minuten

{% if product.id == "n8n-starter-bundle" %}

**n8n Starter Bundle — Quick Start:**

1. **n8n installieren** (falls noch nicht): `docker run -p 5678:5678 n8nio/n8n`
2. **Workflow importieren**: n8n öffnen → Import → JSON-Datei auswählen
3. **Credentials einrichten**: Settings → Credentials → Stripe/Webhook konfigurieren
4. **Webhook aktivieren**: Im Workflow auf "Active" schalten
5. **Test-Trigger**: Im Workflow auf "Execute" klicken

📄 Detaillierte Anleitung: Liegt als `README.md` im ZIP-Archiv

{% elsif product.id == "grafana-dashboard-pack" %}

**Grafana Dashboard Pack — Quick Start:**

1. **Grafana öffnen** und zu Dashboards navigieren
2. **Import**: Dashboards → New → Import → JSON hochladen
3. **Datasource verknüpfen**: Prometheus-URL eingeben (Standard: `localhost:9090`)
4. **Fertig!** Dashboard ist sofort aktiv

📄 Schritt-für-Schritt: Siehe `INSTALL_GUIDE.md` im Download

{% elsif product.id == "ai-agent-team-blueprint" %}

**AI Agent Team Blueprint — Quick Start:**

1. **Blueprint lesen**: Fange mit `01_OVERVIEW.md` an (5 Min.)
2. **Stack wählen**: Docker Swarm (empfohlen) oder Kubernetes
3. **Agents deployen**: Folge der Reihenfolge in `DEPLOY_ORDER.md`
4. **Mattermost verbinden**: Webhook-URL in Agent-Config eintragen

📄 Vollständige Dokumentation: Im `docs/` Ordner im Download

{% else %}

**Quick Start:**

1. ZIP-Datei entpacken
2. `README.md` öffnen und Anleitung folgen
3. Bei Fragen: hello@ai-engineering.at

{% endif %}

---

## Du brauchst Hilfe?

- **Fragen zum Produkt**: Antworte einfach auf diese Mail
- **Community**: [GitHub Issues](https://github.com/AI-Engineerings-at) für technische Probleme
- **Schnelle Antworten**: Schreibe mir auf Twitter/X [@ai_engineering_at](https://x.com)

---

## Nächste Schritte (optional)

Wenn dir das Produkt gefällt:

⭐ **Hinterlasse eine Bewertung** auf Gumroad — hilft anderen Käufern enorm
🔗 **Teile deinen Setup** auf LinkedIn/Twitter mit `#AIEngineering`
📬 **Bleib informiert**: Du bist jetzt automatisch auf der Kundenliste für Updates

---

Danke nochmal für dein Vertrauen!

Joe
AI-Engineering.at

---

*Kaufbestätigung: {{ order.id }} | Produkt: {{ product.name }}*
*[Datenschutz](https://www.ai-engineering.at/datenschutz) | [Support](mailto:hello@ai-engineering.at)*
