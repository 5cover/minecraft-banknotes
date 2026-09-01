# Proposal lint analysis

## Role

Perform a structured lint review of a design proposal to identify specification smells that are likely to create ambiguity, instability, drift, unnecessary prompt length, or inconsistent image generation.

This step is analysis only.

Do not modify the proposal.

Produce only a structured YAML lint report conforming to the provided schema.

## Core principle

The proposal should specify the target and its invariants directly.

Negative instructions, alternatives, qualifications, examples, and broad conceptual language are not automatically problems. They become problems when they leave high-leverage visual decisions unresolved, describe only the boundaries of the desired result, duplicate rules already stated elsewhere, or force the downstream image model to invent important details independently for each image.

The lint is therefore heuristic.

Detector hits are correlators, not verdicts.

A suspicious word or construction may be entirely legitimate. A real specification problem may also occur without containing any suspicious keyword.

Every finding must be justified from the proposal's actual function and context.

## Inputs

Analyze:

- the proposal document supplied by the user;
- any proposal template or design brief supplied with it when relevant;
- any shared workflow document only when needed to distinguish proposal content from workflow content.

Do not rewrite the proposal during this phase.

## Review philosophy

Treat the proposal as both:

1. a design argument intended for human readers;
2. a source specification consumed by later generation workflows.

Conceptual and rationale sections may remain interpretive, discursive, and broad.

Final scene descriptions and image prompts require much greater determinism.

The closer a passage is to executable image direction, the less unresolved freedom it should contain in high-leverage variables such as:

- dominant subject;
- secondary subject;
- number of major objects;
- viewpoint;
- camera height;
- camera direction;
- spatial relationship;
- foreground/background allocation;
- environment;
- human presence;
- palette;
- lighting;
- rendering language;
- density;
- recto-verso relationship.

Do not demand arbitrary numerical precision. Precision is valuable when it stabilizes a variable that materially affects the result.

## Finding structure

Every finding must be independently reviewable by the user.

Each finding must explain:

- what was detected;
- which lexical, structural, or semantic proxies led to inspection;
- confidence in those proxies;
- possible false positives;
- possible false negatives;
- what underlying specification problem the passage may reveal;
- why the issue matters;
- what questions a reviewer should ask;
- one or more actionable resolution options;
- the recommended option;
- the expected effect on specification quality;
- the exact proposal locations involved.

The user will later fill in `decision` and `note`.

Do not fill those fields during analysis.

## Detector families

The following detector families are points of attention, not banlists.

### 1. Unresolved alternatives

#### Detector proxies

Search for formulations such as:

- `or`
- `either`
- `and/or`
- `alternatively`
- `option`
- `one of`
- slash alternatives such as `bridge/viaduct`
- parallel formulations offering different visible subjects, environments, viewpoints, or compositions

Confidence:

- high when the alternatives change a dominant subject, camera, environment, count, or composition;
- medium when they change a secondary element;
- low when the construction occurs in conceptual prose, exclusions, comparisons, or exhaustive definitions.

False positives:

- legitimate conceptual distinctions;
- mutually exclusive prohibitions;
- prose explaining why one selected option was chosen over another;
- harmless implementation flexibility outside the visible composition.

False negatives:

- alternatives expressed in separate sentences without an explicit `or`;
- multiple examples presented as if all were valid scene choices;
- vague nouns that implicitly leave several interpretations open.

#### What it reveals

The proposal may be delegating an art-direction decision to the generation model.

#### Questions to ask

- Are both alternatives genuinely permitted in the final design?
- Would different runs plausibly choose different branches?
- Does the choice materially affect silhouette, density, viewpoint, symbolism, or series coherence?
- Can one branch be selected now?

#### Typical resolutions

- select one alternative;
- split conceptual scope from concrete representation;
- move rejected alternatives into rationale or changelog;
- keep the alternative only if variability is intentional and harmless.

### 2. Soft optionality

#### Detector proxies

Search for:

- `may`
- `might`
- `could`
- `perhaps`
- `possibly`
- `optionally`
- `if desired`
- `where appropriate`
- `as needed`
- `can include`
- `may appear`

Confidence rises when the optional element affects composition or identity.

#### What it reveals

A visible decision may not actually have been made.

#### Questions to ask

- If this element appears in half the generations and disappears in the other half, is that acceptable?
- Is the element important enough to specify?
- If it is not important, should it be removed from the proposal entirely?

