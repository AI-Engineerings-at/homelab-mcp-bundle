# Ollama MCP Server

Model Context Protocol Server für Ollama — ermöglicht AI-Agents Zugriff auf lokale LLMs.

> **Use Case**: Claude kann über diesen MCP Server andere lokale LLMs (llama3, mistral, phi3, etc.) aufrufen und deren Antworten in seine Workflows einbinden.

## Features

| Tool | Beschreibung |
|------|--------------|
| `models_list` | Alle verfügbaren Modelle mit Größe und Metadaten |
| `generate` | Text generieren aus Prompt (Single-Shot) |
| `chat` | Multi-Turn Chat mit Message-History |
| `pull` | Modell aus Ollama Registry laden |

## Installation

```bash
pip install mcp
```

## Konfiguration

```bash
export OLLAMA_BASE_URL=http://localhost:11434    # Ollama URL (optional)
export OLLAMA_DEFAULT_MODEL=llama3.2:3b         # Standard-Modell (optional)
```

## Claude Desktop Konfiguration

`~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ollama": {
      "command": "python3",
      "args": ["/path/to/ollama-mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_DEFAULT_MODEL": "llama3.2:3b"
      }
    }
  }
}
```

## Beispiele

```
models_list()
→ llama3.1:8b (4.58GB), llama3.2:3b (1.88GB)

generate("Erkläre Docker Swarm in 3 Sätzen", model="llama3.2:3b")
→ "Docker Swarm ist ein Container-Orchestrierungssystem..."

chat([
  {"role": "user", "content": "Was ist Prometheus?"},
  {"role": "user", "content": "Wie richte ich Alert Rules ein?"}
])

pull("mistral:7b")
```

## Anforderungen

- Ollama installiert und gestartet (`ollama serve`)
- Python 3.10+
- `mcp[cli]>=1.0.0`
