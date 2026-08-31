# Layered professional design package specification

## Purpose

This document defines the repeatable construction package for the final twelve banknote designs.

The proposal defines meaning and visual intent. This package defines assets, dimensions, layers, transformations, assembly, exports, and quality control.

The system minimises dependence on image-generation consistency. Generative tools are used primarily for the twelve scene plates. Shared maps, flag geometry, lettering, numerals, frames, label geometry, ore blocks, paper treatment, and most denomination patterns are created once and reused through deterministic transforms.

## 1. Working scale and exact artboards

Use a working raster scale of 20 pixels per millimetre. Keep vector components as vectors until export.

### 1.1 Trim dimensions

| Denomination | Physical size |    Trim canvas |
| ------------ | ------------: | -------------: |
| €5           |   120 × 62 mm | 2400 × 1240 px |
| €10          |   127 × 67 mm | 2540 × 1340 px |
| €20          |   133 × 72 mm | 2660 × 1440 px |
| €50          |   140 × 77 mm | 2800 × 1540 px |
| €100         |   147 × 77 mm | 2940 × 1540 px |
| €200         |   153 × 77 mm | 3060 × 1540 px |

These dimensions apply to both sides.

### 1.2 Bleed canvas

Add 3 mm bleed on every edge for working masters.

At 20 px/mm, add 60 pixels on each side. The bleed canvas is therefore 120 pixels wider and 120 pixels higher than the trim canvas.

| Denomination |   Bleed canvas |
| ------------ | -------------: |
| €5           | 2520 × 1360 px |
| €10          | 2660 × 1460 px |
| €20          | 2780 × 1560 px |
| €50          | 2920 × 1660 px |
| €100         | 3060 × 1660 px |
| €200         | 3180 × 1660 px |

All final public PNG files are exported at trim size with no visible area outside the banknote.

## 2. Colour management

Use sRGB for generation and review PNG files.

Maintain 16-bit RGB masters where supported. Produce CMYK proof files only after the visual design is approved and a print profile is selected.

Store all palette values in one machine-readable palette file so that shared assets can be recoloured without regeneration.

### 2.1 Denomination palettes

| Denomination | Paper     | Dominant  | Structural dark | Accent    |
| ------------ | --------- | --------- | --------------- | --------- |
| €5           | `#EEEDE6` | `#6B6D6C` | `#303334`       | `#7C846F` |
| €10          | `#EFE5E4` | `#854650` | `#4A292E`       | `#A4464F` |
| €20          | `#EEE9DC` | `#6C8197` | `#344858`       | `#3E6393` |
| €50          | `#F0E5D7` | `#A66B4B` | `#5C3C2E`       | `#708C82` |
| €100         | `#E7ECE5` | `#587762` | `#30493A`       | `#41845B` |
| €200         | `#F1E8D5` | `#AF8948` | `#5D4A2B`       | `#C39A3F` |

These values are starting points. Store approved revisions in `palettes.json`; do not alter individual files by eye after the palette is frozen.

### 2.2 Colour transform

Apply one saved transform per denomination to both sides.

The transform maps highlights toward the paper swatch, middle values toward the dominant swatch, and shadows toward the structural-dark swatch.

Preserve a separate accent mask for ore fragments, powered redstone, pigment, copper reflections, emeralds, and selected gold details. Accent coverage should remain approximately 3 to 5 percent of the visible surface.

Do not recolour shared assets by regenerating them. Recolour vector fills or apply the stored palette transform.

## 3. Project directory

Use this directory structure:

- `00_documentation/`
  - `crafting-europe-v3.md`
  - `design-package.md`
  - `manifest.csv`
  - `layout.json`
  - `palettes.json`
  - `checksums.sha256`
- `01_shared_assets/`
  - `vector/`
  - `raster/`
  - `fonts_or_outlined_type/`
  - `textures/`
