# Evaluation plan

This document specifies planned evaluation, not collected labels or measured performance.
Corpus-scale analysis does not replace human validation.
Project-level findings require project context.
See [collection](COLLECTION.md) and [storage](STORAGE.md) for provenance and record handling.

### Layer B: development pilot

Use 60 theorem families with two proof variants each to develop rules and annotation guidance.
All 60 families are development data, not the final held-out test set.
Start with ten families to estimate annotation hours and extraction feasibility.
Record Lean experience, annotation time, disagreement, and collection cost.
Use pilot results to set a feasible budget before freezing final evaluation.

A merged change is a weak signal, not proof that every quality dimension improves.
Exclude API-renaming and toolchain-only changes from same-environment refactoring comparisons.
Retain review rationale and check both variants in a common environment when feasible.
Label pairs requiring different environments separately.
Do not label AI-generated proofs as negative solely because of their origin.
Do not infer human authorship from an early timestamp alone.

### Layer C: independent final evaluation

Target 300 to 1,000 finding-level judgments across at least 100 held-out theorem families.
Separately target at least 300 proof-comparison pairs from at least 300 held-out families.
A family can support both tasks, but it contributes only once to family-level coverage counts.
This design proposes human-evaluation targets, not collected dataset counts.
Exclude all development-pilot families and their near duplicates.

Stratify sampling by subject, proof length, proof form, and source category.
Include logic, induction, algebraic reasoning, and set or function reasoning.
Include simple, long, automated, and structured proofs.
Record sampling probabilities and report results by stratum.
Separate population-weighted estimates from deliberately enriched hard-case evaluation.

Estimate annotation hours from the pilot before committing to final sample sizes.
If resources cannot meet these targets, revise the scope before evaluating test labels.
Publish achieved counts and limitations instead of claiming the original release targets passed.
Sparse rules with insufficient findings remain inconclusive.

### Annotation protocol

Obtain two independent ratings per pair or finding.
Use a third rating to resolve disagreement, or retain the item as disputed.
Compare readability and modularity separately and permit ties or insufficient context.
Hide author identity, provenance category, and model name during rating.
Display relevant definitions, helpers, and module context to both raters.
Train raters on development examples and randomize variant order.

Report agreement before adjudication and preserve original judgments.
Collect finding-level labels separately from pairwise preferences.
Ask whether the pattern exists, whether the warning fits the context, and whether its proposed action is useful.
Precision measures warnings that both detect a real pattern and justify the stated interpretation.
Report action usefulness separately.
Retain ties, insufficient context, and unresolved disputes as separate categories.

Exclude unresolved labels from adjudicated precision but report their share of all emitted findings.
Also report a conservative estimate that counts unresolved findings as failures.
Project-level structural warnings need module or project context, not isolated proof snippets.
Report these judgments separately from theorem-level judgments.
Do not infer project maintainability solely from an average of proof ratings.

### Provenance and split controls

For each example, record repository, commit, file, declaration, license, and required context.
Record source history, attribution evidence, toolchain, dependencies, verification result, annotation rationale, and uncertainty.
Keep synthetic degradations separate from naturally occurring examples.
Check redistribution rights before publishing source code in a dataset.
If natural pairs are scarce, use curated variants and report them separately.
Do not present synthetic changes as naturally observed preferences.

Define a family by the mathematical claim and proof strategy, including renamed or generalized variants.
Keep variants, near duplicates, and duplicated fork content in the same split.
Audit normalized statement matches and shared proof fragments for possible duplicates.
Record manual grouping decisions before splitting.
Group direct proof-revealing dependencies, not all shared foundational imports.
Reserve independent projects or module clusters for cross-project generalization checks where feasible.

A single Mathlib snapshot cannot establish generalization to arbitrary Lean projects.
Report theorem-family, module-cluster, and project separation separately.
Distinguish unknown model pretraining exposure from development-set leakage.
Treat model evaluation on public proofs as potentially contaminated.
Freeze sampling manifests and thresholds before final evaluation.
Do not use final test labels to adjust rules or thresholds.


## Acceptance targets

This design proposes release gates, not measured results.

- At least 90% of the curated supported declarations produce a report without extraction errors.
- Repeated analysis produces identical structural fields under a fixed environment.
- Resource measurements do not belong to the deterministic field set.
- The repeated-fragment heuristic targets at least 80% precision on adjudicated held-out findings.
- Target 300 to 1,000 held-out finding judgments across at least 100 theorem families.
- Require at least 100 findings across 30 held-out families to assess an individual heuristic.
- Target at least 300 held-out comparison pairs across at least 300 families for human-preference evaluation.
- Report insufficient evidence if the test set does not meet these denominators.
- Freeze eligibility rules before evaluation.
- Report corpus-scale coverage against all inventoried modules and declarations and the supported subset separately.
- Report maintainer-repository discovery, collection, exclusions, failures, and deduplication separately.
- State achieved final annotation counts and any departure from the frozen targets.
- Report per-rule denominators, disputed findings, and unresolved context limits.
- Report uncertainty intervals with resampling at the theorem-family level.
- Compare the analyzer against existing lint and length-only baselines on the same labeled tasks.
- Use existing lint findings unchanged for the lint baseline.
- Rank variants by token count for the length baseline and permit equal-length ties.
- Report paired human preferences without claiming that disagreement proves the analyzer wrong or right.

The following additional gates apply only to the optional refactoring extension:

- Every fixture with a changed statement, prohibited axiom, or original-target shortcut fails candidate verification.
- Every valid helper-extraction fixture within the declared supported subset passes the specified candidate checks.
- Fixtures cover indirect placeholders, universe changes, added hypotheses, environment mutation, shortcuts, tampered artifacts, and resource exhaustion.
- Passing these fixtures establishes only the tested cases, not a universal security or verification guarantee.
- No candidate path changes the user's source files or sends remote data without explicit permission.

The development pilot cannot establish final performance, universal beauty, or broad generalization.
Large unlabeled corpora do not replace independent human evaluation.
Do not use its scores for student grades.
Expand evaluation before making claims about maintenance outcomes or unseen mathematical domains.
