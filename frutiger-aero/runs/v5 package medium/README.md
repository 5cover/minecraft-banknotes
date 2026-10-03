# Living Systems

Twelve banknote concept designs implementing proposal Version 5: Infrastructure, Communication, Mobility, Interpretation, Environment and Future. The final output sizes follow the user's authoritative table, including the €100 and €200 proportions that supersede the approximate ratios in the proposal.

Open `outputs/contacts/Living_Systems_contact_sheet.png` to review the series. The twelve final, flattened RGB PNGs are in `outputs/notes/`.

## Build

Python 3.10 or later is required. From this package directory:

```bash
python -m pip install -r requirements.txt
python scripts/build_notes.py
python scripts/build_contact_sheets.py
```

The build uses retained generated pixels and portable approved assets; it requires no image service, network access, or installed system fonts. `requirements-lock.txt` records the versions used for the delivered exports.

To rebuild the stable lettering, flag and map derivatives from the bundled source font and geographic data:

```bash
python scripts/build_assets.py
```

To regenerate the exact scene-placement contexts and approved monochromatic artwork derivatives from the saved artwork sources:

```bash
python scripts/build_contexts.py
python scripts/isolate_artwork.py
python scripts/build_notes.py
python scripts/build_contact_sheets.py
```

To inspect the already positioned transparent layers for one note:

```bash
python scripts/build_notes.py --design EUR100_verso --layers
```

Layer previews are written to `outputs/layer_previews/EUR100_verso/`. Omit `--design` to export the full series. They are optional rebuild products rather than additional master files.

## Composition and editing

`layout.yaml` controls dimensions, source crop, placement, palette translation, quiet-field fade, artwork opacity, protected fields, and layer order. Objects with stable identifiers are records keyed by those identifiers.

The primary image is cropped with uniform scaling to cover the exact canvas. Its luminosity is translated into the denomination's shadow, midtone and paper colors. A smooth paper-tone field protects the monetary rail. Separately generated monetary artwork follows, then outlined numerals, the grouped EURO / ΕΥΡΩ / ЕВРО inscriptions and the shared flag or map asset.

Monetary artwork is generated against the saved context for that individual note. The source plate contains no primary scene or fixed institutional artwork. Its white matte is removed by multiplying inverse luminance with source alpha, then applying the recorded density gain, denomination ink and configured opacity. This retains antialiased edges and genuine transparency. The source and approved derivative are both retained.

The Greek and Cyrillic characters are real glyphs from the bundled font. The portable lettering consists of outlined SVGs and compact controlled rasterizations. Equal cap heights and one grouped placement give the three scripts equal authority. DejaVu Sans supplies the prototype letterforms, with explicit tracking and optical placement; this is not a newly drawn complete typeface.

The map uses one fixed geographic silhouette and projection for all six reverses. Denomination-specific interior line treatments are clipped to that same mask. The flag retains its blue rectangle and twelve upright yellow stars. Signature, serial and tactile areas are reserved for later controlled work; no invented signature, serial number or technical security feature is included.

Changing a numeral, inscription, palette, opacity or asset placement is deterministic. Replacing a primary scene requires reviewing its dependent monetary artwork. Image generation itself is not deterministic; the preserved selections, rather than prompts or seeds, make the delivered composition reproducible.

## Contents and sources

- `design-package.md` and `proposal-v5.md`: original supplied production workflow and proposal.
- `output-specification.md`: the user's exact final output contract.
- `generation-record.yaml` and `prompts/`: selected plates, dependencies, generation instructions and targeted revisions. Built-in ImageGen was used for all generated scene and monetary artwork.
- `generated/primary/`: selected primary images and source versions retained for targeted revisions.
- `generated/contexts/`: exact downstream generation inputs and the orchestral seating occupancy guide.
- `generated/monetary_artwork/`: source plates and isolated approved layers.
- `assets/approved/`: reusable lettering, European flag and map assets.
- `assets/supplied/`: supplied jury report, source font with license, and geographic source data.
- `scripts/`: the Python code used for the build and contact sheet.

The map derives from the public-domain [Natural Earth 1:110m country geometry](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson), using a fixed European crop, no internal country borders, and consistent equirectangular x/y scales. It is geographic artwork, not an image-model pseudo-map. The bundled source font retains its upstream license in `assets/supplied/font-license.txt`.

These are independent alternative design concepts. The source proposal and jury report are preserved as project material; the package does not represent an issued banknote series or a technical security specification.
