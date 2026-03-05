#!/usr/bin/env python3
"""
gemini-brand-gen v1.0 -- Universal Brand Asset Generator
Gemini Free API (SVG gen) + Playwright (HTML->PNG)

Formats: cover(800x800) ig-post(1080x1080) fb-post(1200x630)
         twitter-post(1200x675) yt-thumb(1280x720) ig-story(1080x1920)
         fb-banner(820x312) li-banner(1584x396)

Usage:
  python3 brand_gen.py --title "My Product" --format cover
  python3 brand_gen.py --title "Docker Guide" --format yt-thumb --type thumbnail
  python3 brand_gen.py --prompt "Banner for n8n tutorial" --format fb-banner
  python3 brand_gen.py --brand custom.json --title "Launch" --accent "#FF6B6B"
  python3 brand_gen.py --list-formats
"""

import argparse, json, os, re, base64, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT  = SCRIPT_DIR.parent.parent
ENV_FILE   = REPO_ROOT / ".env"
DEFAULT_BRAND_FILE = SCRIPT_DIR / "brand_kit_default.json"
OUTPUT_DIR = REPO_ROOT / "products" / "brand-gen-output"

FORMATS = {
    "cover":        {"w": 800,  "h": 800,  "layout": "square",    "desc": "Gumroad/Stripe Product Cover"},
    "ig-post":      {"w": 1080, "h": 1080, "layout": "square",    "desc": "Instagram Feed Post"},
    "fb-post":      {"w": 1200, "h": 630,  "layout": "landscape", "desc": "Facebook / LinkedIn Post"},
    "twitter-post": {"w": 1200, "h": 675,  "layout": "landscape", "desc": "Twitter/X Post"},
    "yt-thumb":     {"w": 1280, "h": 720,  "layout": "landscape", "desc": "YouTube Thumbnail"},
    "ig-story":     {"w": 1080, "h": 1920, "layout": "story",     "desc": "Instagram Story / TikTok"},
    "fb-banner":    {"w": 820,  "h": 312,  "layout": "banner",    "desc": "Facebook Page Cover"},
    "li-banner":    {"w": 1584, "h": 396,  "layout": "banner",    "desc": "LinkedIn Page Header"},
}

ASSET_TYPES = ["cover", "thumbnail", "banner", "social", "story", "ad"]
ASSET_HINTS = {
    "cover":     "product showcase: floating UI card or document mockup",
    "thumbnail": "bold visual: large icon or symbol dominating the frame",
    "banner":    "wide decorative header: abstract geometric shapes or connected nodes",
    "social":    "info-card: stats, icons, or bullet-list visualization",
    "story":     "tall mobile visual: large centered icon with decorative rings",
    "ad":        "attention-grabbing: bold shape with clear call-to-action area",
}


def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def load_brand(path=None, overrides=None):
    if path and Path(path).exists():
        brand = json.loads(Path(path).read_text(encoding="utf-8"))
    elif DEFAULT_BRAND_FILE.exists():
        brand = json.loads(DEFAULT_BRAND_FILE.read_text(encoding="utf-8"))
    else:
        brand = {
            "name": "AI Engineering", "accent": "#10B981", "accent_dark": "#059669",
            "bg": "#0F172A", "domain": "ai-engineering.at",
            "logo": str(Path("/home/joe/Playbook01/landing-page/public/eagle-logo-inverted.png")),
        }
    if overrides:
        brand.update({k: v for k, v in overrides.items() if v})
    return brand


def load_logo_b64(logo_path):
    p = Path(logo_path)
    if not p.exists():
        return ""
    ext = p.suffix.lstrip(".")
    with open(p, "rb") as f:
        return f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()


def gemini_call(prompt, api_key, max_tokens=3000, temp=0.65):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temp, "maxOutputTokens": max_tokens},
    }
    url = (f"https://generativelanguage.googleapis.com/v1beta/models"
           f"/gemini-2.5-flash:generateContent?key={api_key}")
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def extract_svg(text):
    for pat in [r'(<svg[\s\S]*?</svg>)', r'```(?:svg|xml)?\s*\n([\s\S]*?</svg>)']:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            s = m.group(1)
            if "<svg" in s:
                return s
    return None


def extract_json_obj(text):
    m = re.search(r'\{[\s\S]*\}', text)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return None


