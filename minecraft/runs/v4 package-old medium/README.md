# Crafting Europe design package

This concept package implements the six-denomination, twelve-side series described in the supplied proposal and construction specification.

## Primary review files

Open `06_exports/review_png/` for the twelve exact-trim sRGB note faces. Contact sheets are in `06_exports/contact_sheets/`. Generated scene sources are preserved unchanged in `04_scene_plates/`; shared vectors, ore identifiers, palette data, layout data, layer handoffs, manifests, and checksums are included.

## Production status

The package is suitable for concept review. It is deliberately marked `SPECIMEN • ART CONCEPT • NOT LEGAL TENDER`. The ore cubes are deterministic project-created stand-ins because no licensed canonical texture captures were supplied; replace them with approved source textures before public or commercial production. The Europe silhouette is a consistent concept master and should be replaced by an approved geographic source before final geographic QA. Typeface SVGs retain text objects for editability; outline them in the chosen production font before archive approval. Specialist security, tactile, CMYK, accessibility, and print-production testing remain separate phases.

## Generation method

The twelve source scenes were created with the built-in image-generation workflow. All note furniture and assembly were generated deterministically from `layout.json` and `palettes.json`.
