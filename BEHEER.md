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

Bij elke pull request draait automatisch een **controle** (onderaan de pull request, bij "Checks"). Die zoekt naar kapotte links, ontbrekende afbeeldingen, foto's zonder beschrijving of afmetingen, externe links die niet in een nieuw tabblad openen en fouten in de structured data, en draait Lighthouse op alle pagina's. Staat er een rood kruisje, klik dan op **Details** om te zien wat er mis is, en merge pas als de controle groen is.

Een fout gemaakt? Elke wijziging staat in de geschiedenis van GitHub en kan worden teruggedraaid (knop **Revert** bij de gemergde pull request).

## Overzicht van de pagina's

| Bestand | Pagina |
|---|---|
| `index.html` | Startpagina, met de veelgestelde vragen |
| `geschiedenis.html` | Geschiedenis: video, tijdlijn, foto's, oproep, architect, "In het kort" |
| `activiteiten.html` | Activiteiten en tradities, met Open Monumentendag |
| `bereikbaarheid.html` | Bezoek en contact |
| `donateur.html` | Donateur worden en bedrijfsvrienden |
| `nalaten.html` | Nalaten aan de toren |
| `anbistatus.html` | ANBI-gegevens: bestuur, verslag en cijfers |
| `inmemoriam.html` | In memoriam Peter Breukink |
| `privacy.html` | Privacyverklaring |
| `404.html` | Pagina voor links die niet bestaan |
| `llms.txt` | Samenvatting voor AI-diensten zoals ChatGPT |
| `sitemap.xml` | Lijst van pagina's voor zoekmachines |

## Elk jaar bijwerken

Er komt elk jaar automatisch een herinnering (zie [Herinneringen](#herinneringen)).

### Open Monumentendag (voor de zomer)

De datum en tijden staan op vijf plekken. Pas ze allemaal aan:

1. `activiteiten.html`: de zin "Open Monumentendag 2027 is op zaterdag 11 en zondag 12 september. Op zondag is de toren geopend van 11.00 tot 17.00 uur."
2. `activiteiten.html`, bovenaan tussen `<script type="application/ld+json">`: `"name"`, `"startDate"` en `"endDate"`. Gebruik de vorm `2027-09-12T11:00:00+02:00` (jaar-maand-dag, tijd, zomertijd).
3. `index.html`: het antwoord op "Kan ik de Dierense Toren beklimmen?" in de veelgestelde vragen.
4. `index.html`, bovenaan tussen `<script type="application/ld+json">`: dezelfde tekst bij `"Kan ik de Dierense Toren beklimmen?"`.
5. `llms.txt`: de regel die begint met "Bezoek:".

Zet daarna de datum bij **Laatst bijgewerkt** goed (zie hieronder).

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

## Foto's toevoegen

- Maak de foto eerst kleiner: maximaal ongeveer 1200 pixels breed, als JPG, liefst onder de 400 KB.
- Geef het bestand een beschrijvende naam in kleine letters met streepjes, bijvoorbeeld `kerstboom-2026.jpg`, en zet het in de map `img/web/`.
- Zet in de HTML altijd een beschrijving (`alt="..."`) en de afmetingen (`width` en `height` in pixels) bij de foto.
- Zet geen originele, grote bestanden in de repository.
- Gebruik alleen foto's die je zelf hebt gemaakt of waarvoor je toestemming hebt.

## Afspraken in de code

Deze afspraken houden de site snel, vindbaar en privacyvriendelijk. Als je alleen tekst aanpast, hoef je er niets mee.

- **`?v=dev` achter bestandsnamen** (bijvoorbeeld `css/site.css?v=dev`) laten staan. Bij het publiceren wordt dit automatisch vervangen door een versienummer, zodat bezoekers nooit een oude versie uit hun browsercache zien.
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
