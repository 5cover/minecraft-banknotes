# Reproducible layered design package

## Purpose

This document defines the workflow for building the final twelve banknote images from specialized generated layers, reusable assets, and deterministic composition rules.

The aim is not to simulate a central-bank production archive.
The aim is to create a self-contained design kit that:

- keeps the main generated components swappable;
- gives each generated component a specialized visual task;
- preserves visual coherence through ordered, context-aware generation;
- reuses stable assets instead of regenerating them;
- assembles finished notes deterministically;
- exports the final flattened note PNGs directly;
- preserves the intermediates and documentation required to reproduce the build.

The proposal defines meaning and art direction.
This file defines package contents, generation order, reusable inputs, generated intermediates, layout control, layer order, Python construction, and final exports.

## Core principles

1. Separation is technical, not aesthetic.

   A layer is separated so it can be replaced, cropped, repositioned, and recomposed. Separation does not imply visual simplicity, generic geometry, low detail, or independence from the rest of the note.

2. Specialize generation by responsibility.

   The environmental scene and the monetary artwork solve different visual problems and should be generated separately.

   The scene generator concentrates on Minecraft fidelity, spatial coherence, terrain or architecture, lighting, texture, and environmental detail.

   The monetary-artwork generator concentrates on banknote richness, border logic, field transitions, denomination identity, empty ore-badge design, quiet zones, and integration with the approved scene.

3. Preserve holistic awareness through ordered generation.

   Generated layers are isolated in output but designed in context. A downstream layer should see the approved upstream layers and layout proxies it must visually respond to.

4. Merge layers when their visual dependency is genuinely mutual.

   Ornament and the empty ore badge are one monetary-artwork responsibility. They are generated together so their line language, density, geometry, and local transitions belong to the same note.

   The canonical ore block remains separate.

5. Reuse everything that can be an asset.

   Ore blocks, numerals, euro scripts, the EU flag, the Europe map, and other stable elements should exist as assets and be reused across builds.

6. Keep the note skeleton deterministic.

   Stable placement, cropping, masks, asset scale, z-order, and final canvas dimensions are controlled by YAML and Python rather than rediscovered by the image model.

7. Preserve denomination-specific richness.

   The series shares a structural grammar, not one recolored decorative template. Each denomination may have its own border rhythm, badge geometry, field texture, visual density, and ornament language.

8. Keep the scene visually primary.

   Monetary artwork should make the scene feel like part of a banknote, not bury it beneath a visible template.

9. Use Markdown and YAML.

   Documentation belongs in Markdown. Structured project data belongs in YAML. Avoid unnecessary manifests, archive bureaucracy, and redundant production artifacts.

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

No outer presentation margin, photographed-paper context, mockup background, skew, rotation, or drop shadow belongs in the final note files.

## 2. Deliverable contents

The final package must contain:

- `design-package.md`;
- the current proposal file used as conceptual reference;
- `README.md` with a short build summary;
- Python scripts used for construction;
- YAML files used by the scripts;
- all provided inputs;
- the approved generated scene plates;
- the approved generated monetary artwork plates;
- the contextual generation composites required to reproduce those artwork plates;
- any edited project copy of the Europe map;
- derived typography assets;
- the final flattened note PNGs;
- at least one contact sheet.

The package should be directly inspectable and directly runnable.
A reviewer should not need to reconstruct the notes manually in Paint.NET or another editor simply to see the final result.

## 3. Package structure

A recommended package tree is:

- `README.md`
- `design-package.md`
- `layout.yaml`
- `generation-record.yaml`
- `scripts/`
  - `build_type_assets.py`
  - `build_contexts.py`
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
  - `artwork/`
  - `contexts/`
- `outputs/`
  - `notes/`
  - `contacts/`
  - `layer_previews/`
- `docs/`

The exact tree may vary, but the distinction between reusable assets, generated scene plates, generated monetary artwork, contextual generation references, scripts, layout data, and finished outputs must remain clear.

## 4. Naming convention

Use a single naming system throughout.

Recommended patterns:

