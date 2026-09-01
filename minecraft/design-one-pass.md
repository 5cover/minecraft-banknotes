# One-pass concept validation brief

## Purpose

Generate twelve complete banknote images in one pass per image: one recto and one verso for each denomination.

These images are concept-validation plates. They test the natural-recto and constructed-verso narrative, denomination identity, Minecraft recognition, colour restraint, common layout, and especially whether the twelve notes read as one coherent visual series before final layered construction.

The one-pass workflow deliberately does less than the layered design-package workflow. It does not split reusable assets or attempt deterministic assembly. Its purpose is to test the concept quickly as complete finished-looking plates. Because the images remain flattened, visual consistency between denominations is especially important.

They test the natural-recto and constructed-verso narrative, denomination identity, Minecraft recognition, colour restraint, and common layout before final layered construction.

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

Every note fills its canvas exactly. Use straight edges, no outer paper margin, no rotation, no perspective distortion, no drop shadow, and no surrounding background.

## 2. Common visual direction

The twelve plates must read as one visual family.

The world must be immediately recognisable as Minecraft. Begin from Minecraft itself rather than from an abstract civic scene translated into cubes. Use familiar Minecraft terrain morphology, canonical or near-canonical block textures, recognisable object proportions, characteristic vegetation, ordinary building materials, familiar workstations, and game-native mechanisms.

A useful test is to imagine the banknote frame removed. The central illustration should still read as a carefully composed Minecraft view rather than generic voxel concept art. Rectos may approach the directness of cropped in-game views. Versos may be more ambitious constructions, but they should still be made from recognisable Minecraft objects, mechanics, and building vocabulary.

Do not draw a dark contour around every cube. Adjacent blocks of the same material should often read as continuous surfaces. Cubic construction is communicated through stepped terrain, texture changes, shadows, silhouettes, and material boundaries.

Use a hybrid print treatment. Preserve Minecraft textures and forms, then add restrained banknote linework, paper tone, guilloche, subtle overprint, and selective engraving. The monetary treatment should frame and integrate the Minecraft world rather than repaint the whole scene into historical engraving.

Use mildly saturated denomination colours. The note should look printed rather than backlit.

Use Minecraft typeface lettering for the large denomination and for `EURO ΕΥΡΩ ЕВРО`. Do not use a generic sans-serif face and do not invent extra text.

The European flag, euro scripts, map, and signature field must appear integrated into the note.

Describe a consistent silhouette, projection, orientation, relative scale, and print treatment for every common component in the prompt for each of the twelve images.

### 2.1 Series consistency

Consistency is a primary requirement of the one-pass workflow. The twelve images are generated separately, but they should look as though they belong to one designed series.

Maintain broadly the same across all denominations:

- Minecraft texture sharpness and sampling;
- apparent block scale and object legibility;
- lighting naturalism;
- edge treatment;
- level of environmental detail;
- density of banknote ornament;
- amount of selective engraving;
- paper and print character;
- saturation restraint;
- typography system;
- institutional-field treatment;
- ore-label treatment;
- overall seriousness and finish.

Do not let one denomination become smooth voxel art, another become painterly fantasy, another become heavily engraved, and another resemble a raw game screenshot. Differences should come from the denomination subject, palette, terrain, and scene structure, not from a change of rendering style.

When the generation system permits image references, use one or more successful earlier plates as visual references for later plates. Use them to preserve texture behaviour, detail density, print treatment, and overall visual grammar, not to copy their composition.

Before moving from one denomination to the next, compare the new plate with the existing series. Correct style drift rather than accepting a locally attractive image that breaks the family.

## 3. Common recto composition

Use the same broad proportional arrangement for all six rectos. Exact coordinates do not need to be identical in the one-pass workflow, but the overall balance of value field, scene, ore label, and institutional field should remain visibly related.

The left field contains the large denomination numeral, a smaller repeated value, the euro symbol, and a quiet patterned background.

The centre contains one coherent natural Minecraft landscape. It is a landscape, cave, ravine, or exterior formation viewed from a single camera position. Do not combine a perspective landscape with a geological cutaway or expose invisible underground layers.

The scene should preserve the directness of an in-game Minecraft view. Canonical terrain, texture scale, lighting, water, vegetation, cave behaviour, and visible ore should remain legible enough that the central scene would still read as Minecraft without the surrounding currency design.

The ore label is offset to the right, near the transition between landscape and institutional field. It is circular, near-white, softly tinted with the denomination colour, and approximately the same size relative to note height on every recto.

Inside the label, centre one canonical isometric ore block at the same apparent size and angle on every denomination.

