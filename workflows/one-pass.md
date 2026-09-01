# One-pass concept validation brief

## Purpose

Generate twelve complete banknote images in one pass per image: one recto and one verso for each denomination.

These images are concept-validation plates. They test the proposal's recto-verso narrative, denomination identity, colour policy, common layout, visual hierarchy, rendering language, and especially whether the twelve notes read as one coherent visual series before final layered construction.

The one-pass workflow deliberately does less than the layered design-package workflow. It does not split reusable assets or attempt deterministic assembly. Its purpose is to test the proposal quickly as complete finished-looking plates. Because the images remain flattened, visual consistency between independently generated denominations is especially important.

Do not create variants, alternate compositions, or extra exploratory images. Generate exactly the twelve files listed below.

## 1. Output list and exact dimensions

Scaling aspect ratios to a maximum height of 938 pixels.

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

Every note fills its canvas exactly. Use straight edges, no outer paper margin, no rotation, no perspective distortion of the note itself, no drop shadow, and no surrounding background.

## 2. Source of truth

The proposal is authoritative for the design.

This workflow defines how to generate the twelve flattened validation plates. It does not define their theme, scene content, visual movement, recurring motifs, recto-verso relationship, typography, palette, architecture, human presence, print treatment, or denomination-specific imagery unless those requirements are explicitly stated here as production constraints.

Do not import assumptions from another proposal or from a previous use of this workflow. In particular, do not assume that rectos and versos follow any specific narrative pattern merely because an earlier series did.

When the workflow and proposal appear to overlap, use this hierarchy:

1. the proposal governs what the design is;
2. this brief governs how the one-pass validation set is generated;
3. generation defaults are used only where neither document specifies an answer.

Do not use generation defaults to replace a proposal decision with a more familiar or easier visual solution.

## 3. Extract a series contract before generating

Before generating the first plate, read the entire proposal and internally extract a compact series contract.

The contract should capture every proposal rule that must remain stable across independently generated images, including where applicable:

- the conceptual role of the recto and verso;
- the common composition and relative placement of value, narrative, institutional, and reserved fields;
- the dominant visual hierarchy expected on each side;
- the rendering medium and degree of realism or abstraction;
- edge behaviour, texture behaviour, surface finish, and atmospheric treatment;
- the common camera or viewpoint family;
- the level and distribution of detail;
- the colour and saturation policy;
- the relationship between image colour and paper or print colour;
- typography and numeral treatment;
- Europe-map geometry and treatment;
- flag, signature, serial, tactile, and other institutional fields;
- any recurring motif, identifier, frame, border, or anchor;
- the treatment of people or figures;
- proposal-wide exclusions;
- denomination-specific subjects, secondary elements, palettes, silhouettes, and exclusions.

Do not output this contract as an extra artifact. Use it as the fixed generation basis for all twelve images.

The contract is especially important because the images are generated separately. A rule stated once in the proposal must not silently disappear from later prompts.

## 4. Make every image prompt self-contained

Do not rely on conversational memory, the previous image, or the generation model inferring the rest of the series.

Every image prompt must restate all shared visual rules that materially affect that plate, then add the denomination-specific instructions from the proposal.

Shared wording should remain as stable as possible across all twelve prompts. If the proposal defines a common rendering style, institutional layout, map treatment, border language, recurring element, typography system, or print character, describe those elements consistently rather than paraphrasing them differently on each denomination.

The per-image prompt should contain, in substance:

1. denomination, side, filename, and exact canvas size;
2. the side's conceptual role according to the proposal;
3. the dominant subject or organising landscape;
4. the limited supporting elements required by the proposal;
5. viewpoint, framing, scale, and compositional hierarchy;
6. denomination palette and the series-wide colour policy;
7. the shared rendering and surface language;
8. the common banknote composition and institutional elements;
9. any proposal-defined recurring device or fixed element;
10. explicit exclusions relevant to that side and denomination.

Do not shorten later prompts merely because the same rules were used earlier. Repetition is intentional here: it reduces style drift between independent generations.

## 5. Preserve visual hierarchy

A complete scene is not a checklist of everything associated with its concept.

Follow the proposal's hierarchy literally. If it identifies one dominant object, structure, landscape, or spatial proposition, make that element unmistakably primary. If it permits one or two secondary elements, keep them subordinate in scale, contrast, placement, and detail.

Do not add extra objects merely to make the theme more explicit. Do not convert conceptual breadth into visual cacophony.

A viewer should be able to identify the principal scene at thumbnail scale before inspecting supporting detail.

Where the proposal deliberately defines a system through several coordinated elements rather than one object, preserve one dominant organising landscape or compositional order so that the elements still read as one scene.

Maintain proposal-defined quiet zones. Empty sky, water, wall, floor, terrain, paper tone, or other low-density areas are active parts of the composition and should not be automatically filled.

Unless the proposal explicitly asks for them, do not add explanatory arrows, process bands, icon strips, floating labels, diagrams, timelines, interface panels, or decorative symbols that merely restate the concept.

## 6. Recto and verso discipline

Follow the proposal's recto-verso logic exactly.

Do not assume that the verso is simply a larger, busier, more populated, or more detailed version of the recto. If the proposal calls for a change of scale, function, viewpoint, system, context, or conceptual register, make that change qualitative and visible.

The two sides should still belong to one denomination through palette, typography, border logic, institutional treatment, and any proposal-defined formal echoes.

Recto and verso do not need to depict the same physical place unless the proposal says they do.

Do not use a generic solution such as “iconic object on the front, city panorama on the back” unless that structure is actually part of the proposal.

## 7. Series consistency