#### Typical resolutions

- make the element required;
- remove it;
- define a narrow condition under which it appears;
- demote it from image specification to conceptual rationale.

### 3. Weak preference instead of decision

#### Detector proxies

Search for:

- `prefer`
- `preferably`
- `ideally`
- `should generally`
- `usually`
- `tend to`
- `roughly`
- `approximately` when the relevant variable could be concretely fixed
- `typically`

#### What it reveals

The proposal may know what it wants but still phrase the requirement as advice.

#### Questions to ask

- Is this genuinely a preference?
- What failure is permitted if the preference is ignored?
- Would a fixed requirement improve consistency without becoming brittle?

#### Typical resolutions

- convert to a direct requirement;
- define an allowed range;
- retain as preference only when variation is useful.

### 4. Negative sediment

#### Detector proxies

Search for:

- `do not`
- `don't`
- `must not`
- `never`
- `avoid`
- `exclude`
- `is not`
- `not X but Y`
- `rather than`
- `instead of`
- `without becoming`
- repeated negative clauses near one another

Also count negative-instruction density by section.

#### What it reveals

The proposal may be preserving the history of past failures instead of integrating those failures into a stronger positive target definition.

#### Questions to ask

For every negative instruction:

- Is the prohibited behavior plausible?
- Is it materially harmful?
- Is the prohibition specific enough that compliance can be judged?
- Is it already made unnecessary by a positive requirement?
- Can the underlying intent be expressed more directly as a target or invariant?

#### Good negative instructions

Keep negative instructions when they are specific, actionable, non-redundant, and externally distinguishable.

Examples:

- no outer presentation margin;
- exactly two secondary dishes, no additional dishes;
- no realistic human faces;
- no generated pseudo-lettering.

#### Weak negative instructions

Flag broad or inactionable formulations such as:

- do not make it generic;
- avoid clutter;
- avoid excessive detail;
- do not make it too futuristic;
- do not overdo the effect.

#### Typical resolutions

- replace with a positive compositional requirement;
- consolidate several prohibitions into one invariant;
- remove redundant prohibition;
- retain a precise interdiction when it covers a real recurrent failure not fully excluded by the positive specification.

### 5. Broad or untestable negation

#### Detector proxies

Search negative clauses containing vague evaluative words such as:

- generic
- excessive
- too much
- overdone
- chaotic
- cluttered
- boring
- unrealistic
- arbitrary
- awkward
- bad
- inappropriate

#### What it reveals

The proposal identifies an undesired quality without specifying the observable condition that would prevent it.

#### Questions to ask

- What concrete feature would make the result non-generic or non-cluttered?
- Can hierarchy, object count, density, camera, or palette be specified instead?

#### Typical resolutions

Replace the vague interdiction with positive observable requirements.

### 6. Contrastive over-definition

#### Detector proxies

Search for repeated:

- `not X but Y`
- `rather than`
- `instead of`
- `does not`
- `is not`
- `without`
- long passages defining the proposal primarily against neighboring styles or concepts

#### What it reveals

The target may be described through exclusions more strongly than through its own construction.

#### Questions to ask

- Does Y already have a strong positive definition?
- Is the contrast necessary for conceptual understanding?
- Is the passage carrying historical debate that belongs in rationale or changelog rather than final specification?

#### Typical resolutions

- state the target directly;
- retain one contrast where it genuinely clarifies a boundary;
- move discarded alternatives out of executable prompt text.

### 7. Enumeration pressure

#### Detector proxies

Search for:

- long comma-separated noun lists;
- `includes`
- `including`
- `such as`
- `for example`
- `among`
- `features`
- colon followed by many items;
- several semicolon-separated visual elements.

Confidence rises in final scene descriptions and prompts.

#### What it reveals

Conceptual completeness may be leaking into visual composition.

#### Questions to ask

- Are all listed items supposed to be visible?
- Which item is dominant?
- Which one is secondary?
- Which items merely explain the broader concept and should stay out of the image?

#### Typical resolutions

- introduce an explicit representation channel;
- select one dominant subject and at most the necessary secondary elements;
- move taxonomy lists back into rationale.

### 8. Additive instruction accumulation

#### Detector proxies

Count verbs such as:

- `include`
- `add`
- `show`
- `feature`
- `contain`
- `incorporate`
- `integrate`
- `combine`
- `connect`
- `surround`
- `populate`

Flag unusual clusters within one scene specification.

#### What it reveals

The prompt may have been built by accretion, with each revision adding another object.

#### Questions to ask

- Does every added element have a distinct visual function?
- Has the scene acquired more subjects than its hierarchy can support?
- Can several additions be removed because the main scene already expresses the concept?

#### Typical resolutions

- delete low-value additions;
- subordinate secondary elements explicitly;
- replace additive lists with a spatial composition rule.

### 9. Missing or weak representation channel

#### Detector proxies

Look for broad denomination concepts such as:

- infrastructure
- communication
- mobility
- interpretation
- environment
- future
- information
- knowledge
- stewardship
- trust
- continuity

Then inspect whether the proposal explicitly selects a concrete representation channel.

#### What it reveals

The proposal may ask the image to illustrate an abstract category directly.

#### Questions to ask

Can the denomination be expressed as:

`Concept → representation channel → concrete scene`

For example:

`Mobility → rail → curved rail bridge`

#### Typical resolutions

Add a single explicit representation channel and ensure recto and verso derive from it.

### 10. Abstract visual nouns and placeholder architecture

#### Detector proxies

Search for nouns such as:

- system
- complex
- hub
- campus
- facility
- center / centre
- network
- environment
- institution
- forum
- exchange
- landscape
- infrastructure

These words are not inherently bad. Flag them when they substitute for a sketchable physical scene.

#### What it reveals

A phrase may sound concrete while leaving the model to invent the actual architecture.

#### Questions to ask

- Could a designer sketch the dominant geometry from this sentence alone?
- What is the largest visible object?
- What identifies the place at thumbnail scale?
- Is the noun merely a conceptual label?

#### Typical resolutions

Replace placeholder language with concrete structures, spatial relations, and counts.

### 11. Concept leakage into executable prompts

#### Detector proxies

Search final prompts for:

- `represents`
- `symbolizes`
- `expresses`
- `suggests`
- `embodies`
- `evokes`
- `communicates`
- `implies`
- `gives a sense of`
- `creates a feeling of`

#### What it reveals

The prompt may be asking the generation model to solve conceptual interpretation instead of executing visual direction.

#### Questions to ask

- What visible object, geometry, lighting, crop, or spatial relationship should create this meaning?
- Can the conceptual statement remain in rationale while the prompt becomes concrete?

#### Typical resolutions

Translate the intended meaning into visible construction.

### 12. Unspecified hierarchy

#### Detector proxies

Inspect scene descriptions containing many concrete nouns but little or no hierarchy language such as:

- dominant
- primary
- secondary
- subordinate
- background
- foreground
- largest
- central
- occupies
- cropped
- distant
- supporting

A missing keyword is not itself a violation. Judge the actual hierarchy.

#### What it reveals

The model knows what objects exist but not which one matters most.

#### Questions to ask

- What survives thumbnail reduction?
- What is the principal noun of the scene?
- What is the maximum number of secondary elements?
- Which details exist only for close reading?

#### Typical resolutions

State one dominant element or one dominant organizing landscape, then rank all other visible content.

### 13. Unspecified cardinality

#### Detector proxies

Search important plurals with no count:

- dishes
- towers
- buildings
- figures
- vehicles
- paths
- bridges
- turbines
- screens
- antennas
- trees
- structures

#### What it reveals

Independent generations may invent materially different density.

#### Questions to ask

- Does the number affect silhouette, balance, or complexity?
- If yes, can it be fixed?
- If no, is the plural detail too minor to specify?

#### Typical resolutions

- specify an exact count;
- specify a narrow range only when variation is intentional;
- remove the element from the prompt if its count is irrelevant.

### 14. Unspecified camera or viewpoint

#### Detector proxies

Check whether final scene descriptions specify:

- eye level;
- low angle;
- high angle;
- elevated;
- frontal;
- rear view;
- three-quarter;
- oblique;
- overhead;
- camera direction;
- crop.

Also flag vague phrases such as `dynamic view`, `cinematic angle`, `interesting perspective`.

#### What it reveals

Independent images may acquire incompatible spatial grammars.

#### Questions to ask

- Is camera height part of recto-verso logic?
- Is camera direction essential to the dominant silhouette?
- Would a different viewpoint change the scene's meaning?