def fallback_svg(accent):
    return f"""<svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="240" rx="12" fill="#0F172A" stroke="{accent}" stroke-width="1" opacity="0.5"/>
  <rect x="20" y="20" width="90" height="8" rx="4" fill="{accent}" opacity="0.8"/>
  <rect x="20" y="42" width="140" height="6" rx="3" fill="#334155"/>
  <rect x="20" y="58" width="110" height="6" rx="3" fill="#334155"/>
  <rect x="20" y="74" width="160" height="6" rx="3" fill="#334155"/>
  <rect x="20" y="90" width="95" height="6" rx="3" fill="#334155"/>
  <rect x="20" y="118" width="75" height="24" rx="6" fill="{accent}" opacity="0.15"/>
  <rect x="104" y="118" width="75" height="24" rx="6" fill="{accent}" opacity="0.10"/>
  <circle cx="320" cy="120" r="60" fill="{accent}" opacity="0.06"/>
  <circle cx="320" cy="120" r="38" fill="{accent}" opacity="0.05"/>
  <circle cx="320" cy="120" r="18" fill="{accent}" opacity="0.08"/>
</svg>"""


def gemini_svg(title, description, accent, asset_type, api_key):
    hint = ASSET_HINTS.get(asset_type, "clean abstract tech illustration")
    prompt = f"""Create a minimal SVG illustration for a dark digital marketing asset.

Topic: {title}
Context: {description or "digital product"}
Visual concept: {hint}
Accent color: {accent}

Rules:
- viewBox MUST be exactly: viewBox="0 0 400 240"
- Max 55 SVG elements
- Dark fills only: #0F172A, #1E293B, #0D1117
- Use {accent} ONLY for accents/borders/strokes (never large fills)
- Rounded corners rx=8 for cards, rx=4 for small elements
- Style: professional tech UI mockup, NOT clip art
- NO stroke-width > 2

Return ONLY the complete <svg> element."""

    try:
        text = gemini_call(prompt, api_key, max_tokens=2800)
        svg = extract_svg(text)
        if svg:
            svg = re.sub(r'viewBox="[^"]*"', 'viewBox="0 0 400 240"', svg)
            return svg
        print("  [warn] No valid SVG from Gemini -- fallback")
    except urllib.error.HTTPError as e:
        print(f"  [warn] Gemini HTTP {e.code} -- fallback")
    except Exception as e:
        print(f"  [warn] Gemini: {e} -- fallback")
    return fallback_svg(accent)


def gemini_spec(user_prompt, fmt_name, api_key):
    prompt = f"""You are a brand designer AI. Generate marketing asset specs.

User request: "{user_prompt}"
Target: {fmt_name} ({FORMATS[fmt_name]['desc']})

Return JSON with exactly these keys:
{{
  "title": "headline (max 40 chars)",
  "subtitle": "supporting text (1-2 sentences)",
  "eyebrow": "category label (2-4 words, uppercase)",
  "badge": "badge text like 'New Release' or empty string",
  "features": ["feature 1", "feature 2", "feature 3"],
  "price": "EUR 49 or FREE or empty",
  "asset_type": "cover|thumbnail|banner|social|story|ad",
  "hero_hint": "describe what SVG visual to draw"
}}

Return ONLY the JSON object."""
    try:
        text = gemini_call(prompt, api_key, max_tokens=600, temp=0.7)
        spec = extract_json_obj(text)
        if spec:
            return spec
    except Exception as e:
        print(f"  [warn] Spec gen failed: {e}")
    return {"title": user_prompt[:40], "subtitle": "", "eyebrow": "", "badge": "",
            "features": [], "price": "", "asset_type": "social",
            "hero_hint": f"abstract visual for: {user_prompt}"}


