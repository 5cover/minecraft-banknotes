# Reproducible layered design package

## Purpose

This document defines a reusable workflow for producing a banknote series from specialized generated imagery, reusable assets, and deterministic composition. It applies to any series proposal using the same production approach.

The series proposal is authoritative for the theme, visual language, motifs, sides, denominations, image contents, palette, typography, recurring identifiers, institutional treatment, exclusions, reference images, and exact final output dimensions. This workflow does not define or override any of them.

The package should be a self-contained design kit that preserves selected intermediates, keeps useful elements swappable, creates the final flattened designs through Python, and permits rebuilding without manually reconstructing the compositions in an image editor. It is not an archival or print-manufacturing specification.

## Core principles

1. Separation is technical, not aesthetic. An isolated layer may be dense, irregular, highly authored, and visually dependent on other layers. A transparent file is not an instruction to make a sterile overlay.
2. Specialize generation. The primary imagery and the monetary artwork have different jobs. Generate them separately so each can receive the model's full attention.
3. Design downstream layers in context. Generation order is explicit. Later work sees the actual approved upstream work and accurate proxies for assets that will be placed afterward.
4. Merge genuinely mutual generative responsibilities. If the series has a recurring decorative field or identifier whose form needs to interlock with nearby ornament, generate that empty field together with the monetary artwork. Keep any supplied inset object separate.
5. Reuse stable assets. Supplied and approved typography, symbols, maps, identifiers, illustrations, and other recurring elements should not be repainted in every generation.
6. Compose deterministically. Layout, cropping, masking, scaling, display treatment, layer order, and output dimensions belong to configuration and Python, not to repeated image-model interpretation.
7. Preserve a family without imposing cloned decoration. Common hierarchy and visual grammar coexist with the variations specified for each denomination or side.
8. Optimize for a convincing finished note and useful editing, not for maximum layer count or an imitation of a professional print archive.

## 1. Project contract and output specification

Read the series proposal and inspect all supplied assets before generating imagery or choosing a layout. Extract the relevant instructions into `layout.yaml` and a short `README.md`. Do not silently substitute a generic banknote design for an underspecified proposal.

The proposal or an accompanying project brief must establish, for every required design:

- denomination or other identifier, side, and exact export filename;
- final canvas width and height, or exact dimensions from which they can be derived without guesswork;
- primary imagery and its role;
- recurring motifs and which parts are separable assets;
- palette, print language, typography, institutional information, and exclusions;
- fixed series elements and permitted denomination-specific variation.

If a required filename, output size, essential asset, or defining visual instruction is missing, resolve it from the supplied project material or request the missing information rather than inventing a supposedly authoritative value.

Do not hard-code the number of denominations, physical formats, named scripts, or a recurring badge type into this workflow. Build exactly the designs specified by the active proposal.

Unless the project specifies otherwise, final note PNGs contain the straight, full note to the canvas edge, without a mockup background, skew, photographic surroundings, or an outer presentation margin. Output dimensions must match the proposal exactly.

## 2. Deliverable contents

The completed package must include:

- this workflow file and the actual series proposal used;
- a short `README.md` containing the exact build commands and dependencies;
- `layout.yaml` and a lightweight `generation-record.yaml`;
- the Python scripts actually used to make the final files;
- all supplied source assets that can be included in the package, and portable approved derivatives for any input that cannot be redistributed;
- all approved generated imagery and monetary-artwork intermediates consumed by the build;
- the contextual composite for each monetary-artwork generation, plus its generation instructions and input references;
- edited source assets and a record of changes, where applicable;
- final flattened PNGs at the exact project dimensions;
- at least one contact sheet for reviewing the series.

Store intermediates in useful original and approved forms where changes were made. Do not duplicate every asset as a large full-canvas raster merely because such a copy could be generated.

A recorded prompt and seed do not guarantee byte-for-byte reproduction of an image-model output. Reproducibility means that the selected generated pixels are retained, transformations are documented, and the final notes can be built deterministically from the approved files. Preserve prompts and reference inputs to make creative regeneration possible, but do not describe it as deterministic.