The label contains no ore name, no explanatory text, no second block, no use symbol, no arrow, no orbiting icon, and no material-state sequence.

The right field contains the flag, `EURO ΕΥΡΩ ЕВРО`, one consistent Europe map, signature reservation, and secondary value.

Recto borders use abstract material rhythm only. Do not add minecarts, furnaces, tools, books, wheels, lamps, or other future uses to recto strips.

## 4. Common verso composition

Use the same broad value-field, constructed-scene, and institutional-field structure for every verso.

Each reverse has one dominant Minecraft-native subject. Supporting uses remain visible, but they are subordinate to that subject. The note should be recognisable by its principal form before small details are inspected.

Use an elevated oblique viewpoint across the series, but keep the camera close enough that canonical blocks, workstations, rails, redstone components, bookshelves, villagers, storage, and other game objects remain identifiable. Avoid distant whole-city panoramas that force the model to invent large amounts of generic voxel architecture.

The central image is one integrated constructed Minecraft environment. Material uses must be understood from recognisable game objects, buildings, machines, transport, streets, interiors, agriculture, study, exchange, and public life.

Do not begin from an abstract European institution and then turn it into cubes. Begin from Minecraft nouns and actions, then arrange them so the scene carries the denomination concept.

Do not add a recipe panel, arrowed stages, row of application icons, lower strip of transformations, or mandatory line running across the note.

Rails, roads, wiring, and water channels may appear naturally inside the depicted environment. They must not become explanatory overlays.

Keep figures small. Civilisation and its systems are the subject.

## 5. Denomination directions

### 5.1 €5 coal recto

Show a canonical Minecraft mountain landscape with a broad exposed stone cliff, alpine grass blocks, small flowers, restrained snow, distant block mountains, and a naturally visible seam of canonical coal-ore blocks on the cliff face.

Do not show through the mountain. Do not depict a crust or mantle section. Do not outline every stone cube.

Use graphite grey, limestone, charcoal, muted alpine green, and very limited warm accents.

The pale label contains one canonical coal-ore block.

### 5.2 €5 coal verso

Show a large Minecraft furnace and smelting complex as the dominant subject.

Build it from recognisable furnaces, blast furnaces, hoppers, chests, minecarts, rails, anvils, smithing areas, fuel storage, stone, brick, and iron. Repeated furnace mouths, loading bays, hopper banks, and rail intake should make the note identifiable as the furnace note.

Minecarts bring coal into the complex. Iron ore enters through a separate intake. Finished metal supports a limited number of nearby workshops, bridge works, and station structures.

Keep the surrounding settlement subordinate. Do not turn the scene into a general industrial fantasy city.

Integrate limited smoke into the sky and print texture. Include a restrained area of repaired ground and replanted vegetation.

Do not include a transformation strip or row of use icons.

### 5.3 €10 redstone recto

Show a canonical Minecraft deepslate cavern with a naturally visible redstone-ore vein, water, dripstone, and restrained distant lava.

Use canonical deepslate and redstone textures. Avoid fantasy cave architecture and continuous cube outlines.

Use oxidised red, burgundy, deepslate, pale rose-grey, and very limited powered-red accents.

The pale label contains one canonical redstone-ore block.

### 5.4 €10 redstone verso

Show a large Minecraft redstone automation and logic build as the dominant subject.

Use recognisable redstone dust, torches, repeaters, comparators, observers, pistons, lamps, note blocks, hoppers, doors, rails, sorting systems, and controlled mechanisms. Open façades, roofless sections, or transparent areas may reveal the machinery.

An automated farm, item sorting, controlled doors, rail signalling, lighting, and a compact teaching or testing area may appear as secondary applications connected to the central build.

Keep the architecture straightforward and Minecraft-native. Do not turn the logic hall into a fantasy technology palace.

Distribute the systems through one coherent environment rather than arranging them as a circuit diagram or ordered list.

### 5.5 €20 lapis lazuli recto

Show a broad canonical Minecraft stone cavern with a modest natural lapis-ore deposit, water descending along one wall, a shallow pool, pale stone, and cool grey rock.

Use weathered ultramarine, slate blue, parchment, cool grey, and limited deep-blue ore accents.

The pale label contains one canonical lapis-ore block.

### 5.6 €20 lapis lazuli verso

Show a large Minecraft library and enchanting complex as the dominant subject.

Begin with recognisable bookshelves, lecterns, enchanting tables, maps, item frames, chests, desks, glass, familiar stone and wood, stairs, slabs, courtyards, and visible work areas. The scene should first look like an ambitious Minecraft learning build, not a fantasy university translated into blocks.

A central library hall or courtyard anchors the image. Pigment preparation, bookbinding, map work, teaching, observation, restoration, and enchanting occupy subordinate spaces.

