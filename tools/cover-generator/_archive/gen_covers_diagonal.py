#!/usr/bin/env python3
"""
gen_covers_diagonal.py -- Diagonal Cascading Rows Cover Generator

3 diagonale Reihen x 8 Karten = 24 PDF-Seiten

  Reihe 0 (FRONT/UNTEN):  Seiten 1-8,   unten-rechts,  hoechster z-index
  Reihe 1 (MITTE):        Seiten 15-22,  dahinter/oben
  Reihe 2 (BACK/OBEN):    Seiten 30-37,  ganz hinten

Innerhalb jeder Reihe geht es DIAGONAL: unten-links -> oben-rechts.
Jede vordere Reihe UEBERLAPPT die Reihe dahinter.

Usage:
  python3 gen_covers_diagonal.py                      # Mockup-Karten
  python3 gen_covers_diagonal.py --pages /tmp/pages/  # echte PDF-Seiten
  python3 gen_covers_diagonal.py --size both          # wide + square
"""

import base64, argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR  = Path("/home/joe/cli_bridge/products/cover-templates")
EAGLE_PATHS = [
    Path("/home/joe/phantom-ai/landing-page/public/eagle-logo.png"),
    Path("/home/joe/Playbook01/landing-page/public/eagle-logo.png"),
    Path("/home/joe/lead-magnet/logo-new.png"),
]

LAYOUT_WIDE = {
    "canvas_w": 1280, "canvas_h": 720,
    "card_w": 112, "card_h": 158,
    "cards_per_row": 8,
    "step_x": 55,    # x-Schritt innerhalb Reihe (nach rechts)
    "step_y": -30,   # y-Schritt innerhalb Reihe (nach oben = DIAGONAL)
    "row_dx": -115,  # x-Versatz pro Reihe nach hinten (weiter links)
    "row_dy": -80,   # y-Versatz pro Reihe nach hinten (weiter oben)
    "base_x": 710,   # x-Start Reihe 0 (vorne)
    "base_y": 480,   # y-Start Reihe 0 (vorne)
    "rotation": -9,
    "num_rows": 3,
}

LAYOUT_SQUARE = {
    "canvas_w": 800, "canvas_h": 800,
    "card_w": 95, "card_h": 134,
    "cards_per_row": 7,
    "step_x": 52,
    "step_y": -28,
    "row_dx": -100,
    "row_dy": -75,
    "base_x": 380,
    "base_y": 580,
    "rotation": -9,
    "num_rows": 3,
}

PRODUCT = {
    "title": "Der Lokale<br><em>AI-Stack</em>",
    "subtitle": "DSGVO-konformer AI-Server in 7 Tagen",
    "price": "EUR 49",
    "category": "Playbook",
    "accent": "#10B981",
    "features": ["8 Kapitel", "Ollama + GPU", "n8n Integration", "DSGVO-konform"],
    "stats": [("180+", "Seiten"), ("42", "Diagramme"), ("15+", "Services")],
    "row_labels": ["Kapitel 1-3", "Kapitel 4-6", "Kapitel 7-8"],
}


def load_b64(path):
    p = Path(path) if path else None
    if p and p.exists() and p.stat().st_size > 0:
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        return "data:" + mime + ";base64," + base64.b64encode(p.read_bytes()).decode()
    return ""


def find_eagle():
    for p in EAGLE_PATHS:
        if p.exists():
            return load_b64(p)
    return ""


def find_pages(pages_dir, num_rows, cards_per_row):
    if not pages_dir or not Path(pages_dir).exists():
        return [[""] * cards_per_row for _ in range(num_rows)]
    d = Path(pages_dir)
    all_pngs = sorted(d.glob("*.png")) + sorted(d.glob("*.jpg"))
    total = len(all_pngs)
    if total == 0:
        return [[""] * cards_per_row for _ in range(num_rows)]
    row_starts = [0, min(14, total), min(29, total)]
    rows = []
    for start in row_starts:
        row_imgs = [load_b64(all_pngs[start + i]) if (start + i) < total else ""
                    for i in range(cards_per_row)]
        rows.append(row_imgs)
    return rows


