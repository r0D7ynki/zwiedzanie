# -*- coding: utf-8 -*-
"""Buduje przewodnik PDF: Malbork i państwo krzyżackie."""
import subprocess, html, os
from urllib.parse import urlparse, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)          # katalog malbork/
HTML_PATH = os.path.join(OUT_DIR, "przewodnik.html")
PDF_PATH = os.path.join(OUT_DIR, "Malbork_plan_nauki_i_zrodla.pdf")


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


def pl_hours(n):
    """Odmiana słowa godzina: 1 godzina, 2-4 godziny, 5+ godzin."""
    if n == 1:
        return "godzina"
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return "godziny"
    return "godzin"


def dom(url):
    return urlparse(url).netloc.replace("www.", "")


def link(label, url, show_dom=True):
    d = f' <span class="dom">{html.escape(dom(url))}</span>' if show_dom else ""
    return f'<a href="{html.escape(url)}">{label}</a>{d}'


# ----------------------------------------------------------------- dane

STAGES = [
    {
        "n": 1, "title": "Tło: Polska w rozbiciu i Prusowie", "years": "1138–1226", "time": "3 h",
        "goal": "Zrozumiesz, dlaczego książęta polscy potrzebowali zakonu rycerskiego.",
        "events": [
            ("1138", "Umiera Bolesław Krzywousty. Państwo dzieli się między synów. Zaczyna się rozbicie dzielnicowe."),
            ("XII–XIII w.", "Książęta walczą o Kraków i o zwierzchność. Polska nie ma jednego władcy."),
            ("XIII w.", "Prusowie żyją między Wisłą a Niemnem. Nie mają państwa ani chrztu. Napadają na Mazowsze."),
            ("1226", "Konrad I Mazowiecki zaprasza Zakon Krzyżacki. Daje mu ziemię chełmińską."),
            ("1226", "Cesarz Fryderyk II wydaje złotą bullę w Rimini. Nadaje Zakonowi Prusy jako lenno."),
        ],
        "web": [
            ("Wikipedia: Prusowie", "https://pl.wikipedia.org/wiki/Prusowie"),
            ("Wikipedia: Konrad I mazowiecki", "https://pl.wikipedia.org/wiki/Konrad_I_mazowiecki"),
            ("Wikipedia: Zakon krzyżacki", "https://pl.wikipedia.org/wiki/Zakon_krzy%C5%BCacki"),
        ],
        "video": [
            ("Kings and Generals: How the Teutonic Order Conquered Prussia", "https://www.youtube.com/watch?v=HBYC7IGutIo", "film angielski, dobre mapy"),
            ("Historia bez cenzury: Zakute łby — Krzyżacy", "https://www.youtube.com/watch?v=PIBpU2BXRdE", "lekkie wprowadzenie"),
        ],
        "books": [("Andrzej Nowak, Dzieje Polski, t. 2", "rozdziały o dzielnicach i o Prusach")],
        "quiz": [
            "Dlaczego Konrad Mazowiecki zaprosił Krzyżaków?",
            "Skąd Zakon wziął prawo do Prus? Czym różni się bulla cesarska od nadania księcia?",
            "Kim byli Prusowie i dlaczego nie stworzyli państwa?",
        ],
    },
    {
        "n": 2, "title": "Podbój Prus i budowa państwa zakonnego", "years": "1226–1309", "time": "4 h",
        "goal": "Zobaczysz, jak mała wspólnota zakonna zbudowała państwo i pierwszy Malbork.",
        "events": [
            ("1230", "Hermann Balk przekracza Wisłę. Zakon stawia pierwsze zamki drewniano-ziemne."),
            ("1231–1233", "Powstają Toruń i Chełmno. Zakon buduje sieć warowni."),
            ("1237", "Zakon Krzyżacki łączy się z Kawalerami Mieczowymi (Inflanty)."),
            ("1242–1249", "I powstanie Prusów. Kończy je pokój w Dzierzgoniu."),
            ("1260", "Klęska pod Durbe. Zaczyna się II powstanie Prusów. Zakon niemal traci wszystko."),
            ("1274–1280", "Koniec powstania. Zakon buduje Malbork. Miasto dostaje prawa miejskie w 1280 roku."),
            ("1291", "Upada Akka. Zakon traci Ziemię Świętą i szuka nowej siedziby."),
            ("1308–1309", "Zakon zajmuje Gdańsk. Wielki mistrz przenosi stolicę do Malborka."),
        ],
        "web": [
            ("Muzeum Zamkowe: historia zamku 1280–1457", "https://zamek.malbork.pl/wizyta/historia-zamku/lata-1280-1457/"),
            ("Wikipedia: Państwo zakonu krzyżackiego", "https://pl.wikipedia.org/wiki/Pa%C5%84stwo_zakonu_krzy%C5%BCackiego"),
        ],
        "video": [
            ("ThrashingMadPL: Historia Zakonu Krzyżackiego, cz. 1", "https://www.youtube.com/watch?v=D9Ki7hIlYIY", "polski, szczegółowy"),
            ("ThrashingMadPL: Historia Zakonu Krzyżackiego, cz. 2", "https://www.youtube.com/watch?v=Bap5S7TOnpA", ""),
            ("Kings and Generals: Structure of the Teutonic Order", "https://www.youtube.com/watch?v=lKqIOw-htmo", "jak działało państwo"),
        ],
        "books": [("William Urban, The Teutonic Knights. A Military History", "podbój Prus i organizacja armii")],
        "quiz": [
            "Co dało Zakonowi połączenie z Kawalerami Mieczowymi?",
            "Dlaczego wielki mistrz wybrał Malbork, a nie Gdańsk?",
            "Jak Zakon finansował budowę zamków?",
        ],
    },
    {
        "n": 3, "title": "Malbork stolicą Zakonu", "years": "1309–1370", "time": "4 h",
        "goal": "Poznasz życie codzienne na zamku i spór z Polską o Pomorze.",
        "events": [
            ("1309", "Malbork staje się siedzibą wielkiego mistrza. Zamek rośnie przez cały wiek."),
            ("1320–1321", "Procesy polsko-krzyżackie przed papieżem. Polska żąda zwrotu Pomorza."),
            ("1327–1332", "Wojna. Zakon zajmuje Kujawy i ziemię dobrzyńską."),
            ("1333", "Koronacja Kazimierza Wielkiego. Polska szuka porozumienia."),
            ("1343", "Pokój w Kaliszu. Kazimierz zrzeka się Pomorza Gdańskiego, odzyskuje Kujawy."),
            ("1352–1382", "Winrich von Kniprode rządzi Zakonem. To złoty wiek państwa."),
            ("1380–1399", "Powstaje Pałac Wielkich Mistrzów. Malbork staje się rezydencją na miarę Europy."),
        ],
        "web": [
            ("Muzeum Zamkowe: historia zamku 1280–1457", "https://zamek.malbork.pl/wizyta/historia-zamku/lata-1280-1457/"),
            ("Wikipedia: Zamek w Malborku", "https://pl.wikipedia.org/wiki/Zamek_w_Malborku"),
            ("Histmag: Malbork — siedziba wielkich mistrzów", "https://histmag.org/Malbork-siedziba-wielkich-mistrzow-10007"),
            ("Wikipedia: Pokój kaliski", "https://pl.wikipedia.org/wiki/Pok%C3%B3j_kaliski"),
        ],
        "video": [
            ("ThrashingMadPL: Historia Zakonu Krzyżackiego, cz. 3", "https://www.youtube.com/watch?v=nB_DNm8QWm4", ""),
            ("ThrashingMadPL: Historia Zakonu Krzyżackiego, cz. 4", "https://www.youtube.com/watch?v=JIhGTjD-Xg8", ""),
        ],
        "books": [("Karol Górski, Dzieje Malborka", "rozdziały o mieście i o zamku w XIV wieku")],
        "quiz": [
            "Dlaczego Kazimierz Wielki ustąpił w Kaliszu?",
            "Jak zamek pokazywał potęgę Zakonu?",
            "Kto mieszkał na zamku wysokim, kto na średnim, a kto na przedzamczu?",
        ],
    },
    {
        "n": 4, "title": "Złoty wiek, Grunwald i oblężenie Malborka", "years": "1370–1411", "time": "6 h",
        "goal": "Przejdziesz przez najważniejszy rok w historii zamku.",
        "events": [
            ("1385", "Unia w Krewie. Polska i Litwa łączą siły przeciw Zakonowi."),
            ("1386", "Chrzest i koronacja Władysława Jagiełły. Litwa przyjmuje chrzest."),
            ("1409", "Wybucha wielka wojna. Zakon zajmuje ziemię dobrzyńską."),
            ("15 lipca 1410", "Bitwa pod Grunwaldem. Armia polsko-litewska rozbija Zakon. Ginie wielki mistrz Ulrich von Jungingen."),
            ("25 lipca – 19 września 1410", "Oblężenie Malborka. Heinrich von Plauen broni zamku. Polacy odchodzą."),
            ("1 lutego 1411", "I pokój toruński. Zakon płaci okup, ale zachowuje większość ziemi."),
        ],
        "web": [
            ("Wikipedia: Wielka wojna z zakonem krzyżackim", "https://pl.wikipedia.org/wiki/Wielka_wojna_z_zakonem_krzy%C5%BCackim"),
            ("Wikipedia: Bitwa pod Grunwaldem", "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem"),
            ("Wikipedia: Władysław II Jagiełło", "https://pl.wikipedia.org/wiki/W%C5%82adys%C5%82aw_II_Jagie%C5%82%C5%82o"),
            ("Muzeum Grunwald", "https://muzeum-grunwald.pl/"),
        ],
        "video": [
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 1", "https://www.youtube.com/watch?v=leELmda8xG4", "seria ma 7 części"),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 2", "https://www.youtube.com/watch?v=09xC9yrymtw", ""),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 3", "https://www.youtube.com/watch?v=JXAY_kFBNYE", ""),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 4", "https://www.youtube.com/watch?v=qSj63SC72cY", ""),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 5", "https://www.youtube.com/watch?v=5L6Zcn1pTj4", ""),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 6", "https://www.youtube.com/watch?v=8w3aeShfPVQ", ""),
            ("ThrashingMadPL: Bitwa pod Grunwaldem, cz. 7 — oblężenie", "https://www.youtube.com/watch?v=yZw7Rg99FzU", "kluczowy odcinek"),
            ("HistoryMarche: Battle of Grunwald 1410", "https://www.youtube.com/watch?v=Hgl77ZdyxvE", "animowane mapy"),
            ("Na bitewnym szlaku: Krzyżacka hekatomba", "https://www.youtube.com/watch?v=QVr2ak2K2ds", "przebieg bitwy"),
        ],
        "books": [("Stefan Kuczyński, Wielka wojna z Zakonem Krzyżackim 1409–1411", "klasyczna monografia wojny")],
        "quiz": [
            "Dlaczego Jagiełło nie zdobył Malborka?",
            "Kto zorganizował obronę zamku i jak to zrobił?",
            "Co Polska zyskała w Toruniu w 1411 roku?",
        ],
    },
    {
        "n": 5, "title": "Upadek państwa zakonnego i wojna trzynastoletnia", "years": "1411–1466", "time": "5 h",
        "goal": "Zobaczysz, jak państwo Zakonu upadło od środka, a Malbork wrócił do Polski.",
        "events": [
            ("1414", "Wojna głodowa. Armia polska pustoszy Prusy, ale nie zdobywa zamków."),
            ("1422", "Pokój w Melnie. Zakon traci kolejne ziemie."),
            ("1430s", "Miasta i szlachta pruska są niezadowolone z podatków i sądów Zakonu."),
            ("1440", "Powstaje Związek Pruski. Spotkanie w Kwidzynie."),
            ("1454", "Prusy wchodzą do Polski. Wybucha wojna trzynastoletnia."),
            ("18 września 1454", "Klęska Polaków pod Chojnicami. Wojna się przedłuża."),
            ("1457", "Malbork przechodzi w ręce polskie. Kazimierz Jagiellończyk wjeżdża do zamku."),
            ("19 października 1466", "II pokój toruński. Prusy Królewskie wracają do Polski. Wielki mistrz przenosi się do Królewca."),
        ],
        "web": [
            ("Wikipedia: Wojna trzynastoletnia", "https://pl.wikipedia.org/wiki/Wojna_trzynastoletnia"),
            ("Wikipedia: Drugi pokój toruński", "https://pl.wikipedia.org/wiki/Drugi_pok%C3%B3j_toru%C5%84ski"),
            ("Wikipedia: Związek Pruski", "https://pl.wikipedia.org/wiki/Zwi%C4%85zek_Pruski"),
            ("ZPE: Wojna trzynastoletnia — lekcja", "https://zpe.gov.pl/a/wojna-trzynastoletnia-polski-z-zakonem-krzyzackim/DVhXDJsl3"),
        ],
        "video": [
            ("Co za historia: Jagiellonowie i wojna trzynastoletnia", "https://www.youtube.com/watch?v=QuMhflN__hc", "odcinek 12"),
            ("Na bitewnym szlaku: Bitwa pod Chojnicami 1454", "https://www.youtube.com/watch?v=u3wWFs72Yq4", ""),
            ("Historia bez cenzury: Z ciupagą na Grunwald", "https://www.youtube.com/watch?v=Mwc7xGKUQ7c", "kontekst epoki"),
        ],
        "books": [("Andrzej Nowak, Dzieje Polski, t. 3 (1340–1468)", "rozdziały o Kazimierzu Jagiellończyku")],
        "quiz": [
            "Dlaczego miasta pruskie zbuntowały się przeciw Zakonowi?",
            "Kto płacił za wojnę trzynastoletnią?",
            "Co Polska zyskała w 1466 roku, a co straciła?",
        ],
    },
    {
        "n": 6, "title": "Malbork w Polsce i w Prusach", "years": "1466–1945", "time": "4 h",
        "goal": "Zobaczysz, jak zamek zmieniał funkcje: rezydencja, koszary, muzeum.",
        "events": [
            ("1466–1772", "Malbork jest stolicą województwa malborskiego. Zamek należy do starostów."),
            ("1626–1629", "Szwedzi zajmują Malbork podczas wojny o ujście Wisły."),
            ("1655–1660", "Potop szwedzki. Zamek znowu w rękach Szwedów."),
            ("1772", "I rozbiór Polski. Malbork trafia do Prus."),
            ("1774–1800", "Zamek służy jako magazyn i koszary. Budynki niszczeją."),
            ("1817", "Prusy zaczynają odbudowę zamku. Prace trwają ponad sto lat."),
            ("1882–1922", "Conrad Steinbrecht kieruje rekonstrukcją. Zamek odzyskuje gotycki wygląd."),
            ("1945", "Walki o Malbork. Zamek płonie, miasto leży w gruzach."),
        ],
        "web": [
            ("Muzeum Zamkowe: historia zamku 1457–1772", "https://zamek.malbork.pl/wizyta/historia-zamku/lata-1457-1772/"),
            ("Muzeum Zamkowe: historia zamku 1772–1945", "https://zamek.malbork.pl/wizyta/historia-zamku/lata-1772-1945/"),
            ("Dzieje.pl: trzy polskie wieki zamku", "https://dzieje.pl/wystawy/wystawa-prezentujaca-trzy-polskie-wieki-zamku-krzyzackiego-w-malborku"),
            ("Wikipedia: I rozbiór Polski", "https://pl.wikipedia.org/wiki/I_rozbi%C3%B3r_Polski"),
        ],
        "video": [
            ("Historia jakiej nie znacie: jak Polska przejęła Malbork", "https://www.youtube.com/watch?v=msxxEE8DBN0", ""),
        ],
        "books": [("Norman Davies, Boże igrzysko", "rozdziały o rozbiorach i XIX wieku")],
        "quiz": [
            "Dlaczego zamek popadł w ruinę po 1772 roku?",
            "Czym była pruska odbudowa zamku i kto ją prowadził?",
            "Jak Malbork zmienił się po 1945 roku?",
        ],
    },
    {
        "n": 7, "title": "Zniszczenie, odbudowa, UNESCO", "years": "1945–dziś", "time": "4 h",
        "goal": "Zrozumiesz, ile z tego, co dziś widzisz, jest rekonstrukcją.",
        "events": [
            ("1945", "Armia radziecka zdobywa Malbork. Pożary niszczą około połowy zamku."),
            ("1945–1949", "Pierwsze prace zabezpieczające. Zamek jest ruiną."),
            ("1961", "Powstaje Muzeum Zamkowe w Malborku."),
            ("1997", "Zamek trafia na Listę Światowego Dziedzictwa UNESCO."),
            ("2000s–dziś", "Konserwacja, badania archeologiczne, nowe trasy zwiedzania."),
        ],
        "web": [
            ("Muzeum Zamkowe: historia zamku 1945–obecnie", "https://zamek.malbork.pl/wizyta/historia-zamku/lata-1945-obecnie/"),
            ("UNESCO: Castle of the Teutonic Order in Malbork", "https://whc.unesco.org/en/list/847"),
            ("Muzeum Zamkowe: historia muzeum", "https://zamek.malbork.pl/muzeum/historia-muzeum/"),
        ],
        "video": [
            ("Muzeum Zamkowe: Komnaty dostojników krzyżackich", "https://www.youtube.com/watch?v=GRnku1gHhqw", "kanał muzeum"),
            ("Muzeum Zamkowe: podcast Posłuchaj Muzeum, odc. 5", "https://www.youtube.com/watch?v=nwHykmd0gaA", "o wnętrzach"),
        ],
        "books": [("Publikacje Muzeum Zamkowego", "przewodniki i monografie wydane przez muzeum")],
        "quiz": [
            "Co przetrwało pożar w 1945 roku?",
            "Co odbudowano po wojnie, a co zbudowano od nowa?",
            "Co daje zamkowi wpis na listę UNESCO?",
        ],
    },
    {
        "n": 8, "title": "Powtórka i wycieczka", "years": "dziś", "time": "3 h",
        "goal": "Sprawdzisz wiedzę i przygotujesz wizytę w Malborku.",
        "events": [
            ("Zadanie 1", "Narysuj z pamięci os czasu od 1226 do 1466 roku. Zaznacz dziesięć dat."),
            ("Zadanie 2", "Opisz trasę: zamek wysoki, średni, przedzamcze. Powiedz, kto tam mieszkał."),
            ("Zadanie 3", "Zaplanuj wizytę. Sprawdź bilety, godziny i trasę zwiedzania."),
            ("Zadanie 4", "Wysłuchaj audioprzewodnika. Porównaj go z tym, co przeczytałeś."),
        ],
        "web": [
            ("Muzeum Zamkowe: bilety i godziny", "https://zamek.malbork.pl/wizyta/"),
            ("Muzeum Zamkowe: wirtualny spacer", "https://zamek.malbork.pl/muzeum/wirtualny-spacer/"),
            ("Muzeum Zamkowe: audioprzewodnik", "https://zamek.malbork.pl/wizyta/audio-przewodnik/"),
        ],
        "video": [
            ("Zwiedzanie zamku z przewodnikiem", "https://www.youtube.com/watch?v=kXmGYKggv6w", "praktyczne wskazówki"),
        ],
        "books": [("Jan Długosz, Roczniki czyli kroniki sławnego Królestwa Polskiego", "fragment o Grunwaldzie — źródło z epoki")],
        "quiz": [
            "Które daty są najważniejsze dla Malborka?",
            "Kto był wrogiem, a kto sojusznikiem Zakonu?",
            "Co powiesz komuś, kto twierdzi, że zamek jest w całości średniowieczny?",
        ],
    },
]

