"""Maakt de HTML voor de brochure "De geschiedenis van de Dierense Toren" uit de
inhoud van geschiedenis.html, zodat de brochure gelijk blijft met de website.

Gebruik (vanuit de hoofdmap van de repository):
  python3 .github/scripts/brochure.py
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --no-pdf-header-footer --print-to-pdf=downloads/geschiedenis-dierense-toren.pdf brochure.html
  rm brochure.html qr-brochure.png

De QR-code (qr-brochure.png) moet naast brochure.html staan; zie BEHEER.md.
"""
import html
import re

s = open("geschiedenis.html", encoding="utf-8").read()


def strip(t):
    return re.sub(r"<[^>]+>", "", t).strip()


# Tijdlijn
items = []
for li in re.findall(r'<li class="tl-slide".*?</li>', s, re.S):
    img = re.search(r'<img src="(img/web/[^"?]+)\?v=dev" alt="([^"]*)"', li)
    cap = re.search(r"<figcaption>(.*?)</figcaption>", li)
    items.append({
        "year": re.search(r'<div class="year">(.*?)</div>', li).group(1),
        "title": re.search(r"<h3>(.*?)</h3>", li).group(1),
        "text": re.search(r"<p>(.*?)</p>", li, re.S).group(1),
        "img": img.group(1) if img else None,
        "alt": img.group(2) if img else "",
        "cap": cap.group(1) if cap else "",
    })

# Architect
arch = re.search(r'<section class="section[^"]*" id="architect">.*?<div class="prose">(.*?)</div>\s*</div>\s*</section>', s, re.S).group(1)
arch = re.sub(r"\s*\n\s*", "\n", arch).strip()

# In het kort
facts = re.search(r'<h2 class="mt-0">In het kort</h2>\s*<dl class="defs mt-2">(.*?)</dl>', s, re.S).group(1)
facts = re.sub(r'<a href="#architect">(.*?)</a>', r"\1", facts)
facts = re.sub(r'<a href="https://www\.monumenten\.nl[^"]*"[^>]*>(.*?)</a>', r"\1", facts)

tl_html = ""
for i, it in enumerate(items):
    fig = (f'<figure><img src="{it["img"]}" alt="{it["alt"]}">'
           + (f"<figcaption>{it['cap']}</figcaption>" if it["cap"] else "") + "</figure>") if it["img"] else ""
    side = "links" if i % 2 == 0 else "rechts"
    tl_html += (f'<article class="item {side}{"" if it["img"] else " zonder-foto"}">{fig}'
                f'<div class="tekst"><p class="jaar">{it["year"]}</p><h3>{it["title"]}</h3><p>{it["text"]}</p></div></article>\n')

