# Crafting Europe

## Layered professional design package specification

### Purpose

This document defines the practical production workflow for the final twelve banknote images.

The proposal defines meaning, narrative, and visual intent.
This package defines reusable assets, generated intermediates, fixed layer structure, deterministic composition, export sizes, and the documentation required to rebuild the finished notes.

The objective is simple:

- generate only what benefits from AI generation;
- reuse everything that can be reused;
- keep generated elements swappable;
- keep final assembly deterministic;
- deliver finished banknotes that can be viewed immediately, without manual reconstruction.

This is not a speculative print-studio archive. It is a reproducible design package for concept-quality fictional banknotes.

## Core principles

1. Separate generation from composition.

   AI should generate scene-dependent imagery and a small number of decorative plates. It should not be responsible for repeatedly redrawing stable institutional elements.

2. Turn repeatable elements into assets.

   Ore blocks, lettering, numerals, the EU flag, the Europe map, and other stable components should be stored once and reused.

3. Assemble the final notes deterministically.

   Final note construction should be performed by Python scripts from fixed coordinates and documented rules, not by manual drag-and-drop and not by asking an image model to rediscover the layout.

4. Prefer vector where appropriate.

   Typography, numerals, the EU flag, and the Europe map should remain vector assets whenever possible. Scene imagery and AI-generated decorative plates remain raster.

5. Keep the package self-contained.

   The package must include the final exported notes, all reusable inputs, all generated intermediates used to build them, the composition scripts, and the documentation required to reproduce the assembly.

6. Keep the workflow simple.

   Avoid unnecessary archival machinery. No CSV manifests, no decorative bureaucracy, and no redundant pseudo-professional outputs. Use Markdown for documentation and YAML for structured data.

## 1. Authoritative final output sizes

The final flattened note exports use the following exact trim sizes.

| File               | Side       | Aspect ratio | Scale by |          Size |
| ------------------ | ---------- | ------------ | -------- | ------------: |
| `EUR005_recto.png` | €5 recto   | 60:31        | 30       | 1800 × 930 px |
| `EUR005_verso.png` | €5 verso   | 60:31        | 30       | 1800 × 930 px |
| `EUR010_recto.png` | €10 recto  | 127:67       | 14       | 1778 × 938 px |
| `EUR010_verso.png` | €10 verso  | 127:67       | 14       | 1778 × 938 px |
| `EUR020_recto.png` | €20 recto  | 133:72       | 13       | 1729 × 936 px |
| `EUR020_verso.png` | €20 verso  | 133:72       | 13       | 1729 × 936 px |
| `EUR050_recto.png` | €50 recto  | 20:11        | 85       | 1700 × 935 px |
| `EUR050_verso.png` | €50 verso  | 20:11        | 85       | 1700 × 935 px |
| `EUR100_recto.png` | €100 recto | 147:82       | 11       | 1617 × 902 px |
| `EUR100_verso.png` | €100 verso | 147:82       | 11       | 1617 × 902 px |
| `EUR200_recto.png` | €200 recto | 153:82       | 11       | 1683 × 902 px |
| `EUR200_verso.png` | €200 verso | 153:82       | 11       | 1683 × 902 px |

These dimensions are the authoritative output canvases.

No outer presentation margin, mockup background, photographed-paper context, skew, or drop shadow is part of the final note files.

## 2. Deliverable contents

The final package must contain:

- `design-package-v2.md` or the approved package specification file;
- the theme proposal file used as conceptual reference;
- a short `README.md` describing the package;
- the composition scripts used to build the notes;
- the YAML configuration files used by the scripts;
- all provided assets;
- all generated intermediate plates actually used in the final build;
- the final flattened note PNGs;
- one or more contact sheets for fast review.

The package should not require the recipient to spend significant time reconstructing the notes manually in an image editor.

## 3. Package structure

Use a simple structure such as:

- `README.md`
- `design-package-v2.md`
- `layout.yaml`
- `palette.yaml`
- `generation-record.yaml`
- `scripts/`
  - `build_notes.py`
  - `build_type_assets.py`
  - `build_contact_sheets.py`
