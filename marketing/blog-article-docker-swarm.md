# Docker Compose vs Docker Swarm for AI Workloads — What Nobody Tells You

*Published on AI-Engineering.at | ~8 min read*

---

You've built your first AI agent pipeline. It runs beautifully on `docker compose up`. Then your GPU box starts sweating, your colleague wants to spin up a second instance, and suddenly you're Googling "how to scale Docker containers" at 2am.

Been there. Here's what you actually need to know.

---

## The Setup: What We're Actually Comparing

This isn't a generic Docker tutorial. We're talking about **AI workloads specifically**:

- LLM inference servers (Ollama, vLLM, LocalAI)
- Embedding pipelines and vector DB loaders
- n8n / Airflow workflow orchestrators
- Monitoring stacks (Prometheus + Grafana)
- Agents that call other agents

These workloads have specific demands: GPU affinity, persistent volumes, low-latency inter-service communication, and zero-tolerance for downtime during model hot-swaps.

---

## Docker Compose: Your Local Lab Hero

Docker Compose is the tool you learned in week one. It works. It's fast to iterate with. For a single machine running your homelab AI stack, it's probably fine.

**Where Compose shines:**

```yaml
# Simple, readable, version-controlled
services:
  ollama:
    image: ollama/ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"

  n8n:
    image: n8nio/n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
    depends_on:
      - postgres
```

Clean. Declarative. One command to bring everything up.

**The real limits:**

| Limitation | Impact for AI Stacks |
|------------|---------------------|
| Single host only | No failover if GPU box dies |
| Manual scaling | `docker compose up --scale` is clunky |
| No rolling updates | You get downtime during redeploy |
| No health-based routing | Dead container = dead endpoint |

If you're running a production-grade inference API that your team depends on — Compose starts to hurt.

---

## Docker Swarm: The Underrated Middle Ground

Before you jump to Kubernetes (and its 47 YAML files), meet Docker Swarm.

Swarm is Docker's native clustering mode. You get:
- Multi-node orchestration
- Rolling updates with zero downtime
- Built-in load balancing via overlay networks
- Service constraints (pin services to GPU nodes!)

**The architecture that actually works:**

```
Manager Node (Swarm Leader)
├── Scheduler: routes requests
├── Service discovery: DNS-based
└── State store: Raft consensus

Worker Nodes
├── docker-swarm3 (RTX 3090) ← Ollama pinned here
├── docker-swarm2 (CPU heavy) ← n8n, databases
└── docker-swarm (General)   ← Monitoring
```

**Real Swarm config for Ollama with GPU pinning:**

```yaml
version: "3.9"
services:
  ollama:
    image: ollama/ollama
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.hostname == docker-swarm3  # GPU node only!
      restart_policy:
        condition: on-failure
        delay: 5s
    volumes:
      - ollama_models:/root/.ollama
    networks:
      - ai_overlay

networks:
  ai_overlay:
    driver: overlay
    attachable: true
```

The `placement.constraints` key is your best friend. It ensures your 8B parameter model always lands on the node with 24GB VRAM — not the node running your monitoring stack.

---

## Head-to-Head: AI Workload Decision Matrix

| Feature | Compose | Swarm |
|---------|---------|-------|
| Setup time | 5 minutes | 30 minutes |
| GPU pinning | Limited | Native via constraints |
| Multi-node | No | Yes |
| Rolling updates | No | Yes |
| Service mesh | No | Overlay networks |
| Secrets management | .env files | Docker secrets |
| Ops complexity | Low | Medium |
| Kubernetes learning curve | — | Much lower |

---

## The Hybrid Pattern We Use in Production