def card_html(cx, cy, cw, ch, rot, z, img_uri, page_num, accent):
    if img_uri:
        inner = (f'<img src="{img_uri}" style="width:100%;height:100%;'
                 f'object-fit:cover;object-position:top center;display:block">')
    else:
        lines = "".join(
            f'<div style="height:{h}px;background:rgba(255,255,255,{op});'
            f'border-radius:2px;margin-bottom:{mb}px"></div>'
            for h, op, mb in [
                (2,0.35,4),(14,0.12,3),(14,0.09,3),(14,0.12,6),
                (10,0.08,3),(10,0.11,3),(10,0.09,6),(14,0.13,3),
                (14,0.10,3),(10,0.07,6),(14,0.12,3),(10,0.08,0),
            ]
        )
        inner = (f'<div style="width:100%;height:100%;background:linear-gradient(160deg,'
                 f'#0a1628 0%,#0c1e35 100%);padding:10px 9px;position:relative">'
                 f'<div style="position:absolute;bottom:8px;right:8px;font-size:11px;'
                 f'font-weight:700;color:{accent};opacity:0.7">{page_num}</div>'
                 f'{lines}</div>')
    return (f'<div style="position:absolute;left:{cx}px;top:{cy}px;'
            f'width:{cw}px;height:{ch}px;transform:rotate({rot}deg);z-index:{z};'
            f'border-radius:5px;overflow:hidden;'
            f'border:1.5px solid rgba(255,255,255,0.13);'
            f'box-shadow:0 10px 35px rgba(0,0,0,0.75),0 2px 8px rgba(0,0,0,0.5);">'
            f'{inner}</div>')


def build_diagonal_rows(layout, rows_data, accent):
    n        = layout["cards_per_row"]
    num_rows = layout["num_rows"]
    html     = ""
    for r in range(num_rows):
        # r=0 = VORNE (unten-rechts, hoher z-index)
        # r=2 = HINTEN (oben-links, niedriger z-index)
        z_base   = (num_rows - r) * 10
        row_imgs = rows_data[r] if r < len(rows_data) else [""] * n
        rx = layout["base_x"] + r * layout["row_dx"]
        ry = layout["base_y"] + r * layout["row_dy"]
        for c in range(n):
            cx = rx + c * layout["step_x"]
            cy = ry + c * layout["step_y"]
            img = row_imgs[c] if c < len(row_imgs) else ""
            page_offsets = [1, 15, 30]
            page_num = page_offsets[r] + c if r < len(page_offsets) else r * n + c + 1
            html += card_html(cx, cy, layout["card_w"], layout["card_h"],
                              layout["rotation"], z_base + (n - c), img, page_num, accent)
    return html


def build_row_labels(layout, labels, accent):
    html = ""
    for r, lbl in enumerate(labels):
        if not lbl:
            continue
        lbl_x = layout["base_x"] + r * layout["row_dx"] - 5
        lbl_y = layout["base_y"] + r * layout["row_dy"] - 18
        html += (f'<div style="position:absolute;left:{lbl_x}px;top:{lbl_y}px;'
                 f'font-size:9px;font-weight:700;color:{accent};opacity:0.5;'
                 f'letter-spacing:.1em;text-transform:uppercase;z-index:5;'
                 f'white-space:nowrap">{lbl}</div>')
    return html


def build_html_wide(layout, rows_html, labels_html, eagle_b64, product):
    a = product["accent"]
    w, h = layout["canvas_w"], layout["canvas_h"]
    feats = "".join(
        f'<div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);'
        f'border-radius:5px;padding:5px 11px;color:rgba(248,250,252,0.75);'
        f'font-size:12px;font-weight:500">&#10003; {f}</div>'
        for f in product["features"])
    stats = "".join(
        f'<div style="text-align:left">'
        f'<div style="font-size:22px;font-weight:800;color:{a};line-height:1">{n}</div>'
        f'<div style="font-size:9px;color:rgba(255,255,255,0.28);text-transform:uppercase;'
        f'letter-spacing:.07em;margin-top:2px">{l}</div></div>'
        for n, l in product["stats"])
    eagle_html = (f'<img src="{eagle_b64}" style="width:24px;height:24px;object-fit:contain;'
                  f'opacity:0.55;filter:brightness(0) invert(1)" alt="">') if eagle_b64 else ""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#F8FAFC}}
