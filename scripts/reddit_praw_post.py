#!/usr/bin/env python3
"""
Reddit PRAW Posting Script — ai-engineering.at
Usage: python3 reddit_praw_post.py --post austria_kmu
       python3 reddit_praw_post.py --list
       python3 reddit_praw_post.py --dry-run --all-dach
"""
import argparse
import sys
import os
import time

# === CREDENTIALS (set via env vars or edit here) ===
CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID', 'REPLACE_WITH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET', 'REPLACE_WITH_CLIENT_SECRET')
USERNAME = os.environ.get('REDDIT_USERNAME', 'ai_engineering_at')
PASSWORD = os.environ.get('REDDIT_PASSWORD', 'REPLACE_WITH_PASSWORD')
USER_AGENT = 'ai-engineering-at-bot/1.0 (by u/ai_engineering_at)'

# === POSTS ===
POSTS = {
    'austria_kmu': {
        'subreddit': 'Austria',
        'title': 'Lokale KI für österreichische KMU: DSGVO-konform ohne Cloud',
        'text': '''**Update 2026: Wir haben einen vollständigen lokalen AI-Stack für österreichische KMU aufgebaut.**

Hintergrund: Viele KMU wollen KI nutzen, aber DSGVO-konform. Das geht — vollständig lokal.

**Was wir gebaut haben:**
- Ollama (llama3.1:8b) auf eigenem Server — kein OpenAI, kein Azure
- Prometheus + Grafana Monitoring (Enterprise-Grade, komplett lokal)
- n8n Automatisierung (Workflows ohne Cloud-Abhängigkeit)
- DSB-konformes Setup: keine personenbezogenen Daten verlassen die Firma

**Ergebnisse nach 6 Monaten:**
- GPU-Inference unter 5s (RTX 3090, lokales Modell)
- 0 DSGVO-Verstöße (vs. hypothetische Risiken mit US-Cloud-AI)
- Hardware-Kosten amortisiert in ~8 Monaten

**Wichtigster Lernfaktor:** Die meisten KMU glauben, lokale KI sei "für die IT-Spezialisten".
Das stimmt nicht mehr. Mit dem richtigen Stack läuft das auf Standard-Hardware.

Wir haben das gesamte Setup als Playbook dokumentiert (inkl. Monitoring-Configs, n8n-Workflows, DSGVO-Checkliste).

Hat jemand ähnliche Erfahrungen? Was waren eure größten Hürden bei der KI-Implementierung?''',
    },
    'germany_dsgvo': {
        'subreddit': 'germany',
        'title': 'Selbst gehosteter AI-Stack für DSGVO: 6 Monate KMU Learnings',
        'text': '''**Nach 6 Monaten lokaler KI in einem österreichischen KMU — was wirklich funktioniert:**

Der DSGVO-Druck auf KMU bezüglich KI-Nutzung wächst. ChatGPT und Co. sind für viele Anwendungen
einfach nicht konform nutzbar, sobald Kundendaten im Spiel sind.

**Unser Stack (selbst gehostet, kein Cloud-Zwang):**
- **LLM:** Ollama mit llama3.1:8b (auch qwen2.5 für deutsche Texte getestet — top Qualität!)
- **Automatisierung:** n8n (Workflows, Webhooks, API-Integrationen)
- **Monitoring:** Prometheus + Grafana + Alertmanager
- **Infra:** Proxmox VE Cluster, Docker Swarm

**Lessons Learned:**
1. Qwen 2.5 für deutsche Texte klar besser als Llama für DE-Sprache
2. Grafana-Dashboards brauchen Zeit für Tuning, aber danach Gold wert
3. n8n ist für KMU-Automatisierung optimal — kein Code nötig für 80% der Fälle
4. GPU nicht zwingend — CPU-Inference reicht für die meisten KMU-Anwendungen

**Was habt ihr für lokale KI-Lösungen in Produktion? Welche Modelle nutzt ihr?**''',
    },
    'de_technik': {
        'subreddit': 'de_technik',
        'title': 'Produktionsbereiter lokaler LLM-Stack (Lessons Learned nach 6 Monaten)',
        'text': '''**Technische Details: Lokaler AI-Stack in Produktion**

Nach 6 Monaten Betrieb möchte ich unsere Architektur und Learnings teilen.

**Stack:**
```
Hardware: RTX 3090 (24GB VRAM), Proxmox VE Cluster (3 Nodes)
Inference: Ollama (llama3.1:8b primary, llama3.2:3b fallback)
Orchestration: Docker Swarm (3 Manager + Worker)
Monitoring: Prometheus + Grafana (Node Exporter, cAdvisor)
Alerting: Alertmanager → Mattermost (5 Alert Rules)
Automation: n8n (5 aktive Workflows)
```

**Performance-Benchmarks:**
- RTX 3090: ~5s für 500-Token-Response (llama3.1:8b)
- CPU-Fallback (Swarm): ~15s gleiche Query
- GPU-Auslastung: Ø 40% unter Last

**Monitoring-Setup (Enterprise-Grade):**
- 6 Prometheus Alert Rules (TargetDown, HighCPU, HighMemory, DiskSpaceLow/Critical, HighNetworkTraffic)
- Grafana Dashboards: Infra, Docker Swarm, Network, Services, Alerts
- Uptime Kuma: 28 Monitors (HTTP, Ping, TCP)
- Alertmanager → Mattermost Integration

**Was hat nicht funktioniert:**
- k3s statt Docker Swarm (zu komplex für unser Team-Level)
- Langchain in Python (Overhead zu hoch, n8n native reicht)

**Fragen / Diskussion gerne im Thread!**''',
    },
    'de_edv': {
        'subreddit': 'de_EDV',
        'title': 'Lokaler LLM-Stack für DSGVO-konformes KI: Setup + Monitoring (Open Source)',
        'text': '''Teile unsere Architektur für einen produktionsbereiten lokalen AI-Stack.

**Problem:** KMU brauchen KI, können aber US-Cloud-Dienste wegen DSGVO oft nicht nutzen.
**Lösung:** Vollständig selbst gehosteter Stack.

**Core Components:**
- **Ollama** — LLM Inference (llama3.1:8b, llama3.2:3b Fallback)
- **Docker Swarm** — Container Orchestration (3 Manager + 1 Worker)
- **n8n** — Workflow Automation (REST, Webhooks, alle gängigen APIs)
- **Prometheus + Grafana** — Full Observability
- **Mattermost** — Internes Chat + Bot-Commands

**AIOps Integration:**
Wir haben einen Service Monitor Agent gebaut, der:
- Prometheus Alerts direkt nach Mattermost sendet
- Auf `claude <frage>` Commands im Chat antwortet (LLM-gestützt)
- Async Antworten via Ollama (~5-7s, kein Timeout-Problem)

**Was nutzt ihr für lokale KI in der Produktion? Welche Monitoring-Setups empfiehlt ihr?**''',
    },
    'selfhosted': {
        'subreddit': 'selfhosted',
        'title': 'GDPR-compliant local AI stack for SMBs — 6 months in production (n8n + Ollama + Prometheus)',
        'text': '''After 6 months running a local AI stack in production for an Austrian SMB, here are the key takeaways.

**Why local?** EU GDPR creates real compliance challenges with US-based AI APIs when processing customer data. Local inference solves this.

**Stack:**
- **Ollama** (llama3.1:8b on RTX 3090, llama3.2:3b CPU fallback)
- **Docker Swarm** (3-node cluster on Proxmox VE)
- **n8n** for workflow automation (replaced a dozen SaaS tools)
- **Prometheus + Grafana + Alertmanager** for full observability
- **Mattermost** as internal hub + bot interface

**Numbers:**
- RTX 3090: ~5s/500 tokens (llama3.1:8b)
- CPU fallback: ~15s same query
- 28 uptime monitors, 6 alert rules
- 5 active n8n workflows handling customer delivery, notifications, reporting

**GDPR angle:** All data stays on-premise. The compliance story is simple: "No data leaves our network."

**Key learning:** n8n is dramatically underrated for SMB automation. Replaced Zapier + Make + several custom scripts.

Happy to share specific configs if anyone's interested.''',
    },
    'homelab': {
        'subreddit': 'homelab',
        'title': 'Built an enterprise-grade AI monitoring stack on Proxmox — sharing configs (Prometheus + Grafana + Ollama)',
        'text': '''Been running this for 6 months and finally have something worth sharing.

**Hardware:**
- Proxmox VE cluster (3 nodes: 2x HP server, 1x workstation with RTX 3090)
- Docker Swarm on VMs (3 managers, 1 worker)

**Services running:**
- Ollama (llama3.1:8b on GPU, llama3.2:3b CPU fallback)
- Prometheus + Grafana (25 dashboards — Node Exporter, cAdvisor, custom panels)
- Alertmanager → Mattermost (so I get pings when something dies)
- n8n (workflow automation, replaced most of my cronjobs + scripts)
- Uptime Kuma (28 monitors across all services)
- AIOps agent that answers questions in Mattermost chat via LLM

**Grafana setup:** 25 dashboards across Infrastructure, Docker, Network, Apps, Alerts folders. Made a pack of the good ones — Node Exporter Full (2 variants), Proxmox via Prometheus, Pi-hole, Traefik, Blackbox Exporter, Docker Container Summary, and our custom homelab dashboards.

**What surprised me:** The AI angle. Having `claude status` and `claude warum ist pve3 so ausgelastet?` work via Mattermost chat is actually useful — not just a toy.

Anyone else running Proxmox + Docker Swarm? Curious about alternative setups.''',
    },
    'n8n': {
        'subreddit': 'n8n',
        'title': 'Built 13 production workflows for a SaaS product launch — lessons learned',
        'text': '''Just finished a product launch using n8n as the backbone. Sharing what worked.

**What we built:**
- Rapidmail Opt-In → Download token generation → Email delivery (P0 critical path)
- Stripe payment → License generation → Customer onboarding email
- Daily sequencer for 7-day email funnel (dynamic, not just scheduled blasts)
- Prometheus alert pipeline: alert → LLM analysis → Mattermost notification
- n8n ↔ Mattermost bot for infrastructure commands

**Stack:**
- n8n self-hosted on Docker Swarm
- Rapidmail for email delivery (EU-based, GDPR-friendly)
- Stripe for payments
- Ollama (local LLM) for alert analysis
- Mattermost as internal hub

**Lessons learned:**
1. **Error handlers on EVERY production workflow** — learned this the hard way
2. **Webhook naming matters** — `/opt-in-handler` beats `/webhook/abc123` for debugging
3. **n8n ↔ Mattermost integration is underrated** — build your team's ops bot in n8n, not a custom server
4. **Local LLM via n8n HTTP node** — point to Ollama, done. No OpenAI dependency.

We packaged 3 of the most reusable workflows (AI alert pipeline, Opt-In → Download, Welcome mail) as a starter bundle for anyone building similar setups.

Happy to discuss any of the flows in detail.''',
    },
    'grafana': {
        'subreddit': 'grafana',
        'title': 'Share: 25 dashboard pack for homelab/SMB — Proxmox, Docker Swarm, Node Exporter, Traefik, Pi-hole',
        'text': '''Put together a curated set of 25 Grafana dashboards for our homelab/SMB monitoring setup. Sharing the list in case useful.

**Custom dashboards (built for our stack):**
- Voice Gateway Enterprise Monitoring (31 panels — if you run Whisper STT / Piper TTS)
- Docker Swarm Cluster Overview
- Infrastructure Overview (multi-node)
- System Overview (per-host)
- Network Traffic Analysis
- Services Status (uptime, response time)
- Alerts Overview (Prometheus integration)
- Disk Space Monitor
- Docker Monitoring (cAdvisor-based)

**Community picks (from grafana.com, tested):**
- Node Exporter Full — ID 1860 (the classic, 31 panels)
- Node Exporter Full — ID 12486 (updated variant)
- Proxmox Cluster [Flux] — Proxmox VE 7/8 via InfluxDB or Prometheus
- Proxmox via Prometheus — if you use pve_exporter
- Pi-hole Exporter
- NGINX Ingress Controller
- Traefik v1 + v2 (two variants)
- Blackbox Exporter (HTTP endpoint probing — great for uptime monitoring)
- Raspberry Pi + Docker
- Docker Container Summary

**Data sources needed:** Prometheus, node_exporter, cAdvisor, pve_exporter (for Proxmox), pihole_exporter (for Pi-hole), Loki (optional).

All tested on Grafana 10.x / 11.x. Let me know if you want the JSON for any specific one.''',
    },
    'devops': {
        'subreddit': 'devops',
        'title': 'AIOps on a budget: Prometheus alerts → local LLM analysis → Mattermost (open source stack)',
        'text': '''Built an AIOps pipeline for our 5-node homelab/SMB cluster. Full open source, no SaaS. Sharing the architecture.

**The problem:** Alert fatigue. Prometheus fires, Alertmanager pings Mattermost, nobody reads it because it's noise.

**The solution:** Add LLM context before the human sees it.

**Architecture:**
```
Prometheus → Alertmanager → Service Monitor Agent (custom Python)
                                    ↓
                          Quick classification
                          (is this critical/warning/info?)
                                    ↓
                          Ollama (local LLM) for async analysis
                          [primary: RTX 3090, llama3.1:8b]
                          [fallback: CPU inference, llama3.2:3b]
                                    ↓
                          Mattermost #ops-alerts
                          (with context: "pve3 CPU high because backup job running since 2h")
```

**Bonus — chat interface:**
```
@claude warum ist pve3 so ausgelastet?
→ LLM checks metrics, responds in ~5-7s
→ async, no timeout issues
```

**What we're running:**
- Alert rules: TargetDown, HighCPU, HighMemory, DiskSpaceLow/Critical, HighNetworkTraffic
- Response time: ~0.1s for quick commands, ~5-7s for LLM analysis
- Uptime: 6 weeks without manual intervention

The LLM adds context. Instead of "CPU > 80% on pve3", ops gets "pve3 CPU high since 14:32, correlates with backup job started at 14:30, expected duration ~30min based on past runs."

Anyone else doing LLM-augmented alerting? What's your stack?''',
    }
}