TIMELINE_1 = [
    ("1198", "Papież uznaje Zakon Krzyżacki."),
    ("1226", "Konrad Mazowiecki zaprasza Krzyżaków. Złota bulla w Rimini."),
    ("1230", "Krzyżacy przybywają nad Wisłę. Zaczyna się podbój Prus."),
    ("1231", "Zakon zakłada Toruń."),
    ("1260", "Klęska pod Durbe. Wybucha II powstanie Prusów."),
    ("1274", "Koniec powstania. Zaczyna się budowa Malborka."),
    ("1280", "Malbork dostaje prawa miejskie."),
    ("1308", "Krzyżacy zajmują Gdańsk."),
    ("1309", "Stolica Zakonu przenosi się do Malborka."),
    ("1343", "Pokój w Kaliszu. Kazimierz Wielki zrzeka się Pomorza."),
    ("1385", "Unia w Krewie. Polska i Litwa łączą siły."),
    ("1386", "Chrzest i koronacja Władysława Jagiełły."),
    ("1409", "Wybucha wielka wojna z Zakonem."),
    ("15 VII 1410", "Bitwa pod Grunwaldem."),
    ("25 VII – 19 IX 1410", "Oblężenie Malborka."),
    ("1411", "I pokój toruński. Zakon płaci okup."),
    ("1414", "Wojna głodowa."),
    ("1422", "Pokój w Melnie."),
    ("1440", "Powstaje Związek Pruski."),
    ("1454", "Prusy wchodzą do Polski. Wybucha wojna trzynastoletnia."),
    ("18 IX 1454", "Klęska polska pod Chojnicami."),
    ("1457", "Kazimierz Jagiellończyk wjeżdża do Malborka."),
    ("19 X 1466", "II pokój toruński. Koniec państwa zakonnego w Malborku."),
]