- `EUR005_recto_scene_source.png`
- `EUR005_recto_scene_final.png`
- `EUR005_recto_context.png`
- `EUR005_recto_artwork_source.png`
- `EUR005_recto_artwork_final.png`
- `EUR005_recto_final.png`
- `EUR005_recto_scene_mask.svg`
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
Use one raster for each denomination motif:

- coal ore;
- redstone ore;
- lapis ore;
- copper ore;
- emerald ore;
- gold ore.

These are inserted into the empty ore badge after monetary artwork generation.
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
3. convert the glyphs to outlined SVG paths;
4. optionally produce matching transparent PNG previews.

The final build should use the derived outlined SVG assets, or their controlled rasterized equivalents, not live font rendering.

Required type assets include:

- `EURO`;
- `ΕΥΡΩ`;
- `ЕВРО`;
- `5`, `10`, `20`, `50`, `100`, `200`;
- `€`;
- any repeated secondary denomination strings used in the chosen layout.

### 5.3 Grouped euro-script asset

The three euro scripts should exist as one grouped reusable asset as well as separate source assets if useful.

The grouped asset defines:

- matched optical size;
- matched line weight;
- consistent line spacing;
- fixed ordering;
- a common overall bounding box.

`EURO` must not appear smaller merely because its Latin glyphs occupy less visual area than the Greek or Cyrillic lines.

### 5.4 EU flag SVG

The provided EU flag SVG is a stable reusable asset.

Do not regenerate it.
Do not redraw the stars.
Do not replace it with an AI-painted approximation.

If tonal or texture integration is applied, keep the geometry intact and document the treatment.

### 5.5 Europe map SVG

The provided Europe map SVG is a reusable asset.
The model may tweak it if necessary.

Permitted tweaks include:

- adding or changing fill;
- adjusting stroke or line treatment;
- minor path cleanup;
- minor path adjustment where necessary for visual use.

If a tweak is made, keep:

- the original provided SVG;
- the edited SVG actually used in the build;
- a short note in `generation-record.yaml` describing the change.

Once approved, the edited SVG becomes the shared project map and is reused consistently.

### 5.6 Optional shared assets

If used, the package may also include:

- signature placeholder;
- serial placeholder;
- common paper texture;
- common print-grain overlay;
- scene masks;
- helper geometry for deterministic placement.

Only include these if they are actually part of the build.

## 6. Generative decomposition

The generated note is divided into two principal specialized responsibilities.

### 6.1 Scene plate

The scene plate contains only the environmental or constructed Minecraft scene.

Its job is to maximize:

- game fidelity;
- spatial coherence;
- environmental composition;
- recognizable textures and objects;
- lighting;
- material detail;
- appropriate depth and density.

It does not need to solve monetary ornament or institutional layout.

### 6.2 Monetary artwork plate

The monetary artwork plate contains the generated graphic design that turns the environmental scene into a banknote surface.

It includes, where appropriate:

- denomination-specific border systems;
- value-field background treatment;
- institutional-field background treatment;
- guilloche-like or line-based ornament;
- scene transitions;
- decorative incursions around the scene;
- tonal and textural fields;
- denomination-specific visual rhythms;
- the complete empty ore badge on rectos, including its field, shape, ring treatment, and local decoration;
- quiet areas prepared for deterministic institutional assets.

It excludes:

- the environmental scene itself;
- the canonical ore cube;
- denomination numerals;
- EURO / ΕΥΡΩ / ЕВРО lettering;
- EU flag;
- Europe map;
- generated pseudo-text;
- any stable reusable asset handled deterministically.

The monetary artwork plate is not a generic frame.
It is a sophisticated denomination-specific banknote design layer.

## 7. Why scene and monetary artwork remain separate

The two layers are separated because specialization improves quality.

The scene can be generated as a strong Minecraft image without spending effort on banknote ornament.
The monetary artwork can be generated as rich currency design without spending effort reconstructing the environment.

The separation also makes both components replaceable.

A scene can be replaced while preserving the design system.
A monetary artwork plate can be replaced while preserving the selected scene.

