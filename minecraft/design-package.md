# Reproducible layered design package

## Purpose

This document defines the workflow for building the final twelve banknote images from a small set of reusable assets, generated intermediates, and deterministic composition rules.

The aim is not to simulate a central-bank production archive.
The aim is to create a self-contained design kit that:

- keeps generated elements swappable;
- reuses stable assets instead of regenerating them;
- assembles finished notes deterministically;
- exports the final flattened note PNGs directly;
- provides enough documentation and scripts to rebuild the notes without manual reconstruction.

The proposal defines meaning and art direction.
This file defines package contents, reusable inputs, generated intermediates, layout control, layer order, composition scripts, and final exports.

## Core principles

1. Generate only what benefits from generation.

   AI should generate the main scene plates and selected denomination-specific ornament plates. It should not repeatedly redraw stable institutional assets.

2. Reuse what can be reused.

   Ore blocks, numerals, euro scripts, the EU flag, the Europe map, and other stable elements should exist as assets and be reused across builds.

3. Keep the note skeleton deterministic.

   Stable elements such as numerals, euro scripts, badge placement, map placement, and flag placement should be controlled by layout data and composition scripts.

4. Preserve denomination-specific richness.

   The series shares a common structure, but each denomination should retain its own border language, badge treatment, local texture rhythm, and ornament identity. Shared structure does not mean recolored sameness.

5. Keep the scene visually primary.

   The main scene remains the heart of the note. Ornament, side fields, and institutional elements support it rather than suppressing it.

6. Use Markdown and YAML.

   Documentation belongs in Markdown. Structured project data belongs in YAML. Avoid decorative machinery such as CSV manifests or excessive archival overhead.

## 1. Authoritative final output sizes

The final note exports use the following exact canvas sizes.

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

These canvas sizes are authoritative.
No outer presentation margin, skew, photographed-paper context, or mockup background belongs in the final note files.

## 2. Deliverable contents

The final package must contain:

- `design-package.md`;
- the current proposal file used as conceptual reference;
- `README.md` with a short usage summary;
- Python scripts used for construction;
- YAML files used by the scripts;
- all provided inputs;
- all generated intermediates actually used in the final build;
- the final flattened note PNGs;
- at least one contact sheet.

The package should be directly inspectable and directly runnable.
A reviewer should not need to reconstruct the notes manually in Paint.NET or another editor just to see the finished result.

## 3. Package structure

A recommended package tree is:

- `README.md`
- `design-package.md`
- `layout.yaml`
- `generation-record.yaml`
- `scripts/`
  - `build_type_assets.py`
  - `build_notes.py`
  - `build_contact_sheets.py`
- `assets/`
  - `font/`
  - `ore_blocks/`
  - `flags/`
  - `maps/`
  - `type_svg/`
  - `type_png/`
  - `placeholders/`
  - `masks/`
- `generated/`
  - `scenes/`
  - `ornaments/`
  - `badges/`
  - `map_tweaks/`
- `outputs/`
  - `notes/`
  - `contacts/`
  - `layer_previews/`
- `docs/`

The exact tree may vary, but the distinction between assets, generated intermediates, scripts, layout data, and finished outputs must remain clear.

## 4. Naming convention

Use a single naming system throughout.

Recommended patterns:

- `EUR005_recto_scene.png`
- `EUR005_recto_ornament.png`
- `EUR005_recto_badge.png`
- `EUR005_recto_final.png`
- `EUR005_recto_scene_mask.svg`
- `EUR005_recto_layers.png` only if a full-canvas preview is exported
- `ore_coal_iso.png`
- `eu_flag_master.svg`
- `europe_map_master.svg`
- `europe_map_project.svg`
- `euro_scripts_master.svg`
- `value_005_master.svg`

Use `recto` and `verso` in file names rather than abbreviations.

## 5. Inputs and reusable assets

The following inputs are provided and become part of the package.

### 5.1 Isometric ore rasters

The provided isometric ore rasters are authoritative reusable assets.
Use one raster file for each denomination motif:

- coal ore;
- redstone ore;
- lapis ore;
- copper ore;
- emerald ore;
- gold ore.

These are inserted into the badge field.
They are not regenerated as part of note construction.

If a small display adjustment is needed for paper integration, create a derived project copy and freeze it as the approved ore asset.
Do not ask the model to reinterpret the ore cube.

### 5.2 Minecraft typeface