TIMELINE_2 = [
    ("1525", "Hołd pruski. Zakon ulega sekularyzacji."),
    ("1626–1629", "Szwedzi w Malborku."),
    ("1655–1660", "Potop szwedzki. Zamek znowu zajęty."),
    ("1772", "I rozbiór Polski. Malbork w Prusach."),
    ("1817", "Początek pruskiej odbudowy zamku."),
    ("1882–1922", "Conrad Steinbrecht prowadzi rekonstrukcję."),
    ("1945", "Walki o Malbork. Zamek płonie."),
    ("1961", "Powstaje Muzeum Zamkowe."),
    ("1997", "Zamek wpisany na listę UNESCO."),
]

GLOSSARY = [
    ("Zakon krzyżacki", "Zakon rycerski, założony w Akce około 1190 roku. Najpierw opiekował się pielgrzymami, potem walczył."),
    ("Wielki mistrz", "Najwyższy zwierzchnik Zakonu. Od 1309 roku mieszkał w Malborku."),
    ("Komtur", "Zarządzał zamkiem i okolicą, czyli komturią."),
    ("Rejza", "Wyprawa wojenna Zakonu na Litwę. Miała wyglądać jak krucjata."),
    ("Prusowie", "Lud bałtyjski między Wisłą a Niemnem. Nie miał własnego państwa."),
    ("Związek Pruski", "Organizacja miast i szlachty pruskiej. Powstała w 1440 roku przeciw Zakonowi."),
    ("Prusy Królewskie", "Zachodnia część Prus. Weszła do Polski w 1466 roku."),
    ("Hołd pruski", "Akt z 1525 roku. Albrecht Hohenzollern złożył hołd Zygmuntowi Staremu."),
    ("Hanza", "Związek miast handlowych. Gdańsk i Toruń należały do niego."),
]