The cost is that visual coherence is no longer automatic.
This workflow recovers coherence through context-aware generation and a fixed dependency order.

## 8. Dependency graph and generation order

The production graph is intentionally acyclic.

Use this order:

1. proposal and series visual grammar;
2. deterministic layout and proxy geometry;
3. scene generation;
4. scene selection and crop freeze;
5. context-composite construction;
6. monetary-artwork generation using the approved scene and proxies;
7. deterministic asset placement and treatment;
8. final flattening;
9. review and selective iteration.

The important dependency is:

`layout -> scene -> approved scene crop -> context -> monetary artwork -> deterministic assets -> final note`

### 8.1 Upstream and downstream responsibility

A downstream generated layer may depend visually on upstream layers.
An upstream layer should not depend on unfinished downstream pixels when a layout proxy can provide the necessary information.

For example:

- the scene knows the intended crop and broad placement, but does not need the finished ornament;
- the monetary artwork sees the actual approved scene and proxy silhouettes for later assets;
- the ore cube and institutional assets are placed after the artwork is approved.

### 8.2 Replacing an upstream layer

Replacing an upstream layer may invalidate downstream generated layers.

If the scene changes substantially, the monetary artwork may need regeneration because it was designed around the previous scene.

This is expected.
Swappability means the component can be replaced cleanly, not that every dependent artistic decision remains valid after any replacement.

### 8.3 Replacing a downstream layer

Replacing the monetary artwork does not require regenerating the approved scene.
Changing typography placement, flag treatment, map scale, or ore-block placement does not require any AI regeneration.

## 9. Layout skeleton and proxies

The note skeleton is deterministic and exists before generation begins.

It defines composition without becoming visible artwork.

### 9.1 Layout source of truth

Use a single `layout.yaml` file to define, for each note side:

- output width and height;
- scene crop and placement;
- broad scene mask or aperture if used;
- main numeral box;
- secondary value box if used;
- grouped euro-script box;
- EU flag box;
- Europe map box;
- signature or placeholder box;
- ore-badge footprint on rectos;
- ore-block box inside the badge;
- z-order;
- optional clipping masks.

### 9.2 Proxy geometry

Before monetary-artwork generation, create a temporary context composite that shows the approved scene plus simple proxy shapes for later deterministic assets.

The context composite may show:

- numeral silhouette or placeholder box;
- euro-script silhouette or placeholder box;
- EU flag box;
- Europe map silhouette or box;
- signature field;
- ore-block silhouette inside the intended badge region;
- any required quiet zone.

These proxies are not final artwork and must not appear in the exported monetary-artwork layer.

Their purpose is to give the model holistic composition awareness without baking reusable assets into the generated layer.

### 9.3 Badge footprint

Because the empty badge is part of the monetary artwork, `layout.yaml` should define only the broad badge footprint and ore-block area before artwork generation.

Within that footprint, the model may vary the badge geometry and detailing by denomination.

This allows substantial visual variation without allowing the badge to drift arbitrarily across the note.

## 10. Scene generation

### 10.1 Generation responsibility

Generate one specialized scene plate for each of the twelve note sides.

The scene should not contain monetary ornament or stable institutional assets.

### 10.2 Overscan

Prefer some extra image beyond the final visible crop when practical.

This gives the deterministic composition stage room to:

- reposition slightly;
- change crop;
- adjust scale;
- avoid accidental edge collisions.

The scene does not need to be generated already trapped inside its final aperture.

### 10.3 Shared style consistency

All twelve scene plates should maintain broadly the same:

- rendering language;
- level of detail;
- texture crispness;
- Minecraft fidelity;
- edge behaviour;
- lighting naturalism;
- degree of saturation;
- apparent block-detail scale.

Consistency is especially important because the scene layer is generated independently from the monetary artwork.

The model must not allow one note to become painterly, smoothed, cinematic voxel art while another resembles a crisp game view.

### 10.4 Minecraft fidelity

Use:

- canonical or near-canonical block textures;
- recognizable terrain behaviour;
- recognizable game objects and workstations;
- believable block proportions;
- familiar environmental scale.