def post_to_reddit(subreddit: str, title: str, text: str, dry_run: bool = False):
    if dry_run:
        print(f"[DRY RUN] Would post to r/{subreddit}:")
        print(f"  Title: {title}")
        print(f"  Text preview: {text[:120]}...")
        return 'dry-run'

    try:
        import praw
    except ImportError:
        print("praw not installed. Run: pip install praw")
        sys.exit(1)

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD,
        user_agent=USER_AGENT
    )

    sub = reddit.subreddit(subreddit)
    submission = sub.submit(title=title, selftext=text)
    url = f"https://reddit.com{submission.permalink}"
    print(f"Posted: {url}")
    return url


def main():
    parser = argparse.ArgumentParser(description='Reddit PRAW Post Tool — ai-engineering.at')
    parser.add_argument('--post', help='Post ID to publish (see --list)')
    parser.add_argument('--subreddit', help='Override subreddit')
    parser.add_argument('--list', action='store_true', help='List available posts')
    parser.add_argument('--dry-run', action='store_true', help='Preview without posting')
    parser.add_argument('--all-dach', action='store_true', help='Post all DACH posts with rate-limiting')
    args = parser.parse_args()

    if args.list:
        print("Available posts:")
        for key, post in POSTS.items():
            print(f"  {key:20s} r/{post['subreddit']:20s} — {post['title'][:55]}...")
        return

    if args.all_dach:
        dach_posts = ['austria_kmu', 'germany_dsgvo', 'de_technik', 'de_edv']
        for post_id in dach_posts:
            post = POSTS[post_id]
            print(f"\nPosting '{post_id}' to r/{post['subreddit']}...")
            post_to_reddit(post['subreddit'], post['title'], post['text'], args.dry_run)
            if not args.dry_run and post_id != dach_posts[-1]:
                print("Waiting 10 min before next post (rate limiting)...")
                time.sleep(600)
        return

    if args.post:
        post = POSTS.get(args.post)
        if not post:
            print(f"Unknown post ID: {args.post}")
            print("Use --list to see available posts.")
            sys.exit(1)
        subreddit = args.subreddit or post['subreddit']
        post_to_reddit(subreddit, post['title'], post['text'], args.dry_run)
        return

    parser.print_help()


if __name__ == '__main__':
    main()
