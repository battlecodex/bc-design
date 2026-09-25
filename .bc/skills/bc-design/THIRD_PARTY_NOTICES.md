# Third-party notices

This file travels with every installed copy of the BC Design skill family. The MIT license of the BC Design project covers original BC Design code and documentation only; the material below remains under its upstream terms.

## UI UX Pro Max

- **Upstream:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Used here:** the catalog data in `data/` is derived from the UI UX Pro Max data set. This covers `styles.csv`, `colors.csv`, `typography.csv`, `ux-guidelines.csv`, `charts.csv`, `products.csv`, `landing.csv`, `icons.csv`, `app-interface.csv`, `react-performance.csv`, `ui-reasoning.csv`, `motion.csv`, `catalog-summary.json`, `data-provenance.json`, `google-fonts.csv`, `google-font-licenses.json`, `phosphor-icons-upstream.json`, and the stack catalogs in `data/stacks/`. BC Design adds `alignment-overrides.json`, `bc-alignment-policy.json`, `spatial-effects.csv`, and its own search, audit, and generator scripts.

```
MIT License

Copyright (c) 2024 Next Level Builder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ThreeUI

- **Upstream:** https://github.com/MengTo/threeui (Community release)
- **Used here:** the spatial generators in `scripts/spatial.py` and the templates in `assets/spatial/` adapt ThreeUI scene architecture, including the ribbon wave field. No ThreeUI Pro or Beta component source is included.

```
MIT License

Copyright (c) 2026 Meng To

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Google Fonts metadata

`data/google-fonts.csv` and `data/google-font-licenses.json` describe families from [google/fonts](https://github.com/google/fonts). The per-family license recorded in `google-font-licenses.json` is the source of truth for any font use; families may be licensed under the SIL Open Font License (OFL) or Apache License 2.0. Follow the applicable family license when distributing font files or generated assets.

## Phosphor icon metadata

`data/phosphor-icons-upstream.json` is a catalog snapshot of [Phosphor Icons](https://github.com/phosphor-icons/core). Phosphor's upstream license and attribution terms apply if you use the icons themselves; BC Design does not relicense upstream icon artwork.