- `assets/`
  - `font/`
  - `ore_blocks/`
  - `maps/`
  - `flags/`
  - `type_svg/`
  - `type_png/`
  - `placeholders/`
- `generated/`
  - `scenes/`
  - `frames/`
  - `ore_labels/`
  - `map_tweaks/`
- `outputs/`
  - `notes/`
  - `contacts/`
  - `layer_previews/`
- `docs/`
  - proposal and supporting notes

The exact tree may be adapted, but the distinction between shared assets, generated plates, scripts, and final outputs must remain clear.

## 4. Naming convention

Use one stable file naming system.

Recommended pattern:

- `EUR005_recto_scene.png`
- `EUR005_recto_frame.png`
- `EUR005_recto_label.png`
- `EUR005_recto_final.png`
- `EUR005_recto_layers.png` only if a preview is exported
- `ore_coal_iso.png`
- `eu_flag_master.svg`
- `europe_map_master.svg`
- `euro_scripts_master.svg`
- `value_005_master.svg`

Use `recto` and `verso` in names rather than single-letter abbreviations. The files are few enough that readability matters more than extreme abbreviation.

## 5. Inputs and reusable assets

The following inputs are provided and become part of the package.

### 5.1 Isometric ore rasters

Provided ore blocks are authoritative reusable assets.

Use one raster file for each denomination motif:

- coal ore;
- redstone ore;
- lapis ore;
- copper ore;
- emerald ore;
- gold ore.

These files are inserted into the ore-label field. They are not regenerated as part of the final layout.

If light paper integration or minor colour adaptation is required, create a derived display version from the provided file and freeze it as the project asset. Do not ask the image model to reinterpret the block.

### 5.2 Minecraft typeface

The provided TTF file is a source asset, not a runtime dependency.

Use it to generate deterministic typography assets through a Python script.
The composition pipeline should not rely on SVG text elements that assume the font is installed on the viewer’s system.

The recommended method is:

1. use the TTF file in `build_type_assets.py`;
2. generate the required strings and numerals;
3. convert them to outlined SVG paths;
4. optionally rasterize matching transparent PNG versions for easier preview or manual import.

The final composition should use the derived outlined SVG assets, or their matching raster exports if needed, not live font references.

Required strings and numeral assets include:

- `EURO`
- `ΕΥΡΩ`
- `ЕВРО`
- `5`, `10`, `20`, `50`, `100`, `200`
- `€`
- any small repeated denomination strings used consistently across the series

Spacing, scale, and treatment should be defined once and reused.

### 5.3 EU flag SVG

The provided EU flag SVG is a stable reusable asset.

Do not regenerate it.
Do not redraw the stars.
Do not replace it with an AI-painted rectangle.

The script may recolour or lightly integrate it into the note through opacity, texture overlay, or subtle tonal adjustment if that treatment is explicitly documented and remains consistent.

### 5.4 Europe map SVG

The provided Europe map SVG is also a reusable asset.

Unlike the flag, the map may be tweaked if necessary.
Permitted tweaks include:

- adding or changing fill;
- adjusting stroke or internal line treatment;
- minor path cleanup;
- minor simplification or correction required for the banknote composition.

If a tweak is made, the package must keep:

- the original provided SVG;
- the edited SVG actually used in the build;
- a short note in `generation-record.yaml` or `README.md` describing the tweak.

After the edited SVG is approved, it becomes the frozen shared map asset and is reused throughout the series.

### 5.5 Other reusable assets

The package may also contain reusable assets for:

- signature placeholder;
- serial placeholder;
- a common paper texture;
- a common grain or print overlay;
- shared tactile-mark placeholder shapes if they are used visually;
- denomination border or frame helper geometry, if deterministic and reused.

Only include these if they are actually used.

## 6. Generated components

Generation should be limited to the components that genuinely need it.

### 6.1 Scene plates

A scene plate is the main image layer for a given side.

One scene plate is generated for each of the twelve notes:

- six rectos;
- six versos.

These are the main variable images of the series.

They should be stored as raster PNGs at the final note size or larger in the same aspect ratio. If generated larger, the deterministic build script handles scaling and placement.

### 6.2 Empty ore-label plates

Generate one ore-label plate per recto denomination.

This plate contains:

