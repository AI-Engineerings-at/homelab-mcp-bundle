#!/usr/bin/env python3
"""
Ollama MCP Server
Enables AI agents to interact with local Ollama LLMs via Model Context Protocol.

Features:
- models/list     — List all available models with metadata
- generate        — Generate text from a prompt (single-shot)
- chat            — Chat with message history (multi-turn)
- pull            — Pull/download a model from Ollama registry
"""

import os
import json
import urllib.request
from typing import Any
from mcp.server.fastmcp import FastMCP

# Configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.environ.get("OLLAMA_DEFAULT_MODEL", "llama3.2:3b")

mcp = FastMCP("ollama-mcp")


def ollama_request(method: str, path: str, data: dict = None, stream: bool = False) -> Any:
    """HTTP request to Ollama API."""
    url = f"{OLLAMA_BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Ollama API error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ollama not reachable at {OLLAMA_BASE_URL}: {e.reason}")


@mcp.tool()
def models_list() -> str:
    """
    Lists all available Ollama models with size and metadata.

    Returns:
        JSON list of models with name, size, family, parameter count, and modification date
    """
    resp = ollama_request("GET", "/api/tags")
    models = resp.get("models", [])

    result = []
    for m in models:
        details = m.get("details", {})
        result.append({
            "name": m.get("name"),
            "size_gb": round(m.get("size", 0) / 1024**3, 2),
            "family": details.get("family"),
            "parameter_size": details.get("parameter_size"),
            "quantization": details.get("quantization_level"),
            "format": details.get("format"),
            "modified_at": m.get("modified_at", "")[:19] if m.get("modified_at") else None,
        })

    return json.dumps({
        "models": result,
        "total": len(result),
        "ollama_url": OLLAMA_BASE_URL,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def generate(prompt: str, model: str = None, system: str = None, temperature: float = 0.7) -> str:
    """
    Generates a text response from a prompt (single-shot, no history).

    Args:
        prompt: The input prompt
        model: Model name (default: configured default model)
        system: Optional system prompt to set context/persona
        temperature: Sampling temperature 0.0-2.0 (default: 0.7)

    Returns:
        JSON with generated response, model used, and token stats

    Example:
        generate("Erkläre Docker in 3 Sätzen", model="llama3.2:3b")
    """
    selected_model = model or OLLAMA_DEFAULT_MODEL

    payload: dict = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }
    if system:
        payload["system"] = system

    resp = ollama_request("POST", "/api/generate", payload)

    return json.dumps({
        "model": resp.get("model"),
        "response": resp.get("response"),
        "done": resp.get("done"),
        "total_duration_ms": round(resp.get("total_duration", 0) / 1_000_000, 0),
        "eval_count": resp.get("eval_count"),
        "prompt_eval_count": resp.get("prompt_eval_count"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def chat(messages: list, model: str = None, system: str = None, temperature: float = 0.7) -> str:
    """
    Chat with a model using message history (multi-turn conversation).

    Args:
        messages: List of message dicts with 'role' ('user'/'assistant') and 'content'
        model: Model name (default: configured default model)
        system: Optional system prompt
        temperature: Sampling temperature 0.0-2.0 (default: 0.7)

    Returns:
        JSON with assistant's response and conversation stats

    Example:
        chat([
            {"role": "user", "content": "Was ist Prometheus?"},
            {"role": "assistant", "content": "Prometheus ist ein Monitoring-System..."},
            {"role": "user", "content": "Wie konfiguriert man Alert Rules?"}
        ])
    """
    selected_model = model or OLLAMA_DEFAULT_MODEL

    chat_messages = []
    if system:
        chat_messages.append({"role": "system", "content": system})
    chat_messages.extend(messages)

    payload = {
        "model": selected_model,
        "messages": chat_messages,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    resp = ollama_request("POST", "/api/chat", payload)
    message = resp.get("message", {})

    return json.dumps({
        "model": resp.get("model"),
        "role": message.get("role"),
        "content": message.get("content"),
        "done": resp.get("done"),
        "total_duration_ms": round(resp.get("total_duration", 0) / 1_000_000, 0),
        "eval_count": resp.get("eval_count"),
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def pull(model_name: str) -> str:
    """
    Pulls/downloads a model from Ollama registry.

    Args:
        model_name: Model name to pull (e.g. 'llama3.2:3b', 'mistral:7b', 'phi3:mini')

    Returns:
        JSON with pull status

    Note:
        Large models may take several minutes to download.
        After pulling, the model appears in models_list().
    """
    resp = ollama_request("POST", "/api/pull", {
        "name": model_name,
        "stream": False,
    })

    return json.dumps({
        "model": model_name,
        "status": resp.get("status"),
        "message": f"Model '{model_name}' pull completed with status: {resp.get('status')}",
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(f"Ollama MCP Server starting...", flush=True)
    print(f"Ollama URL: {OLLAMA_BASE_URL} | Default model: {OLLAMA_DEFAULT_MODEL}", flush=True)
    mcp.run()