BOOKS = [
    ("Karol Górski", "Dzieje Malborka", "Wydawnictwo Morskie, Gdańsk 1973",
     "Klasyczna monografia miasta i zamku. Zacznij od niej, gdy chcesz poznać Malbork, a nie całą Polskę.",
     "https://lubimyczytac.pl/ksiazka/4934511/dzieje-malborka"),
    ("Andrzej Nowak", "Dzieje Polski, t. 1–3", "Biały Kruk, Kraków 2014–2017",
     "Najlepszy wybór na początek. Tom 3 obejmuje lata 1340–1468, czyli Grunwald i wojnę trzynastoletnią.", None),
    ("Norman Davies", "Boże igrzysko. Historia Polski", "Znak, Kraków",
     "Szeroka perspektywa. Pokazuje Polskę na tle Europy. Czytaj równolegle z Nowakiem.", None),
    ("Jerzy Wyrozumski", "Historia Polski do roku 1505", "PWN, Warszawa",
     "Podręcznik akademicki. Zwięzły i porządny. Dobry do sprawdzania faktów.", None),
    ("Stefan Kuczyński", "Wielka wojna z Zakonem Krzyżackim w latach 1409–1411", "MON, Warszawa",
     "Szczegółowa monografia wojny. Sięgnij po nią po etapie 4.", None),
    ("William Urban", "The Teutonic Knights. A Military History", "Greenhill Books, 2003",
     "Historia Zakonu po angielsku. Dobra do tematów wojskowych i organizacyjnych.", None),
    ("Henryk Sienkiewicz", "Krzyżacy", "powieść, 1900",
     "Powieść, nie podręcznik. Przeczytaj po etapie 5. Zobaczysz, jak mity wchodzą do kultury.", None),
    ("Jan Długosz", "Roczniki czyli kroniki sławnego Królestwa Polskiego", "źródło z XV wieku",
     "Źródło z epoki. Pamiętaj, że Długosz był stronniczy. Czytaj go krytycznie.", None),
]

WEB_EXTRA = [
    ("Muzeum Zamkowe w Malborku — strona główna", "https://zamek.malbork.pl/", "instytucja"),
    ("Muzeum Zamkowe — historia zamku (przegląd)", "https://zamek.malbork.pl/wizyta/historia-zamku/", "instytucja"),
    ("Muzeum Zamkowe — publikacje popularnonaukowe", "https://zamek.malbork.pl/wydawnictwo/publikacje-popularnonaukowe/", "instytucja"),
    ("Muzeum Zamkowe — książki i media (sklep)", "https://zamek.malbork.pl/kategoria-produktu/ksiazki-i-media/", "instytucja"),
    ("Muzeum Zamkowe — podcast Posłuchaj Muzeum", "https://zamek.malbork.pl/aktualnosci/posluchaj-muzeum-podcast-muzeum-zamkowego-w-malborku-odc-2/", "instytucja"),
    ("UNESCO — Castle of the Teutonic Order in Malbork", "https://whc.unesco.org/en/list/847", "instytucja"),
    ("Muzeum Grunwald — strona główna", "https://muzeum-grunwald.pl/", "instytucja"),
    ("Muzeum Grunwald — historia muzeum", "https://muzeum-grunwald.pl/o-muzeum/historia-muzeum/", "instytucja"),
    ("Wikipedia — Zamek w Malborku", "https://pl.wikipedia.org/wiki/Zamek_w_Malborku", "encyklopedia"),
    ("Wikipedia — Malbork", "https://pl.wikipedia.org/wiki/Malbork", "encyklopedia"),
    ("Wikipedia — Zakon krzyżacki", "https://pl.wikipedia.org/wiki/Zakon_krzy%C5%BCacki", "encyklopedia"),
    ("Wikipedia — Państwo zakonu krzyżackiego", "https://pl.wikipedia.org/wiki/Pa%C5%84stwo_zakonu_krzy%C5%BCackiego", "encyklopedia"),
    ("Wikipedia — Prusowie", "https://pl.wikipedia.org/wiki/Prusowie", "encyklopedia"),
    ("Wikipedia — Konrad I mazowiecki", "https://pl.wikipedia.org/wiki/Konrad_I_mazowiecki", "encyklopedia"),
    ("Wikipedia — Wielka wojna z zakonem krzyżackim", "https://pl.wikipedia.org/wiki/Wielka_wojna_z_zakonem_krzy%C5%BCackim", "encyklopedia"),
    ("Wikipedia — Bitwa pod Grunwaldem", "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem", "encyklopedia"),
    ("Wikipedia — Wojna trzynastoletnia", "https://pl.wikipedia.org/wiki/Wojna_trzynastoletnia", "encyklopedia"),
    ("Wikipedia — Drugi pokój toruński", "https://pl.wikipedia.org/wiki/Drugi_pok%C3%B3j_toru%C5%84ski", "encyklopedia"),
    ("Wikipedia — Związek Pruski", "https://pl.wikipedia.org/wiki/Zwi%C4%85zek_Pruski", "encyklopedia"),
    ("Wikipedia — Kazimierz III Wielki", "https://pl.wikipedia.org/wiki/Kazimierz_III_Wielki", "encyklopedia"),
    ("Wikipedia — Władysław II Jagiełło", "https://pl.wikipedia.org/wiki/W%C5%82adys%C5%82aw_II_Jagie%C5%82%C5%82o", "encyklopedia"),
    ("Wikipedia — Pokój kaliski", "https://pl.wikipedia.org/wiki/Pok%C3%B3j_kaliski", "encyklopedia"),
    ("Wikipedia — I rozbiór Polski", "https://pl.wikipedia.org/wiki/I_rozbi%C3%B3r_Polski", "encyklopedia"),
    ("Histmag — Malbork, siedziba wielkich mistrzów", "https://histmag.org/Malbork-siedziba-wielkich-mistrzow-10007", "artykuł"),
    ("Dzieje.pl — trzy polskie wieki zamku", "https://dzieje.pl/wystawy/wystawa-prezentujaca-trzy-polskie-wieki-zamku-krzyzackiego-w-malborku", "artykuł"),
    ("ZPE — wojna trzynastoletnia (lekcja)", "https://zpe.gov.pl/a/wojna-trzynastoletnia-polski-z-zakonem-krzyzackim/DVhXDJsl3", "lekcja"),
    ("Polskie Radio — Mediewanna o Krzyżakach", "https://www.polskieradio.pl/dwojka/audycje/mediewanna,9935/odcinek/jak-krzyzacy-zmienili-zycie-obyczaje-kuchnie-swoich-czasow-na-terenie-polski-gosc-bogdan-galazka,ebc9589e-f60d-48a8-a6dd-f572df89504b", "podcast"),
]