.cv{{width:{w}px;height:{h}px;position:relative;overflow:hidden;background:linear-gradient(135deg,#090E1C 0%,#0C1428 50%,#070B16 100%)}}
.cv::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 820px 620px at 28% 50%,{a}18 0%,transparent 68%);z-index:0}}
.cv::after{{content:'';position:absolute;inset:0;background-image:linear-gradient({a}06 1px,transparent 1px),linear-gradient(90deg,{a}06 1px,transparent 1px);background-size:52px 52px;z-index:1}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,{a},{a},transparent);z-index:20}}
.vdiv{{position:absolute;left:498px;top:60px;bottom:60px;width:1px;background:linear-gradient(to bottom,transparent,{a}25,transparent);z-index:5}}
.lft{{position:absolute;left:0;top:0;width:510px;height:{h}px;display:flex;flex-direction:column;justify-content:center;padding:56px 44px 56px 52px;z-index:20}}
.br{{display:flex;align-items:center;gap:10px;margin-bottom:22px}}
.bn{{font-size:10px;font-weight:700;color:#2a3c54;letter-spacing:2.5px;text-transform:uppercase}}
.ct{{display:inline-flex;background:{a}1E;border:1px solid {a}4E;color:{a};font-size:11px;font-weight:700;padding:5px 14px;border-radius:3px;letter-spacing:2px;text-transform:uppercase;margin-bottom:20px;width:fit-content}}
h1{{font-size:52px;font-weight:800;line-height:1.07;color:#EFF3F8;margin-bottom:12px;letter-spacing:-1.5px}}
h1 em{{font-style:normal;color:{a}}}
.sub{{font-size:15px;color:#4d6480;line-height:1.55;margin-bottom:24px;max-width:390px}}
.pr{{font-size:46px;font-weight:800;color:{a};margin-bottom:20px}}
.fs{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:28px}}
.div2{{height:1px;background:linear-gradient(to right,{a}40,transparent);margin-bottom:18px}}
.sts{{display:flex;gap:20px}}
.rgt{{position:absolute;left:510px;top:0;right:0;height:{h}px;overflow:hidden;z-index:10}}
.fade-r{{position:absolute;top:0;right:0;width:100px;height:100%;background:linear-gradient(to right,transparent,#090E1C);z-index:50}}
.fade-t{{position:absolute;top:0;left:0;right:0;height:80px;background:linear-gradient(to bottom,#090E1C,transparent);z-index:50}}
.fade-b{{position:absolute;bottom:0;left:0;right:0;height:80px;background:linear-gradient(to top,#090E1C,transparent);z-index:50}}
</style></head><body>
<div class="cv">
  <div class="lline"></div><div class="vdiv"></div>
  <div class="lft">
    <div class="br">{eagle_html}<span class="bn">AI Engineering</span></div>
    <div class="ct">{product['category']}</div>
    <h1>{product['title']}</h1>
    <p class="sub">{product['subtitle']}</p>
    <div class="pr">{product['price']}</div>
    <div class="fs">{feats}</div>
    <div class="div2"></div>
    <div class="sts">{stats}</div>
  </div>
  <div class="rgt">
    {rows_html}
    {labels_html}
    <div class="fade-r"></div><div class="fade-t"></div><div class="fade-b"></div>
  </div>
</div></body></html>"""


def build_html_square(layout, rows_html, labels_html, eagle_b64, product):
    a = product["accent"]
    w, h = layout["canvas_w"], layout["canvas_h"]
    eagle_html = (f'<img src="{eagle_b64}" style="width:28px;height:28px;object-fit:contain;'
                  f'opacity:0.5;filter:brightness(0) invert(1)" alt="">') if eagle_b64 else ""
    feats = "  o  ".join(product["features"])
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#F8FAFC}}
.cv{{width:{w}px;height:{h}px;position:relative;overflow:hidden;background:linear-gradient(160deg,#090E1C 0%,#0C1428 55%,#070B16 100%)}}
.cv::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 600px 500px at 50% 40%,{a}15 0%,transparent 70%);z-index:0}}
.cv::after{{content:'';position:absolute;inset:0;background-image:linear-gradient({a}06 1px,transparent 1px),linear-gradient(90deg,{a}06 1px,transparent 1px);background-size:48px 48px;z-index:1}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(to bottom,transparent,{a},{a},transparent);z-index:20}}
.cards{{position:absolute;inset:0;overflow:hidden;z-index:10}}
.overlay{{position:absolute;bottom:0;left:0;right:0;height:42%;background:linear-gradient(to bottom,transparent 0%,rgba(7,11,22,0.92) 50%,#070B16 100%);z-index:30}}
.fade-r{{position:absolute;top:0;right:0;width:80px;height:100%;background:linear-gradient(to right,transparent,#090E1C);z-index:35}}
.fade-t{{position:absolute;top:0;left:0;right:0;height:60px;background:linear-gradient(to bottom,#090E1C,transparent);z-index:35}}
.txt{{position:absolute;bottom:0;left:0;right:0;padding:20px 28px 28px;z-index:40}}
.ct{{display:inline-flex;background:{a}20;border:1px solid {a}50;color:{a};font-size:10px;font-weight:700;padding:4px 12px;border-radius:3px;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px}}
h1{{font-size:42px;font-weight:800;line-height:1.05;color:#EFF3F8;margin-bottom:8px;letter-spacing:-1px}}
h1 em{{font-style:normal;color:{a}}}
.sub{{font-size:12px;color:#4d6480;margin-bottom:14px}}
.bot{{display:flex;align-items:center;justify-content:space-between}}
.br{{display:flex;align-items:center;gap:8px}}
.bn{{font-size:9px;font-weight:700;color:#253548;letter-spacing:2px;text-transform:uppercase}}
.pr{{font-size:34px;font-weight:800;color:{a}}}
</style></head><body>
<div class="cv">
  <div class="lline"></div>
  <div class="cards">
    {rows_html}
    {labels_html}
    <div class="fade-r"></div><div class="fade-t"></div>
  </div>
  <div class="overlay"></div>
  <div class="txt">
    <div class="ct">{product['category']}</div>
    <h1>{product['title']}</h1>
    <p class="sub">{feats}</p>
    <div class="bot">
      <div class="br">{eagle_html}<span class="bn">AI Engineering</span></div>
      <div class="pr">{product['price']}</div>
    </div>
  </div>
</div></body></html>"""


def render_to_png(html_str, out_path, canvas_w, canvas_h):
    hp = f"/tmp/diag_cover_{out_path.stem}.html"
    Path(hp).write_text(html_str, encoding="utf-8")
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--no-sandbox","--disable-setuid-sandbox",
                                      "--disable-web-security"])
        pg = br.new_page(viewport={"width": canvas_w, "height": canvas_h})
        pg.goto(f"file://{hp}", wait_until="networkidle")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out_path),
                      clip={"x": 0, "y": 0, "width": canvas_w, "height": canvas_h})
        br.close()
    Path(hp).unlink(missing_ok=True)
    kb = out_path.stat().st_size // 1024
    print(f"  ok  {out_path.name}  ({canvas_w}x{canvas_h}, {kb}KB)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages", help="Dir mit PDF-Seiten-PNGs")
    parser.add_argument("--out",   help="Output-Dateiname")
    parser.add_argument("--size",  choices=["wide","square","both"], default="wide")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    eagle = find_eagle()
    sizes = ["wide","square"] if args.size == "both" else [args.size]

    for size in sizes:
        layout    = LAYOUT_WIDE if size == "wide" else LAYOUT_SQUARE
        rows_data = find_pages(args.pages, layout["num_rows"], layout["cards_per_row"])
        has_real  = any(any(img for img in row) for row in rows_data)
        src       = f"Seiten aus {args.pages}" if has_real else "Mockup-Karten"
        print(f"\n[{size}]  {layout['num_rows']} diagonale Reihen x {layout['cards_per_row']} Karten  [{src}]")
        rows_html  = build_diagonal_rows(layout, rows_data, PRODUCT["accent"])
        labels_html= build_row_labels(layout, PRODUCT["row_labels"], PRODUCT["accent"])
        if size == "wide":
            html     = build_html_wide(layout, rows_html, labels_html, eagle, PRODUCT)
            out_name = args.out or "cover-diagonal-wide.png"
        else:
            html     = build_html_square(layout, rows_html, labels_html, eagle, PRODUCT)
            out_name = args.out or "cover-diagonal-square.png"
        out_path = OUTPUT_DIR / out_name if not Path(out_name).is_absolute() else Path(out_name)
        if args.dry_run:
            hp = f"/tmp/diag_{size}.html"
            Path(hp).write_text(html, encoding="utf-8")
            print(f"  DRY  -> {hp}")
            continue
        render_to_png(html, out_path, layout["canvas_w"], layout["canvas_h"])

    print("\nFertig!")


if __name__ == "__main__":
    main()
