# Mekholi · Version 1.0 · Regular prototype 1

**Designer:** Surajit Singha Sisir  
**Developer:** Ningshing Che  
**Intended language:** Bishnupriya Manipuri (Bengali/Assamese script)  
**Style:** Serif · Regular 400, upright  
**Target:** Web and print  
**Status:** Experimental derivative, awaiting native-language and visual approval.

## What this bundle contains
- `fonts/ttf/Mekholi-Regular.ttf`: installable desktop/print font.
- `fonts/web/Mekholi-Regular.woff2` and `.woff`: web fonts.
- `fonts/web/mekholi.css`: ready-to-copy CSS with relative font paths.
- `specimens/Mekholi-preview.html`: self-contained preview with embedded fonts, upstream comparison, and editable sample.
- `specimens/Mekholi-Regular-specimen.png` and `.pdf`: raster visual proof; PDF is not an embedded-font/prepress certification.
- `source/`: original upstream input, reproducible build and validation scripts, requirements.
- `documentation/`: validation, exact changes, licensing/provenance, Unicode coverage, full-family roadmap.
- `OFL.txt`: SIL OFL 1.1 with retained upstream notice and added Mekholi copyright/RFN header.

## What changed—and what did not
This prototype derives directly from Kalpurush 0.258. It is **not a newly drawn, original typeface**. Its first visual change is a 3% horizontal expansion of outlines, advances, horizontal mark positioning and caret coordinates. Vertical letter shapes are unchanged. It remains very close to Kalpurush.

Naming, credits, line metrics and web packaging were revised. Old grid-fitting data was removed because it no longer matches the changed outlines. No new glyphs or language-specific ligatures were drawn. Existing GSUB and GPOS functionality is retained. It has 586 glyphs and 210 mapped Unicode code points, including basic Latin, digits and much of the Bengali/Assamese script, but not every assigned character in that script.

“Version 1.0” is the requested project version; the binary name also says **Prototype 1**. It does not mean production approval. The naming is provisionally Mekholi; no trademark/name-collision search has been completed.

## Install and use
Install the TTF using your operating system's font installer. In design software choose **Mekholi / Regular**. Keep this experimental build out of production documents until reviewed. Remove or disable earlier Mekholi prototypes when testing a replacement, to avoid font-cache conflicts.

For a website, copy the entire `fonts/web/` directory and load its CSS. Use:

```css
body { font-family: 'Mekholi', serif; font-weight: 400; line-height: 1.6; }
```

The supplied CSS disables synthetic bold and italic. Do not request other weights yet. This bundle contains one static font, **not a variable font**.

## Next approval milestone
1. Review the embedded upstream-versus-Mekholi specimens at text and display sizes.
2. Supply a native Bishnupriya Manipuri alphabet, running text, names, punctuation and essential conjuncts, including use of ৰ/ৱ if required.
3. Decide what to redraw: base proportions, terminals/serifs, vowel signs and conjunct personality. A width adjustment alone is not enough for a distinctive finished design.
4. Validate native-language text with a fluent reader, then check collisions, browsers, Office, PDFs and actual print output.
5. Develop Regular and Bold masters; extend toward Thin/Black through optical corrections and compatible interpolation. Draw genuine italic masters rather than just slanting upright outlines.
6. Deliver the 18 planned static styles and, if desired, separately engineered variable upright/italic fonts. No delivery dates or completed family are implied by the roadmap.

## Rebuild
Python 3.11+ recommended:

```sh
pip install -r source/requirements.txt
python source/build.py
python source/validate.py
```

Build transforms use fontTools; validation uses HarfBuzz through uharfbuzz. The source TTF is a binary starting point, not a newly authored editable multi-master design source. All project additions were made locally; no commit or push was performed.

## License
Font derivatives are distributed under SIL OFL 1.1; preserve `OFL.txt` and upstream attribution. The upstream reserved name is **Kalpurush**; the new family uses **Mekholi**. See `documentation/PROVENANCE.md` for the historical 1.0/1.1 discrepancy. No upstream endorsement is claimed. Font files cannot be sold by themselves under OFL; documents and designs made with them are not thereby licensed under OFL.


---
Mekholi modifications copyright (c) 2026 Surajit Singha Sisir and Ningshing Che. Reserved Font Name: Mekholi. Licensed under SIL OFL 1.1: https://openfontlicense.org/ — see `OFL.txt`. Upstream copyright and RFN are preserved in that file.

## Reserved name and licensing metadata
Mekholi is now a Reserved Font Name, as confirmed by the project owner. Downstream modified fonts must not use that primary name without permission from the corresponding copyright holders. The original upstream RFN Kalpurush remains in the notices. `FONTLOG.txt` records this metadata-only revision; the full license is embedded in all three generated fonts.
