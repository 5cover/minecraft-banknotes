# Crafting Europe

Twelve finished banknote concept PNGs implement proposal-v8.md at its exact canvas sizes. Export names follow the naming convention approved in the conversation. Each recto contains the supplied canonical ore insert; reverses carry the constructed scenes without a repeated ore emblem.

## Build

Use Python 3.10 or later and Inkscape 1.2 or later on PATH. Install Python dependencies with `python -m pip install -r requirements.txt`. From the package root run, in order:

1. `python scripts/build_type_assets.py`
2. `python scripts/build_contexts.py`
3. `python scripts/build_notes.py`
4. `python scripts/build_contact_sheets.py`

The retained image plates are the build inputs. No image service or account is required to rebuild the final PNGs. The image generator itself is not deterministic. Prompts, actual contexts, primary pixels and transparent monetary-artwork pixels are retained for creative regeneration.

For positioned full-canvas layers, run `python scripts/build_notes.py --design EUR005_recto --layers`. Omit `--design` to export layers for all designs. These optional files are not needed for the normal build.

The delivered outputs were checked with `python scripts/verify_build.py`: exact sizes and identical deterministic rebuilds for all twelve files, plus font preservation and script coverage. Dependency versions are pinned in `requirements.txt`; the SVG renderer version is recorded in `generation-record.yaml`.

## Editing

`layout.yaml` controls dimensions, exports, scene crop, asset boxes, edge extension, colours, paper-grain seed and layer order. Coordinates are normalized xywh boxes. All paths are relative to this root. Primary plates are fitted to their recorded boxes at the recorded centre; a small edge-pixel extension underneath the decorative frame prevents paper seams without changing the visible approved composition. Monetary plates are resized to the final canvas; their original generated dimensions and alpha are preserved in the source PNGs.

Value outlines are fitted to their boxes as controlled monetary lettering, with a common top and cap-height alignment. The three euro scripts are one outlined SVG object with common capital height, natural spacing and centred lines. The Europe map and flag use the supplied SVG geometry; the map receives a uniform denomination ink and 70 percent alpha. The flag has restrained overprint opacity. Original ore rasters are cropped only to alpha bounds and fitted at a common scale. A feathered paper underprint supports script legibility over dense ornament. A seeded fine paper grain is applied after composition. Signature and serial areas are design reservations, not issued identifiers. Edge mark groups are a visual tactile concept, not a physical production specification.

Changing only fixed assets or coordinates needs no image generation. Replacing a primary requires review of its dependent context and monetary artwork. `generation-record.yaml` gives that relationship and prompt paths.

## Font extension

`assets/approved/Minecraft-Crafting-Europe.ttf` is also provided separately. It adds U+0395, U+03A5, U+03A1, U+03A9, U+0415, U+0412, U+0420 and U+041E for ΕΥΡΩ and ЕВРО. Seven matching forms reuse the supplied Latin outlines under distinct Unicode mappings. Omega is newly drawn on the source's 64-unit grid with a 768-unit capital height and 128-unit principal strokes. Advance widths and spacing follow the matching source capitals. All pre-existing outlines, metrics and Unicode mappings are preserved. The family and PostScript names distinguish the modified font from the original. This is the required capital extension, not full Greek or Cyrillic language coverage.

`build_type_assets.py` rebuilds the font, outlined denominations, grouped scripts and specimen. Source attribution remains CraftronGaming; no additional redistribution licence is asserted. The original font and ore rasters are preserved under `assets/supplied/inputs/`.

## Review

`outputs/contacts/Crafting_Europe_contact_sheet.png` pairs all rectos and versos. `outputs/contacts/font-specimen.png` shows the font extension. Notes are flattened RGB PNGs with no presentation margin. This is a layered design study, not a manufacturing or security master.