Avoid:

- heavy outlines around every cube;
- generic voxel fantasy;
- invented materials replacing familiar blocks;
- smooth surfaces that suppress Minecraft texture identity.

### 10.5 Recto scene rule

Recto scenes should generally approach the visual directness of a carefully selected Minecraft view.

If the monetary artwork is hidden, the scene should still read immediately as Minecraft.

### 10.6 Verso scene rule

Verso scenes may be larger and denser, but they should remain Minecraft-native.

Construct concepts from recognizable Minecraft objects, architecture, terrain, villagers, workstations, mechanisms, and systems rather than translating an abstract civic idea into generic cubes.

### 10.7 Scene exclusions

Do not generate scene plates with:

- EU flag;
- Europe map;
- ore badge;
- ore-block inset;
- denomination numerals;
- euro scripts;
- pseudo-text;
- HUD;
- inventory bar;
- crosshair;
- recipe strip;
- explanatory arrows.

## 11. Scene selection and crop freeze

After generating candidate scene imagery:

1. select the approved scene;
2. determine the final scale and crop;
3. record the scale and crop in `layout.yaml`;
4. create the positioned scene preview at final note size;
5. freeze that scene state before monetary-artwork generation begins.

The monetary artwork must respond to the actual approved scene crop, not merely the scene prompt.

If the scene crop later changes substantially, review whether the monetary artwork remains valid.

## 12. Context-composite construction

Use `build_contexts.py` to construct one context image for each note side before monetary-artwork generation.

The context image contains:

- the approved positioned scene;
- the final note canvas boundary;
- simple layout proxies for deterministic assets;
- badge footprint and ore-block proxy on rectos;
- any scene mask or aperture information useful to the design.

The context should be visually clear enough for the model to understand the complete note composition, but simple enough that it cannot be mistaken for final ornament.

Save these context images under `generated/contexts/` because they are part of the reproducible generation history.

## 13. Monetary-artwork generation

Generate one monetary artwork plate for each note side after the scene crop is frozen.

### 13.1 Context-aware generation

The model should see the context composite containing the actual approved scene and layout proxies.

It must design the monetary artwork in relation to:

- scene silhouette;
- scene tonal masses;
- open areas in the scene;
- denomination colour and motif;
- numeral location;
- euro-script location;
- map location;
- flag location;
- ore-block location on rectos;
- overall note proportions.

The output, however, contains only the monetary artwork layer.

### 13.2 Technical separation, visual interdependence

The monetary artwork may visually react to the scene in sophisticated ways.

It may:

- curve around important scene forms;
- fade into or out of scene edges;
- carry patterns that echo environmental geometry;
- use asymmetric ornament;
- create irregular scene transitions;
- weave visually behind or around deterministic asset positions;
- place dense and quiet zones according to the underlying scene;
- integrate the empty badge into the surrounding denomination-specific ornament.

It must not become visually generic merely because it is isolated as a separate file.

### 13.3 Richness target

Monetary artwork should aim for the richness and seriousness of the strongest one-pass notes.

It should contain enough small and medium-scale structure to feel designed as currency rather than as a scene pasted into a rectangular template.

The target is not maximum density everywhere.
The target is controlled richness with hierarchy.

### 13.4 Denomination variation

Do not generate one base monetary-artwork system and simply recolor it six times.

Keep series continuity through:

- layout grammar;
- typography;
- institutional placement;
- related density;
- related print language;
- recurring compositional logic.

Allow denomination-specific variation in:

- badge geometry;
- border rhythm;
- ornamental motifs;
- local field shapes;
- aperture interaction;
- surface pattern;
- visual emphasis;
- asymmetry.

### 13.5 Empty badge integration

On rectos, the empty ore badge is generated as part of the monetary artwork plate.

The artwork generator should design the badge together with its surrounding ornament so that they share one visual language.

The badge must reserve a clear central region for the canonical ore raster.

It may vary substantially between denominations while remaining within the broad footprint specified by `layout.yaml`.

### 13.6 Monetary-artwork exclusions

Do not generate:

