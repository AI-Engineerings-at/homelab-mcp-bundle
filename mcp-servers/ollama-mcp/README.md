# Ollama MCP Server

**Run local LLMs from any MCP-capable AI assistant — list models, generate text, chat and pull new models.**

> Built by [AI-Engineering.at](https://ai-engineering.at) — Self-Hosted AI Infrastructure.

---

## What is this?

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that connects AI assistants
(Claude, Cursor, etc.) directly to your local [Ollama](https://ollama.ai) instance.

Use Claude to query your **self-hosted Llama, Mistral, or Gemma models** — or let one AI orchestrate another.

---

## Tools (4)

| Tool | Description |
|------|-------------|
| `models_list` | List all locally available models (name, size, quantization) |
| `generate` | Single-turn text generation with optional system prompt |
| `chat` | Multi-turn chat with message history (system/user/assistant) |
| `pull` | Download a model from the Ollama registry |

---

## Requirements

- Python 3.11+
- [Ollama](https://ollama.ai) running locally or on your network
- At least one model pulled (e.g. `ollama pull llama3.2:3b`)

---

## Quick Start

```bash
# 1. Install dependencies
pip install mcp httpx

# 2. Set your Ollama URL (default: http://localhost:11434)
export OLLAMA_BASE_URL="http://localhost:11434"

# 3. Run the server
python3 src/ollama_mcp/server.py
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API base URL |

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ollama": {
      "command": "python3",
      "args": ["/path/to/ollama-mcp/src/ollama_mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434"
      }
    }
  }
}
```

### Remote Ollama (e.g. home server with GPU)

```json
{
  "mcpServers": {
    "ollama": {
      "command": "python3",
      "args": ["/path/to/ollama-mcp/src/ollama_mcp/server.py"],
      "env": {
        "OLLAMA_BASE_URL": "http://192.168.1.100:11434"
      }
    }
  }
}
```

### Claude Code CLI

```bash
claude mcp add ollama python3 \
  /path/to/ollama-mcp/src/ollama_mcp/server.py \
  -e OLLAMA_BASE_URL=http://localhost:11434
```

---

## Example Prompts

```
"What models do I have available on Ollama?"
"Generate a Python script for parsing CSV files using llama3.2:3b"
"Chat with mistral:7b: explain Docker networking in simple terms"
"Pull the codellama:13b model"
```

---

## Use Cases

- **AI orchestrating AI** — let Claude delegate tasks to your local models
- **Privacy-first**: run sensitive queries on your own hardware
- **Cost-free inference** — no API bills for bulk tasks
- **Model comparison** — test the same prompt across multiple local models

---

## Roadmap (v0.2+)

- [ ] `delete_model` — Remove unused models to free disk space
- [ ] `model_info` — Show model details (parameters, context length)
- [ ] `list_running` — See currently loaded models in memory
- [ ] Streaming responses support
- [ ] Docker image for zero-config deployment

---

## License

MIT — use freely, modify and resell.

---

*Made with love by the AI-Engineering.at team.*