## 3. Simple project structure

A typical package is:

```text
README.md
design-package.md
[series-proposal].md
layout.yaml
generation-record.yaml
scripts/
    build_type_assets.py       # only if type conversion is needed
    build_contexts.py
    build_notes.py
    build_contact_sheets.py
assets/
    supplied/
    approved/
    derived/
    masks/
generated/
    primary/
    contexts/
    monetary_artwork/
outputs/
    notes/
    contacts/
    layer_previews/          # optional, produced on demand
```

Add folders only when the project uses them. The tree distinguishes source assets, approved or derived assets, generated components, contextual references, scripts, and finished outputs. No CSV manifest, checksum bureaucracy, nested archives, obligatory bleed/print masters, or unused output formats are required.

Use names that combine the project's design identifier, side, and component, for example `NOTE_A_recto_primary.png`, `NOTE_A_recto_context.png`, and `NOTE_A_recto_artwork.png`. Final export filenames must use the project specification, not these illustrative names.

## 4. Supplied assets and stable derivatives

Inspect every supplied asset. Identify whether it is a reusable source, a per-design insert, a font, a vector symbol, a mask, or an example/reference image. Preserve the original as appropriate and use one approved project version throughout the series wherever common geometry is required.

### 4.1 Raster inserts

If the proposal uses a recurring object inserted into an empty artwork field, retain the supplied raster as a separate asset. Place it deterministically after the artwork is generated. Do not ask the image model to repaint it as part of the primary imagery or monetary artwork.

If paper integration or colour adaptation is necessary, derive a display version non-generatively and retain its original. Any shared scale, pose, cropping, or lighting requirements come from the proposal.

### 4.2 Vector assets

Prefer SVG for reusable maps, symbols, illustrations, lettering outlines, and other geometry that benefits from resolution-independent scaling. Retain the original and any approved edited version separately. Record permitted changes and the exact derivative used for final composition.

The proposal determines which assets must retain exact geometry and which may be edited. Do not independently loosen a project's geometry requirements. A single approved shared asset should not be redrawn independently for each denomination.

### 4.3 Typeface and lettering assets

If a font is supplied, use it as a construction input rather than relying on the recipient's installed fonts or unresolved SVG `<text>` elements. Generate approved strings and numerals as outlined SVG paths, with optional compact raster previews, when that is compatible with the typeface and project requirements.

Check that the supplied font actually contains every required glyph. Do not silently substitute characters or a different typeface when it does not. Use approved supplementary lettering or supplied outlines for missing forms and document the choice.

Where a proposal requires a multi-line or multi-script block, construct it as one grouped asset with intentionally matched optical size, weight, spacing, and ordering. Place the group as one object unless the design specifically requires independent lines.

A script such as `build_type_assets.py` should recreate the outlined assets from the permitted source inputs. The final note builder should use the outlines or their controlled rasterizations rather than live font rendering. Keep deliverable assets portable even when the source font cannot be redistributed.

### 4.4 Deterministic display treatment

Shared assets may receive documented palette fills, opacity, paper interaction, restrained overprint, clipping, or texture treatment so they belong to the note rather than appearing pasted on. Preserve any exact institutional or identity-critical geometry.

Display treatment must be repeatable and must not become an excuse to generate the same stable object anew on every note.

## 5. Generative decomposition

The default workflow separates two principal generated components per required design.

### 5.1 Primary imagery plate

This plate carries the main image or scene defined by the proposal. Its generator concentrates on the series-specific visual language, subject fidelity, composition, depth, lighting, texture, and detail. It does not need to solve monetary ornament or render stable institutional assets.

It may be a landscape, constructed environment, portrait, symbolic image, or another kind of principal imagery. The proposal determines its content and visual rules; this workflow imposes no subject matter of its own.

### 5.2 Monetary-artwork plate

