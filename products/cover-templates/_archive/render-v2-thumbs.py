#!/usr/bin/env python3
"""Render all cover-v2-*.html files → PNG (800x800)."""
import asyncio
from pathlib import Path

BASE = Path(__file__).parent

V2_FILES = [
    ("cover-v2-playbook.html",   "cover-v2-playbook.png"),
    ("cover-v2-n8n.html",        "cover-v2-n8n.png"),
    ("cover-v2-dsgvo.html",      "cover-v2-dsgvo.png"),
    ("cover-v2-blueprint.html",  "cover-v2-blueprint.png"),
    ("cover-v2-grafana.html",    "cover-v2-grafana.png"),
    ("cover-v2-cheatsheet.html", "cover-v2-cheatsheet.png"),
    ("cover-v2-mcp.html",        "cover-v2-mcp.png"),
]

async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        for html_name, png_name in V2_FILES:
            html_path = BASE / html_name
            if not html_path.exists():
                print(f"  SKIP (fehlt): {html_name}")
                continue
            out_path = BASE / png_name
            print(f"  [{html_name}] -> {png_name}")
            page = await browser.new_page(viewport={"width": 800, "height": 800})
            await page.goto(f"file://{html_path}", wait_until="networkidle")
            await page.wait_for_timeout(800)
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": 800, "height": 800}
            )
            await page.close()
            size_kb = out_path.stat().st_size // 1024
            print(f"    OK {png_name} ({size_kb}KB)")
        await browser.close()
    print("\nAlle Thumbnail v2 fertig!")

if __name__ == "__main__":
    asyncio.run(render())