- the label shape;
- the pale field;
- internal denomination-specific decoration;
- edge treatment.

It must remain empty in the centre.
The ore block itself is inserted separately as a reusable asset.

Store these as transparent full-canvas PNGs positioned exactly where they belong in the final recto.

### 6.3 Frame and ornament plates

Generate one frame plate per note side where required.

The frame plate may contain:

- border structures;
- decorative bands;
- background printed details;
- static note ornament;
- any areas intended to sit above the scene.

It must not contain reusable institutional assets that are better handled separately, such as:

- ore block raster;
- EU flag;
- Europe map;
- EURO / ΕΥΡΩ / ЕВРО lettering;
- denomination numerals if these are created deterministically.

Store frame plates as full-canvas transparent PNGs at final note size.

### 6.4 Optional generated tweaks

If a scene or frame requires a non-destructive local repair, keep the corrected version and the source version.

Do not overcomplicate this with large archival overhead. A simple pattern such as:

- `EUR020_verso_scene_source.png`
- `EUR020_verso_scene_final.png`

is sufficient.

## 7. Scene-generation rules

The package workflow must explicitly preserve a consistent visual grammar across the twelve scene plates.

### 7.1 Shared style requirements

All scene plates should maintain broadly the same:

- level of detail;
- edge behaviour;
- texture sharpness;
- rendering language;
- degree of Minecraft fidelity;
- saturation restraint;
- sense of material continuity.

The model must not let one denomination become smooth, painterly, heavily engraved, or block-softened while another resembles a crisp Minecraft screenshot.

### 7.2 Minecraft fidelity

Recto and verso scenes should remain recognisably Minecraft.

Required qualities include:

- canonical or near-canonical block textures;
- recognisable terrain behaviour;
- recognisable objects and workstations;
- recognisable visual scale;
- no heavy universal outlines around every block;
- no drift into generic voxel fantasy.

### 7.3 Recto scene rule

Recto scenes should generally aim for the visual directness of a carefully selected Minecraft view.

If the note frame is hidden, the central image should still read as Minecraft, not as generic cubic concept art.

### 7.4 Verso scene rule

Verso scenes may be denser and more constructed, but they should still be built from recognisable Minecraft objects, architecture, terrain, and mechanics.

The scene must not try to solve the concept by inventing a block-fantasy city that only vaguely resembles the game.

### 7.5 Exclusions for scene generation

Do not generate scene plates with:

- the EU flag;
- the Europe map;
- ore label field;
- ore block inset;
- final denomination text;
- pseudo-lettering;
- UI elements;
- game logo;
- inventory bar;
- crosshair;
- decorative recipe strips;
- explanatory arrows.

These belong either to the reusable asset system or are excluded entirely.

## 8. Structural composition model

Final notes are assembled from a small number of full-canvas layers.

The minimal intended layer family is:

1. scene plate;
2. ore-label plate, recto only;
3. ore block asset, recto only;
4. frame / ornament plate;
5. value typography assets;
6. EURO / ΕΥΡΩ / ЕВРО asset;
7. EU flag asset;
8. Europe map asset;
9. optional signature or other institutional placeholders.

Every layer used in final composition should be available either as:

- SVG for vector assets, or
- transparent PNG for raster assets.

For ease of deterministic composition, the build pipeline should generate full-canvas positioned PNG versions of the vector assets before flattening, even if the master asset remains SVG.

This gives two useful forms:

- compact reusable master asset;
- full-canvas placed layer preview.

The full-canvas placed versions are useful both for verification and for easy import into Paint.NET or another editor if manual adjustment is ever required.

## 9. Centralized layout specification

The exact positions of stable elements belong here, not scattered across the whole proposal.

Generated plates may remain visually unconstrained internally, but fixed note elements should be placed by documented coordinates.

### 9.1 Layout source of truth

Use a single `layout.yaml` as the authoritative layout file.

It should define, for each note side:

- output width and height;
- scene placement transform;
- ore-label placement, recto only;
- ore-block placement, recto only;
- numeral placement;
- EURO / ΕΥΡΩ / ЕВРО placement;
- EU flag placement;
- Europe map placement;
- any repeated secondary institution fields;
- z-order.

