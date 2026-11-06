# Site maintenance and tests

Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
SIL OFL 1.1: https://openfontlicense.org/ — see `mekholi-family/OFL.txt`.

From the repository root:

```sh
python tools/build_site.py
python tools/check_site.py
jekyll build
```

`check_site.py` uses only the Python standard library and runs in the existing Pages workflow before Jekyll. It checks local links/anchors, CSS assets, the Bengali name, coverage count, ZIP integrity, license matching and the archive's 54 font files. It does not verify external URLs or all accessibility requirements.

Optional Chromium functional tests:

```sh
pip install playwright
python -m playwright install --with-deps chromium
python -m http.server 8000
# In another terminal:
python tools/test_browser.py
# Test the built output at a subpath:
MEKHOLI_SITE_URL=http://127.0.0.1:8000/_site/ python tools/test_browser.py
```

These tests load all four pages and all 18 font faces; exercise controls, presets, unmapped-character warnings, CSS clipboard copying, shared-sample restoration, PNG downloading and resetting; check mobile horizontal overflow; and collect JavaScript and HTTP errors. The tests need clipboard permissions and a browser environment capable of PNG downloads. The exported image is written to the operating system's temporary directory.

The initial implementation passed local Chromium checks on source and built Jekyll output, including a nested URL path. This is not a claim of Safari/Firefox/Android/iOS, assistive-technology or production print certification. Site updates do not change the existing font binaries or retroactively certify their original shape design.
