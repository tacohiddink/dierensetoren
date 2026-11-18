#!/usr/bin/env bash
# Stelt de site samen in _site en vervangt elke "?v=dev" door een versienummer
# dat per bestand uit de inhoud wordt berekend. Zo halen browsers een gewijzigd
# bestand direct opnieuw op, terwijl ongewijzigde foto's in de cache blijven.
# De <lastmod> in sitemap.xml, "dateModified" en "Laatst bijgewerkt" op de pagina's
# en de datum onderaan llms.txt komen uit de laatste commit van elk bestand.
# Gebruik: .github/scripts/bouw.sh <versie>
#   <versie> wordt alleen gebruikt voor verwijzingen naar bestanden die niet bestaan.
set -euo pipefail
versie="${1:?geef een versie op, bijvoorbeeld de korte commit-hash}"

rm -rf _site
mkdir _site
rsync -a \
  --exclude .git --exclude .github --exclude .idea \
  --exclude .gitignore --exclude README.md --exclude BEHEER.md --exclude _config.yml \
  --exclude lighthouserc.json --exclude _site --exclude node_modules --exclude opmaak-screenshots \
  --exclude brochure.html --exclude qr-brochure.png --exclude werkblad.html --exclude todo.txt \
  ./ _site/

python3 - "$versie" <<'EOF'
import hashlib, re, subprocess, sys
from pathlib import Path

versie = sys.argv[1]
root = Path("_site").resolve()
hashes = {}

def hash_van(pad):
    if pad not in hashes:
        hashes[pad] = hashlib.sha1(pad.read_bytes()).hexdigest()[:8]
    return hashes[pad]

def versioneer(bestand):
    def vervang(m):
        ref = m.group(1)
        pad = (root / ref.lstrip("/")) if ref.startswith("/") else (bestand.parent / ref)
        pad = pad.resolve()
        return f"{ref}?v={hash_van(pad) if pad.is_file() else versie}"
    tekst = bestand.read_text(encoding="utf-8")
    bestand.write_text(re.sub(r"""([^\s"'(),?=]+)\?v=dev""", vervang, tekst), encoding="utf-8")

for f in list(root.glob("*.html")) + list(root.glob("css/*.css")):
    versioneer(f)

# lastmod in de sitemap uit git; zonder git (of zonder geschiedenis) blijft de oude datum staan
sitemap = root / "sitemap.xml"
def laatste_commit(bron):
    try:
        uit = subprocess.run(["git", "log", "-1", "--format=%cs", "--", bron], capture_output=True, text=True, check=True).stdout.strip()
        return uit or None
    except (OSError, subprocess.CalledProcessError):
        return None
def lastmod(m):
    loc = m.group(1)
    bron = loc.split("dierensetoren.nl/", 1)[1] or "index.html"
    datum = laatste_commit(bron)
    return m.group(0) if not datum else f"<loc>{loc}</loc><lastmod>{datum}</lastmod>"
sitemap.write_text(re.sub(r"<loc>([^<]+)</loc><lastmod>[^<]+</lastmod>", lastmod, sitemap.read_text(encoding="utf-8")), encoding="utf-8")

# "dateModified" en "Laatst bijgewerkt" op elke pagina, en onderaan llms.txt, ook uit git
MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]
def leesbaar(datum):
    j, m, d = datum.split("-")
    return f"{int(d)} {MAANDEN[int(m) - 1]} {j}"
for f in root.glob("*.html"):
    datum = laatste_commit(f.name)
    if not datum:
        continue
    tekst = f.read_text(encoding="utf-8")
    tekst = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{datum}"', tekst)
    tekst = re.sub(r'(Laatst bijgewerkt: )<time datetime="\d{4}-\d{2}-\d{2}">[^<]*</time>', lambda m: f'{m.group(1)}<time datetime="{datum}">{leesbaar(datum)}</time>', tekst)
    f.write_text(tekst, encoding="utf-8")
llms = root / "llms.txt"
datum = laatste_commit(".")
if llms.exists() and datum:
    llms.write_text(re.sub(r"Laatst bijgewerkt: .*", f"Laatst bijgewerkt: {leesbaar(datum)}", llms.read_text(encoding="utf-8")), encoding="utf-8")
EOF

if grep -rl '?v=dev' _site --include='*.html' --include='*.css'; then
  echo "Niet alle versienummers zijn vervangen" >&2
  exit 1
fi