#### Typical resolutions

Fix camera height, orientation, and major crop.

### 15. Camera or spatial alternatives

#### Detector proxies

Search phrases such as:

- `low or elevated`
- `front or side`
- `rear or middle`
- `river or valley`
- `foreground or middle distance`
- `diagonally or laterally`

#### What it reveals

A major compositional choice remains unresolved.

#### Typical resolution

Select one.

### 16. Relational vagueness

#### Detector proxies

Search:

- `near`
- `around`
- `beside`
- `somewhere`
- `toward`
- `in the distance`
- `surrounded by`
- `connected to`
- `integrated with`
- `flows into`
- `links to`
- `transitions into`

#### What it reveals

Objects are conceptually related but geometrically under-specified.

#### Questions to ask

- Can the relationship be seen?
- Through what exact spatial mechanism?
- Should the object be left/right, foreground/background, crossing the frame, touching an edge, or aligned on a datum?

#### Typical resolutions

Specify visible geometry where it materially affects composition.

### 17. Unbounded relative modifiers

#### Detector proxies

Search:

- large
- small
- broad
- narrow
- subtle
- restrained
- limited
- few
- several
- sparse
- dense
- prominent
- substantial
- modest

#### What it reveals

Relative language can be sufficient, or it can hide unstable scale and density.

#### Questions to ask

- Is the relation clear from context?
- Does variation materially affect the scene?
- Would approximate occupancy, count, or rank stabilize it?

#### Typical resolutions

Keep useful relational terms; quantify or rank only high-leverage variables.

### 18. Style adjectives without construction

#### Detector proxies

Search:

- clean
- modern
- optimistic
- elegant
- institutional
- sophisticated
- dynamic
- premium
- serious
- calm
- futuristic
- civic
- refined

#### What it reveals

Mood may be named without specifying how it is visually produced.

#### Questions to ask

Which concrete choices create the style:

- materials?
- lighting?
- surface finish?
- edge behavior?
- geometry?
- density?
- saturation?
- texture?
- depth?

#### Typical resolutions

Translate mood words into visual properties while retaining the adjective only if it remains useful as a summary.

### 19. Rendering ambiguity or mixed rendering vocabularies

#### Detector proxies

Search combinations of:

- photorealistic
- realistic
- stylized
- illustrative
- architectural render
- engraved
- intaglio
- vector
- painterly
- halftone
- 3D render
- matte
- glossy
- cinematic

#### What it reveals

The proposal may contain incompatible or under-defined rendering languages.

#### Questions to ask

- Is the hybrid intentional?
- Which visual subsystem gets which treatment?
- Are edge behavior, texture, lighting, and surface finish defined consistently?

#### Typical resolutions

Define the rendering system by assigned roles instead of stacking style labels.

### 20. Recto-verso duplication

#### Detector proxies

Compare recto and verso descriptions for the same denomination.

Flag when:

- the same dominant noun appears on both sides;
- the verso is primarily the recto with more objects;
- both sides use nearly identical camera height and spatial structure;
- the only difference is scale or detail density without a new conceptual role.

#### What it reveals

The reverse may be “recto plus more” instead of revealing a qualitatively different system.

#### Questions to ask

- What does turning the note reveal that the recto cannot?
- Does the verso change scale, viewpoint, mechanism, spatial logic, or institutional depth?
- Is the reverse a genuine answer to the recto?

#### Typical resolutions

Redefine the verso around the broader system, backstage mechanism, production system, network, or supporting infrastructure.

### 21. Cross-denomination sameness

#### Detector proxies

Compare scene structures across denominations.

Flag repeated patterns such as:

- six campuses;
- six elevated landscapes;
- six central halls;
- six bridges;
- six generic civic complexes;
- identical object counts and camera logic where distinction is expected.

#### What it reveals

Series coherence may have collapsed into interchangeable imagery.

#### Questions to ask

- Is the repetition intentional series grammar or accidental scene reuse?
- Can each note be recognized by silhouette in grayscale?

### 22. Cross-denomination rendering drift

#### Detector proxies

Compare rendering instructions across denomination chapters and prompts.

Look for inconsistent:

- lighting;
- saturation;
- edge treatment;
- texture sharpness;
- material finish;
- depth;
- line treatment;
- amount of detail;
- human treatment.

#### What it reveals