page = f"""<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><title>De geschiedenis van de Dierense Toren</title>
<style>
@font-face {{ font-family: Fraunces; src: url("fonts/fraunces-latin.woff2") format("woff2"); font-weight: 500 600; }}
@font-face {{ font-family: Fraunces; src: url("fonts/fraunces-latin-ext.woff2") format("woff2"); font-weight: 500 600; unicode-range: U+0100-024F, U+1E00-1EFF; }}
@font-face {{ font-family: Inter; src: url("fonts/inter-latin.woff2") format("woff2"); font-weight: 400 700; }}
@font-face {{ font-family: Inter; src: url("fonts/inter-latin-ext.woff2") format("woff2"); font-weight: 400 700; unicode-range: U+0100-024F, U+1E00-1EFF; }}
@page {{ size: A4; margin: 18mm 18mm 20mm; @bottom-center {{ content: counter(page); font: 9pt Inter, sans-serif; color: #968e86; }} }}
@page :first {{ margin: 0; @bottom-center {{ content: none; }} }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{ font-family: Inter, sans-serif; color: #1f2328; font-size: 10.5pt; line-height: 1.55; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
h1, h2, h3 {{ font-family: Fraunces, serif; font-weight: 600; line-height: 1.15; margin: 0 0 3mm; }}
h2 {{ font-size: 22pt; color: #1f2328; }}
h3 {{ font-size: 13pt; }}
p {{ margin: 0 0 3mm; }}
.eyebrow {{ font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; color: #9a3b22; margin: 0 0 2mm; }}
.cover {{ height: 297mm; position: relative; background: #2b2a2e url("img/web/toren-voorkant.jpg") center 30% / cover; color: #fff; page-break-after: always; }}
.cover::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,18,22,.15) 30%, rgba(20,18,22,.85) 100%); }}
.cover .in {{ position: absolute; left: 20mm; right: 20mm; bottom: 26mm; z-index: 1; }}
.cover .eyebrow {{ color: #f2c27a; font-size: 10pt; }}
.cover h1 {{ font-size: 44pt; line-height: 1.02; margin-bottom: 6mm; }}
.cover p {{ font-size: 12pt; max-width: 120mm; color: rgba(255,255,255,.92); }}
.cover .bron {{ margin-top: 10mm; font-size: 9pt; color: rgba(255,255,255,.75); }}
.inleiding {{ page-break-after: always; }}
.inleiding .lead {{ font-size: 12.5pt; color: #4a4f57; margin-bottom: 8mm; }}
dl {{ display: grid; grid-template-columns: 36mm 1fr; gap: 2.2mm 6mm; margin: 0; }}
dt {{ font-weight: 600; }}
dd {{ margin: 0; color: #2c3036; }}
.item {{ padding: 6mm 0; border-top: 1px solid #e6e0d6; }}
.item figure, .item .jaar, .item h3 {{ break-inside: avoid; break-after: avoid; page-break-after: avoid; }}
.item p {{ orphans: 3; widows: 3; }}
.item figure {{ margin: 0 0 3mm; }}
.item img {{ display: block; width: auto; max-width: 100%; max-height: 62mm; border-radius: 2mm; }}
.item figcaption {{ font-size: 8pt; color: #4a4f57; margin-top: 1.5mm; line-height: 1.35; }}
.jaar {{ font-family: Fraunces, serif; font-weight: 600; font-size: 15pt; color: #9a3b22; margin: 0 0 1mm; }}
.item p {{ color: #2c3036; font-size: 10pt; }}
.architect {{ page-break-before: always; }}
.architect blockquote {{ margin: 4mm 0 5mm; padding: 1mm 0 1mm 5mm; border-left: 1mm solid #c8891f; font-family: Fraunces, serif; font-style: italic; font-size: 11.5pt; }}
.architect h3 {{ margin-top: 5mm; }}
.slot {{ page-break-before: always; display: grid; grid-template-columns: 1fr 42mm; gap: 10mm; align-items: start; }}
.slot img.qr {{ width: 42mm; height: 42mm; image-rendering: pixelated; }}
.slot .qr-tekst {{ font-size: 8.5pt; color: #4a4f57; text-align: center; margin-top: 2mm; }}
.kader {{ background: #9a3b22; color: #fff; border-radius: 3mm; padding: 7mm; margin-top: 6mm; }}
.kader h3 {{ color: #fff; }}
.kader p {{ color: rgba(255,255,255,.92); margin: 0 0 2mm; }}
.colofon {{ margin-top: 10mm; font-size: 8.5pt; color: #4a4f57; }}
</style></head><body>

<section class="cover"><div class="in">
  <p class="eyebrow">Monument in Dieren sinds 1925</p>
  <h1>De geschiedenis van de Dierense Toren</h1>
  <p>Van de stichting van de parochie in de twaalfde eeuw tot het eeuwfeest in 2025: het verhaal van een toren die bleef staan.</p>
  <p class="bron">Stichting De Dierense Toren &middot; dierensetoren.nl</p>
</div></section>

<section class="inleiding">
  <p class="eyebrow">Inleiding</p>
  <h2>Een toren die het dorp niet wilde missen</h2>
  <p class="lead">De Dierense Toren werd in 1925 gebouwd bij de rooms-katholieke kerk aan de Hogestraat. Toen de kerk in 1977 werd gesloopt, bleef de toren staan dankzij de inzet van de Dierense bevolking. Sinds 1987 is hij gerestaureerd en herbestemd, en nog altijd bepaalt hij het silhouet van Dieren.</p>
  <h3>In het kort</h3>
  <dl>{facts}</dl>
</section>

<section class="tijdlijn">
  <p class="eyebrow">Tijdlijn</p>
  <h2>Van de 12e eeuw tot nu</h2>
  {tl_html}
</section>

<section class="architect">
  <p class="eyebrow">De architect</p>
  <h2>Wolter te Riele (1867&ndash;1937)</h2>
  {arch}
</section>

<section class="slot">
  <div>
    <p class="eyebrow">Meer weten</p>
    <h2>De toren bezoeken en steunen</h2>
    <p>De Dierense Toren staat aan de Hogestraat 12 in Dieren, op ongeveer vijf minuten lopen van station Dieren. Bij de toren is een eigen, rolstoeltoegankelijke parkeerplaats. Tijdens Open Monumentendag is de toren te beklimmen; elke zaterdag om 18.00 uur luiden de klokken.</p>
    <p>Heeft u oude foto&rsquo;s of verhalen over de kerk of de toren? De stichting hoort ze graag via info@dierensetoren.nl.</p>
    <div class="kader">
      <h3>Help de toren nog 100 jaar te laten staan</h3>
      <p>Stichting De Dierense Toren is een culturele ANBI en wordt volledig gedragen door vrijwilligers en donateurs. Donateur worden kan al vanaf &euro;&nbsp;5 per jaar.</p>
      <p>IBAN NL10 INGB 0006 4931 17 t.n.v. Stichting De Dierense Toren</p>
    </div>
    <p class="colofon">Stichting De Dierense Toren &middot; Hogestraat 12, 6953 AS Dieren &middot; info@dierensetoren.nl &middot; KvK 41048726 &middot; RSIN 008408063<br>Teksten en beelden: website dierensetoren.nl. Deze brochure geeft een impressie van het boekje over de geschiedenis van de Dierense Toren, dat bij de stichting te bestellen is.</p>
  </div>
  <div><img class="qr" src="qr-brochure.png" alt="QR-code naar dierensetoren.nl"><p class="qr-tekst">Scan voor de website</p></div>
</section>
</body></html>
"""
open("brochure.html", "w", encoding="utf-8").write(page)
print(f"brochure.html: {len(items)} tijdlijnitems")