Here's the real-world architecture we run for the AI Engineering homelab:

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Swarm Cluster                   │
├─────────────────┬──────────────────┬────────────────────┤
│  docker-swarm   │  docker-swarm2   │  docker-swarm3     │
│  (Manager)      │  (Manager)       │  (Manager/Leader)  │
│                 │                  │                     │
│  - Portainer    │  - n8n           │  - Ollama LLM      │
│  - Prometheus   │  - PostgreSQL    │  - Whisper STT     │
│  - Grafana      │  - Redis         │  - Piper TTS       │
│  - Alertmanager │  - AdGuard 2     │  - AdGuard 1       │
└─────────────────┴──────────────────┴────────────────────┘
                           │
                    Overlay Network
                    (ai_net, 10.0.0.0/24)
```

9 stacks, 22 services, ~28 monitoring targets — all declared in YAML, deployed with `docker stack deploy`.

**The workflow:**
1. Develop locally with Compose (fast iteration)
2. Test the stack YAML against a staging Swarm
3. Deploy to production Swarm with `docker stack deploy -c stack.yml stack_name`

Same YAML format. Different runtime semantics.

---

## When to Skip Both and Go Kubernetes

Swarm is not Kubernetes. You'll hit its ceiling if you need:

- Advanced autoscaling (HPA, VPA)
- GPU operator with fractional GPU sharing
- Multi-tenant model serving with resource quotas
- GitOps with ArgoCD or Flux

For a team of 5 running internal AI tooling? Swarm is sufficient and way less operational overhead.

For a SaaS product serving 1000 tenants with different model requirements? Start planning your K8s migration now.

---

## Practical Migration: Compose → Swarm

Migrating your existing Compose setup takes about an hour:

**Step 1: Initialize the Swarm**
```bash
docker swarm init --advertise-addr <manager-ip>
```

**Step 2: Add version and deploy section to your compose files**
```yaml
# Add to each service that needs placement
deploy:
  replicas: 1
  placement:
    constraints:
      - node.role == worker
  restart_policy:
    condition: on-failure
```

**Step 3: Deploy**
```bash
docker stack deploy -c docker-compose.yml mystack
docker service ls  # verify all services are 1/1
```

**Step 4: Verify overlay networking**
```bash
docker network ls | grep overlay
# ai_net    abc123def456  overlay  swarm
```

Your services can now reach each other by service name across nodes.

---

## The Part Nobody Writes About: Secrets

This is where Compose really falls short for AI workloads.

Compose handles secrets via environment variables or `.env` files. These end up in your shell history, in process listings, sometimes in Docker inspect output.

Swarm secrets are different:

```bash
# Create a secret (encrypted in Raft store)
echo "sk-..." | docker secret create openai_api_key -

# Reference in your stack
services:
  agent:
    image: myagent:latest
    secrets:
      - openai_api_key
    environment:
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
```

The secret is available at `/run/secrets/openai_api_key` inside the container — never as an env variable, never in `docker inspect` output.

For API keys to OpenAI, Anthropic, or your self-hosted model endpoints: this matters.

---

## TL;DR — Which Should You Choose?

**Choose Compose if:**
- Single machine, single developer
- Development / experimentation
- You need to iterate fast
- GPU is on the same host as everything else

**Choose Swarm if:**
- Multiple nodes (even just 2)
- Production workloads that need uptime
- You need GPU pinning across a cluster
- You want zero-downtime deploys

**The real answer:** Start with Compose. When you add your second machine or your first "production" workload, migrate to Swarm. The YAML format is ~90% compatible — it's not as painful as it sounds.

---

## Ready to Deploy Your Own AI Stack?

The patterns above are extracted from our **DSGVO-Ready AI Stack for German Teams** — a production-ready Docker Swarm configuration with:

- Ollama + n8n + Prometheus/Grafana pre-configured
- GPU placement rules included
- DSGVO compliance documentation
- Swarm secrets setup for all API keys
- 1-click deploy scripts

**[→ DSGVO AI Stack — EUR 79](https://www.ai-engineering.at/#products)**

Questions? Find us on [GitHub](https://github.com/ai-engineering-at) or reach out via the contact form.

---

*Tags: Docker, Docker Swarm, AI Infrastructure, MLOps, Self-Hosted, DSGVO*