This plate contains the designed currency surface around and, where appropriate, over the primary imagery. Depending on the proposal, it can include borders, denomination-specific patterns, background fields, fine ornament, transitional textures, irregular incursions, quiet-but-designed regions, and an empty recurring identifier field.

It is not a generic frame. It is a sophisticated visual composition created in relation to the approved primary imagery. It excludes the primary imagery pixels and any stable objects that will be inserted deterministically.

If a proposed identifier and its surrounding ornament have a mutual visual dependency, generate them in the same monetary-artwork plate. Do not create separate image-model steps merely to keep them technically isolated when they need one shared visual decision. Conversely, do not invent a badge or identifier for a series that does not call for one.

### 5.3 Additional components only when useful

Add another generated layer only if it has a clear independent editing benefit and a workable dependency order. Do not split the artwork into many nominal panels or line systems simply to increase the number of files.

## 6. Generation order and dependencies

The default production order is:

```text
proposal + supplied assets + series references
                    ↓
        layout and asset proxies
                    ↓
          primary imagery
                    ↓
      approve crop and placement
                    ↓
          context composite
                    ↓
   context-aware monetary artwork
                    ↓
  approved deterministic asset versions
                    ↓
       Python composition + export
                    ↓
            series review
```

Asset preparation and layout planning may happen before primary generation. Deterministic insertion happens after the monetary artwork is approved, even though its future position is shown to the model through proxies.

The graph should be acyclic during a build. A downstream plate may respond to approved upstream pixels. An upstream plate should use a proxy rather than depending on unfinished downstream art. If two generated elements genuinely need to determine each other's shape at once, consider merging those generative responsibilities while keeping stable inserts separate.

Replacing an upstream plate may require review or regeneration of the dependent artwork. Replacing monetary artwork alone does not require rerendering the approved primary plate. Changing only deterministic assets or coordinates should not require image generation.

## 7. Centralized layout and proxies

Use `layout.yaml` as the single source of truth for every final canvas. The layout controls:

- design ID, side, export filename, width, and height;
- approved primary-image crop, fit mode, scale, and offset;
- broad image aperture or clipping mask where used;
- fixed asset boxes or centres, sizes, and alignment;
- footprint of an empty identifier field, if the series has one;
- quiet zones and any no-paint exclusions that are genuinely needed;
- z-order, masks, and deterministic display treatments.

Coordinates may be in final pixels or normalized proportions, but the file must state which. Scripts must resolve them reproducibly. The proposal may define common proportional rules; `layout.yaml` records the actual values used by the build.

Do not freeze every edge of the generated artwork in YAML. The generated monetary-artwork plate may have irregular boundaries, designed overlap, and denomination-specific ornament. Control the stable framework and reserved asset positions, not every decorative contour.

### 7.1 Proxy context

Before monetary-artwork generation, create a temporary context composite showing the approved, positioned primary imagery and accurate proxies for elements to be inserted afterward. Use silhouettes or intentionally simple boxes rather than pretending that placeholders are final artwork.

A proxy should communicate visual occupancy, not demand an empty rectangular panel. Quiet zones can retain pattern, paper tone, and ornament so long as the eventual asset remains legible. The proxy itself must not be copied into the final artwork plate.

Protect only what needs protection: critical text, identity symbols, and other project-defined elements. Decorative artwork may weave behind or around those objects when masking and layer order make the result deliberate.

## 8. Primary imagery generation

Generate the primary plates separately from monetary artwork, following the active proposal. Allow reasonable overscan where the output method permits it so crop and scale can be adjusted afterward.

Across the series, maintain the same visual grammar as specified by the proposal. Compare approved plates side by side for rendering medium, apparent detail scale, texture treatment, edge behavior, lighting, depth, atmospheric handling, tonal range, saturation, and overall density. Do not allow one denomination to drift into a new illustration style simply because its subject is different.

