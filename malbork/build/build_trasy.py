# -*- coding: utf-8 -*-
"""Buduje przewodnik PDF: Malbork — Trasy zwiedzania w listopadzie (Wydanie studenckie)."""
import subprocess, html, os
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)          # katalog malbork/
HTML_PATH = os.path.join(OUT_DIR, "trasy.html")
PDF_PATH = os.path.join(OUT_DIR, "Malbork_trasy_zwiedzania_listopad.pdf")
MD_PATH = os.path.join(OUT_DIR, "TRASY_ZWIEDZANIA.md")


def find_chrome():
    """Szuka przeglądarki, która potrafi wydrukować PDF."""
    env = os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    candidates = [
        os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"),
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/snap/bin/chromium",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise SystemExit("Nie znalazłem Chrome/Chromium. Ustaw zmienną CHROME.")


CHROME = find_chrome()

CSS = """
@page { size: A4; margin: 12mm 13mm 12mm 13mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Noto Serif", Georgia, serif; font-size: 9.3pt;
       line-height: 1.45; color: #241c15; background: #fff; }
h1, h2, h3, h4, .sans { font-family: "Noto Sans", "Noto Sans Display", sans-serif; }
a { color: #8f3a2c; text-decoration: none; border-bottom: 0.4pt solid #d5b79c; }
p { margin: 0 0 2.2mm 0; }
ul, ol { margin: 0 0 2.2mm 0; padding-left: 5mm; }
li { margin-bottom: 1.1mm; }

/* cover */
.cover { position: relative; height: 268mm; padding: 14mm 14mm 12mm 14mm; overflow: hidden;
  background: linear-gradient(155deg, #fcf7ee 0%, #f6eedd 50%, #efe0c8 100%);
  border: 0.8pt solid #d9c6ae; }
.band { position: absolute; top: 0; right: 0; bottom: 0; width: 8mm;
  background: repeating-linear-gradient(0deg, #8f3a2c 0 4mm, #a24c39 4mm 8mm); }
.cv-top { position: relative; margin-top: 10mm; }
.kicker { font-size: 8pt; letter-spacing: 2.5pt; text-transform: uppercase;
  color: #8f3a2c; font-weight: 700; }
.cover h1 { font-size: 30pt; line-height: 1.08; margin: 6mm 0 0 0; color: #2a1a12;
  font-weight: 800; letter-spacing: -0.6pt; max-width: 130mm; }
.cover .sub { font-family: "Noto Sans", sans-serif; font-size: 10.5pt; color: #8f3a2c;
  margin-top: 4mm; font-weight: 600; }
.rule { height: 2.2pt; width: 32mm; background: #8f3a2c; margin: 6mm 0; }
.cover .lead { font-size: 10.5pt; line-height: 1.5; color: #4a3a2c; max-width: 126mm; }

.badges { display: flex; gap: 4mm; margin-top: 5mm; }
.badge { background: #8f3a2c; color: #fff; padding: 1.5mm 3.5mm; font-size: 8pt;
  font-family: "Noto Sans", sans-serif; font-weight: 700; border-radius: 2mm; }
.badge.gold { background: #b8894a; }

.highlights { position: absolute; left: 14mm; right: 22mm; bottom: 68mm; }
.highlights h3 { margin: 0 0 2mm 0; font-size: 9.5pt; color: #8f3a2c; text-transform: uppercase; letter-spacing: 1pt; }
.hl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; }
.hl-item { background: rgba(255,255,255,0.7); border: 0.5pt solid #d9c6ae; padding: 2.5mm 3mm; border-radius: 1.5mm; }
.hl-item b { display: block; font-family: "Noto Sans", sans-serif; font-size: 9pt; color: #2a1a12; margin-bottom: 0.5mm; }
.hl-item span { font-size: 8pt; color: #5a4838; line-height: 1.35; display: block; }

.facts { position: absolute; left: 14mm; right: 22mm; bottom: 25mm; display: flex; gap: 6mm; }
.fact { border-top: 0.8pt solid #cbb397; padding-top: 2.2mm; flex: 1; }
.fact b { display: block; font-family: "Noto Sans", sans-serif; font-size: 14pt; color: #8f3a2c; }
.fact span { font-size: 7.8pt; color: #6b5744; }
.cv-foot { position: absolute; left: 14mm; right: 22mm; bottom: 10mm; font-size: 7.6pt; color: #7a6350; }

/* sections */
.newpage { break-before: page; }
h2.sec { font-size: 14.5pt; margin: 0 0 3mm 0; padding-bottom: 2mm;
  border-bottom: 2pt solid #8f3a2c; color: #2a1a12; font-weight: 800;
  letter-spacing: -0.2pt; break-after: avoid; }
h2.sec .num { color: #b8894a; font-weight: 800; margin-right: 2.4mm; }
h3 { font-size: 10.5pt; margin: 3.8mm 0 1.5mm 0; color: #8f3a2c; font-weight: 700; break-after: avoid; }
h4 { font-size: 7.6pt; margin: 0 0 1.2mm 0; letter-spacing: 1.3pt; text-transform: uppercase;
  color: #8a6a4a; font-weight: 700; }
.lede { font-size: 9.8pt; color: #4a3a2c; line-height: 1.48; margin-bottom: 3mm; }

.box { background: #faf5ea; border: 0.6pt solid #e3d2b8; border-left: 3pt solid #b8894a;
  padding: 3mm 3.8mm; margin: 0 0 3mm 0; break-inside: avoid; border-radius: 1mm; }
.box.dark { background: #f5ecdf; border-left-color: #8f3a2c; }
.box.tip { background: #eef6f0; border-color: #c0dec8; border-left-color: #2e7d32; }
.box.warn { background: #fdf5ea; border-color: #edd1a9; border-left-color: #d97706; }
.box h3 { margin-top: 0; }
.box p:last-child, .box ul:last-child, .box ol:last-child { margin-bottom: 0; }

table { width: 100%; border-collapse: collapse; font-size: 8.5pt; margin-bottom: 3mm; }
th { text-align: left; font-family: "Noto Sans", sans-serif; font-size: 7.2pt; letter-spacing: 1pt;
  text-transform: uppercase; color: #8a6a4a; border-bottom: 1.2pt solid #c9a58c; padding: 1mm 2mm 1.5mm 0; }
td { padding: 1.2mm 2mm 1.2mm 0; border-bottom: 0.4pt solid #eadcc8; vertical-align: top; }
td.cost { font-family: "Noto Sans", sans-serif; font-weight: 700; color: #8f3a2c; white-space: nowrap; }
td.time { font-family: "Noto Sans", sans-serif; font-weight: 700; color: #b8894a; white-space: nowrap; }
tr:last-child td { border-bottom: none; }
tr.total { font-weight: 700; background: #faf5ea; }
tr.total td { border-top: 1.2pt solid #8f3a2c; border-bottom: 1.2pt solid #8f3a2c; padding-top: 2mm; padding-bottom: 2mm; }

/* itinerary items */
.timeline { display: flex; flex-direction: column; gap: 2.8mm; margin-bottom: 3.5mm; }
.tl-item { display: flex; gap: 3.5mm; background: #fdfbf7; border: 0.5pt solid #e6d8c3;
  padding: 2.6mm 3mm; border-radius: 1.2mm; break-inside: avoid; }
.tl-time { flex: 0 0 24mm; font-family: "Noto Sans", sans-serif; font-size: 8.5pt;
  font-weight: 700; color: #8f3a2c; border-right: 1.5pt solid #b8894a; padding-right: 2.5mm; }
.tl-time .dur { display: block; font-size: 7.2pt; font-weight: 400; color: #7a6350; }
.tl-body { flex: 1; }
.tl-title { font-family: "Noto Sans", sans-serif; font-size: 9.2pt; font-weight: 700; color: #2a1a12; margin-bottom: 0.8mm; }
.tl-desc { font-size: 8.4pt; color: #423528; line-height: 1.38; }
.tl-desc p { margin: 0 0 1.2mm 0; }
.tl-desc p:last-child { margin: 0; }
.tag { display: inline-block; font-family: "Noto Sans", sans-serif; font-size: 6.8pt;
  background: #f0e6d6; color: #734825; padding: 0.4mm 1.8mm; border-radius: 1mm; font-weight: 600; margin-right: 1.5mm; }

.cols-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; }
.col-card { background: #faf5ea; border: 0.6pt solid #e3d2b8; padding: 3mm 3.5mm; border-radius: 1mm; break-inside: avoid; }
.col-card h4 { margin-top: 0; margin-bottom: 1.5mm; color: #8f3a2c; font-size: 8.5pt; letter-spacing: 0.5pt; }
.col-card p { font-size: 8.3pt; line-height: 1.38; margin: 0; }

.footer-nav { font-size: 7.4pt; color: #8a7360; text-align: center; margin-top: 4mm;
  border-top: 0.5pt solid #e3d2b8; padding-top: 1.5mm; }
"""


def build_html():
    html_out = f"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<title>Malbork — Trasy zwiedzania w listopadzie</title>
<style>{CSS}</style>
</head>
<body>

<!-- STRONA 1: OKŁADKA -->
<div class="cover">
  <div class="band"></div>
  <div class="cv-top">
    <div class="kicker">Kompletny przewodnik terenowy · Edycja studencka</div>
    <h1>Trasy zwiedzania Malborka</h1>
    <div class="sub">Wszystkie części miasta krok po kroku · Sezon jesienno-zimowy (połowa listopada)</div>
    <div class="rule"></div>
    <div class="lead">
      Kompleksowy plan zwiedzania całego Malborka bez pomijania żadnej dzielnicy.
      Zaprojektowany specjalnie na krótkie listopadowe dni.
      Maksymalizuje czas dziennego światła.
      Optymalizuje wydatki dzięki ulgom studenckim i darmowej komunikacji miejskiej.
    </div>
    <div class="badges">
      <span class="badge">Trasa 1-dniowa (Ekspresowa)</span>
      <span class="badge gold">Trasa 2-dniowa (Kompletna)</span>
      <span class="badge">Budżet studenta</span>
    </div>
  </div>

  <div class="highlights">
    <h3>Co obejmuje ten przewodnik</h3>
    <div class="hl-grid">
      <div class="hl-item">
        <b>1. Zamek Krzyżacki (UNESCO)</b>
        <span>Zamek Niski (Przedzamcze), Zamek Średni z Pałacem Wielkich Mistrzów, Zamek Wysoki, Gdanisko oraz Wały von Plauena.</span>
      </div>
      <div class="hl-item">
        <b>2. Nadbrzeże Nogatu i Kałdowo</b>
        <span>Kładka piesza, bulwar Macieja Kilarskiego i najsłynniejsza panorama zamku od zachodniej strony rzeki.</span>
      </div>
      <div class="hl-item">
        <b>3. Średniowieczne Stare Miasto</b>
        <span>Ratusz Staromiejski, Brama Mariacka, Brama Garncarska, mury miejskie, kościół św. Jana i Szkoła Łacińska.</span>
      </div>
      <div class="hl-item">
        <b>4. Nowożytne Śródmieście i Wielbark</b>
        <span>Zabytkowy dworzec PKP, neogotycka Wieża Ciśnień, Muzeum Miasta w willi Flötera oraz Cmentarz Wojenny Wspólnoty Brytyjskiej.</span>
      </div>
    </div>
  </div>

  <div class="facts">
    <div class="fact">
      <b>32–36 zł</b>
      <span>Całkowity koszt 1 dnia (bilet + obiad)</span>
    </div>
    <div class="fact">
      <b>0 zł</b>
      <span>Autobusy MZK Malbork (darmowe dla każdego)</span>
    </div>
    <div class="fact">
      <b>1 zł</b>
      <span>Bilet studencki do Muzeum Zamkowego</span>
    </div>
    <div class="fact">
      <b>15:50</b>
      <span>Zachód słońca (kluczowy punkt planu)</span>
    </div>
  </div>

  <div class="cv-foot">
    Listopad 2026 · Opracowano na podstawie aktualnych harmonogramów Muzeum Zamkowego, MZK Malbork i Urzędu Miasta.
  </div>
</div>

<!-- STRONA 2: LOGISTYKA LISTOPADA I KOSZTORYS -->
<div class="newpage">
  <h2 class="sec"><span class="num">01</span> Realia listopada i budżet studenta</h2>
  <div class="lede">
    Zwiedzanie Malborka w połowie listopada ma ogromną zaletę: brak letnich tłumów i kolejek.
    Wymaga jednak żelaznej dyscypliny czasowej. Słońce zachodzi przed godziną 16:00.
  </div>

  <div class="box warn">
    <h3>Złote zasady listopada w Malborku</h3>
    <ul>
      <li><b>Krótki dzień:</b> Wschód słońca o 7:15, zachód już o 15:50. Po 16:15 zapada zupełny zmrok.</li>
      <li><b>Godziny zamku w sezonie zimowym:</b> Wnętrza są czynne od 9:00 do 15:00. Ostatnie wejście na Trasę Historyczną następuje o 12:45.</li>
      <li><b>Nigdy w poniedziałek:</b> W poniedziałki wnętrza zamkowe są zamknięte. Działa tylko trasa spacerowa po dziedzińcach. Wybierz dni od wtorku do niedzieli.</li>
      <li><b>Złota godzina fotograficzna:</b> W listopadzie najpiękniejsze światło na zamek od strony Nogatu jest między 13:45 a 15:15.</li>
    </ul>
  </div>

  <h3>Kalkulacja kosztów (Status studenta)</h3>
  <table>
    <thead>
      <tr>
        <th>Atrakcja / Wydatek</th>
        <th>Szczegóły i warunki</th>
        <th>Standard</th>
        <th>Student</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Zamek w Malborku (Trasa Historyczna)</b></td>
        <td>Program rządowy „Muzeum za 1 zł” (do 26 r.ż. z legitymacją) · audioprzewodnik w cenie</td>
        <td>80,00 zł</td>
        <td class="cost">1,00 zł*</td>
      </tr>
      <tr>
        <td><b>Muzeum Miasta Malborka</b></td>
        <td>Willa Flötera, ul. Kościuszki 54 · Wystawa o Stalagu XX-B i powojennym Malborku</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Zabytkowa Wieża Ciśnień</b></td>
        <td>Plac Słowiański · Taras widokowy na miasto</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Średniowieczne Stare Miasto i Plenery</b></td>
        <td>Ratusz, Brama Garncarska, Brama Mariacka, kościół św. Jana, kładka na Nogacie</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Centrum Kultury „Szkoła Łacińska”</b></td>
        <td>Zrekonstruowany gmach nad rzeką (wejście do wnętrz i na taras bezpłatne)</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Cmentarz Wojenny Wspólnoty Brytyjskiej</b></td>
        <td>Wielbark · Miejsce pamięci lotników RAF i ofiar Stalagu XX-B</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Komunikacja miejska (MZK Malbork)</b></td>
        <td>Wszystkie linie autobusowe w granicach miasta są całkowicie bezpłatne</td>
        <td>0,00 zł</td>
        <td class="cost">0,00 zł</td>
      </tr>
      <tr>
        <td><b>Ciepły posiłek / Obiad studencki</b></td>
        <td>Bar mleczny / bistro w centrum miasta (np. Bar Bis, Bistro na Fali)</td>
        <td>32,00 zł</td>
        <td class="cost">28,00 zł</td>
      </tr>
      <tr class="total">
        <td><b>RAZEM CAŁY DZIEŃ W MALBORKU</b></td>
        <td>Wszystkie zabytki miasta + zamek + transport + obiad</td>
        <td>112,00 zł</td>
        <td class="cost">29,00 zł</td>
      </tr>
    </tbody>
  </table>

  <div class="box tip">
    <h3>Wskazówka dotycząca biletu za 1 zł</h3>
    <p>
      Muzeum Zamkowe w Malborku realizuje program ministerialny, który umożliwia zakup biletu na Trasę Historyczną za symboliczną kwotę <b>1 zł</b> dzieciom i młodzieży uczącej się oraz studentom do ukończenia 26 roku życia.
      W kasie lub przy kontroli koniecznie pokaż <b>ważną fizyczną lub elektroniczną (mLegitymacja) legitymację studencką</b>.
      Gdyby pula dzienna była wyczerpana lub wiek przekraczał 26 lat, standardowy bilet ulgowy poza sezonem kosztuje 60 zł.
    </p>
  </div>

  <div class="box dark">
    <h3>Darmowa komunikacja MZK</h3>
    <p>
      Od lipca 2022 roku wszystkie autobusy MZK w granicach Malborka kursują bezpłatnie. Nie kupujesz żadnych biletów ani nie kasujesz kart. Wsiadasz na dworcu PKP i jedziesz bezpośrednio pod zamek lub do oddalonej dzielnicy Wielbark.
    </p>
  </div>
</div>

<!-- STRONA 3: TOPOGRAFIA I LOGICZNY UKŁAD MIASTA -->
<div class="newpage">
  <h2 class="sec"><span class="num">02</span> Anatomia Malborka: Pięć rejonów do odkrycia</h2>
  <div class="lede">
    Większość turystów popełnia błąd: wysiada z pociągu, idzie do zamku i natychmiast wraca.
    Malbork to jednak wielowarstwowy organizm o unikalnej historii. Poniższa mapa obszarów pozwoli Ci poznać każde skrzydło miasta bez zbędnych kilometrów.
  </div>

  <div class="cols-2">
    <div class="col-card">
      <h4>Obszar A: Zespół Zamkowy</h4>
      <p>
        <b>Charakter:</b> Największa ceglana twierdza Europy.<br>
        <b>Co obejmuje:</b> Przedzamcze z Karwanem i infirmerią, Zamek Średni z Pałacem Wielkich Mistrzów i Wielkim Refektarzem, Zamek Wysoki z kościołem NMP i Złotą Bramą, wieżę Gdanisko, mury fosy oraz ziemne Wały von Plauena z 1410 roku.<br>
        <b>Czas zwiedzania:</b> 4,0–4,5 godziny.
      </p>
    </div>
    <div class="col-card">
      <h4>Obszar B: Kałdowo i Rzeka Nogat</h4>
      <p>
        <b>Charakter:</b> Punkt widokowy i nadrzeczny bulwar.<br>
        <b>Co obejmuje:</b> Przejście nowoczesną kładką pieszą przez rzekę Nogat na prawy brzeg (Kałdowo). Widok na potężną ścianę Zamku Wysokiego i Pałacu Wielkich Mistrzów odbijających się w wodzie.<br>
        <b>Czas zwiedzania:</b> 45 minut (najlepiej o 13:45–14:30).
      </p>
    </div>
  </div>

  <div style="height: 3.5mm;"></div>

  <div class="cols-2">
    <div class="col-card">
      <h4>Obszar C: Średniowieczne Stare Miasto</h4>
      <p>
        <b>Charakter:</b> Zniszczone w 1945 r., zachowało gotycki rdzeń.<br>
        <b>Co obejmuje:</b> Gotycki Ratusz Staromiejski z XIV w. ze sterczynami, Brama Garncarska (Elbląska), Brama Mariacka (Sztumska), fragmenty gotyckich murów obronnych, XIV-wieczny kościół farny św. Jana Chrzciciela i Szkoła Łacińska.<br>
        <b>Czas zwiedzania:</b> 1,5 godziny.
      </p>
    </div>
    <div class="col-card">
      <h4>Obszar D: Nowe Miasto i Śródmieście XIX w.</h4>
      <p>
        <b>Charakter:</b> Pruski rozkwit po doprowadzeniu kolei.<br>
        <b>Co obejmuje:</b> Dworzec Kolejowy z 1891 r. (neogotyk, stropy, witraże), neogotycka Wieża Ciśnień z 1905 r. przy Placu Słowiańskim, secesyjna Willa Flötera (Muzeum Miasta) oraz deptak przy ul. Kościuszki z pomnikiem króla Kazimierza Jagiellończyka.<br>
        <b>Czas zwiedzania:</b> 1,5–2,0 godziny.
      </p>
    </div>
  </div>

  <div style="height: 3.5mm;"></div>

  <div class="box">
    <h4>Obszar E: Dzielnica Wielbark (Pamięć XX wieku)</h4>
    <p>
      <b>Charakter:</b> Południowa dzielnica Malborka, związana z dramatyczną historią II wojny światowej.<br>
      <b>Co obejmuje:</b> Cmentarz Wojenny Wspólnoty Brytyjskiej (Malbork Commonwealth War Cemetery) oraz pomnik jeńców wojennych Stalagu XX-B. Spoczywa tu ponad 200 żołnierzy brytyjskich, kanadyjskich i nowozelandzkich oraz lotników RAF. Niezwykle klimatyczne i ciche miejsce pamięci w otoczeniu starych drzew.<br>
      <b>Dojazd:</b> Bezpłatny autobus MZK linii 1 lub 6 z przystanku pod dworcem lub z centrum prosto pod cmentarz (ok. 10 minut).
    </p>
  </div>

  <div class="box tip">
    <h3>Dlaczego taka kolejność gwarantuje najwyższą wydajność?</h3>
    <p>
      Układ Malborka jest liniowo-promienisty wzdłuż rzeki Nogat i linii kolejowej.
      Najbardziej wydajna trasa zaczyna się na ZAMKU z samego rana.
      Dzięki temu unikasz ryzyka zamknięcia wystaw wewnętrznych (wstęp tylko do 12:45!).
      Następnie wychodzisz dokładnie na zachodni brzeg rzeki w momencie, gdy słońce stoi najniżej i najlepiej doświetla gotyckie cegły.
      Wszystkie obiekty miejskie i muzealne w centrum zwiedzasz w drodze powrotnej w kierunku dworca PKP.
    </p>
  </div>
</div>

<!-- STRONA 4: TRASA JEDNODNIOWA (EKSPRESOWA I DOKŁADNA) -->
<div class="newpage">
  <h2 class="sec"><span class="num">03</span> Plan 1-Dniowy: Od świtu do zmierzchu</h2>
  <div class="lede">
    Trasa zoptymalizowana dla osób przyjeżdżających pociągiem rano. Pozwala zobaczyć wszystkie kluczowe punkty miasta w ciągu jednego, intensywnego dnia w listopadzie.
  </div>

  <div class="timeline">
    <div class="tl-item">
      <div class="tl-time">08:15 – 08:45<span class="dur">30 min</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">START</span>Dworzec PKP Malbork i przejście do Zamku</div>
        <div class="tl-desc">
          Wysiądź z pociągu. Obejrzyj zabytkową halę dworcową z 1891 roku: rzeźbione modrzewiowe stropy, kute latarnie i herby pruskich miast. Przejdź ul. Dworcową i Kościuszki w stronę zamku (15 minut pieszo lub bezpłatny autobus MZK nr 1/6 do przystanku „Plac Słowiański”).
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">08:45 – 09:00<span class="dur">15 min</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">KASY</span>Kasy Muzeum Zamkowego i odbiór audioprzewodnika</div>
        <div class="tl-desc">
          Kup bilet w ramach akcji „Muzeum za 1 zł” (okaż legitymację studencką). Pobierz audioprzewodnik w cenie biletu. Sprzęt samoczynnie uruchamia nagrania w odpowiednich salach.
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">09:00 – 13:15<span class="dur">4h 15m</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">RDZEŃ</span>Wielkie zwiedzanie Zespołu Zamkowego (Trasa Historyczna)</div>
        <div class="tl-desc">
          <p><b>1. Zamek Średni:</b> Dziedziniec, piwnice gospodarcze, Pałac Wielkich Mistrzów z arcydziełami gotyku świeckiego (Refektarz Letni i Zimowy), Wielki Refektarz ze sklepieniem palmowym, wystawa bursztynu i zbrojownia z militariami.</p>
          <p><b>2. Zamek Wysoki:</b> Przejście przez most zwodzony. Dziedziniec krużgankowy ze studnią pelikana, Kościół NMP ze zrekonstruowaną figurą Madonny, krypta św. Anny (groby mistrzów), dormitoria, kuchnia konwentu.</p>
          <p><b>3. Gdanisko i Tarasy:</b> Długi arkadowy ganek prowadzący do wieży ustępowej. Wyjście na tarasy zewnętrzne, cmentarz braci zakonnych i mury obronne.</p>
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">13:15 – 14:00<span class="dur">45 min</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">PANORAMA</span>Kładka na Nogacie i Punkt Widokowy Kałdowo</div>
        <div class="tl-desc">
          Zejdź na Bulwar Macieja Kilarskiego. Przejdź nowoczesną kładką pieszą na zachodni brzeg rzeki Nogat do Kałdowa. O tej porze listopadowe słońce miękko oświetla zachodnią fasadę twierdzy. To najlepsze miejsce na legendarne zdjęcia całego zamku odbijającego się w rzece.
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">14:00 – 15:15<span class="dur">1h 15m</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">MIASTO</span>Średniowieczne Stare Miasto Malborka</div>
        <div class="tl-desc">
          Wróć kładką. Zwiedź gotycki <b>kościół św. Jana Chrzciciela</b> z XIV w. (fara miejska). Zobacz <b>Szkołę Łacińską</b> nad brzegiem Nogatu, a następnie wejdź na dawny rynek: zobacz gotycki <b>Ratusz Staromiejski</b> (ok. 1380 r.) z ozdobnymi sterczynami, potężną <b>Bramę Garncarską</b> oraz zachowaną <b>Bramę Mariacką</b> wraz z odcinkiem murów obronnych.
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">15:15 – 16:15<span class="dur">1h 00m</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">POSIŁEK</span>Ciepły obiad studencki w centrum</div>
        <div class="tl-desc">
          Przejdź w stronę Placu Kazimierza Jagiellończyka i ul. Kościuszki. Zjedz rozgrzewający posiłek (np. Bar Bis lub Bistro na Fali, ceny dań obiadowych: 22–30 zł). O 15:50 zachodzi słońce – miasto zaczyna rozbłyskiwać iluminacjami.
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">16:15 – 17:30<span class="dur">1h 15m</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">KLIMAT</span>Wieża Ciśnień, Muzeum Miasta i nocny Malbork</div>
        <div class="tl-desc">
          Podejdź na Plac Słowiański pod neogotycką Wieżę Ciśnień (1905 r.) przypominającą obronną basztę. Zobacz zabytkową willę Flötera (Muzeum Miasta Malborka) przy ul. Kościuszki 54. Wieczorny spacer rozświetlonym deptakiem pod pomnik króla Kazimierza Jagiellończyka.
        </div>
      </div>
    </div>

    <div class="tl-item">
      <div class="tl-time">17:30 – 18:00<span class="dur">30 min</span></div>
      <div class="tl-body">
        <div class="tl-title"><span class="tag">KONIEC</span>Powrót na Dworzec PKP</div>
        <div class="tl-desc">
          Spacer powrotny w stronę dworca kolejowego. Odbiór gorącej herbaty i powrót pociągiem.
        </div>
      </div>
    </div>
  </div>
</div>

<!-- STRONA 5: TRASA DWUDNIOWA (WEEKENDOWA) I PORADY -->
<div class="newpage">
  <h2 class="sec"><span class="num">04</span> Wariant 2-Dniowy: Kompleksowy weekend</h2>
  <div class="lede">
    Jeśli dysponujesz weekendem, podziel zwiedzanie na dwa dni. Daje to czas na spokojną analizę detali zamkowych i odwiedzenie oddalonej dzielnicy Wielbark bez pośpiechu.
  </div>

  <div class="cols-2">
    <div class="col-card">
      <h4>Dzień 1: Cały Zamek, Kałdowo i Wały Plauena</h4>
      <p><b>09:00–14:00:</b> Zamek Wysoki, Średni i Niski. Bardzo dokładne przejście wszystkich sal, wystawy bursztynu i broni.</p>
      <p style="margin-top: 1.5mm;"><b>14:00–15:00:</b> Przejście na Kałdowo przez kładkę na złotą godzinę fotograficzną.</p>
      <p style="margin-top: 1.5mm;"><b>15:00–16:00:</b> Zewnętrzny pierścień obronny: Wały von Plauena, sucha fosa i baszta Maślankowa od strony północno-wschodniej.</p>
      <p style="margin-top: 1.5mm;"><b>16:30–18:30:</b> Obiad, kawa i wieczorny spacer wzdłuż podświetlonych murów zamkowych nad Nogatem.</p>
    </div>
    <div class="col-card">
      <h4>Dzień 2: Miejskie dziedzictwo i Wielbark</h4>
      <p><b>09:30–11:30:</b> Stare Miasto: Ratusz, Bramy, kościół św. Jana, Szkoła Łacińska (opcjonalny seans w planetarium za 13 zł).</p>
      <p style="margin-top: 1.5mm;"><b>11:45–13:15:</b> Muzeum Miasta Malborka (ul. Kościuszki 54) – wystawa o losach miasta i obozie Stalag XX-B.</p>
      <p style="margin-top: 1.5mm;"><b>13:30–15:00:</b> Przejazd darmowym autobusem MZK (linia 1) do Wielbarka. Zwiedzanie Cmentarza Wojennego Wspólnoty Brytyjskiej.</p>
      <p style="margin-top: 1.5mm;"><b>15:15–16:30:</b> Wieża Ciśnień, punkt widokowy, obiad na deptaku i powrót na zabytkowy Dworzec PKP.</p>
    </div>
  </div>

  <h3>Praktyczny poradnik studenta na listopad</h3>
  <div class="box tip">
    <h4>Ubiór i wyposażenie na zamek w chłodne dni</h4>
    <ul>
      <li><b>Zimne kamienne mury:</b> W salach zamkowych i krużgankach panuje niska temperatura (często taka sama jak na zewnątrz, ok. 3–6°C). Ubierz się na cebulkę.</li>
      <li><b>Wygodne buty z dobrą podeszwą:</b> Schody gotyckie, kocie łby i strome podejścia na wieże wymagają stabilnego, nieślizgającego się obuwia.</li>
      <li><b>Powerbank i słuchawki:</b> Niska temperatura szybko rozładowuje telefon. Jeśli używasz telefonu do zdjęć lub audioprzewodnika, miej ze sobą przenośną baterię.</li>
      <li><b>Własny mały termos:</b> Gorąca herbata pita na tarasach zamkowych z widokiem na Nogat ratuje przed wychłodzeniem.</li>
    </ul>
  </div>

  <div class="box dark">
    <h4>Gdzie tanio i smacznie zjeść w Malborku?</h4>
    <ul>
      <li><b>Bar Bis (ul. Kościuszki 14):</b> Tradycyjne obiady domowe, zupy, pierogi i kotlety. Duże porcje w studenckich cenach (zestaw 22–28 zł).</li>
      <li><b>Bistro na Fali / Przystanek Nogat (bulwar):</b> Ciepłe zupy rybne, dania obiadowe i kawa z widokiem na rzekę.</li>
      <li><b>Cukiernia Jędruś (ul. Mickiewicza / Kościuszki):</b> Legendarna lokalna cukiernia, znana ze świeżych drożdżówek i ciast.</li>
    </ul>
  </div>

  <div class="box">
    <h4>Wskazówki transportowe (Pociągi PKP)</h4>
    <p>
      Malbork jest znakomicie skomunikowany dzięki magistrali kolejowej Warszawa–Gdańsk.
      Studenci korzystają z ustawowej ulgi <b>51%</b> na wszystkie pociągi TLK, IC i Polregio.
      Dojazd z Trójmiasta pociągiem Regio trwa zaledwie 35–45 minut (koszt biletu studenckiego: ok. 9,50 zł).
      Z Warszawy dojedziesz pociągiem IC w ok. 2 godziny 15 minut (bilet studencki od 32 zł).
    </p>
  </div>

  <div class="footer-nav">
    Przewodnik po Malborku · Repozytorium zwiedzanie · r0D7ynki · Listopad 2026
  </div>
</div>

</body>
</html>
"""
    return html_out


def build_markdown():
    """Generuje wersję Markdown do czytania na GitHubie."""
    md = """# Malbork — Trasy zwiedzania w listopadzie (Wydanie studenckie)

Kompleksowy plan zwiedzania całego Malborka bez pomijania żadnej dzielnicy.
Zaprojektowany specjalnie na krótkie listopadowe dni.
Maksymalizuje czas dziennego światła i optymalizuje budżet dzięki ulgom studenckim oraz darmowej komunikacji miejskiej.

PDF do druku znajdziesz w pliku: [Malbork_trasy_zwiedzania_listopad.pdf](Malbork_trasy_zwiedzania_listopad.pdf).

---

## 1. Kluczowe realia listopada

1. **Krótki dzień:** Wschód słońca ok. 7:15, zachód słońca już o **15:50**. Po 16:15 zapada pełen zmrok.
2. **Godziny zamku:** Wnętrza i wystawy są otwarte od wtorku do niedzieli w godzinach **9:00 – 15:00**. Ostatnie wejście na Trasę Historyczną jest możliwe o **12:45**.
3. **Uwaga na poniedziałki:** W poniedziałki wnętrza są nieczynne (dostępna jest tylko bezpłatna trasa spacerowa po dziedzińcach). Wybierz zwiedzanie od wtorku do niedzieli.
4. **Złota godzina:** Najlepsze światło fotograficzne na zamek od strony rzeki Nogat panuje w godzinach **13:45 – 15:15**.

---

## 2. Kosztorys studenta

| Atrakcja / Pozycja | Informacje i warunki | Standard | Student |
|:-------------------|:---------------------|---------:|--------:|
| **Zamek w Malborku (Trasa Historyczna)** | Program „Muzeum za 1 zł” (do 26 r.ż. z legitymacją) · audioprzewodnik w cenie | 80,00 zł | **1,00 zł** |
| **Muzeum Miasta Malborka** | Willa Flötera, ul. Kościuszki 54 · Wystawa o Stalagu XX-B | 0,00 zł | **0,00 zł** |
| **Wieża Ciśnień (punkt widokowy)** | Plac Słowiański · Neogotyk z 1905 roku | 0,00 zł | **0,00 zł** |
| **Stare Miasto i plenery** | Ratusz, Brama Garncarska, Brama Mariacka, kościół św. Jana, mury | 0,00 zł | **0,00 zł** |
| **Kładka na Nogacie i punkt Kałdowo** | Najlepsza panorama zamku od zachodniej strony | 0,00 zł | **0,00 zł** |
| **Szkoła Łacińska** | Zrekonstruowany obiekt nad brzegiem Nogatu | 0,00 zł | **0,00 zł** |
| **Cmentarz Wojenny Wspólnoty Brytyjskiej** | Wielbark · Groby lotników RAF i ofiar Stalagu XX-B | 0,00 zł | **0,00 zł** |
| **Komunikacja MZK Malbork** | Wszystkie autobusy miejskie są bezpłatne od 2022 roku | 0,00 zł | **0,00 zł** |
| **Ciepły obiad studencki** | Tradycyjne danie obiadowe w centrum (np. Bar Bis) | 32,00 zł | **28,00 zł** |
| **SUMA CAŁY DZIEŃ** | **Kompletne zwiedzanie miasta z obiadem** | **112,00 zł** | **29,00 zł** |

*Uwaga:* Jeśli wyczerpie się pula programu „Muzeum za 1 zł” lub wiek przekracza 26 lat, bilet ulgowy poza sezonem kosztuje 60,00 zł.

---

## 3. Pięć obszarów Malborka

- **Obszar A: Zespół Zamkowy (UNESCO):** Zamek Niski (Przedzamcze, Karwan, infirmeria), Zamek Średni (Pałac Wielkich Mistrzów, Wielki Refektarz, wystawa bursztynu, militaria), Zamek Wysoki (krużganki, studnia z pelikanem, kościół NMP, Złota Brama, krypta św. Anny), Gdanisko i Wały von Plauena.
- **Obszar B: Kałdowo i Rzeka Nogat:** Kładka piesza, bulwar Macieja Kilarskiego i słynny punkt widokowy z panoramą zamku odbijającego się w rzece.
- **Obszar C: Średniowieczne Stare Miasto:** Gotycki Ratusz Staromiejski z XIV w., Brama Garncarska, Brama Mariacka, fragmenty gotyckich murów obronnych, kościół św. Jana Chrzciciela i Szkoła Łacińska.
- **Obszar D: Nowe Miasto i Śródmieście XIX w.:** Dworzec Kolejowy (1891 r., neogotyk), neogotycka Wieża Ciśnień (1905 r.), willa Flötera (Muzeum Miasta) i deptak przy ul. Kościuszki z pomnikiem króla Kazimierza Jagiellończyka.
- **Obszar E: Dzielnica Wielbark (Historia XX w.):** Malbork Commonwealth War Cemetery (cmentarz aliancki) oraz miejsce pamięci niemieckiego obozu jenieckiego Stalag XX-B.

---

## 4. Najbardziej wydajna trasa 1-dniowa (Ekspresowa)

| Godzina | Miejsce | Co robisz |
|:--------|:--------|:----------|
| **08:15 – 08:45** | **Dworzec PKP** | Przyjazd pociągiem. Podziwiasz neogotycką architekturę dworca z 1891 r. Idziesz pieszo (15 min) lub jedziesz darmowym autobusem MZK (linia 1 lub 6) pod zamek. |
| **08:45 – 09:00** | **Kasy zamkowe** | Kupujesz bilet w programie „Muzeum za 1 zł” (pokazujesz legitymację). Odbierasz audioprzewodnik. |
| **09:00 – 13:15** | **Muzeum Zamkowe** | Zwiedzasz cały zamek z audioprzewodnikiem: Zamek Średni (Wielki Refektarz, Pałac Wielkich Mistrzów, bursztyny), Zamek Wysoki (kościół NMP, krypta św. Anny), wieżę Gdanisko i tarasy. |
| **13:15 – 14:00** | **Kładka i Kałdowo** | Schodzisz na bulwar nad Nogatem. Przechodzisz kładką do Kałdowa na prawy brzeg. Oglądasz panoramę zamku w najlepszym popołudniowym świetle. |
| **14:00 – 15:15** | **Stare Miasto** | Zwiedzasz kościół św. Jana, Szkołę Łacińską, gotycki Ratusz Staromiejski, Bramę Garncarską, Bramę Mariacką i gotyckie mury obronne. |
| **15:15 – 16:15** | **Centrum / Obiad** | Ciepły obiad w centrum (Bar Bis lub Bistro na Fali). O 15:50 zachodzi słońce. |
| **16:15 – 17:30** | **Śródmieście nocą** | Neogotycka Wieża Ciśnień przy Placu Słowiańskim, willa Flötera (Muzeum Miasta Malborka) i spacer rozświetlonym deptakiem pod pomnik Kazimierza Jagiellończyka. |
| **17:30 – 18:00** | **Dworzec PKP** | Spacer powrotny na dworzec i wyjazd pociągiem. |

---

## 5. Plan 2-Dniowy (Weekendowy dla pasjonatów)

- **Dzień 1: Zamek Krzyżacki od podszewki i rzeka Nogat**
  - **Rano (09:00–14:00):** Wyczerpujące zwiedzanie wszystkich komnat Zamku Wysokiego, Średniego, zbrojowni i wystaw czasowych.
  - **Popołudnie (14:00–15:30):** Przejście na Kałdowo na zachód słońca. Obchód zewnętrznych bastionów: Wały von Plauena i sucha fosa.
  - **Wieczór (16:30–19:00):** Obiad, kawa i spacer po zmroku wzdłuż oświetlonych murów zamkowych nad Nogatem.
- **Dzień 2: Miejskie dziedzictwo i dzielnica Wielbark**
  - **Rano (09:30–11:30):** Dawne Stare Miasto: Ratusz, Bramy, fara św. Jana i Szkoła Łacińska.
  - **Przedpołudnie (11:45–13:00):** Muzeum Miasta Malborka w willi Flötera (wystawa o Stalagu XX-B i powojennych losach miasta).
  - **Wczesne popołudnie (13:15–15:00):** Przejazd darmowym autobusem MZK (linia 1) do Wielbarka. Zwiedzanie Cmentarza Wojennego Wspólnoty Brytyjskiej.
  - **Popołudnie (15:15–16:30):** Plac Słowiański, Wieża Ciśnień, posiłek i powrót na dworzec kolejowy.

---

## 6. Porady praktyczne

- **Ciepłe warstwy ubrań:** Kamienne mury zamkowe i nieogrzewane krużganki wychładzają organizm. Ubierz ciepłą bieliznę termiczną, czapkę i rękawiczki.
- **Obuwie:** Wybierz wygodne buty na grubej podeszwie. Gotyckie schody i bruk bywają śliskie w listopadzie.
- **Powerbank:** Chłód drastycznie skraca czas pracy baterii w telefonie.
- **Dojazd PKP:** Zniżka studencka 51% obowiązuje na wszystkie pociągi w Polsce. Z Gdańska dojedziesz w 35 minut, a z Warszawy w nieco ponad 2 godziny.
"""
    return md


if __name__ == "__main__":
    html_content = build_html()
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Zapisano HTML:", HTML_PATH)

    subprocess.run([
        CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", "--virtual-time-budget=4000",
        f"--print-to-pdf={PDF_PATH}", "file://" + HTML_PATH,
    ], check=True, capture_output=True)
    print("Wygenerowano PDF:", PDF_PATH)

    md_content = build_markdown()
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Zapisano Markdown:", MD_PATH)
