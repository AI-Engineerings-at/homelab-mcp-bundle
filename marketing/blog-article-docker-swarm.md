---
title: Docker Compose vs Docker Swarm für AI-Workloads — Der praktische Vergleich
description: Erfahre, wann du Docker Compose vs Docker Swarm für Self-Hosted AI nutzen solltest. Vergleich mit realen Praxisbeispielen aus unserem Homelab.
keywords:
  - docker swarm AI
  - docker compose vs swarm
  - self-hosted AI infrastructure
  - container orchestration
  - ollama docker
  - produktive AI systeme
author: Lisa01
date: 2026-02-26
slug: docker-swarm-ai-workloads
readtime: 12 min
---

# Docker Compose vs Docker Swarm für AI-Workloads — Wann nutzt man was?

Wer sich mit Self-Hosted AI beschäftigt, steht unweigerlich vor dieser Frage: Reicht Docker Compose für meine AI-Infrastruktur aus, oder brauche ich die volle Power von Docker Swarm? Die Antwort ist nicht trivial — und hängt stark davon ab, wie weit deine AI-Ambitionen gehen.

In diesem Artikel zeige ich dir **echte Unterschiede mit Praxisbeispielen** aus unserem produktiven Homelab. Du wirst verstehen, wann Compose ausreicht und wann Swarm unverzichtbar ist.

## Was ist Docker Compose?

Docker Compose ist das **Schweizer Messer für lokale Container-Orchestrierung**. Mit einer einfachen YAML-Datei definierst du alle Services, Volumes und Networks — und startest alles mit `docker compose up`.

**Typische Anwendung:**
```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  webui:
    image: ghcr.io/open-webui/open-web-ui:latest
    ports:
      - "8080:8080"
    depends_on:
      - ollama
```

Das ist es. Ein Befehl, und die ganze AI-Stack läuft lokal auf einem Docker Host.

**Stärken von Compose:**
- Super einfach zu verstehen und zu debuggen
- Perfekt für Entwicklung und Testing
- Minimale Lernkurve
- Schnelle lokale Prototypen

**Grenzen von Compose:**
- Läuft auf **einem einzelnen Host** — keine Verteilung auf mehrere Maschinen
- Keine automatische Fehlertoleranz — wenn der Host abstürzt, ist alles weg
- Manual Scaling — man muss die YAML manuell anpassen und neu deployen
- Kein Health-Check Management — Prozesse starten blind neu
- Nicht für Produktion geeignet

## Was ist Docker Swarm?

Docker Swarm ist Dockers **native Orchestrierungslösung** — ein echtes Cluster-Management System, das mehrere Docker-Hosts als einen logischen "Schwarm" verwaltet.

**Typische Swarm-Architektur:**
```
┌─────────────────────────────────────┐
│  Docker Swarm Cluster               │
├─────────────────────────────────────┤
│ Manager 1 (Leader)                  │
│ ├─ Service: Ollama                  │
│ └─ Service: Prometheus              │
├─────────────────────────────────────┤
│ Manager 2 / Worker 1                │
│ └─ Service: n8n                     │
├─────────────────────────────────────┤
│ Worker 2                            │
│ ├─ Service: Grafana                 │
│ └─ Service: Neo4j                   │
└─────────────────────────────────────┘
```

**Stärken von Swarm:**
- **Cluster-fähig** — mehrere Hosts als eine Einheit
- **Hochverfügbarkeit (HA)** — automatisches Failover bei Ausfällen
- **Self-Healing** — Swarm startet Containers automatisch neu
- **Deklarativ** — Services sind "zustandsorientiert"
- **Einfach zu verstehen** — weniger Overhead als Kubernetes
- **Integriert in Docker** — keine separate Installation nötig

**Grenzen von Swarm:**
- Kleinerer Feature-Satz als Kubernetes
- Weniger Community-Ökosystem
- Nicht ideal für riesige Cluster (>1000 Nodes)

## Der Vergleich — 6 Punkte, die wirklich zählen

### 1. Skalierung & Multi-Host Support

**Docker Compose:**
- Alles auf einem Host
- Wenn die CPU/GPU/RAM voll ist → Pech
- Horizontal skalieren bedeutet: Manuell SSH in neuen Server, Compose starten, hoffen, dass die Konfiguration passt

**Docker Swarm:**
- Services automatisch über mehrere Hosts verteilt
- "Ich brauche 4 Ollama-Replicas" → Swarm deployed automatisch auf verschiedene Nodes
- GPU-Placement per Constraint konfigurierbar

