"""Maakt de HTML voor het werkblad "Speurtocht: de Dierense Toren" (groep 6-8).
De tekening van de toren en de stijl ervan komen uit geschiedenis.html en
css/site.css, zodat het werkblad gelijk blijft met de website.

Gebruik (vanuit de hoofdmap van de repository):
  python3 .github/scripts/werkblad.py
  python3 -m http.server 8765 &
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --no-pdf-header-footer --print-to-pdf=downloads/werkblad-dierense-toren.pdf \
    http://localhost:8765/werkblad.html
  kill %1; rm werkblad.html
"""
import random
import re

s = open("geschiedenis.html", encoding="utf-8").read()
css = open("css/site.css", encoding="utf-8").read()

# Tekening van de toren en de bijbehorende stijl
svg = re.search(r'<svg class="toren-tekening".*?</svg>', s, re.S).group(0)
svg = svg.replace('id="toren-titel"', 'id="w-titel"').replace('id="toren-desc"', 'id="w-desc"').replace("toren-titel toren-desc", "w-titel w-desc")
root = re.search(r":root \{.*?\}", css, re.S).group(0)
svg_css = "\n".join(l for l in css.splitlines() if l.startswith(".toren-tekening "))

# Woordzoeker
WOORDEN = ["TOREN", "SPITS", "KLOKKEN", "WINDHAAN", "GALMGAT", "UURWERK", "DIEREN", "MONUMENT", "KERK", "KRUIS"]
N = 12
rnd = random.Random(1925)
raster = [[None] * N for _ in range(N)]
richtingen = [(0, 1), (1, 0), (1, 1)]
for w in sorted(WOORDEN, key=len, reverse=True):
    for _ in range(1000):
        dr, dc = rnd.choice(richtingen)
        r = rnd.randrange(N - dr * (len(w) - 1))
        c = rnd.randrange(N - dc * (len(w) - 1))
        vakjes = [(r + i * dr, c + i * dc) for i in range(len(w))]
        if all(raster[y][x] in (None, w[i]) for i, (y, x) in enumerate(vakjes)):
            for i, (y, x) in enumerate(vakjes):
                raster[y][x] = w[i]
            break
    else:
        raise SystemExit(f"{w} past niet in de woordzoeker")
LETTERS = "ABDEGHIKLMNOPRSTUVWZ"
woordzoeker = "".join("<tr>" + "".join(f"<td>{ch or rnd.choice(LETTERS)}</td>" for ch in rij) + "</tr>" for rij in raster)

# Tijdlijn: jaartallen op volgorde, gebeurtenissen door elkaar
tijdlijn = [
    ("1895", "De katholieke kerk aan de Hogestraat wordt gebouwd"),
    ("1925", "De toren wordt ingewijd"),
    ("1943", "De Duitsers nemen de klokken mee"),
    ("1948", "Er komen drie nieuwe klokken"),
    ("1987", "De toren is opgeknapt en gaat weer open"),
    ("2025", "De toren bestaat 100 jaar"),
]
volgorde = [4, 2, 5, 0, 3, 1]
letters = "ABCDEF"
tl_jaren = "".join(f'<li><span class="jaar">{j}</span><span class="stip"></span></li>' for j, _ in tijdlijn)
tl_feiten = "".join(f'<li><span class="stip"></span><b>{letters[i]}</b> {tijdlijn[k][1]}</li>' for i, k in enumerate(volgorde))
tl_antwoord = ", ".join(f"{tijdlijn[k][0]} = {letters[i]}" for k in range(6) for i in range(6) if volgorde[i] == k)

lijnen = lambda n: '<div class="lijn"></div>' * n

