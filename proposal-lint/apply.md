# Proposal lint application

## Role

Apply the human decisions recorded in a completed proposal lint review YAML.

This step is execution only.

The analysis phase has already occurred.

Do not search for new proposal smells.

Do not apply recommendations that the user did not explicitly approve.

## Inputs

Use:

- the proposal that was linted;
- the completed lint review YAML;
- the lint schema when needed to interpret fields.

## Source of authority

For each finding, use this priority order:

1. `decision`
2. `note`
3. selected option
4. original finding description
5. original proposal context

Human decisions and notes override the analysis recommendation.

## Decision interpretation

### Selected option

Example:

```yaml
decision: A
```

Apply option `A`.

Interpret `note` as a natural-language refinement, constraint, correction, or partial override of that option.

### Reject

```yaml
decision: reject
```

Make no change for that finding.

### Defer

```yaml
decision: defer
```

Make no change for that finding.

### Undecided

```yaml
decision: null
```

Make no change.

Do not infer approval from `recommendation`.

### Custom

```yaml
decision: custom
note: >
  ...
```

Apply only the instruction expressed in `note`.

If the custom note intentionally resolves the issue differently from every proposed option, follow the note.

Do not invent missing intent.

## Scope discipline

Modify only content materially required by approved findings.

Do not perform opportunistic cleanup.

Do not fix newly noticed smells.

Do not silently normalize neighboring text unless necessary for grammatical, structural, or semantic coherence after an approved edit.

A future lint cycle can review remaining issues.

## Application principles

When resolving an approved finding:

- preserve the proposal's core concept;
- preserve user-authored design decisions;
- preserve terminology unless the selected decision changes it;
- preserve deliberate ambiguity when the decision explicitly keeps it;
- preserve conceptual nuance in rationale sections;
- increase determinism in executable scene descriptions only where approved;
- keep useful, specific, actionable prohibitions;
- prefer positive target definitions when the selected decision calls for a negative-to-positive refactor;
- avoid replacing one vague formulation with another;
- synchronize dependent references only when the approved finding explicitly concerns stale residue or contradiction, or when synchronization is strictly necessary to keep the proposal internally consistent.

## Applying alternatives

When an approved finding selects one branch among alternatives:

- remove the rejected branch from executable specification;
- preserve discarded alternatives only if the selected option explicitly moves them to rationale, history, or changelog;
- ensure downstream references use the selected branch consistently.

## Applying negative-instruction refactors

When an approved finding replaces a negation:

- identify the positive invariant or target behavior selected by the user;
- rewrite the relevant passage around that target;
- keep the original prohibition only if the selected option explicitly retains it or if it remains necessary to block a distinct, specific, plausible failure;
- do not accumulate both formulations redundantly.

## Applying hierarchy fixes

When an approved finding resolves visual hierarchy:

- state the dominant element explicitly;
- state secondary elements and counts where selected;
- demote or remove other content as specified;
- ensure scene prompts reflect the same hierarchy.

## Applying camera fixes

When an approved finding specifies camera or viewpoint:

- update all affected scene descriptions and final prompts;
- preserve series-wide camera grammar;
- remove conflicting viewpoint language.

## Applying representation-channel fixes

When an approved finding establishes:

`Concept → representation channel → concrete scene`

propagate that decision only to sections that materially restate the denomination's visual logic.

Do not rewrite unrelated conceptual sections.

## Applying stale-residue or contradiction fixes

For an approved cross-section consistency finding:

- identify the canonical decision specified by the selected option or note;
- update every listed related location;
- remove terminology belonging to superseded concepts;
- verify tables, prompts, accessibility descriptions, border logic, security-ready motifs, continuity summaries, and evaluation summaries only when they are listed or necessarily affected.

## Applied field

After successfully applying a selected or custom decision:

```yaml
applied: true
```

For:

- reject;
- defer;
- null;
- impossible-to-apply decisions;

leave:

```yaml
applied: false
```

Do not change `decision`, `note`, `recommendation`, detector evidence, or option text.

## Failure handling

If an approved decision cannot be applied because required source content is missing or the instruction is internally impossible:

- do not improvise a substitute;
- leave `applied: false`;
- report the finding ID and reason at the end.

## Validation after edits

After applying all approved findings:

1. confirm no unapproved finding was applied;
2. confirm selected alternatives are consistent in all affected locations;
3. confirm no approved negative-to-positive refactor accidentally retained redundant sediment;
4. confirm scene prompts remain concrete and grammatical;
5. confirm proposal structure remains valid;
6. confirm changelog or version information is updated only if requested by an approved finding or by the user's application request.

Do not run a new lint analysis.

## Output

Modify the proposal directly.

Update only the `applied` fields in the lint YAML.

At the end, report briefly:

- number of findings applied;
- files modified;
- approved findings that could not be applied;
- rejected findings;
- deferred findings;
- undecided findings.

Do not include new recommendations.