The provided TTF file is a source input, not a runtime dependency.

Use it to generate deterministic typography assets through Python.
Do not rely on live SVG text elements that assume the font is installed on the viewer’s system.

Recommended method:

1. read the TTF in `build_type_assets.py`;
2. generate the required strings and numerals;
3. convert them to outlined SVG assets;
4. optionally produce matching transparent PNG previews.

The final build should use the derived outlined SVG assets, or their controlled rasterized equivalents, not live text rendering.

Required type assets include:

- `EURO`;
- `ΕΥΡΩ`;
- `ЕВРО`;
- `5`, `10`, `20`, `50`, `100`, `200`;
- `€`;
- any repeated secondary denomination strings used in the chosen layout.

### 5.3 Grouped euro-script asset

The three euro scripts should exist as one grouped reusable asset as well as separate source assets if useful.

The grouped asset should define a single stack with matched size, matched optical weight, and matched spacing logic.

This avoids uneven results such as `EURO` appearing smaller than the two lines below.

### 5.4 EU flag SVG

The provided EU flag SVG is a stable reusable asset.

Do not regenerate it.
Do not redraw the stars.
Do not replace it with an AI-painted rectangle.

If tonal or texture integration is applied, document it and keep it consistent.

### 5.5 Europe map SVG

The provided Europe map SVG is a reusable asset.
The model may tweak it if necessary.

Permitted tweaks include:

- adding or changing fill;
- adjusting stroke or line treatment;
- minor path cleanup;
- minor shape correction if needed for the composition.

If a tweak is made, keep:

- the original provided SVG;
- the edited SVG actually used in the build;
- a short note in `generation-record.yaml`.

Once approved, the edited SVG becomes the shared project map and should be reused consistently.

### 5.6 Optional shared assets

If used, the package may also include:

- signature placeholder;
- serial placeholder;
- a common paper texture;
- a common print-grain overlay;
- full-note masks or aperture masks;
- helper geometry for deterministic placement.

Only include these if they are actually part of the build.

## 6. Useful atomic elements

The workflow should decompose the notes into actually useful swappable elements.

The preferred atomic elements are:

- scene plate;
- denomination-specific ornament plate;
- denomination-specific empty badge plate, recto only;
- ore block asset, recto only;
- numeral asset;
- grouped euro-script asset;
- EU flag asset;
- Europe map asset;
- optional placeholder assets;
- deterministic layout and mask data.

Avoid decomposing the note into fake micro-layers that add complexity without practical editing value.

## 7. Generated components

Generation should be limited to the elements that benefit from it.

### 7.1 Scene plates

Generate one scene plate for each note side.
There are twelve scene plates in total:

- six rectos;
- six versos.

These are the main variable images of the series.

They may be generated at final size or larger in the same aspect ratio.
If generated larger, the build script handles scaling and placement.

### 7.2 Denomination-specific badge plates

Generate one empty badge plate for each recto denomination.
There are six badge plates in total.

Each badge plate contains:

- the badge shape;
- the pale field;
- denomination-specific internal pattern or texture;
- ring detailing;
- edge treatment.

The centre remains empty.
The ore block is inserted separately.

Keep fixed across the six badges:

- overall size category;
- placement logic;
- relation between badge size and ore-block size;
- role as the recto identifier field.

Allow to vary by denomination:

- border rhythm;
- internal pattern;
- ring language;
- local texture logic;
- visual motif tied to the material.

The six badges should not be a single base badge merely recolored.

### 7.3 Denomination-specific ornament plates

Generate ornament plates that carry the note’s decorative richness.

Do not generate one universal frame and recolor it.
The correct rule is:

- shared structural skeleton;
- denomination-specific ornament.

An ornament plate may contain:

- border systems;
- side-field textures;
- local decorative bands;
- field transitions;
- aperture surround treatment;
- note-surface details that sit above or around the scene.

It must not contain stable reusable assets better handled elsewhere, such as:

- ore block raster;
- EU flag;
- Europe map;
- grouped euro scripts;
- numerals, if these are built deterministically.

### 7.4 Recommended ornament subtypes

To reduce ambiguity, do not describe the whole note shell to the model simply as “the frame.”
That wording is too open and tends to create visible scaffolding.

When useful, think in the following subtypes:

- border / ornament plate;
- left value-field background plate;
- right institutional-field background plate;
- optional aperture-surround treatment.

