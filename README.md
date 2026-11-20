# வால்மீகி ராமாயணம் — Valmiki Ramayanam (Tamil)

A free reading site for the original **Valmiki Ramayanam**, sargam by sargam:

- a Tamil story (கதைச் சுருக்கம்) for every sargam,
- every Sanskrit shloka, in Tamil script (with ² ³ ⁴ marks) or Devanagari,
- a Tamil meaning (பொருள்) under each shloka,
- simple cartoon-style pictures for the chapter and for each scene,
- read-aloud buttons (story, and all shlokas with Tamil meaning) with previous / pause / next / stop, using the phone's own Tamil voice.

Only Valmiki's text is followed: nothing from Kamba Ramayanam or TV versions.

Live site: https://rajkumar71234-ui.github.io/valmiki-ramayanam/

## How the site is organised

| Path | What it is |
|---|---|
| `index.html`, `kandam.html`, `sargam.html` | The three pages (home, list of sargams, chapter page) |
| `assets/` | Styles, script, icon |
| `data/kandams.json` | The 7 Kandams, sargam counts (648 in total) and which sargams are ready |
| `data/<k>/<sss>.json` | One file per sargam, built by the tool below |
| `img/<k>/<sss>/` | The pictures for that sargam (SVG, about 20 KB each) |
| `content/<k>/<sss>.sa.wiki` | Sanskrit source text (from Sanskrit Wikisource) |
| `content/<k>/<sss>.ta.json` | Tamil story, scenes and Tamil meaning of each shloka |
| `tools/` | Build scripts and the drawing kit |

## Adding a sargam

1. Save the Sanskrit Wikisource text as `content/<k>/<sss>.sa.wiki`
   (page `रामायणम्/<काण्डम्>/सर्गः <n>`, `?action=raw`).
2. Write `content/<k>/<sss>.ta.json` (story, scenes, meanings — see `content/1/002.ta.json`).
3. Draw the pictures with `tools/art.py` (see `tools/art_1_002.py`).
4. Build: `python3 tools/build_sarga.py <k> <s> --check <second-source.json>`
   (needs `pip install aksharamukha`). The check flags verses that differ from a second edition.

## Sources and credits

- Sanskrit text: Sanskrit Wikisource (southern recension); sargam and shloka numbers follow it.
  Cross-checked against the DharmicData / IIT Kanpur verse files.
- Tamil-script conversion: Aksharamukha.
- Tamil story, Tamil meanings and pictures: written and drawn fresh for this site.
  Found a mistake? Use the “பிழை தெரிவிக்க” link under any shloka.