- ore cube;
- numeral text;
- EURO / ΕΥΡΩ / ЕВРО;
- EU flag;
- Europe map;
- signature text;
- pseudo-lettering;
- visible layout guides;
- notebook-like horizontal rules;
- placeholder panel lines;
- template scaffolding;
- abstract wireframe frames;
- generic blank rectangles pretending to be banknote structure.

### 13.7 Transparency and isolation

Prefer monetary artwork as a transparent full-canvas PNG.

If the generation system cannot reliably return transparency, isolate the artwork through a simple documented masking step and save the resulting transparent project layer.

The approved transparent artwork file is the component consumed by the final builder.

## 14. Deterministic asset integration

After the monetary artwork plate is approved, insert stable assets deterministically.

These include:

- ore block on rectos;
- main numeral and euro sign;
- secondary denomination typography if used;
- grouped EURO / ΕΥΡΩ / ЕВРО asset;
- EU flag;
- Europe map;
- signature or other placeholders.

### 14.1 Printed display treatments

Reusable assets may receive deterministic denomination-specific display treatments so they belong materially to the note.

Permitted treatments include:

- fill changes;
- opacity changes;
- palette tinting;
- paper texture interaction;
- restrained overprint;
- masking;
- line or grain integration.

The treatment must not alter the underlying identity or geometry of fixed institutional assets.

### 14.2 EU flag integration

The flag geometry remains exact.
Its display version may receive restrained paper or denomination integration so it does not appear pasted onto the note as a clean digital rectangle.

### 14.3 Europe map integration

Use the approved project map at a clearly legible scale.

The map should not become a tiny token in the institutional field.
Its size and position are controlled by `layout.yaml` and reviewed across the full series.

### 14.4 Euro-script integration

Place the grouped euro-script asset as one composition.
Do not independently size the three script lines during final note construction.

### 14.5 Ore-block integration

Insert the canonical ore raster into the empty badge after monetary-artwork generation.

Keep its apparent scale and isometric treatment consistent across rectos unless the proposal explicitly requires otherwise.

## 15. Centralized layout specification

All stable positions belong in `layout.yaml`.
They should not be scattered across generation prompts as loosely repeated prose.

### 15.1 Coordinate model

Use pixel coordinates derived from the authoritative final output sizes.

A simple format is sufficient:

- `x`, `y` for top-left placement;
- `width`, `height` for boxes;
- `cx`, `cy`, `diameter` or `size` for centered elements;
- scene scale and offsets;
- mask references;
- z-order.

### 15.2 Hard-controlled elements

At minimum, hard-control:

- final canvas size;
- scene crop, scale, and offset;
- ore-block placement and scale;
- main numeral placement and scale;
- grouped euro-script placement and scale;
- EU flag placement;
- Europe map placement and scale;
- signature or placeholder placement;
- z-order;
- masks or clipping used in final composition.

### 15.3 Broad artwork constraints

The monetary artwork itself is not positioned element by element through YAML.
It is a full-canvas generated design layer.

YAML controls the proxy geometry it must respect and the deterministic elements inserted afterward.

This keeps the artistic layer free while the final build remains reproducible.

## 16. Typography workflow

Typography must be deterministic and reusable.

### 16.1 Source

The provided Minecraft TTF is the source.

### 16.2 Derived assets

Use `build_type_assets.py` to generate:

- outlined SVG numerals;
- outlined SVG euro sign;
- outlined SVG `EURO`;
- outlined SVG `ΕΥΡΩ`;
- outlined SVG `ЕВРО`;
- grouped euro-script stack;
- optional PNG previews.

### 16.3 Final use

The build script inserts these assets according to `layout.yaml`.
Do not rely on live text rendering during final composition.

## 17. Python scripts

The package should include a small Python toolchain.

### 17.1 `build_type_assets.py`

Purpose:

- read the provided TTF;
- generate outlined SVG lettering and numerals;
- generate grouped euro-script assets;
- generate preview PNGs if useful.

### 17.2 `build_contexts.py`

Purpose:

- read `layout.yaml`;
- position the approved scene crop;
- draw simple proxies for later deterministic assets;
- export the context composites used for monetary-artwork generation.

### 17.3 `build_notes.py`

Purpose:

- read `layout.yaml` and `generation-record.yaml`;
- position and crop scene plates;
- place the monetary artwork plate;
- rasterize vector assets when needed;
- apply deterministic display treatments;
- insert all stable assets;
- apply masks and z-order;
- flatten the final note PNGs;
- optionally export full-canvas placed layers for inspection.

### 17.4 `build_contact_sheets.py`

Purpose:

- generate overview sheets for review;
- optionally build recto, verso, paired, and grayscale contact sheets.

## 18. YAML files

Use YAML for the project’s small amount of structured data.

### 18.1 `layout.yaml`

Stores:

- final dimensions;
- scene crop and placement;
- proxy geometry;
- deterministic asset placement;
- masks;
- z-order.

### 18.2 `generation-record.yaml`

Stores a lightweight record of:

- approved scene source for each side;
- approved scene crop or scene version;
- context composite used for artwork generation;
- approved monetary artwork source;
- the scene on which each monetary artwork plate depends;
- whether the Europe map SVG was adjusted;
- any small manual repair or approval note worth preserving.

This dependency record is useful because replacing an upstream scene can invalidate downstream artwork.

It is not intended as bureaucratic version tracking.

## 19. Construction procedure

### 19.1 Prepare reusable inputs

1. Place the provided TTF, ore rasters, EU flag SVG, and Europe map SVG in `assets/`.
2. If the map is adjusted, save the approved project map separately.
3. Run `build_type_assets.py` to create deterministic typography assets.
4. Define the stable layout and proxy geometry in `layout.yaml`.

### 19.2 Generate and freeze scenes

1. Generate the twelve specialized scene plates.
2. Compare them as a complete visual family.
3. Select the approved scene for each note side.
4. Set scene crop, scale, and offset in `layout.yaml`.
5. Freeze the approved positioned scene state.

### 19.3 Build context composites

1. Run `build_contexts.py`.
2. Export one context image per side containing the positioned scene and simple proxies.
3. Verify that proxy positions are large enough and compositionally useful before artwork generation.

### 19.4 Generate monetary artwork

1. Use the relevant context composite as the visual basis.
2. Generate denomination-specific monetary artwork with the empty badge integrated on rectos.
3. Require output isolation from the scene and deterministic assets.
4. Review richness, scene integration, denomination identity, and quiet zones.
5. Freeze the approved monetary artwork plate.

### 19.5 Build final notes

1. Run `build_notes.py`.
2. Composite the approved scene and monetary artwork.
3. Insert ore cube, typography, flag, map, and placeholders deterministically.
4. Apply documented display treatments.
5. Export the final flattened note PNGs.
6. Optionally export full-canvas placed layer previews.

### 19.6 Build contact sheets

1. Run `build_contact_sheets.py`.
2. Export at least one whole-series overview.

## 20. Layer order for final flattening

A typical final order is:

1. positioned scene plate;
2. monetary artwork plate, including empty recto badge;
3. canonical ore block, recto only;
4. main numeral and euro sign;
5. secondary denomination typography if used;
6. grouped euro-script asset;
7. EU flag;
8. Europe map;
9. signature or placeholder assets;
10. optional common paper or print integration overlay.

The exact order may be adjusted for a specific design, but it must be fixed and documented.

## 21. Full-canvas support

The workflow must support full-canvas placed layer exports.

This does not mean every reusable master asset must be stored only as a full-canvas raster.

Use two forms where useful:

- master asset: compact reusable SVG or cropped PNG;
- placed layer export: full-canvas transparent PNG at final note size.

Examples:

- `assets/maps/europe_map_project.svg`
- `outputs/layer_previews/EUR020_recto_map.png`

- `assets/ore_blocks/ore_lapis_iso.png`
- `outputs/layer_previews/EUR020_recto_ore.png`

This makes the package easy to inspect or import into Paint.NET without forcing every stored master asset to contain large transparent margins.

## 22. Final exports