### 9.2 Coordinate model

Use pixel coordinates derived from the final output size.

A simple format is sufficient:

- top-left `x`, `y` coordinates;
- width and height for boxes;
- centre and size for circular or square insertions;
- optional scale and offset for generated scene plates.

Where a common proportional rule exists, it may be expressed once and converted to pixels by script.

### 9.3 Required fixed placements

At minimum, the layout specification should centrally control:

- ore-label position and size;
- ore-block position and size inside the label;
- main numeral position and scale;
- secondary value placement if present;
- EU flag box;
- EURO / ΕΥΡΩ / ЕВРО field;
- Europe map box;
- signature or placeholder area;
- final frame alignment.

### 9.4 Scene placement

Scene plates are the one place where some flexibility is useful.

For each side, the layout may define:

- target scene box;
- fit mode, usually `cover`;
- optional scale factor;
- optional `offset_x` and `offset_y`.

This keeps the final layout deterministic while allowing small corrections if a generated scene needs a slight repositioning.

### 9.5 Recommended structural rule

The note skeleton should be deterministic.
The scene content may remain generative.

That division is the core logic of the package.

## 10. Typography workflow

Typography must be deterministic and reusable.

### 10.1 Source

The provided Minecraft TTF is the source.

### 10.2 Derived assets

Use `build_type_assets.py` to generate:

- outlined SVG numerals;
- outlined SVG euro sign;
- outlined SVG `EURO`;
- outlined SVG `ΕΥΡΩ`;
- outlined SVG `ЕВРО`;
- optional transparent PNG previews of each asset.

### 10.3 Final use

The build script inserts the derived assets into each note according to `layout.yaml`.

Do not rely on text rendering during final composition.
Do not assume the font is installed externally.

## 11. Composition scripts

The package should include a small Python toolchain.

### 11.1 `build_type_assets.py`

Purpose:

- read the provided TTF;
- generate outlined SVG lettering and numerals;
- generate PNG previews if desired.

### 11.2 `build_notes.py`

Purpose:

- read `layout.yaml` and `palette.yaml`;
- place all layers for each note side;
- apply deterministic scaling and positioning;
- rasterize vector assets if needed;
- flatten the final note PNGs;
- optionally export full-canvas layer previews for inspection.

### 11.3 `build_contact_sheets.py`

Purpose:

- generate overview sheets for fast review;
- optionally build recto, verso, paired, and grayscale contact sheets.

### 11.4 Optional layer-preview export

The composition script may expose an option such as:

- export final flattened notes only;
- export flattened notes plus placed full-canvas layer previews.

This is useful for manual inspection and optional editing, but it should not become a mandatory bloated archive.

## 12. YAML files

Use YAML for the small amount of structured project data.

### 12.1 `layout.yaml`

Stores note-by-note geometry and layer placement.

### 12.2 `palette.yaml`

Stores denomination colour values if the build script applies any deterministic recolour or overlay treatment.

This can remain simple. If colour is handled mainly in the generated plates, the palette file may only define shared UI or decorative asset colours.

### 12.3 `generation-record.yaml`

Stores a lightweight record of:

- which generated plate was selected for each note side;
- whether the Europe map SVG was tweaked;
- whether a scene source was replaced by a corrected version;
- any notable manual approval decision.

This is documentation, not bureaucracy.

## 13. Construction procedure

The package must include a reproducible step-by-step build sequence.

### 13.1 Prepare shared assets

1. Place the provided TTF, ore rasters, EU flag SVG, and Europe map SVG in the `assets/` tree.
2. If the Europe map is tweaked, save the revised version as a separate approved file.
3. Run `build_type_assets.py` to generate the deterministic typography assets.

### 13.2 Prepare generated intermediates

1. Generate the twelve scene plates.
2. Generate the six empty recto ore-label plates.
3. Generate the required frame / ornament plates.
4. Review them for consistency and freeze the approved versions.

### 13.3 Configure layout

1. Populate `layout.yaml` with the exact note sizes.
2. Set the fixed placements for all stable layers.
3. Set any scene placement offsets.

### 13.4 Build notes

