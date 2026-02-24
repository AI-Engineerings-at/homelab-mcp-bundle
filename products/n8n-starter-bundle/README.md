# n8n Starter Bundle — DACH AI Automation

**3 produktionsreife Workflows | Sofort einsatzbereit | DSGVO-konform**

---

## Enthaltene Workflows

### 1. Stripe → Download-Delivery (`01_stripe-download-delivery.json`)
Automatischer digitaler Produktversand nach Stripe-Zahlung.
- Stripe Webhook empfangen
- Zahlung verifizieren
- Download-Link per E-Mail versenden
- Ideal für: E-Books, Templates, Software-Lizenzen

### 2. Ollama LLM Analysis (`02_ollama-llm-analysis.json`)
Lokale KI-Analyse mit Ollama — kein OpenAI-API-Key nötig.
- Webhook-getriggert
- Lokales LLM (llama3.1, llama3.2)
- Mattermost/Slack-Integration
- Ideal für: Self-Hosted AI, DSGVO-konforme KI

### 3. DSGVO Art.30 Verarbeitungsverzeichnis (`03_dsgvo-art30-tracker.json`)
Webhook-API zum Erfassen von Verarbeitungstätigkeiten.
- POST-Endpoint für neue Einträge
- Validierung der Pflichtfelder
- Strukturierte JSON-Ausgabe
- Ideal für: DSGVO-Compliance, Datenschutzbeauftragte

---

## Installation

1. n8n öffnen → Workflows → Import
2. JSON-Datei hochladen
3. Credentials anpassen (Stripe, SMTP, Ollama-URL)
4. Workflow aktivieren

## Anforderungen
- n8n >= 1.0
- Für Workflow 1: Stripe Account
- Für Workflow 2: Ollama lokal oder remote
- Für Workflow 3: Kein externes Service nötig

---

*Erstellt von AI-Engineerings | DACH-optimiert | 2026*
