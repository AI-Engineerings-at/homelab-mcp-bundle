# Cloudflare Tunnel — 5 Schritte Copy-Paste

**Ziel**: ai-engineering.at Services öffentlich ohne Port-Forwarding

---

## SCHRITT 1 — Tunnel erstellen (Browser, 2 min)

1. Öffne: **https://one.dash.cloudflare.com**
2. Links: **Networks → Tunnels → Create a tunnel**
3. Name: `homelab-tunnel` → Save
4. Wähle **Docker**
5. **Token kopieren und aufheben!** (langer String mit `eyJ...`)

---

## SCHRITT 2 — Subdomains zuweisen (Browser, 1 min)

In Cloudflare: **homelab-tunnel → Configure → Public Hostname → Add**

| Subdomain | Domain | Service URL |
|-----------|--------|-------------|
| `n8n` | ai-engineering.at | `http://10.40.10.80:5678` |
| `download` | ai-engineering.at | `http://10.40.10.99:3002` |

Klick jeweils **Save**.

---

## SCHRITT 3 — SSH + Token speichern (Terminal)

```bash
ssh root@10.40.10.83
```

```bash
# DEIN_TOKEN = der lange eyJ... String aus Schritt 1
echo "DEIN_TOKEN_HIER" | docker secret create cloudflare_tunnel_token -
```

---

## SCHRITT 4 — Stack deployen (Terminal, alles auf einmal)

```bash
mkdir -p /opt/stacks/cloudflare-tunnel && cat > /opt/stacks/cloudflare-tunnel/docker-compose.yml << 'EOF'
version: '3.8'
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    command: tunnel --no-autoupdate run
    environment:
      - TUNNEL_TOKEN_FILE=/run/secrets/cloudflare_tunnel_token
    secrets:
      - cloudflare_tunnel_token
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
secrets:
  cloudflare_tunnel_token:
    external: true
EOF
docker stack deploy -c /opt/stacks/cloudflare-tunnel/docker-compose.yml cloudflare-tunnel
```

---

## SCHRITT 5 — Prüfen (30 Sekunden warten)

```bash
docker service logs cloudflare-tunnel_cloudflared 2>&1 | tail -5
```

Erwartetes Ergebnis: `Registered tunnel connection` ✅

**Cloudflare UI prüfen**: Networks → Tunnels → homelab-tunnel → Status: **HEALTHY**

---

## Ergebnis

| Was | URL |
|-----|-----|
| n8n Webhooks | https://n8n.ai-engineering.at |
| Downloads | https://download.ai-engineering.at |

**Kein Router anfassen. Kein Port öffnen. Kostenlos.**

---

*Bei Problemen: `docker service ps cloudflare-tunnel_cloudflared --no-trunc`*