- `02_ore_blocks/`
  - `source_textures/`
  - `renders/`
  - `masks/`
- `03_denomination_assets/`
  - `EUR005/`
  - `EUR010/`
  - `EUR020/`
  - `EUR050/`
  - `EUR100/`
  - `EUR200/`
- `04_scene_plates/`
  - one recto and one verso folder per denomination
- `05_layered_masters/`
  - twelve layered working files
- `06_exports/`
  - `review_png/`
  - `print_tiff/`
  - `proof_pdf/`
  - `contact_sheets/`
- `07_archive/`
  - superseded versions and review notes

## 4. Naming convention

Use `EUR` followed by a three-digit denomination, side, layer number, and description.

Examples:

- `EUR005_R_10_scene.png`
- `EUR005_R_20_value-field.svg`
- `EUR005_R_40_ore-label.svg`
- `EUR005_R_41_ore-block.png`
- `EUR005_R_52_europe-map.svg`
- `EUR005_V_10_scene.png`
- `EUR005_V_60_border.svg`
- `EUR005_V_90_flat.png`

Use `R` for recto and `V` for verso.

Layer numbers remain consistent across all twelve masters.

## 5. Shared assets created once

The following assets are never regenerated per denomination.

### 5.1 Europe map

Create `europe-map-master.svg` from one approved projection and coastline path.

Keep:

- one silhouette;
- one orientation;
- one projection;
- one internal coastline geometry;
- one view box;
- one aspect ratio.

For each denomination, duplicate the linked instance, scale it to the prescribed map box, and recolour it through `palettes.json`.

Do not redraw, restyle, stretch, or prompt-generate the map again.

Export a full-canvas transparent PNG for each note side in addition to the shared SVG so every component can be inspected independently.

### 5.2 European flag

Create `eu-flag-master.svg` with exact twelve-star geometry and a 3:2 field.

Use the same master everywhere.

For concept and review plates, integrate the flag with the note by applying the common paper texture and a restrained denomination-colour overprint at low opacity. Preserve the recognisable blue field and yellow stars, but avoid a flat digital rectangle.

Do not regenerate the flag.

### 5.3 Euro scripts

Create one vector master containing:

- `EURO`
- `ΕΥΡΩ`
- `ЕВРО`

Use a Minecraft-derived pixel alphabet designed as one family across Latin, Greek, and Cyrillic.

Outline the approved lettering before archival export so the package does not depend on an installed font.

Do not use generated lettering in final masters.

### 5.4 Numerals and euro sign

Create vector masters for:

- `5`
- `10`
- `20`
- `50`
- `100`
- `200`
- `€`

Use the same type system as the scripts.

Scale by note height according to `layout.json`. Do not generate numerals as part of the scene plate.

### 5.5 Signature and serial placeholders

Create neutral vector placeholders with no real signature and no functional serial number.

Use the same geometry and baseline rules throughout the series.

### 5.6 Paper and print textures

Create one seamless paper texture at 20 px/mm and one large non-repeating master covering the largest bleed canvas.

Create separate deterministic overlays for:

- paper fibre;
- subtle plate grain;
- low-opacity stipple;
- selective linework;
- registration variation for review simulation.

Use the same texture masters on every denomination. Change opacity or palette through stored parameters, not through new generation.

## 6. Canonical ore-block assets

The ore block is the only object inside the recto label.

### 6.1 Source

Use canonical game textures or user-supplied approved captures for:

- coal ore;
- redstone ore;
- lapis ore;
- copper ore;
- emerald ore;
- gold ore.

Do not ask an image generator to invent the blocks.

Keep source files private to the project and respect applicable asset-use terms.

### 6.2 Deterministic render

Render every block from the same simple cube scene:

- orthographic camera;
- azimuth 45 degrees;
- elevation 35.264 degrees;
- identical cube dimensions;
- identical camera distance;
- identical neutral lighting;
- transparent background;
- no cast shadow;
- no outline;
- nearest-neighbour texture sampling before final print treatment.