These may be generated together or separately, but the prompt should make their role explicit.

### 7.5 Local repairs

If a generated component needs a small non-destructive repair, keep both the source and approved project version.

A simple naming pattern is sufficient:

- `EUR020_verso_ornament_source.png`
- `EUR020_verso_ornament_final.png`

## 8. Reserved zones and deterministic masks

Stable note elements should occupy reserved zones.
Generated ornament should not paint freely across them.

At minimum, define reserved zones for:

- ore badge, recto only;
- grouped euro-script field;
- EU flag field;
- Europe map field;
- signature or placeholder field;
- any fixed denomination field that should remain clear.

These reserved zones should be defined in `layout.yaml` and, where useful, by mask assets in `assets/masks/`.

This avoids failures such as:

- ornament or border crossing through the badge;
- the map being crowded or clipped;
- script fields becoming inconsistent;
- decorative structure behaving like visible template guides.

## 9. Scene-generation rules

The package workflow must explicitly preserve a consistent visual grammar across the twelve scene plates.

### 9.1 Shared style requirements

All scene plates should maintain broadly the same:

- level of detail;
- edge behaviour;
- texture crispness;
- rendering language;
- degree of Minecraft fidelity;
- saturation restraint;
- material continuity.

The model must not let one denomination become smooth or painterly while another resembles a crisp Minecraft render.

### 9.2 Minecraft fidelity

Recto and verso scenes should remain recognisably Minecraft.
Required qualities include:

- canonical or near-canonical block textures;
- recognisable terrain behaviour;
- recognisable objects and workstations;
- recognisable visual scale;
- no heavy universal outlines around every block;
- no drift into generic voxel fantasy.

### 9.3 Recto scene rule

Recto scenes should generally aim for the directness of a carefully selected Minecraft view.
If the note shell is hidden, the image should still read as Minecraft rather than generic cubic concept art.

### 9.4 Verso scene rule

Verso scenes may be denser and more constructed, but they should still be built from recognisable Minecraft objects, architecture, terrain, and mechanics.

The scene must not solve the concept by inventing a block-fantasy city that only vaguely resembles Minecraft.

### 9.5 Reference-based consistency

When the workflow supports it, use the strongest one-pass notes as visual references for package generation.

Use them not as compositions to copy, but as references for:

- decorative density;
- frame richness;
- field texture;
- the relation between scene and ornament;
- overall seriousness.

This is especially useful when generating ornament plates.
The objective is to preserve the richness seen in strong one-pass notes while still producing clean modular components.

### 9.6 Scene exclusions

Do not generate scene plates with:

- the EU flag;
- the Europe map;
- the badge field;
- the ore block inset;
- final denomination lettering;
- pseudo-text;
- UI elements;
- inventory bar;
- crosshair;
- recipe strips;
- explanatory arrows.

These belong either to reusable assets or are excluded altogether.

## 10. Ornament-generation rules

This section addresses the main failure mode seen in earlier package attempts: thin generic overlays and visible template scaffolding.

### 10.1 Ornament purpose

Ornament should provide note richness, density, and local identity.
It should not behave like a visible layout template.

### 10.2 Ornament requirements

Ornament generation should aim for:

- density comparable to the stronger one-pass notes;
- denomination-specific border logic;
- denomination-specific local texture and rhythm;
- convincing integration with the scene;
- quiet but detailed side fields;
- clear termination around reserved zones.

### 10.3 Ornament exclusions

Do not generate:

- notebook-like horizontal rules;
- placeholder panel lines;
- template scaffolding;
- guide lines;
- abstract wireframe frames;
- visible design-grid artifacts;
- generic blank panels pretending to be note structure.

### 10.4 Ornament relationship to the scene

The scene remains visually primary.
The ornament plate should enrich the note without flattening or overpowering the central image.

## 11. Structural composition model

Final notes are assembled from a small number of full-canvas layers.

The normal layer family is:

1. scene plate;
2. badge plate, recto only;
3. ore block asset, recto only;
4. ornament plate;
5. numeral asset;
6. secondary denomination asset if used;
7. grouped euro-script asset;
8. EU flag asset;
9. Europe map asset;
10. signature or placeholder assets;
11. optional paper or print overlay if handled separately.

Every layer used in the final build should be available either as:

- SVG for vector assets, or
- transparent PNG for raster assets.

For convenience, the build pipeline may also export full-canvas positioned PNG versions of placed vector assets.

