# Crafting Europe banknote design package

This package contains twelve one-pass concept-validation plates: one recto and one verso for each of the €5, €10, €20, €50, €100, and €200 denominations.

## Contents

- `images/`: the twelve final PNG plates at the exact dimensions specified in the brief
- `contact-sheet.png`: a labelled overview of the complete series
- `generation-prompts.md`: the production prompt system and denomination directions
- `manifest.json`: denomination, side, motif, function, palette, and dimensions
- `SHA256SUMS.txt`: file-integrity hashes for the twelve plates
- `briefs/`: copies of the supplied one-pass brief and proposal

## Series logic

| Value | Natural material | Constructed-world function |
| ---: | --- | --- |
| €5 | Coal | Energy |
| €10 | Redstone | Automation and information |
| €20 | Lapis lazuli | Knowledge and culture |
| €50 | Copper | Infrastructure |
| €100 | Emerald | Exchange and trust |
| €200 | Gold | Reserve and continuity |

The fronts present each material in a natural Minecraft setting. The backs show a Minecraft-native civic or technical system shaped by its use. A stable value field, institutional field, Europe map, flag treatment, pixel-derived typography, printed-paper texture, and restrained banknote ornament connect all twelve plates.

## Production note

These are flattened concept plates produced for visual validation, not layered production artwork or legal tender. Image-generation systems can approximate multilingual display type but do not provide typographic source files; all official lettering, stars, maps, signatures, serial areas, accessibility devices, and security features should be rebuilt as controlled vector artwork before any later production stage.

## Image-generation mode

The plates were created with the built-in image-generation workflow. One targeted text correction was requested for the €5 front while preserving the rest of that plate. Final images were then normalized to the exact pixel dimensions in the supplied brief.