Export each block at 1024 × 1024 pixels as transparent PNG.

The visible cube must occupy the same percentage of the 1024-pixel square in all six files.

### 6.3 Derived outputs

For each ore, provide:

- `ore-<name>-iso-source.png`
- `ore-<name>-iso-print.png`
- `ore-<name>-mask.png`
- `ore-<name>-preview.png`

The print version receives the same restrained paper and colour treatment as the note. Geometry and texture placement remain unchanged.

## 7. Parametric layout

Store all layout values in `layout.json` as normalised coordinates relative to trim width `W` and trim height `H`.

### 7.1 Shared recto coordinates

Use these starting values:

| Element                   | Position or size        |
| ------------------------- | ----------------------- |
| Outer frame inset         | `0.025H`                |
| Left value field width    | `0.18W`                 |
| Institutional field start | `0.70W`                 |
| Ore-label centre X        | `0.685W`                |
| Ore-label centre Y        | `0.50H`                 |
| Ore-label diameter        | `0.44H`                 |
| Ore-block visible width   | `0.58 × label diameter` |
| Main numeral height       | `0.50H`                 |
| Main numeral left edge    | `0.045W`                |
| Main numeral top          | `0.17H`                 |
| Flag height               | `0.085H`                |
| Flag width                | `0.1275H`               |
| Flag top                  | `0.055H`                |
| Flag left                 | `0.735W`                |
| Euro-script baseline      | `0.195H`                |
| Map box left              | `0.785W`                |
| Map box top               | `0.275H`                |
| Map box width             | `0.165W`                |
| Map box height            | `0.405H`                |
| Signature box left        | `0.735W`                |
| Signature box top         | `0.745H`                |
| Signature box width       | `0.220W`                |
| Signature box height      | `0.115H`                |

Use proportional placement rather than hand-positioning each denomination.

### 7.2 Shared verso coordinates

Use these starting values:

| Element                   | Position or size |
| ------------------------- | ---------------- |
| Outer frame inset         | `0.025H`         |
| Left value field width    | `0.15W`          |
| Panorama start            | `0.15W`          |
| Institutional field start | `0.82W`          |
| Main numeral height       | `0.50H`          |
| Main numeral left edge    | `0.045W`         |
| Main numeral top          | `0.17H`          |
| Euro scripts left         | `0.735W`         |
| Euro-script baseline      | `0.105H`         |
| Map box left              | `0.825W`         |
| Map box top               | `0.205H`         |
| Map box width             | `0.135W`         |
| Map box height            | `0.455H`         |
| Secondary field left      | `0.825W`         |
| Secondary field top       | `0.725H`         |
| Secondary field width     | `0.135W`         |
| Secondary field height    | `0.160H`         |

The verso has no reserved recipe strip, arrow band, use-icon row, or forced route across the lower edge.

### 7.3 Optical adjustments

Allow optical corrections of no more than 1 percent of `W` or `H` after full-series review.

Record every correction in `layout.json`. Do not make undocumented per-file changes.

## 8. Layer stack

Every layered master uses the following order.

| Layer | Name                              | Source                                    |
| ----: | --------------------------------- | ----------------------------------------- |
|    00 | Transparent bleed background      | deterministic                             |
|    05 | Paper base                        | shared raster                             |
|    10 | Main scene plate                  | generated once for that side              |
|    11 | Scene correction                  | local non-generative edits                |
|    12 | Scene palette transform           | saved transform                           |
|    20 | Value-field base                  | vector                                    |
|    21 | Main numeral and euro sign        | linked vector                             |
|    30 | Institutional-field base          | vector                                    |
|    31 | European flag                     | linked vector                             |
|    32 | Euro scripts                      | linked vector                             |
|    33 | Europe map                        | linked vector                             |
|    34 | Signature and serial placeholders | linked vector                             |
|    40 | Ore-label base, recto only        | vector                                    |
|    41 | Canonical ore block, recto only   | deterministic raster                      |
|    42 | Ore-label texture, recto only     | procedural/vector                         |
|    50 | Outer frame                       | vector                                    |
|    51 | Denomination border pattern       | tiled vector                              |
|    60 | Tactile and security reservations | vector                                    |
|    70 | Selective linework                | deterministic raster                      |
|    71 | Stipple and plate grain           | shared raster                             |
|    72 | Paper fibre overlay               | shared raster                             |
|    80 | Proof-only registration effect    | deterministic, disabled in archive master |
|    90 | Trim and export guides            | non-printing                              |