Separately generated images may no longer read as one series.

#### Typical resolutions

Lift stable rendering rules into a common series invariant and remove conflicting local instructions.

### 23. Stale concept residue

#### Detector proxies

Build a canonical record for each denomination:

- concept;
- representation channel;
- recto dominant subject;
- recto camera;
- verso dominant subject;
- verso camera;
- palette;
- grayscale silhouette;
- border motif;
- security-ready motif.

Then search the entire proposal for conflicting older terminology or imagery.

#### What it reveals

A revision changed the main scene but left old assumptions elsewhere.

#### Questions to ask

- Does every summary, table, accessibility rule, border, watermark, continuity section, and prompt describe the current design?
- Is an old scene still influencing downstream requirements?

#### Typical resolutions

Update or remove stale references. Prefer one canonical design record as the source of truth.

### 24. Cross-section contradiction

#### Detector proxies

Compare repeated facts and design decisions across:

- executive summary;
- denomination table;
- narrative sections;
- scene descriptions;
- prompt sections;
- accessibility;
- continuity;
- security;
- evaluation summary;
- appendices.

#### What it reveals

The proposal has multiple inconsistent sources of truth.

#### Typical resolutions

Select the canonical decision, update all derived descriptions, and eliminate contradictory wording.

### 25. Duplicated rules and local sediment

#### Detector proxies

Search exact and near-duplicate sentences, repeated prohibitions, and repeated style instructions.

#### What it reveals

A series-wide invariant may have been copied into many local prompts, creating maintenance risk and context bloat.

#### Questions to ask

- Does the local repetition add denomination-specific meaning?
- Could one common rule govern all scenes?

#### Typical resolutions

Centralize genuine invariants. Keep local repetition only when downstream generation requires explicit restatement.

When the proposal itself is meant to feed independent generation prompts, distinguish document-level duplication from deliberate prompt-level restatement.

### 26. Repeated exception handling

#### Detector proxies

Search:

- except
- unless
- however
- but
- with the exception of
- special case
- only for

especially when clustered around one general rule.

#### What it reveals

The general abstraction may be wrong.

#### Questions to ask

- Can a better rule naturally include the exception?
- Is the exception actually a meaningful denomination-specific design choice?

### 27. False precision

#### Detector proxies

Inspect exact percentages, counts, dimensions, and ratios.

#### What it reveals

The proposal may spend precision on variables that do not materially stabilize the result.

#### Questions to ask

- Would changing this number within a small range alter the design?
- Is the number derived from a real constraint?
- Is it enforceable downstream?

#### Typical resolutions

Keep meaningful precision; simplify decorative precision.

### 28. Missing precision in high-leverage variables

#### Detector proxies

The inverse of false precision.

Compare how much detail is spent on minor ornament versus:

- protagonist;
- count;
- camera;
- spatial relationship;
- silhouette;
- palette;
- rendering;
- human presence.

#### What it reveals

The specification is precise in low-value places and vague where variation matters.

#### Typical resolutions

Move the precision budget toward high-leverage scene decisions.

### 29. Workflow leakage into proposal

#### Detector proxies

Search proposal prose for:

- filenames;
- generation order;
- tool names;
- layer assembly;
- reference-image mechanics;
- retries;
- seeds;
- model-specific behavior;
- temporary production instructions.

#### What it reveals

Jury-facing or concept-facing material has absorbed implementation details.

#### Typical resolutions

Move operational material into workflow documentation unless it is itself part of the design specification.

### 30. Proposal leakage into reusable workflow

When a reusable workflow is also supplied, search it for project-specific:

- titles;
- motifs;
- named materials;
- named scenes;
- palettes;
- aesthetic references;
- denomination-specific examples.

#### What it reveals

The workflow has duplicated proposal truth and become non-reusable.

#### Typical resolutions

Replace project-specific content with instructions to extract the relevant invariant from the proposal.

### 31. Negative-to-positive refactor opportunity

This is a derived review, not a lexical hit.

For every meaningful negative instruction, attempt a positive rewrite.

Compare:

- clarity;
- generativity;
- specificity;
- redundancy;
- enforceability.

If the positive requirement fully subsumes the prohibition, propose replacing it.

If the prohibition still blocks a plausible harmful behavior not excluded by the positive target, retain it.

### 32. Choice-budget overload

For each final scene, enumerate unresolved high-leverage choices:

- dominant subject;
- secondary subject;
- count;
- camera;
- environment;
- composition;
- figures;
- lighting;
- palette;
- rendering.

Do not require all variables to be fixed.

Flag scenes where several consequential variables remain simultaneously open.

#### What it reveals

The “prompt” may actually describe a family of possible images.

### 33. Noun-hierarchy overload

Extract concrete visible nouns from each final scene.

Inspect:

- count;
- repetition;
- explicit ranking;
- spatial organization.

Flag scenes with many concrete nouns but no clear visual hierarchy.

### 34. Normative polarity

Estimate by section:

- positive requirements;
- negative restrictions.

Do not score quality mechanically.

Flag sections where the proposal describes exclusions much more extensively than the target.

Explain whether the imbalance appears justified.

### 35. Resolution symmetry

Compare equivalent denomination sections.

Flag when one denomination is substantially less resolved than its peers in:

- representation channel;
- subject;
- count;
- camera;
- spatial structure;
- figures;
- palette;
- rendering;
- recto-verso distinction.

The objective is not identical structure. The objective is comparable decisiveness.

## Macro questions

In addition to detector-specific checks, ask:

1. Can every final scene be sketched without inventing its protagonist?
2. Can every scene be identified at thumbnail scale?
3. Does each denomination have an explicit representation channel?
4. Does every recto and verso have a qualitatively distinct role?
5. Are camera choices deliberate?
6. Are visible object counts stable where they affect density?
7. Are rendering rules shared unless a difference is intentional?
8. Does the proposal define the desired target more strongly than the history of rejected alternatives?
9. Are negative instructions mostly specific, actionable, and testable?
10. Are rationale sections broad while executable prompts are concrete?
11. Does each prompt read as one resolved production specification rather than a menu?
12. Has revision left stale terminology elsewhere?
13. Are common invariants centralized while denomination-specific decisions remain local?
14. Are there places where multiple local corrections point to one missing abstraction?

## Priority

Assign:

- `high`: likely to cause materially different outputs, contradictory instructions, or major series drift;
- `medium`: meaningful ambiguity or prompt-quality problem requiring judgment;
- `low`: plausible smell with limited downstream effect.

Priority reflects review value, not detector confidence.

## Confidence

Assign detector confidence separately:

- `high`: strong evidence that the observed construction correlates with the diagnosed problem;
- `medium`: plausible signal requiring contextual review;
- `low`: weak lexical or structural signal worth surfacing because the consequence could still matter.

Always describe false-positive and false-negative risks.

## Options

Every finding must offer at least one actionable option.

Use multiple options when there are genuinely different reasonable strategies.

Examples:

- select one alternative;
- remove the unstable clause;
- replace a negative instruction with a positive invariant;
- consolidate several negatives into one rule;
- add a representation channel;
- fix an exact count;
- specify camera height and direction;
- rewrite a placeholder noun into concrete architecture;
- remove low-value objects;
- move conceptual explanation out of the prompt;
- synchronize stale references;
- centralize a duplicated invariant;
- leave unchanged when the ambiguity is intentional.

Options are proposals, not commands.

The user remains free to select an option, reject the finding, defer it, or provide a custom natural-language instruction.

## Location

Every finding must be easy to locate.

Provide:

- file;
- section or subsection;
- short unique anchor;
- related locations when the issue spans multiple sections.

Do not rely on line numbers alone.

## Summary

The YAML begins with a summary containing:

- total findings;
- counts by category;
- counts by priority;
- counts by detector confidence;
- number of prompts or scene specifications reviewed;
- number of scenes with unresolved high-leverage choice overload;
- approximate positive versus negative instruction counts;
- general observations.

These metrics are diagnostic only.

Do not convert them into a quality score.

## Human decisions

Every finding contains:

```yaml
decision:
note:
```

Both remain null during analysis.

The user may later write:

```yaml
decision: A
```

or:

```yaml
decision: reject
```

or:

```yaml
decision: defer
```

or:

```yaml
decision: custom
note: >
  Keep the negative instruction, but replace the vague phrase
  "avoid clutter" with a rule limiting the scene to one dominant
  object and two subordinate objects.
```

## Output

Write only the lint review YAML requested by the user.

It must conform exactly to `proposal-lint.schema.yaml`.

Do not modify the proposal in this phase.