def build_html(brand, title, subtitle, features, price, svg, fmt_name,
               badge="", eyebrow=""):
    fmt = FORMATS[fmt_name]
    w, h = fmt["w"], fmt["h"]
    layout = fmt["layout"]
    a, ad = brand["accent"], brand.get("accent_dark", brand["accent"])
    bg = brand.get("bg", "#0F172A")
    domain = brand.get("domain", "")
    s = min(w / 800, h / 800)

    logo_b64 = load_logo_b64(brand.get("logo", ""))
    logo_h = (f'<img src="{logo_b64}" style="width:{int(28*s)}px;height:{int(28*s)}px;'
              f'object-fit:contain;opacity:0.6">' if logo_b64 else "")
    pills    = "".join(f'<span class="pill">{f}</span>' for f in (features or []))
    badge_h  = f'<span class="badge">{badge}</span>' if badge else ""
    ey_h     = f'<div class="ey">{eyebrow}</div>' if eyebrow else ""
    price_h  = f'<div class="price">{price}</div>' if price else ""
    brand_h  = (f'<div class="brand">{logo_h}<span>{domain}</span></div>'
                if (logo_b64 or domain) else "")

    if layout in ("landscape", "banner"):
        rw = int(350*s) if layout == "landscape" else int(220*s)
        content = f"""<div class="content">
  <div class="left">{badge_h}{ey_h}<h1 class="title">{title}</h1>
    <p class="sub">{subtitle}</p><div class="pills">{pills}</div>
    <div class="bot">{price_h}{brand_h}</div></div>
  <div class="right"><div class="hero">{svg}</div></div>
</div>"""
        layout_css = (f".content{{display:flex;flex-direction:row;align-items:center;"
                      f"gap:{int(32*s)}px;height:100%;width:100%}}"
                      f".left{{flex:1;display:flex;flex-direction:column;justify-content:center}}"
                      f".right{{width:{rw}px;flex-shrink:0;display:flex;"
                      f"justify-content:center;align-items:center}}")
    elif layout == "story":
        content = f"""<div class="content">
  {badge_h}{ey_h}<div class="hero">{svg}</div>
  <h1 class="title">{title}</h1><p class="sub">{subtitle}</p>
  <div class="pills">{pills}</div><div class="bot">{price_h}{brand_h}</div>
</div>"""
        layout_css = (f".content{{display:flex;flex-direction:column;align-items:center;"
                      f"justify-content:center;text-align:center;height:100%;width:100%;"
                      f"gap:{int(16*s)}px}}")
    else:
        content = f"""<div class="content">
  <div>{badge_h}{ey_h}<h1 class="title">{title}</h1><p class="sub">{subtitle}</p></div>
  <div class="hero">{svg}</div>
  <div><div class="pills">{pills}</div><div class="bot">{price_h}{brand_h}</div></div>
</div>"""
        layout_css = ".content{display:flex;flex-direction:column;justify-content:space-between;height:100%;width:100%}"

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;overflow:hidden;font-family:'Inter',sans-serif}}
.wrap{{width:{w}px;height:{h}px;background:{bg};position:relative;overflow:hidden;
  padding:{int(42*s)}px {int(50*s)}px {int(40*s)}px {int(50*s)}px}}
.grid{{position:absolute;inset:0;
  background-image:linear-gradient({a}09 1px,transparent 1px),linear-gradient(90deg,{a}09 1px,transparent 1px);
  background-size:{int(54*s)}px {int(54*s)}px;z-index:0}}
.glow{{position:absolute;width:{int(520*s)}px;height:{int(520*s)}px;
  background:radial-gradient(circle,{a}18 0%,transparent 65%);
  top:50%;left:50%;transform:translate(-50%,-50%);z-index:0}}
.corner{{position:absolute;top:0;right:0;width:{int(180*s)}px;height:{int(180*s)}px;
  border-left:1px solid {a}22;border-bottom:1px solid {a}22;
  border-bottom-left-radius:{int(180*s)}px;z-index:1}}
.lline{{position:absolute;left:0;top:0;bottom:0;width:3px;
  background:linear-gradient(to bottom,transparent,{a}BB,transparent);z-index:1}}
.wrap>*:not(.grid):not(.glow):not(.corner):not(.lline){{position:relative;z-index:10}}
.badge{{display:inline-flex;align-items:center;gap:6px;background:{a}18;
  border:1px solid {a}44;border-radius:100px;padding:{int(5*s)}px {int(14*s)}px;
  color:{a};font-size:{round(10.5*s,1)}px;font-weight:600;letter-spacing:.07em;
  text-transform:uppercase;margin-bottom:{int(14*s)}px}}