Every raster layer is provided as a full-canvas transparent PNG at the exact bleed dimensions, even when its visible content occupies a small area.

Every vector layer is provided as SVG and as a full-canvas transparent PNG preview.

## 9. Scene-plate generation

The twelve scene plates are the principal generative assets.

### 9.1 General scene rules

Generate scenes without:

- numerals;
- euro scripts;
- flag;
- Europe map;
- signature field;
- serial field;
- border;
- ore label;
- pictogram strips;
- arrowed stages;
- UI elements;
- game logo;
- pseudo-text.

Generate at the exact bleed-canvas size or larger with the same aspect ratio. Preserve enough content beyond the scene mask for minor positional adjustment.

### 9.2 Recto scene plates

Each recto scene is one coherent Minecraft landscape.

Do not generate a geological cutaway, visible crust, mantle section, split surface-and-underground view, or transparent mountain.

Use canonical terrain morphology and familiar materials. Do not place dark contours around every block.

The ore must appear naturally in the landscape, but it does not need to carry the full burden of identification because the canonical block will be inserted separately in the label.

### 9.3 Verso scene plates

Each verso scene is one integrated constructed environment.

Do not create a lower recipe panel, sequence of framed applications, row of icons, arrowed stages, or explanatory route.

The material's uses must be visible through spatial relations and activity.

### 9.4 Scene source files

For every scene provide:

- original generated image;
- selected working image;
- generation metadata or prompt record;
- scene mask;
- correction layer;
- approved colour-treated scene;
- rejection notes for discarded outputs.

Keep original pixels unchanged in the archive. Apply corrections non-destructively.

## 10. Denomination scene inventory

### 10.1 EUR005

Recto scene: canonical mountain landscape, exposed coal seam, alpine grass, restrained snow, distant valley, no cutaway.

Verso scene: coal transport, furnaces, blast furnaces, hoppers, smithing, rail logistics, iron bridge, industrial town, repaired ground.

### 10.2 EUR010

Recto scene: canonical deepslate cavern, visible redstone vein, water, dripstone, restrained lava, no fantasy cave architecture.

Verso scene: distributed redstone systems across farming, sorting, doors, rail control, lighting, music, logic, and teaching.

### 10.3 EUR020

Recto scene: broad stone cavern, modest lapis seam, water, pale rock, cool mineral atmosphere.

Verso scene: pigment workshop, library, enchanting space, classroom, maps, observatory, stained glass, bookbinding, public reading, applied learning.

### 10.4 EUR050

Recto scene: dripstone cave, copper ore, granite, water, raw copper, restrained early green staining.

Verso scene: civic copper infrastructure, roofs across oxidation stages, lighting, lightning protection, water, observation, archaeology, transport, maintenance, supporting iron.

### 10.5 EUR100

Recto scene: high mountain, snow, sparse grass, valley, isolated emerald ore on a visible cliff.

Verso scene: public market square, villager professions, farms, library, maps, workshops, well, bridge, repair, exchange without interface graphics.

### 10.6 EUR200

Recto scene: badlands mesas, ravine, exposed gold ore, sparse vegetation, optional distant mineshaft, no cutaway.

Verso scene: assay and reserve district, transport, clock hall, observatory, treatment garden, beacon, public square, scientific uses, balanced piglin exchange.

