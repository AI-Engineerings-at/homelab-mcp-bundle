#!/usr/bin/env python3
"""Patch cover-v2-n8n-test.html with layout improvements."""

SRC = "/home/joe/cli_bridge/products/cover-templates/cover-v2-n8n-test.html"
DST = SRC

with open(SRC, "r") as f:
    html = f.read()

# 1. Eagle-BG: größer + weiter nach unten
html = html.replace("width: 490px; height: 490px;", "width: 490px; height: 490px;")  # bereits geändert via sed

# 4. Brand-name: logo-style CSS hinzufügen
old_brand = "  .brand-name {\n    font-size: 12px; font-weight: 700; color: #475569;\n    letter-spacing: 1.5px; text-transform: uppercase;\n  }"
new_brand = """  .brand-logo-img {
    width: 26px; height: 26px; object-fit: contain;
    filter: drop-shadow(0 0 8px rgba(251,146,60,0.5));
    flex-shrink: 0;
  }
  .brand-name {
    font-size: 11px; font-weight: 800; color: #FB923C;
    letter-spacing: 2px; text-transform: uppercase;
    font-family: 'Courier New', monospace;
  }"""
if old_brand in html:
    html = html.replace(old_brand, new_brand)
    print("✓ brand-name CSS patched")
else:
    print("✗ brand-name CSS not found!")

# 5. brand-mid CSS einfügen vor /* STATS */
brand_mid_css = """  /* BRAND MID — visible between product image and stats */
  .brand-mid {
    position: relative; z-index: 20;
    display: flex; align-items: center; justify-content: center;
    gap: 8px;
    padding: 5px 0 3px;
    flex-shrink: 0;
  }
  .brand-mid-img {
    width: 18px; height: 18px; object-fit: contain;
    filter: drop-shadow(0 0 6px rgba(251,146,60,0.5));
  }
  .brand-mid-name {
    font-size: 10px; font-weight: 700;
    color: #FB923C;
    letter-spacing: 2.5px; text-transform: uppercase;
    font-family: 'Courier New', monospace;
  }
"""
if "  /* STATS */" in html:
    html = html.replace("  /* STATS */", brand_mid_css + "  /* STATS */")
    print("✓ brand-mid CSS inserted")
else:
    print("✗ /* STATS */ marker not found!")

# 6. Brand div: img tag hinzufügen
old_brand_div = '<div class="brand">\n      <span class="brand-name">ai-engineering.at</span>'
new_brand_div = '<div class="brand">\n      <img class="brand-logo-img" id="brlogoA" src="" alt="AI Engineering">\n      <span class="brand-name">ai-engineering.at</span>'
if old_brand_div in html:
    html = html.replace(old_brand_div, new_brand_div)
    print("✓ brand img tag added")
else:
    print("✗ brand div not found!")

# 7. brand-mid div zwischen visual und stats
old_stats = '\n  <div class="stats">'
new_stats = '\n  <div class="brand-mid"><img class="brand-mid-img" id="brlogoB" src="" alt=""><span class="brand-mid-name">ai-engineering.at</span></div>\n  <div class="stats">'
if old_stats in html:
    html = html.replace(old_stats, new_stats)
    print("✓ brand-mid div inserted before stats")
else:
    print("✗ stats div not found!")

# 8. JS für Logo-Kopie
js_inject = """<script>
(function(){
  var eImg = document.querySelector('.eagle-bg img');
  if(eImg){
    var src = eImg.src;
    var a = document.getElementById('brlogoA');
    var b = document.getElementById('brlogoB');
    if(a) a.src = src;
    if(b) b.src = src;
  }
})();
</script>
</body>"""
if "</body>" in html:
    html = html.replace("</body>", js_inject)
    print("✓ JS injected")
else:
    print("✗ </body> not found!")

with open(DST, "w") as f:
    f.write(html)
print(f"\nSaved: {DST}")