.ey{{color:{a};font-size:{round(11*s,1)}px;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;margin-bottom:{int(12*s)}px}}
.title{{font-family:'Space Grotesk',sans-serif;font-size:{int(58*s)}px;font-weight:800;
  line-height:1.06;color:#F8FAFC;letter-spacing:-.025em;margin-bottom:{int(14*s)}px}}
.title em{{color:{a};font-style:normal}}
.sub{{font-size:{round(14.5*s,1)}px;color:rgba(248,250,252,.52);line-height:1.62;
  margin-bottom:{int(18*s)}px;max-width:{int(480*s)}px}}
.hero{{display:flex;justify-content:center;align-items:center;flex-shrink:0;margin:{int(8*s)}px 0}}
.hero svg{{max-width:100%;height:auto;filter:drop-shadow(0 8px 28px {a}28)}}
.pills{{display:flex;flex-wrap:wrap;gap:{int(7*s)}px;margin-bottom:{int(12*s)}px}}
.pill{{font-size:{round(10.5*s,1)}px;font-weight:500;color:#CBD5E1;
  background:rgba(30,41,59,.9);border:1px solid #334155;
  padding:{int(4*s)}px {int(12*s)}px;border-radius:20px}}
.price{{font-family:'Space Grotesk',sans-serif;font-size:{int(20*s)}px;font-weight:800;
  background:linear-gradient(135deg,{a},{ad});border-radius:{int(9*s)}px;
  padding:{int(9*s)}px {int(20*s)}px;color:#fff;display:inline-block}}
.brand{{display:flex;align-items:center;gap:7px;font-size:{round(9.5*s,1)}px;
  color:rgba(255,255,255,.18);letter-spacing:.09em;text-transform:uppercase}}
.bot{{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:{int(10*s)}px}}
{layout_css}
</style></head><body>
<div class="wrap">
  <div class="grid"></div><div class="glow"></div>
  <div class="corner"></div><div class="lline"></div>
  {content}
</div></body></html>"""


def render_html(html, output, w, h):
    tmp = output.with_suffix(".tmp.html")
    tmp.write_text(html, encoding="utf-8")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            page = br.new_page(viewport={"width": w, "height": h})
            page.goto(f"file://{tmp.resolve()}", wait_until="networkidle")
            page.wait_for_timeout(2500)
            page.screenshot(path=str(output),
                            clip={"x": 0, "y": 0, "width": w, "height": h})
            br.close()
    finally:
        tmp.unlink(missing_ok=True)
    return output


def main():
    ap = argparse.ArgumentParser(description="gemini-brand-gen -- Universal Brand Asset Generator")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--prompt", metavar="TEXT",
        help="Natural language -> Gemini generates full spec")
    mode.add_argument("--title", metavar="TEXT", help="Main headline")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--badge", default="")
    ap.add_argument("--features", nargs="*", default=[], metavar="F")
    ap.add_argument("--price", default="")
    ap.add_argument("--type", default="cover", choices=ASSET_TYPES, dest="asset_type")
    ap.add_argument("--format", default="cover", choices=list(FORMATS.keys()))
    ap.add_argument("--output", type=Path, default=None)
    ap.add_argument("--brand", type=Path, default=None)
    ap.add_argument("--accent", default="")
    ap.add_argument("--bg", default="")
    ap.add_argument("--logo", default="")
    ap.add_argument("--no-gemini", action="store_true")
    ap.add_argument("--save-html", action="store_true")
    ap.add_argument("--list-formats", action="store_true")
    args = ap.parse_args()

    if args.list_formats:
        print(f"{'Format':<16} {'Size':<14} Description")
        print("-" * 58)
        for k, v in FORMATS.items():
            print(f"  {k:<14} {v['w']}x{v['h']:<9} {v['desc']}")
        return

    if not args.prompt and not args.title:
        ap.error("Provide --title TEXT or --prompt TEXT")

    env = load_env()
    api_key = env.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    if not api_key and not args.no_gemini:
        print("WARNING: GEMINI_API_KEY not found -- using fallback SVG")
        args.no_gemini = True

    brand = load_brand(args.brand, {"accent": args.accent or None,
                                    "bg": args.bg or None,
                                    "logo": args.logo or None})
    fmt = FORMATS[args.format]
    ts  = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.prompt and not args.no_gemini:
        print(f"  Spec via Gemini: {args.prompt!r}")
        spec     = gemini_spec(args.prompt, args.format, api_key)
        title    = spec.get("title", args.prompt[:40])
        subtitle = spec.get("subtitle", "")
        eyebrow  = spec.get("eyebrow", "")
        badge    = spec.get("badge", "")
        features = spec.get("features", [])[:5]
        price    = spec.get("price", "")
        atype    = spec.get("asset_type", args.asset_type)
        hero_hint = spec.get("hero_hint", title)
        print(f"  Title: {title}")
    else:
        title    = args.title or (args.prompt[:40] if args.prompt else "")
        subtitle = args.subtitle
        eyebrow  = args.eyebrow
        badge    = args.badge
        features = args.features
        price    = args.price
        atype    = args.asset_type
        hero_hint = title

    slug   = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
    output = args.output or (OUTPUT_DIR / f"{slug}-{args.format}-{ts}.png")

    print(f"\ngemini-brand-gen v1.0")
    print(f"  Brand:  {brand.get('name','?')}  accent={brand['accent']}")
    print(f"  Format: {args.format}  ({fmt['w']}x{fmt['h']})")
    print(f"  Title:  {title}")
    print(f"  Output: {output}")

    if args.no_gemini:
        svg = fallback_svg(brand["accent"])
        print("  SVG: fallback")
    else:
        print(f"  SVG via Gemini ({atype})...")
        svg = gemini_svg(hero_hint, subtitle, brand["accent"], atype, api_key)
        print(f"  SVG: {len(svg)} chars")

    html = build_html(brand, title, subtitle, features, price, svg,
                      args.format, badge, eyebrow)
    if args.save_html:
        html_out = output.with_suffix(".html")
        html_out.write_text(html, encoding="utf-8")
        print(f"  HTML: {html_out}")

    output.parent.mkdir(parents=True, exist_ok=True)
    print("  Rendering...")
    render_html(html, output, fmt["w"], fmt["h"])
    print(f"  Done! {output} ({output.stat().st_size // 1024} KB)\n")


if __name__ == "__main__":
    main()
