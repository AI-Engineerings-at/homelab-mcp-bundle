# automation/ — n8n Social Media & Lead-Gen Workflows

> Lisa01 n8n-Beauftragte | Stand: 2026-02-24

## Enthaltene Workflows

| Datei | n8n Name | ID | Status |
|-------|----------|----|--------|
| `n8n_twitter_post.json` | Social: Twitter/X Post via API | `LDyK8nBLpzGALuyj` | inaktiv (braucht Credentials) |
| `n8n_linkedin_post.json` | Social: LinkedIn Post via API | `Ko81KzIdUHBFS2Ms` | inaktiv (braucht Credentials) |
| `n8n_rapidmail_optin.json` | P0-REV-01: Download-Link nach Opt-In (v2) | `HLrn0v1vHDXNaeOB` | inaktiv (braucht SMTP) |
| `n8n_rapidmail_welcome_mail.json` | REV: Rapidmail Welcome-Mail nach Opt-In | `m6EGyo55z7DWmb8q` | **deployed** (braucht RAPIDMAIL_API_KEY env var) |

## WICHTIG: n8n v2.7.5 Webhook-URL Format

In dieser n8n Version haben API-erstellte Workflows einen **Workflow-ID-Prefix**:

```
# FALSCH (nicht mehr gültig):
http://10.40.10.80:5678/webhook/rapidmail-optin

# KORREKT:
http://10.40.10.80:5678/webhook/{WORKFLOW_ID}/webhook/{PATH}
```

Webhook-Pfade aus der DB:
```sql
SELECT * FROM n8n.webhook_entity;
```

## Setup-Anleitung

### 1. Twitter/X Post Workflow

**Benötigt**: OAuth 1.0a Credentials (Twitter Developer Portal)

```bash
# In n8n: Settings → Credentials → Add
# Type: OAuth1 API
# Felder: Consumer Key, Consumer Secret, Access Token, Access Token Secret
# Herkunft: developer.twitter.com → Your App → Keys and Tokens
```

**Webhook-URL** (nach Aktivierung):
```
POST http://10.40.10.80:5678/webhook/LDyK8nBLpzGALuyj/webhook/twitter-post
```

**Test-Payload**:
```json
{"text": "Mein erster Tweet via n8n! #automation"}
```

### 2. LinkedIn Post Workflow

**Benötigt**: LinkedIn OAuth 2.0 Bearer Token

```bash
# Author URN ermitteln:
curl -H "Authorization: Bearer {TOKEN}" https://api.linkedin.com/v2/me
# → id: "ABC123" → author_urn: "urn:li:person:ABC123"

# Org-Post (für Company Pages):
# author_urn: "urn:li:organization:12345"
```

**Webhook-URL** (nach Aktivierung):
```
POST http://10.40.10.80:5678/webhook/Ko81KzIdUHBFS2Ms/webhook/linkedin-post
```

**Test-Payload**:
```json
{
  "text": "Post über Automation! #n8n",
  "author_urn": "urn:li:person:DEINE_ID"
}
```

### 3. Rapidmail Opt-In → Download-Link

**Benötigt**: SMTP Credential in n8n + Download-URL

```bash
# n8n Environment Variables:
DOWNLOAD_URL=https://deine-domain.de/download/lead-magnet.pdf
SENDER_EMAIL=hallo@deine-domain.de

# In n8n: Credential "SMTP Email" anlegen
# Workflow aktivieren
```

**Webhook-URL** (bereits aktiv als Test-Version):
```
POST http://10.40.10.80:5678/webhook/6XkbGwtKhf5LE9i6/webhook/rapidmail-optin-test
```

**In Rapidmail eintragen** (bei Bestätigung/Double Opt-In):
```
POST http://10.40.10.80:5678/webhook/HLrn0v1vHDXNaeOB/webhook/rapidmail-optin
```

**Test-Payload**:
```json
{"email": "test@example.com", "firstname": "Max"}
```

**Getesteter Curl-Befehl** (funktioniert! ✅):
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"max@example.com","firstname":"Max"}' \
  "http://10.40.10.82:5678/webhook/6XkbGwtKhf5LE9i6/webhook/rapidmail-optin-test"
```

### 4. REV: Rapidmail Welcome-Mail nach Opt-In (NEU - 2026-02-24)

**Workflow-ID**: `m6EGyo55z7DWmb8q`
**Kein SMTP nötig** — nutzt Rapidmail REST API direkt (HTTP Request)

**Benötigt**: `RAPIDMAIL_API_KEY` Env-Var in n8n

```bash
# n8n Environment Variables setzen (auf docker-swarm):
ssh root@10.40.10.80 "
docker service inspect agents_service-monitor --format '{{json .Spec.TaskTemplate.ContainerSpec.Env}}'
# Dann n8n Stack neu deployen mit:
# RAPIDMAIL_API_KEY=<api-key>
# DOWNLOAD_URL=https://ai-engineering.at/download/...
# SENDER_EMAIL=hallo@ai-engineering.at
# SENDER_NAME=Joe von AI-Engineering.at
"
```

**Webhook-URL** (nach Aktivierung):
```
POST http://10.40.10.80:5678/webhook/m6EGyo55z7DWmb8q/webhook/rapidmail-confirmed
```

**In Rapidmail eintragen** (bei Double Opt-In Bestätigung):
```
Mailing-Liste → Einstellungen → Webhooks → Bei Bestätigung:
POST http://10.40.10.80:5678/webhook/m6EGyo55z7DWmb8q/webhook/rapidmail-confirmed
```

**Test**:
```bash
curl -X POST -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","firstname":"Max"}' \
  http://10.40.10.80:5678/webhook-test/rapidmail-confirmed
```

## Nächste Schritte

1. **RAPIDMAIL_API_KEY** in Rapidmail holen: Profil → API → API-Key erstellen
2. **n8n Env-Var** setzen + Welcome-Mail Workflow (`m6EGyo55z7DWmb8q`) aktivieren
3. **Rapidmail Webhook** auf den Workflow-Webhook zeigen lassen
4. **Twitter API Keys** von @joe oder Twitter Developer Portal besorgen
5. **LinkedIn Token** via OAuth2 App generieren
6. Twitter + LinkedIn Workflows aktivieren

## Bekannte Issues

- **n8n v2.7.5 webhook URL**: Immer `/{workflowId}/webhook/{path}` verwenden
- **SMTP Placeholder**: `SMTP_CREDENTIAL_ID` muss durch echte Credential-ID ersetzt werden
- **Twitter OAuth1**: Twitter v2 API erfordert OAuth 1.0a User Context für POST /2/tweets