**Praxisbeispiel aus unserem Homelab:**
Wir laufen auf 3 Proxmox Nodes mit Docker Swarm. Wenn die GPU auf docker-swarm3 überlastet ist, shiftet Swarm automatisch neue n8n-Workflows auf docker-swarm (anderer Manager). Ollama läuft auf exakt einem Node (wegen GPU), aber Prometheus und Grafana laufen verteilt.

**Gewinner:** Docker Swarm bei Multi-Host-Infrastruktur

---

### 2. High Availability & Fehlertoleranz

**Docker Compose:**
- Der Host stirbt → alles ist weg
- Man braucht externe Monitoring & Restart-Logik (systemd, cron, custom Scripts)
- Keine automatische Service-Migration

**Docker Swarm:**
- 3 Manager-Nodes (Leader + 2 Follower)
- Swarm bleibt quorate, auch wenn 1 Manager ausfällt
- Services werden automatisch auf andere Nodes rescheduled
- Globale Services (z.B. Node Exporter) laufen auf jedem Node

**Praxisbeispiel:**
Letzte Woche ist docker-swarm2 wegen RAM-Fehler abgestürzt. Swarm hat:
1. Den Node als `down` markiert
2. Alle Services automatisch auf Swarm 3 und Swarm rescheduled
3. Zero Downtime für Grafana, n8n, Prometheus

Mit Compose hätten wir das manuell reparieren müssen.

**Gewinner:** Docker Swarm für Produktion

---

### 3. GPU-Management & AI-Spezifische Features

**Docker Compose:**
```yaml
services:
  ollama:
    runtime: nvidia
    environment:
      - CUDA_VISIBLE_DEVICES=0
```

Das funktioniert, solange alles auf einem Host läuft. Aber:
- Keine Smart-GPU-Placement über mehrere Nodes
- Keine Resource-Limits pro Service
- Keine GPU-Constraints ("nur dieser Service auf der RTX 4090")

**Docker Swarm:**
```yaml
services:
  ollama:
    image: ollama/ollama
    deploy:
      placement:
        constraints:
          - node.labels.gpu == "a100"
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

Mit Swarm kannst du:
- Nodes mit `docker node update --label-add gpu=a100 docker-swarm3` taggen
- Services explizit auf GPU-Nodes placen
- Mehrere GPU-Services koordiniert laufen lassen

**Gewinner:** Docker Swarm für GPU-intensive AI Workloads

---

### 4. Deployment & Updates

**Docker Compose:**
```bash
docker compose down
docker compose pull
docker compose up
```

Dieser Prozess ist **nicht-atomar**. Wenn etwas schief geht, sind Services offline.

**Docker Swarm:**
```bash
docker service update --image ollama:latest ollama_service
```

Swarm macht Rolling Updates:
1. Startet neue Container mit neuem Image
2. Testet auf Health
3. Nur wenn erfolgreich → alte Container stoppen
4. Wenn Fehler → automatisches Rollback

Zero Downtime. Atomar. Sicher.

**Gewinner:** Docker Swarm

---

### 5. Monitoring & Observability

**Docker Compose:**
- Keine eingebauten Health Checks
- Du musst externe Tools (cAdvisor, Prometheus scraper) manuell konfigurieren
- Logs? `docker compose logs -f` und hoffen, dass die Maschine nicht stirbt

**Docker Swarm:**
- Service Health integriert
- Jeder Swarm Manager kennt den State aller Services
- `docker service ps <service>` zeigt Fehler, Restarts, Replicas
- Mit Prometheus Label-basiertes Discovering

**Gewinner:** Docker Swarm

---

### 6. Komplexität vs. Vorteile

**Docker Compose:**
- Flache Lernkurve (1-2 Tage)
- YAML-Syntax leicht zu verstehen
- Debugging ist trivial: `docker compose logs`

**Docker Swarm:**
- Konzepte: Services, Tasks, Replicas, Constraints, Placement
- Stack-Deployments vs. Service-Updates
- Quorum, Leader Election, Raft Consensus (muss man nicht verstehen, aber gut zu wissen)
- Debugging: `docker service logs`, `docker service inspect`, `docker node ls`

**Tipping Point:** Docker Swarm wird ab 5+ Services oder Multi-Host-Szenarien *einfacher* als Compose. Man schreibt weniger YAML-Hacks und handwritten Bash-Scripts.

**Gewinner:** Compose für Simplicity, Swarm für Enterprise-Pattern

## Wann Compose, wann Swarm? — Die Entscheidungsmatrix

| Szenario | Compose | Swarm |
|----------|---------|-------|
| **Lokale Entwicklung** | ✅ Perfekt | Overkill |
| **1 Host, <5 Services** | ✅ Ideal | Optional |
| **2+ Hosts** | ❌ Nicht geeignet | ✅ Erforderlich |
| **GPU AI-Workloads** | ⚠️ Möglich | ✅ Besser |
| **High Availability erforderlich** | ❌ Nein | ✅ Ja |
| **Automatische Failover** | ❌ Nein | ✅ Ja |
| **Rolling Deployments** | ⚠️ Manuell | ✅ Automatisch |
| **Production AI-Stack** | ❌ Nein | ✅ Ja |
| **Self-Hosted Infrastruktur** | ⚠️ Zu einfach | ✅ Goldstandard |

**Faustregel:**
- **Compose:** Laptop, Entwicklung, Proof-of-Concept
- **Swarm:** Alles, das laufen und nicht kaputt gehen darf

## Praxisbeispiel — AI Stack mit Docker Swarm

Hier ist, was wir in unserem Homelab produktiv laufen lassen:

**3 Swarm Manager Nodes:**
```
docker-swarm (10.40.10.80)    — Leader
docker-swarm2 (10.40.10.82)   — Manager
docker-swarm3 (10.40.10.83)   — Manager + GPU
```

**9 Docker Stacks deployed:**

| Stack | Services | AI-Relevanz |
|-------|----------|------------|
| **ollama** | Ollama Server | GPU-beschleunigt (llama3.2:3b) |
| **n8n** | Workflow Automation | Trainings-Pipelines, Datenverarbeitung |
| **monitoring** | Prometheus, Grafana, Alertmanager | Observability für alle Services |
| **aiops** | Neo4j, Context Manager | Knowledge Graph, Agent State |
| **portainer** | Web UI | Cluster Management |
| **adguard** | DNS Filter | Netzwerk (redundant auf 2 Nodes) |
| **kroki** | Diagramm-Rendering | Dokumentation |
| **core** | Kong API Gateway, PostgreSQL, Redis | API Management + Persistence |
| **agents** | Service Monitor Agent v4 | Mattermost Integration |

**Der Trick:** Jeder Service hat Health Checks, HA ist konfiguriert, GPUs sind über Labels gemanagt.

**Beispiel Service Definition:**
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.labels.gpu == true
      update_config:
        parallelism: 1
        delay: 10s
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
```

