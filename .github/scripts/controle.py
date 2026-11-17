"""Controleert de gebouwde site (_site) op fouten voordat een wijziging live gaat.

Fouten (laten de controle falen):
- verwijzingen naar bestanden die niet bestaan (links, afbeeldingen, video, CSS, srcset)
- links naar een #anker dat niet op de pagina staat
- afbeeldingen zonder alt, width of height
- externe links zonder target="_blank" rel="noopener"
- ongeldige structured data (JSON-LD), sitemap of og:image
- achtergebleven "?v=dev"
- Open Monumentendag die voorbij is, of die niet overal hetzelfde jaar en dezelfde
  datum heeft (pagina's, llms.txt, structured data en het agenda-item)

Waarschuwingen (falen niet): externe links die niet bereikbaar lijken.

Gebruik: python3 controle.py <map met de gebouwde site>
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE = "https://dierensetoren.nl"
root = Path(sys.argv[1]).resolve()
errors, warnings = [], []
external = {}


def error(f, msg):
    errors.append((f, msg))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.ids, self.imgs, self.links, self.jsonld = [], set(), [], [], []
        self.og_images, self._in_ld, self._ld = [], False, ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src", "poster"):
            if a.get(key):
                self.refs.append(a[key])
        if a.get("srcset"):
            self.refs += [part.strip().split()[0] for part in a["srcset"].split(",") if part.strip()]
        if tag == "img":
            self.imgs.append(a)
        if tag == "a" and a.get("href"):
            self.links.append(a)
        if tag == "meta" and a.get("property") == "og:image":
            self.og_images.append(a.get("content", ""))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._ld = True, ""

    def handle_data(self, data):
        if self._in_ld:
            self._ld += data

    def handle_endtag(self, tag):
        if tag == "script" and self._in_ld:
            self.jsonld.append(self._ld)
            self._in_ld = False


def local_target(ref, page):
    """Zet een lokale verwijzing om naar (bestand, anker), of None voor externe of speciale links."""
    if ref.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None
    if ref.startswith(("http://", "https://", "//")):
        if ref.startswith(SITE):
            ref = ref[len(SITE):] or "/"
        else:
            return None
    parts = urlsplit(ref)
    path = parts.path
    if not path:
        return page, parts.fragment
    base = root if path.startswith("/") else page.parent
    target = (base / path.lstrip("/")).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, parts.fragment


pages = {}
for f in sorted(root.rglob("*.html")):
    p = Page()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f.resolve()] = p

for f, p in pages.items():
    name = f.relative_to(root)
    for ref in p.refs:
        t = local_target(ref, f)
        if t is None:
            if ref.startswith("http"):
                external.setdefault(ref, name)
            continue
        target, frag = t
        if not target.exists():
            error(name, f"verwijst naar een bestand dat niet bestaat: {ref}")
        elif frag and target.suffix == ".html" and frag not in pages.get(target, Page()).ids:
            error(name, f"anker bestaat niet: {ref}")
    for img in p.imgs:
        src = img.get("src", "")
        for attr in ("alt", "width", "height"):
            if attr not in img:
                error(name, f"afbeelding zonder {attr}: {src}")
    for a in p.links:
        href = a["href"]
        if href.startswith("http") and not href.startswith(SITE):
            if a.get("target") != "_blank" or "noopener" not in (a.get("rel") or ""):
                error(name, f'externe link zonder target="_blank" rel="noopener": {href}')
    for block in p.jsonld:
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            error(name, f"ongeldige structured data (JSON-LD): {e}")
    for og in p.og_images:
        t = local_target(og, f)
        if not og.startswith(SITE) or t is None or not t[0].exists():
            error(name, f"og:image bestaat niet op de site: {og}")

for css in root.rglob("*.css"):
    for ref in re.findall(r'url\(["\']?([^"\')]+)', css.read_text(encoding="utf-8")):
        t = local_target(ref, css)
        if t and not t[0].exists():
            error(css.relative_to(root), f"verwijst naar een bestand dat niet bestaat: {ref}")

for f in list(root.rglob("*.html")) + list(root.rglob("*.css")):
    if "?v=dev" in f.read_text(encoding="utf-8"):
        error(f.relative_to(root), 'bevat nog "?v=dev"')

sitemap = root / "sitemap.xml"
if sitemap.exists():
    try:
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in ET.parse(sitemap).getroot().findall("s:url/s:loc", ns):
            t = local_target(loc.text.strip(), root / "index.html")
            if t is None or not t[0].exists():
                error("sitemap.xml", f"pagina bestaat niet: {loc.text}")
    except ET.ParseError as e:
        error("sitemap.xml", f"ongeldige XML: {e}")

llms = root / "llms.txt"
if llms.exists():
    for url in re.findall(r"\((https://dierensetoren\.nl[^)]*)\)", llms.read_text(encoding="utf-8")):
        t = local_target(url, root / "index.html")
        if t is None or not t[0].exists():
            error("llms.txt", f"pagina bestaat niet: {url}")

# Open Monumentendag: de datum mag niet voorbij zijn en moet overal hetzelfde jaar hebben
act = root / "activiteiten.html"
if act.exists():
    event = None
    for block in pages[act.resolve()].jsonld:
        try:
            ld = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(ld, dict) and ld.get("@type") == "Event":
            event = ld
    if not event or "startDate" not in event:
        error("activiteiten.html", "geen Event met startDate voor Open Monumentendag in de structured data")
    else:
        start = event["startDate"]
        jaar = start[:4]
        if start[:10] < date.today().isoformat():
            error("activiteiten.html", f"Open Monumentendag ({start[:10]}) is voorbij: zet de nieuwe datum op alle plekken uit BEHEER.md")
        for naam in ("index.html", "activiteiten.html", "en.html", "llms.txt"):
            bestand = root / naam
            if not bestand.exists():
                continue
            ruw = bestand.read_text(encoding="utf-8")
            if naam.endswith(".txt"):
                ruw = ruw.replace("\n", ". ")  # in llms.txt is elke regel een eigen zin
            # descriptions tellen mee: die noemen het jaar soms ook
            meta = " ".join(c + ". " for c in re.findall(r'<meta (?:name|property)="(?:og:)?description" content="([^"]*)"', ruw))
            tekst = re.sub(r"<script.*?</script>", " ", ruw, flags=re.S)
            tekst = re.sub(r"\s+", " ", meta + re.sub(r"<[^>]+>", " ", tekst))
            gemeld = set()
            # elk jaartal in de zin met "Monumentendag" of "Heritage Day" en in de zin erna
            for m in re.finditer(r"Monumentendag|Heritage Day", tekst):
                stuk = tekst[m.start():m.start() + 300]
                einden = [e.end() for e in re.finditer(r"[.!?](\s|$)", stuk)]
                if len(einden) >= 2:
                    stuk = stuk[:einden[1]]
                for j in re.findall(r"\b(20[2-9]\d)\b", stuk):
                    if j != jaar and (j, stuk[:60]) not in gemeld:
                        gemeld.add((j, stuk[:60]))
                        error(naam, f"Open Monumentendag noemt {j}, maar de structured data noemt {jaar}: {stuk[:90]}")
        ics = root / "downloads" / "open-monumentendag-dierense-toren.ics"
        if ics.exists():
            inhoud = ics.read_text(encoding="utf-8")
            verwacht = start[:10].replace("-", "") + "T" + start[11:16].replace(":", "") + "00"
            if f"DTSTART;TZID=Europe/Amsterdam:{verwacht}" not in inhoud:
                error("downloads/open-monumentendag-dierense-toren.ics", f"DTSTART komt niet overeen met de structured data ({start})")
            if f"open-monumentendag-{jaar}@" not in inhoud:
                error("downloads/open-monumentendag-dierense-toren.ics", f"UID noemt niet het jaar {jaar}")

# Externe links: alleen waarschuwen, want andere sites zijn soms tijdelijk onbereikbaar of weren robots
for url, name in sorted(external.items()):
    if "google.com/maps" in url:
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (linkcontrole dierensetoren.nl)"})
        with urllib.request.urlopen(req, timeout=15) as r:
            if r.status >= 400:
                warnings.append((name, f"externe link geeft {r.status}: {url}"))
    except Exception as e:  # noqa: BLE001 - elke fout is hier een waarschuwing
        warnings.append((name, f"externe link niet bereikbaar ({e.__class__.__name__}): {url}"))

for f, msg in warnings:
    print(f"::warning file={f}::{msg}")
for f, msg in errors:
    print(f"::error file={f}::{msg}")
print(f"{len(pages)} pagina's gecontroleerd: {len(errors)} fout(en), {len(warnings)} waarschuwing(en).")
sys.exit(1 if errors else 0)
