# Handleiding: de website bijwerken

Deze handleiding is voor het bestuur en vrijwilligers van Stichting De Dierense Toren. Je hebt geen programmeerkennis nodig, wel een GitHub-account met toegang tot deze repository.

## Hoe de site werkt

- De site bestaat uit gewone HTML-bestanden in deze repository, één per pagina (zie het overzicht hieronder).
- Elke wijziging op de branch `master` wordt automatisch gepubliceerd op [dierensetoren.nl](https://dierensetoren.nl). Dat duurt ongeveer een minuut. Je ziet de voortgang onder het tabblad **Actions**.
- Er is geen database en geen beheeromgeving: wat in de bestanden staat, staat op de site.

## Een tekst aanpassen via de website van GitHub

1. Open het bestand op GitHub, bijvoorbeeld `activiteiten.html`.
2. Klik rechtsboven op het potloodje (**Edit this file**).
3. Zoek de tekst op met Ctrl+F (of Cmd+F op een Mac) en pas hem aan. Laat de codes tussen `<` en `>` staan; verander alleen de tekst ertussen.
4. Klik op **Commit changes...** en kies **Create a new branch** en daarna **Propose changes**.
5. Klik op **Create pull request**. Laat iemand anders er eventueel nog naar kijken.
6. Klik op **Merge pull request**. Na ongeveer een minuut staat de wijziging live.

Bij elke pull request draait automatisch een **controle** (onderaan de pull request, bij "Checks"). Die zoekt naar kapotte links, ontbrekende afbeeldingen, foto's zonder beschrijving of afmetingen, externe links die niet in een nieuw tabblad openen en fouten in de structured data, draait Lighthouse op alle pagina's, en test de opmaak op desktop en mobiel. Bij die laatste stap worden ook screenshots gemaakt en vergeleken met de huidige site: in het overzicht van de controle (Details → Summary) zie je welke pagina's er anders uitzien, en onder **Artifacts** staan de screenshots (nieuw, huidig en verschil). Kijk daar even naar voordat je merget. Staat er een rood kruisje, klik dan op **Details** om te zien wat er mis is, en merge pas als de controle groen is.

Een fout gemaakt? Elke wijziging staat in de geschiedenis van GitHub en kan worden teruggedraaid (knop **Revert** bij de gemergde pull request).

## Overzicht van de pagina's

| Bestand | Pagina |
|---|---|
| `index.html` | Startpagina, met "Nu bij de toren" en de veelgestelde vragen |
| `geschiedenis.html` | Geschiedenis: video, "In het kort", tijdlijn, tekening van de toren, architect, foto's, oproep |
| `activiteiten.html` | Activiteiten & bezoek: Open Monumentendag, route, parkeren, contact en tradities |
| `bereikbaarheid.html` | Doorverwijzing naar Activiteiten & bezoek (voor oude links) |
| `nieuws.htm`, `main_nieuws.htm`, `main_riele.htm`, `main_beheren.htm`, `bunker_right.htm` | Doorverwijzingen van adressen van de oude website (tot 2019) |
| `donateur.html` | Steun de toren: donateur, bedrijfsvriend en nalaten |
| `stichting.html` | Over de stichting: wat we doen, hoe het begon, bestuur, in memoriam en contact |
| `nalaten.html` | Nalaten aan de toren |
| `verhuur.html` | Ruimte huren (nu verhuurd aan De Nieuwe Yogi) |
| `anbistatus.html` | ANBI-gegevens: bestuur, verslag en cijfers |
| `inmemoriam.html` | In memoriam Peter Breukink |
| `privacy.html` | Privacyverklaring |
| `en.html` | Korte Engelse pagina voor toeristen |
| `toegankelijkheid.html` | Toegankelijkheidsverklaring |
| `404.html` | Pagina voor links die niet bestaan |
| `llms.txt` | Samenvatting voor AI-diensten zoals ChatGPT |
| `sitemap.xml` | Lijst van pagina's voor zoekmachines |

## Elk jaar bijwerken

Er komt elk jaar automatisch een herinnering (zie [Herinneringen](#herinneringen)).

### Open Monumentendag (voor de zomer)

De datum en tijden staan op acht plekken. Pas ze allemaal aan:

1. `activiteiten.html`: de zin "Open Monumentendag 2027 is op zaterdag 11 en zondag 12 september. Op zondag is de toren geopend van 11.00 tot 17.00 uur."
2. `activiteiten.html`, bovenaan tussen `<script type="application/ld+json">`: `"name"`, `"startDate"` en `"endDate"`. Gebruik de vorm `2027-09-12T11:00:00+02:00` (jaar-maand-dag, tijd, zomertijd).
3. `index.html`: het antwoord op "Kan ik de Dierense Toren beklimmen?" in de veelgestelde vragen.
4. `index.html`, bovenaan tussen `<script type="application/ld+json">`: dezelfde tekst bij `"Kan ik de Dierense Toren beklimmen?"`.
5. `llms.txt`: de regel die begint met "Bezoek:".
6. `downloads/open-monumentendag-dierense-toren.ics` (het agenda-item achter de knop "Zet in je agenda"): `UID` (jaartal), `DTSTART` en `DTEND` in de vorm `20270912T110000` (jaar-maand-dag, T, uur-minuut-seconde), en `DTSTAMP` (de datum van vandaag).
7. `en.html`: de zin "Heritage Day 2027: …" met de datum en de openingstijden in het Engels, en bovenaan het jaartal in de twee descriptions (`name="description"` en `og:description`).
8. `index.html`: de kaart "Binnenkort: Open Monumentendag" onder "Nu bij de toren". Kijk daar meteen of de andere twee kaarten nog actueel zijn.

Zet daarna de datum bij **Laatst bijgewerkt** goed (zie hieronder).

De automatische controle bij een pull request helpt: die faalt als Open Monumentendag in de structured data al voorbij is, als een van de plekken hierboven een ander jaar noemt, of als het agenda-item een andere datum heeft.

### ANBI-verslag en financiële cijfers (begin van het jaar)

Een culturele ANBI moet deze gegevens actueel op de website hebben.

1. `anbistatus.html`, onder "Verslag van de activiteiten in …": pas het jaartal en de tekst aan.
2. `anbistatus.html`, de tabel onder "Financiële verantwoording": vervang de oudste kolom door het nieuwe jaar. De kolommen staan in de regel met `<thead>`; elke rij heeft per jaar één `<td>`.
3. `anbistatus.html`: controleer de lijst met bestuursleden.
4. Zet de datum bij **Laatst bijgewerkt** goed.

### Laatst bijgewerkt

Na een inhoudelijke wijziging op de ANBI- of activiteitenpagina pas je de datum op drie plekken aan:

- onderaan de pagina: `<time datetime="2026-11-16">16 november 2026</time>` (beide datums);
- bovenaan de pagina bij `"dateModified": "2026-11-16"`;
- onderaan `llms.txt`: "Laatst bijgewerkt: …".

De datums in `sitemap.xml` hoef je niet bij te werken: die worden bij het publiceren automatisch uit de laatste wijziging van elke pagina gehaald.

## Brochure (PDF) bijwerken

De brochure `downloads/geschiedenis-dierense-toren.pdf` wordt gemaakt uit de inhoud van `geschiedenis.html` (tijdlijn, architect en "In het kort"). Maak hem opnieuw als die pagina inhoudelijk verandert. Je hebt een Mac met Google Chrome nodig:

```sh
python3 .github/scripts/brochure.py
# QR-code naar de geschiedenispagina, als qr-brochure.png naast brochure.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --no-pdf-header-footer --print-to-pdf=downloads/geschiedenis-dierense-toren.pdf brochure.html
rm brochure.html qr-brochure.png
```

Controleer de PDF daarna even op de pagina-indeling, en pas zo nodig het aantal pagina's en de bestandsgrootte aan in de downloadlink op `geschiedenis.html`.

## Werkblad voor scholen (PDF) bijwerken

Het werkblad `downloads/werkblad-dierense-toren.pdf` (groep 6–8, 4 pagina's met antwoorden) wordt gemaakt met `.github/scripts/werkblad.py`. De teksten en vragen staan in dat script; de tekening van de toren komt uit `geschiedenis.html`. Maak het werkblad zo opnieuw (Mac met Google Chrome):

```sh
python3 .github/scripts/werkblad.py
python3 -m http.server 8765 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --no-pdf-header-footer --print-to-pdf=downloads/werkblad-dierense-toren.pdf \
  http://localhost:8765/werkblad.html
kill %1; rm werkblad.html
```

Controleer daarna of het werkblad nog op 4 pagina's past.

## Foto's toevoegen

- Maak de foto eerst kleiner: maximaal ongeveer 1200 pixels breed, als JPG, liefst onder de 400 KB.
- Geef het bestand een beschrijvende naam in kleine letters met streepjes, bijvoorbeeld `kerstboom-2026.jpg`, en zet het in de map `img/web/`.
- Zet in de HTML altijd een beschrijving (`alt="..."`) en de afmetingen (`width` en `height` in pixels) bij de foto.
- Voor de fotogalerij op de geschiedenispagina is er van grote foto's ook een kleine versie van 480 pixels breed (`naam-480.jpg` en `naam-480.avif`), zodat de miniaturen snel laden.
- Zet geen originele, grote bestanden in de repository.
- Gebruik alleen foto's die je zelf hebt gemaakt of waarvoor je toestemming hebt.

## Afspraken in de code

Deze afspraken houden de site snel, vindbaar en privacyvriendelijk. Als je alleen tekst aanpast, hoef je er niets mee.

- **`?v=dev` achter bestandsnamen** (bijvoorbeeld `css/site.css?v=dev`) laten staan. Bij het publiceren wordt dit per bestand vervangen door een versienummer dat uit de inhoud wordt berekend. Bezoekers zien zo nooit een oude versie uit hun browsercache, en foto's die niet veranderd zijn hoeven ze niet opnieuw te downloaden.
- **Links naar andere websites** krijgen `target="_blank" rel="noopener"`, zodat ze in een nieuw tabblad openen.
- **Geen externe diensten toevoegen** die cookies plaatsen of bezoekers volgen (zoals Google Analytics, YouTube-video's of social-mediaknoppen). Dan is een cookiebanner nodig en moet de privacyverklaring worden aangepast. De lettertypes staan daarom op de eigen site, en de Google-kaart laadt pas na een klik.
- **Structured data** (de blokken `<script type="application/ld+json">`) beschrijft de toren, de stichting, de veelgestelde vragen en Open Monumentendag voor Google. Houd die gelijk met de zichtbare tekst.

## Lokaal bekijken (voor wie dat wil)

Dubbelklik op een HTML-bestand om het in je browser te openen. Voor de 404-pagina en een paar andere details is een kleine webserver nodig:

```sh
python3 -m http.server 8000
```

Open daarna http://localhost:8000.

## Herinneringen

Het workflowbestand `.github/workflows/herinneringen.yml` maakt elk jaar automatisch een melding (issue) aan op GitHub:

- **15 januari:** ANBI-verslag en financiële cijfers bijwerken.
- **1 juni:** datum en tijden van Open Monumentendag bijwerken.

Wie de repository volgt, krijgt die meldingen per e-mail. Sluit de melding als de taak klaar is.
