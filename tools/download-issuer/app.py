#!/usr/bin/env python3
"""
Download Issuer Service — Port 3002
Generates time-limited signed download links for digital products.
"""

import os
import time
import hmac
import hashlib
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ISSUER_SECRET = os.environ.get(
    "DOWNLOAD_ISSUER_SECRET",
    "b9a8d68a57293a634c5d384bbf12358428ff31d0ef7715b5534139cc45807845"
)
TOKEN_TTL = int(os.environ.get("TOKEN_TTL_SECONDS", 3600))  # 1 Stunde
FILES_DIR = os.path.join(os.path.dirname(__file__), "files")

# Produkt -> Datei Mapping
# NOTE: Files must exist in ./files/ directory before product is purchasable
PRODUCT_MAP = {
    "playbook01":         "Der-Lokale-AI-Stack-Playbook.pdf",    # EUR 49 - Playbook (2.4MB)
    "lead-magnet":        "lead-magnet.pdf",                     # Free lead magnet
    "n8n-bundle":         "n8n-bundle.zip",                      # EUR 29 - n8n Workflow Bundle (13 WF)
    "grafana-pack":       "grafana-dashboard-pack.zip",          # EUR 39 - Grafana Dashboard Pack
    "dsgvo-template":     "dsgvo-art30-template.zip",            # EUR 79 - DSGVO Art.30 Template
    "ai-agent-blueprint": "ai-agent-team-blueprint.zip",         # EUR 19 - AI Agent Team Blueprint
    "komplett-bundle":    "ai-engineering-komplett-bundle.zip",   # EUR 149 - Alle 5 Produkte
    "homelab-mcp-bundle": "Homelab-MCP-Bundle-Cheat-Sheet.pdf",  # FREE - MCP Cheat Sheet
}


def make_token(product_id: str, purchase_ref: str, expires_at: int) -> str:
    msg = f"{product_id}:{purchase_ref}:{expires_at}"
    return hmac.new(ISSUER_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()


def verify_token(token: str, product_id: str, purchase_ref: str, expires_at: int) -> bool:
    expected = make_token(product_id, purchase_ref, expires_at)
    return hmac.compare_digest(token, expected)


def get_base_url() -> str:
    return os.environ.get("BASE_URL", "http://10.40.10.99:3002")


class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")

    def send_json(self, code: int, data: dict):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            available = [p for p, f in PRODUCT_MAP.items()
                         if os.path.exists(os.path.join(FILES_DIR, f))]
            self.send_json(200, {
                "status": "ok",
                "service": "download-issuer",
                "products_configured": len(PRODUCT_MAP),
                "products_available": len(available),
                "available": available,
            })
            return

        if parsed.path.startswith("/download/"):
            self._handle_download(parsed)
            return

        self.send_json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/download-link":
            # Validate secret header
            secret = self.headers.get("x-download-issuer-secret", "")
            if not hmac.compare_digest(secret, ISSUER_SECRET):
                self.send_json(401, {"error": "unauthorized"})
                return

            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}

            product_id   = body.get("product_id", "")
            purchase_ref = body.get("purchase_ref", "unknown")

            if product_id not in PRODUCT_MAP:
                self.send_json(400, {"error": f"unknown product_id: {product_id}"})
                return

            # Check if file is actually available
            filename = PRODUCT_MAP[product_id]
            filepath = os.path.join(FILES_DIR, filename)
            if not os.path.exists(filepath):
                self.send_json(503, {
                    "error": f"product file not yet available: {filename}",
                    "hint": "Upload the file to the files/ directory"
                })
                return

            expires_at = int(time.time()) + TOKEN_TTL
            token = make_token(product_id, purchase_ref, expires_at)
            url = f"{get_base_url()}/download/{token}?p={product_id}&ref={purchase_ref}&exp={expires_at}"

            self.send_json(200, {
                "download_url": url,
                "expires_in_seconds": TOKEN_TTL,
                "product_id": product_id,
                "filename": filename,
            })
            return

        self.send_json(404, {"error": "not found"})

    def _handle_download(self, parsed):
        token = parsed.path.split("/download/")[-1]
        params = parse_qs(parsed.query)

        product_id   = params.get("p", [""])[0]
        purchase_ref = params.get("ref", ["unknown"])[0]
        expires_at   = int(params.get("exp", [0])[0])

        if int(time.time()) > expires_at:
            self.send_json(410, {"error": "link expired"})
            return

        if not verify_token(token, product_id, purchase_ref, expires_at):
            self.send_json(403, {"error": "invalid token"})
            return

        filename = PRODUCT_MAP.get(product_id)
        if not filename:
            self.send_json(404, {"error": "product not found"})
            return

        filepath = os.path.join(FILES_DIR, filename)
        if not os.path.exists(filepath):
            self.send_json(503, {"error": f"file not available: {filename}"})
            return

        with open(filepath, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3002))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"[download-issuer] Listening on 0.0.0.0:{port}")
    print(f"[download-issuer] Files dir: {FILES_DIR}")
    print(f"[download-issuer] Products configured: {list(PRODUCT_MAP.keys())}")
    server.serve_forever()