At minimum, export:

- the twelve final note PNGs at the exact sizes listed in Section 1;
- one recto contact sheet;
- one verso contact sheet;
- one paired or all-series review sheet.

Optional useful exports include:

- grayscale contact sheet;
- full-canvas layer previews for any or all note sides.

Do not require TIFFs, PDFs, nested archives, or oversized review bundles unless specifically needed.

## 23. Quality control

### 23.1 Scene consistency

Confirm that:

- all twelve scenes belong to one visual family;
- detail level is broadly comparable;
- Minecraft textures remain crisp and recognizable;
- block surfaces are not smoothed into another voxel style;
- rectos preserve game-like directness where intended;
- versos remain Minecraft-native rather than generic block fantasy.

### 23.2 Monetary-artwork quality

Confirm that:

- monetary artwork is rich enough to make the result feel like a banknote;
- it does not read as a sterile overlay or collage of utility panels;
- it responds to the actual scene rather than framing it generically;
- denomination-specific ornament is genuinely distinct;
- the badge feels integrated with surrounding ornament;
- no visible layout guides or scaffold-like structures appear;
- quiet zones remain visually designed rather than empty blank rectangles.

### 23.3 Structural checks

Confirm that:

- every final file matches the exact target size;
- scene placement follows `layout.yaml`;
- ore-block placement and scale are correct;
- the grouped euro-script block has uniform optical sizing;
- the EU flag is consistently placed;
- the Europe map is large enough to function as a visible institutional element;
- deterministic assets do not collide with the monetary artwork.

### 23.4 Reusability checks

Confirm that:

- ore cubes come from the provided assets;
- the EU flag is reused rather than redrawn;
- the Europe map comes from the approved project source;
- typography comes from derived font assets rather than image generation;
- scenes and monetary artwork exist as separate replaceable files;
- final notes rebuild correctly through Python.

### 23.5 Dependency checks

Confirm that:

- each monetary artwork plate records the scene/context it was designed against;
- replacing a scene triggers review of the dependent artwork;
- replacing monetary artwork does not require replacing the scene;
- changing deterministic assets does not require AI regeneration.

## 24. Intended editing model

The package should support changes at the level where they actually belong.

Examples:

- scene wrong: replace the scene, freeze a new crop, rebuild the context, then review or regenerate the dependent monetary artwork;
- ornament or badge weak: replace only the monetary artwork plate;
- badge ore cube wrong: replace only the ore asset;
- map too small: change `layout.yaml` and rebuild;
- euro scripts visually uneven: correct the grouped typography asset and rebuild;
- flag treatment too clean: adjust the deterministic display treatment and rebuild;
- scene crop slightly wrong: adjust scale or offsets and review whether the monetary artwork still fits.

The workflow does not pretend every layer is independent of every other layer.
It makes dependencies explicit so changes remain controlled.

## 25. What this workflow deliberately avoids

This workflow deliberately avoids:

- treating layer separation as an instruction to simplify design;
- generating ornament in a visual vacuum;
- one universal decorative template recolored across the series;
- separate badge generation when badge and surrounding ornament are better solved together;
- visible layout guides or scaffold-like frame generation;
- generic blank side panels;
- regenerated typography, maps, flags, or ore blocks;
- forcing the scene generator to solve banknote graphics;
- forcing the monetary-artwork generator to reconstruct Minecraft environments;
- pretending that replacing an upstream scene never affects downstream design;
- fake print-production complexity;
- CSV manifests and checksum bureaucracy;
- unnecessary micro-layer decomposition.

The objective is specialized generation with controlled interdependence.
The scene and monetary artwork remain independently stored and swappable, but each is allowed to be visually sophisticated.

## 26. Minimum package checklist

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
- approved generated scene plates;
- saved context composites;
- approved generated monetary artwork plates with empty recto badges;
- derived typography assets;
- the twelve final flattened note PNGs;
- at least one contact sheet.

If a reviewer can inspect the specialized layers, understand which generated layers depend on which upstream choices, run the scripts, and immediately view the final notes without manual reconstruction, the package has succeeded.
