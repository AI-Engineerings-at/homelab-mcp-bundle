#!/usr/bin/env python3
"""Cover v4 - Slideworks-style mit ECHTEN Produkt-Screenshots."""
import base64, asyncio, sys
from pathlib import Path

BASE = Path(__file__).parent
ROOT = BASE.parent.parent
TMP  = Path("/tmp")

def b64(path):
    p = Path(path)
    if not p.exists():
        print(f"  WARN: {path} fehlt")
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQAABjE+ibYAAAAASUVORK5CYII="
    data = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{data}"

def logo():
    for c in [ROOT/"lead-magnet"/"logo-new.png",
              Path("/home/joe/phantom-ai/landing-page/public/eagle-logo.png")]:
        if c.exists(): return b64(str(c))
    return ""

def cover_wide(product_name,subtitle,price,category,features,accent,imgs,img_aspect,**k):
    i = [b64(p) for p in imgs[:3]]
    while len(i)<3: i.append(i[-1])
    L = logo()
    lt = f'<img src="{L}" alt="">' if L else ""
    fh = "".join(f'<span class="feat">✓ {f}</span>' for f in features[:4])
    if img_aspect=="portrait":
        fan = """
        .ss{position:absolute;right:25px;top:50%;transform:translateY(-50%);width:650px;height:540px;}
        .sh{position:absolute;border-radius:7px;overflow:hidden;
          box-shadow:0 18px 55px rgba(0,0,0,.78);border:2px solid rgba(255,255,255,.07);}
        .sh img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;}
        .s1{width:228px;height:322px;right:12px;top:82px;transform:rotate(9deg);z-index:1;}
        .s2{width:228px;height:322px;right:152px;top:52px;transform:rotate(2deg);z-index:2;}
        .s3{width:228px;height:322px;right:292px;top:92px;transform:rotate(-6deg);z-index:3;}"""
    else:
        fan = """
        .ss{position:absolute;right:18px;top:50%;transform:translateY(-50%);width:680px;height:540px;}
        .sh{position:absolute;border-radius:8px;overflow:hidden;
          box-shadow:0 18px 55px rgba(0,0,0,.78);border:2px solid rgba(255,255,255,.07);}
        .sh img{width:100%;height:100%;object-fit:cover;object-position:top left;display:block;}
        .s1{width:428px;height:255px;right:0;top:200px;transform:rotate(5deg);z-index:1;}
        .s2{width:428px;height:255px;right:48px;top:112px;transform:rotate(1deg);z-index:2;}
        .s3{width:428px;height:255px;right:96px;top:22px;transform:rotate(-4deg);z-index:3;}"""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=1280">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:720px;overflow:hidden;background:#090E1C;
  font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#F8FAFC}}
