# SECURITY NOTES

## 2026-02-25 — Hardcoded Secret in n8n Workflow entfernt

### Problem
**Datei**: `products/n8n-starter-bundle/01_stripe-download-delivery.json`
**Node**: `Download-Link generieren` (id: `get-download-link`)
**Header**: `x-download-issuer-secret`

Ein SHA256-Secret-Token war direkt im Workflow-JSON hardcodiert. Diese Datei liegt im Git-Repository und wäre bei einem Push öffentlich sichtbar geworden.

### Was wurde geändert
Der echte Secret-Wert (`b9a8...845`) wurde ersetzt durch:
```
REPLACE_WITH_ENV_VAR
```

### Empfohlene Lösung (Produktiv-Setup)
Das Secret muss als n8n Environment Variable konfiguriert werden:

1. **n8n `.env` Datei** (auf dem Server, NICHT im Repo):
   ```
   DOWNLOAD_ISSUER_SECRET=<echtes_secret>
   ```

2. **Im Workflow** den Wert auf die n8n-Variable umstellen:
   ```
   ={{ $env.DOWNLOAD_ISSUER_SECRET }}
   ```

3. **Secret rotieren**: Da der Wert in Git-History existiert (Commit `af8d2e9` und früher), sollte das Secret auf dem Download-Server neu generiert und dort aktualisiert werden.

### Action Items
- [ ] Neues Secret auf dem Download-Server (10.40.10.99:3002) generieren
- [ ] Altes Secret invalidieren
- [ ] In n8n Produktiv-Instanz als ENV Variable setzen
- [ ] Workflow in n8n mit `$env.DOWNLOAD_ISSUER_SECRET` aktualisieren

### Verantwortlich
@lisa01 — Security-Fix-Commit 2026-02-25