## 11. Scene colour and print transform

Apply the same recorded sequence to every scene.

### 11.1 Base preparation

1. Place the approved scene at bleed size.
2. Preserve a linked copy of the original.
3. Correct perspective only when the generated note-space scene is inconsistent with the intended panorama.
4. Remove generated text, invented interface elements, and non-canonical decorative objects through local edits.
5. Do not smooth canonical block textures into painted surfaces.

### 11.2 Palette mapping

1. Convert a copy to luminance.
2. Map highlights, middle values, and shadows through the denomination palette.
3. Restore accent colour only through the approved accent mask.
4. Reduce global saturation until large colour fields read as printed ink.
5. Save the transform as a reusable action or node graph.

### 11.3 Selective linework

1. Create a luminance copy.
2. Apply a small blur equal to approximately `0.0015H` to suppress texture noise.
3. Derive edges from the blurred image so major forms are selected rather than every block seam.
4. Remove repeating one-block grid edges where they create continuous cube outlines.
5. Composite the structural line layer in the denomination dark at low opacity.
6. Add denser linework only in borders, maps, distant atmospheric forms, and selected shadows.

Do not apply universal engraving to every surface.

### 11.4 Paper integration

1. Composite the shared paper base beneath the scene.
2. Apply the common paper fibre above the scene at stored opacity.
3. Apply plate grain and stipple through shared masks.
4. Use the same grain scale on all denominations.
5. Keep the ore block and principal numeral clearer than surrounding fine texture.

## 12. Ore-label construction

The label is assembled, not generated.

### 12.1 Base

Create one vector circle master.

Scale it to `0.44H` and place its centre at `(0.685W, 0.50H)`.

Fill it with a mix of the paper swatch and approximately 5 to 8 percent of the denomination dominant colour.

### 12.2 Texture

Use one deterministic texture per denomination:

| Denomination | Texture                             |
| ------------ | ----------------------------------- |
| €5           | sedimentary hatching                |
| €10          | faint signal traces                 |
| €20          | manuscript ruling and pigment grain |
| €50          | conductive mesh                     |
| €100         | exchange lattice                    |
| €200         | concentric reserve rings            |

Keep texture contrast low enough that the field reads as near-white.

### 12.3 Ore block

Place the canonical `ore-<name>-iso-print.png` at the exact common scale.

Use no caption, name, symbol, second object, drop shadow, orbit ring, or use icon.

### 12.4 Edge

Use one fine inner rule and one outer rule with the denomination pattern between them.

Do not create a glass lens effect.

## 13. Border construction

Create vector border tiles once per denomination.

The border carries abstract material rhythm only.

| Denomination | Border source                         |
| ------------ | ------------------------------------- |
| €5           | strata and coal speck rhythm          |
| €10          | branching signal geometry             |
| €20          | manuscript rhythm and pigment grain   |
| €50          | conductive bands and oxidation fields |
| €100         | market paving and exchange lattice    |
| €200         | reserve rings and measured facets     |

Use corner modules that are not stretched. Extend straight sections by repetition or parametric generation.

Do not include use carousels, minecart strips, furnace icons, tools, books, wheels, or material recipes in the recto border.

## 14. Typography and institutional composition

### 14.1 Typography

Place the numeral, euro sign, and three scripts from linked vectors.

Use exact strings only. Do not rely on image-generated text.

### 14.2 Map

Place the linked map master into the map box without changing its aspect ratio.

Use contain-fit, not stretch-to-fill.

Recolour through palette variables.

### 14.3 Flag

Place the linked flag master at the exact common size relative to note height.

Apply shared paper grain and the approved low-opacity denomination overprint.

### 14.4 Institutional fields

Use common vector frames for signature, serial placeholder, secondary value, and technical reservations.

Their geometry is generated from `layout.json` and reused.

## 15. Master-file package per side