## 12. Centralized layout specification

All stable placements belong in one centralized section of the workflow and in one YAML source of truth.
They should not be scattered through scene prompts.

### 12.1 Layout source of truth

Use a single `layout.yaml` file to define, for each note side:

- output width and height;
- scene placement box and any offset;
- badge placement and size, recto only;
- ore-block placement and size, recto only;
- main numeral placement and size;
- grouped euro-script placement;
- EU flag placement;
- Europe map placement;
- placeholder or signature placement;
- z-order;
- any mask assignments.

### 12.2 Coordinate model

Use pixel coordinates derived from the final output size.
A simple structure is sufficient:

- top-left `x`, `y`;
- `width`, `height` for rectangles;
- `cx`, `cy`, `diameter` or `size` for circular or square insertions;
- optional scale and offset for scene placement.

### 12.3 Hard-controlled stable placements

At minimum, hard-control the following:

- badge placement and size;
- ore-block placement and size inside the badge;
- main numeral placement and scale;
- grouped euro-script placement;
- EU flag placement;
- Europe map placement;
- signature or placeholder placement;
- ornament alignment;
- any masks that clear reserved zones.

### 12.4 Scene placement

Scene plates are the one place where a small amount of placement flexibility remains useful.
For each note side, the layout may define:

- target scene box;
- fit mode, usually `cover`;
- optional scale factor;
- optional `offset_x` and `offset_y`.

This keeps the layout deterministic while allowing small corrections if a generated scene needs slight repositioning.

### 12.5 Right-field guidance

The right institutional field must not be undersized or visually weak.
At minimum:

- the Europe map should occupy a clearly legible lower-right field;
- the grouped euro-script asset should have consistent size and weight across notes;
- the EU flag should sit within a stable field of its own;
- these elements should feel integrated into the note rather than pasted on top.

## 13. Typography workflow

Typography must be deterministic and reusable.

### 13.1 Source

The provided Minecraft TTF is the source.

### 13.2 Derived assets

Use `build_type_assets.py` to generate:

- outlined SVG numerals;
- outlined SVG euro sign;
- outlined SVG `EURO`;
- outlined SVG `ΕΥΡΩ`;
- outlined SVG `ЕВРО`;
- the grouped euro-script stack asset;
- optional PNG previews.

### 13.3 Final use

The build script inserts these assets according to `layout.yaml`.
Do not rely on live text rendering during final composition.

## 14. Python scripts

The package should include a small Python toolchain.

### 14.1 `build_type_assets.py`

Purpose:

- read the provided TTF;
- generate outlined SVG lettering and numerals;
- generate preview PNGs if desired.

### 14.2 `build_notes.py`

Purpose:

- read `layout.yaml` and `generation-record.yaml`;
- rasterize vector assets as needed;
- place all layers for each note side;
- apply deterministic scaling, masking, and placement;
- flatten the final note PNGs;
- optionally export full-canvas layer previews.

### 14.3 `build_contact_sheets.py`

Purpose:

- generate overview sheets for review;
- optionally build recto, verso, paired, and grayscale contact sheets.

## 15. YAML files

Use YAML for the project’s small amount of structured data.

### 15.1 `layout.yaml`

Stores note-by-note geometry, layer placement, masks, and z-order.

### 15.2 `generation-record.yaml`

Stores a lightweight record of:

- which generated components were approved for each note side;
- whether the Europe map SVG was adjusted;
- whether a source component was replaced by a corrected project copy;
- any manual approval notes worth preserving.

This is documentation, not bureaucracy.

## 16. Construction procedure

The package must contain a reproducible build sequence.

### 16.1 Prepare shared inputs

1. Place the provided TTF, ore rasters, EU flag SVG, and Europe map SVG in `assets/`.
2. If the map is adjusted, save the approved project map as a separate file.
3. Run `build_type_assets.py` to generate typography assets.

### 16.2 Prepare generated intermediates

1. Generate the twelve scene plates.
2. Generate the six denomination-specific empty badge plates.
3. Generate the denomination-specific ornament plates.
4. Review them for consistency, richness, and correct use of reserved zones.
5. Freeze the approved files.

### 16.3 Configure layout

1. Populate `layout.yaml` with the exact output sizes.
2. Define all stable placements.
3. Define reserved zones and masks.
4. Define any scene-placement offsets.

### 16.4 Build the notes