Consistency is a primary requirement of the one-pass workflow. The twelve images are generated separately, but they should look as though they belong to one designed series.

Maintain broadly the same across all denominations, according to the proposal:

- rendering medium and degree of realism;
- texture sharpness and sampling;
- apparent detail scale;
- lighting naturalism and softness;
- edge treatment;
- atmospheric depth;
- density of environmental detail;
- density of banknote ornament;
- paper and print character;
- saturation restraint;
- typography system;
- numeral treatment;
- institutional-field treatment;
- treatment of recurring components;
- overall seriousness and finish.

Differences should come from the proposal's denomination-specific subject, palette, spatial structure, silhouette, and intentional exceptions, not from accidental changes in illustration style.

Do not allow one plate to become photorealistic while another becomes stylised, one to become painterly while another becomes diagrammatic, or one to become heavily engraved while another behaves like a clean digital render unless the proposal explicitly requires such contrast.

Common components must maintain a consistent silhouette, projection, orientation, relative scale, alignment logic, and surface treatment wherever the proposal defines them as fixed.

## 8. Generation order and visual references

Generate denomination pairs in ascending order unless the proposal defines another dependency:

€5 recto, €5 verso, €10 recto, €10 verso, €20 recto, €20 verso, €50 recto, €50 verso, €100 recto, €100 verso, €200 recto, €200 verso.

The first completed recto and first completed verso establish practical style anchors for the remaining plates. They do not override the proposal; they demonstrate how its shared rules have been realised.

When the generation system permits image references, use one or more earlier plates as visual references for later plates. Use them to preserve rendering language, texture behaviour, detail density, lighting, print treatment, institutional integration, and overall finish, not to copy their denomination-specific composition.

Use recto references preferentially for later rectos and verso references preferentially for later versos when the two sides have intentionally different spatial behaviour.

Before generating each later plate, compare the intended prompt against the existing series contract and the established visual anchors. Resolve likely style drift in the prompt before generation rather than accepting a locally attractive image that breaks the family.

## 9. Proposal fidelity and invention control

The one-pass workflow is a translation task, not an ideation pass.

Do not invent a new motif, architectural type, symbolic device, recurring badge, institution, character, secondary narrative, or visual metaphor because the proposal seems abstract. Use the concrete representation chosen by the proposal.

If a proposal deliberately represents a broad concept through one specific channel, depict that channel confidently rather than encoding every possible meaning of the concept into the scene.

Supporting detail may elaborate the selected scene, but it must remain consistent with the proposal's world, style, period, level of realism, and exclusions.

Where a proposal intentionally keeps institutions or places anonymous, preserve that anonymity. Do not add real-world branding, logos, named organisations, or identifying signage unless requested.

Do not invent readable pseudo-text. Use only lettering the proposal explicitly requires, and treat any other textual texture as controlled non-linguistic detail unless exact text has been supplied.

## 10. Institutional and monetary integration

The result must be a complete banknote plate, not a scene placed inside a decorative frame after the fact.

Integrate the proposal-defined numeral hierarchy, euro scripts, European flag, Europe map, signature reservation, serial reservations, tactile areas, borders, and security-ready zones from the beginning of the composition.

The narrative image remains important, but it must coexist with monetary hierarchy and denomination recognition.

Keep all common institutional elements consistent across the series according to the proposal. Do not redesign the Europe map, flag treatment, script placement, signature field, or common frame independently for each denomination.

Do not simulate finished security technology unless the proposal explicitly requires a visual mock-up of it. Security-ready areas are compositional reservations, not permission to invent holograms, foils, windows, or optical effects.

## 11. One-pass image quality

Each image should look finished enough to judge the concept as a complete note.

Do not leave obvious placeholder panels, rough compositing seams, empty template boxes, undeveloped institutional fields, or unresolved scene boundaries simply because the image is a validation plate.

At the same time, do not solve one-pass uncertainty by adding ornamental complexity. Finish comes from confident hierarchy, coherent rendering, integrated banknote structure, and disciplined detail.

The image should survive two tests:

At thumbnail scale, denomination, dominant colour, principal silhouette, and overall series family should be clear.

At close scale, the proposal-specific scene, materials, structures, small details, border logic, and print or surface treatment should reward inspection without displacing the primary reading.

## 12. Final one-pass check

Before returning the twelve images, verify that:

- exactly the twelve requested files exist and no variants or exploratory images are returned;
- every canvas has the exact listed dimensions;
- every note reaches the image edge without an outer margin;
- all note edges are straight and parallel to the canvas;
- every recto follows the proposal-defined recto role;
- every verso follows the proposal-defined verso role;
- each side has the proposal-defined dominant subject or dominant organising landscape;
- supporting elements remain subordinate rather than becoming an equal-weight catalogue;
- no denomination introduces a motif or scene type absent from the proposal;
- recto and verso are qualitatively distinct wherever the proposal requires them to be;
- all twelve plates share the same proposal-defined rendering language, texture behaviour, edge treatment, lighting family, detail scale, and level of finish;
- no denomination drifts into a different illustration or rendering style without an explicit proposal reason;
- colour follows both the denomination palette and the series-wide saturation or hue policy;
- map geometry and other fixed institutional components remain consistent;
- all required lettering follows the same proposal-defined typography system;
- recurring devices, when present, retain consistent scale, orientation, placement logic, and treatment;
- no unrequested labels, arrows, icon strips, interface graphics, logos, pseudo-text, or explanatory diagrams have been added;
- there is no surrounding photographic background, drop shadow, presentation surface, skew, or perspective distortion of the note;
- each plate reads as part of the same banknote series before close inspection.