# ----------------------------------------------------------------- css

CSS = """
@page { size: A4; margin: 13mm 14mm 13mm 14mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: "Noto Serif", Georgia, serif; font-size: 9.6pt;
       line-height: 1.44; color: #241c15; background: #fff; }
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
.cv-top { position: relative; margin-top: 12mm; }
.kicker { font-size: 7.8pt; letter-spacing: 2.6pt; text-transform: uppercase;
  color: #8f3a2c; font-weight: 700; }
.cover h1 { font-size: 33pt; line-height: 1.05; margin: 8mm 0 0 0; color: #2a1a12;
  font-weight: 800; letter-spacing: -0.7pt; max-width: 120mm; }
.cover .sub { font-family: "Noto Sans", sans-serif; font-size: 10.4pt; color: #8f3a2c;
  margin-top: 4mm; letter-spacing: 0.2pt; }
.rule { height: 2.2pt; width: 32mm; background: #8f3a2c; margin: 6mm 0; }
.cover .lead { font-size: 11.2pt; line-height: 1.52; color: #4a3a2c; max-width: 124mm; }
.cv-tl { position: absolute; left: 14mm; right: 22mm; bottom: 80mm; }
.cv-tl .bar { height: 1.4pt; background: #8f3a2c; opacity: 0.45; }
.cv-tl .pts { display: flex; }
.cv-tl .pt { flex: 1; position: relative; padding-top: 4mm; }
.cv-tl .pt::before { content: ""; position: absolute; top: -1.6mm; left: 0; width: 2.6mm;
  height: 2.6mm; border-radius: 50%; background: #8f3a2c; }
.cv-tl .pt b { display: block; font-family: "Noto Sans", sans-serif; font-size: 10.6pt;
  color: #8f3a2c; font-weight: 800; }
.cv-tl .pt span { font-size: 7.8pt; color: #6b5744; }
.facts { position: absolute; left: 14mm; right: 22mm; bottom: 30mm; display: flex; gap: 8mm; }
.fact { border-top: 0.7pt solid #cbb397; padding-top: 2.2mm; flex: 1; }
.fact b { display: block; font-family: "Noto Sans", sans-serif; font-size: 15pt; color: #8f3a2c; }
.fact span { font-size: 8pt; color: #6b5744; }
.cv-foot { position: absolute; left: 14mm; right: 22mm; bottom: 12mm; font-size: 7.8pt; color: #7a6350; }

/* sections */
.newpage { break-before: page; }
h2.sec { font-size: 15pt; margin: 0 0 3.4mm 0; padding-bottom: 2mm;
  border-bottom: 2pt solid #8f3a2c; color: #2a1a12; font-weight: 800;
  letter-spacing: -0.2pt; break-after: avoid; }
h2.sec .num { color: #b8894a; font-weight: 800; margin-right: 2.4mm; }
h3 { font-size: 11pt; margin: 4.2mm 0 1.5mm 0; color: #8f3a2c; font-weight: 700; break-after: avoid; }
h4 { font-size: 7.6pt; margin: 0 0 1.2mm 0; letter-spacing: 1.5pt; text-transform: uppercase;
  color: #8a6a4a; font-weight: 700; }
.lede { font-size: 10.2pt; color: #4a3a2c; line-height: 1.5; margin-bottom: 3mm; }
.box { background: #faf5ea; border: 0.6pt solid #e3d2b8; border-left: 3pt solid #b8894a;
  padding: 3.4mm 4mm; margin: 0 0 3.4mm 0; break-inside: avoid; }
.box.dark { background: #f5ecdf; border-left-color: #8f3a2c; }
.box h3 { margin-top: 0; }
.box p:last-child, .box ul:last-child { margin-bottom: 0; }

table { width: 100%; border-collapse: collapse; font-size: 8.5pt; }
th { text-align: left; font-family: "Noto Sans", sans-serif; font-size: 7.4pt; letter-spacing: 1pt;
  text-transform: uppercase; color: #8a6a4a; border-bottom: 1pt solid #c9a58c; padding: 0 2mm 1.4mm 0; }
td { padding: 0.75mm 2mm 0.75mm 0; border-bottom: 0.4pt solid #eadcc8; vertical-align: top; }
td.yr { font-family: "Noto Sans", sans-serif; font-weight: 700; color: #8f3a2c;
  white-space: nowrap; width: 32mm; font-size: 8.4pt; }
tr.total td { border-bottom: none; font-weight: 700; color: #2a1a12; padding-top: 2.2mm; }
table.tl { break-inside: avoid; }

/* stage cards */
.stage { border: 0.6pt solid #e0cfb6; background: #fdfaf4; margin: 0 0 3.2mm 0; break-inside: avoid; }
.stage .head { display: flex; align-items: baseline; gap: 3mm; padding: 2.1mm 3.4mm 1.7mm 3.4mm;
  border-bottom: 0.6pt solid #e8dbc7; background: #f7efe1; }
.stage .no { font-family: "Noto Sans", sans-serif; font-size: 12pt; font-weight: 800; color: #fff;
  background: #8f3a2c; width: 8mm; height: 8mm; border-radius: 50%; text-align: center;
  line-height: 8mm; flex: 0 0 8mm; }
.stage .ttl { flex: 1; }
.stage .ttl h3 { margin: 0; font-size: 10.6pt; color: #2a1a12; }
.stage .ttl .sub { font-size: 8pt; color: #7a6350; margin-top: 0.6mm; }
.stage .time { font-family: "Noto Sans", sans-serif; font-size: 7.6pt; color: #6b5744;
  white-space: nowrap; border: 0.6pt solid #cbb397; padding: 0.8mm 2mm; border-radius: 2mm; }
.stage .body { padding: 2.1mm 3.4mm 1.2mm 3.4mm; }
.goal { font-style: italic; color: #5a4636; margin-bottom: 1.4mm; font-size: 8.7pt; }
.events { font-size: 8.5pt; line-height: 1.37; }
.events li { margin-bottom: 0.7mm; }
.events b { color: #8f3a2c; font-family: "Noto Sans", sans-serif; font-size: 8.4pt; }

.grid2 { display: grid; grid-template-columns: 1.12fr 1fr; column-gap: 6mm; }
.col h4 { margin-top: 0; }
.src h4 { margin-top: 2mm; }
.src h4:first-child { margin-top: 0; }
.src ul { list-style: none; padding: 0; margin: 0; font-size: 7.9pt; line-height: 1.3; }
.src li { margin: 0 0 0.7mm 0; }
.dom { font-size: 7pt; color: #9a8570; font-family: "Noto Sans", sans-serif; }
.note { font-size: 7.4pt; color: #9a8570; font-style: italic; }
.quiz { margin-top: 1.6mm; padding-top: 1.4mm; border-top: 0.5pt dashed #d3bfa3; break-inside: avoid; }
.quiz ol { padding-left: 4.2mm; font-size: 8.2pt; margin: 0; }
.quiz li { margin-bottom: 0.6mm; }

/* appendix */
.cat { margin-bottom: 3.6mm; }
.cat h3 { font-size: 9.6pt; margin: 0 0 1.8mm 0; border-bottom: 0.6pt solid #e8dbc7; padding-bottom: 0.8mm; }
.lnk-grid { column-count: 2; column-gap: 7mm; }
.lnk { font-size: 8pt; line-height: 1.34; margin-bottom: 1.9mm; break-inside: avoid; }
.lnk .t { font-weight: 600; color: #2a1a12; }
.lnk .u { display: block; font-family: "Noto Sans Mono", monospace; font-size: 6.9pt;
  color: #7a6350; overflow-wrap: anywhere; border-bottom: none; }

"""