Das ist **einmal geschrieben, läuft überall** — völlig egal, ob docker-swarm3 morgen stirbt.

## Fertig konfigurierter AI Stack — Spare dir Monate an Konfiguration

Wenn dich diese Komplexität abschreckt: kein Problem. Wir haben einen **kompletten, produktionsreifen AI Stack** mit Docker Swarm zusammengestellt.

Inklusive:
- ✅ 3 Node Swarm Cluster Setup
- ✅ Ollama mit GPU-Beschleunigung
- ✅ n8n für AI-Workflows
- ✅ Prometheus + Grafana Monitoring
- ✅ Neo4j Knowledge Graph
- ✅ Mattermost Integration für Alerts
- ✅ HA-Konfiguration für alle Services
- ✅ Sicherheit, Backups, DSGVO-Konformität

**Der DSGVO AI Stack** (EUR 79) enthält:
- Docker Compose + Docker Swarm Vergleich (vollständige Dokumentation)
- 5 fertige Stack-Konfigurationen
- Shell-Scripts für automatisiertes Deployment
- Prometheus Alert Rules (30+ vorkonfiguriert)
- Grafana Dashboard Templates
- Troubleshooting-Guide

[👉 DSGVO AI Stack auf Gumroad kaufen](https://aiengineering.gumroad.com/l/dsgvo-bundle)

Zahlreiche Homelab-Betreiber haben damit produktive Infrastruktur in wenigen Stunden statt Wochen aufgebaut.

## Fazit

**Docker Compose ist großartig.** Für Entwicklung, lokale Tests, schnelle Prototypen.

**Docker Swarm ist notwendig.** Für alles, das zuverlässig laufen muss. Für AI-Workloads mit GPUs. Für Self-Hosted Infrastruktur, die nicht kaputt gehen darf.

Die gute Nachricht: Swarm ist nicht mal 10% komplexer als Compose. Die Lernkurve ist flach. Und die Zugewinne (HA, Automatisierung, Skalierung) sind gigantisch.

**Wenn du AI selbst hosten willst:** Invest 2 Tage in Swarm lernen. Es lohnt sich.

---

**Noch Fragen zur Architektur?** Schreib einen Kommentar oder check die offizielle [Docker Swarm Dokumentation](https://docs.docker.com/engine/swarm/).

**Fertig zum Implementieren?** Der DSGVO AI Stack zeigt dir, wie's gemacht wird. [Kaufen auf Gumroad](https://aiengineering.gumroad.com/l/dsgvo-bundle).

---

*Artikel erstellt: 26.02.2026 | Lesedauer: 12 Minuten*
