# Malbork

Zamek w Malborku to największa ceglana twierdza świata. Przez prawie 150 lat był
stolicą państwa zakonnego. Ten folder zawiera plan nauki jego historii razem
z historią Polski w średniowieczu.

## Co jest w środku

| Plik | Do czego |
|:-----|:---------|
| [PLAN.md](PLAN.md) | Plan nauki: 8 etapów, kalendarium, źródła i pytania. Czytaj na ekranie. |
| [Malbork_plan_nauki_i_zrodla.pdf](Malbork_plan_nauki_i_zrodla.pdf) | Ta sama treść do druku. 12 stron, A4. |
| `build/` | Skrypty, które generują oba pliki. |

## Od czego zacząć

Etap 1 daje tło. Etap 2 pokazuje, jak powstało państwo zakonne. Etap 4 prowadzi
przez Grunwald i oblężenie Malborka. Etap 5 tłumaczy, jak Malbork wrócił do Polski.
Etapy 2, 4 i 5 to rdzeń.

## Jak przebudować PDF

Potrzebujesz Pythona 3 i Chrome albo Chromium.

```bash
cd build
python3 build.py     # tworzy PDF i przewodnik.html
python3 make_md.py   # tworzy PLAN.md
```

Jeśli Chrome jest w nietypowym miejscu, ustaw zmienną `CHROME`:

```bash
CHROME=/usr/bin/chromium python3 build.py
```

## Gdzie zmieniać treść

Cała treść siedzi w `build/build.py`. Szukaj list:

- `STAGES` — osiem etapów: wydarzenia, linki, pytania.
- `TIMELINE_1` i `TIMELINE_2` — kalendarium.
- `GLOSSARY` — słownik pojęć.
- `BOOKS` — książki.
- `WEB_EXTRA` — linki w dodatku.

Zmieniasz dane w jednym miejscu. PDF i Markdown powstają z tych samych danych.

## Uwagi

- Linki sprawdzone 4 listopada 2026.
- Wikipedia to punkt startowy, nie źródło naukowe.
- „Krzyżacy” Sienkiewicza to powieść, nie podręcznik.
- Daty sporów (na przykład rzeź Gdańska w 1308) warto sprawdzić w dwóch źródłach.
