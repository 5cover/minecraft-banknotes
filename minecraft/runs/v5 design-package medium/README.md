# Crafting Europe design package

This folder is a self-contained, deterministic concept-design kit for twelve fictional euro banknotes. It implements the supplied proposal and package specification with generated Minecraft-native scene plates, supplied institutional assets, supplied ore-block rasters, repeatable typography assets, fixed layout data, exact-size final PNGs, and contact sheets.

## Build

From this folder, run:

    python scripts/build_type_assets.py
    python scripts/build_notes.py --layer-previews
    python scripts/build_contact_sheets.py
    python scripts/check_package.py

Requirements: Python 3.10+, Pillow, PyYAML, and fontTools. Pre-rendered PNG companions for the supplied SVG assets are included. If either companion is removed, `scripts/rasterize_svg.js` can rebuild it with Node.js and Sharp.

## Asset policy

- The supplied `Minecraft.ttf` is authoritative for Latin lettering, numerals, and the euro sign.
- The font does not contain Greek or Cyrillic glyphs. Matching block-grid outlines for `ΕΥΡΩ` and `ЕВРО` are therefore created by `build_type_assets.py`; this is recorded in `generation-record.yaml`.
- The six supplied denomination ore blocks are used without reinterpretation. `iron.webp` is retained as a supporting asset but is not a denomination motif.
- The supplied EU flag and Europe map SVGs are preserved unchanged and rasterized only during composition.
- The twelve scene plates are generated raster intermediates. No text, flag, map, ore medallion, or denomination typography is embedded in them.
- Frames and empty ore medallions are generated deterministically by `build_notes.py`, rather than painted into the scene plates.

## Output

`outputs/notes/` contains the twelve exact-size flattened notes. `outputs/contacts/` contains recto, verso, paired, and grayscale review sheets. `outputs/layer_previews/` contains full-canvas placed layers for inspection and optional editing.

The scene prompt set is preserved in `docs/scene-prompts.md`.

The included scene plates use lossless indexed-colour PNG encoding to keep the portable package compact. `scripts/optimize_scene_plates.py` reapplies that encoding after scene replacement if desired.

This is fictional concept art and is deliberately distinguishable from circulating legal tender.