Each side folder contains:

- layered master in PSD, PSB, or ORA format;
- linked-asset folder;
- every raster layer as full-canvas transparent PNG;
- every vector layer as SVG;
- every vector layer as full-canvas PNG preview;
- trim preview PNG;
- bleed preview PNG;
- 16-bit RGB TIFF;
- proof PDF;
- layer manifest CSV;
- checksum file;
- review notes.

The master must open without missing links.

## 16. Final export set

For each of the twelve sides export:

- `*_flat_srgb.png` at exact trim dimensions;
- `*_flat_16bit.tif` at exact trim dimensions;
- `*_bleed_16bit.tif` at bleed dimensions;
- `*_proof.pdf` with trim and bleed information;
- `*_layers.zip` containing individual layers;
- `*_master.zip` containing the working master and linked assets.

For the complete series export:

- recto contact sheet;
- verso contact sheet;
- paired-side contact sheet;
- grayscale contact sheet;
- ore-label comparison sheet;
- map-placement comparison sheet;
- colour-palette sheet;
- accessibility review sheet.

## 17. Deterministic reuse rules

Use these rules to minimise regeneration:

- Europe map: one SVG, recoloured and placed by coordinates.
- Flag: one SVG, same geometry, same relative size, shared print treatment.
- Scripts and numerals: linked vectors, never generated inside images.
- Ore blocks: deterministic renders from canonical textures.
- Ore label: one vector master, scaled by note height.
- Paper texture: one shared master.
- Frame: parametric vector geometry driven by note dimensions.
- Border patterns: one tile per denomination, reused on both sides.
- Tactile reservations: shared vector system.
- Colour treatment: stored palette transform per denomination.
- Selective linework: stored deterministic filter sequence.
- Scene corrections: non-destructive local layers.

Regenerate a scene only when its world, composition, or Minecraft fidelity is wrong. Do not regenerate a scene to correct typography, map geometry, label size, border placement, paper grain, or colour balance.

## 18. Quality-control checklist

### 18.1 Geometry

- trim and bleed dimensions match the tables;
- note edges are perfectly horizontal and vertical;
- no outer margin appears in trim exports;
- all fixed elements match `layout.json`;
- ore-label diameter and centre are exact;
- map aspect ratio is unchanged;
- flag geometry is unchanged.

### 18.2 Minecraft fidelity

- terrain is recognisably Minecraft;
- canonical materials and objects remain recognisable;
- block surfaces are not universally outlined;
- rectos contain no geological cutaway;
- structures do not drift into generic voxel fantasy;
- mechanisms and workstations remain game-native where shown;
- no HUD, inventory, crosshair, game logo, or pseudo-text appears.

### 18.3 Narrative

- recto shows natural occurrence and context;
- ore label contains one canonical block only;
- verso shows an integrated constructed world;
- no recto use pictograms appear;
- no verso recipe strip, arrows, or forced process band appears;
- figures remain secondary to systems and civic spaces.

### 18.4 Consistency

- ore blocks use the same isometric view and apparent scale;
- map geometry is identical across the series;
- scripts and numerals come from linked vectors;
- paper grain scale is identical;
- colour follows the approved palette;
- shared assets have matching checksums;
- layer names and numbers follow the convention.

### 18.5 Review at several scales

Review every side:

- at full resolution;
- at physical size;
- at 25 percent;
- as a small contact-sheet image;
- in grayscale;
- with the left or right edge partly covered;
- beside all other denominations.

## 19. Delivery manifest

`manifest.csv` records:

- file path;
- denomination;
- side;
- layer number;
- asset type;
- pixel dimensions;
- colour space;
- bit depth;
- source master;
- transformation applied;
- version;
- approval state;
- checksum.

`checksums.sha256` confirms that shared assets are identical wherever reuse is required.

The delivered package is complete only when every manifest entry resolves to an existing file and all twelve layered masters open without missing assets.