1. Run `build_notes.py`.
2. The script rasterizes placed vector assets as needed.
3. The script composites all layers in the specified order.
4. The script exports the final flattened note PNGs.
5. If enabled, the script also exports placed full-canvas layer previews.

### 13.5 Build contact sheets

1. Run `build_contact_sheets.py`.
2. Export at least one full-series overview.

## 14. Layer order for deterministic flattening

A typical flattening order is:

1. scene plate;
2. ore-label plate, recto only;
3. ore block, recto only;
4. frame / ornament plate;
5. main numeral;
6. secondary denomination text if used;
7. EURO / ΕΥΡΩ / ЕВРО;
8. EU flag;
9. Europe map;
10. signature or placeholder elements;
11. optional common paper or print overlay if this is handled separately.

The exact order may be adjusted, but it must be fixed and documented.

## 15. Full-canvas support

The workflow must support full-canvas placed layer exports.

This does not mean every master asset must be stored only as a full-canvas file. The useful distinction is:

- master asset: compact reusable source, such as SVG or cropped PNG;
- placed layer export: full-canvas transparent PNG at final note size.

For example:

- `assets/maps/europe_map_master.svg`
- `outputs/layer_previews/EUR020_recto_map.png`

The first is reusable.
The second is a placed preview for verification and optional manual work.

This approach gives the convenience of editor-ready layer files without bloating the core asset system.

## 16. Final exports

At minimum, export:

- the twelve final note PNGs at the exact sizes listed in Section 1;
- one recto contact sheet;
- one verso contact sheet;
- one paired contact sheet or another overall review sheet.

Optional useful exports include:

- grayscale contact sheet;
- full-canvas layer previews for each note side.

Do not require TIFFs, PDFs, archive nesting, or oversized review files unless they are specifically needed.

## 17. Quality control

### 17.1 Structural checks

Confirm that:

- every final file matches the exact target size;
- all fixed elements follow `layout.yaml`;
- ore-label position and scale are consistent;
- ore-block scale is consistent;
- EU flag placement is consistent;
- Europe map placement is consistent;
- typography is stable and not regenerated per note.

### 17.2 Scene checks

Confirm that:

- all scene plates belong to one visual family;
- block textures remain recognisably Minecraft;
- rectos preserve screenshot-like directness where intended;
- versos remain Minecraft-native rather than generic voxel fantasy;
- saturation remains controlled;
- no scene contains accidental pseudo-text, UI, or excluded overlays.

### 17.3 Reusability checks

Confirm that:

- ore blocks come from the provided assets;
- the EU flag is reused rather than redrawn;
- the Europe map is reused from the approved source;
- typography comes from derived font assets rather than image generation;
- changing one swappable component and rerunning the script updates the finished note without manual reconstruction.

## 18. Intended editing model

This package is designed so that a change to one component does not require rebuilding the whole note by hand.

Examples:

- replace one scene plate, rerun the script, get the updated note;
- adjust the ore-label position in `layout.yaml`, rerun the script, update all rectos;
- tweak the map SVG once, rerun the script, update all notes that use it;
- refine the numeral SVGs, rerun the script, update all notes.

That is the practical measure of success.

## 19. What this workflow deliberately avoids

This package deliberately avoids:

- fake print-production complexity;
- giant flattened duplicates of every possible variant;
- CSV manifests and checksum bureaucracy;
- archives within archives;
- unstable AI-generated text;
- re-generating assets that should be reused;
- forcing the image model to solve layout over and over again;
- treating every decorative decision as a separate professional pipeline.

The goal is not to simulate a central-bank production archive.
The goal is to create a clean, swappable, reproducible design kit that builds the final fictional notes deterministically.

## 20. Minimum final package checklist

Before delivery, confirm that the package includes:

- documentation in Markdown;
- Python build scripts;
- `layout.yaml`;
- provided ore rasters;
- provided TTF;
- provided EU flag SVG;
- original and approved Europe map SVG if edited;
- generated scene plates;
- generated ore-label plates;
- generated frame plates;
- derived typography assets;
- the twelve final flattened note PNGs;
- at least one contact sheet.

If the recipient can open the package, inspect the assets, run the scripts, and immediately view the final notes without reconstructing them manually, the package has succeeded.
