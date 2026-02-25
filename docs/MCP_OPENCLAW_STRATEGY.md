# MCP Launch + OpenClaw Strategie — AI-Engineering.at

> **Stand**: 2026-02-25 | Analyst: @lisa01
> **Entscheidung @jim**: Phase 1 = MCP v1.0.0 Launch, Phase 2 = OpenClaw Skills
> **Pricing**: Free auf ClawHub.com + EUR 49 Support Bundle auf Gumroad

---

## Executive Summary

Unsere 6 MCP Server (37 Tools) adressieren eine klare Marktlücke:
**5 von 6 Servern haben kein Äquivalent im OpenClaw Ökosystem** — weder auf clawhub.com
noch in den 51 gebündelten Skills. Wir sind First Mover in der Self-Hosted DevOps Nische.

**3 kritische Erkenntnisse:**

1. **Marktlücke OpenClaw**: portainer, proxmox, uptime-kuma, ollama, mattermost — keiner
   dieser Skills existiert auf clawhub.com (geprüft 2026-02-25). Wir können 5 Kategorien
   von Grund auf besetzen.

2. **Security-first USP**: 36% der MCP Server auf smithery.ai/mcp.so sind anfällig für
   Prompt Injection (Tool-Description-Injection). Unser Bundle mit expliziter Security-Doku
   und validierten Inputs ist ein starkes Differenzierungsmerkmal.

3. **Self-Healing Demand**: Skills mit autonomem Monitoring + Auto-Recovery haben
   7.100+ GitHub Stars (Referenzprojekte) — die Nachfrage nach "intelligenten" Ops-Tools
   ist hoch. Unser AIOps v4.1 System liefert genau das als Grundlage.

---

## Marktanalyse — Key Findings

### MCP Server Markt (Smithery.ai / mcp.so / clawhub.com)

| Kategorie | Markt-Status | Unser Server | Vorteil |
|-----------|-------------|--------------|---------|
| Portainer/Docker Swarm | **Nicht existent** | portainer-mcp (6 Tools) | First Mover |
| Proxmox VE | **Nicht existent** | proxmox-mcp (8 Tools) | First Mover |
| Uptime Kuma | **Nicht existent** | uptime-kuma-mcp (5 Tools) | First Mover |
| Ollama (local LLM) | 2 rudimentäre | ollama-mcp (4 Tools) | Besser + dokumentiert |
| Mattermost | 1 inoffiziell | mattermost-mcp (7 Tools) | Produktionsgetestet |
| n8n | 1 existiert | n8n-mcp (7 Tools) | Mehr Tools, besser |

### Wettbewerbs-Gap: OpenClaw Skills

Von 51 gebündelten OpenClaw Skills (Stand 2026.2.23):
- **Kein** portainer-skill
- **Kein** proxmox-skill
- **Kein** uptime-kuma-skill
- **Kein** ollama-skill (nur allgemein)
- **Kein** mattermost-skill

→ **Wir können clawhub.com in unserer Nische dominieren** bevor andere es bemerken.

### Pricing-Benchmark

| Anbieter | Modell | Preis |
|----------|--------|-------|
| 90% MCP Server (GitHub) | Open Source | Gratis |
| mcpmarket.com (Einzelserver) | Premium | $5–15 |
| Gumroad DevOps Bundles | Bundle + Doku | EUR 19–49 |
| **Wir (Entscheidung @jim)** | **ClawHub gratis + Gumroad Support Bundle** | **EUR 0 + EUR 49** |

**Rationale**: Gratis-Skills auf ClawHub → maximale Reichweite + GitHub Stars.
EUR 49 Support Bundle auf Gumroad → Premium-Käufer die Setup-Hilfe brauchen.

---

## Roadmap

### PHASE 1 — MCP Server Launch v1.0.0 (JETZT)

> **Status**: v1.0.0 ist ready. 6 Server, 37 Tools, README fertig.

