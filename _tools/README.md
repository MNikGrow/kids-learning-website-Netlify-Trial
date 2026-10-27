# BodhiCubs content tools

Used by the monthly BodhiCubs marketing task.

- `printables_lib.py` – shared drawing helpers (fonts, icons, page frame, word search, maze, picture sudoku).
- `example_christmas_packs.py` – how the Christmas packs were built (cover, thank-you page, color + B&W, answer keys).
- `example_pins.py` – how the 1000x1500 Pinterest pins were built from PDF pages.

Each monthly pack lives at `/printables/<slug>/` with `index.html`, PDFs and `img/` previews,
and is linked from `/printables/index.html` and listed in `/sitemap.xml`.
