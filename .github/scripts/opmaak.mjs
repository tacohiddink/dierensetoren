// Opmaakcontrole: test de opmaak van alle pagina's op desktop en mobiel, en vergelijkt
// screenshots met de huidige versie van de site.
//
// Fouten (laten de controle falen):
// - tekst- en fotoblokken (.split) staan op desktop niet naast elkaar
// - de pagina is op mobiel breder dan het scherm (horizontaal scrollen)
// - een foto laadt niet
// - een JavaScript-fout op de pagina
//
// Ter informatie: screenshots van elke pagina (nieuw, huidig en verschil) en een
// overzicht van welke pagina's er anders uitzien.
//
// Gebruik: node opmaak.mjs <nieuwe site> <huidige site of -> <uitvoermap>
import { chromium } from "playwright";
import pixelmatch from "pixelmatch";
import { PNG } from "pngjs";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const [nieuwDir, huidigDir, uitDir] = process.argv.slice(2);
const paginas = JSON.parse(fs.readFileSync("lighthouserc.json", "utf8")).ci.collect.url.map((u) => new URL(u).pathname);
const schermen = [
  { naam: "desktop", viewport: { width: 1280, height: 800 }, isMobile: false },
  { naam: "mobiel", viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
];
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".png": "image/png",
  ".avif": "image/avif", ".svg": "image/svg+xml", ".woff2": "font/woff2", ".mp4": "video/mp4", ".txt": "text/plain", ".xml": "application/xml" };

function server(dir) {
  return new Promise((resolve) => {
    const s = http.createServer((req, res) => {
      const p = path.join(dir, decodeURIComponent(new URL(req.url, "http://x").pathname));
      fs.readFile(p.endsWith("/") ? path.join(p, "index.html") : p, (err, data) => {
        if (err) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { "Content-Type": types[path.extname(p)] || "application/octet-stream" });
        res.end(data);
      });
    }).listen(0, "127.0.0.1", () => resolve(s));
  });
}

async function laadVolledig(page) {
  // Effecten die niet elke keer pixel-identiek renderen uitzetten, zodat alleen echte wijzigingen opvallen
  await page.addStyleTag({ content: "*, *::before, *::after { backdrop-filter: none !important; -webkit-backdrop-filter: none !important; transition: none !important; animation: none !important; caret-color: transparent !important; }" });
  // Alle foto's direct laden en de pagina doorscrollen, zodat het screenshot compleet is
  await page.evaluate(async () => {
    document.querySelectorAll('img[loading="lazy"]').forEach((i) => { i.loading = "eager"; });
    for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 50)); }
    window.scrollTo(0, 0);
    await Promise.all([...document.images].filter((i) => i.getAttribute("src")).map((i) => i.decode().catch(() => {})));
    await document.fonts.ready;
  });
  await page.waitForTimeout(300);
}

function vergelijk(a, b) {
  // Maak beide afbeeldingen even groot (wit opvullen) en tel de afwijkende pixels
  const w = Math.max(a.width, b.width), h = Math.max(a.height, b.height);
  const pad = (img) => { const o = new PNG({ width: w, height: h }); o.data.fill(255); PNG.bitblt(img, o, 0, 0, img.width, img.height, 0, 0); return o; };
  const pa = pad(a), pb = pad(b), diff = new PNG({ width: w, height: h });
  const n = pixelmatch(pa.data, pb.data, diff.data, w, h, { threshold: 0.1 });
  return { procent: (100 * n) / (w * h), diff, hoogteVerschil: b.height - a.height };
}

const fouten = [];
const regels = [];
fs.mkdirSync(uitDir, { recursive: true });
const nieuw = await server(nieuwDir);
const huidig = huidigDir !== "-" ? await server(huidigDir) : null;
const browser = await chromium.launch(process.env.CI ? {} : { channel: "chrome" });