1. Run `build_notes.py`.
2. The script places all layers in the documented order.
3. The script applies masking and deterministic placement.
4. The script exports the final flattened note PNGs.
5. If enabled, the script also exports full-canvas layer previews.

### 16.5 Build contact sheets

1. Run `build_contact_sheets.py`.
2. Export at least one whole-series overview.

## 17. Layer order for flattening

A standard flattening order is:

1. scene plate;
2. badge plate, recto only;
3. ore block, recto only;
4. ornament plate;
5. main numeral;
6. secondary denomination asset if used;
7. grouped euro-script asset;
8. EU flag;
9. Europe map;
10. signature or placeholder assets;
11. optional paper or print overlay.

The exact order may be adjusted, but it must be fixed and documented.

## 18. Full-canvas support

The workflow must support full-canvas placed layer exports.
This does not mean every master asset must exist only as a full-canvas file.

Use two complementary forms:

- master asset: compact reusable source, such as SVG or cropped PNG;
- placed layer export: full-canvas transparent PNG at final note size.

For example:

- `assets/maps/europe_map_project.svg`
- `outputs/layer_previews/EUR020_recto_map.png`

The first is the reusable source.
The second is the placed preview.

This makes the package editor-friendly without bloating the core asset system.

## 19. Final exports

At minimum, export:

- the twelve final note PNGs at the exact sizes listed in Section 1;
- one recto contact sheet;
- one verso contact sheet;
- one paired or all-series review sheet.

Optional useful exports include:

- grayscale contact sheets;
- full-canvas layer previews for each note side.

Do not require TIFFs, PDFs, nested archives, or oversized review bundles unless they are specifically needed.

## 20. Quality control

### 20.1 Structural checks

Confirm that:

- every final file matches the exact target size;
- all stable elements follow `layout.yaml`;
- badge placement and scale are consistent;
- ore-block scale is consistent;
- the grouped euro-script block is visually uniform;
- the Europe map is large enough and consistently placed;
- ornament does not cross the badge or other reserved zones;
- typography is not being regenerated per note.

### 20.2 Visual checks

Confirm that:

- all scene plates belong to one visual family;
- rectos preserve the desired screenshot-like directness where intended;
- versos remain Minecraft-native rather than generic voxel fantasy;
- ornament density remains rich enough;
- denomination-specific identity is preserved;
- the scene remains visually primary.

### 20.3 Reusability checks

Confirm that:

- ore cubes come from the provided assets;
- the EU flag is reused rather than redrawn;
- the Europe map comes from the approved shared source;
- typography comes from derived font assets rather than image generation;
- changing one swappable element and rerunning the script updates the finished note without manual reconstruction.

## 21. Intended editing model

This workflow is designed so that a change to one component does not require rebuilding the whole note by hand.

Examples:

- replace one scene plate, rerun the script, and get the updated note;
- replace one ornament plate, rerun the script, and compare results immediately;
- change badge placement in `layout.yaml`, rerun the script, and update all relevant rectos;
- adjust the grouped euro-script asset once, rerun the script, and update all notes;
- adjust the Europe map SVG once, rerun the script, and update all notes that use it.

That is the practical measure of success.

## 22. What this workflow avoids

This workflow deliberately avoids:

- one universal ornament template recolored across the whole series;
- visible layout guides or scaffold-like frame generation;
- fake print-production complexity;
- redundant oversized duplicates;
- CSV manifests and checksum bureaucracy;
- unstable AI-generated text;
- re-generating stable assets;
- asking the model to rediscover the note layout every time;
- decomposing the note into many tiny layers that provide little editing value.

The objective is a clean, swappable, reproducible package that preserves the visual richness of the best note renders while keeping the final build deterministic.

## 23. Minimum package checklist

Before delivery, confirm that the package includes:

- `design-package.md`;
- the proposal file used for the series;
- `README.md`;
- Python build scripts;
- `layout.yaml`;
- `generation-record.yaml`;
- provided ore rasters;
- provided TTF;
- provided EU flag SVG;
- original and approved project Europe map SVG, if adjusted;
- generated scene plates;
- generated denomination-specific badge plates;
- generated denomination-specific ornament plates;
- derived typography assets;
- the twelve final flattened note PNGs;
- at least one contact sheet.

If a reviewer can open the package, inspect the assets, run the scripts, and view the finished notes immediately without manual reconstruction, the package has succeeded.
