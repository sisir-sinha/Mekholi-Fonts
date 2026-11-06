# Prototype 1 changes

1. Family Mekholi, style Regular, PostScript Mekholi-Regular, weight 400, version 1.000 / Prototype 1. Project designer/developer recorded separately from upstream attribution.
2. All outlines decomposed and expanded horizontally by 1.03. Advances and left-sidebearings expanded with OpenType rounding. Horizontal GPOS placement/advance/anchor coordinates and GDEF coordinate caret values expanded consistently. No new letters or ligatures.
3. Original invalidated TrueType hint programs and precomputed device metrics removed. Font remains unhinted; small-screen performance requires review. `gasp` enables smoothing/grid-fit behavior where available but does not supply hinting instructions.
4. hhea and OS/2 typo ascender 1050, descender -550, gap 0. Windows ascent 1100, descent 550. OS/2 version 4 with USE_TYPO_METRICS enabled. Line-height intention 1.6 em. Glyph-bound containment is not a guarantee for every possible stacked-mark sequence.
5. The initial Windows descent proposal of 500 failed on synthetic ছ্বু and ঞ্ঝু (bottoms -518 and -508). Final descent 550 contains all tested shaped output.
6. Existing coverage and layout preserved. No variation axes; no bold/italic generated. Upstream units-per-em remains 1000.
7. WOFF and WOFF2 generated from the revised TTF. All formats reopen successfully. Full-file checksum and every table checksum pass on the TTF.
8. Validation: 4,103 strings, no missing glyphs, no changes to glyph IDs/clusters versus upstream, no vertical overflow against the chosen Windows bounds in that corpus. Advance scaling matches the expected 1.03 rounded result. This does not test every collision or establish linguistic correctness.
9. Historical head timestamps retained for rebuild stability; they are not Mekholi release dates. The inherited PANOSE serif classification remains unchanged; it is not a newly assessed classification.

## Known gaps
- No native Bishnupriya Manipuri corpus or reader approval yet.
- No independently drawn original shape system yet; 3% width change is a preliminary experiment.
- No kerning redesign, optical-size masters, regenerated hinting, or exhaustive contour QA.
- No OTS/FontBakery certification, real-browser screenshots, DirectWrite/CoreText/Android tests, or press proof.
- Unmapped assigned Bengali characters include U+0980, U+09FB, U+09FC, U+09FD, U+09FE. Coverage inventory is in `coverage.txt`.


---
Mekholi modifications copyright (c) 2026 Surajit Singha Sisir and Ningshing Che. Reserved Font Name: Mekholi. Licensed under SIL OFL 1.1: https://openfontlicense.org/ — see `OFL.txt`. Upstream copyright and RFN are preserved in that file.
