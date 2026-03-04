# Cloudflare Tunnel Setup — Copy-Paste Anleitung
## für ai-engineering.at → n8n, Downloads, Landing Page

---

## Was du brauchst

- Cloudflare Account (kostenlos)
- Domain ai-engineering.at → muss bei Cloudflare als Zone sein
- Docker Swarm Zugriff (du hast es)

---

## Schritt 1: Cloudflare Tunnel erstellen (Web UI)

1. Gehe zu: **https://one.dash.cloudflare.com**
2. Links: **Networks → Tunnels**
3. Klick: **"Create a tunnel"**
4. Name: `homelab-tunnel`
5. Klick: **"Save tunnel"**
6. Wähle **Docker** als Connector
7. **Kopiere den Token** — sieht so aus:
   ```
   eyJhIjoiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...
   ```
   → Speichere ihn! Du brauchst ihn in Schritt 3.

---

## Schritt 2: DNS Records konfigurieren (in Cloudflare)

Gehe zu **Networks → Tunnels → homelab-tunnel → Configure → Public Hostname**

Füge diese Routen hinzu (Add a public hostname):

| Subdomain | Domain | Service |
|-----------|--------|---------|
| `n8n` | ai-engineering.at | `http://10.40.10.80:5678` |
| `download` | ai-engineering.at | `http://10.40.10.99:3002` |
| `api` | ai-engineering.at | `http://10.40.10.80:8000` |

→ DNS Records werden automatisch erstellt!

---

## Schritt 3: cloudflared als Docker Stack deployen

SSH auf docker-swarm3 (Leader):

```bash
ssh root@10.40.10.83
```

Stack-Datei erstellen:

```bash
cat > /opt/stacks/cloudflare-tunnel/docker-compose.yml << 'STACK'
version: '3.8'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    command: tunnel --no-autoupdate run --token ${TUNNEL_TOKEN}
    environment:
      - TUNNEL_TOKEN=${TUNNEL_TOKEN}
    networks:
      - proxy
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      restart_policy:
        condition: on-failure
        delay: 5s

networks:
  proxy:
    external: true
    name: core_proxy
STACK
```

Token als Swarm Secret speichern:

```bash
# Ersetze XXXX mit deinem echten Token aus Schritt 1!
echo "DEIN_TOKEN_HIER" | docker secret create cloudflare_tunnel_token -
```

Stack deployen:

```bash
TUNNEL_TOKEN=$(docker secret inspect cloudflare_tunnel_token --format '{{.Spec.Data}}' | base64 -d) \
  docker stack deploy -c /opt/stacks/cloudflare-tunnel/docker-compose.yml cloudflare-tunnel
```

---

## Schritt 4: Testen

```bash
# Tunnel Status prüfen
docker service logs cloudflare-tunnel_cloudflared

# Von außen testen (nach 1-2 Minuten)
curl https://n8n.ai-engineering.at/healthz
```

Cloudflare UI → Networks → Tunnels → homelab-tunnel → Status: **HEALTHY** ✅

---

## Schritt 5: n8n Webhook URL aktualisieren

In n8n Settings (http://10.40.10.80:5678/settings/personal):

```
Webhook URL: https://n8n.ai-engineering.at
```

→ Alle neuen Webhooks nutzen automatisch die öffentliche URL!

---

## Fertig! Deine Services sind jetzt public:

| URL | Service |
|-----|---------|
| `https://n8n.ai-engineering.at` | n8n Webhooks (Stripe etc.) |
| `https://download.ai-engineering.at` | Download-Issuer :3002 |
| `https://api.ai-engineering.at` | Kong API Gateway |

**Kein Port-Forwarding nötig. Kein offener Router-Port. Kostenlos.**

---

## Troubleshooting

```bash
# Tunnel läuft nicht?
docker service ps cloudflare-tunnel_cloudflared --no-trunc

# Neu deployen
docker service update --force cloudflare-tunnel_cloudflared

# Logs live
docker service logs -f cloudflare-tunnel_cloudflared
```

## Nächster Schritt nach Setup:

Stripe Webhook URL von `http://10.40.10.99:3002/...` auf `https://download.ai-engineering.at/...` ändern!
→ In Stripe Dashboard: Developers → Webhooks → Edit endpoint URL