The project may permit variation in camera, scene complexity, time of day, or palette. Preserve that intended variation. Consistency does not mean identical framing, lighting, ornament, or density regardless of narrative.

Avoid embedding stable typography, institutional symbols, repeated identification objects, or final note ornament inside the primary plate when they are to be inserted elsewhere. Apply the proposal's subject-specific exclusions rather than a fixed theme-specific exclusion list from this workflow.

Keep selected source output and the approved corrected plate when they differ. Record reference images and generation instructions sufficiently to explain how the chosen intermediate was made.

## 9. Approve the image crop

Before designing monetary artwork:

1. select the primary plate for each design;
2. decide its final crop, scale, placement, and any mask;
3. record the placement in `layout.yaml`;
4. render a full-canvas positioned preview;
5. review the preview as part of the complete series;
6. freeze this positioned state as the input to downstream generation.

The monetary-artwork generator must respond to this actual approved image placement, not solely to its text prompt.

## 10. Context-composite construction

Use `build_contexts.py` to render one context image for each monetary-artwork plate. Include the approved positioned imagery, note boundary, and proxies for fixed assets and proposed recurring identifiers. Include clipping/aperture information only where it helps the design.

Contexts are generation inputs, not final output layers. Save the actual contexts used. They support repeatable project review and reveal which scene placement the monetary artwork was designed around.

The context should not accidentally suggest notebook ruling, visible grids, generic frames, or blank component slots as the desired decoration. Distinguish clear planning marks from examples of finished artistic treatment in the accompanying generation instruction.

## 11. Monetary-artwork generation

Generate one monetary-artwork plate for each required design against its own approved context composite. The generator may see the complete current composition, but its output must contain only the monetary artwork it is responsible for.

The artwork may respond to the main image's silhouettes, tonal masses, edges, openings, geometry, and narrative. It may echo forms, transition irregularly across scene boundaries, vary local detail, weave behind asset positions, and create designed quiet zones. Its technical isolation must not make it visually neutral or simplistic.

Use the proposal's border logic, emblem or identifier treatment, palette, density goals, and denomination differences. Do not invent a universal recolored template unless the proposal actually calls for one. Use strong approved design references as visual guidance when available, while generating the requested isolated component rather than copying text or institutional assets from the reference.

If an empty recurring identifier is part of the artwork, integrate its shell and surrounding ornament in this same generation. Keep the space for its later inserted object clear, but do not require every denomination to use an identical decorative shell unless specified.

Do not generate visible planning marks, guide grids, placeholder panel borders, fake interface controls, unreadable pseudo-text, or other artifacts of the context image. Do not generate assets whose exact forms are supplied for deterministic placement.

Prefer a transparent full-canvas artwork PNG. If transparency is not reliably available, use a documented method to isolate artwork cleanly, retain the source, and inspect the resulting alpha edges. Do not merely assert that a fully opaque note-like render is an isolated component.

## 12. Approved assets and final integration

After artwork approval, generate or prepare portable derivatives of the stable assets and place them using `layout.yaml`. Use the project's actual asset list. Examples might include typographic groups, numerals, symbols, maps, recurring inset imagery, signature fields, or other institutional elements.

A fixed asset may have a consistent shared geometry with project-specific colour or print treatment. Maintain legibility and visual integration. If any fixed asset appears too small, visually foreign, awkwardly positioned, or in collision with ornament, fix its source, display treatment, mask, or YAML placement before asking the image model to regenerate an unrelated layer.

## 13. Python construction scripts

Provide scripts that actually build the delivered notes; do not include empty template code presented as a functioning build.

Suggested responsibilities:

- `build_type_assets.py`, only if needed: read source fonts or letterforms, generate portable approved outlines and previews, report missing glyphs rather than substituting silently.
- `build_contexts.py`: read configuration, position approved primary images, draw proxies, and export the exact contexts used downstream.
- `build_notes.py`: read configuration, crop and position primary imagery, composite the monetary artwork, rasterize vector assets at target resolution, place stable elements, apply documented masks and treatments, and flatten each finished PNG.
- `build_contact_sheets.py`: generate simple series-wide review sheets from the actual finished exports.