for (const scherm of schermen) {
  const context = await browser.newContext({ viewport: scherm.viewport, isMobile: scherm.isMobile, hasTouch: scherm.hasTouch, deviceScaleFactor: 1, reducedMotion: "reduce" });
  for (const p of paginas) {
    const naam = `${p.replace(/^\//, "").replace(".html", "")}-${scherm.naam}`;
    const page = await context.newPage();
    const jsFouten = [];
    page.on("pageerror", (e) => jsFouten.push(e.message));
    await page.goto(`http://127.0.0.1:${nieuw.address().port}${p}`, { waitUntil: "load" });
    await laadVolledig(page);

    const r = await page.evaluate((desktop) => {
      const f = [];
      if (document.documentElement.scrollWidth > window.innerWidth + 1) f.push(`pagina is ${document.documentElement.scrollWidth}px breed op een scherm van ${window.innerWidth}px`);
      for (const img of document.querySelectorAll("img")) {
        if (img.getAttribute("src") && !(img.complete && img.naturalWidth > 0)) f.push(`foto laadt niet: ${img.currentSrc || img.src}`);
      }
      if (desktop) {
        document.querySelectorAll(".split").forEach((s, i) => {
          const blokken = [...s.children].flatMap((c) => (getComputedStyle(c).display === "contents" ? [...c.children] : [c]))
            .filter((c) => getComputedStyle(c).display !== "none");
          if (blokken.length !== 2) { f.push(`tweekoloms-blok ${i + 1} heeft ${blokken.length} vakken in plaats van 2`); return; }
          const [a, b] = blokken.map((c) => c.getBoundingClientRect());
          if (b.left < a.right) f.push(`tweekoloms-blok ${i + 1}: tekst en foto staan onder elkaar in plaats van naast elkaar`);
        });
      }
      return f;
    }, !scherm.isMobile);
    for (const m of [...r, ...jsFouten.map((e) => `JavaScript-fout: ${e}`)]) fouten.push(`${p} (${scherm.naam}): ${m}`);

    const nieuwPng = path.join(uitDir, `${naam}-nieuw.png`);
    await page.screenshot({ path: nieuwPng, fullPage: true, mask: [page.locator("video")] });
    await page.close();

    if (huidig) {
      const hp = await context.newPage();
      const res = await hp.goto(`http://127.0.0.1:${huidig.address().port}${p}`, { waitUntil: "load" });
      if (!res || res.status() === 404) { regels.push(`| ${p} | ${scherm.naam} | nieuwe pagina |`); await hp.close(); continue; }
      await laadVolledig(hp);
      const huidigPng = path.join(uitDir, `${naam}-huidig.png`);
      await hp.screenshot({ path: huidigPng, fullPage: true, mask: [hp.locator("video")] });
      await hp.close();
      const v = vergelijk(PNG.sync.read(fs.readFileSync(huidigPng)), PNG.sync.read(fs.readFileSync(nieuwPng)));
      if (v.procent > 0.05) {
        fs.writeFileSync(path.join(uitDir, `${naam}-verschil.png`), PNG.sync.write(v.diff));
        const hoogte = v.hoogteVerschil ? `, ${v.hoogteVerschil > 0 ? "+" : ""}${v.hoogteVerschil}px hoogte` : "";
        regels.push(`| ${p} | ${scherm.naam} | ${v.procent.toFixed(1)}% anders${hoogte} |`);
      } else {
        fs.rmSync(huidigPng);
      }
    }
  }
  await context.close();
}
await browser.close();
nieuw.close(); huidig?.close();

let samenvatting = "## Opmaakcontrole\n\n";
samenvatting += fouten.length ? `### ${fouten.length} fout(en)\n\n${fouten.map((f) => `- ${f}`).join("\n")}\n\n` : "Geen opmaakfouten gevonden.\n\n";
if (huidig) {
  samenvatting += regels.length
    ? `### Pagina's die er anders uitzien\n\n| Pagina | Scherm | Verschil |\n|---|---|---|\n${regels.join("\n")}\n\nBekijk de screenshots in het artifact **opmaak-screenshots** (nieuw, huidig en verschil).\n`
    : "Geen zichtbare verschillen met de huidige site.\n";
}
console.log(samenvatting);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, samenvatting);
for (const f of fouten) console.log(`::error::${f}`);
process.exit(fouten.length ? 1 : 0);
