# Mekholi — experimental 18-style static family

**Version:** 1.0 / Experimental Family 1  
**Designer:** Surajit Singha Sisir  
**Developer:** Ningshing Che  
**Intended language:** Bishnupriya Manipuri, using Bengali/Assamese-script coverage  
**Target:** web and print · **Category:** serif

## Important status
This is a **Kalpurush-derived prototype**, not an independently drawn original typeface. Weights are mechanically generated contour offsets, not optically refined masters. Styles labelled Italic are **12-degree slanted upright outlines**, not true italic designs. Thin strokes, serif detail, heavy counters, spacing and mark attachment need optical review. No native Bishnupriya Manipuri reader or production print/browser approval has been obtained.

There are **18 static styles**, not variable fonts:

| Weight | Upright | Slanted italic |
|---|---|---|
| 100 | Thin | Thin Italic |
| 200 | Extra Light | Extra Light Italic |
| 300 | Light | Light Italic |
| 400 | Regular | Regular Italic |
| 500 | Medium | Medium Italic |
| 600 | Semi Bold | Semi Bold Italic |
| 700 | Bold | Bold Italic |
| 800 | Extra Bold | Extra Bold Italic |
| 900 | Black | Black Italic |

## Contents
- `fonts/ttf/`: 18 desktop/print TTF files.
- `fonts/web/`: 18 WOFF2 files, 18 WOFF files and complete `mekholi.css`.
- `specimens/Mekholi-family-preview.html`: standalone interactive preview with embedded fonts.
- `specimens/Mekholi-family.png` and `.pdf`: raster proof sheets, not prepress certification.
- `source/`: original upstream font and rebuild/validation tools.
- `documentation/`: provenance, family manifest, validation results and checksums.
- `OFL.txt`, `OFL-FAQ.txt`, `FONTLOG.txt`: licensing and change history.

## Web use
Copy the entire `fonts/web/` directory and load `mekholi.css`. Example:

```html
<link rel="stylesheet" href="fonts/web/mekholi.css">
```
```css
body { font-family: 'Mekholi', serif; font-weight: 400; line-height: 1.75; }
h1 { font-weight: 700; }
em { font-style: italic; }
```

Select a shipped weight from 100 to 900 in steps of 100. The CSS uses relative paths and disables font synthesis through the `.mekholi` class. Web use may load only the styles actually requested.

## Desktop use
Install the TTF files. Modern applications should group them under Mekholi using typographic family/style names. Older applications may show weight-specific family names (for example Mekholi Thin), with Regular/Italic style links. Uninstall earlier Mekholi test builds before replacing them to avoid cache and duplicate-name conflicts. Family Regular has unified family line metrics and a different build ID from the earlier standalone prototype; do not install both simultaneously.

## Engineering
1. Rebuild the original Regular derivative: 3% width expansion, synchronized horizontal positioning, revised metadata and removed invalidated hinting.
2. Apply FreeType contour expansion/contraction of -28, -19, -10, 0, +10, +20, +32, +44 and +58 font units; clean weighted contours with Skia PathOps. These are experimental weight assignments, not calibrated stem targets.
3. Preserve original cmap, glyph order, GSUB and GDEF classification; retain GPOS, applying horizontal shear to anchors and placement offsets in slanted styles.
4. Keep advances constant across weights as an initial spacing policy; recalculate outline left sidebearings. This is not a finished spacing/kerning pass.
5. Use common hhea/typo metrics 1100/-650/0 and Windows metrics 1300/700 for consistent family layout. Line-height intention: 1.75 em. No hinting has been regenerated.
6. Embed the complete OFL 1.1 text, project credits, copyright/RFN declarations and correct weight/italic naming in each output; generate WOFF and WOFF2.

## Validation
`documentation/validation.json` records **4,103 strings per style / 73,854 cases total**. Implemented checks pass for:
- table and complete-file TTF checksums;
- glyph outline loading, no newly empty glyphs and unchanged 210-codepoint coverage;
- no `.notdef` output in the tested strings;
- unchanged glyph selection/cluster mapping relative to upstream;
- no tested shaped outlines beyond the chosen Windows vertical metrics;
- expected licensing, weight and italic metadata;
- WOFF/WOFF2 reopen with the same cmap and glyph order.

These tests do not establish linguistic correctness, collision-free marks, preserved thin details, ideal counters, full contour topology, hinting quality or cross-platform production readiness. Other Unicode sequences and stacked marks can still expose problems. Actual FreeType sample renders are included for visual review.

## Rebuild on Linux
Requires Python 3.11+ and the FreeType shared library, e.g. Debian/Ubuntu `libfreetype6`.

```sh
pip install -r source/requirements.txt
python source/build_family.py
python source/validate_family.py
```

`build_regular.py` creates the base; `weight_outlines.py` uses FreeType and Skia PathOps; `build_family.py` packages all styles. No FontForge dependency is used in the final build. Output is static TTF/WOFF/WOFF2, not a multi-master design source or variable font. Original input and older upstream license metadata are retained for provenance.

## License and attribution
SIL Open Font License 1.1: https://openfontlicense.org/ — see `OFL.txt`.

Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che, for Mekholi modifications, with Reserved Font Name Mekholi.

Upstream copyright (c) 2022 Tanbin Islam Siyam, with Reserved Font Name Kalpurush. Original Bengali design by Md. Tanbin Islam Siyam / Avro Font Development Project; Latin based on Gentium. Acknowledgment does not imply endorsement. The upstream LICENSE/older embedded 1.0 discrepancy is recorded in `documentation/PROVENANCE.md`.

Redistribute fonts with their notices and OFL. Modified fonts must respect Reserved Font Names unless permission is obtained. Font files cannot be sold by themselves; documents created with them are not required to use the OFL.