def render_stage(s):
    ev = "".join(f"<li><b>{d}</b> — {t}</li>" for d, t in s["events"])
    web = "".join(f"<li>{link(l, u)}</li>" for l, u in s["web"])
    vids = "".join(
        f"<li>{link(l, u, False)}" + (f' <span class="note">{n}</span>' if n else "") + "</li>"
        for l, u, n in s["video"])
    bks = "".join(
        f"<li><em>{l}</em>" + (f' <span class="note">{n}</span>' if n else "") + "</li>"
        for l, n in s["books"])
    quiz = "".join(f"<li>{q}</li>" for q in s["quiz"])
    return f"""
<div class="stage">
  <div class="head">
    <div class="no">{s['n']}</div>
    <div class="ttl"><h3>{s['title']}</h3><div class="sub">lata {s['years']}</div></div>
    <div class="time">{s['time']}</div>
  </div>
  <div class="body">
    <div class="goal">Cel: {s['goal']}</div>
    <div class="grid2">
      <div class="col">
        <h4>Co się wtedy działo</h4>
        <ul class="events">{ev}</ul>
      </div>
      <div class="col src">
        <h4>Strony</h4><ul>{web}</ul>
        <h4>Wideo</h4><ul>{vids}</ul>
        <h4>Książki</h4><ul>{bks}</ul>
      </div>
    </div>
    <div class="quiz"><h4>Sprawdź się</h4><ol>{quiz}</ol></div>
  </div>
</div>"""


