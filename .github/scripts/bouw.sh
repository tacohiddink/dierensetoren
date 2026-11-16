#!/usr/bin/env bash
# Stelt de site samen in _site en vervangt elke "?v=dev" door een versienummer,
# zodat browsers na een wijziging direct de nieuwe CSS, JS en foto's ophalen.
# Gebruik: .github/scripts/bouw.sh <versie>
set -euo pipefail
versie="${1:?geef een versie op, bijvoorbeeld de korte commit-hash}"

rm -rf _site
mkdir _site
rsync -a \
  --exclude .git --exclude .github --exclude .idea \
  --exclude .gitignore --exclude README.md --exclude BEHEER.md --exclude _config.yml \
  --exclude lighthouserc.json --exclude _site --exclude node_modules --exclude opmaak-screenshots \
  --exclude brochure.html --exclude qr-brochure.png --exclude werkblad.html \
  ./ _site/
sed -i.bak "s/?v=dev/?v=${versie}/g" _site/*.html _site/css/*.css
rm -f _site/*.bak _site/css/*.bak
if grep -rl '?v=dev' _site --include='*.html' --include='*.css'; then
  echo "Niet alle versienummers zijn vervangen" >&2
  exit 1
fi
