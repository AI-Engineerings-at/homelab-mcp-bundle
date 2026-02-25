# Proxmox MCP Server

Model Context Protocol Server für Proxmox VE — ermöglicht AI-Agents Cluster-Verwaltung über natürliche Sprache.

> **Marktlücke**: Kein kommerzieller Proxmox MCP Server existiert (Stand: 2026-02)

## Features

| Tool | Beschreibung |
|------|--------------|
| `nodes_list` | Alle PVE Cluster-Nodes mit CPU/RAM/Disk-Auslastung |
| `vms_list` | Alle VMs und LXCs (optional: Filter nach Node) |
| `vm_status` | Live-Status einer einzelnen VM/LXC |
| `vm_start` | VM oder LXC starten |
| `vm_stop` | VM oder LXC stoppen (graceful ACPI oder force) |
| `vm_resources` | Top CPU/RAM Verbraucher + Cluster-Totals |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export PVE_HOST=10.40.10.14          # Proxmox VE Hostname/IP
export PVE_USER=root@pam             # Benutzer (optional, Standard: root@pam)
export PVE_PASSWORD=<dein-passwort>  # Passwort (PFLICHT)
export PVE_VERIFY_SSL=false          # SSL-Verifizierung (optional, Standard: false)
```

## Claude Desktop Konfiguration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "proxmox": {
      "command": "python3",
      "args": ["/path/to/proxmox-mcp/server.py"],
      "env": {
        "PVE_HOST": "10.40.10.14",
        "PVE_PASSWORD": "<dein-passwort>"
      }
    }
  }
}
```

## Beispiele

```
# Alle Nodes anzeigen
nodes_list()
→ pve: online, CPU=13.5%, RAM=95.3%, Disk=12.7%

# Alle VMs auflisten
vms_list()
→ 8 VMs auf 3 Nodes (pve, pve1, pve3)

# VM starten
vm_start(node="pve1", vmid=103)
→ {"task_id": "UPID:pve1:...", "status": "started"}

# Top Ressourcen-Verbraucher
vm_resources()
→ Top CPU: docker-swarm3 (15.2%), docker-swarm (8.1%)
```

## Sicherheitshinweis

Der `vm_start` und `vm_stop` Befehl verändert den Zustand von VMs. In Produktionsumgebungen empfiehlt sich ein dedizierter API-Benutzer mit eingeschränkten Rechten (z.B. `PVEVMAdmin` Rolle).

## Test

```bash
PVE_PASSWORD=<passwort> python3 test.py
```

## Anforderungen

- Proxmox VE 7.0+
- Python 3.10+
- `mcp[cli]>=1.0.0`
