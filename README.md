# Mekholi Fonts — মেখলি

A Bishnupriya Manipuri serif font project.

**Designer:** Surajit Singha Sisir · **Developer:** Ningshing Che

## Current experimental family
See **[mekholi-family/README.md](mekholi-family/README.md)** for all 18 static styles, installation, web CSS, licensing and build instructions.

- [Desktop TTF files](mekholi-family/fonts/ttf/)
- [Web WOFF/WOFF2 and CSS](mekholi-family/fonts/web/)
- [Interactive preview — download and open in a browser](mekholi-family/specimens/Mekholi-family-preview.html)
- [Visual proof sheet](mekholi-family/specimens/Mekholi-family.png)
- [OFL 1.1 and copyright/RFN notices](mekholi-family/OFL.txt)
- [Validation results](mekholi-family/documentation/validation.json)

**Not a finished original design:** Mekholi currently derives from Kalpurush, with an initial 3% horizontal expansion. Additional weights are mechanical contour offsets; italic-labelled styles are slanted uprights. Native-language validation, distinctive redraws and optical refinement remain pending. The prototype family is not a variable font.

## Repository structure
- `mekholi-family/`: current experimental 18-style family, under SIL OFL 1.1.
- `mekholi-prototype/`: earlier standalone Regular prototype and its history. Do not install it alongside family Regular.
- `ttf/`: original reference files supplied with this repository, left unchanged. They are **not** Mekholi releases; the Mekholi license notice does not relicense these third-party files. In particular, SutonnyOMJ rights remain unresolved and it was not used in Mekholi.

Mekholi modifications copyright (c) 2026 Surajit Singha Sisir and Ningshing Che; Reserved Font Name Mekholi. Upstream copyright and Reserved Font Names are retained in the family license. https://openfontlicense.org/


## Documentation website & playground

- **Website:** https://sisir-sinha.github.io/Mekholi-Fonts/
- **Complete font guide:** https://sisir-sinha.github.io/Mekholi-Fonts/documentation.html
- **License guide:** https://sisir-sinha.github.io/Mekholi-Fonts/license.html
- **Live sandbox:** https://sisir-sinha.github.io/Mekholi-Fonts/playground.html

The Bengali display name is **মেখলি**. Internal font naming remains **Mekholi**.

The site has no external font CDN or analytics. The playground offers all 18 styles, custom text, size/leading/tracking/alignment and color controls, character-coverage checks, CSS copying, fragment-based sample sharing, and local 2× PNG proof export. It does not save samples on a server. No native-language or production approval is implied.

### GitHub Pages
The root `_config.yml` and static HTML pages work with `.github/workflows/jekyll-gh-pages.yml`. In repository **Settings → Pages**, use **GitHub Actions** as the source. The workflow publishes on pushes to `main`; the public URL is available after a successful deployment. Relative asset URLs work under the project path `/Mekholi-Fonts/`.

### Maintain and preview the site
```sh
python tools/build_site.py     # regenerate pages and downloadable ZIP
python tools/check_site.py     # dependency-free links/assets/package checks
python -m http.server 8000     # then open http://localhost:8000
```

The website generator uses only Python's standard library. Font binaries do not change when generating the site. `assets/coverage.json` lists the 210 currently mapped code points; update it from the font cmap if coverage changes. Font builds have separate dependencies described in the family README.