#### Ziele Phase 1
- MCP Bundle auf GitHub publishen (public)
- Smithery.ai + mcp.so Einträge erstellen
- EUR 49 Support Bundle auf Gumroad listen
- Launch-Content verbreiten (Reddit, HN, Twitter/X)

#### Deliverables Phase 1

| Task | Wer | Aufwand | Priorität |
|------|-----|---------|-----------|
| GitHub Release v1.0.0 taggen | @jim | 30 min | P0 |
| Smithery.ai Listing erstellen (6 Server) | @lisa01 | 2h | P0 |
| mcp.so Listing erstellen | @lisa01 | 1h | P1 |
| Gumroad Support Bundle (EUR 49) erstellen | @jim | 2h | P0 |
| Reddit r/homelab Launch Post | @lisa01 | 1h | P1 |
| Reddit r/selfhosted Post | @lisa01 | 30 min | P1 |
| Hacker News "Show HN" | @jim | 1h | P1 |
| Twitter/X Thread | @lisa01 | 1h | P2 |

**Timing**: Alles in 1–2 Tagen launchbar.

#### EUR 49 Support Bundle — Inhalt

Das Gumroad-Produkt enthält:
- **Setup Guide** (PDF): Schritt-für-Schritt für alle 6 Server mit Screenshots
- **.env Templates**: Alle Konfigurationen vorgefertigt, nur Werte eintragen
- **claude_desktop_config.json**: Vollständige Konfiguration für alle 6 Server
- **Troubleshooting FAQ**: 20 häufige Probleme mit Lösungen
- **10 getestete Prompt-Vorlagen**: z.B. "Zeige alle Swarm-Services mit Status"
- **Security Hardening Checklist**: Prompt Injection Prevention, Token-Scoping
- **E-Mail Support**: 30 Tage direkter Support von @lisa01 / @jim

**Preisbegründung EUR 49**:
- Claude Code Pro kostet EUR 18/Monat — EUR 49 einmalig ist ein gutes Verhältnis
- Zielgruppe zahlt EUR 100+ für ähnliche DevOps-Templates
- 2–3 gesparte Setup-Stunden rechtfertigen den Preis sofort

---

### PHASE 2 — OpenClaw Skills auf ClawHub.com (2–3 Wochen nach Launch)

> **Basis**: MCP Server sind bekannt → gleichen Code als OpenClaw Skills portieren.
> **Vorteil**: Doppelte Reichweite mit 80% weniger Aufwand (Code existiert schon).

#### Konzept: MCP → OpenClaw Skills

OpenClaw Skills sind SKILL.md-Dateien die dem LLM erklären wie es ein CLI-Tool nutzen
soll. Kein neuer Code nötig — wir schreiben Instruktionen für unsere bestehenden MCP-Server.

**Mit `mcporter` (installierbar via `clawhub install mcporter`) können OpenClaw-Agents
unsere MCP-Server direkt ansprechen** → Brücke zwischen beiden Ökosystemen.

#### Geplante OpenClaw Skills

| Skill Name | Basis | Aufwand | ClawHub-Status |
|-----------|-------|---------|----------------|
| `portainer-ops` | portainer-mcp | 2h | Leer (First Mover!) |
| `proxmox-ops` | proxmox-mcp | 3h | Leer (First Mover!) |
| `n8n-ops` | n8n-mcp | 2h | Leer (First Mover!) |
| `uptime-kuma-ops` | uptime-kuma-mcp | 2h | Leer (First Mover!) |
| `ollama-ops` | ollama-mcp | 2h | 0 konkurrierend |
| `homelab-monitor` | Kombination | 4h | Leer (MEGA-Skill!) |

**Gesamt-Aufwand Phase 2**: ~15h Arbeit für 6 Skills + ClawHub Publisher-Account.

#### `homelab-monitor` Mega-Skill (Highlight)

Kombiniert in einem Skill:
- Prometheus Metriken abfragen
- Grafana Alert-Status
- Uptime Kuma Monitor-Status
- Node Exporter Daten (CPU/RAM/Disk)