.cv{{width:1280px;height:720px;position:relative;overflow:hidden;
  background:linear-gradient(135deg,#090E1C 0%,#0C1428 45%,#070B16 100%)}}
.cv::before{{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 780px 580px at 27% 50%,{accent}1C 0%,transparent 68%);z-index:0}}
.lft{{position:absolute;left:0;top:0;width:558px;height:720px;
  display:flex;flex-direction:column;justify-content:center;
  padding:58px 42px 58px 56px;z-index:10}}
.br{{display:flex;align-items:center;gap:10px;margin-bottom:24px}}
.br img{{width:26px;height:26px;object-fit:contain;opacity:.62}}
.bn{{font-size:10px;font-weight:700;color:#3A4C64;letter-spacing:2.5px;text-transform:uppercase}}
.ct{{display:inline-flex;background:{accent}1E;border:1px solid {accent}4E;
  color:{accent};font-size:11px;font-weight:700;
  padding:5px 14px;border-radius:3px;letter-spacing:2px;text-transform:uppercase;
  margin-bottom:20px;width:fit-content}}
h1{{font-size:49px;font-weight:800;line-height:1.09;color:#EFF3F8;
  margin-bottom:13px;letter-spacing:-1.5px}}
h1 em{{font-style:normal;color:{accent}}}
.sub{{font-size:16px;color:#5D738C;line-height:1.55;margin-bottom:28px;max-width:408px}}
.pr{{font-size:42px;font-weight:800;color:{accent};margin-bottom:24px}}
.fs{{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:36px}}
.feat{{background:#101828;border:1px solid #1A2840;color:#7A95B0;
  font-size:12px;font-weight:500;padding:5px 12px;border-radius:5px}}
.ft{{font-size:11px;color:#2B3C52;letter-spacing:2px;text-transform:uppercase}}
.dv{{position:absolute;left:546px;top:68px;bottom:68px;width:1px;
  background:linear-gradient(to bottom,transparent,{accent}26,transparent);z-index:5}}
{fan}
.vr{{position:absolute;right:0;top:0;width:88px;height:720px;
  background:linear-gradient(to right,transparent,#090E1C);z-index:20}}
.vl{{position:absolute;left:518px;top:0;width:68px;height:720px;
  background:linear-gradient(to left,transparent,#090E1C68);z-index:8}}
</style></head><body>
<div class="cv">
  <div class="dv"></div>
  <div class="lft">
    <div class="br">{lt}<span class="bn">AI Engineering</span></div>
    <div class="ct">{category}</div>
    <h1>{product_name}</h1>
    <p class="sub">{subtitle}</p>
    <div class="pr">{price}</div>
    <div class="fs">{fh}</div>
    <div class="ft">ai-engineering.at</div>
  </div>
  <div class="ss">
    <div class="sh s1"><img src="{i[0]}"></div>
    <div class="sh s2"><img src="{i[1]}"></div>
    <div class="sh s3"><img src="{i[2]}"></div>
  </div>
  <div class="vr"></div><div class="vl"></div>
</div></body></html>"""

def cover_sq(product_name,subtitle,price,category,features,accent,imgs,img_aspect,**k):
    i = [b64(p) for p in imgs[:3]]
    while len(i)<3: i.append(i[-1])
    L = logo()
    lt = f'<img src="{L}" alt="">' if L else ""
    fh = "".join(f'<span class="feat">✓ {f}</span>' for f in features[:4])
    if img_aspect=="portrait":
        fan = """
        .ss{position:relative;width:600px;height:295px;overflow:hidden;}
        .sh{position:absolute;border-radius:5px;overflow:hidden;
          box-shadow:0 13px 38px rgba(0,0,0,.78);border:2px solid rgba(255,255,255,.07);}
        .sh img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;}
        .s1{width:153px;height:218px;right:52px;top:28px;transform:rotate(8deg);z-index:1;}
        .s2{width:153px;height:218px;right:158px;top:14px;transform:rotate(2deg);z-index:2;}
        .s3{width:153px;height:218px;right:264px;top:38px;transform:rotate(-6deg);z-index:3;}"""
    else:
        fan = """
        .ss{position:relative;width:600px;height:295px;overflow:hidden;}
        .sh{position:absolute;border-radius:6px;overflow:hidden;
          box-shadow:0 13px 38px rgba(0,0,0,.78);border:2px solid rgba(255,255,255,.07);}
        .sh img{width:100%;height:100%;object-fit:cover;object-position:top left;display:block;}
        .s1{width:286px;height:192px;right:18px;top:68px;transform:rotate(6deg);z-index:1;}
        .s2{width:286px;height:192px;right:88px;top:36px;transform:rotate(1deg);z-index:2;}
        .s3{width:286px;height:192px;right:158px;top:10px;transform:rotate(-5deg);z-index:3;}"""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=600">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:600px;height:600px;overflow:hidden;background:#090E1C;
  font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#F8FAFC}}
.cv{{width:600px;height:600px;position:relative;overflow:hidden;
  background:linear-gradient(160deg,#090E1C 0%,#0C1428 55%,#070B16 100%);
  display:flex;flex-direction:column}}
.cv::before{{content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 500px 340px at 50% 24%,{accent}18 0%,transparent 70%);z-index:0}}
.top{{position:relative;z-index:10;flex:0 0 auto;padding:26px 30px 16px}}
.br{{display:flex;align-items:center;gap:8px;margin-bottom:13px}}
.br img{{width:20px;height:20px;object-fit:contain;opacity:.6}}
.bn{{font-size:9px;font-weight:700;color:#3A4C64;letter-spacing:2.5px;text-transform:uppercase}}
.ct{{display:inline-flex;background:{accent}1E;border:1px solid {accent}4E;
  color:{accent};font-size:10px;font-weight:700;
  padding:4px 12px;border-radius:3px;letter-spacing:2px;text-transform:uppercase;margin-bottom:11px}}
h1{{font-size:31px;font-weight:800;line-height:1.1;color:#EFF3F8;margin-bottom:6px}}
h1 em{{font-style:normal;color:{accent}}}
.sub{{font-size:12px;color:#5D738C;margin-bottom:11px;line-height:1.45}}
.pr{{font-size:29px;font-weight:800;color:{accent};margin-bottom:9px}}
.fs{{display:flex;flex-wrap:wrap;gap:5px}}
.feat{{background:#101828;border:1px solid #1A2840;color:#7A95B0;
  font-size:10px;padding:3px 9px;border-radius:4px}}
.bot{{position:relative;z-index:10;flex:1;overflow:hidden}}
{fan}
.vb{{position:absolute;bottom:31px;left:0;right:0;height:52px;
  background:linear-gradient(to bottom,transparent,#090E1C58);z-index:25}}
.bar{{position:absolute;bottom:0;left:0;right:0;height:31px;
  background:{accent}13;border-top:1px solid {accent}26;
  display:flex;align-items:center;padding:0 18px;z-index:30}}
.bar span{{font-size:10px;color:#3A4C64;letter-spacing:2px;text-transform:uppercase}}
</style></head><body>
<div class="cv">
  <div class="top">
    <div class="br">{lt}<span class="bn">AI Engineering</span></div>
    <div class="ct">{category}</div>
    <h1>{product_name}</h1>
    <p class="sub">{subtitle}</p>
    <div class="pr">{price}</div>
    <div class="fs">{fh}</div>
  </div>
  <div class="bot">
    <div class="ss">
      <div class="sh s1"><img src="{i[0]}"></div>
      <div class="sh s2"><img src="{i[1]}"></div>
      <div class="sh s3"><img src="{i[2]}"></div>
    </div>
    <div class="vb"></div>
    <div class="bar"><span>ai-engineering.at</span></div>
  </div>
</div></body></html>"""

PRODUCTS = {
  "n8n": {"fn":cover_wide,"size":(1280,720),
    "product_name":"n8n Starter<br><em>Bundle</em>",
    "subtitle":"5 Production-Ready Workflows für deine AI-Automation",
    "price":"EUR 29","category":"n8n Automation",
    "features":["5 Workflows","Stripe & Gumroad","AI Pipeline","Video-Tutorial"],
    "accent":"#FB923C","imgs":[str(ROOT/"n8n-dashboard-dark.png"),str(ROOT/"n8n-aiops-alert-pipeline.png"),str(ROOT/"n8n-rapidmail-doi-download.png")],
    "img_aspect":"landscape","output":"cover-v4-n8n-1280x720.png"},
  "playbook": {"fn":cover_wide,"size":(1280,720),
    "product_name":"Der Lokale<br><em>AI-Stack</em>",
    "subtitle":"DSGVO-konformer AI-Server in 7 Tagen — 8 Kapitel, Schritt für Schritt",
    "price":"EUR 49","category":"Playbook",
    "features":["8 Kapitel","Ollama + GPU","n8n Integration","DSGVO-konform"],
    "accent":"#10B981","imgs":[str(TMP/"playbook-page-001.png"),str(TMP/"playbook2-002.png"),str(TMP/"playbook2-003.png")],
    "img_aspect":"portrait","output":"cover-v4-playbook-1280x720.png"},
  "dsgvo": {"fn":cover_wide,"size":(1280,720),
    "product_name":"DSGVO Art.30<br><em>Compliance Kit</em>",
    "subtitle":"6 sofort ausfüllbare Templates für AI-Unternehmen",
    "price":"EUR 79","category":"DSGVO Compliance",
    "features":["6 Templates","Art. 30 konform","DPIA inkl.","Sofort einsetzbar"],
    "accent":"#C084FC","imgs":[str(TMP/"dsgvo-page-1.png"),str(TMP/"dsgvo2-2.png"),str(TMP/"dsgvo2-3.png")],
    "img_aspect":"portrait","output":"cover-v4-dsgvo-1280x720.png"},
  "grafana": {"fn":cover_sq,"size":(600,600),
    "product_name":"Grafana<br><em>Dashboard Pack</em>",
    "subtitle":"6 Production-Ready Homelab & DevOps Dashboards",
    "price":"EUR 39","category":"Grafana Monitoring",
    "features":["6 Dashboards","Proxmox VE","Docker Swarm","Node Exporter"],
    "accent":"#60A5FA","imgs":[str(ROOT/"grafana-node-exporter-full.png"),str(ROOT/"grafana-docker-swarm.png"),str(ROOT/"grafana-infra-overview.png")],
    "img_aspect":"landscape","output":"cover-v4-grafana-600x600.png"},
  "blueprint-sq": {"fn":cover_sq,"size":(600,600),
    "product_name":"AI Agent Team<br><em>Blueprint</em>",
    "subtitle":"Dein autonomes Multi-Agent-Team in 2 Stunden",
    "price":"EUR 19","category":"AI Agents",
    "features":["11 Dateien","Multi-Agent","Mattermost","n8n Integration"],
    "accent":"#4ADE80","imgs":[str(TMP/"blueprint-page-1.png"),str(TMP/"blueprint2-2.png"),str(TMP/"blueprint2-3.png")],
    "img_aspect":"portrait","output":"cover-v4-blueprint-600x600.png"},
  "blueprint-wide": {"fn":cover_wide,"size":(1280,720),
    "product_name":"AI Agent Team<br><em>Blueprint</em>",
    "subtitle":"Dein autonomes Multi-Agent-Team in 2 Stunden — 11 Dateien, sofort einsetzbar",
    "price":"EUR 19","category":"AI Agents",
    "features":["11 Dateien","Multi-Agent Setup","Mattermost","n8n Automation"],
    "accent":"#4ADE80","imgs":[str(TMP/"blueprint-page-1.png"),str(TMP/"blueprint2-2.png"),str(TMP/"blueprint2-3.png")],
    "img_aspect":"portrait","output":"cover-v4-blueprint-1280x720.png"},
}

async def render_all(targets=None):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        items = [(k,v) for k,v in PRODUCTS.items() if targets is None or k in targets]
        for key,prod in items:
            print(f"\n[{key}] → {prod['output']}")
            html = prod["fn"](**{k:v for k,v in prod.items() if k not in("fn","size","output")})
            tmp = BASE/f"_tmp_{key}.html"
            tmp.write_text(html,encoding="utf-8")
            w,h = prod["size"]
            page = await browser.new_page(viewport={"width":w,"height":h})
            await page.goto(f"file://{tmp}",wait_until="networkidle")
            await page.wait_for_timeout(600)
            out = BASE/prod["output"]
            await page.screenshot(path=str(out),clip={"x":0,"y":0,"width":w,"height":h})
            await page.close()
            tmp.unlink(missing_ok=True)
            print(f"  ✅ {out.name} ({w}x{h}, {out.stat().st_size//1024}KB)")
        await browser.close()
    print("\n✅ Alle Covers fertig!")

if __name__=="__main__":
    asyncio.run(render_all(sys.argv[1:] or None))