Treat enchanting as accumulated knowledge improving practical capability rather than as glowing fantasy spectacle.

Do not force every cultural use into the scene. Prefer a smaller number of strong Minecraft-native elements with clear relationships.

### 5.7 €50 copper recto

Show a canonical Minecraft dripstone cave or weathered stone chamber with a broad copper-ore vein, granite, pointed dripstone, shallow water, raw copper formations, warm grey rock, orange mineral points, and restrained green staining near moisture.

Use aged copper, umber, warm paper, and limited verdigris.

The pale label contains one canonical copper-ore block.

### 5.8 €50 copper verso

Show a major Minecraft bridge and public-service span as the dominant subject.

Build it from recognisable stone, brick, copper blocks in several oxidation states, rails, water channels, stairs, slabs, fences, lamps, lightning rods, service paths, and compact maintenance buildings. The long span should make the note identifiable as the infrastructure note.

Transport, water, lighting, and maintenance functions run through or alongside the span. Smelting or preparation areas may occupy one approach. Keep the surrounding settlement limited and subordinate.

Use visible orange-to-green copper ageing across roofs, housings, and exposed sections. A spyglass or archaeological brush may appear as small secondary canonical objects.

Do not expand the scene into a generic city merely to include every historical use of copper.

### 5.9 €100 emerald recto

Show a high canonical Minecraft mountain landscape with snow, sparse grass, clouds, pale stone, a steep valley, and one naturally exposed emerald-ore block on a visible cliff surface.

Use mineral green, forest green, pale mint-grey, stone, and limited bright emerald accents.

The pale label contains one canonical emerald-ore block.

### 5.10 €100 emerald verso

Show a developed Minecraft villager market square as the dominant subject.

Use recognisable villagers of several professions, profession workstations, a bell, stalls, paths, farms, wells, storage, workshops, houses, and visible exchanges. The scene may be more deliberate than a naturally generated village, but it should remain clearly derived from Minecraft village vocabulary.

Farms, a library, cartography, masonry, smithing, storage, repair, roads, and meeting spaces connect to the square but remain secondary. Emeralds circulate through visible villager trading relationships.

Do not use trade-interface boxes, floating offer cards, symbolic scales, or a barter timeline.

Do not turn the square into a generic medieval fantasy bazaar.

### 5.11 €200 gold recto

Show a canonical Minecraft badlands landscape with layered terracotta mesas, ravine, sparse vegetation, eroded pillars, and naturally exposed gold ore on a visible stone surface.

A distant abandoned mineshaft may appear, but do not expose the interior of the entire mesa.

Use antique gold, ochre, cream, terracotta, dark brown, and limited bright-gold accents.

The pale label contains one canonical gold-ore block.

### 5.12 €200 gold verso

Show a fortified Minecraft reserve and storage complex as the dominant subject.

Build the scene from recognisable gold blocks and ingots, chests or barrels, secure storage rooms, powered rails, minecarts, clocks, a beacon, furnaces or smithing areas, brewing stands, golden apples, and a controlled Nether portal.

These elements should collectively imply a treasury or reserve institution. Do not begin with a monumental bank or palace and merely render it in blocks.

Powered rails connect storage to transport. Clocks and observation support coordination. Brewing equipment and golden food provide a limited treatment layer. The beacon forms a clear vertical accent attached to the reserve complex.

A balanced piglin exchange area may appear near the portal, but it remains subordinate to the reserve complex.

Keep the supporting civic environment compact. Suggest gold's wider meanings through a few strong canonical uses rather than an entire fantasy city.

## 6. Final one-pass check

Before returning the twelve images, verify that:

- every canvas has the exact listed dimensions;
- every note reaches the image edge without an outer margin;
- all edges are straight and parallel to the canvas;
- all rectos are landscapes rather than cutaways;
- every ore label contains only one canonical ore block;
- every ore block uses the same apparent size and isometric view;
- no recto contains use pictograms;
- no verso contains a recipe strip, arrows, or a forced process band;
- Minecraft is recognised through textures, terrain, objects, and mechanics rather than continuous cube outlines;
- no image resembles a generic voxel-fantasy game;
- all twelve plates share the same broad rendering language, texture sharpness, edge behaviour, lighting naturalism, and level of detail;
- no denomination drifts into a different illustration style;
- rectos and versos remain recognisably Minecraft even when the banknote frame is mentally removed;
- colours remain mildly saturated;
- map geometry and institutional placement remain consistent;
- all required lettering uses the same Minecraft-derived pixel system;
- there is no HUD, inventory, crosshair, game logo, pseudo-text, or photographic background.
