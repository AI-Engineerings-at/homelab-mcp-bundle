#!/usr/bin/env python3
"""
Patch alle thumbnail-*.html: Split-Layout, rechts echtes Produktbild.
Dann neu rendern mit Playwright.
"""
import asyncio
import re
from pathlib import Path

BASE = Path(__file__).parent

# Mapping: HTML -> Produktbild (relativ zu BASE)
THUMBNAILS = [
    ("thumbnail-n8n-starter-bundle.html",     "thumbnail-n8n-starter-bundle.png",     "n8n-starter-bundle-cover-electric.png"),
    ("thumbnail-ai-agent-blueprint.html",      "thumbnail-ai-agent-blueprint.png",      "ai-agent-blueprint-cover-electric.png"),
    ("thumbnail-dsgvo-art30-bundle.html",      "thumbnail-dsgvo-art30-bundle.png",      "dsgvo-art30-bundle-cover-electric.png"),
    ("thumbnail-grafana-dashboard-pack.html",  "thumbnail-grafana-dashboard-pack.png",  "grafana-dashboard-pack-cover-electric.png"),
    ("thumbnail-homelab-mcp-bundle.html",      "thumbnail-homelab-mcp-bundle.png",      "homelab-mcp-bundle-cover-electric.png"),
    ("thumbnail-localai-playbook.html",        "thumbnail-localai-playbook.png",        "localai-playbook-cover-electric.png"),
]

EXTRA_CSS = """
  /* === SPLIT LAYOUT PATCH === */
  .container {
    flex-direction: row !important;
    align-items: stretch !important;
    justify-content: flex-start !important;
  }
  .eagle-bg {
    width: 360px !important;
    left: 22% !important;
    top: 45% !important;
    opacity: 0.18 !important;
  }
  .content {
    width: 420px !important;
    align-items: flex-start !important;
    text-align: left !important;
    padding: 48px 30px 48px 48px !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
  }
  .tech-chip:nth-child(1) { transform: none !important; margin-bottom: 0 !important; }
  .tech-chip:nth-child(2) { transform: none !important; margin-bottom: 0 !important; }
  .tech-chip:nth-child(3) { transform: none !important; margin-bottom: 0 !important; }
  .tech-chip:nth-child(4) { transform: none !important; margin-bottom: 0 !important; }
  .tech-row {
    flex-direction: row !important;
    flex-wrap: wrap !important;
    align-items: flex-start !important;
    justify-content: flex-start !important;
    gap: 8px !important;
  }
  .product-panel {
    width: 380px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 40px 40px 20px;
    position: relative;
    z-index: 10;
  }
  .product-panel::before {
    content: '';
    position: absolute;
    left: 0; top: 10%; height: 80%; width: 1px;
    background: linear-gradient(to bottom, transparent, rgba(ACCENT_RGB,0.4), transparent);
  }
  .product-panel img {
    width: 300px;
    height: 300px;
    object-fit: cover;
    border-radius: 18px;
    box-shadow: 0 12px 60px rgba(0,0,0,0.85), 0 0 50px rgba(ACCENT_RGB,0.25);
    border: 1px solid rgba(255,255,255,0.08);
  }
  /* === END SPLIT LAYOUT PATCH === */
"""

# Files that already have split layout built-in — render only, no patching
RENDER_ONLY = [
    ("thumbnail-komplett-bundle.html", "thumbnail-komplett-bundle.png"),
]


def get_accent_rgb(html_content: str) -> str:
    m = re.search(r'rgba\((\d+),(\d+),(\d+),0\.\d+\)', html_content)
    if m:
        return f"{m.group(1)},{m.group(2)},{m.group(3)}"
    return "16,185,129"


def patch_html(html_path: Path, product_img: str) -> str:
    content = html_path.read_text(encoding="utf-8")

    accent_rgb = get_accent_rgb(content)
    css_patch = EXTRA_CSS.replace("ACCENT_RGB", accent_rgb)

    content = content.replace("</style>", css_patch + "\n</style>", 1)

    product_panel_html = f'''
  <div class="product-panel">
    <img src="{product_img}" alt="Produktbild">
  </div>'''

    content = content.replace(
        '<div class="footer">',
        product_panel_html + '\n  <div class="footer">',
        1
    )

    return content


def patch_all():
    for html_name, png_name, product_img in THUMBNAILS:
        html_path = BASE / html_name
        if not html_path.exists():
            print(f"  SKIP (fehlt): {html_name}")
            continue
        product_path = BASE / product_img
        if not product_path.exists():
            print(f"  WARNUNG: Produktbild fehlt: {product_img}")
        print(f"  Patching {html_name} ...")
        patched = patch_html(html_path, product_img)
        html_path.write_text(patched, encoding="utf-8")
        print(f"    OK")


async def render_all():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        for html_name, png_name, _ in THUMBNAILS:
            html_path = BASE / html_name
            if not html_path.exists():
                print(f"  SKIP: {html_name}")
                continue
            out_path = BASE / png_name
            print(f"  Rendering {html_name} ...")
            page = await browser.new_page(viewport={"width": 800, "height": 800})
            await page.goto(f"file://{html_path}", wait_until="networkidle")
            await page.wait_for_timeout(1000)
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": 800, "height": 800}
            )
            await page.close()
            size_kb = out_path.stat().st_size // 1024
            print(f"    OK {png_name} ({size_kb}KB)")
        # Render-only files (already have split layout — no patching needed)
        for html_name, png_name in RENDER_ONLY:
            html_path = BASE / html_name
            if not html_path.exists():
                print(f"  SKIP: {html_name}")
                continue
            out_path = BASE / png_name
            print(f"  Rendering {html_name} ...")
            page = await browser.new_page(viewport={"width": 800, "height": 800})
            await page.goto(f"file://{html_path}", wait_until="networkidle")
            await page.wait_for_timeout(1000)
            await page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": 800, "height": 800}
            )
            await page.close()
            size_kb = out_path.stat().st_size // 1024
            print(f"    OK {png_name} ({size_kb}KB)")
        await browser.close()
    print("\nAlle Thumbnails gerendert!")


if __name__ == "__main__":
    print("=== Patching HTML files ===")
    patch_all()
    print("\n=== Rendering PNGs ===")
    asyncio.run(render_all())