def build_html():
    total_h = sum(int(s["time"].split()[0]) for s in STAGES)
    rows = "".join(
        f"<tr><td class='yr'>{s['n']}</td><td><b>{s['title']}</b><br>"
        f"<span class='note'>lata {s['years']}</span></td>"
        f"<td style='text-align:right;white-space:nowrap'>{s['time']}</td></tr>"
        for s in STAGES)

    tl1 = "".join(f"<tr><td class='yr'>{y}</td><td>{e}</td></tr>" for y, e in TIMELINE_1)
    tl2 = "".join(f"<tr><td class='yr'>{y}</td><td>{e}</td></tr>" for y, e in TIMELINE_2)
    gloss = "".join(f"<li><b>{t}</b> — {d}</li>" for t, d in GLOSSARY)

    books = "".join(
        f"""<div class="box" style="margin-bottom:2.6mm;padding:2.6mm 3.6mm">
        <div class="sans" style="font-weight:700;font-size:9.4pt">{a} — <em>{t}</em></div>
        <div class="note" style="font-style:normal;margin:0.6mm 0 1.4mm 0">{pub}</div>
        <div style="font-size:8.9pt">{why}</div>
        {f'<div style="margin-top:1.2mm;font-size:7.8pt">{link("Zobacz opis książki", u)}</div>' if u else ""}
        </div>"""
        for a, t, pub, why, u in BOOKS)

    stages_html = "".join(render_stage(s) for s in STAGES)

    # zbierz linki do dodatku
    seen, groups, order = set(), {}, []
    for label, url, cat in WEB_EXTRA:
        if url in seen:
            continue
        seen.add(url)
        groups.setdefault(cat, []).append((label, url))
        if cat not in order:
            order.append(cat)
    for s in STAGES:
        for label, url in s["web"]:
            if url not in seen:
                seen.add(url)
                groups.setdefault("strony z etapów", []).append((label, url))
                if "strony z etapów" not in order:
                    order.append("strony z etapów")
    vids = []
    for s in STAGES:
        for label, url, n in s["video"]:
            if url not in seen:
                seen.add(url)
                vids.append((label, url))

    n_links = len(seen)

    cat_names = {
        "instytucja": "Muzea i instytucje",
        "encyklopedia": "Wikipedia — punkt startowy, nie źródło naukowe",
        "artykuł": "Artykuły i portale historyczne",
        "lekcja": "Lekcje i materiały edukacyjne",
        "podcast": "Podcasty i audycje radiowe",
        "strony z etapów": "Pozostałe strony z etapów",
    }

    def grid(items):
        return '<div class="lnk-grid">' + "".join(
            f'<div class="lnk"><span class="t">{l}</span>'
            f'<a class="u" href="{html.escape(u)}">{html.escape(unquote(u))}</a></div>'
            for l, u in items) + "</div>"

    appendix = "".join(
        f'<div class="cat"><h3>{cat_names.get(c, c)}</h3>{grid(groups[c])}</div>' for c in order)
    if vids:
        appendix += f'<div class="cat"><h3>Wideo (YouTube)</h3>{grid(vids)}</div>'
    counts = [(cat_names.get(c, c), len(groups[c])) for c in order] + [("Wideo (YouTube)", len(vids))]
    uses = {
        "Muzea i instytucje": "źródło pierwotne, bilety, wystawy",
        "Wikipedia — punkt startowy, nie źródło naukowe": "szybki przegląd i bibliografia",
        "Artykuły i portale historyczne": "kontekst i ciekawostki",
        "Lekcje i materiały edukacyjne": "powtórka w formie lekcji",
        "Podcasty i audycje radiowe": "słuchanie w drodze",
        "Pozostałe strony z etapów": "materiały z etapów",
        "Wideo (YouTube)": "przebieg wydarzeń i mapy",
    }
    rows = "".join(
        f"<tr><td>{name}</td><td style='text-align:right;white-space:nowrap'>{n}</td>"
        f"<td style='color:#5a4636'>{uses.get(name, '')}</td></tr>" for name, n in counts)
    appendix += (f'<div class="cat"><h3>Podsumowanie zestawu</h3><table>'
                 f'<thead><tr><th>Kategoria</th><th style="text-align:right">Ile</th><th>Do czego</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table></div>')

    doc = f"""<!DOCTYPE html>
<html lang="pl"><head><meta charset="utf-8">
<title>Malbork i państwo krzyżackie — plan nauki i źródła</title>
<style>{CSS}</style></head>
<body>

<div class="cover">
  <div class="band"></div>
  <div class="cv-top">
    <div class="kicker">Plan nauki · 8 etapów · {n_links} źródeł online</div>
    <h1>Malbork<br>i państwo<br>krzyżackie</h1>
    <div class="sub">Historia zamku i Polski w średniowieczu</div>
    <div class="rule"></div>
    <p class="lead">Wydarzenia w kolejności, źródła po polsku i po angielsku, pytania kontrolne po każdym etapie. Od rozbicia dzielnicowego do współczesności.</p>
  </div>
  <div class="cv-tl">
    <div class="bar"></div>
    <div class="pts">
      <div class="pt"><b>1226</b><span>Zakon przybywa</span></div>
      <div class="pt"><b>1309</b><span>Malbork stolicą</span></div>
      <div class="pt"><b>1410</b><span>Grunwald</span></div>
      <div class="pt"><b>1466</b><span>Koniec państwa</span></div>
      <div class="pt"><b>1997</b><span>Lista UNESCO</span></div>
    </div>
  </div>
  <div class="facts">
    <div class="fact"><b>{total_h} h</b><span>tyle czasu potrzeba na całość</span></div>
    <div class="fact"><b>8</b><span>etapów, od 1226 do dziś</span></div>
    <div class="fact"><b>{n_links}</b><span>sprawdzonych źródeł online</span></div>
  </div>
  <div class="cv-foot">Wersja 1.0 · listopad 2026 · wszystkie linki sprawdzone w dniu wydania</div>
</div>

<div class="newpage"></div>

<section>
  <h2 class="sec"><span class="num">01</span>Jak korzystać z tego planu</h2>
  <p class="lede">Ten plan prowadzi Cię od tła do współczesności. Najpierw poznasz epokę. Potem zobaczysz, jak powstało państwo zakonne. Następnie przejdziesz przez wiek XIV i XV. Na końcu zobaczysz, co stało się z zamkiem po 1466 roku.</p>
  <p>Każdy etap ma trzy części: wydarzenia, źródła i pytania. Źródła są różne. Strona daje szybki przegląd. Film pokazuje przebieg. Książka dodaje niuanse. Dzięki temu ta sama historia wraca w innym języku.</p>

  <div class="box dark">
    <h3>Pięć zasad, które oszczędzą Ci czasu</h3>
    <ul>
      <li><b>Jeden etap to jeden wieczór.</b> Nie zaczynaj następnego, aż odpowiesz na pytania.</li>
      <li><b>Czytaj z mapą.</b> Zaznacz Malbork, Gdańsk, Toruń, Grunwald i Chojnice.</li>
      <li><b>Notuj daty i osoby.</b> Jedna kartka na etap wystarczy.</li>
      <li><b>Film traktuj jako wprowadzenie.</b> Książka daje tło i spór naukowy.</li>
      <li><b>Wracaj do pytań po tygodniu.</b> Powtórka utrwala wiedzę lepiej niż czytanie od nowa.</li>
    </ul>
  </div>

  <h3>Plan w skrócie</h3>
  <table>
    <thead><tr><th>Etap</th><th>Temat i lata</th><th style="text-align:right">Czas</th></tr></thead>
    <tbody>{rows}
      <tr class="total"><td></td><td>Razem</td><td style="text-align:right">{total_h} {pl_hours(total_h)}</td></tr>
    </tbody>
  </table>
  <p class="note" style="margin-top:2.6mm">Przy tempie 5–6 godzin w tygodniu całość zajmie około 5–6 tygodni. Wersja skrócona: etapy 2, 4 i 5 to rdzeń historii Malborka.</p>

</section>

<section class="newpage">
  <h2 class="sec"><span class="num">02</span>Tło i pojęcia</h2>
  <p class="lede">W XIII wieku Polska była podzielona na dzielnice. Książęta walczyli ze sobą o Kraków. Na północy żyli Prusowie. Nie mieli państwa ani chrztu. Książę Konrad Mazowiecki sprowadził w 1226 roku Zakon Krzyżacki. Zakon podbił Prusy i zbudował własne państwo. W 1309 roku przeniósł stolicę do Malborka.</p>

  <h3>Dziewięć pojęć, bez których nie zrozumiesz źródeł</h3>
  <ul>{gloss}</ul>

  <div class="box">
    <h3>Dlaczego Malbork jest wyjątkowy?</h3>
    <p>Zamek jest największą ceglaną twierdzą na świecie. Zajmuje około 21 hektarów. Składa się z trzech części: zamku wysokiego, średniego i przedzamcza. Przez 150 lat był stolicą państwa zakonnego. To jedno z niewielu miejsc, gdzie widać całą historię władzy: od zakonu, przez króla polskiego, po pruskie koszary.</p>
  </div>

  <div class="box">
    <h3>Trzy warstwy czasu na zamku</h3>
    <p><b>Warstwa średniowieczna.</b> Gotyckie mury, Pałac Wielkich Mistrzów, kościół NMP.<br>
    <b>Warstwa pruska.</b> Odbudowa z XIX wieku według wizji romantyków.<br>
    <b>Warstwa powojenna.</b> Rekonstrukcja po 1945 roku i prace konserwatorskie do dziś.</p>
    <p class="note">Dlatego pytanie „co tu jest oryginalne?” jest trudne. Wróć do niego po etapie 7.</p>
  </div>

  <div class="box">
    <h3>Sześć miejsc na mapie</h3>
    <p><b>Malbork</b> — stolica Zakonu, największy zamek ceglany. <b>Gdańsk</b> — port i punkt sporu o Pomorze.<br>
    <b>Toruń</b> — pierwsza warownia Zakonu, miejsce dwóch pokojów. <b>Grunwald</b> — pole bitwy z 1410 roku.<br>
    <b>Chojnice</b> — klęska polska w 1454 roku. <b>Kwidzyn</b> — miejsce powstania Związku Pruskiego.</p>
    <p class="note">Zaznacz te miejsca na mapie Polski. Zobaczysz, że wszystkie leżą w pasie od Wisły do Bałtyku.</p>
  </div>
</section>

<section class="newpage">
  <h2 class="sec"><span class="num">03</span>Kalendarium</h2>
  <p>Przeczytaj całą listę. Nie ucz się jej na pamięć. Kalendarium pokazuje rytm wydarzeń. Daty znajdziesz też w etapach.</p>
  <h3>Średniowiecze: od Zakonu do II pokoju toruńskiego</h3>
  <table class="tl"><tbody>{tl1}</tbody></table>
  <h3>Później: od hołdu pruskiego do UNESCO</h3>
  <table class="tl"><tbody>{tl2}</tbody></table>
  <div class="box" style="margin-top:3mm">
    <p><b>Zapamiętaj trzy cezury.</b> 1309 — Malbork staje się stolicą. 1410 — Grunwald. 1466 — koniec państwa zakonnego w Malborku. Te trzy daty porządkują całą opowieść.</p>
  </div>
</section>

<div class="newpage"></div>

<section>
  <h2 class="sec"><span class="num">04</span>Osiem etapów nauki</h2>
  <p class="lede">Idź po kolei. Każdy etap kończy się pytaniami. Jeśli nie umiesz odpowiedzieć, wróć do źródeł z tego etapu. Strony dają przegląd, filmy pokazują przebieg, książki dodają tło.</p>
</section>

{stages_html}

<div class="newpage"></div>

<section>
  <h2 class="sec"><span class="num">05</span>Książki</h2>
  <p class="lede">Osiem pozycji. Nie musisz czytać wszystkich. Wybierz jedną książkę na etap i jedną „grubą” na całość.</p>
  {books}
  <div class="box" style="margin-top:1mm">
    <h3>Gdzie kupić lub wypożyczyć</h3>
    <p>{link("Lubimyczytać — opisy i opinie", "https://lubimyczytac.pl/")}<br>
    {link("Biblioteka Narodowa — katalog online", "https://katalogi.bn.org.pl/")}<br>
    {link("Sklep Muzeum Zamkowego — wydawnictwa", "https://zamek.malbork.pl/kategoria-produktu/ksiazki-i-media/")}</p>
  </div>
</section>

<div class="newpage"></div>

<section>
  <h2 class="sec"><span class="num">06</span>Wszystkie linki</h2>
  <p class="lede">Pełne adresy do wydruku. Linki w tekście są klikalne. Ta lista działa także na papierze.</p>
  {appendix}
  <div class="box" style="margin-top:2mm">
    <h3>Jeśli link przestanie działać</h3>
    <p>Wpisz tytuł filmu w wyszukiwarkę YouTube. Wpisz tytuł artykułu na stronie muzeum. Strony zmieniają adresy, ale tytuły zostają. Pełne adresy są tu po to, żebyś miał punkt wyjścia.</p>
  </div>
</section>

<div class="newpage"></div>

<section>
  <h2 class="sec"><span class="num">07</span>Ściąga i sposób sprawdzania źródeł</h2>

  <h3>Plan na sześć tygodni</h3>
  <table>
    <thead><tr><th>Tydzień</th><th>Etapy</th><th>Na czym się skupić</th><th style="text-align:right">Czas</th></tr></thead>
    <tbody>
      <tr><td class="yr">1</td><td>1–2</td><td>Prusowie, zaproszenie Zakonu, pierwsze zamki</td><td style="text-align:right">7 h</td></tr>
      <tr><td class="yr">2</td><td>3</td><td>Malbork jako stolica, spór o Pomorze, Kazimierz Wielki</td><td style="text-align:right">4 h</td></tr>
      <tr><td class="yr">3</td><td>4</td><td>Unia w Krewie, Grunwald, oblężenie Malborka</td><td style="text-align:right">6 h</td></tr>
      <tr><td class="yr">4</td><td>5</td><td>Związek Pruski, wojna trzynastoletnia, 1466</td><td style="text-align:right">5 h</td></tr>
      <tr><td class="yr">5</td><td>6–7</td><td>Prusy, rozbiory, odbudowa, UNESCO</td><td style="text-align:right">8 h</td></tr>
      <tr><td class="yr">6</td><td>8</td><td>Powtórka, własna os czasu, plan wizyty</td><td style="text-align:right">3 h</td></tr>
    </tbody>
  </table>

  <h3>Dwanaście dat, które musisz znać</h3>
  <table class="tl"><tbody>
    <tr><td class='yr'>1226</td><td>Konrad Mazowiecki zaprasza Krzyżaków.</td><td class='yr' style='padding-left:6mm'>1230</td><td>Początek podboju Prus.</td></tr>
    <tr><td class='yr'>1280</td><td>Prawa miejskie Malborka.</td><td class='yr' style='padding-left:6mm'>1309</td><td>Malbork stolicą Zakonu.</td></tr>
    <tr><td class='yr'>1343</td><td>Pokój w Kaliszu.</td><td class='yr' style='padding-left:6mm'>1385</td><td>Unia w Krewie.</td></tr>
    <tr><td class='yr'>1410</td><td>Grunwald i oblężenie Malborka.</td><td class='yr' style='padding-left:6mm'>1411</td><td>I pokój toruński.</td></tr>
    <tr><td class='yr'>1440</td><td>Związek Pruski.</td><td class='yr' style='padding-left:6mm'>1454</td><td>Wybuch wojny trzynastoletniej.</td></tr>
    <tr><td class='yr'>1466</td><td>II pokój toruński.</td><td class='yr' style='padding-left:6mm'>1945</td><td>Zniszczenie zamku i odbudowa.</td></tr>
  </tbody></table>

  <h3>Sześć postaci</h3>
  <ul>
    <li><b>Konrad I Mazowiecki</b> — zaprosił Zakon do Polski.</li>
    <li><b>Hermann von Salza</b> — wielki mistrz, który zbudował podstawy państwa.</li>
    <li><b>Winrich von Kniprode</b> — wielki mistrz w złotym wieku Zakonu.</li>
    <li><b>Ulrich von Jungingen</b> — wielki mistrz poległy pod Grunwaldem.</li>
    <li><b>Heinrich von Plauen</b> — obrońca Malborka w 1410 roku.</li>
    <li><b>Kazimierz Jagiellończyk</b> — przyjął Malbork do Polski w 1457 roku.</li>
  </ul>

  <div class="box dark">
    <h3>Jak sprawdzać źródła</h3>
    <ul>
      <li><b>Porównaj dwie daty.</b> Jeśli źródła się różnią, sprawdź trzecie.</li>
      <li><b>Sprawdź autora.</b> Muzeum i uniwersytet mają większą wagę niż blog.</li>
      <li><b>Wikipedia to start, nie koniec.</b> Zjedź na dół i przeczytaj bibliografię.</li>
      <li><b>Odróżniaj powieść od historii.</b> Sienkiewicz pisał literaturę. Długosz pisał kronikę ze swoim zdaniem.</li>
      <li><b>Uważaj na liczby.</b> „Największy zamek świata” to popularne hasło. Sprawdź, co mierzono.</li>
    </ul>
  </div>

  <div class="box">
    <h3>Co dalej?</h3>
    <p>Po etapie 8 zaplanuj wizytę. Weź notatki. Zwiedzaj z audioprzewodnikiem. Po powrocie przeczytaj jeden rozdział Górskiego. Zobaczysz, jak wiedza z książki spotyka się z murem.</p>
    <p class="note">Plan obejmuje historię polityczną. Nie obejmuje historii sztuki, archeologii ani życia codziennego. To dobry następny krok po opanowaniu podstaw.</p>
  </div>
</section>

</body></html>"""
    return doc, n_links


if __name__ == "__main__":
    doc, n = build_html()
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(doc)
    print("HTML:", len(doc), "znaków;", n, "unikalnych linków")
    subprocess.run([
        CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", "--virtual-time-budget=4000",
        f"--print-to-pdf={PDF_PATH}", "file://" + HTML_PATH,
    ], check=True, capture_output=True)
    print("PDF:", PDF_PATH)
