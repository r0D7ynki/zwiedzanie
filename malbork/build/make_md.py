# -*- coding: utf-8 -*-
"""Generuje wersję Markdown przewodnika (PLAN.md) z tych samych danych co PDF.

Uruchomienie:
    python3 build/make_md.py
"""
import os
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), "PLAN.md")


def pl_hours(n):
    """Odmiana słowa godzina: 1 godzina, 2-4 godziny, 5+ godzin."""
    if n == 1:
        return "godzina"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "godziny"
    return "godzin"


def esc(t):
    return t.replace("|", "\\|")


def main():
    L = []
    total = sum(int(s["time"].split()[0]) for s in B.STAGES)
    L.append("# Malbork i państwo krzyżackie — plan nauki\n")
    L.append("> 8 etapów · %d %s · 58 źródeł online · "
             "[PDF do druku](Malbork_plan_nauki_i_zrodla.pdf)\n" % (total, B.pl_hours(total)))
    L.append("Ten plan prowadzi od rozbicia dzielnicowego do współczesności. "
             "Najpierw pokazuje tło. Potem tłumaczy, jak powstało państwo zakonne. "
             "Następnie prowadzi przez wiek XIV i XV. Na końcu pokazuje, co stało się z zamkiem po 1466 roku.\n")
    L.append("Każdy etap ma trzy części: wydarzenia, źródła i pytania kontrolne. "
             "Strona daje szybki przegląd. Film pokazuje przebieg. Książka dodaje niuanse.\n")

    L.append("## Jak korzystać z tego planu\n")
    L.append("1. **Jeden etap to jeden wieczór.** Nie zaczynaj następnego, aż odpowiesz na pytania.")
    L.append("2. **Czytaj z mapą.** Zaznacz Malbork, Gdańsk, Toruń, Grunwald i Chojnice.")
    L.append("3. **Notuj daty i osoby.** Jedna kartka na etap wystarczy.")
    L.append("4. **Film traktuj jako wprowadzenie.** Książka daje tło i spór naukowy.")
    L.append("5. **Wracaj do pytań po tygodniu.** Powtórka utrwala wiedzę lepiej niż czytanie od nowa.\n")

    L.append("## Plan w skrócie\n")
    L.append("| Etap | Temat | Lata | Czas |")
    L.append("|:---:|:------|:-----|-----:|")
    for s in B.STAGES:
        L.append("| %d | %s | %s | %s |" % (s["n"], esc(s["title"]), s["years"], s["time"]))
    L.append("| | **Razem** | | **%d %s** |\n" % (total, B.pl_hours(total)))

    L.append("## Kalendarium\n")
    L.append("| Rok | Wydarzenie |")
    L.append("|:----|:-----------|")
    for y, e in B.TIMELINE_1 + B.TIMELINE_2:
        L.append("| %s | %s |" % (y, esc(e)))
    L.append("")

    L.append("## Etapy\n")
    for s in B.STAGES:
        L.append("### Etap %d. %s\n" % (s["n"], s["title"]))
        L.append("**Lata:** %s · **Czas:** %s\n" % (s["years"], s["time"]))
        L.append("**Cel:** %s\n" % s["goal"])
        L.append("**Co się wtedy działo**\n")
        for d, t in s["events"]:
            L.append("- **%s** — %s" % (d, t))
        L.append("\n**Źródła**\n")
        for label, url in s["web"]:
            L.append("- Strona: [%s](%s)" % (label, url))
        for label, url, note in s["video"]:
            extra = " (%s)" % note if note else ""
            L.append("- Wideo: [%s](%s)%s" % (label, url, extra))
        for label, note in s["books"]:
            extra = " — %s" % note if note else ""
            L.append("- Książka: *%s*%s" % (label, extra))
        L.append("\n**Sprawdź się**\n")
        for i, q in enumerate(s["quiz"], 1):
            L.append("%d. %s" % (i, q))
        L.append("")

    L.append("## Książki\n")
    L.append("| Autor | Tytuł | Wydanie | Po co |")
    L.append("|:------|:------|:--------|:-----|")
    for a, t, pub, why, url in B.BOOKS:
        link = " [opis](%s)" % url if url else ""
        L.append("| %s | *%s*%s | %s | %s |" % (a, t, link, pub, esc(why)))
    L.append("")

    L.append("## Wszystkie linki\n")
    cats, order = {}, []
    for label, url, cat in B.WEB_EXTRA:
        if cat not in cats:
            cats[cat] = []
            order.append(cat)
        cats[cat].append((label, url))
    names = {
        "instytucja": "Muzea i instytucje",
        "encyklopedia": "Wikipedia — punkt startowy, nie źródło naukowe",
        "artykuł": "Artykuły i portale historyczne",
        "lekcja": "Lekcje i materiały edukacyjne",
        "podcast": "Podcasty i audycje radiowe",
    }
    for cat in order:
        L.append("### %s\n" % names.get(cat, cat))
        for label, url in cats[cat]:
            L.append("- [%s](%s) — `%s`" % (label, url, unquote(url).split("//")[-1]))
        L.append("")

    L.append("### Wideo (YouTube)\n")
    for s in B.STAGES:
        for label, url, note in s["video"]:
            L.append("- [%s](%s)" % (label, url))
    L.append("")

    L.append("## Ściąga\n")
    L.append("### Dwanaście dat\n")
    L.append("| Rok | Co się stało |")
    L.append("|:----|:-------------|")
    dates = [
        ("1226", "Konrad Mazowiecki zaprasza Krzyżaków."),
        ("1230", "Początek podboju Prus."),
        ("1280", "Prawa miejskie Malborka."),
        ("1309", "Malbork stolicą Zakonu."),
        ("1343", "Pokój w Kaliszu."),
        ("1385", "Unia w Krewie."),
        ("1410", "Grunwald i oblężenie Malborka."),
        ("1411", "I pokój toruński."),
        ("1440", "Związek Pruski."),
        ("1454", "Wybuch wojny trzynastoletniej."),
        ("1466", "II pokój toruński."),
        ("1945", "Zniszczenie zamku i odbudowa."),
    ]
    for y, e in dates:
        L.append("| %s | %s |" % (y, e))
    L.append("")
    L.append("### Sześć postaci\n")
    for line in [
        "**Konrad I Mazowiecki** — zaprosił Zakon do Polski.",
        "**Hermann von Salza** — wielki mistrz, który zbudował podstawy państwa.",
        "**Winrich von Kniprode** — wielki mistrz w złotym wieku Zakonu.",
        "**Ulrich von Jungingen** — wielki mistrz poległy pod Grunwaldem.",
        "**Heinrich von Plauen** — obrońca Malborka w 1410 roku.",
        "**Kazimierz Jagiellończyk** — przyjął Malbork do Polski w 1457 roku.",
    ]:
        L.append("- " + line)
    L.append("")
    L.append("### Jak sprawdzać źródła\n")
    for line in [
        "Porównaj dwie daty. Jeśli źródła się różnią, sprawdź trzecie.",
        "Sprawdź autora. Muzeum i uniwersytet mają większą wagę niż blog.",
        "Wikipedia to start, nie koniec. Zjedź na dół i przeczytaj bibliografię.",
        "Odróżniaj powieść od historii. Sienkiewicz pisał literaturę, Długosz kronikę ze swoim zdaniem.",
        "Uważaj na liczby. „Największy zamek świata” to popularne hasło. Sprawdź, co mierzono.",
    ]:
        L.append("- " + line)
    L.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("Zapisano:", OUT)


if __name__ == "__main__":
    main()
