"""
Ollama MCP Server
Ollama REST API via Model Context Protocol

Tools:
  - models_list   List all locally available models
  - generate      Generate text from a prompt (single-turn)
  - chat          Multi-turn chat with message history
  - pull          Pull (download) a model from the Ollama registry
"""

import asyncio
import json
import os
import sys
from typing import Any

import httpx

# MCP SDK imports
sys.path.insert(0, "/home/joe/.local/lib/python3.14/site-packages")
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


# ── Config from environment ────────────────────────────────────────────────────
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://10.40.10.99:11434")


# ── Ollama API client ──────────────────────────────────────────────────────────
class OllamaClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    async def models_list(self) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base}/api/tags")
            r.raise_for_status()
            return r.json()

    async def generate(
        self,
        model: str,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system:
            body["system"] = system
        if max_tokens:
            body["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.base}/api/generate", json=body)
            r.raise_for_status()
            return r.json()

    async def chat(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> dict:
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if max_tokens:
            body["options"]["num_predict"] = max_tokens

        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(f"{self.base}/api/chat", json=body)
            r.raise_for_status()
            return r.json()

    async def pull(self, model: str) -> list[dict]:
        """Pull a model — streams progress, returns final status."""
        body = {"name": model, "stream": True}
        lines: list[dict] = []
        async with httpx.AsyncClient(timeout=600) as client:
            async with client.stream("POST", f"{self.base}/api/pull", json=body) as r:
                r.raise_for_status()
                async for line in r.aiter_lines():
                    if line.strip():
                        try:
                            lines.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        return lines


# ── MCP Server ─────────────────────────────────────────────────────────────────
server = Server("ollama-mcp")
ollama = OllamaClient(OLLAMA_BASE_URL)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="models_list",
            description=(
                "List all models currently available on the Ollama instance. "
                "Returns model name, size, parameter count and modification date."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="generate",
            description=(
                "Generate text from a prompt using an Ollama model (single-turn). "
                "Use 'chat' for multi-turn conversations."
            ),
            inputSchema={
                "type": "object",
                "required": ["model", "prompt"],
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model name, e.g. 'llama3.1:8b' or 'llama3.2:3b'",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to send to the model",
                    },
                    "system": {
                        "type": "string",
                        "description": "Optional system prompt to set the assistant's persona/context",
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature 0.0–2.0 (default 0.7)",
                        "default": 0.7,
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate (optional, model default if omitted)",
                    },
                },
            },
        ),
        types.Tool(
            name="chat",
            description=(
                "Multi-turn chat with an Ollama model. "
                "Pass a messages array with role/content pairs (system, user, assistant)."
            ),
            inputSchema={
                "type": "object",
                "required": ["model", "messages"],
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model name, e.g. 'llama3.1:8b'",
                    },
                    "messages": {
                        "type": "array",
                        "description": (
                            "Conversation history as [{role, content}] — "
                            "roles: 'system', 'user', 'assistant'"
                        ),
                        "items": {
                            "type": "object",
                            "required": ["role", "content"],
                            "properties": {
                                "role": {
                                    "type": "string",
                                    "enum": ["system", "user", "assistant"],
                                },
                                "content": {"type": "string"},
                            },
                        },
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature 0.0–2.0 (default 0.7)",
                        "default": 0.7,
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate (optional)",
                    },
                },
            },
        ),
        types.Tool(
            name="pull",
            description=(
                "Pull (download) a model from the Ollama registry. "
                "Use models_list first to see what's already available locally."
            ),
            inputSchema={
                "type": "object",
                "required": ["model"],
                "properties": {
                    "model": {
                        "type": "string",
                        "description": "Model name to pull, e.g. 'mistral:7b' or 'llama3.2:3b'",
                    },
                },
            },
        ),
    ]


# ── Tool dispatcher ─────────────────────────────────────────────────────────────
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    args = arguments or {}

    try:
        if name == "models_list":
            data = await ollama.models_list()
            models = data.get("models", [])
            summary = [
                {
                    "name": m.get("name"),
                    "size_gb": round(m.get("size", 0) / 1_073_741_824, 2),
                    "parameter_size": m.get("details", {}).get("parameter_size"),
                    "quantization": m.get("details", {}).get("quantization_level"),
                    "modified_at": m.get("modified_at"),
                }
                for m in models
            ]
            text = json.dumps(summary, indent=2, ensure_ascii=False)

        elif name == "generate":
            data = await ollama.generate(
                model=args["model"],
                prompt=args["prompt"],
                system=args.get("system"),
                temperature=args.get("temperature", 0.7),
                max_tokens=args.get("max_tokens"),
            )
            result = {
                "model": data.get("model"),
                "response": data.get("response", ""),
                "done": data.get("done"),
                "total_duration_s": round(data.get("total_duration", 0) / 1e9, 2),
                "eval_count": data.get("eval_count"),
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "chat":
            data = await ollama.chat(
                model=args["model"],
                messages=args["messages"],
                temperature=args.get("temperature", 0.7),
                max_tokens=args.get("max_tokens"),
            )
            result = {
                "model": data.get("model"),
                "message": data.get("message", {}),
                "done": data.get("done"),
                "total_duration_s": round(data.get("total_duration", 0) / 1e9, 2),
                "eval_count": data.get("eval_count"),
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        elif name == "pull":
            lines = await ollama.pull(args["model"])
            # Return last status line + summary
            last = lines[-1] if lines else {}
            result = {
                "model": args["model"],
                "status": last.get("status", "unknown"),
                "done": last.get("status") == "success",
                "progress_steps": len(lines),
            }
            text = json.dumps(result, indent=2, ensure_ascii=False)

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as exc:
        text = json.dumps({"error": str(exc)}, indent=2)

    return [types.TextContent(type="text", text=text)]


# ── Entry point ─────────────────────────────────────────────────────────────────
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ollama-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