Use documented, installable Python dependencies. A basic `requirements.txt` is useful when it contains only libraries the scripts really use. All file paths should be relative to the package root; builds should not depend on a developer's absolute local paths.

The scripts must use deterministic placement and compositing. They should fail clearly when a required file is missing or a final canvas has the wrong dimensions. Do not silently substitute an empty layer or an unrelated asset.

## 14. YAML and generation record

Keep configuration small. `layout.yaml` records final dimensions, approved crops, assets, positions, masks, z-order, and required treatments. `generation-record.yaml` records selected source and approved generated images, the context used for each monetary-artwork plate, upstream dependencies, relevant generation instructions, and approved asset edits.

The record should make it possible to answer: “Which primary image and context was this artwork designed against?” It need not become a comprehensive asset-management database.

The proposal supplies the visual rules. Do not copy the full narrative, denomination descriptions, or visual exclusion lists into YAML merely to give them a machine-readable appearance.

## 15. Final flattening and full-canvas support

Use a documented, project-specific layer order. A typical default is:

1. positioned primary imagery;
2. monetary artwork, including any empty decorative identifier field;
3. separately inserted recurring motif or object, if used;
4. values and inscriptions;
5. institutional symbols and other fixed assets;
6. optional common print treatment, if actually part of the design.

The precise order and any over/under masking must be recorded. An ornamental line must not accidentally cover the legible content of a later asset. Intentional overlaps can be retained when the final result reads correctly.

Export final flattened PNGs directly through Python at the exact configured sizes. Do not rely on manual Paint.NET composition to produce the authoritative final files.

Support an optional full-canvas placed-layer export for a selected design or the whole series. These transparent PNGs should have the final canvas dimensions and already-correct positioning, making them convenient for editor inspection. Their compact source masters remain separately stored, and the large preview copies need not be bundled for every layer unless requested.

No `.pdn`, PSD, TIFF, PDF, bleed master, nested layer ZIP, or additional proof format is mandatory.

## 16. Quality control

Review the finished series as actual notes, not merely as a directory of valid files.

Check:

- every required design exists and its filename and pixel dimensions match the project specification;
- scenes belong to the intended common visual language, without unapproved stylistic drift;
- generated monetary artwork is rich and integrated rather than a generic visible scaffold;
- denomination-specific variation is preserved where the proposal calls for it;
- fixed assets are legible, correctly scaled, correctly grouped, and materially integrated;
- recurring asset geometry is identical where the proposal requires it;
- masks, alpha edges, crops, and layer order create no accidental collisions or seams;
- the final notes do not look like a collage of otherwise competent components;
- the final PNGs can be rebuilt from the delivered intermediates and scripts;
- the generation record identifies the approved upstream image and context for each dependent plate.

Check contact sheets as well as full-size notes. Where useful, inspect with primary imagery alone, monetary artwork alone, fixed assets alone, and the final composite to identify which layer causes a defect.

## 17. Editing and iteration

Change the component responsible for a defect:

- primary image wrong: replace it, approve a new crop, rebuild the context, then review or regenerate dependent artwork;
- monetary artwork weak or poorly integrated: replace that plate without changing the approved primary imagery;
- recurring object wrong: replace its approved asset;
- typography, symbol size, or placement wrong: update the asset or YAML and rebuild;
- small crop error: update scene scale or offset, then check whether the dependent artwork still fits.

Swappability does not mean visual independence. A replacement primary image can invalidate artwork that was designed around its silhouette. The files remain separate so that changes can be selective, visible, and controlled.

## 18. Minimum completion criterion

A package is complete when the reviewer can inspect the source and generated components, understand the dependency order, run the documented scripts, and immediately view all required finished note PNGs without reconstructing them by hand.

Preserve the sophistication of the design, but keep the production machinery no more complicated than the design requires.