**Use Case**: Ein einziger OpenClaw-Befehl in Mattermost zeigt den kompletten Infra-Status.
Kein einziger kombinierter Monitoring-Skill existiert auf clawhub.com.

#### Phase 2 Monetarisierung

| Kanal | Modell | Erwartung |
|-------|--------|-----------|
| ClawHub.com | Gratis (6 Skills) | Community Growth, GitHub Stars |
| Gumroad | "OpenClaw Homelab Starter Kit" EUR 39 | 3–8 Käufer/Monat |
| Cross-Sell | Phase-1-Käufer → OpenClaw Skills | +30% Upsell |

---

## Timeline

```
HEUTE (2026-02-25)
│
├── GitHub Release v1.0.0 taggen
├── Smithery.ai Listings (6 Server)
│
WOCHE 1 (2026-03-03)
│
├── Gumroad Support Bundle live (EUR 49)
├── Reddit + HN Launch Posts
├── Erste Käufer / Feedback
│
WOCHE 2–3 (bis 2026-03-17)
│
├── Phase 2 Start: SKILL.md für portainer-ops schreiben
├── clawhub.com Publisher Account einrichten
├── portainer-ops + proxmox-ops live auf ClawHub
│
WOCHE 3–4 (bis 2026-03-24)
│
├── Alle 6 Skills auf ClawHub live
├── homelab-monitor Mega-Skill publishen
├── OpenClaw Homelab Starter Kit (EUR 39) auf Gumroad
│
MONAT 2 (April 2026)
│
└── Stabilisierung, Support, Community-Aufbau
    └── AI Agent Blueprint v2 mit OpenClaw-Kapitel (EUR 49)
```

---

## Prognose

### Phase 1 (MCP Launch)

| Kanal | Käufer/Monat | MRR |
|-------|-------------|-----|
| Gumroad Support Bundle (EUR 49) | 3–8 | EUR 147–392 |
| Smithery.ai organisch (free) | — | EUR 0 (Sichtbarkeit) |
| **Phase 1 MRR** | | **EUR 147–392** |

### Phase 2 (OpenClaw Skills, ab Monat 2)

| Kanal | Käufer/Monat | MRR |
|-------|-------------|-----|
| ClawHub gratis → Gumroad Konversion | 3–6 | EUR 117–234 |
| OpenClaw Homelab Starter Kit (EUR 39) | 3–8 | EUR 117–312 |
| **Phase 2 zusätzlich** | | **EUR 234–546** |

**Kumulierter MRR nach Monat 2**: EUR 381–938

---

## Entscheidungen (@jim, 2026-02-25)

- [x] **Fokus: Erst MCP Launch (v1.0.0), dann OpenClaw Skills (Phase 2)**
- [x] **Pricing: Free auf ClawHub + EUR 49 Support Bundle auf Gumroad**
- [x] **Security-first als USP kommunizieren** (36% Wettbewerb anfällig für Prompt Injection)
- [x] **Self-Healing / AIOps als Differenzierung** (7.1k Stars Nachfrage-Signal)
- [ ] GitHub Release v1.0.0 → @jim
- [ ] Gumroad Support Bundle erstellen → @jim / @lisa01
- [ ] Smithery.ai Listings → @lisa01

---

## Offene Fragen

1. **Gumroad oder eigene Seite?** — Gumroad für Quick Launch empfohlen, später ai-engineering.at
2. **GitHub Repo Name?** — `AI-Engineerings-at/Playbook01` oder eigenes `mcp-homelab-bundle`?
3. **Support-Umfang EUR 49**: E-Mail 30 Tage ausreichend oder Discord/Mattermost Channel?

---

*Erstellt: 2026-02-25 | @lisa01 | ai-engineering.at*
*Basis: OPENCLAW_ANALYSE.md, ANALYSE.md (Marktrecherche), mcp-servers/README.md*
*Review: @jim (Entscheidungen bestätigt 2026-02-25)*
