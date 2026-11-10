# Zwiedzanie

Przewodniki po miejscach, które warto zobaczyć na żywo. Każdy folder to jedno miejsce.
W środku znajdziesz plan nauki, listę źródeł i PDF do wydruku.

## Miejsca

| Miejsce | Temat | Czas | Pliki |
|:--------|:------|-----:|:------|
| [Malbork](malbork/) | Zamek krzyżacki i Polska w średniowieczu | 33 godziny | [PLAN.md](malbork/PLAN.md) · [PDF](malbork/Malbork_plan_nauki_i_zrodla.pdf) |
| [Malbork — Trasy](malbork/) | Kompletne trasy zwiedzania miasta (listopad) | 1–2 dni | [TRASY_ZWIEDZANIA.md](malbork/TRASY_ZWIEDZANIA.md) · [PDF](malbork/Malbork_trasy_zwiedzania_listopad.pdf) |

## Jak czytać

1. Otwórz `PLAN.md`. To wersja do czytania na ekranie. Linki działają.
2. Weź PDF, gdy chcesz drukować albo uczyć się bez internetu.
3. Idź etapami. Po każdym etapie odpowiedz na pytania.

## Struktura

```
zwiedzanie/
├── README.md
└── malbork/
    ├── README.md                     # co jest w folderze i jak go przebudować
    ├── PLAN.md                       # plan nauki w Markdown
    ├── TRASY_ZWIEDZANIA.md           # trasy zwiedzania w Markdown
    ├── Malbork_plan_nauki_i_zrodla.pdf
    ├── Malbork_trasy_zwiedzania_listopad.pdf
    └── build/
        ├── build.py                  # generuje plan nauki (PDF i HTML)
        ├── build_trasy.py            # generuje trasy zwiedzania (PDF, MD i HTML)
        └── make_md.py                # generuje PLAN.md
```

## Dodanie kolejnego miejsca

1. Zrób folder z nazwą miejsca, na przykład `torun/`.
2. Skopiuj `malbork/README.md` i zmień treść.
3. Dodaj plan w Markdown i PDF.
4. Dopisz wiersz w tabeli „Miejsca” powyżej.

## O źródłach

Wszystkie linki sprawdziłem w listopadzie 2026. Prowadzą do stron muzeów, Wikipedii,
YouTube i portali historycznych. To nie jest praca naukowa. To plan nauki dla osoby,
która zaczyna i chce mieć porządek zamiast przypadkowych linków.

Wikipedia służy tu jako punkt startowy. Każdy artykuł ma na dole bibliografię.
Warto tam zajrzeć, gdy temat zaczyna wciągać.