page = f"""<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><title>Werkblad: de Dierense Toren</title>
<style>
@font-face {{ font-family: Fraunces; src: url("fonts/fraunces-latin.woff2") format("woff2"); font-weight: 500 600; }}
@font-face {{ font-family: Fraunces; src: url("fonts/fraunces-latin-ext.woff2") format("woff2"); font-weight: 500 600; unicode-range: U+0100-024F, U+1E00-1EFF; }}
@font-face {{ font-family: Inter; src: url("fonts/inter-latin.woff2") format("woff2"); font-weight: 400 700; }}
@font-face {{ font-family: Inter; src: url("fonts/inter-latin-ext.woff2") format("woff2"); font-weight: 400 700; unicode-range: U+0100-024F, U+1E00-1EFF; }}
{root}
{svg_css}
@page {{ size: A4; margin: 14mm 16mm 16mm; @bottom-center {{ content: "Stichting De Dierense Toren \\00b7  dierensetoren.nl \\00b7  vrij te kopi\\00eb ren voor gebruik in de klas"; font: 8pt Inter, sans-serif; color: #968e86; }} @bottom-right {{ content: counter(page); font: 8pt Inter, sans-serif; color: #968e86; }} }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{ font-family: Inter, sans-serif; color: #1f2328; font-size: 11.5pt; line-height: 1.5; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
h1, h2, h3 {{ font-family: Fraunces, serif; font-weight: 600; line-height: 1.15; margin: 0; }}
h1 {{ font-size: 22pt; }}
h2 {{ font-size: 15pt; margin: 0 0 2.5mm; display: flex; align-items: center; gap: 3mm; }}
h2 .nr {{ flex: none; width: 8mm; height: 8mm; border-radius: 50%; background: #9a3b22; color: #fff; font: 600 11pt Inter, sans-serif; display: grid; place-items: center; }}
p {{ margin: 0 0 2.5mm; }}
.blad {{ page-break-after: always; }}
.blad:last-child {{ page-break-after: auto; }}
.kop {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid #9a3b22; padding-bottom: 3mm; margin-bottom: 5mm; }}
.kop .eyebrow {{ font-size: 8.5pt; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; color: #9a3b22; margin: 0 0 1mm; }}
.naam {{ font-size: 10pt; color: #4a4f57; text-align: right; line-height: 2.2; }}
.naam span {{ display: inline-block; width: 38mm; border-bottom: 1px solid #4a4f57; }}
.lees {{ display: grid; grid-template-columns: 1fr 44mm; gap: 6mm; background: #f3ece1; border-radius: 3mm; padding: 4mm 5mm; margin-bottom: 5mm; }}
.lees p {{ font-size: 10.5pt; margin-bottom: 2mm; }}
.lees p:last-child {{ margin: 0; }}
.lees figure {{ margin: 0; }}
.lees img {{ width: 100%; border-radius: 2mm; display: block; }}
.lees figcaption {{ font-size: 7pt; color: #4a4f57; margin-top: 1mm; }}
.opdracht {{ margin-bottom: 5mm; break-inside: avoid; }}
.vragen {{ margin: 0; padding-left: 6mm; }}
.vragen li {{ margin-bottom: 2mm; }}
.lijn {{ border-bottom: 1px solid #b9b2a8; height: 7.5mm; }}
.tijdlijn {{ display: grid; grid-template-columns: 30mm 1fr; gap: 0 22mm; }}
.tijdlijn ul {{ list-style: none; margin: 0; padding: 0; }}
.tijdlijn li {{ height: 9mm; display: flex; align-items: center; gap: 3mm; }}
.tijdlijn .jaar {{ font: 600 14pt Fraunces, serif; color: #9a3b22; width: 18mm; }}
.stip {{ width: 3mm; height: 3mm; border-radius: 50%; background: #1f2328; flex: none; }}
.tekenen {{ display: grid; grid-template-columns: 58mm 1fr; gap: 8mm; align-items: center; }}
.tekenen .toren-tekening {{ max-height: 118mm; }}
.woordbank {{ border: 1.5px dashed #c8891f; border-radius: 3mm; padding: 3mm 4mm; margin: 0 0 4mm; font-size: 10.5pt; }}
.invul {{ list-style: none; margin: 0; padding: 0; }}
.invul li {{ display: flex; align-items: flex-end; gap: 3mm; height: 9.5mm; }}
.invul b {{ width: 7mm; height: 7mm; border-radius: 50%; background: #9a3b22; color: #fff; display: grid; place-items: center; font-size: 10pt; flex: none; }}
.invul span {{ flex: 1; border-bottom: 1px solid #b9b2a8; height: 7mm; }}
.pittig {{ font-size: 8pt; font-weight: 600; color: #fff; background: #c8891f; border-radius: 99px; padding: .3mm 2mm; margin-left: 1.5mm; vertical-align: 1px; }}
.zoek {{ display: grid; grid-template-columns: auto 1fr; gap: 8mm; align-items: start; }}
.zoek table {{ border-collapse: collapse; }}
.zoek td {{ width: 6mm; height: 6mm; text-align: center; font: 600 11pt Inter, sans-serif; border: 1px solid #e6e0d6; }}
.zoek ul {{ list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 8mm; font-size: 10.5pt; line-height: 1.9; }}
.zoek ul li::before {{ content: ""; display: inline-block; width: 3.2mm; height: 3.2mm; border: 1.2px solid #4a4f57; border-radius: .8mm; margin-right: 2mm; vertical-align: -.4mm; }}
.vak {{ border: 1.5px solid #b9b2a8; border-radius: 3mm; height: 30mm; }}
.antwoorden h2 {{ margin-top: 3mm; font-size: 13pt; }}
.antwoorden {{ font-size: 10.5pt; }}
.zoek-antwoord td {{ width: 5.2mm; height: 5.2mm; font-size: 8.5pt; }}
.antwoorden ol {{ margin: 0 0 3mm; padding-left: 6mm; }}
.antwoorden li {{ margin-bottom: 1.5mm; }}
.zoek-antwoord td.raak {{ background: #f2c27a; }}
</style></head><body>

<section class="blad">
  <div class="kop">
    <div><p class="eyebrow">Werkblad groep 6, 7 en 8</p><h1>Speurtocht: de Dierense Toren</h1></div>
    <div class="naam">Naam: <span></span><br>Groep: <span></span></div>
  </div>

  <div class="lees">
    <div>
      <p>Midden in Dieren, aan de Hogestraat, staat een hoge bakstenen toren met een spitse punt. Dat is de Dierense Toren. Hij werd gebouwd in 1924 en 1925, naast de katholieke kerk die daar al sinds 1895 stond. Architect Wolter te Riele maakte het ontwerp. Op 17 mei 1925 werd de toren ingewijd.</p>
      <p>In de Tweede Wereldoorlog, in 1943, namen de Duitsers de klokken mee. In 1948 kwamen er drie nieuwe klokken. Die luiden nog steeds, elke zaterdag om 18.00 uur.</p>
      <p>In de jaren zeventig werd de kerk afgebroken. Ook de toren dreigde te verdwijnen. Maar veel mensen in Dieren wilden hun toren houden. Een groep inwoners, het Comit&eacute; K12, kwam in actie, en dat lukte: de toren bleef staan. In 1987 was hij helemaal opgeknapt. Er kwamen kantoren en een vergaderruimte in, en boven bij de klokken een uitkijkpunt.</p>
      <p>Nu is de toren een monument. Vrijwilligers zorgen ervoor dat hij mooi blijft. In 2025 bestond hij 100 jaar.</p>
    </div>
    <figure><img src="img/web/toren-hogestraat-2008.jpg" alt="De Dierense Toren aan de Hogestraat"><figcaption>Foto: Anton van Daal (CC BY-NC 3.0)</figcaption></figure>
  </div>

  <div class="opdracht">
    <h2><span class="nr">1</span>Lees de tekst en beantwoord de vragen</h2>
    <ol class="vragen">
      <li>Aan welke straat staat de toren?{lijnen(1)}</li>
      <li>Wie maakte het ontwerp van de toren?{lijnen(1)}</li>
      <li>Wat gebeurde er in 1943 met de klokken?{lijnen(1)}</li>
      <li>Op welke dag en hoe laat luiden de klokken?{lijnen(1)}</li>
      <li>De kerk is afgebroken. Waarom staat de toren er nog wel?{lijnen(2)}</li>
    </ol>
  </div>
</section>

<section class="blad">
  <div class="opdracht">
    <h2><span class="nr">2</span>Tijdlijn</h2>
    <p>Trek een lijn van elk jaartal naar wat er in dat jaar gebeurde.</p>
    <div class="tijdlijn"><ul>{tl_jaren}</ul><ul>{tl_feiten}</ul></div>
  </div>

  <div class="opdracht">
    <h2><span class="nr">3</span>Wat zie je aan de toren?</h2>
    <div class="tekenen">
      {svg}
      <div>
        <p>Schrijf bij elk nummer wat het is. Kies uit de woorden in het kader.</p>
        <p class="woordbank">galmgaten &middot; de voet met steunberen &middot; kruis en windhaan &middot; kantoren en vergaderruimte &middot; wijzerplaat &middot; spits</p>
        <ul class="invul">{"".join(f"<li><b>{n}</b><span></span></li>" for n in range(1, 7))}</ul>
        <p style="margin-top:4mm;font-size:10pt">Achter de galmgaten hangen de klokken. Waarom zitten daar gaten in de muur, denk je?</p>
        {lijnen(2)}
      </div>
    </div>
  </div>
</section>

<section class="blad">
  <div class="opdracht">
    <h2><span class="nr">4</span>Rekenen met de toren</h2>
    <ol class="vragen">
      <li>De toren werd ingewijd in 1925. Hoe oud is de toren nu?{lijnen(1)}</li>
      <li>Hoe oud is de toren in het jaar dat jij 18 wordt?{lijnen(1)}</li>
      <li>De drie nieuwe klokken kostten in 1948 samen 7920 gulden. De regering betaalde daarvan 3161 gulden. Hoeveel moest de kerk zelf betalen?{lijnen(1)}</li>
      <li>De klokken luiden &eacute;&eacute;n keer per week. Ongeveer hoe vaak hebben ze geluid sinds 1948? <span class="pittig">Pittig</span>{lijnen(1)}</li>
    </ol>
  </div>

  <div class="opdracht">
    <h2><span class="nr">5</span>Woordzoeker</h2>
    <p>Zoek de woorden. Ze staan van links naar rechts, van boven naar beneden of schuin.</p>
    <div class="zoek"><table>{woordzoeker}</table><ul>{"".join(f"<li>{w.lower()}</li>" for w in WOORDEN)}</ul></div>
  </div>

  <div class="opdracht">
    <h2><span class="nr">6</span>Jij bent de baas van de toren</h2>
    <p>De toren kreeg in 1987 een nieuwe functie. Stel dat jij mag kiezen wat er nu in de toren komt. Wat zou jij ervan maken? Teken of schrijf het op.</p>
    <div class="vak"></div>
    <p style="margin-top:3mm;font-size:10pt"><b>Vraag het thuis:</b> kennen je ouders of grootouders de oude kerk nog? Een mooi verhaal of een oude foto? Je juf of meester kan het mailen naar info@dierensetoren.nl.</p>
  </div>
</section>

<section class="blad antwoorden">
  <div class="kop"><div><p class="eyebrow">Voor de leerkracht</p><h1>Antwoorden</h1></div></div>
  <h2><span class="nr">1</span>Vragen bij de tekst</h2>
  <ol>
    <li>De Hogestraat (nummer 12).</li>
    <li>Architect Wolter te Riele.</li>
    <li>De Duitsers namen ze mee.</li>
    <li>Op zaterdag om 18.00 uur.</li>
    <li>Veel inwoners wilden de toren houden. Een groep inwoners, het Comit&eacute; K12, kwam in actie.</li>
  </ol>
  <h2><span class="nr">2</span>Tijdlijn</h2>
  <p>{tl_antwoord}</p>
  <h2><span class="nr">3</span>Wat zie je aan de toren?</h2>
  <p>1 kruis en windhaan, 2 spits, 3 wijzerplaat, 4 galmgaten, 5 kantoren en vergaderruimte, 6 de voet met steunberen. De galmgaten laten het geluid van de klokken naar buiten; de schuine planken (galmborden) houden regen tegen en sturen het geluid naar beneden.</p>
  <h2><span class="nr">4</span>Rekenen</h2>
  <ol>
    <li>Het huidige jaar min 1925 (in 2027 is de toren 102 jaar).</li>
    <li>Geboortejaar + 18 &minus; 1925.</li>
    <li>7920 &minus; 3161 = 4759 gulden.</li>
    <li>Ongeveer 52 keer per jaar. Van 1948 tot 2027 is 79 jaar: 79 &times; 52 = 4108 keer.</li>
  </ol>
  <h2><span class="nr">5</span>Woordzoeker</h2>
  <div class="zoek zoek-antwoord"><table>{"".join("<tr>" + "".join(f'<td class="raak">{ch}</td>' if ch else "<td></td>" for ch in rij) + "</tr>" for rij in raster)}</table>
  <div><p><b>Meer weten?</b> Op dierensetoren.nl/geschiedenis.html staan de hele geschiedenis, een video van een minuut, oude foto&rsquo;s en een brochure om te downloaden.</p>
  <p>De toren is te beklimmen tijdens Open Monumentendag. Vragen of idee&euml;n voor een les? Mail naar info@dierensetoren.nl.</p></div></div>
</section>
</body></html>
"""
open("werkblad.html", "w", encoding="utf-8").write(page)
print(f"werkblad.html: woordzoeker {N}x{N} met {len(WOORDEN)} woorden")
